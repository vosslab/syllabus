"""Synchronize the Fall 2026 important-dates tables from their Google Sheet."""

# Standard Library
import io
import re
import csv
import html
import time
import random
import pathlib
import datetime
import http.client
import subprocess
import urllib.parse
import urllib.request


SPREADSHEET_ID = "1YuK02ObBJgxFlQSLx0xtKdaLNBfuOgM466Hh6MRQczE"
SPREADSHEET_CSV_URL = (
	f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=csv"
)
OUTPUT_RELATIVE_PATH = pathlib.Path("site_docs/generated/FALL_2026_IMPORTANT_DATES.md")
MAX_RESPONSE_BYTES = 1_000_000
MAX_ROWS = 1_000
MAX_FIELD_CHARACTERS = 2_000
EXPECTED_HEADERS = ("date", "confirmed", "wk", "x", "event", "notes")
DATE_PATTERN = re.compile(
	r"^(Mon|Tue|Wed|Thu|Fri|Sat|Sun), "
	r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) "
	r"([0-9]{2}), ([0-9]{4})$"
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
MONTH_NAMES = (
	"",
	"January",
	"February",
	"March",
	"April",
	"May",
	"June",
	"July",
	"August",
	"September",
	"October",
	"November",
	"December",
)
WEEKDAY_NAMES = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
CATEGORY_RULES = (
	(
		"Holidays and closures",
		("holiday", "no classes", "closing", "intersession break", "martin luther"),
	),
	(
		"Registration and withdrawal",
		(
			"registration",
			"register",
			"add a class",
			"drop a class",
			"drop class",
			"refund",
			"schedule goes live",
		),
	),
	(
		"Graduation",
		("graduation", "commencement", "degree conferral", "degrees posted", "thesis"),
	),
	(
		"Grades and evaluations",
		(
			"progress report",
			"attendance reporting",
			"reporting due",
			"grades due",
			"grades available",
			"course evaluations",
			"evaluation results",
			"mid-term grades",
		),
	),
	(
		"Classes and exams",
		("first day of", "classes end", "final exam period"),
	),
	(
		"Faculty and department",
		(
			"faculty conference",
			"grant proposal",
			"book orders",
			"poster presentations",
			"conference",
		),
	),
	("Student support", ("student support", "esl support")),
	("University event", ("convocation",)),
)


class CalendarEntry:
	"""One validated row from the important-dates worksheet."""

	def __init__(
		self,
		date: datetime.date,
		event: str,
		category: str,
	) -> None:
		self.date = date
		self.event = event
		self.category = category


class GoogleRedirectHandler(urllib.request.HTTPRedirectHandler):
	"""Follow only the HTTPS Google redirects required by the CSV export."""

	#============================================
	def redirect_request(
		self,
		req: urllib.request.Request,
		fp: http.client.HTTPResponse,
		code: int,
		msg: str,
		headers: http.client.HTTPMessage,
		newurl: str,
	) -> urllib.request.Request | None:
		"""Validate each Google export redirect before following it."""
		# ASVS 15.3.2: required redirects stay on expected Google HTTPS hosts.
		validate_google_url(newurl)
		redirected_request = super().redirect_request(req, fp, code, msg, headers, newurl)
		return redirected_request


#============================================
def get_repo_root() -> pathlib.Path:
	"""Return the repository root reported by Git."""
	completed = subprocess.run(
		["git", "rev-parse", "--show-toplevel"],
		check=True,
		capture_output=True,
		text=True,
	)
	repo_root = pathlib.Path(completed.stdout.strip())
	return repo_root


#============================================
def validate_google_url(url: str) -> None:
	"""Require an HTTPS URL on an expected Google document host."""
	parsed_url = urllib.parse.urlsplit(url)
	hostname = parsed_url.hostname
	allowed_host = hostname == "docs.google.com"
	if hostname is not None and hostname.endswith(".googleusercontent.com"):
		allowed_host = True
	# ASVS 12.3.1, 12.3.2, 13.2.4: use TLS validation and a host allowlist.
	if parsed_url.scheme != "https" or not allowed_host or parsed_url.port not in (None, 443):
		raise ValueError("Google Sheets export redirected to an unsupported location")
	return None


