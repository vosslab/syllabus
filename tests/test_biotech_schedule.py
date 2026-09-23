"""Focused offline tests for the BIOL 480 Google Sheets importer."""

# PIP3 modules
import pytest

# local repo modules
import build_lib.biotech_schedule


SAMPLE_CSV = (
	"Wk,Date,Stage,Weekly Topic,Assign,Assignments Due\n"
	'1,"Thu, Sep 03, 2026",Foundations,"Course Introduction & Format;\n'
	'What is Biotechnology?",,\n'
	'2,"Thu, Sep 10, 2026",Individual Project,"Set #1: Basics of Biotechnology\n'
	'and the Central Dogma",HW 0,"Project Ideas | <script> due\n'
	'Instructor response"\n'
	'\u2013,"Fri, Oct 30, 2026",,"last day to drop for a ""W"" grade",,\n'
	'10,"Thu, Nov 05, 2026",Transition,"Set #5: Medicinal Biotechnology",movie form,\n'
	'11,"Thu, Nov 12, 2026",Group Project,Set #6: Regulation Biotechnology,HW 5,Groups Formed\n'
	',"Thu, Nov 26, 2026",,"No Class, Thanksgiving Week",,\n'
)


#============================================
def test_parse_and_render_preserve_sheet_fields_and_stage_notices() -> None:
	"""Every worksheet field maps to the staged schedule without collapsing assignment columns."""
	entries = build_lib.biotech_schedule.parse_csv(SAMPLE_CSV)
	markdown = build_lib.biotech_schedule.render_markdown(entries)
	assert len(entries) == 6
	assert entries[0].stage == "Course foundations"
	assert entries[0].weekly_topic == "Course Introduction & Format;\nWhat is Biotechnology?"
	assert entries[1].assign == "HW 0"
	assert entries[1].assignments_due == "Project Ideas | <script> due\nInstructor response"
	assert entries[2].stage == "Individual project"
	assert entries[3].stage == "Transition"
	assert entries[4].stage == "Group project"
	assert entries[5].stage == "Group project"
	assert "| Wk | Date | Stage | Weekly Topic | Assign | Assignments Due |" in markdown
	assert "Course Introduction &amp; Format;<br>What is Biotechnology?" in markdown
	assert (
		f"[BIOL 480 schedule spreadsheet](https://docs.google.com/spreadsheets/d/"
		f"{build_lib.biotech_schedule.SPREADSHEET_ID}/edit)" in markdown
	)
	assert "| HW 0 | Project Ideas &#124; &lt;script&gt; due<br>Instructor response |" in markdown
	assert '| - | Fri, Oct 30 | Individual project | last day to drop for a "W" grade |' in markdown
	assert "| - | Thu, Nov 26 | Group project | No Class, Thanksgiving Week |" in markdown


#============================================
def test_parse_csv_rejects_an_unknown_schema() -> None:
	"""A changed first-worksheet contract fails closed."""
	with pytest.raises(ValueError, match="unsupported header schema"):
		build_lib.biotech_schedule.parse_csv("Week,Date,Topic,Due\n")


#============================================
@pytest.mark.parametrize(
	("csv_text", "message"),
	(
		(
			"Wk,Date,Stage,Weekly Topic,Assign,Assignments Due\n"
			'1,"Thu, Sep 03, 2026",Foundations,Topic,\n',
			"wrong number of columns",
		),
		(
			"Wk,Date,Stage,Weekly Topic,Assign,Assignments Due\n"
			'1,"Mon, Sep 03, 2026",Foundations,Topic,,\n',
			"wrong weekday",
		),
		(
			"Wk,Date,Stage,Weekly Topic,Assign,Assignments Due\n"
			'1,"Thu, Sep 03, 2026",Unknown,Topic,,\n',
			"unsupported stage",
		),
		(
			"Wk,Date,Stage,Weekly Topic,Assign,Assignments Due\n"
			'1,"Thu, Sep 03, 2026",,Topic,,\n',
			"without a registered stage",
		),
		(
			"Wk,Date,Stage,Weekly Topic,Assign,Assignments Due\n"
			'2,"Thu, Sep 10, 2026",Foundations,Later,,\n'
			'1,"Thu, Sep 03, 2026",Foundations,Earlier,,\n',
			"not in chronological order",
		),
	),
)
def test_parse_csv_rejects_invalid_schema_rows_and_order(csv_text: str, message: str) -> None:
	"""Rectangular rows, known stages, weekday matches, and chronological order are enforced."""
	with pytest.raises(ValueError, match=message):
		build_lib.biotech_schedule.parse_csv(csv_text)
