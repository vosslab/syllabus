"""Parse and render the Fall 2026 Genetics schedule worksheet."""

# Standard Library
import io
import re
import csv
import pathlib
import datetime

# local repo modules
import build_lib.google_sheets
import build_lib.markdown_text


SPREADSHEET_ID = "1XLZcg8PnW4GyMxFctAKCTvzN9qImIb5S3bK6hyeDz0Q"
USER_AGENT = "vosslab-syllabus-calendar-sync/1.0"
OUTPUT_RELATIVE_PATH = pathlib.Path("site_docs/fall_2026/genetics/SCHEDULE.md")
MAX_ROWS = 1_000
EXPECTED_HEADERS = (
	"wk",
	"lect",
	"date",
	"lecture",
	"quiz",
	"in-class activity",
	"quiz",
	"assign due",
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


class ScheduleEntry:
	"""One validated row from the Genetics worksheet."""

	def __init__(
		self,
		week: str,
		lecture_number: str,
		date: datetime.date,
		topic: str,
		activity: str,
		quiz_coverage: str,
		quiz_due: str,
		assignments_due: str,
	) -> None:
		self.week = week
		self.lecture_number = lecture_number
		self.date = date
		self.topic = topic
		self.activity = activity
		self.quiz_coverage = quiz_coverage
		self.quiz_due = quiz_due
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
def normalize_number(value: str, field_name: str) -> str:
	"""Validate a week or lecture number, preserving an explicit no-number marker."""
	number = normalize_cell(value)
	if number == "" or number in build_lib.markdown_text.WEEK_DASH_MARKERS:
		return "-"
	if not number.isdigit() or not 1 <= int(number) <= 20:
		raise ValueError(f"Google Sheets export contains an unsupported {field_name} value")
	return str(int(number))


#============================================
def normalize_quiz(value: str, due_date: bool = False) -> str:
	"""Validate a quiz coverage number or a quiz due marker."""
	quiz = normalize_cell(value)
	if quiz == "" or quiz in build_lib.markdown_text.WEEK_DASH_MARKERS:
		return ""
	if due_date:
		match = re.fullmatch(r"Q([1-5])", quiz, re.IGNORECASE)
		if match is None:
			raise ValueError("Google Sheets export contains an unsupported quiz due value")
		return match.group(1)
	if not quiz.isdigit() or not 1 <= int(quiz) <= 5:
		raise ValueError("Google Sheets export contains an unsupported quiz coverage value")
	return str(int(quiz))


#============================================
def parse_entry(raw_row: list[str]) -> ScheduleEntry:
	"""Validate and convert one rectangular worksheet row."""
	if len(raw_row) != len(EXPECTED_HEADERS):
		raise ValueError("Google Sheets export contains a row with the wrong number of columns")
	(
		week_text,
		lecture_number_text,
		date_text,
		topic_text,
		quiz_coverage_text,
		activity_text,
		quiz_due_text,
		assignments_due_text,
	) = raw_row
	week = normalize_number(week_text, "week")
	lecture_number = normalize_number(lecture_number_text, "lecture number")
	date = parse_date(normalize_cell(date_text))
	topic = normalize_cell(topic_text, preserve_lines=True)
	activity = normalize_cell(activity_text, preserve_lines=True)
	quiz_coverage = normalize_quiz(quiz_coverage_text)
	quiz_due = normalize_quiz(quiz_due_text, due_date=True)
	assignments_due = normalize_cell(assignments_due_text, preserve_lines=True)
	if assignments_due in build_lib.markdown_text.WEEK_DASH_MARKERS:
		assignments_due = ""
	if not any((topic, activity, quiz_coverage, quiz_due, assignments_due)):
		raise ValueError("Google Sheets export contains a schedule row without details")
	return ScheduleEntry(
		week,
		lecture_number,
		date,
		topic,
		activity,
		quiz_coverage,
		quiz_due,
		assignments_due,
	)


#============================================
def parse_csv(csv_text: str) -> list[ScheduleEntry]:
	"""Validate the eight-column sheet schema and return chronological schedule rows."""
	reader = csv.reader(io.StringIO(csv_text, newline=""))
	raw_header = next(reader, None)
	if raw_header is None:
		raise ValueError("Google Sheets export is empty")
	# ASVS 2.1.1, 2.2.1: accept only the documented first-worksheet schema.
	header = tuple(normalize_header(value) for value in raw_header)
	if header != EXPECTED_HEADERS:
		raise ValueError("Google Sheets export has an unsupported header schema")
	entries: list[ScheduleEntry] = []
	for raw_row in reader:
		if not any(value.strip() for value in raw_row):
			continue
		if len(entries) >= MAX_ROWS:
			raise ValueError("Google Sheets export contains too many rows")
		entry = parse_entry(raw_row)
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
def render_quiz_number(number: str) -> str:
	"""Render an explicit quiz label with its supplementary color cue."""
	return f'<span class="schedule-quiz-key schedule-quiz-key--{number}">Quiz {number}</span>'


#============================================
def render_table_row(entry: ScheduleEntry) -> str:
	"""Render one validated schedule entry as a tall, two-column Markdown row."""
	date_text = (
		f"{WEEKDAY_NAMES[entry.date.weekday()]}, "
		f"{MONTH_ABBREVIATIONS[entry.date.month]} {entry.date.day}"
	)
	first_cell_lines = []
	if entry.week != "-":
		first_cell_lines.append(f"Week {entry.week}")
	if entry.lecture_number != "-":
		first_cell_lines.append(f"Lecture {entry.lecture_number}")
	first_cell_lines.append(date_text)
	details = []
	if entry.topic:
		details.append(f"**Topic:** {render_multiline_cell(entry.topic)}")
	if entry.activity:
		details.append(f"**Activity:** {render_multiline_cell(entry.activity)}")
	if entry.quiz_coverage:
		details.append(f"**Quiz coverage:** {render_quiz_number(entry.quiz_coverage)}")
	if entry.quiz_due:
		details.append(f"**Quiz due:** {render_quiz_number(entry.quiz_due)}")
	if entry.assignments_due:
		details.append(f"**Assignments due:** {render_multiline_cell(entry.assignments_due)}")
	values = ("<br>".join(first_cell_lines), "<br>".join(details))
	return f"| {' | '.join(values)} |"


#============================================
def render_markdown(entries: list[ScheduleEntry]) -> str:
	"""Render the full Genetics schedule snapshot and its source link."""
	spreadsheet_url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit"
	lines = [
		"<!-- Generated by launchers/sync_calendars.py. Do not edit directly. -->",
		"",
		"# Dates and topics",
		"",
		f"The schedule is drawn from the [Genetics schedule spreadsheet]({spreadsheet_url}).",
		"",
		"**Quiz coverage** names the topics included; **Quiz due** marks the date the quiz is scheduled.",
		"Quiz numbers remain explicit, with color serving as a visual cue. Assignment numbers name",
		"the work due on that date. Chapter numbers in **Topic** refer to the Genetics LibreTexts.",
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
	"""Fetch, validate, and render the Genetics schedule without writing it."""
	csv_text = fetch_csv_text()
	entries = parse_csv(csv_text)
	markdown = render_markdown(entries)
	return markdown, len(entries)
