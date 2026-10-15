"""Parse and render the Fall 2026 Biostatistics schedule worksheet."""

# Standard Library
import io
import re
import csv
import pathlib
import datetime

# local repo modules
import build_lib.google_sheets
import build_lib.markdown_text


SPREADSHEET_ID = "1i_Whr_y3r43MynI-5QL3inDpBG8N1N8-M2nDtOB8ypg"
USER_AGENT = "vosslab-syllabus-calendar-sync/1.0"
OUTPUT_RELATIVE_PATH = pathlib.Path("site_docs/fall_2026/biostats/SCHEDULE.md")
MAX_ROWS = 1_000
DATE_PATTERN = re.compile(
	r"^(Mon|Tue|Wed|Thu|Fri|Sat|Sun), "
	r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) "
	r"([0-9]{1,2}), ([0-9]{4})$"
)
MONTH_NUMBERS = {
	"Jan": 1,
	"Feb": 2,
	"Mar": 3,
	"Apr": 4,
	"May": 5,
	"Jun": 6,
	"Jul": 7,
	"Aug": 8,
	"Sep": 9,
	"Oct": 10,
	"Nov": 11,
	"Dec": 12,
}
MONTH_ABBREVIATIONS = (
	"",
	"Jan",
	"Feb",
	"Mar",
	"Apr",
	"May",
	"Jun",
	"Jul",
	"Aug",
	"Sep",
	"Oct",
	"Nov",
	"Dec",
)
WEEKDAY_NAMES = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")


class ScheduleEntry:
	"""One validated row from the Biostatistics worksheet."""

	def __init__(
		self,
		week: str,
		date: datetime.date,
		details: list[tuple[str, str]],
	) -> None:
		self.week = week
		self.date = date
		self.details = details


#============================================
def fetch_csv_text() -> str:
	"""Download the first worksheet as a bounded UTF-8 CSV document."""
	return build_lib.google_sheets.fetch_csv_text(SPREADSHEET_ID, USER_AGENT)


#============================================
def normalize_cell(value: str, preserve_lines: bool = False) -> str:
	"""Normalize worksheet typography and whitespace while preserving intended lines."""
	return build_lib.markdown_text.normalize_spreadsheet_cell(value, preserve_lines)


#============================================
def normalize_header(value: str) -> str:
	"""Convert a worksheet header into its expected canonical name."""
	return " ".join(normalize_cell(value).lower().split())


#============================================
def parse_date(value: str) -> datetime.date:
	"""Parse and cross-check the worksheet's fixed English date format."""
	match = DATE_PATTERN.fullmatch(value)
	if match is None:
		raise ValueError("Google Sheets export contains a date in an unsupported format")
	weekday_text, month_text, day_text, year_text = match.groups()
	parsed_date = datetime.date(int(year_text), MONTH_NUMBERS[month_text], int(day_text))
	if parsed_date.year != 2026:
		raise ValueError("Google Sheets export contains a date outside Fall 2026")
	if WEEKDAY_NAMES[parsed_date.weekday()] != weekday_text:
		raise ValueError("Google Sheets export contains a date with the wrong weekday")
	return parsed_date


#============================================
def normalize_week(value: str) -> str:
	"""Validate a semester week number or a special-date marker."""
	week = normalize_cell(value)
	if week == "" or week in build_lib.markdown_text.WEEK_DASH_MARKERS:
		return "-"
	if not week.isdigit() or not 1 <= int(week) <= 20:
		raise ValueError("Google Sheets export contains an unsupported week value")
	return str(int(week))


#============================================
def parse_entry(
	raw_row: list[str],
	headers: list[str],
	week_index: int,
	date_index: int,
) -> ScheduleEntry:
	"""Validate structural fields and preserve all labeled details in sheet order."""
	if len(raw_row) != len(headers):
		raise ValueError("Google Sheets export contains a row with the wrong number of columns")
	week = normalize_week(raw_row[week_index])
	date = parse_date(normalize_cell(raw_row[date_index]))
	details = [
		(label, normalize_cell(value, preserve_lines=True))
		for index, (label, value) in enumerate(zip(headers, raw_row))
		if index not in (week_index, date_index)
	]
	if not any(value for label, value in details):
		raise ValueError("Google Sheets export contains a schedule row without details")
	return ScheduleEntry(week, date, details)


