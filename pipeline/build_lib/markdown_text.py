"""Encode external text for literal Markdown table cells."""

# Standard Library
import html


WEEK_DASH_MARKERS = ("-", "\u2013", "\u2014")


#============================================
def normalize_spreadsheet_cell(value: str, preserve_lines: bool = False) -> str:
	"""Normalize spreadsheet whitespace and reject unsafe controls and oversized cells."""
	for character in value:
		if ord(character) < 32 and character not in "\t\r\n":
			raise ValueError("Google Sheets export contains a prohibited control character")
	normalized = value.replace("\t", " ")
	if preserve_lines:
		lines = [" ".join(line.split()) for line in normalized.splitlines()]
		normalized = "\n".join(lines).strip()
	else:
		normalized = " ".join(normalized.split())
	return normalized


#============================================
def escape_markdown_cell(value: str) -> str:
	"""Escape HTML and Markdown syntax at the final output boundary."""
	# ASVS 1.1.2, 1.2.1: encode spreadsheet text for its final Markdown context.
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
