#!/usr/bin/env python3
"""Report the content-derived widths for Markdown tables without building the site."""

# Standard Library
import re
import sys
import json
import html
import pathlib
import argparse
import collections
from dataclasses import asdict


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
PIPELINE_ROOT = REPO_ROOT / "pipeline"
if str(PIPELINE_ROOT) not in sys.path:
	sys.path.insert(0, str(PIPELINE_ROOT))

# local repo modules
import build_lib.syllabus_content
import build_lib.table_layouts


LINK_PATTERN = re.compile(r"!?(\[[^]]*\])\([^)]*\)")
HTML_TAG_PATTERN = re.compile(r"<[^>]+>")
MARKDOWN_PUNCTUATION_PATTERN = re.compile(r"[*_~`]")


#============================================
def visible_markdown_text(cell_text: str) -> str:
	"""Approximate the visible label of one validated Markdown table cell."""
	def keep_label(match: re.Match[str]) -> str:
		return match.group(1)[1:-1]

	text = LINK_PATTERN.sub(keep_label, cell_text)
	text = HTML_TAG_PATTERN.sub(" ", text)
	text = MARKDOWN_PUNCTUATION_PATTERN.sub("", text)
	return " ".join(html.unescape(text).split())


#============================================
def markdown_tables(
	markdown_text: str,
	source_label: str,
) -> tuple[tuple[int, tuple[str, ...], tuple[tuple[str, ...], ...]], ...]:
	"""Extract validated pipe tables with their one-based source line numbers."""
	build_lib.syllabus_content.validate_markdown_tables(markdown_text, source_label)
	lines = markdown_text.splitlines()
	tables = []
	line_index = 0
	while line_index < len(lines):
		line = lines[line_index].strip()
		if not line.startswith("|") or not line.endswith("|"):
			line_index += 1
			continue
		block_start = line_index
		block_lines = []
		while line_index < len(lines):
			candidate = lines[line_index].strip()
			if not candidate.startswith("|") or not candidate.endswith("|"):
				break
			block_lines.append(candidate)
			line_index += 1
		headers = tuple(
			visible_markdown_text(cell)
			for cell in build_lib.syllabus_content.split_markdown_table_row(block_lines[0])
		)
		body_rows = tuple(
			tuple(
				visible_markdown_text(cell)
				for cell in build_lib.syllabus_content.split_markdown_table_row(row)
			)
			for row in block_lines[2:]
		)
		tables.append((block_start + 1, headers, body_rows))
	return tuple(tables)


#============================================
def resolve_markdown_paths(input_paths: tuple[pathlib.Path, ...]) -> tuple[pathlib.Path, ...]:
	"""Resolve Markdown files from explicit files or directories."""
	markdown_paths = set()
	for input_path in input_paths:
		resolved_path = input_path.resolve()
		if not resolved_path.exists():
			raise FileNotFoundError(f"Input does not exist: {input_path}")
		if resolved_path.is_file():
			if resolved_path.suffix.lower() != ".md":
				raise ValueError(f"Input file is not Markdown: {input_path}")
			markdown_paths.add(resolved_path)
			continue
		for markdown_path in resolved_path.rglob("*.md"):
			if {"downloads", "generated"}.intersection(markdown_path.parts):
				continue
			markdown_paths.add(markdown_path.resolve())
	return tuple(sorted(markdown_paths))


#============================================
def build_report(markdown_paths: tuple[pathlib.Path, ...]) -> list[dict[str, object]]:
	"""Calculate layouts for every table in the selected Markdown sources."""
	report = []
	for markdown_path in markdown_paths:
		markdown_text = markdown_path.read_text(encoding="utf-8")
		parsed_tables = markdown_tables(
			markdown_text,
			str(markdown_path),
		)
		layouts = build_lib.table_layouts.calculate_shared_table_layouts(
			tuple(
				(headers, body_rows)
				for _line_number, headers, body_rows in parsed_tables
			)
		)
		series_sizes = collections.Counter(headers for _line, headers, _rows in parsed_tables)
		for (line_number, headers, _body_rows), layout in zip(
			parsed_tables,
			layouts,
			strict=True,
		):
			try:
				display_path = markdown_path.relative_to(REPO_ROOT)
			except ValueError:
				display_path = markdown_path
			report.append(
				{
					"path": str(display_path),
					"line": line_number,
					"headers": headers,
					"series_size": series_sizes[headers],
					**asdict(layout),
				}
			)
	return report


#============================================
def print_report(report: list[dict[str, object]]) -> None:
	"""Print one compact, human-readable layout report."""
	for table in report:
		compact_label = "compact" if table["is_compact"] else "full-width"
		print(
			f"{table['path']}:{table['line']}  {table['profile']}  "
			f"{table['minimum_width_ch']}ch  {compact_label}  "
			f"series {table['series_size']}"
		)
		for header, demand, percentage in zip(
			table["headers"],
			table["column_demands"],
			table["column_percentages"],
			strict=True,
		):
			print(f"  {percentage:>3}%  demand {demand:>2}ch  {header}")
	print(f"\n{len(report)} table(s) analyzed")
	return None


#============================================
def main() -> int:
	"""Run the read-only Markdown table width calculator."""
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument(
		"inputs",
		nargs="*",
		type=pathlib.Path,
		default=(REPO_ROOT / "site_docs" / "fall_2026",),
		help="Markdown files or directories (default: site_docs/fall_2026)",
	)
	parser.add_argument("--json", action="store_true", help="emit JSON instead of text")
	arguments = parser.parse_args()
	input_paths = tuple(arguments.inputs) or (REPO_ROOT / "site_docs" / "fall_2026",)
	markdown_paths = resolve_markdown_paths(input_paths)
	report = build_report(markdown_paths)
	if arguments.json:
		print(json.dumps(report, indent="\t"))
	else:
		print_report(report)
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
