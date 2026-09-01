"""Classify syllabus tables and derive wrap-aware widths from their content."""

# Standard Library
import re
import html
import math
import collections
import xml.etree.ElementTree
from dataclasses import dataclass

# PIP3 modules
import markdown
import markdown.util
import markdown.extensions
import markdown.treeprocessors


# These bounds are renderer-independent typography heuristics, not table-specific widths.
# They let prose request useful space without allowing one URL or identifier to dominate.
MINIMUM_COLUMN_DEMAND = 4
MAXIMUM_COLUMN_DEMAND = 44
MAXIMUM_WORD_DEMAND = 24
HEADER_WRAP_FACTOR = 6
BODY_WRAP_FACTOR = 12
COMPACT_WRAP_FACTOR = 3
CELL_HORIZONTAL_ALLOWANCE = 3
COMPACT_CELL_HORIZONTAL_ALLOWANCE = 2
COMPACT_COLUMN_TEXT_LIMIT = 12
COMPACT_TABLE_CHARACTER_LIMIT = 32
FLEXIBLE_COLUMN_GROWTH_FACTOR = 1.25
MAXIMUM_GROWING_SCHEDULE_COLUMNS = 2
HTML_PLACEHOLDER_PATTERN = re.compile(markdown.util.HTML_PLACEHOLDER % r"([0-9]+)")
HTML_TAG_PATTERN = re.compile(r"<[^>]+>")
STAGED_SCHEDULE_HEADERS = ("Wk", "Date", "Stage", "Topic", "In class", "Work due")
STAGED_SCHEDULE_DATE_DEMAND = 7
SCHEDULE_STAGE_KEYS = {
	"Course foundations": "foundations",
	"Individual project": "individual",
	"Group project": "group",
}


@dataclass(frozen=True)
class TableLayout:
	"""One content-derived layout shared by HTML, PDF, DOCX, and audit tools."""

	profile: str
	column_demands: tuple[int, ...]
	column_percentages: tuple[int, ...]
	compact_columns: tuple[bool, ...]
	minimum_width_ch: int
	is_compact: bool


#============================================
def restore_stashed_html_text(
	text: str,
	raw_html_blocks: tuple[str | xml.etree.ElementTree.Element, ...],
) -> str:
	"""Replace Markdown's raw-HTML placeholders with their visible text."""
	def replace_placeholder(match: re.Match[str]) -> str:
		block_index = int(match.group(1))
		if block_index >= len(raw_html_blocks):
			return ""
		raw_block = raw_html_blocks[block_index]
		if isinstance(raw_block, str):
			raw_text = raw_block
		else:
			raw_text = xml.etree.ElementTree.tostring(raw_block, encoding="unicode")
		restored = HTML_PLACEHOLDER_PATTERN.sub(replace_placeholder, raw_text)
		visible_text = HTML_TAG_PATTERN.sub(" ", restored)
		return visible_text

	restored_text = HTML_PLACEHOLDER_PATTERN.sub(replace_placeholder, text)
	return restored_text


#============================================
def normalize_cell_text(
	element: xml.etree.ElementTree.Element,
	raw_html_blocks: tuple[str | xml.etree.ElementTree.Element, ...] = (),
) -> str:
	"""Return one table cell as normalized visible text."""
	text = "".join(element.itertext())
	restored = restore_stashed_html_text(text, raw_html_blocks)
	normalized = " ".join(html.unescape(restored).split())
	return normalized


#============================================
def table_headers(
	element: xml.etree.ElementTree.Element,
	raw_html_blocks: tuple[str | xml.etree.ElementTree.Element, ...] = (),
) -> tuple[str, ...]:
	"""Return the first semantic header row from one HTML table element."""
	header_row = element.find("./thead/tr")
	if header_row is None:
		return ()
	headers = tuple(
		normalize_cell_text(cell, raw_html_blocks)
		for cell in header_row.findall("th")
	)
	return headers


