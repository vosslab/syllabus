"""Validate and compose Markdown for complete syllabi."""

# Standard Library
import os
import re
import pathlib
import subprocess

# PIP3 modules
import yaml

# local repo modules
import build_lib.syllabus_model
import build_lib.markdown_includes


SECRET_PATTERNS = (
	re.compile(r"zoom\.us/j/", re.IGNORECASE),
	re.compile(r"\bpwd=", re.IGNORECASE),
	re.compile(r"\b(?:passcode|password)\s*[:=]", re.IGNORECASE),
	re.compile(r"discord(?:\.gg|\.com/invite)/", re.IGNORECASE),
)
PROHIBITED_CONTROL_PATTERN = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
MARKDOWN_TABLE_SEPARATOR_PATTERN = re.compile(r":?-{3,}:?")
REQUIRED_LEARNING_TITLE = "# Learning Objectives, Outcomes, and Goals"
REQUIRED_LEARNING_MARKERS = (
	"## Roosevelt learning goals",
	"## Learning Objectives",
	"Students completing this course will have achieved:",
	"## Course Learning Outcomes",
	"Students completing this course will be able to:",
	"## Learning Goals",
	"Overall, this course aims to accomplish:",
)


#============================================
def scan_text_for_secrets(text_value: str, source_label: str) -> None:
	"""Reject public content that resembles meeting credentials or invite links."""
	for pattern in SECRET_PATTERNS:
		match = pattern.search(text_value)
		if match is not None:
			raise ValueError(f"{source_label}: prohibited public credential pattern: {match.group(0)}")
	return None


#============================================
def scan_text_for_prohibited_controls(text_value: str, source_label: str) -> None:
	"""Reject control characters that can change Markdown line structure."""
	match = PROHIBITED_CONTROL_PATTERN.search(text_value)
	if match is not None:
		codepoint = ord(match.group(0))
		raise ValueError(f"{source_label}: prohibited control character: U+{codepoint:04X}")
	return None


#============================================
def split_markdown_table_row(line: str) -> tuple[str, ...]:
	"""Return cells from one leading-and-trailing-pipe Markdown row."""
	stripped = line.strip()
	if not stripped.startswith("|") or not stripped.endswith("|"):
		raise ValueError("Markdown table rows must start and end with a pipe")
	cell_text = stripped[1:-1]
	cells = tuple(cell.strip() for cell in re.split(r"(?<!\\)\|", cell_text))
	return cells


#============================================
def count_markdown_tables(markdown_text: str) -> int:
	"""Count pipe tables by their header separator rows."""
	lines = markdown_text.split("\n")
	table_count = 0
	for line_index in range(1, len(lines)):
		current = lines[line_index].strip()
		previous = lines[line_index - 1].strip()
		if not current.startswith("|") or not current.endswith("|"):
			continue
		if not previous.startswith("|") or not previous.endswith("|"):
			continue
		separator_cells = split_markdown_table_row(current)
		if separator_cells and all(
			MARKDOWN_TABLE_SEPARATOR_PATTERN.fullmatch(cell) is not None
			for cell in separator_cells
		):
			table_count += 1
	return table_count


#============================================
def validate_markdown_tables(markdown_text: str, source_label: str) -> None:
	"""Require simple, rectangular Markdown tables with named header cells."""
	lines = markdown_text.split("\n")
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
			block_lines.append(lines[line_index])
			line_index += 1
		if len(block_lines) < 2:
			raise ValueError(f"{source_label}:{block_start + 1}: incomplete Markdown table")
		header_cells = split_markdown_table_row(block_lines[0])
		separator_cells = split_markdown_table_row(block_lines[1])
		if len(header_cells) < 2 or any(not cell for cell in header_cells):
			raise ValueError(f"{source_label}:{block_start + 1}: table headers must be named")
		if len(separator_cells) != len(header_cells) or any(
			MARKDOWN_TABLE_SEPARATOR_PATTERN.fullmatch(cell) is None
			for cell in separator_cells
		):
			raise ValueError(f"{source_label}:{block_start + 2}: invalid table separator row")
		for row_offset, row_line in enumerate(block_lines[2:], start=3):
			row_cells = split_markdown_table_row(row_line)
			if len(row_cells) != len(header_cells):
				raise ValueError(
					f"{source_label}:{block_start + row_offset}: inconsistent table columns"
				)
	return None


