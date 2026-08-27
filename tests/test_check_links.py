"""Tests for the external Markdown link checker."""

# Standard Library
import pathlib

# local repo modules
import check_links


#============================================
def test_extract_links_reports_sources_and_ignores_code_fences(tmp_path: pathlib.Path) -> None:
	"""Real Markdown links are found without treating examples as destinations."""
	markdown_path = tmp_path / "page.md"
	markdown_path.write_text(
		"# Links\n\n[Policy](https://example.com/policy)\n\n"
		"```markdown\n[Example](https://invalid.example/)\n```\n"
		"<https://example.com/help>\n",
		encoding="utf-8",
	)

	links = check_links.extract_links(markdown_path)

	assert set(links) == {"https://example.com/policy", "https://example.com/help"}
	assert links["https://example.com/policy"][0].line_number == 3


#============================================
def test_extract_links_unescapes_markdown_query_characters(tmp_path: pathlib.Path) -> None:
	"""Escaped ampersands and underscores become their requested URL characters."""
	markdown_path = tmp_path / "page.md"
	markdown_path.write_text(
		"[Form](https://example.com/form?a=1\\&layout\\_id=2)\n",
		encoding="utf-8",
	)

	links = check_links.extract_links(markdown_path)

	assert list(links) == ["https://example.com/form?a=1&layout_id=2"]


#============================================
def test_extract_links_accepts_iso_8859_1_source(tmp_path: pathlib.Path) -> None:
	"""Legacy repository Markdown encoding does not prevent URL discovery."""
	markdown_path = tmp_path / "page.md"
	markdown_path.write_bytes(b"Caf\xe9: [Help](https://example.com/help)\n")

	links = check_links.extract_links(markdown_path)

	assert list(links) == ["https://example.com/help"]


#============================================
def test_describe_soft_error_detects_error_url_and_html_title() -> None:
	"""HTTP 200 error destinations still fail the link audit."""
	error_url = check_links.describe_soft_error(
		"https://example.com/error.php?issue=noredirect",
		"text/html; charset=utf-8",
		b"<title>Welcome</title>",
	)
	error_title = check_links.describe_soft_error(
		"https://example.com/page",
		"text/html; charset=utf-8",
		b"<html><title>404 - Page Not Found</title></html>",
	)

	assert error_url == "redirected to an error page"
	assert error_title == "error page title: 404 - Page Not Found"


#============================================
def test_discover_markdown_files_rejects_non_markdown(tmp_path: pathlib.Path) -> None:
	"""Explicit non-Markdown inputs fail before any network requests occur."""
	text_path = tmp_path / "links.txt"
	text_path.write_text("https://example.com", encoding="utf-8")

	try:
		check_links.discover_markdown_files([text_path])
	except ValueError as error:
		assert "expected a Markdown file" in str(error)
	else:
		raise AssertionError("non-Markdown input was accepted")
