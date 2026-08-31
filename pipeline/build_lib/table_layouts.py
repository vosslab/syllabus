"""Classify syllabus tables and derive wrap-aware widths from their content."""

# Standard Library
import math
import collections
import xml.etree.ElementTree
from dataclasses import dataclass

# PIP3 modules
import markdown
import markdown.extensions
import markdown.treeprocessors


# These bounds are renderer-independent typography heuristics, not table-specific widths.
# They let prose request useful space without allowing one URL or identifier to dominate.
MINIMUM_COLUMN_DEMAND = 4
MAXIMUM_COLUMN_DEMAND = 44
MAXIMUM_WORD_DEMAND = 24
HEADER_WRAP_FACTOR = 6
BODY_WRAP_FACTOR = 12
CELL_HORIZONTAL_ALLOWANCE = 3
COMPACT_TABLE_CHARACTER_LIMIT = 32


@dataclass(frozen=True)
class TableLayout:
	"""One content-derived layout shared by HTML, PDF, DOCX, and audit tools."""

	profile: str
	column_demands: tuple[int, ...]
	column_percentages: tuple[int, ...]
	minimum_width_ch: int
	is_compact: bool


#============================================
def normalize_cell_text(element: xml.etree.ElementTree.Element) -> str:
	"""Return one table cell as normalized visible text."""
	text = "".join(element.itertext())
	normalized = " ".join(text.split())
	return normalized


#============================================
def shared_course_detail_row_indexes(
	headers: tuple[str, ...],
	body_rows: tuple[tuple[str, ...], ...],
) -> tuple[int, ...]:
	"""Identify course-detail rows that share one visible value across sections."""
	if classify_table_headers(headers) != "course-details":
		return ()
	shared_indexes = []
	for row_index, row in enumerate(body_rows):
		left_value = " ".join(row[1].split())
		right_value = " ".join(row[2].split())
		if left_value and left_value == right_value:
			shared_indexes.append(row_index)
	indexes = tuple(shared_indexes)
	return indexes


#============================================
def table_headers(element: xml.etree.ElementTree.Element) -> tuple[str, ...]:
	"""Return the first semantic header row from one HTML table element."""
	header_row = element.find("./thead/tr")
	if header_row is None:
		return ()
	headers = tuple(normalize_cell_text(cell) for cell in header_row.findall("th"))
	return headers


#============================================
def table_body_rows(
	element: xml.etree.ElementTree.Element,
) -> tuple[tuple[str, ...], ...]:
	"""Return normalized visible text from every table body row."""
	rows = []
	for row in element.findall("./tbody/tr"):
		cells = tuple(normalize_cell_text(cell) for cell in row.findall("td"))
		rows.append(cells)
	return tuple(rows)


#============================================
def classify_table_headers(headers: tuple[str, ...]) -> str:
	"""Map stable student-facing headers to one column-sizing profile."""
	if headers == ("Assessment", "Possible points", "Approximate share", "Your points"):
		return "point-plan"
	if len(headers) == 4 and headers[:3] == ("Week", "Date", "Topic"):
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
	if len(headers) == 3 and headers[0] == "Field":
		return "course-details"
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
	demands = []
	for column_index, header in enumerate(headers):
		column_demand = text_width_demand(header, HEADER_WRAP_FACTOR)
		for row in body_rows:
			cell_demand = text_width_demand(row[column_index], BODY_WRAP_FACTOR)
			column_demand = max(column_demand, cell_demand)
		demands.append(column_demand)
	column_demands = tuple(demands)
	minimum_width_ch = sum(column_demands) + CELL_HORIZONTAL_ALLOWANCE * len(headers)
	# Each column pays its own padding/border cost. Include that fixed cost in the
	# relative vector so compact numeric columns still fit their visible headers.
	column_width_demands = tuple(
		demand + CELL_HORIZONTAL_ALLOWANCE
		for demand in column_demands
	)
	return TableLayout(
		profile=profile,
		column_demands=column_demands,
		column_percentages=normalize_percentages(column_width_demands),
		minimum_width_ch=minimum_width_ch,
		is_compact=minimum_width_ch <= COMPACT_TABLE_CHARACTER_LIMIT,
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
def merge_shared_course_detail_cells(
	table: xml.etree.ElementTree.Element,
	headers: tuple[str, ...],
	body_rows: tuple[tuple[str, ...], ...],
) -> None:
	"""Render each shared course-detail value once across both section columns."""
	rows = table.findall("./tbody/tr")
	shared_indexes = shared_course_detail_row_indexes(headers, body_rows)
	for row_index in shared_indexes:
		cells = rows[row_index].findall("td")
		cells[1].set("colspan", "2")
		rows[row_index].remove(cells[2])
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
		table_contents = tuple(
			(table_headers(table), table_body_rows(table))
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
			merge_shared_course_detail_cells(table, headers, body_rows)
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
