"""Build complete DOCX and PDF syllabi from course manifests."""

# Standard Library
import os
import re
import sys
import html
import shutil
import pathlib
import zipfile
import argparse
import tempfile
import subprocess
import dataclasses
import importlib.util

# PIP3 modules
import docx
import yaml
import pypdf
import markdown
import docx.oxml
import docx.oxml.ns


SECRET_PATTERNS = (
	re.compile(r"zoom\.us/j/", re.IGNORECASE),
	re.compile(r"\bpwd=", re.IGNORECASE),
	re.compile(r"\b(?:passcode|password)\s*[:=]", re.IGNORECASE),
	re.compile(r"discord(?:\.gg|\.com/invite)/", re.IGNORECASE),
)


@dataclasses.dataclass(frozen=True)
class SyllabusManifest:
	"""Validated paths and metadata for one complete syllabus."""

	path: pathlib.Path
	title: str
	course_code: str
	term: str
	author: str
	language: str
	status: str
	publication_status: str
	download_basename: str
	sections: tuple[pathlib.Path, ...]
	shared_sections: tuple[pathlib.Path, ...]


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
def require_text(data: dict[object, object], key: str, manifest_path: pathlib.Path) -> str:
	"""Return one required, non-empty string field from manifest data."""
	value = data[key]
	if not isinstance(value, str) or not value.strip():
		raise ValueError(f"{manifest_path}: {key} must be a non-empty string")
	text_value = value.strip()
	return text_value


#============================================
def resolve_sources(
	data: dict[object, object],
	key: str,
	manifest_path: pathlib.Path,
	docs_root: pathlib.Path,
) -> tuple[pathlib.Path, ...]:
	"""Resolve and validate an ordered manifest source list."""
	value = data[key]
	if not isinstance(value, list) or not value:
		raise ValueError(f"{manifest_path}: {key} must be a non-empty list")
	resolved_paths = []
	for item in value:
		if not isinstance(item, str) or not item.strip():
			raise ValueError(f"{manifest_path}: {key} entries must be non-empty strings")
		candidate = (manifest_path.parent / item).resolve()
		if not candidate.is_relative_to(docs_root.resolve()):
			raise ValueError(f"{manifest_path}: source escapes site_docs: {item}")
		if not candidate.is_file():
			raise FileNotFoundError(f"{manifest_path}: missing source: {item}")
		resolved_paths.append(candidate)
	sources = tuple(resolved_paths)
	return sources


#============================================
def load_manifest(manifest_path: pathlib.Path, docs_root: pathlib.Path) -> SyllabusManifest:
	"""Load one YAML manifest and reject incomplete or unsafe values."""
	loaded = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
	if not isinstance(loaded, dict):
		raise ValueError(f"{manifest_path}: manifest root must be a mapping")
	title = require_text(loaded, "title", manifest_path)
	course_code = require_text(loaded, "course_code", manifest_path)
	term = require_text(loaded, "term", manifest_path)
	author = require_text(loaded, "author", manifest_path)
	language = require_text(loaded, "language", manifest_path)
	status = require_text(loaded, "status", manifest_path)
	publication_status = require_text(loaded, "publication_status", manifest_path)
	download_basename = require_text(loaded, "download_basename", manifest_path)
	if status not in {"current", "archived"}:
		raise ValueError(f"{manifest_path}: status must be current or archived")
	if publication_status not in {"draft", "approved"}:
		raise ValueError(f"{manifest_path}: publication_status must be draft or approved")
	if re.fullmatch(r"[A-Z0-9_]+", download_basename) is None:
		raise ValueError(f"{manifest_path}: download_basename must use A-Z, 0-9, and underscores")
	sections = resolve_sources(loaded, "sections", manifest_path, docs_root)
	shared_sections = resolve_sources(loaded, "shared_sections", manifest_path, docs_root)
	manifest = SyllabusManifest(
		path=manifest_path,
		title=title,
		course_code=course_code,
		term=term,
		author=author,
		language=language,
		status=status,
		publication_status=publication_status,
		download_basename=download_basename,
		sections=sections,
		shared_sections=shared_sections,
	)
	return manifest


#============================================
def scan_text_for_secrets(text_value: str, source_label: str) -> None:
	"""Reject public content that resembles meeting credentials or invite links."""
	for pattern in SECRET_PATTERNS:
		match = pattern.search(text_value)
		if match is not None:
			raise ValueError(f"{source_label}: prohibited public credential pattern: {match.group(0)}")
	return None


