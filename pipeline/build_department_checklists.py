#!/usr/bin/env python3
"""Generate one page-referenced department checklist per live syllabus."""

# Standard Library
import re
import sys
import copy
import html
import shutil
import pathlib
import argparse
import tempfile
import subprocess
import importlib.util
import urllib.parse

# PIP3 modules
import yaml
import pypdf

# local repo modules
import build_lib.syllabus_model


ALLOWED_STATUSES = {"covered", "needs_review", "not_applicable"}
REQUIRED_ITEM_KEYS = {"id", "group", "label", "status", "evidence", "note"}


#============================================
def get_repo_root() -> pathlib.Path:
	"""Return the repository root reported by Git."""
	completed = subprocess.run(
		["git", "rev-parse", "--show-toplevel"],
		check=True,
		capture_output=True,
		text=True,
	)
	return pathlib.Path(completed.stdout.strip()).resolve()


#============================================
def require_mapping(value: object, location: str) -> dict[object, object]:
	"""Return a mapping or reject malformed authored checklist data."""
	if not isinstance(value, dict):
		raise ValueError(f"{location} must be a mapping")
	return value


#============================================
def require_text(data: dict[object, object], key: str, location: str) -> str:
	"""Return one required non-empty text value."""
	value = data.get(key)
	if not isinstance(value, str) or not value.strip():
		raise ValueError(f"{location}.{key} must be a non-empty string")
	return value.strip()


#============================================
def validate_evidence(value: object, location: str) -> tuple[dict[str, str], ...]:
	"""Validate evidence labels and site-relative syllabus routes."""
	if not isinstance(value, list):
		raise ValueError(f"{location}.evidence must be a list")
	evidence = []
	for index, raw_link in enumerate(value):
		link_location = f"{location}.evidence[{index}]"
		link = require_mapping(raw_link, link_location)
		if set(link) != {"label", "path"}:
			raise ValueError(f"{link_location} must contain only label and path")
		evidence.append(
			{
				"label": require_text(link, "label", link_location),
				"path": require_text(link, "path", link_location),
			}
		)
	return tuple(evidence)


#============================================
def validate_item(raw_item: object, location: str) -> dict[str, object]:
	"""Validate and normalize one rubric item."""
	item = require_mapping(raw_item, location)
	if set(item) != REQUIRED_ITEM_KEYS:
		raise ValueError(f"{location} must contain exactly {sorted(REQUIRED_ITEM_KEYS)}")
	status = require_text(item, "status", location)
	if status not in ALLOWED_STATUSES:
		raise ValueError(f"{location}.status must be one of {sorted(ALLOWED_STATUSES)}")
	normalized = {
		"id": require_text(item, "id", location),
		"group": require_text(item, "group", location),
		"label": require_text(item, "label", location),
		"status": status,
		"evidence": validate_evidence(item["evidence"], location),
		"note": require_text(item, "note", location),
	}
	if status == "covered" and not normalized["evidence"]:
		raise ValueError(f"{location}: covered items require evidence")
	return normalized


#============================================
def apply_overrides(
	items: list[dict[str, object]],
	raw_overrides: object,
	location: str,
) -> list[dict[str, object]]:
	"""Apply validated course-specific status, note, or evidence replacements."""
	overrides = require_mapping(raw_overrides, location)
	items_by_id = {str(item["id"]): item for item in copy.deepcopy(items)}
	for item_id, raw_override in overrides.items():
		if not isinstance(item_id, str) or item_id not in items_by_id:
			raise ValueError(f"{location}: unknown rubric item {item_id!r}")
		override = require_mapping(raw_override, f"{location}.{item_id}")
		if not set(override).issubset({"status", "note", "evidence"}):
			raise ValueError(f"{location}.{item_id}: unsupported override field")
		item = items_by_id[item_id]
		if "status" in override:
			status = require_text(override, "status", f"{location}.{item_id}")
			if status not in ALLOWED_STATUSES:
				raise ValueError(f"{location}.{item_id}.status is invalid")
			item["status"] = status
		if "note" in override:
			item["note"] = require_text(override, "note", f"{location}.{item_id}")
		if "evidence" in override:
			item["evidence"] = validate_evidence(
				override["evidence"],
				f"{location}.{item_id}",
			)
		if item["status"] == "covered" and not item["evidence"]:
			raise ValueError(f"{location}.{item_id}: covered items require evidence")
	return list(items_by_id.values())