#============================================
def scan_public_sources(docs_root: pathlib.Path) -> None:
	"""Scan public text sources before generating downloads."""
	for suffix in ("*.md", "*.yml", "*.yaml"):
		for source_path in sorted(docs_root.rglob(suffix)):
			if "downloads" in source_path.parts:
				continue
			content = source_path.read_text(encoding="utf-8")
			scan_text_for_prohibited_controls(content, str(source_path))
			scan_text_for_secrets(content, str(source_path))
			if source_path.suffix == ".md":
				validate_markdown_tables(content, str(source_path))
	return None


#============================================
def require_public_only_repository(repo_root: pathlib.Path) -> None:
	"""Reject tracked raw content while allowing ignored local public references."""
	# ASVS 1.2.5: pass the fixed Git command and pathspec as separate arguments.
	completed = subprocess.run(
		["git", "ls-files", "-z", "--", "raw"],
		cwd=repo_root,
		check=True,
		capture_output=True,
	)
	tracked_raw_paths = tuple(
		path.decode("utf-8") for path in completed.stdout.split(b"\0") if path
	)
	if tracked_raw_paths:
		path_list = ", ".join(tracked_raw_paths)
		raise RuntimeError(
			"only public-safe canonical content belongs in this repository; "
			f"remove tracked raw content: {path_list}"
		)
	return None


#============================================
def require_single_content_authority(repo_root: pathlib.Path) -> None:
	"""Reject a parallel Markdown or manifest tree below templates."""
	templates_root = repo_root / "templates"
	for suffix in ("*.md", "*.yml", "*.yaml"):
		for source_path in sorted(templates_root.rglob(suffix)):
			# ASVS 2.1.1: enforce the documented site_docs-only source boundary.
			raise RuntimeError(
				f"{source_path}: live syllabus content belongs only under site_docs"
			)
	return None


#============================================
def validate_course_learning_framework(
	sections: tuple[pathlib.Path, ...],
	docs_root: pathlib.Path,
) -> None:
	"""Require the four ordered learning sections and Roosevelt goal bullets."""
	framework_paths = tuple(
		path for path in sections if path.name == "COURSE_LEARNING_FRAMEWORK.md"
	)
	if len(framework_paths) != 1:
		raise ValueError("sections must contain exactly one COURSE_LEARNING_FRAMEWORK.md")
	framework_path = framework_paths[0]
	markdown = framework_path.read_text(encoding="utf-8")
	markdown = build_lib.markdown_includes.expand_includes(markdown, framework_path, docs_root)
	if not markdown.startswith(REQUIRED_LEARNING_TITLE + "\n"):
		raise ValueError(
			f"{framework_path}: title must be {REQUIRED_LEARNING_TITLE.removeprefix('# ')}"
		)
	marker_positions = []
	for marker in REQUIRED_LEARNING_MARKERS:
		position = markdown.find(marker)
		if position < 0:
			raise ValueError(f"{framework_path}: missing required learning marker: {marker}")
		marker_positions.append(position)
	if marker_positions != sorted(marker_positions):
		raise ValueError(f"{framework_path}: required learning sections are out of order")
	roosevelt_start = marker_positions[0] + len(REQUIRED_LEARNING_MARKERS[0])
	roosevelt_end = marker_positions[1]
	roosevelt_markdown = markdown[roosevelt_start:roosevelt_end]
	if re.search(r"^[-*+]\s+\S", roosevelt_markdown, re.MULTILINE) is None:
		raise ValueError(f"{framework_path}: Roosevelt learning goals must be bullet points")
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
def remove_heading_sections(markdown_text: str, heading_names: tuple[str, ...]) -> str:
	"""Remove level-two web-navigation sections from composed documents."""
	heading_options = "|".join(re.escape(name) for name in heading_names)
	pattern = rf"^## (?:{heading_options})\s*$.*?(?=^## |\Z)"
	without_sections = re.sub(pattern, "", markdown_text, flags=re.MULTILINE | re.DOTALL)
	return without_sections


