"""Parse and render the Fall 2026 BIOL 480 schedule worksheet."""

# Standard Library
import io
import re
import csv
import pathlib
import datetime

# local repo modules
import build_lib.google_sheets
import build_lib.markdown_text


SPREADSHEET_ID = "1jnuSTeZwKhj0Vt0L27DpK2kGs7dW9FndcqZdaSrKUcQ"
USER_AGENT = "vosslab-syllabus-calendar-sync/1.0"
OUTPUT_RELATIVE_PATH = pathlib.Path("site_docs/fall_2026/biotech/SCHEDULE.md")
MAX_ROWS = 1_000
EXPECTED_HEADERS = (
	"wk",
	"date",
	"stage",
	"weekly topic",
	"assign",
	"assignments due",
)
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
STAGE_LABELS = {
	"foundations": "Course foundations",
	"individual project": "Individual project",
	"transition": "Transition",
	"group project": "Group project",
}


class ScheduleEntry:
	"""One validated row from the BIOL 480 worksheet."""

	def __init__(
		self,
		week: str,
		date: datetime.date,
		stage: str,
		weekly_topic: str,
		assign: str,
		assignments_due: str,
	) -> None:
		self.week = week
		self.date = date
		self.stage = stage
		self.weekly_topic = weekly_topic
		self.assign = assign
		self.assignments_due = assignments_due


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
def normalize_stage(value: str, week: str, previous_stage: str) -> str:
	"""Normalize a known phase or carry it through a blank dated notice row."""
	stage_text = normalize_cell(value)
	if stage_text == "":
		if week != "-" or previous_stage == "":
			raise ValueError("Google Sheets export contains a row without a registered stage")
		return previous_stage
	try:
		return STAGE_LABELS[stage_text.lower()]
	except KeyError as error:
		raise ValueError("Google Sheets export contains an unsupported stage") from error


#============================================
def parse_entry(raw_row: list[str], previous_stage: str = "") -> ScheduleEntry:
	"""Validate and convert one rectangular worksheet row."""
	if len(raw_row) != len(EXPECTED_HEADERS):
		raise ValueError("Google Sheets export contains a row with the wrong number of columns")
	week_text, date_text, stage_text, topic_text, assign_text, assignments_due_text = raw_row
	week = normalize_week(week_text)
	date = parse_date(normalize_cell(date_text))
	stage = normalize_stage(stage_text, week, previous_stage)
	weekly_topic = normalize_cell(topic_text, preserve_lines=True)
	assign = normalize_cell(assign_text, preserve_lines=True)
	assignments_due = normalize_cell(assignments_due_text, preserve_lines=True)
	if weekly_topic == "":
		raise ValueError("Google Sheets export contains a schedule row without a topic or notice")
	return ScheduleEntry(week, date, stage, weekly_topic, assign, assignments_due)


#============================================
def parse_csv(csv_text: str) -> list[ScheduleEntry]:
	"""Validate the six-column sheet schema and return chronological schedule rows."""
	reader = csv.reader(io.StringIO(csv_text, newline=""))
	raw_header = next(reader, None)
	if raw_header is None:
		raise ValueError("Google Sheets export is empty")
	# ASVS 2.1.1, 2.2.1: accept only the documented first-worksheet schema.
	header = tuple(normalize_header(value) for value in raw_header)
	if header != EXPECTED_HEADERS:
		raise ValueError("Google Sheets export has an unsupported header schema")
	entries: list[ScheduleEntry] = []
	previous_stage = ""
	for raw_row in reader:
		if not any(value.strip() for value in raw_row):
			continue
		if len(entries) >= MAX_ROWS:
			raise ValueError("Google Sheets export contains too many rows")
		entry = parse_entry(raw_row, previous_stage)
		if entries and entry.date < entries[-1].date:
			raise ValueError("Google Sheets export is not in chronological order")
		entries.append(entry)
		previous_stage = entry.stage
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
	values = (
		entry.week,
		date_text,
		entry.stage,
		render_multiline_cell(entry.weekly_topic),
		render_multiline_cell(entry.assign),
		render_multiline_cell(entry.assignments_due),
	)
	return f"| {' | '.join(values)} |"


#============================================
def render_markdown(entries: list[ScheduleEntry]) -> str:
	"""Render the full BIOL 480 schedule snapshot."""
	lines = [
		"<!-- Generated by launchers/sync_calendars.py. Do not edit directly. -->",
		"",
		"# Dates and topics",
		"",
		"The **Stage** column groups the semester's course phases. **Assign** and",
		"**Assignments Due** preserve the separate worksheet fields. Shark Tank slides are due",
		"six hours before class. Students complete peer-evaluation forms for the individual and group",
		"presentations and the group-member contribution form for the group project.",
		"",
		f"The schedule is drawn from the [BIOL 480 schedule spreadsheet](https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit).",
		"",
		"| Wk | Date | Stage | Weekly Topic | Assign | Assignments Due |",
		"| ---: | --- | --- | --- | --- | --- |",
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
	"""Fetch, validate, and render the BIOL 480 schedule without writing it."""
	csv_text = fetch_csv_text()
	entries = parse_csv(csv_text)
	markdown = render_markdown(entries)
	return markdown, len(entries)