#============================================
def scan_public_sources(docs_root: pathlib.Path) -> None:
	"""Scan tracked-shape public text sources before generating downloads."""
	for suffix in ("*.md", "*.yml", "*.yaml"):
		for source_path in sorted(docs_root.rglob(suffix)):
			if "downloads" in source_path.parts:
				continue
			content = source_path.read_text(encoding="utf-8")
			scan_text_for_secrets(content, str(source_path))
	return None


#============================================
def normalize_admonitions(markdown: str) -> str:
	"""Convert Material admonitions into portable Markdown for Pandoc."""
	lines = markdown.splitlines()
	normalized = []
	in_admonition = False
	for line in lines:
		match = re.fullmatch(r'!!!\s+[-\w]+(?:\s+"([^"]+)")?\s*', line)
		if match is not None:
			title = match.group(1)
			if title is None:
				title = "Note"
			normalized.append(f"**{title}**")
			in_admonition = True
			continue
		if in_admonition and line.startswith("    "):
			normalized.append(line[4:])
			continue
		if in_admonition and not line.strip():
			normalized.append("")
			continue
		in_admonition = False
		normalized.append(line)
	result = "\n".join(normalized)
	return result


#============================================
def prepare_section(markdown: str, is_overview: bool, anchor: str) -> str:
	"""Remove web-only controls and demote headings for the merged document."""
	without_downloads = re.sub(
		r'<div class="syllabus-downloads".*?</div>\s*',
		"",
		markdown,
		flags=re.DOTALL,
	)
	if is_overview:
		without_navigation = re.sub(
			r"^## (?:Course pages|Find what you need)\s*$.*?(?=^## |\Z)",
			"",
			without_downloads,
			count=1,
			flags=re.MULTILINE | re.DOTALL,
		)
	else:
		without_navigation = without_downloads
	lines = []
	anchored_heading = False
	for line in without_navigation.splitlines():
		match = re.match(r"^(#{1,6})(\s+.*)$", line)
		if match is None:
			lines.append(line)
			continue
		level = min(len(match.group(1)) + 1, 6)
		heading_suffix = match.group(2)
		if not anchored_heading:
			heading_suffix += f" {{#{anchor}}}"
			anchored_heading = True
		lines.append("#" * level + heading_suffix)
	prepared = "\n".join(lines).strip() + "\n"
	return prepared


#============================================
def load_markdown_configuration(
	config_path: pathlib.Path,
) -> tuple[tuple[str, ...], dict[str, dict[object, object]]]:
	"""Load the Python-Markdown extension stack used by the MkDocs site."""
	loaded = yaml.safe_load(config_path.read_text(encoding="utf-8"))
	if not isinstance(loaded, dict):
		raise ValueError(f"{config_path}: configuration root must be a mapping")
	if "markdown_extensions" not in loaded:
		raise ValueError(f"{config_path}: missing markdown_extensions")
	configured_extensions = loaded["markdown_extensions"]
	if not isinstance(configured_extensions, list) or not configured_extensions:
		raise ValueError(f"{config_path}: markdown_extensions must be a non-empty list")
	extension_names = []
	extension_configs = {}
	for item in configured_extensions:
		if isinstance(item, str):
			extension_names.append(item)
			continue
		if not isinstance(item, dict) or len(item) != 1:
			raise ValueError(f"{config_path}: invalid markdown extension entry: {item!r}")
		extension_name, settings = next(iter(item.items()))
		if not isinstance(extension_name, str):
			raise ValueError(f"{config_path}: markdown extension names must be strings")
		if settings is None:
			settings = {}
		if not isinstance(settings, dict):
			raise ValueError(f"{config_path}: {extension_name} settings must be a mapping")
		extension_names.append(extension_name)
		extension_configs[extension_name] = dict(settings)
	extensions = tuple(extension_names)
	return extensions, extension_configs


#============================================
def get_section_title(markdown: str, source_path: pathlib.Path) -> str:
	"""Return the first level-one heading from one section source."""
	match = re.search(r"^#\s+(.+?)\s*$", markdown, re.MULTILINE)
	if match is None:
		raise ValueError(f"{source_path}: section must begin with a level-one heading")
	title = match.group(1)
	return title