#============================================
def fetch_csv_text() -> str:
	"""Download the first worksheet as a bounded UTF-8 CSV document."""
	validate_google_url(SPREADSHEET_CSV_URL)
	request = urllib.request.Request(
		SPREADSHEET_CSV_URL,
		headers={"User-Agent": "vosslab-syllabus-calendar-sync/1.0"},
	)
	opener = urllib.request.build_opener(GoogleRedirectHandler())
	# Pause briefly before the request, per the repository network-client convention.
	time.sleep(random.random())
	# ASVS 13.2.6: the external request has a fixed timeout and no retry storm.
	with opener.open(request, timeout=30) as response:
		validate_google_url(response.geturl())
		# ASVS 4.1.1: require the documented CSV response type and UTF-8 charset.
		if response.headers.get_content_type() != "text/csv":
			raise ValueError("Google Sheets export did not return CSV content")
		charset = response.headers.get_content_charset()
		if charset is not None and charset.lower().replace("-", "") != "utf8":
			raise ValueError("Google Sheets export did not return UTF-8 content")
		body = response.read(MAX_RESPONSE_BYTES + 1)
	# ASVS 2.2.1: reject oversized remote data before decoding or parsing it.
	if len(body) > MAX_RESPONSE_BYTES:
		raise ValueError("Google Sheets export exceeded the allowed response size")
	csv_text = body.decode("utf-8-sig")
	return csv_text


#============================================
def normalize_cell(value: str) -> str:
	"""Normalize safe spreadsheet typography and whitespace for ASCII Markdown."""
	for character in value:
		if ord(character) < 32 and character not in "\t\r\n":
			raise ValueError("Google Sheets export contains a prohibited control character")
	translations = str.maketrans(
		{
			"\u2013": "-",
			"\u2014": "-",
			"\u2212": "-",
			"\u2018": "'",
			"\u2019": "'",
			"\u201c": '"',
			"\u201d": '"',
			"\ufe0e": "",
			"\ufe0f": "",
		}
	)
	normalized = " ".join(value.translate(translations).split())
	if len(normalized) > MAX_FIELD_CHARACTERS:
		raise ValueError("Google Sheets export contains an oversized cell")
	# Repository Markdown accepts ASCII and ISO-8859-1; reject other characters.
	normalized.encode("iso-8859-1")
	return normalized


#============================================
def normalize_header(value: str) -> str:
	"""Convert a worksheet header into its expected canonical name."""
	header = normalize_cell(value).lower()
	if re.fullmatch(r"confirmed for [0-9]{4}", header) is not None:
		header = "confirmed"
	return header


#============================================
def parse_date(value: str) -> datetime.date:
	"""Parse and cross-check the worksheet's fixed English date format."""
	match = DATE_PATTERN.fullmatch(value)
	if match is None:
		raise ValueError("Google Sheets export contains a date in an unsupported format")
	weekday_text, month_text, day_text, year_text = match.groups()
	parsed_date = datetime.date(int(year_text), MONTH_NUMBERS[month_text], int(day_text))
	if WEEKDAY_NAMES[parsed_date.weekday()] != weekday_text:
		raise ValueError("Google Sheets export contains a date with the wrong weekday")
	return parsed_date


#============================================
def normalize_marker(value: str, blank_value: str) -> str:
	"""Convert a checkbox-like worksheet cell to a readable ASCII marker."""
	marker = value.strip().replace("\ufe0e", "").replace("\ufe0f", "")
	if marker.lower() in ("x", "yes", "true") or marker in ("\u2713", "\u2714"):
		return "Yes"
	if marker.lower() in ("", "-", "\u2013", "no", "false"):
		return blank_value
	raise ValueError("Google Sheets export contains an unsupported checkbox marker")


#============================================
def normalize_week(value: str) -> str:
	"""Validate a semester week number or an explicit non-week marker."""
	week = normalize_cell(value)
	if week == "-":
		return week
	if not week.isdigit() or not 1 <= int(week) <= 20:
		raise ValueError("Google Sheets export contains an unsupported week value")
	return week


#============================================
def categorize_event(event: str) -> str:
	"""Infer a stable scanning category from the event wording."""
	event_lower = event.lower()
	for category, phrases in CATEGORY_RULES:
		if any(phrase in event_lower for phrase in phrases):
			return category
	return "Other"