#============================================
def table_body_rows(
	element: xml.etree.ElementTree.Element,
	raw_html_blocks: tuple[str | xml.etree.ElementTree.Element, ...] = (),
) -> tuple[tuple[str, ...], ...]:
	"""Return normalized visible text from every table body row."""
	rows = []
	for row in element.findall("./tbody/tr"):
		cells = tuple(
			normalize_cell_text(cell, raw_html_blocks)
			for cell in row.findall("td")
		)
		rows.append(cells)
	return tuple(rows)


#============================================
def classify_table_headers(headers: tuple[str, ...]) -> str:
	"""Map stable student-facing headers to one column-sizing profile."""
	if headers == ("Assessment", "Possible points", "Approximate share", "Your points"):
		return "point-plan"
	if len(headers) == 4 and headers[:3] == ("Week", "Date", "Topic"):
		return "schedule"
	if len(headers) == 5 and headers[:4] == ("Week", "Date", "Topic", "Quiz"):
		return "schedule"
	if headers == STAGED_SCHEDULE_HEADERS:
		return "schedule"
	if headers == ("Date", "Event", "Type"):
		return "important-dates"
	if headers == ("Required work", "What is expected", "Points"):
		return "project-points"
	if headers == ("Points", "Standard", "Evidence in the work"):
		return "rubric"
	if headers == ("Absence type", "Score", "Included in total points"):
		return "attendance"
	if headers == ("Percentage", "Grade"):
		return "grade-scale"
	if len(headers) == 2 and headers[0] in ("Course summary", "Field"):
		return "key-value"
	header_text = " | ".join(headers)
	raise ValueError(f"Unregistered syllabus table headers: {header_text}")


#============================================
def text_width_demand(text: str, wrap_factor: int) -> int:
	"""Estimate a readable line length without rewarding long prose linearly."""
	normalized = " ".join(text.split())
	if not normalized:
		return MINIMUM_COLUMN_DEMAND
	words = normalized.split(" ")
	longest_word = min(MAXIMUM_WORD_DEMAND, max(len(word) for word in words))
	wrap_aware_length = math.ceil(math.sqrt(len(normalized) * wrap_factor))
	demand = max(MINIMUM_COLUMN_DEMAND, longest_word, wrap_aware_length)
	return min(MAXIMUM_COLUMN_DEMAND, demand)


#============================================
def normalize_percentages(demands: tuple[int, ...]) -> tuple[int, ...]:
	"""Convert positive relative demands to deterministic percentages totaling 100."""
	if not demands or any(demand <= 0 for demand in demands):
		raise ValueError("Table column demands must be positive")
	total = sum(demands)
	raw_percentages = tuple(demand * 100 / total for demand in demands)
	percentages = [math.floor(value) for value in raw_percentages]
	remainder = 100 - sum(percentages)
	priority = sorted(
		range(len(demands)),
		key=lambda index: (raw_percentages[index] - percentages[index], demands[index]),
		reverse=True,
	)
	for index in priority[:remainder]:
		percentages[index] += 1
	return tuple(percentages)


#============================================
def compact_table_columns(
	headers: tuple[str, ...],
	body_rows: tuple[tuple[str, ...], ...],
) -> tuple[bool, ...]:
	"""Identify short identifier columns that should not consume prose space."""
	compact_columns = []
	for column_index, header in enumerate(headers):
		visible_values = [header]
		visible_values.extend(row[column_index] for row in body_rows)
		longest_value = max(len(value) for value in visible_values)
		compact_columns.append(longest_value <= COMPACT_COLUMN_TEXT_LIMIT)
	return tuple(compact_columns)