#============================================
def verify_required_section_titles(
	output_text: str,
	manifest: SyllabusManifest,
	output_path: pathlib.Path,
) -> None:
	"""Require every manifest source heading in one generated document."""
	normalized_output = re.sub(r"\s+", " ", output_text).casefold()
	missing_titles = []
	for source_path in manifest.sections + manifest.shared_sections:
		source_markdown = source_path.read_text(encoding="utf-8")
		section_title = get_section_title(source_markdown, source_path)
		normalized_title = re.sub(r"\s+", " ", section_title).casefold()
		if normalized_title not in normalized_output:
			missing_titles.append(section_title)
	if missing_titles:
		missing_text = ", ".join(missing_titles)
		raise RuntimeError(f"{output_path}: missing manifest sections: {missing_text}")
	return None


#============================================
def verify_download_links(manifest: SyllabusManifest, downloads_dir: pathlib.Path) -> None:
	"""Require overview download targets derived from manifest output names."""
	overview_path = manifest.sections[0]
	overview_markdown = overview_path.read_text(encoding="utf-8")
	for suffix in (".pdf", ".docx"):
		target_path = downloads_dir / f"{manifest.download_basename}{suffix}"
		relative_path = pathlib.Path(os.path.relpath(target_path, overview_path.parent)).as_posix()
		if relative_path not in overview_markdown:
			raise RuntimeError(f"{overview_path}: missing complete-download link: {relative_path}")
	return None


#============================================
def compose_markdown(manifest: SyllabusManifest) -> str:
	"""Compose course and shared sources in manifest order."""
	parts = []
	contents = ["# Contents", ""]
	for index, section_path in enumerate(manifest.sections):
		markdown = section_path.read_text(encoding="utf-8")
		anchor = "course-overview" if index == 0 else section_path.stem.lower().replace("_", "-")
		title = "Course overview" if index == 0 else get_section_title(markdown, section_path)
		contents.append(f"- [{title}](#{anchor})")
		parts.append(prepare_section(markdown, is_overview=index == 0, anchor=anchor))
	for section_path in manifest.shared_sections:
		markdown = section_path.read_text(encoding="utf-8")
		anchor = section_path.stem.lower().replace("_", "-")
		title = get_section_title(markdown, section_path)
		contents.append(f"- [{title}](#{anchor})")
		parts.append(prepare_section(markdown, is_overview=False, anchor=anchor))
	contents.append("")
	if manifest.publication_status == "draft":
		contents.extend(
			[
				"**DRAFT - NOT APPROVED FOR DISTRIBUTION**",
				"",
				"Dates, grading, assignment details, and course-specific policies require review.",
				"",
			]
		)
	combined = "\n".join(contents) + "\n" + "\n\n".join(parts)
	scan_text_for_secrets(combined, str(manifest.path))
	return combined


#============================================
def mark_table_header(row: object) -> None:
	"""Mark one DOCX row as a repeating semantic table header."""
	properties = row._tr.get_or_add_trPr()
	if properties.find(docx.oxml.ns.qn("w:tblHeader")) is None:
		header = docx.oxml.OxmlElement("w:tblHeader")
		header.set(docx.oxml.ns.qn("w:val"), "true")
		properties.append(header)
	return None


#============================================
def format_table_header(row: object) -> None:
	"""Make table headers distinct through both bold text and light shading."""
	mark_table_header(row)
	for cell in row.cells:
		cell_properties = cell._tc.get_or_add_tcPr()
		shading = cell_properties.find(docx.oxml.ns.qn("w:shd"))
		if shading is None:
			shading = docx.oxml.OxmlElement("w:shd")
			cell_properties.append(shading)
		shading.set(docx.oxml.ns.qn("w:fill"), "E6E6E6")
		for paragraph in cell.paragraphs:
			for run in paragraph.runs:
				run.bold = True
	return None


#============================================
def prevent_row_split(row: object) -> None:
	"""Keep a DOCX table row from splitting across pages."""
	properties = row._tr.get_or_add_trPr()
	if properties.find(docx.oxml.ns.qn("w:cantSplit")) is None:
		cant_split = docx.oxml.OxmlElement("w:cantSplit")
		properties.append(cant_split)
	return None


#============================================
def set_document_language(document: object, language_code: str) -> None:
	"""Set the proofing language on paragraph and character styles."""
	for style in document.styles:
		run_properties = style.element.get_or_add_rPr()
		language = run_properties.find(docx.oxml.ns.qn("w:lang"))
		if language is None:
			language = docx.oxml.OxmlElement("w:lang")
			run_properties.append(language)
		language.set(docx.oxml.ns.qn("w:val"), language_code)
	return None