#============================================
def parse_entry(raw_row: list[str]) -> CalendarEntry:
	"""Validate and convert one rectangular worksheet row."""
	if len(raw_row) != len(EXPECTED_HEADERS):
		raise ValueError("Google Sheets export contains a row with the wrong number of columns")
	date_text, confirmed_text, week_text, x_text, event_text, notes_text = raw_row
	event = normalize_cell(event_text)
	if event == "":
		raise ValueError("Google Sheets export contains an event without a name")
	# Confirmation, week, X, and notes are maintainer metadata rather than page content.
	normalize_marker(confirmed_text, "No")
	normalize_week(week_text)
	normalize_marker(x_text, "-")
	normalize_cell(notes_text)
	entry = CalendarEntry(
		date=parse_date(normalize_cell(date_text)),
		event=event,
		category=categorize_event(event),
	)
	return entry


#============================================
def parse_csv(csv_text: str) -> list[CalendarEntry]:
	"""Validate the predictable first-worksheet schema and return its entries."""
	reader = csv.reader(io.StringIO(csv_text, newline=""))
	raw_header = next(reader, None)
	if raw_header is None:
		raise ValueError("Google Sheets export is empty")
	# ASVS 2.1.1, 2.2.1: accept only the documented six-column worksheet schema.
	header = tuple(normalize_header(value) for value in raw_header)
	if header != EXPECTED_HEADERS:
		raise ValueError("Google Sheets export has an unsupported header schema")
	entries: list[CalendarEntry] = []
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
		raise ValueError("Google Sheets export contains no calendar entries")
	return entries


#============================================
def escape_markdown_cell(value: str) -> str:
	"""Encode remote text for safe literal rendering in a Markdown table cell."""
	# ASVS 1.1.2, 1.2.1: encode at the final Markdown/HTML output boundary.
	escaped = html.escape(value, quote=False)
	markdown_replacements = {
		"\\": "&#92;",
		"|": "&#124;",
		"[": "&#91;",
		"]": "&#93;",
		"*": "&#42;",
		"_": "&#95;",
		"`": "&#96;",
		"~": "&#126;",
	}
	for character, replacement in markdown_replacements.items():
		escaped = escaped.replace(character, replacement)
	return escaped


#============================================
def render_table_row(entry: CalendarEntry) -> str:
	"""Render one validated calendar entry as a Markdown table row."""
	date_text = (
		f"{WEEKDAY_NAMES[entry.date.weekday()]}, "
		f"{MONTH_ABBREVIATIONS[entry.date.month]} {entry.date.day:02d}"
	)
	values = (
		date_text,
		entry.event,
		entry.category,
	)
	escaped_values = [escape_markdown_cell(value) for value in values]
	row = f"| {' | '.join(escaped_values)} |"
	return row


#============================================
def render_markdown(entries: list[CalendarEntry]) -> str:
	"""Render entries as visually separated month tables for the page wrapper."""
	lines = [
		"<!-- Generated by pipeline/sync_important_dates.py. Do not edit directly. -->",
	]
	current_month: tuple[int, int] | None = None
	for entry in entries:
		entry_month = (entry.date.year, entry.date.month)
		if entry_month != current_month:
			if current_month is not None:
				lines.extend(("", "---"))
			month_title = f"{MONTH_NAMES[entry.date.month]} {entry.date.year}"
			lines.extend(
				(
					"",
					f"## {month_title}",
					"",
					"| Date | Event | Type |",
					"| --- | --- | --- |",
				)
			)
			current_month = entry_month
		lines.append(render_table_row(entry))
	markdown = "\n".join(lines) + "\n"
	return markdown


#============================================
def write_markdown(markdown: str, output_path: pathlib.Path) -> None:
	"""Write a fully validated page to the trusted repository destination."""
	# ASVS 5.3.2: the caller supplies one code-owned path, never spreadsheet data.
	output_path.parent.mkdir(parents=True, exist_ok=True)
	output_path.write_text(markdown, encoding="utf-8")
	return None


#============================================
def main() -> None:
	"""Refresh the ignored important-dates fragment from the first worksheet."""
	repo_root = get_repo_root()
	output_path = repo_root / OUTPUT_RELATIVE_PATH
	# ASVS 16.5.2, 16.5.3: validate and render in memory before replacing the good page.
	csv_text = fetch_csv_text()
	entries = parse_csv(csv_text)
	markdown = render_markdown(entries)
	write_markdown(markdown, output_path)
	print(f"Updated {OUTPUT_RELATIVE_PATH} with {len(entries)} important dates.")
	return None


if __name__ == "__main__":
	main()