#============================================
def resolve_evidence_source_path(
	manifest: build_lib.syllabus_model.SyllabusManifest,
	course_route: str,
	evidence_path: str,
) -> pathlib.Path:
	"""Resolve one evidence route to its contained Fall 2026 Markdown source."""
	parsed = urllib.parse.urlsplit(evidence_path)
	if parsed.scheme or parsed.netloc or parsed.query or not parsed.path.endswith("/"):
		raise ValueError(f"Evidence path must name a syllabus page route: {evidence_path}")
	term_root = (manifest.docs_root / "fall_2026").resolve()
	course_root = (term_root / course_route).resolve()
	route_text = parsed.path.rstrip("/")
	if route_text in ("", "."):
		source_path = course_root / "index.md"
	else:
		route_path = (course_root / route_text).resolve()
		candidates = (route_path.with_suffix(".md"), route_path / "index.md")
		existing_candidates = tuple(path for path in candidates if path.is_file())
		if len(existing_candidates) != 1:
			raise ValueError(
				f"Evidence route must resolve to exactly one source page: {evidence_path}"
			)
		source_path = existing_candidates[0]
	# ASVS 2.2.1 and 5.3.2: evidence routes resolve only to tracked term Markdown.
	if not source_path.is_relative_to(term_root) or not source_path.is_file():
		raise ValueError(f"Evidence route has no Fall 2026 source page: {evidence_path}")
	return source_path


#============================================
def get_source_page_title(
	manifest: build_lib.syllabus_model.SyllabusManifest,
	course_route: str,
	evidence_path: str,
) -> str:
	"""Return the authoritative H1 for one validated evidence page route."""
	source_path = resolve_evidence_source_path(manifest, course_route, evidence_path)
	for line in source_path.read_text(encoding="utf-8").splitlines():
		if not line.startswith("# "):
			continue
		page_title = re.sub(r"\s+\{[^}]+\}\s*$", "", line[2:]).strip()
		if page_title:
			return page_title
	raise ValueError(f"Evidence source page has no level-one title: {source_path}")


#============================================
def get_evidence_destination_anchor(
	manifest: build_lib.syllabus_model.SyllabusManifest,
	course_route: str,
	evidence_path: str,
) -> str:
	"""Return the named PDF destination for one evidence route and fragment."""
	source_path = resolve_evidence_source_path(manifest, course_route, evidence_path)
	included_paths = manifest.sections + manifest.shared_sections
	if source_path.resolve() not in {path.resolve() for path in included_paths}:
		raise ValueError(f"Evidence page is not included in the complete syllabus: {evidence_path}")
	fragment = urllib.parse.urlsplit(evidence_path).fragment
	if fragment:
		if re.fullmatch(r"[a-z0-9][a-z0-9_-]*", fragment) is None:
			raise ValueError(f"Evidence fragment is not a valid syllabus anchor: {evidence_path}")
		return fragment
	if source_path.resolve() == manifest.sections[0].resolve():
		return "course-overview"
	if source_path.name == "index.md" and source_path.parent.name == "policies":
		return "policies"
	return source_path.stem.lower().replace("_", "-")


#============================================
def load_syllabus_page_map(syllabus_pdf_path: pathlib.Path) -> dict[str, int]:
	"""Return one-based pages for the complete syllabus PDF's named destinations."""
	if not syllabus_pdf_path.is_file():
		raise FileNotFoundError(
			f"Missing complete syllabus PDF: {syllabus_pdf_path}. "
			"Run pipeline/build_syllabi.py before building department checklists."
		)
	reader = pypdf.PdfReader(syllabus_pdf_path)
	page_map = {
		anchor: reader.get_destination_page_number(destination) + 1
		for anchor, destination in reader.named_destinations.items()
	}
	if not page_map:
		raise RuntimeError(f"Complete syllabus has no named destinations: {syllabus_pdf_path}")
	return page_map


