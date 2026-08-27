#!/usr/bin/env python3
"""Check external links in the public syllabus Markdown sources."""

# Standard Library
import re
import sys
import socket
import pathlib
import ipaddress
import argparse
import urllib.error
import urllib.parse
import urllib.request
import concurrent.futures
from dataclasses import dataclass


DEFAULT_SOURCE = pathlib.Path("site_docs")
MAX_SOURCE_BYTES = 2_000_000
MAX_RESPONSE_BYTES = 128_000
DEFAULT_TIMEOUT_SECONDS = 20.0
DEFAULT_WORKERS = 6
USER_AGENT = "Roosevelt-Syllabus-Link-Checker/1.0"
LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(\s*(https?://[^\s)]+)")
AUTOLINK_PATTERN = re.compile(r"<(https?://[^>]+)>")
TITLE_PATTERN = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
SOFT_ERROR_PATTERN = re.compile(
	r"\b(?:404|page not found|not found|no redirect|link expired)\b",
	re.IGNORECASE,
)


@dataclass(frozen=True)
class LinkSource:
	"""One source location for an external link."""

	path: pathlib.Path
	line_number: int


@dataclass(frozen=True)
class LinkResult:
	"""The network result for one unique URL."""

	url: str
	status: int | None
	final_url: str
	detail: str
	ok: bool


#============================================
def parse_args() -> argparse.Namespace:
	"""Parse command-line arguments.

	Returns:
		argparse.Namespace: Validated command-line values.
	"""
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument(
		"paths",
		nargs="*",
		type=pathlib.Path,
		default=[DEFAULT_SOURCE],
		help="Markdown file or directory to scan (default: site_docs)",
	)
	parser.add_argument(
		"--timeout",
		type=float,
		default=DEFAULT_TIMEOUT_SECONDS,
		help=f"seconds allowed per request (default: {DEFAULT_TIMEOUT_SECONDS:g})",
	)
	parser.add_argument(
		"--workers",
		type=int,
		default=DEFAULT_WORKERS,
		help=f"concurrent requests (default: {DEFAULT_WORKERS})",
	)
	args = parser.parse_args()
	if not 1.0 <= args.timeout <= 120.0:
		parser.error("--timeout must be between 1 and 120 seconds")
	if not 1 <= args.workers <= 16:
		parser.error("--workers must be between 1 and 16")
	return args


#============================================
def discover_markdown_files(paths: list[pathlib.Path]) -> list[pathlib.Path]:
	"""Return the Markdown files selected by the user.

	Args:
		paths: Files or directories from the command line.

	Returns:
		list[pathlib.Path]: Unique resolved Markdown file paths.

	Raises:
		ValueError: If an input is missing, unsupported, or too large.
	"""
	files = set()
	for raw_path in paths:
		path = raw_path.resolve()
		if not path.exists():
			raise ValueError(f"path does not exist: {raw_path}")
		candidates = path.rglob("*.md") if path.is_dir() else (path,)
		for candidate in candidates:
			if candidate.suffix.lower() != ".md" or not candidate.is_file():
				raise ValueError(f"expected a Markdown file: {candidate}")
			# ASVS 2.2.1: bound file inputs before loading them into memory.
			if candidate.stat().st_size > MAX_SOURCE_BYTES:
				raise ValueError(f"Markdown file exceeds {MAX_SOURCE_BYTES} bytes: {candidate}")
			files.add(candidate.resolve())
	return sorted(files)


#============================================
def extract_links(path: pathlib.Path) -> dict[str, list[LinkSource]]:
	"""Extract HTTP(S) Markdown destinations and their line numbers.

	Args:
		path: Markdown source file.

	Returns:
		dict[str, list[LinkSource]]: URLs mapped to source locations.
	"""
	links: dict[str, list[LinkSource]] = {}
	in_fence = False
	source_bytes = path.read_bytes()
	try:
		text = source_bytes.decode("utf-8")
	except UnicodeDecodeError:
		# Repository Markdown may use the documented ISO-8859-1 source encoding.
		text = source_bytes.decode("iso-8859-1")
	for line_number, line in enumerate(text.splitlines(), start=1):
		stripped = line.lstrip()
		if stripped.startswith("```") or stripped.startswith("~~~"):
			in_fence = not in_fence
			continue
		if in_fence:
			continue
		for pattern in (LINK_PATTERN, AUTOLINK_PATTERN):
			for match in pattern.finditer(line):
				url = match.group(1).replace(r"\&", "&").replace(r"\_", "_")
				links.setdefault(url, []).append(LinkSource(path, line_number))
	return links


#============================================
def validate_public_url(url: str) -> None:
	"""Reject unsafe schemes, credentials, ports, and non-public destinations.

	Args:
		url: Link or redirect destination.

	Raises:
		ValueError: If the URL could access an unsafe network destination.
	"""
	# ASVS 1.2.2 and 2.2.1: positively validate the complete outbound URL.
	parsed = urllib.parse.urlsplit(url)
	if parsed.scheme not in {"http", "https"} or not parsed.hostname:
		raise ValueError("only absolute HTTP(S) URLs are allowed")
	if parsed.username is not None or parsed.password is not None:
		raise ValueError("URLs containing credentials are not allowed")
	try:
		port = parsed.port
	except ValueError as error:
		raise ValueError("URL contains an invalid port") from error
	if port not in {None, 80, 443}:
		raise ValueError("only ports 80 and 443 are allowed")
	addresses = socket.getaddrinfo(parsed.hostname, port or 443, type=socket.SOCK_STREAM)
	for address in addresses:
		ip = ipaddress.ip_address(address[4][0])
		if not ip.is_global:
			raise ValueError(f"non-public destination is not allowed: {ip}")


class SafeRedirectHandler(urllib.request.HTTPRedirectHandler):
	"""Validate every redirect target before urllib follows it."""

	def redirect_request(
		self,
		req: urllib.request.Request,
		fp: object,
		code: int,
		msg: str,
		headers: object,
		newurl: str,
	) -> urllib.request.Request | None:
		"""Return a redirect request only for a validated public URL."""
		validate_public_url(newurl)
		return super().redirect_request(req, fp, code, msg, headers, newurl)


#============================================
def describe_soft_error(final_url: str, content_type: str, body: bytes) -> str:
	"""Identify common error pages that incorrectly return HTTP 200.

	Args:
		final_url: URL after redirects.
		content_type: Response Content-Type header.
		body: Bounded response prefix.

	Returns:
		str: Failure detail, or an empty string for a normal response.
	"""
	parsed = urllib.parse.urlsplit(final_url)
	if parsed.path.lower().endswith("/error.php"):
		return "redirected to an error page"
	if "html" not in content_type.lower():
		return ""
	text = body.decode("utf-8", errors="replace")
	title_match = TITLE_PATTERN.search(text)
	if title_match and SOFT_ERROR_PATTERN.search(title_match.group(1)):
		return f"error page title: {title_match.group(1).strip()}"
	return ""


#============================================
def check_url(url: str, timeout: float) -> LinkResult:
	"""Fetch one URL and classify HTTP and soft-page failures.

	Args:
		url: Public HTTP(S) destination.
		timeout: Maximum request duration in seconds.

	Returns:
		LinkResult: Bounded result suitable for the CLI report.
	"""
	try:
		validate_public_url(url)
		request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
		opener = urllib.request.build_opener(SafeRedirectHandler())
		# ASVS 4.1.1: inspect the response Content-Type before parsing its body.
		with opener.open(request, timeout=timeout) as response:
			status = response.status
			final_url = response.geturl()
			content_type = response.headers.get("Content-Type", "")
			body = response.read(MAX_RESPONSE_BYTES)
		soft_error = describe_soft_error(final_url, content_type, body)
		if soft_error:
			return LinkResult(url, status, final_url, soft_error, False)
		return LinkResult(url, status, final_url, "", status < 400)
	except urllib.error.HTTPError as error:
		if error.code == 401:
			return LinkResult(
				url,
				error.code,
				error.geturl(),
				"authentication required",
				True,
			)
		return LinkResult(url, error.code, error.geturl(), str(error.reason), False)
	except (OSError, ValueError, urllib.error.URLError) as error:
		return LinkResult(url, None, url, f"{type(error).__name__}: {error}", False)


#============================================
def merge_link_sources(files: list[pathlib.Path]) -> dict[str, list[LinkSource]]:
	"""Collect unique URLs and all source locations from Markdown files."""
	all_links: dict[str, list[LinkSource]] = {}
	for path in files:
		for url, sources in extract_links(path).items():
			all_links.setdefault(url, []).extend(sources)
	return all_links


#============================================
def format_sources(sources: list[LinkSource]) -> str:
	"""Format source locations as a compact comma-separated list."""
	return ", ".join(f"{source.path}:{source.line_number}" for source in sources)


#============================================
def main() -> int:
	"""Run the external-link audit and return a shell-friendly status."""
	args = parse_args()
	try:
		files = discover_markdown_files(args.paths)
	except (OSError, UnicodeError, ValueError) as error:
		print(f"ERROR: {error}", file=sys.stderr)
		return 2
	links = merge_link_sources(files)
	print(f"Checking {len(links)} unique HTTP(S) links from {len(files)} Markdown files...")
	with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
		future_results = {
			executor.submit(check_url, url, args.timeout): url for url in sorted(links)
		}
		results = [future.result() for future in concurrent.futures.as_completed(future_results)]
	failures = 0
	redirects = 0
	authenticated = 0
	for result in sorted(results, key=lambda item: item.url):
		if result.final_url != result.url:
			redirects += 1
		if result.ok:
			if result.status == 401:
				authenticated += 1
				print(f"AUTH 401: {result.url}")
				print(f"  source: {format_sources(links[result.url])}")
			continue
		failures += 1
		status = str(result.status) if result.status is not None else "NETWORK"
		print(f"FAIL {status}: {result.url}")
		if result.final_url != result.url:
			print(f"  final: {result.final_url}")
		print(f"  detail: {result.detail}")
		print(f"  source: {format_sources(links[result.url])}")
	print(
		f"Checked {len(links)} links: {len(links) - failures} passed, "
		f"{failures} failed, {authenticated} require authentication, "
		f"{redirects} redirected."
	)
	return 1 if failures else 0


if __name__ == "__main__":
	sys.exit(main())
