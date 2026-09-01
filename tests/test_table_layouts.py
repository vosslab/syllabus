"""Behavior tests for content-derived syllabus table layouts."""

# Standard Library
import re
import xml.etree.ElementTree

# PIP3 modules
import markdown

# local repo modules
import build_lib.table_layouts


#============================================
def test_numeric_project_column_yields_width_to_descriptive_work() -> None:
	"""Short scores stay compact while student-facing descriptions get room."""
	headers = ("Required work", "What is expected", "Points")
	body_rows = (
		(
			"Research poster",
			"Explain the evidence, connect it to the biological mechanism, and cite sources.",
			"20",
		),
	)
	layout = build_lib.table_layouts.calculate_table_layout(headers, body_rows)
	assert layout.column_percentages[1] > layout.column_percentages[0]
	assert layout.column_percentages[0] > layout.column_percentages[2]
	assert sum(layout.column_percentages) == 100


#============================================
def test_markdown_tables_receive_renderer_neutral_profile_hooks() -> None:
	"""One semantic classification reaches both website and PDF HTML."""
	markdown_text = (
		"| Percentage | Grade |\n"
		"| --- | :---: |\n"
		"| 92.0% and above | A |\n"
	)
	rendered = markdown.markdown(
		markdown_text,
		extensions=("tables", "build_lib.table_layouts"),
	)
	assert 'class="syllabus-table table-layout--grade-scale table-width--intrinsic"' in rendered
	assert 'data-table-profile="grade-scale"' in rendered
	assert 'data-table-widths="' in rendered
	assert '<colgroup>' in rendered
	assert '<div class="md-typeset__scrollwrap">' in rendered


#============================================
def test_repeated_header_series_receives_one_shared_layout() -> None:
	"""Monthly date tables align to the widest content in every shared column."""
	headers = ("Date", "Event", "Type")
	table_contents = (
		(headers, (("Tue, Aug 18", "Faculty Conference", "University event"),)),
		(
			headers,
			((
				"Sun, Nov 01",
				"Priority Registration Begins for Spring and Summer",
				"Registration and withdrawal",
			),),
		),
		(("Percentage", "Grade"), (("92.0% and above", "A"),)),
	)
	layouts = build_lib.table_layouts.calculate_shared_table_layouts(table_contents)
	assert layouts[0] == layouts[1]


#============================================
def test_markdown_repeated_tables_emit_matching_series_widths() -> None:
	"""The HTML branch exposes one width vector for an exact-header series."""
	markdown_text = (
		"| Date | Event | Type |\n"
		"| --- | --- | --- |\n"
		"| Tue, Aug 18 | Faculty Conference | University event |\n\n"
		"| Date | Event | Type |\n"
		"| --- | --- | --- |\n"
		"| Sun, Nov 01 | Priority Registration Begins for Spring and Summer | "
		"Registration and withdrawal |\n"
	)
	rendered = markdown.markdown(
		markdown_text,
		extensions=("tables", "build_lib.table_layouts"),
	)
	width_matches = re.finditer(r'data-table-widths="([^"]+)"', rendered)
	first_widths = next(width_matches).group(1)
	second_widths = next(width_matches).group(1)
	assert first_widths == second_widths


#============================================
def test_key_value_layout_prioritizes_information_column() -> None:
	"""A two-column reference table gives most of its width to the information."""
	headers = ("Field", "Information")
	body_rows = (
		("Meeting", "Tuesday, 1:30-4:25 p.m."),
		("Prerequisites", "BIOL 201, BIOL 202, and BIOL 301 with C- or better"),
	)
	layout = build_lib.table_layouts.calculate_table_layout(headers, body_rows)
	assert layout.profile == "key-value"
	assert layout.column_percentages[0] < layout.column_percentages[1]


#============================================
def test_inline_html_does_not_inflate_visible_column_demand() -> None:
	"""Styling hooks do not count as student-visible table content."""
	plain_markdown = (
		"| Week | Date | Topic | Quiz | Due this date |\n"
		"| --- | --- | --- | --- | --- |\n"
		"| 1 | Sep 1 | Genetic disorders | 1 | Orientation |\n"
	)
	styled_markdown = plain_markdown.replace(
		"| 1 | Orientation |",
		'| <span class="schedule-quiz-key">1</span> | Orientation |',
	)
	plain_html = markdown.markdown(
		plain_markdown,
		extensions=("tables", "build_lib.table_layouts"),
	)
	styled_html = markdown.markdown(
		styled_markdown,
		extensions=("tables", "build_lib.table_layouts"),
	)
	width_pattern = re.compile(r'data-table-widths="([^"]+)"')
	plain_widths = width_pattern.search(plain_html).group(1)
	styled_widths = width_pattern.search(styled_html).group(1)
	assert styled_widths == plain_widths


#============================================
def test_schedule_exam_spans_topic_and_quiz_columns() -> None:
	"""A bold schedule milestone becomes one prominent two-column cell."""
	headers = ("Week", "Date", "Topic", "Quiz", "Due this date")
	table = xml.etree.ElementTree.Element("table")
	table_body = xml.etree.ElementTree.SubElement(table, "tbody")
	row = xml.etree.ElementTree.SubElement(table_body, "tr")
	for value in ("8", "Oct 20", "", "", "Assignment 13"):
		cell = xml.etree.ElementTree.SubElement(row, "td")
		cell.text = value
	strong = xml.etree.ElementTree.SubElement(row.findall("td")[2], "strong")
	strong.text = "MID-TERM EXAM"
	build_lib.table_layouts.merge_schedule_exam_cells(table, headers)
	cells = table.findall("./tbody/tr/td")
	observed = (
		len(cells),
		cells[2].get("class"),
		cells[2].get("colspan"),
		cells[3].text,
	)
	assert observed == (4, "schedule-exam-cell", "2", "Assignment 13")
