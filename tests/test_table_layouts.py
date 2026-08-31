"""Behavior tests for content-derived syllabus table layouts."""

# Standard Library
import re

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