#============================================
def format_evidence_location(
	page_number: int,
	page_title: str,
	evidence_label: str,
) -> str:
	"""Combine a syllabus page number and headings without redundant wording."""
	if page_title.casefold() == evidence_label.casefold():
		return f"Syllabus p. {page_number} - {page_title}"
	location = f"Syllabus p. {page_number} - {page_title} - {evidence_label}"
	return location


#============================================
def get_evidence_location(
	manifest: build_lib.syllabus_model.SyllabusManifest,
	course_route: str,
	evidence: dict[str, str],
	page_map: dict[str, int],
) -> str:
	"""Return one self-contained page and heading reference into the syllabus PDF."""
	anchor = get_evidence_destination_anchor(manifest, course_route, evidence["path"])
	if anchor not in page_map:
		raise ValueError(f"Evidence anchor is missing from the complete syllabus PDF: {anchor}")
	page_title = get_source_page_title(manifest, course_route, evidence["path"])
	return format_evidence_location(page_map[anchor], page_title, evidence["label"])


#============================================
def render_checklist(
	manifest: build_lib.syllabus_model.SyllabusManifest,
	course_route: str,
	items: list[dict[str, object]],
	page_map: dict[str, int],
) -> str:
	"""Render one complete department checklist as portable Markdown."""
	lines = [
		f"# {manifest.course_code} {manifest.title} syllabus checklist",
		"",
		f"**Term:** {manifest.term}",
		"",
		f"**Instructor:** {manifest.author}",
		"",
		f"**Reference syllabus:** `{manifest.download_basename}.pdf`",
		"",
		"**Status key:** `[x]` covered or justified as not applicable; "
		"`[ ]` needs department or instructor review.",
		"",
		"Each location gives the page and section in the separate complete syllabus PDF. Notes "
		"labeled **Doubt** identify items that should not be treated as satisfied until their "
		"applicability or wording is confirmed.",
	]
	current_group = ""
	for item in items:
		group = str(item["group"])
		if group != current_group:
			lines.extend(("", f"## {group}", ""))
			current_group = group
		status = str(item["status"])
		checkbox = "x" if status != "needs_review" else " "
		label = str(item["label"])
		locations = [
			get_evidence_location(manifest, course_route, evidence, page_map)
			for evidence in item["evidence"]
		]
		evidence_text = "; ".join(locations)
		note_prefix = "**Doubt:** " if status == "needs_review" else ""
		status_label = "Not applicable" if status == "not_applicable" else "Location"
		lines.append(f"- [{checkbox}] **{label}**")
		if evidence_text:
			lines.append(f"  - {status_label}: {evidence_text}")
		lines.append(f"  - {note_prefix}{item['note']}")
	lines.extend(("", "## Submission note", ""))
	lines.append(
		"This generated checklist documents the current public syllabus; it does not replace department "
		"review or convert an unresolved item into a completed requirement."
	)
	lines.append("")
	return "\n".join(lines)


