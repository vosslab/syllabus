"""Load and validate complete-syllabus manifests."""

# Standard Library
import re
import pathlib
import dataclasses
import urllib.parse

# PIP3 modules
import yaml


ASSESSMENT_FRAGMENT_PATHS = {
	"assignments": pathlib.PurePosixPath("shared/fragments/assessments/ASSIGNMENTS.md"),
	"group_quizzes": pathlib.PurePosixPath("shared/fragments/assessments/GROUP_QUIZZES.md"),
	"f2f_exams": pathlib.PurePosixPath(
		"shared/fragments/assessments/FACE_TO_FACE_EXAMS.md"
	),
	"online_exams": pathlib.PurePosixPath("shared/fragments/assessments/ONLINE_EXAMS.md"),
}

DISCUSSION_FRAGMENT_PATHS = {
	"no_discussion": (pathlib.PurePosixPath("shared/fragments/discussions/NO_DISCUSSION.md"),),
	"f2f_discussion": (
		pathlib.PurePosixPath("shared/fragments/discussions/FACE_TO_FACE.md"),
		pathlib.PurePosixPath("shared/fragments/discussions/COMMON.md"),
	),
	"remote_discussion": (
		pathlib.PurePosixPath("shared/fragments/discussions/REMOTE.md"),
		pathlib.PurePosixPath("shared/fragments/discussions/COMMON.md"),
	),
}


@dataclasses.dataclass(frozen=True)
class SyllabusManifest:
	"""Validated paths and metadata for one complete syllabus."""

	path: pathlib.Path
	docs_root: pathlib.Path
	title: str
	course_code: str
	term: str
	author: str
	language: str
	course_color: str
	download_basename: str
	sections: tuple[pathlib.Path, ...]
	shared_sections: tuple[pathlib.Path, ...]
	assessment_fragments: tuple[pathlib.Path, ...] = ()
	assessment_examples_url: str | None = None
	discussion_fragments: tuple[pathlib.Path, ...] = ()


#============================================
def validate_course_theme(
	loaded: dict[object, object],
	metadata_path: pathlib.Path,
) -> tuple[str, str]:
	"""Return normalized course accents after validating their CSS-safe form."""
	# ASVS 2.2.1: allow only the documented six-digit hex format at the shared boundary.
	colors = []
	for key in ("course_color", "course_color_dark"):
		color = require_text(loaded, key, metadata_path)
		if re.fullmatch(r"#[0-9A-Fa-f]{6}", color) is None:
			raise ValueError(f"{metadata_path}: {key} must be a six-digit hex color")
		colors.append(color.lower())
	return colors[0], colors[1]


#============================================
def load_course_theme(metadata_path: pathlib.Path) -> tuple[str, str]:
	"""Load CSS-safe light and dark course accents from adjacent metadata."""
	# ASVS 1.5.2: deserialize authored YAML without permitting custom object construction.
	loaded = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))
	if not isinstance(loaded, dict):
		raise ValueError(f"{metadata_path}: metadata root must be a mapping")
	return validate_course_theme(loaded, metadata_path)


#============================================
def require_text(data: dict[object, object], key: str, manifest_path: pathlib.Path) -> str:
	"""Return one required, non-empty string field from manifest data."""
	value = data.get(key)
	if not isinstance(value, str) or not value.strip():
		raise ValueError(f"{manifest_path}: {key} must be a non-empty string")
	text_value = value.strip()
	return text_value


#============================================
def validate_assessment_examples_url(value: str, manifest_path: pathlib.Path) -> str:
	"""Return one allowlisted Biology Problems subject URL."""
	# ASVS 1.2.2, 2.2.1: allow only the official HTTPS origin and one safe subject slug.
	parsed = urllib.parse.urlsplit(value)
	is_valid = (
		parsed.scheme == "https"
		and parsed.netloc == "biologyproblems.org"
		and re.fullmatch(r"/[a-z0-9_-]+/", parsed.path) is not None
		and not parsed.query
		and not parsed.fragment
	)
	if not is_valid:
		raise ValueError(
			f"{manifest_path}: assessment_examples_url must be an HTTPS "
			"biologyproblems.org subject URL"
		)
	return value


#============================================
def resolve_source_list(
	value: object,
	field_name: str,
	manifest_path: pathlib.Path,
	docs_root: pathlib.Path,
) -> tuple[pathlib.Path, ...]:
	"""Resolve and validate an ordered manifest source list."""
	if not isinstance(value, list) or not value:
		raise ValueError(f"{manifest_path}: {field_name} must be a non-empty list")
	resolved_paths = []
	for item in value:
		if not isinstance(item, str) or not item.strip():
			raise ValueError(
				f"{manifest_path}: {field_name} entries must be non-empty strings"
			)
		candidate = (manifest_path.parent / item).resolve()
		# ASVS 5.3.2: accept manifest source paths only after containment validation.
		if not candidate.is_relative_to(docs_root.resolve()):
			raise ValueError(f"{manifest_path}: source escapes site_docs: {item}")
		if not candidate.is_file():
			raise FileNotFoundError(f"{manifest_path}: missing source: {item}")
		resolved_paths.append(candidate)
	sources = tuple(resolved_paths)
	return sources