#============================================
def rewrite_document_links(
	markdown_text: str,
	source_path: pathlib.Path,
	document_anchors: dict[pathlib.Path, str],
) -> str:
	"""Point links between included Markdown files at complete-document sections."""
	def replace_link(match: re.Match[str]) -> str:
		"""Rewrite one link whose target is represented in the document."""
		relative_target = match.group(1)
		fragment = match.group(2)
		resolved_target = (source_path.parent / relative_target).resolve()
		# ASVS 5.3.2: rewrite only paths already validated into this manifest.
		if resolved_target not in document_anchors:
			return match.group(0)
		if fragment:
			document_target = fragment
		else:
			document_target = f"#{document_anchors[resolved_target]}"
		replacement = f"({document_target})"
		return replacement

	pattern = r"\(([^()\s]+\.md)(#[^()\s]+)?\)"
	rewritten = re.sub(pattern, replace_link, markdown_text)
	return rewritten


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
		without_navigation = remove_heading_sections(
			without_downloads,
			("Course pages", "Find what you need"),
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
	manifest: build_lib.syllabus_model.SyllabusManifest,
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
def verify_download_links(
	manifest: build_lib.syllabus_model.SyllabusManifest,
	downloads_dir: pathlib.Path,
) -> None:
	"""Require course and term download targets derived from manifest output names."""
	overview_path = manifest.sections[0]
	term_overview_path = manifest.path.parent.parent / "index.md"
	link_sources = (overview_path, term_overview_path)
	for suffix in (".pdf", ".docx"):
		target_path = downloads_dir / f"{manifest.download_basename}{suffix}"
		for source_path in link_sources:
			source_markdown = source_path.read_text(encoding="utf-8")
			source_markdown = build_lib.markdown_includes.expand_includes(
				source_markdown,
				source_path,
				manifest.docs_root,
			)
			relative_path = pathlib.Path(
				os.path.relpath(target_path, source_path.parent)
			).as_posix()
			if relative_path not in source_markdown:
				raise RuntimeError(
					f"{source_path}: missing complete-download link: {relative_path}"
				)
	return None


#============================================
def compose_markdown(manifest: build_lib.syllabus_model.SyllabusManifest) -> str:
	"""Compose course and shared sources in manifest order."""
	parts = []
	contents = ["# Contents", ""]
	document_anchors = {}
	for index, section_path in enumerate(manifest.sections):
		anchor = "course-overview" if index == 0 else section_path.stem.lower().replace("_", "-")
		document_anchors[section_path.resolve()] = anchor
	for section_path in manifest.shared_sections:
		is_policy_index = section_path.name == "index.md" and section_path.parent.name == "policies"
		anchor = "policies" if is_policy_index else section_path.stem.lower().replace("_", "-")
		document_anchors[section_path.resolve()] = anchor
	# The shared instructor route is embedded under this heading in COURSE_DETAILS.md.
	instructor_route_path = manifest.path.parent.parent / "shared" / "INSTRUCTOR_INFORMATION.md"
	if instructor_route_path.is_file():
		document_anchors[instructor_route_path.resolve()] = "instructor-information"
	for index, section_path in enumerate(manifest.sections):
		markdown = section_path.read_text(encoding="utf-8")
		markdown = build_lib.markdown_includes.expand_includes(
			markdown,
			section_path,
			manifest.docs_root,
		)
		markdown = rewrite_document_links(markdown, section_path, document_anchors)
		anchor = document_anchors[section_path.resolve()]
		title = "Course overview" if index == 0 else get_section_title(markdown, section_path)
		contents.append(f"- [{title}](#{anchor})")
		parts.append(prepare_section(markdown, is_overview=index == 0, anchor=anchor))
	for section_path in manifest.shared_sections:
		markdown = section_path.read_text(encoding="utf-8")
		markdown = build_lib.markdown_includes.expand_includes(
			markdown,
			section_path,
			manifest.docs_root,
		)
		markdown = rewrite_document_links(markdown, section_path, document_anchors)
		is_policy_index = section_path.name == "index.md" and section_path.parent.name == "policies"
		if is_policy_index:
			markdown = remove_heading_sections(markdown, ("Policy topics", "Student support"))
		anchor = document_anchors[section_path.resolve()]
		title = get_section_title(markdown, section_path)
		contents.append(f"- [{title}](#{anchor})")
		parts.append(prepare_section(markdown, is_overview=False, anchor=anchor))
	contents.append("")
	combined = "\n".join(contents) + "\n" + "\n\n".join(parts)
	scan_text_for_secrets(combined, str(manifest.path))
	return combined
