"""Focused offline tests for the Biostatistics Google Sheets importer."""

# PIP3 modules
import pytest
import pathlib
import sys

# local repo modules
import build_lib.biostats_schedule
import build_lib.biotech_schedule
import build_lib.genetics_schedule
import build_lib.important_dates
import build_lib.calendar_sync


SAMPLE_CSV = (
	"Wk,Date,Lecture,Assignments Due\n"
	'1,"Wed, Sep 02, 2026","Course Introduction & Format\n'
	'What is Biostatistics? Types of Data",\n'
	'2,"Wed, Sep 09, 2026","Descriptive statistics: Working with data",'
	'"Interesting Science Figure Assignment"\n'
	'\u2013,"Fri, Oct 30, 2026","Last day to drop for a ""W"" grade",\n'
	'\u2014,"Wed, Nov 25, 2026","Thanksgiving break starts on Tuesday; NO CLASS",\n'
	'15,"Wed, Dec 16, 2026","Finals week class does not meet;\nFinal project is due",\n'
)


#============================================
def test_parse_and_render_map_fields_multiline_and_special_dates() -> None:
	"""The four-column source maps completely, including dated notices and line breaks."""
	entries = build_lib.biostats_schedule.parse_csv(SAMPLE_CSV)
	markdown = build_lib.biostats_schedule.render_markdown(entries)
	assert len(entries) == 5
	assert entries[0].week == "1"
	assert entries[0].date.isoformat() == "2026-09-02"
	assert entries[0].lecture == "Course Introduction & Format\nWhat is Biostatistics? Types of Data"
	assert entries[1].assignments_due == "Interesting Science Figure Assignment"
	assert entries[2].week == "-"
	assert "| Week and date | Schedule details |" in markdown
	assert "| Week 1<br>Wed, Sep 2 |" in markdown
	assert (
		"**Lecture:** Course Introduction &amp; Format<br>"
		"What is Biostatistics? Types of Data" in markdown
	)
	assert "**Assignments due:** Interesting Science Figure Assignment" in markdown
	assert (
		f"[Biostatistics schedule spreadsheet](https://docs.google.com/spreadsheets/d/"
		f"{build_lib.biostats_schedule.SPREADSHEET_ID}/edit)" in markdown
	)
	assert 'Last day to drop for a "W" grade' in markdown
	assert "| Fri, Oct 30 | **Lecture:** Last day to drop" in markdown
	assert "| Wed, Nov 25 | **Lecture:** Thanksgiving break" in markdown
	assert (
		"**Lecture:** Finals week class does not meet;<br>Final project is due"
		in markdown
	)
	assert "SYLLABUS_CHANGE_NOTICE.md" in markdown


#============================================
def test_render_escapes_markdown_and_html_from_spreadsheet_text() -> None:
	"""Remote cell content remains literal within its Markdown table cell."""
	entries = build_lib.biostats_schedule.parse_csv(SAMPLE_CSV)
	entries[0].lecture = "[link](javascript:alert(1)) | <script> *topic*"
	markdown = build_lib.biostats_schedule.render_markdown(entries)
	assert "[link]" not in markdown
	assert "&#91;link&#93;" in markdown
	assert "&#124; &lt;script&gt;" in markdown
	assert "&#42;topic&#42;" in markdown


#============================================
def test_parse_csv_rejects_an_unknown_schema() -> None:
	"""Changed worksheet headers fail before any schedule can be replaced."""
	with pytest.raises(ValueError, match="unsupported header schema"):
		build_lib.biostats_schedule.parse_csv("Week,Date,Topic,Due\n")


#============================================
@pytest.mark.parametrize(
	("csv_text", "message"),
	(
		(
			"Wk,Date,Lecture,Assignments Due\n"
			'1,"Wed, Sep 02, 2026",Only three columns\n',
			"wrong number of columns",
		),
		(
			"Wk,Date,Lecture,Assignments Due\n"
			'1,"Mon, Sep 02, 2026",Topic,\n',
			"wrong weekday",
		),
		(
			"Wk,Date,Lecture,Assignments Due\n"
			'1,"Wed, Sep 02, 2025",Topic,\n',
			"outside Fall 2026",
		),
		(
			"Wk,Date,Lecture,Assignments Due\n"
			'2,"Wed, Sep 09, 2026",Later,\n'
			'1,"Wed, Sep 02, 2026",Earlier,\n',
			"not in chronological order",
		),
	),
)
def test_parse_csv_rejects_malformed_rows_and_dates(csv_text: str, message: str) -> None:
	"""The schema, date, and source-order checks apply to each export."""
	with pytest.raises(ValueError, match=message):
		build_lib.biostats_schedule.parse_csv(csv_text)