#============================================
def render_checklist_html(
	manifest: build_lib.syllabus_model.SyllabusManifest,
	course_route: str,
	items: list[dict[str, object]],
	page_map: dict[str, int],
	stylesheet_path: pathlib.Path,
) -> str:
	"""Render one validated checklist as semantic standalone HTML for PDF."""
	resolved_count = sum(item["status"] != "needs_review" for item in items)
	review_count = len(items) - resolved_count
	document_title = f"{manifest.course_code} {manifest.title} syllabus checklist"
	# ASVS 1.1.2 and 1.2.1: escape authored text at the final HTML boundary.
	escaped_title = html.escape(document_title)
	escaped_course = html.escape(f"{manifest.course_code} - {manifest.title}")
	escaped_course_code = html.escape(manifest.course_code)
	escaped_course_title = html.escape(manifest.title)
	escaped_course_color = html.escape(manifest.course_color, quote=True)
	escaped_term = html.escape(manifest.term)
	escaped_author = html.escape(manifest.author)
	escaped_syllabus_name = html.escape(f"{manifest.download_basename}.pdf")
	escaped_language = html.escape(manifest.language, quote=True)
	escaped_stylesheet = html.escape(stylesheet_path.as_uri(), quote=True)
	parts = [
		"<!doctype html>",
		f'<html lang="{escaped_language}">',
		"<head>",
		'<meta charset="utf-8">',
		f"<title>{escaped_title}</title>",
		f'<meta name="author" content="{escaped_author}">',
		f'<link rel="stylesheet" href="{escaped_stylesheet}">',
		"</head>",
		f'<body class="department-checklist" style="--course-accent: '
		f'{escaped_course_color}">',
		'<header class="document-header">',
		'<p class="document-kind">Fall 2026 department syllabus review</p>',
		f'<h1 data-course-label="{escaped_course}">',
		f'<span class="course-code">{escaped_course_code}</span>',
		'<span class="title-stack">',
		f'<span class="course-name">{escaped_course_title}</span>',
		'<span class="checklist-name">Syllabus checklist</span>',
		'</span>',
		'</h1>',
		'<dl class="document-facts">',
		f"<div><dt>Term</dt><dd>{escaped_term}</dd></div>",
		f"<div><dt>Instructor</dt><dd>{escaped_author}</dd></div>",
		f"<div><dt>Resolved</dt><dd>{resolved_count} of {len(items)}</dd></div>",
		f"<div><dt>Needs review</dt><dd>{review_count}</dd></div>",
		"</dl>",
		f'<p class="reference-syllabus"><strong>Reference syllabus:</strong> '
		f"{escaped_syllabus_name}</p>",
		'<p class="status-key"><strong>Status key:</strong> [x] covered or justified as not '
		'applicable; [ ] needs department or instructor review.</p>',
		'<p class="document-purpose">Each location gives the page and section in the separate '
		'complete syllabus PDF.</p>',
		"</header>",
		"<main>",
	]
	current_group = ""
	for item in items:
		group = str(item["group"])
		if group != current_group:
			parts.append(f"<h2>{html.escape(group)}</h2>")
			current_group = group
		status = str(item["status"])
		if status == "covered":
			status_text = "Covered"
		elif status == "not_applicable":
			status_text = "Not applicable"
		else:
			status_text = "Needs review"
		checkbox = "[ ]" if status == "needs_review" else "[x]"
		parts.extend(
			(
				f'<article class="checklist-item checklist-item--{status}">',
				f'<span class="checklist-mark" aria-label="{status_text}">{checkbox}</span>',
				'<div class="checklist-content">',
				f"<h3>{html.escape(str(item['label']))}</h3>",
				f'<p class="status-label">{status_text}</p>',
			)
		)
		evidence = item["evidence"]
		if evidence:
			parts.append('<ul class="evidence-list">')
			for evidence_reference in evidence:
				location = get_evidence_location(
					manifest,
					course_route,
					evidence_reference,
					page_map,
				)
				escaped_location = html.escape(location)
				parts.append(f"<li><strong>Location:</strong> {escaped_location}</li>")
			parts.append("</ul>")
		note_prefix = "<strong>Doubt:</strong> " if status == "needs_review" else ""
		parts.append(f'<p class="item-note">{note_prefix}{html.escape(str(item["note"]))}</p>')
		parts.extend(("</div>", "</article>"))
	parts.extend(
		(
			"<h2>Submission note</h2>",
			'<p class="submission-note">This generated checklist documents the current public '
			'syllabus. It does not replace department review or convert an unresolved item into a '
			'completed requirement.</p>',
			"</main>",
			"</body>",
			"</html>",
			"",
		)
	)
	document = "\n".join(parts)
	return document


#============================================
def run_weasyprint_pdf(html_path: pathlib.Path, pdf_path: pathlib.Path) -> None:
	"""Render one tagged checklist PDF from trusted staged HTML."""
	# ASVS 1.2.5: pass fixed local artifact paths without a shell.
	command = [
		sys.executable,
		"-m",
		"weasyprint",
		"--pdf-tags",
		str(html_path),
		str(pdf_path),
	]
	subprocess.run(command, check=True)
	if not pdf_path.is_file():
		raise RuntimeError(f"WeasyPrint did not create {pdf_path}")
	return None


