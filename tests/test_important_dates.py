"""Focused tests for the Google Sheets important-dates importer."""

# PIP3 modules
import pytest

# local repo modules
import sync_important_dates


SAMPLE_CSV = (
	'Date,"confirmed\nfor 2026",Wk,X,Event,Notes\n'
	'"Tue, Aug 18, 2026",\u2714\ufe0e,\u2013,\u2714\ufe0e,'
	"8th Annual Faculty Conference,\n"
	'"Tue, Sep 01, 2026",,1,-,Fall Convocation,"Events calendar"\n'
)


#============================================
def test_render_markdown_separates_months_and_escapes_remote_markup() -> None:
	"""Month headings separate tables and remote cell text remains literal."""
	entries = sync_important_dates.parse_csv(SAMPLE_CSV)
	entries[1].event = "[Click](javascript:alert(1)) | <script>"
	markdown = sync_important_dates.render_markdown(entries)
	assert "\n## August 2026\n" in markdown and "\n---\n\n## September 2026\n" in markdown
	assert (
		"[Click]" not in markdown
		and "&#91;Click&#93;" in markdown
		and "&#124; &lt;script&gt;" in markdown
	)


#============================================
def test_render_markdown_omits_maintainer_metadata() -> None:
	"""Personal confirmation, formula, and source-note cells stay out of the page."""
	entries = sync_important_dates.parse_csv(SAMPLE_CSV)
	markdown = sync_important_dates.render_markdown(entries)
	assert "| Date | Event | Type |" in markdown
	assert "Confirmed" not in markdown and "Events calendar" not in markdown


#============================================
def test_parse_csv_rejects_an_unknown_schema() -> None:
	"""A changed worksheet schema fails before a page can be replaced."""
	wrong_schema = "Date,Event\nTue,Example\n"
	with pytest.raises(ValueError, match="unsupported header schema"):
		sync_important_dates.parse_csv(wrong_schema)


#============================================
def test_parse_date_rejects_a_mismatched_weekday() -> None:
	"""The displayed weekday must agree with the calendar date."""
	with pytest.raises(ValueError, match="wrong weekday"):
		sync_important_dates.parse_date("Mon, Aug 18, 2026")


#============================================
@pytest.mark.parametrize(
	("event", "expected"),
	(
		("Last Day to Drop a Class for Full Refund", "Registration and withdrawal"),
		("Labor Day Holiday - NO CLASSES", "Holidays and closures"),
		("Degree Conferral Date", "Graduation"),
	),
)
def test_categorize_event_uses_student_scanning_types(event: str, expected: str) -> None:
	"""Representative event language maps to the intended visible type."""
	category = sync_important_dates.categorize_event(event)
	assert category == expected


#============================================
def test_validate_google_url_rejects_non_google_redirects() -> None:
	"""The fixed export cannot be redirected to an arbitrary remote host."""
	with pytest.raises(ValueError, match="unsupported location"):
		sync_important_dates.validate_google_url("https://example.com/export.csv")


#============================================
def test_validate_google_url_accepts_google_export_hosts() -> None:
	"""The initial and redirected Google export hosts remain available."""
	sync_important_dates.validate_google_url(
		"https://docs.google.com/spreadsheets/export?format=csv"
	)
	sync_important_dates.validate_google_url(
		"https://doc-example.googleusercontent.com/export/file.csv"
	)