#============================================
def calculate_table_layout(
	headers: tuple[str, ...],
	body_rows: tuple[tuple[str, ...], ...],
) -> TableLayout:
	"""Calculate one complete layout from all visible cells in a table."""
	profile = classify_table_headers(headers)
	if not headers:
		raise ValueError("Syllabus tables must have at least one column")
	for row in body_rows:
		if len(row) != len(headers):
			raise ValueError(
				f"{profile}: expected {len(headers)} columns, found {len(row)}"
			)
	compact_columns = compact_table_columns(headers, body_rows)
	demands = []
	for column_index, header in enumerate(headers):
		visible_values = [header]
		visible_values.extend(row[column_index] for row in body_rows)
		if compact_columns[column_index]:
			# Compact identifiers need much less wrap reserve than prose. Keeping their
			# longest unbreakable segment still lets an exceptional weekday wrap without
			# making every ordinary date column equally wide.
			column_demand = max(
				text_width_demand(value, COMPACT_WRAP_FACTOR)
				for value in visible_values
			)
		else:
			column_demand = text_width_demand(header, HEADER_WRAP_FACTOR)
			for row in body_rows:
				cell_demand = text_width_demand(row[column_index], BODY_WRAP_FACTOR)
				column_demand = max(column_demand, cell_demand)
		if headers == STAGED_SCHEDULE_HEADERS and header == "Date":
			# The six-column print layout needs enough intrinsic room for routine dates,
			# while special dates may still wrap at the comma.
			column_demand = max(column_demand, STAGED_SCHEDULE_DATE_DEMAND)
		demands.append(column_demand)
	column_demands = tuple(demands)
	column_width_demands = tuple(
		demand + (
			COMPACT_CELL_HORIZONTAL_ALLOWANCE
			if compact_columns[column_index]
			else CELL_HORIZONTAL_ALLOWANCE
		)
		for column_index, demand in enumerate(column_demands)
	)
	intrinsic_width_ch = sum(column_width_demands)
	is_compact = intrinsic_width_ch <= COMPACT_TABLE_CHARACTER_LIMIT
	if not is_compact and profile == "schedule":
		# Short identifiers need only their intrinsic width. Give the extra line-length
		# budget to prose when a schedule has only two flexible columns. A schedule that
		# already separates several prose roles is intrinsically wide and does not need
		# another multiplier before entering its horizontal-scroll container.
		flexible_column_count = compact_columns.count(False)
		growth_factor = (
			FLEXIBLE_COLUMN_GROWTH_FACTOR
			if flexible_column_count <= MAXIMUM_GROWING_SCHEDULE_COLUMNS
			else 1.0
		)
		column_width_demands = tuple(
			width_demand if compact_columns[column_index] else math.ceil(
				width_demand * growth_factor
			)
			for column_index, width_demand in enumerate(column_width_demands)
		)
	minimum_width_ch = sum(column_width_demands)
	return TableLayout(
		profile=profile,
		column_demands=column_demands,
		column_percentages=normalize_percentages(column_width_demands),
		compact_columns=compact_columns,
		minimum_width_ch=minimum_width_ch,
		is_compact=is_compact,
	)


#============================================
def calculate_shared_table_layouts(
	table_contents: tuple[
		tuple[tuple[str, ...], tuple[tuple[str, ...], ...]],
		...,
	],
) -> tuple[TableLayout, ...]:
	"""Give every exact-header table series one shared content-derived layout."""
	grouped_rows: dict[tuple[str, ...], list[tuple[str, ...]]] = collections.defaultdict(list)
	for headers, body_rows in table_contents:
		grouped_rows[headers].extend(body_rows)
	shared_layouts = {
		headers: calculate_table_layout(headers, tuple(body_rows))
		for headers, body_rows in grouped_rows.items()
	}
	return tuple(shared_layouts[headers] for headers, _body_rows in table_contents)