#============================================
def resolve_sources(
	data: dict[object, object],
	key: str,
	manifest_path: pathlib.Path,
	docs_root: pathlib.Path,
) -> tuple[pathlib.Path, ...]:
	"""Resolve one required top-level manifest source list."""
	sources = resolve_source_list(
		data[key],
		key,
		manifest_path,
		docs_root,
	)
	return sources


#============================================
def resolve_assessment_fragments(
	data: dict[object, object],
	manifest_path: pathlib.Path,
	docs_root: pathlib.Path,
) -> tuple[pathlib.Path, ...]:
	"""Resolve the ordered closed vocabulary of course assessment categories."""
	categories = data["assessments"]
	if not isinstance(categories, list) or not categories:
		raise ValueError(f"{manifest_path}: assessments must be a non-empty list")
	if any(not isinstance(category, str) for category in categories):
		raise ValueError(f"{manifest_path}: assessments entries must be strings")
	if len(set(categories)) != len(categories):
		raise ValueError(f"{manifest_path}: assessments must not contain duplicates")
	unsupported = sorted(set(categories) - set(ASSESSMENT_FRAGMENT_PATHS))
	if unsupported:
		unsupported_text = ", ".join(unsupported)
		raise ValueError(f"{manifest_path}: unsupported assessments: {unsupported_text}")
	term_root = manifest_path.parent.parent
	fragments = tuple(
		(term_root / ASSESSMENT_FRAGMENT_PATHS[category]).resolve()
		for category in categories
	)
	for fragment_path in fragments:
		if not fragment_path.is_relative_to(docs_root.resolve()):
			raise ValueError(f"{manifest_path}: assessment fragment escapes site_docs")
		if not fragment_path.is_file():
			raise FileNotFoundError(f"{manifest_path}: missing assessment fragment: {fragment_path}")
	return fragments


#============================================
def resolve_discussion_fragments(
	data: dict[object, object],
	manifest_path: pathlib.Path,
	docs_root: pathlib.Path,
) -> tuple[pathlib.Path, ...]:
	"""Resolve one course discussion mode to its canonical fragments."""
	discussion = data.get("discussion")
	if not isinstance(discussion, str) or discussion not in DISCUSSION_FRAGMENT_PATHS:
		raise ValueError(f"{manifest_path}: unsupported discussion mode: {discussion}")
	term_root = manifest_path.parent.parent
	fragments = tuple(
		(term_root / relative_path).resolve()
		for relative_path in DISCUSSION_FRAGMENT_PATHS[discussion]
	)
	for fragment_path in fragments:
		if not fragment_path.is_relative_to(docs_root.resolve()):
			raise ValueError(f"{manifest_path}: discussion fragment escapes site_docs")
		if not fragment_path.is_file():
			raise FileNotFoundError(
				f"{manifest_path}: missing discussion fragment: {fragment_path}"
			)
	return fragments


#============================================
def load_manifest(
	manifest_path: pathlib.Path,
	docs_root: pathlib.Path,
) -> SyllabusManifest:
	"""Load one YAML manifest and reject incomplete or unsafe values."""
	loaded = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
	if not isinstance(loaded, dict):
		raise ValueError(f"{manifest_path}: manifest root must be a mapping")
	title = require_text(loaded, "title", manifest_path)
	course_code = require_text(loaded, "course_code", manifest_path)
	term = require_text(loaded, "term", manifest_path)
	author = require_text(loaded, "author", manifest_path)
	language = require_text(loaded, "language", manifest_path)
	course_color = load_course_theme(manifest_path.parent / ".meta.yml")[0]
	download_basename = require_text(loaded, "download_basename", manifest_path)
	if re.fullmatch(r"[A-Z0-9_]+", download_basename) is None:
		raise ValueError(f"{manifest_path}: download_basename must use A-Z, 0-9, and underscores")
	sections = resolve_sources(loaded, "sections", manifest_path, docs_root)
	shared_sections = resolve_sources(loaded, "shared_sections", manifest_path, docs_root)
	assessment_fragments = resolve_assessment_fragments(loaded, manifest_path, docs_root)
	discussion_fragments = resolve_discussion_fragments(loaded, manifest_path, docs_root)
	assessment_examples_url = validate_assessment_examples_url(
		require_text(loaded, "assessment_examples_url", manifest_path),
		manifest_path,
	)
	manifest = SyllabusManifest(
		path=manifest_path,
		docs_root=docs_root.resolve(),
		title=title,
		course_code=course_code,
		term=term,
		author=author,
		language=language,
		course_color=course_color,
		download_basename=download_basename,
		sections=sections,
		shared_sections=shared_sections,
		assessment_fragments=assessment_fragments,
		assessment_examples_url=assessment_examples_url,
		discussion_fragments=discussion_fragments,
	)
	return manifest
