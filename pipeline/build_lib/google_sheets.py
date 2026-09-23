"""Read bounded CSV exports from fixed, public Google Sheets sources."""

# Standard Library
import re
import time
import random
import http.client
import urllib.parse
import urllib.request


MAX_RESPONSE_BYTES = 1_000_000
SPREADSHEET_ID_PATTERN = re.compile(r"[A-Za-z0-9_-]{20,120}")


class GoogleRedirectHandler(urllib.request.HTTPRedirectHandler):
	"""Follow only HTTPS redirects to Google-owned export hosts."""

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
		"""Validate each export redirect before following it."""
		# ASVS 15.3.2: only the intentional Google export redirects are followed.
		validate_google_url(newurl)
		redirected_request = super().redirect_request(req, fp, code, msg, headers, newurl)
		return redirected_request


#============================================
def validate_google_url(url: str) -> None:
	"""Require HTTPS on a Google Sheets export host."""
	parsed_url = urllib.parse.urlsplit(url)
	hostname = parsed_url.hostname
	allowed_host = hostname == "docs.google.com"
	if hostname is not None and hostname.endswith(".googleusercontent.com"):
		allowed_host = True
	# ASVS 12.3.1, 12.3.2, 13.2.4: allow only TLS-validated Google hosts.
	if parsed_url.scheme != "https" or not allowed_host or parsed_url.port not in (None, 443):
		raise ValueError("Google Sheets export redirected to an unsupported location")
	return None


#============================================
def fetch_csv_text(spreadsheet_id: str, user_agent: str) -> str:
	"""Fetch the first worksheet as a bounded UTF-8 CSV document."""
	if SPREADSHEET_ID_PATTERN.fullmatch(spreadsheet_id) is None:
		raise ValueError("Google Sheets export has an unsupported spreadsheet ID")
	export_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv"
	validate_google_url(export_url)
	request = urllib.request.Request(export_url, headers={"User-Agent": user_agent})
	opener = urllib.request.build_opener(GoogleRedirectHandler())
	# Pause briefly before the request, per the repository network-client convention.
	time.sleep(random.random())
	# ASVS 13.2.6: use a fixed timeout and avoid retries that can amplify outages.
	with opener.open(request, timeout=30) as response:
		validate_google_url(response.geturl())
		# ASVS 4.1.1: accept only CSV with an optional UTF-8 charset.
		if response.headers.get_content_type() != "text/csv":
			raise ValueError("Google Sheets export did not return CSV content")
		charset = response.headers.get_content_charset()
		if charset is not None and charset.lower().replace("-", "") != "utf8":
			raise ValueError("Google Sheets export did not return UTF-8 content")
		body = response.read(MAX_RESPONSE_BYTES + 1)
	# ASVS 2.2.1: bound external data before decoding or parsing it.
	if len(body) > MAX_RESPONSE_BYTES:
		raise ValueError("Google Sheets export exceeded the allowed response size")
	return body.decode("utf-8-sig")