#============================================
def verify_pdf_output(pdf_path: pathlib.Path, items: list[dict[str, object]]) -> None:
	"""Require a tagged, letter-size checklist PDF containing every rubric item."""
	metadata = subprocess.run(
		["pdfinfo", str(pdf_path)],
		check=True,
		capture_output=True,
		text=True,
	).stdout
	if re.search(r"^Page size:\s+612 x 792 pts", metadata, re.MULTILINE) is None:
		raise RuntimeError(f"{pdf_path}: PDF is not US letter size")
	if re.search(r"^Tagged:\s+yes\s*$", metadata, re.MULTILINE | re.IGNORECASE) is None:
		raise RuntimeError(f"{pdf_path}: PDF is not tagged")
	font_report = subprocess.run(
		["pdffonts", str(pdf_path)],
		check=True,
		capture_output=True,
		text=True,
	).stdout
	hyperlegible_fonts = [
		line.split()
		for line in font_report.splitlines()
		if "Atkinson-Hyperlegible-Next" in line
	]
	if not hyperlegible_fonts:
		raise RuntimeError(f"{pdf_path}: Atkinson Hyperlegible Next is not embedded")
	if any(font[-5:-2] != ["yes", "yes", "yes"] for font in hyperlegible_fonts):
		raise RuntimeError(f"{pdf_path}: Hyperlegible font lacks embedded Unicode subsets")
	reader = pypdf.PdfReader(pdf_path)
	if not reader.pages:
		raise RuntimeError(f"{pdf_path}: PDF contains no pages")
	for page in reader.pages:
		for annotation_reference in page.get("/Annots", []):
			annotation = annotation_reference.get_object()
			if annotation.get("/Subtype") == "/Link":
				raise RuntimeError(f"{pdf_path}: separate checklist contains a link annotation")
	text_content = subprocess.run(
		["pdftotext", str(pdf_path), "-"],
		check=True,
		capture_output=True,
		text=True,
	).stdout
	normalized_text = " ".join(text_content.split())
	for item in items:
		label = " ".join(str(item["label"]).split())
		if label not in normalized_text:
			raise RuntimeError(f"{pdf_path}: missing rubric item {label!r}")
	if "Location:" not in normalized_text:
		raise RuntimeError(f"{pdf_path}: PDF contains no visible evidence locations")
	if "Syllabus p." not in normalized_text:
		raise RuntimeError(f"{pdf_path}: PDF contains no syllabus page references")
	return None


#============================================
def check_tools() -> None:
	"""Require the deterministic document tools used by the checklist generator."""
	for tool_name in ("pandoc", "pdffonts", "pdfinfo", "pdftotext"):
		if shutil.which(tool_name) is None:
			raise RuntimeError(f"Required checklist tool is not installed: {tool_name}")
	if importlib.util.find_spec("weasyprint") is None:
		raise RuntimeError("Required PDF renderer is missing: install pip_requirements.txt")
	return None


#============================================
def rebuild_syllabi(repo_root: pathlib.Path) -> None:
	"""Rebuild complete syllabi so checklist page references cannot be stale."""
	# ASVS 1.2.5: run the repository-owned builder with a fixed interpreter and no shell.
	subprocess.run(
		[sys.executable, "pipeline/build_syllabi.py"],
		cwd=repo_root,
		check=True,
	)
	return None


#============================================
def load_configuration(config_path: pathlib.Path) -> dict[object, object]:
	"""Safely deserialize and validate the top-level checklist configuration."""
	# ASVS 1.5.2: safe_load prevents authored YAML from constructing arbitrary Python objects.
	loaded = yaml.safe_load(config_path.read_text(encoding="utf-8"))
	configuration = require_mapping(loaded, str(config_path))
	if set(configuration) != {"items", "courses"}:
		raise ValueError(f"{config_path}: expected items and courses")
	return configuration