#============================================
def postprocess_docx(docx_path: pathlib.Path, manifest: SyllabusManifest) -> None:
	"""Apply metadata, language, and table accessibility properties."""
	document = docx.Document(docx_path)
	document.core_properties.title = f"{manifest.course_code}: {manifest.title} - {manifest.term}"
	document.core_properties.author = manifest.author
	document.core_properties.subject = "Complete course syllabus"
	document.core_properties.language = manifest.language
	set_document_language(document, manifest.language)
	for table in document.tables:
		table.style = "Table"
		table.autofit = True
		if table.rows:
			format_table_header(table.rows[0])
		for row in table.rows:
			prevent_row_split(row)
	document.save(docx_path)
	return None


#============================================
def audit_docx_structure(docx_path: pathlib.Path, manifest: SyllabusManifest) -> None:
	"""Report non-blocking DOCX accessibility findings."""
	document = docx.Document(docx_path)
	accessibility_findings = []
	expected_title = f"{manifest.course_code}: {manifest.title} - {manifest.term}"
	if document.core_properties.title != expected_title:
		accessibility_findings.append("missing expected document title metadata")
	if document.core_properties.language != manifest.language:
		accessibility_findings.append("missing expected document language metadata")
	heading_paragraphs = [
		paragraph
		for paragraph in document.paragraphs
		if paragraph.style.name.startswith("Heading ")
	]
	if not heading_paragraphs:
		accessibility_findings.append("no semantic heading styles found")
	if not document.tables:
		accessibility_findings.append("no semantic tables found")
	for table in document.tables:
		header_properties = table.rows[0]._tr.get_or_add_trPr()
		if header_properties.find(docx.oxml.ns.qn("w:tblHeader")) is None:
			accessibility_findings.append("table is missing a repeating header row")
	for finding in accessibility_findings:
		print(f"Accessibility advisory: {docx_path}: {finding}")
	return None


#============================================
def verify_docx_output(docx_path: pathlib.Path, manifest: SyllabusManifest) -> None:
	"""Require a readable DOCX package containing every manifest section."""
	document = docx.Document(docx_path)
	paragraph_text = "\n".join(paragraph.text for paragraph in document.paragraphs)
	verify_required_section_titles(paragraph_text, manifest, docx_path)
	return None


#============================================
def run_pandoc_docx(
	markdown_path: pathlib.Path,
	docx_path: pathlib.Path,
	reference_path: pathlib.Path,
	manifest: SyllabusManifest,
) -> None:
	"""Generate one complete DOCX through Pandoc."""
	command = [
		"pandoc",
		str(markdown_path),
		"--from=markdown+pipe_tables",
		"--to=docx",
		f"--reference-doc={reference_path}",
		f"--metadata=title:{manifest.course_code}: {manifest.title}",
		f"--metadata=subtitle:{manifest.term}",
		f"--metadata=author:{manifest.author}",
		f"--metadata=lang:{manifest.language}",
		f"--output={docx_path}",
	]
	subprocess.run(command, check=True)
	return None


#============================================
def run_markdown_html(
	markdown_text: str,
	html_path: pathlib.Path,
	stylesheet_path: pathlib.Path,
	manifest: SyllabusManifest,
	extensions: tuple[str, ...],
	extension_configs: dict[str, dict[object, object]],
) -> None:
	"""Render semantic standalone HTML with the site's Markdown extension stack."""
	converter = markdown.Markdown(
		extensions=list(extensions),
		extension_configs=extension_configs,
		output_format="html5",
	)
	body_html = converter.convert(markdown_text)
	document_title = f"{manifest.course_code}: {manifest.title} - {manifest.term}"
	escaped_title = html.escape(document_title)
	escaped_course_title = html.escape(f"{manifest.course_code}: {manifest.title}")
	escaped_term = html.escape(manifest.term)
	escaped_author = html.escape(manifest.author)
	escaped_language = html.escape(manifest.language, quote=True)
	document = "\n".join(
		[
			"<!doctype html>",
			f'<html lang="{escaped_language}">',
			"<head>",
			'<meta charset="utf-8">',
			f"<title>{escaped_title}</title>",
			f'<meta name="author" content="{escaped_author}">',
			f'<link rel="stylesheet" href="{stylesheet_path.as_uri()}">',
			"</head>",
			'<body class="syllabus-document">',
			'<header id="title-block-header">',
			f"<h1>{escaped_course_title}</h1>",
			f'<p class="subtitle">{escaped_term}</p>',
			f'<p class="author">{escaped_author}</p>',
			"</header>",
			'<main id="syllabus-content">',
			body_html,
			"</main>",
			"</body>",
			"</html>",
			"",
		]
	)
	html_path.write_text(document, encoding="utf-8")
	return None