#============================================
def test_main_validates_every_source_before_replacing_snapshots(
	tmp_path: pathlib.Path,
	monkeypatch: pytest.MonkeyPatch,
) -> None:
	"""A rejected final source leaves all prior snapshots unchanged."""
	university_path = tmp_path / build_lib.important_dates.OUTPUT_RELATIVE_PATH
	biostats_path = tmp_path / build_lib.biostats_schedule.OUTPUT_RELATIVE_PATH
	biotech_path = tmp_path / build_lib.biotech_schedule.OUTPUT_RELATIVE_PATH
	genetics_path = tmp_path / build_lib.genetics_schedule.OUTPUT_RELATIVE_PATH
	university_path.parent.mkdir(parents=True)
	biostats_path.parent.mkdir(parents=True)
	biotech_path.parent.mkdir(parents=True)
	genetics_path.parent.mkdir(parents=True)
	university_path.write_text("old university\n", encoding="utf-8")
	biostats_path.write_text("old biostatistics\n", encoding="utf-8")
	biotech_path.write_text("old BIOL 480\n", encoding="utf-8")
	genetics_path.write_text("old Genetics\n", encoding="utf-8")
	monkeypatch.setattr(build_lib.calendar_sync, "get_repo_root", lambda: tmp_path)
	monkeypatch.setattr(build_lib.calendar_sync, "fix_markdown_ascii_compliance", lambda text: text)
	monkeypatch.setattr(sys, "argv", ["sync_calendars.py"])
	monkeypatch.setattr(
		build_lib.important_dates,
		"prepare_output",
		lambda: ("new university\n", 1),
	)
	monkeypatch.setattr(
		build_lib.biostats_schedule,
		"prepare_output",
		lambda: ("new biostatistics\n", 1),
	)
	monkeypatch.setattr(
		build_lib.biotech_schedule,
		"prepare_output",
		lambda: ("new BIOL 480\n", 1),
	)
	def reject_genetics_export() -> tuple[str, int]:
		raise ValueError("unsupported Genetics schema")
	monkeypatch.setattr(build_lib.genetics_schedule, "prepare_output", reject_genetics_export)
	with pytest.raises(ValueError, match="unsupported Genetics schema"):
		build_lib.calendar_sync.main()
	assert university_path.read_text(encoding="utf-8") == "old university\n"
	assert biostats_path.read_text(encoding="utf-8") == "old biostatistics\n"
	assert biotech_path.read_text(encoding="utf-8") == "old BIOL 480\n"
	assert genetics_path.read_text(encoding="utf-8") == "old Genetics\n"


#============================================
def test_main_refreshes_all_configured_calendars_together(
	tmp_path: pathlib.Path,
	monkeypatch: pytest.MonkeyPatch,
) -> None:
	"""The default one-command refresh writes all configured calendar sources."""
	monkeypatch.setattr(build_lib.calendar_sync, "get_repo_root", lambda: tmp_path)
	monkeypatch.setattr(build_lib.calendar_sync, "fix_markdown_ascii_compliance", lambda text: text)
	monkeypatch.setattr(sys, "argv", ["sync_calendars.py"])
	monkeypatch.setattr(
		build_lib.important_dates,
		"prepare_output",
		lambda: ("university snapshot\n", 1),
	)
	monkeypatch.setattr(
		build_lib.biostats_schedule,
		"prepare_output",
		lambda: ("biostatistics snapshot\n", 1),
	)
	monkeypatch.setattr(
		build_lib.biotech_schedule,
		"prepare_output",
		lambda: ("BIOL 480 snapshot\n", 1),
	)
	monkeypatch.setattr(
		build_lib.genetics_schedule,
		"prepare_output",
		lambda: ("Genetics snapshot\n", 1),
	)
	build_lib.calendar_sync.main()
	assert (
		(tmp_path / build_lib.important_dates.OUTPUT_RELATIVE_PATH).read_text(encoding="utf-8")
		== "university snapshot\n"
	)
	assert (
		(tmp_path / build_lib.biostats_schedule.OUTPUT_RELATIVE_PATH).read_text(encoding="utf-8")
		== "biostatistics snapshot\n"
	)
	assert (
		(tmp_path / build_lib.biotech_schedule.OUTPUT_RELATIVE_PATH).read_text(encoding="utf-8")
		== "BIOL 480 snapshot\n"
	)
	assert (
		(tmp_path / build_lib.genetics_schedule.OUTPUT_RELATIVE_PATH).read_text(encoding="utf-8")
		== "Genetics snapshot\n"
	)