#============================================
def build_checklists(repo_root: pathlib.Path, output_dir: pathlib.Path) -> tuple[pathlib.Path, ...]:
	"""Generate Markdown, DOCX, and PDF checklists for every configured course."""
	config_path = repo_root / "pipeline" / "department_checklists.yml"
	configuration = load_configuration(config_path)
	raw_items = configuration["items"]
	if not isinstance(raw_items, list) or not raw_items:
		raise ValueError(f"{config_path}: items must be a non-empty list")
	items = [validate_item(value, f"items[{index}]") for index, value in enumerate(raw_items)]
	item_ids = [str(item["id"]) for item in items]
	if len(item_ids) != len(set(item_ids)):
		raise ValueError(f"{config_path}: item IDs must be unique")
	raw_courses = configuration["courses"]
	if not isinstance(raw_courses, list) or not raw_courses:
		raise ValueError(f"{config_path}: courses must be a non-empty list")
	output_root = (repo_root / "department_checklists").resolve()
	resolved_output = output_dir.resolve()
	# ASVS 2.2.1 and 5.3.2: writes stay within the documented output boundary.
	if not resolved_output.is_relative_to(output_root):
		raise ValueError(f"Output directory must stay within {output_root}")
	resolved_output.mkdir(parents=True, exist_ok=True)
	stylesheet_path = repo_root / "pipeline" / "department_checklist_pdf.css"
	if not stylesheet_path.is_file():
		raise FileNotFoundError(f"Missing checklist PDF stylesheet: {stylesheet_path}")
	font_root = repo_root / "site_docs" / "assets" / "fonts"
	for font_name in (
		"atkinson_hyperlegible_next.woff2",
		"atkinson_hyperlegible_next_italic.woff2",
	):
		font_path = font_root / font_name
		if not font_path.is_file():
			raise FileNotFoundError(f"Missing checklist PDF font: {font_path}")
	check_tools()
	generated_paths = []
	# ASVS 5.3.2: intermediate files stay inside the validated generated-output root.
	with tempfile.TemporaryDirectory(prefix=".department_checklist_", dir=resolved_output) as temp_dir:
		temporary_dir = pathlib.Path(temp_dir)
		for index, raw_course in enumerate(raw_courses):
			location = f"courses[{index}]"
			course = require_mapping(raw_course, location)
			if set(course) != {"directory", "overrides"}:
				raise ValueError(f"{location} must contain exactly directory and overrides")
			course_route = require_text(course, "directory", location)
			if not course_route.isidentifier() or course_route.lower() != course_route:
				raise ValueError(f"{location}.directory must be a lowercase identifier")
			manifest_path = repo_root / "site_docs" / "fall_2026" / course_route / "syllabus.yml"
			manifest = build_lib.syllabus_model.load_manifest(manifest_path, repo_root / "site_docs")
			course_items = apply_overrides(items, course["overrides"], f"{location}.overrides")
			syllabus_pdf_path = (
				repo_root / "site_docs" / "downloads" / f"{manifest.download_basename}.pdf"
			)
			page_map = load_syllabus_page_map(syllabus_pdf_path)
			markdown = render_checklist(manifest, course_route, course_items, page_map)
			basename = build_lib.syllabus_model.format_course_document_basename(
				manifest.course_code,
				manifest.term,
				"Department_Checklist",
			)
			markdown_path = resolved_output / f"{basename}.md"
			docx_path = resolved_output / f"{basename}.docx"
			pdf_path = resolved_output / f"{basename}.pdf"
			html_path = temporary_dir / f"{basename}.html"
			markdown_path.write_text(markdown, encoding="utf-8")
			subprocess.run(
				[
					"pandoc",
					str(markdown_path),
					"--from=gfm",
					f"--reference-doc={repo_root / 'pipeline' / 'syllabus_reference.docx'}",
					f"--output={docx_path}",
				],
				check=True,
			)
			html_document = render_checklist_html(
				manifest,
				course_route,
				course_items,
				page_map,
				stylesheet_path,
			)
			html_path.write_text(html_document, encoding="utf-8")
			run_weasyprint_pdf(html_path, pdf_path)
			verify_pdf_output(pdf_path, course_items)
			generated_paths.extend((markdown_path, docx_path, pdf_path))
			print(f"Built {markdown_path.name}, {docx_path.name}, and {pdf_path.name}")
	return tuple(generated_paths)


#============================================
def parse_args(repo_root: pathlib.Path) -> argparse.Namespace:
	"""Parse the contained output-directory option."""
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument(
		"--output-dir",
		type=pathlib.Path,
		default=repo_root / "department_checklists",
		help="directory at or below repository-root department_checklists",
	)
	return parser.parse_args()


#============================================
def main() -> None:
	"""Build all configured department checklists."""
	repo_root = get_repo_root()
	args = parse_args(repo_root)
	rebuild_syllabi(repo_root)
	build_checklists(repo_root, args.output_dir)


if __name__ == "__main__":
	main()
