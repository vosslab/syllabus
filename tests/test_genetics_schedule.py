"""Focused offline tests for the Genetics Google Sheets importer."""

# PIP3 modules
import pytest

# local repo modules
import build_lib.genetics_schedule


SAMPLE_CSV = (
	"Wk,Lect,Date,Lecture,Quiz,\"In-Class\nActivity\",Quiz,\"Assign\nDue\"\n"
	'1,1,"Tue, Sep 01, 2026","Syllabus, Chapter 1: Course introduction and genetic disorders",'
	'1,"Genetic\nDisorders",,\u2014\n'
	'4,4,"Tue, Sep 22, 2026","Mendelian genetics",2,"MultiGene\nCrossover",Q1,"01, 02, 03"\n'
	'7,\u2014,"Tue, Oct 13, 2026","MID-TERM EXAM (Chapters 1\u20134)\n'
	'In person written exam during class",,,,"06"\n'
	',,"Fri, Oct 30, 2026","Last day to drop for a ""W""",,,,\n'
	',,"Tue, Nov 24, 2026","Thanksgiving break starts on Tuesday; NO CLASS",,,,\n'
)


#============================================
def test_parse_and_render_preserves_genetics_sheet_fields() -> None:
	"""The tall schedule retains quiz coverage, quiz due dates, and special-date notices."""
	entries = build_lib.genetics_schedule.parse_csv(SAMPLE_CSV)
	markdown = build_lib.genetics_schedule.render_markdown(entries)
	assert len(entries) == 5
	assert entries[0].lecture_number == "1"
	assert entries[0].topic == "Syllabus, Chapter 1: Course introduction and genetic disorders"
	assert entries[0].activity == "Genetic\nDisorders"
	assert entries[1].quiz_coverage == "2"
	assert entries[1].quiz_due == "1"
	assert entries[1].assignments_due == "01, 02, 03"
	assert "| Week and date | Schedule details |" in markdown
	assert "| Week 1<br>Lecture 1<br>Tue, Sep 1 |" in markdown
	assert "**Activity:** Genetic<br>Disorders" in markdown
	assert (
		'**Quiz coverage:** <span class="schedule-quiz-key schedule-quiz-key--2">Quiz 2</span>'
		in markdown
	)
	assert (
		'**Quiz due:** <span class="schedule-quiz-key schedule-quiz-key--1">Quiz 1</span>'
		in markdown
	)
	assert "**Assignments due:** 01, 02, 03" in markdown
	assert "**Assignments due:** 06" in markdown
	assert "| Week 7<br>Tue, Oct 13 |" in markdown
	assert '| Fri, Oct 30 | **Topic:** Last day to drop for a "W" |' in markdown
	assert "| Tue, Nov 24 | **Topic:** Thanksgiving break" in markdown
	assert (
		f"[Genetics schedule spreadsheet](https://docs.google.com/spreadsheets/d/"
		f"{build_lib.genetics_schedule.SPREADSHEET_ID}/edit)" in markdown
	)


#============================================
@pytest.mark.parametrize(
	("csv_text", "message"),
	(
		(
			SAMPLE_CSV.replace('"Assign\nDue"', "Assignments Due"),
			"unsupported header schema",
		),
		(
			SAMPLE_CSV.replace("Tue, Sep 01, 2026", "Mon, Sep 01, 2026", 1),
			"wrong weekday",
		),
		(
			"Wk,Lect,Date,Lecture,Quiz,In-Class Activity,Quiz,Assign Due\n"
			'2,2,"Tue, Sep 08, 2026",Later,2,,Q1,\n'
			'1,1,"Tue, Sep 01, 2026",Earlier,1,,,\n',
			"not in chronological order",
		),
		(
			"Wk,Lect,Date,Lecture,Quiz,In-Class Activity,Quiz,Assign Due\n"
			'1,1,"Tue, Sep 01, 2026",Only four columns\n',
			"wrong number of columns",
		),
	),
)
def test_parse_csv_rejects_changed_schemas_and_invalid_rows(
	csv_text: str,
	message: str,
) -> None:
	"""The fixed source contract rejects schema, row-shape, date, and order changes."""
	with pytest.raises(ValueError, match=message):
		build_lib.genetics_schedule.parse_csv(csv_text)