#============================================
def run_weasyprint_pdf(
	html_path: pathlib.Path,
	pdf_path: pathlib.Path,
) -> None:
	"""Render standalone syllabus HTML directly to a tagged PDF."""
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
def verify_pdf_output(pdf_path: pathlib.Path, manifest: SyllabusManifest) -> None:
	"""Require a usable PDF and report non-blocking accessibility findings."""
	metadata = subprocess.run(
		["pdfinfo", str(pdf_path)],
		check=True,
		capture_output=True,
		text=True,
	).stdout
	if re.search(r"^Page size:\s+612 x 792 pts", metadata, re.MULTILINE) is None:
		raise RuntimeError(f"{pdf_path}: PDF is not US letter size")
	reader = pypdf.PdfReader(pdf_path)
	if not reader.pages:
		raise RuntimeError(f"{pdf_path}: PDF contains no pages")
	text_content = subprocess.run(
		["pdftotext", str(pdf_path), "-"],
		check=True,
		capture_output=True,
		text=True,
	).stdout
	if len(text_content.strip()) < 100:
		raise RuntimeError(f"{pdf_path}: PDF does not contain enough selectable text")
	verify_required_section_titles(text_content, manifest, pdf_path)
	scan_text_for_secrets(text_content, str(pdf_path))
	accessibility_findings = []
	if re.search(r"^Tagged:\s+yes\s*$", metadata, re.MULTILINE | re.IGNORECASE) is None:
		accessibility_findings.append("PDF is not tagged")
	if not reader.outline:
		accessibility_findings.append("PDF has no heading bookmarks")
	for finding in accessibility_findings:
		print(f"Accessibility advisory: {pdf_path}: {finding}")
	return None


#============================================
def scan_docx_for_secrets(docx_path: pathlib.Path) -> None:
	"""Scan all XML text stored in one generated DOCX."""
	with zipfile.ZipFile(docx_path) as archive:
		xml_parts = []
		for member_name in archive.namelist():
			if member_name.endswith(".xml"):
				xml_parts.append(archive.read(member_name).decode("utf-8", errors="replace"))
	combined_xml = "\n".join(xml_parts)
	scan_text_for_secrets(combined_xml, str(docx_path))
	return None


#============================================
def check_tools() -> None:
	"""Require the lightweight document tools needed for complete exports."""
	for tool_name in ("pandoc", "pdfinfo", "pdftotext"):
		if shutil.which(tool_name) is None:
			raise RuntimeError(f"Required export tool is not installed: {tool_name}")
	if importlib.util.find_spec("weasyprint") is None:
		raise RuntimeError("Required PDF renderer is missing: install pip_requirements.txt")
	return None


#============================================
def reset_downloads(downloads_dir: pathlib.Path) -> None:
	"""Remove generated document artifacts before rebuilding the managed directory."""
	downloads_dir.mkdir(parents=True, exist_ok=True)
	for artifact_path in downloads_dir.iterdir():
		if artifact_path.is_file() and artifact_path.suffix.lower() in {".docx", ".pdf"}:
			artifact_path.unlink()
	return None


#============================================
def build_one_syllabus(
	manifest: SyllabusManifest,
	downloads_dir: pathlib.Path,
	reference_path: pathlib.Path,
	pdf_stylesheet_path: pathlib.Path,
	markdown_extensions: tuple[str, ...],
	markdown_extension_configs: dict[str, dict[object, object]],
	temporary_dir: pathlib.Path,
) -> tuple[pathlib.Path, pathlib.Path]:
	"""Build sibling DOCX and PDF outputs from one composed Markdown source."""
	verify_download_links(manifest, downloads_dir)
	combined_markdown = compose_markdown(manifest)
	docx_markdown_path = temporary_dir / f"{manifest.download_basename}_docx.md"
	docx_markdown_path.write_text(normalize_admonitions(combined_markdown), encoding="utf-8")
	docx_path = downloads_dir / f"{manifest.download_basename}.docx"
	run_pandoc_docx(docx_markdown_path, docx_path, reference_path, manifest)
	postprocess_docx(docx_path, manifest)
	verify_docx_output(docx_path, manifest)
	audit_docx_structure(docx_path, manifest)
	scan_docx_for_secrets(docx_path)
	html_path = temporary_dir / f"{manifest.download_basename}.html"
	run_markdown_html(
		combined_markdown,
		html_path,
		pdf_stylesheet_path,
		manifest,
		markdown_extensions,
		markdown_extension_configs,
	)
	pdf_path = downloads_dir / f"{manifest.download_basename}.pdf"
	run_weasyprint_pdf(html_path, pdf_path)
	verify_pdf_output(pdf_path, manifest)
	print(f"Built {docx_path.name} and {pdf_path.name}")
	outputs = (docx_path, pdf_path)
	return outputs


