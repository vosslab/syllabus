"""Load and validate complete-syllabus manifests."""

# Standard Library
import re
import pathlib
import dataclasses

# PIP3 modules
import yaml


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
	download_basename: str
	sections: tuple[pathlib.Path, ...]
	shared_sections: tuple[pathlib.Path, ...]


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
		# ASVS 5.3.2: accept manifest source paths only after containment validation.
		if not candidate.is_relative_to(docs_root.resolve()):
			raise ValueError(f"{manifest_path}: source escapes site_docs: {item}")
		if not candidate.is_file():
			raise FileNotFoundError(f"{manifest_path}: missing source: {item}")
		resolved_paths.append(candidate)
	sources = tuple(resolved_paths)
	return sources


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
	download_basename = require_text(loaded, "download_basename", manifest_path)
	if re.fullmatch(r"[A-Z0-9_]+", download_basename) is None:
		raise ValueError(f"{manifest_path}: download_basename must use A-Z, 0-9, and underscores")
	sections = resolve_sources(loaded, "sections", manifest_path, docs_root)
	shared_sections = resolve_sources(loaded, "shared_sections", manifest_path, docs_root)
	manifest = SyllabusManifest(
		path=manifest_path,
		docs_root=docs_root.resolve(),
		title=title,
		course_code=course_code,
		term=term,
		author=author,
		language=language,
		download_basename=download_basename,
		sections=sections,
		shared_sections=shared_sections,
	)
	return manifest