#============================================
def add_column_widths(
	table: xml.etree.ElementTree.Element,
	layout: TableLayout,
) -> None:
	"""Emit bounded, content-derived width hints into one HTML table."""
	colgroup = xml.etree.ElementTree.Element("colgroup")
	for percentage in layout.column_percentages:
		# ASVS 1.2.1: only bounded integers from the local calculator reach CSS syntax.
		column = xml.etree.ElementTree.SubElement(colgroup, "col")
		column.set("style", f"width: {percentage}%")
	table.insert(0, colgroup)
	table.set("data-table-widths", ",".join(str(value) for value in layout.column_percentages))
	table.set("data-table-demands", ",".join(str(value) for value in layout.column_demands))
	table.set("style", f"--table-minimum-width: {layout.minimum_width_ch}ch")
	return None


#============================================
def mark_compact_table_cells(
	table: xml.etree.ElementTree.Element,
	layout: TableLayout,
) -> None:
	"""Mark short identifier columns for reduced padding and no wrapping."""
	rows = table.findall("./thead/tr") + table.findall("./tbody/tr")
	for row in rows:
		cells = row.findall("th") + row.findall("td")
		for column_index, cell in enumerate(cells):
			if layout.compact_columns[column_index]:
				classes = cell.get("class", "").split()
				classes.append("syllabus-column--compact")
				cell.set("class", " ".join(dict.fromkeys(classes)))
	return None


#============================================
def merge_schedule_exam_cells(
	table: xml.etree.ElementTree.Element,
	headers: tuple[str, ...],
) -> None:
	"""Span a prominent exam milestone across the Topic and Quiz columns."""
	if len(headers) != 5 or headers[2:4] != ("Topic", "Quiz"):
		return None
	for row in table.findall("./tbody/tr"):
		cells = row.findall("td")
		if len(cells) != len(headers):
			continue
		topic_cell = cells[2]
		quiz_cell = cells[3]
		if topic_cell.find("strong") is None or normalize_cell_text(quiz_cell):
			continue
		topic_cell.set("class", "schedule-exam-cell")
		topic_cell.set("colspan", "2")
		row.remove(quiz_cell)
	return None


#============================================
def append_element_class(
	element: xml.etree.ElementTree.Element,
	class_name: str,
) -> None:
	"""Append one CSS class without duplicating an existing class."""
	classes = element.get("class", "").split()
	classes.append(class_name)
	element.set("class", " ".join(dict.fromkeys(classes)))
	return None


#============================================
def merge_schedule_stage_cells(
	table: xml.etree.ElementTree.Element,
	headers: tuple[str, ...],
	raw_html_blocks: tuple[str | xml.etree.ElementTree.Element, ...] = (),
) -> None:
	"""Group BIOL 480 stages and span non-meeting milestones across prose columns."""
	if headers != STAGED_SCHEDULE_HEADERS:
		return None
	row_details = []
	for row in table.findall("./tbody/tr"):
		cells = row.findall("td")
		if len(cells) != len(headers):
			continue
		week_text = normalize_cell_text(cells[0], raw_html_blocks)
		stage_text = normalize_cell_text(cells[2], raw_html_blocks)
		in_class_text = normalize_cell_text(cells[4], raw_html_blocks)
		work_due_text = normalize_cell_text(cells[5], raw_html_blocks)
		try:
			stage_key = SCHEDULE_STAGE_KEYS[stage_text]
		except KeyError as error:
			raise ValueError(f"Unregistered schedule stage: {stage_text}") from error
		append_element_class(row, "schedule-phase-row")
		append_element_class(row, f"schedule-phase-row--{stage_key}")
		if week_text == "-" and in_class_text == "-" and work_due_text == "-":
			topic_cell = cells[3]
			append_element_class(row, "schedule-milestone-row")
			append_element_class(topic_cell, "schedule-milestone-cell")
			topic_cell.set("colspan", "3")
			row.remove(cells[4])
			row.remove(cells[5])
		row_details.append((row, cells[2], stage_text, stage_key))

	group_start = 0
	while group_start < len(row_details):
		group_end = group_start + 1
		stage_text = row_details[group_start][2]
		while group_end < len(row_details) and row_details[group_end][2] == stage_text:
			group_end += 1
		first_row, first_cell, _stage_text, stage_key = row_details[group_start]
		append_element_class(first_row, "schedule-phase-row--start")
		first_cell.clear()
		first_cell.tag = "th"
		first_cell.set("scope", "rowgroup")
		first_cell.set("rowspan", str(group_end - group_start))
		first_cell.set(
			"class",
			f"schedule-phase-cell schedule-phase-cell--{stage_key}",
		)
		phase_label = xml.etree.ElementTree.SubElement(
			first_cell,
			"span",
			{"class": f"schedule-phase schedule-phase--{stage_key}"},
		)
		phase_label.text = stage_text
		for row, stage_cell, _text, _key in row_details[group_start + 1:group_end]:
			row.remove(stage_cell)
		group_start = group_end
	return None