#============================================
def archive_outputs(
	outputs_by_term: dict[str, list[pathlib.Path]],
	archive_dir: pathlib.Path,
) -> None:
	"""Create one archival ZIP file per term."""
	archive_dir.mkdir(parents=True, exist_ok=True)
	for term, output_paths in sorted(outputs_by_term.items()):
		term_slug = re.sub(r"[^A-Z0-9]+", "_", term.upper()).strip("_")
		archive_path = archive_dir / f"{term_slug}_SYLLABI.zip"
		with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
			for output_path in sorted(output_paths):
				archive.write(output_path, arcname=output_path.name)
		print(f"Archived {archive_path}")
	return None


#============================================
def parse_args() -> argparse.Namespace:
	"""Parse archive and deployment-readiness switches."""
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument(
		"--archive",
		action="store_true",
		help="also create one ZIP archive per term under output/archive",
	)
	parser.add_argument(
		"--require-approved",
		action="store_true",
		help="fail unless every manifest is approved for public deployment",
	)
	args = parser.parse_args()
	return args


#============================================
def main() -> None:
	"""Build all course manifests into complete downloadable files."""
	args = parse_args()
	repo_root = get_repo_root()
	docs_root = repo_root / "site_docs"
	downloads_dir = docs_root / "downloads"
	reference_path = repo_root / "templates" / "syllabus_reference.docx"
	pdf_stylesheet_path = docs_root / "assets" / "stylesheets" / "syllabus_pdf.css"
	mkdocs_config_path = repo_root / "mkdocs.yml"
	if not reference_path.is_file():
		raise FileNotFoundError(
			f"Missing {reference_path}. Run pipeline/create_syllabus_reference_docx.py first."
		)
	if not pdf_stylesheet_path.is_file():
		raise FileNotFoundError(f"Missing PDF stylesheet: {pdf_stylesheet_path}")
	if not mkdocs_config_path.is_file():
		raise FileNotFoundError(f"Missing MkDocs configuration: {mkdocs_config_path}")
	check_tools()
	scan_public_sources(docs_root)
	markdown_extensions, markdown_extension_configs = load_markdown_configuration(
		mkdocs_config_path
	)
	manifest_paths = sorted(docs_root.rglob("syllabus.yml"))
	if not manifest_paths:
		raise RuntimeError("No syllabus.yml manifests found under site_docs")
	manifests = [load_manifest(manifest_path, docs_root) for manifest_path in manifest_paths]
	reset_downloads(downloads_dir)
	if args.require_approved:
		draft_paths = [
			manifest.path
			for manifest in manifests
			if manifest.publication_status != "approved"
		]
		if draft_paths:
			draft_list = ", ".join(str(path.relative_to(repo_root)) for path in draft_paths)
			raise RuntimeError(f"Publication blocked by draft manifests: {draft_list}")
	outputs_by_term: dict[str, list[pathlib.Path]] = {}
	with tempfile.TemporaryDirectory(prefix="syllabus_build_") as temporary_name:
		temporary_dir = pathlib.Path(temporary_name)
		for manifest in manifests:
			outputs = build_one_syllabus(
				manifest,
				downloads_dir,
				reference_path,
				pdf_stylesheet_path,
				markdown_extensions,
				markdown_extension_configs,
				temporary_dir,
			)
			if manifest.term not in outputs_by_term:
				outputs_by_term[manifest.term] = []
			outputs_by_term[manifest.term].extend(outputs)
	if args.archive:
		archive_outputs(outputs_by_term, repo_root / "output" / "archive")
	return None


if __name__ == "__main__":
	main()
