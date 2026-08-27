"""Expand the repository's restricted Markdown include language."""

# Standard Library
import os
import re
import pathlib
import urllib.parse


INCLUDE_MARKER = "--8<--"
INCLUDE_LINE_PATTERN = re.compile(
	r'^--8<--[ \t]+"([^"\r\n]+)"[ \t]*\r?$',
	re.MULTILINE,
)
SAFE_INCLUDE_PATH_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_./-]*\.md")
FRAGMENT_DIRECTORY_NAMES = ("fragments", "generated")
MARKDOWN_LINK_PATTERN = re.compile(
	r'(?P<prefix>!?\[[^\]\r\n]*\]\([ \t]*)(?P<destination><[^>\r\n]+>|[^)\s\r\n]+)'
)
HTML_LINK_PATTERN = re.compile(
	r'(?P<prefix>\b(?:href|src)=["\'])(?P<destination>[^"\']+)(?P<suffix>["\'])',
	re.IGNORECASE,
)


#============================================
def validate_include_name(include_name: str, source_path: pathlib.Path) -> None:
	"""Validate one include path before consulting the filesystem."""
	include_parts = pathlib.PurePosixPath(include_name).parts
	# ASVS 2.1.1 and 2.2.1: FILE_FORMATS.md documents this positive path grammar.
	if SAFE_INCLUDE_PATH_PATTERN.fullmatch(include_name) is None or ".." in include_parts:
		raise ValueError(f"{source_path}: unsafe Markdown include: {include_name}")
	if not any(part in FRAGMENT_DIRECTORY_NAMES for part in include_parts):
		raise ValueError(f"{source_path}: unauthorized Markdown include: {include_name}")
	return None


#============================================
def parse_include_names(markdown_text: str, source_path: pathlib.Path) -> tuple[str, ...]:
	"""Return validated include names and reject every unsupported marker use."""
	include_names = []
	for line_number, line in enumerate(markdown_text.splitlines(), start=1):
		if INCLUDE_MARKER not in line:
			continue
		match = INCLUDE_LINE_PATTERN.fullmatch(line)
		if match is None:
			raise ValueError(
				f"{source_path}:{line_number}: unsupported Markdown include syntax"
			)
		include_name = match.group(1)
		validate_include_name(include_name, source_path)
		include_names.append(include_name)
	names = tuple(include_names)
	return names


#============================================
def rebase_relative_url(
	url: str,
	include_path: pathlib.Path,
	source_path: pathlib.Path,
	resolved_docs_root: pathlib.Path,
) -> str:
	"""Rebase one fragment-relative URL for the page receiving the fragment."""
	parsed_url = urllib.parse.urlsplit(url)
	if parsed_url.scheme or parsed_url.netloc or url.startswith(("/", "#")):
		return url
	if not parsed_url.path:
		return url

	target_path = (include_path.parent / parsed_url.path).resolve()
	if not target_path.is_relative_to(resolved_docs_root):
		raise ValueError(f"{include_path}: relative link escapes site_docs: {url}")

	relative_path = os.path.relpath(target_path, source_path.parent.resolve())
	rebased_path = pathlib.PurePath(relative_path).as_posix()
	if parsed_url.path.endswith("/") and not rebased_path.endswith("/"):
		rebased_path += "/"
	rebased_url = urllib.parse.urlunsplit(
		("", "", rebased_path, parsed_url.query, parsed_url.fragment)
	)
	return rebased_url


#============================================
def rebase_fragment_links(
	markdown_text: str,
	include_path: pathlib.Path,
	source_path: pathlib.Path,
	resolved_docs_root: pathlib.Path,
) -> str:
	"""Rebase relative Markdown and HTML links from a fragment into its destination page."""
	def replace_markdown_link(match: re.Match[str]) -> str:
		"""Rewrite one Markdown link destination while preserving its delimiters."""
		destination = match.group("destination")
		uses_angle_brackets = destination.startswith("<") and destination.endswith(">")
		url = destination[1:-1] if uses_angle_brackets else destination
		rebased_url = rebase_relative_url(
			url,
			include_path,
			source_path,
			resolved_docs_root,
		)
		if uses_angle_brackets:
			rebased_url = f"<{rebased_url}>"
		result = match.group("prefix") + rebased_url
		return result

	def replace_html_link(match: re.Match[str]) -> str:
		"""Rewrite one HTML href or src attribute."""
		rebased_url = rebase_relative_url(
			match.group("destination"),
			include_path,
			source_path,
			resolved_docs_root,
		)
		result = match.group("prefix") + rebased_url + match.group("suffix")
		return result

	rebased_markdown = MARKDOWN_LINK_PATTERN.sub(replace_markdown_link, markdown_text)
	rebased_content = HTML_LINK_PATTERN.sub(replace_html_link, rebased_markdown)
	return rebased_content


#============================================
def read_include(
	include_name: str,
	source_path: pathlib.Path,
	resolved_docs_root: pathlib.Path,
) -> str:
	"""Read one authorized include while containing symlink resolution."""
	include_path = (resolved_docs_root / include_name).resolve()
	if not include_path.is_relative_to(resolved_docs_root):
		raise ValueError(f"{source_path}: include escapes site_docs: {include_name}")
	if not include_path.is_file():
		raise FileNotFoundError(f"{source_path}: missing Markdown include: {include_name}")
	include_markdown = include_path.read_text(encoding="utf-8")
	if not include_markdown.strip():
		raise ValueError(f"{include_path}: Markdown include must not be empty")
	if INCLUDE_MARKER in include_markdown:
		raise ValueError(f"{include_path}: nested Markdown includes are not supported")
	content = rebase_fragment_links(
		include_markdown.strip(),
		include_path,
		source_path,
		resolved_docs_root,
	)
	return content


#============================================
def expand_includes(
	markdown_text: str,
	source_path: pathlib.Path,
	docs_root: pathlib.Path,
) -> str:
	"""Expand one level of authorized Markdown includes below ``docs_root``."""
	resolved_docs_root = docs_root.resolve()
	resolved_source_path = source_path.resolve()
	if not resolved_source_path.is_relative_to(resolved_docs_root):
		raise ValueError(f"{source_path}: include source escapes site_docs")

	# ASVS 2.2.2: the shared engine validates every name and role before file access.
	include_names = parse_include_names(markdown_text, source_path)
	include_content = {}
	for include_name in include_names:
		include_content[include_name] = read_include(
			include_name,
			source_path,
			resolved_docs_root,
		)

	def replace_include(match: re.Match[str]) -> str:
		"""Replace one already validated directive with its fragment content."""
		include_name = match.group(1)
		content = include_content[include_name]
		return content

	expanded = INCLUDE_LINE_PATTERN.sub(replace_include, markdown_text)
	return expanded