#============================================
def wrap_scrollable_table(
	parent: xml.etree.ElementTree.Element,
	child_index: int,
	table: xml.etree.ElementTree.Element,
) -> None:
	"""Give one table a bounded horizontal-scroll owner."""
	scroll_wrapper = xml.etree.ElementTree.Element(
		"div",
		{"class": "md-typeset__scrollwrap"},
	)
	table_wrapper = xml.etree.ElementTree.SubElement(
		scroll_wrapper,
		"div",
		{"class": "md-typeset__table"},
	)
	parent.remove(table)
	table_wrapper.append(table)
	parent.insert(child_index, scroll_wrapper)
	return None


#============================================
class TableLayoutTreeprocessor(markdown.treeprocessors.Treeprocessor):
	"""Attach renderer-neutral profile hooks after Markdown builds each table."""

	def run(
		self,
		root: xml.etree.ElementTree.Element,
	) -> xml.etree.ElementTree.Element:
		"""Classify every semantic table in the rendered Markdown tree."""
		tables_with_parents = []
		for parent in root.iter():
			for child_index, child in enumerate(list(parent)):
				if child.tag == "table":
					tables_with_parents.append((parent, child_index, child))
		raw_html_blocks = tuple(self.md.htmlStash.rawHtmlBlocks)
		table_contents = tuple(
			(
				table_headers(table, raw_html_blocks),
				table_body_rows(table, raw_html_blocks),
			)
			for _parent, _child_index, table in tables_with_parents
		)
		layouts = calculate_shared_table_layouts(table_contents)
		series_sizes = collections.Counter(headers for headers, _body_rows in table_contents)
		for (parent, child_index, table), layout, (headers, body_rows) in zip(
			tables_with_parents,
			layouts,
			table_contents,
			strict=True,
		):
			classes = ["syllabus-table", f"table-layout--{layout.profile}"]
			if layout.is_compact:
				classes.append("table-width--intrinsic")
			table.set("class", " ".join(classes))
			table.set("data-table-profile", layout.profile)
			table.set("data-table-series-size", str(series_sizes[headers]))
			add_column_widths(table, layout)
			mark_compact_table_cells(table, layout)
			merge_schedule_stage_cells(table, headers, raw_html_blocks)
			merge_schedule_exam_cells(table, headers)
			wrap_scrollable_table(parent, child_index, table)
		return root


#============================================
class TableLayoutExtension(markdown.extensions.Extension):
	"""Register semantic table layout classification with Python-Markdown."""

	def extendMarkdown(self, md: markdown.Markdown) -> None:
		"""Run after block parsing and before final HTML serialization."""
		processor = TableLayoutTreeprocessor(md)
		md.treeprocessors.register(processor, "syllabus_table_layouts", 7)
		return None


#============================================
def makeExtension(**kwargs) -> TableLayoutExtension:
	"""Create the extension through Python-Markdown's required entry point."""
	extension = TableLayoutExtension(**kwargs)
	return extension