#============================================
def parse_csv(csv_text: str) -> list[ScheduleEntry]:
	"""Validate the first-worksheet schema and return its chronological entries."""
	reader = csv.reader(io.StringIO(csv_text, newline=""))
	raw_header = next(reader, None)
	if raw_header is None:
		raise ValueError("Google Sheets export is empty")
	# ASVS 2.2.1: validate structural columns; detail headings are display text.
	headers = [normalize_cell(value) for value in raw_header]
	if not all(headers):
		raise ValueError("Biostatistics export requires a nonblank heading for every column")
	header = [normalize_header(value) for value in headers]
	week_columns = [index for index, value in enumerate(header) if value in ("wk", "week")]
	date_columns = [index for index, value in enumerate(header) if value == "date"]
	if len(week_columns) != 1 or len(date_columns) != 1:
		raise ValueError("Biostatistics export requires exactly one Wk (or Week) and one Date column")
	if len(headers) < 3:
		raise ValueError("Biostatistics export requires at least one schedule detail column")
	week_index = week_columns[0]
	date_index = date_columns[0]
	entries: list[ScheduleEntry] = []
	for raw_row in reader:
		if not any(value.strip() for value in raw_row):
			continue
		if len(entries) >= MAX_ROWS:
			raise ValueError("Google Sheets export contains too many rows")
		entry = parse_entry(raw_row, headers, week_index, date_index)
		if entries and entry.date < entries[-1].date:
			raise ValueError("Google Sheets export is not in chronological order")
		entries.append(entry)
	if not entries:
		raise ValueError("Google Sheets export contains no schedule entries")
	return entries


#============================================
def render_multiline_cell(value: str) -> str:
	"""Escape each source line and join it with a code-owned HTML line break."""
	if value == "":
		return "-"
	return "<br>".join(
		build_lib.markdown_text.escape_markdown_cell(line)
		for line in value.split("\n")
	)


#============================================
def render_table_row(entry: ScheduleEntry) -> str:
	"""Render one validated schedule entry as a Markdown table row."""
	date_text = (
		f"{WEEKDAY_NAMES[entry.date.weekday()]}, "
		f"{MONTH_ABBREVIATIONS[entry.date.month]} {entry.date.day}"
	)
	week_and_date = f"Week {entry.week}<br>{date_text}" if entry.week != "-" else date_text
	details = []
	for label, value in entry.details:
		if value:
			# ASVS 1.2.1: headings and values are both external display text.
			escaped_label = build_lib.markdown_text.escape_markdown_cell(label)
			details.append(f"**{escaped_label}:** {render_multiline_cell(value)}")
	values = (week_and_date, "<br>".join(details))
	return f"| {' | '.join(values)} |"


#============================================
def render_markdown(entries: list[ScheduleEntry]) -> str:
	"""Render the full course schedule snapshot."""
	lines = [
		"<!-- Generated by launchers/sync_calendars.py. Do not edit directly. -->",
		"",
		"# Dates and topics",
		"",
		"Online tutorial assignments begin in Week 3. Each tutorial's directions provide its due date.",
		"",
		f"The schedule is drawn from the [Biostatistics schedule spreadsheet](https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit).",
		"",
		"| Week and date | Schedule details |",
		"| --- | --- |",
	]
	lines.extend(render_table_row(entry) for entry in entries)
	lines.extend(
		(
			"",
			'--8<-- "fall_2026/shared/fragments/SYLLABUS_CHANGE_NOTICE.md"',
		)
	)
	return "\n".join(lines) + "\n"


#============================================
def prepare_output() -> tuple[str, int]:
	"""Fetch, validate, and render the Biostatistics schedule without writing it."""
	csv_text = fetch_csv_text()
	entries = parse_csv(csv_text)
	markdown = render_markdown(entries)
	return markdown, len(entries)
