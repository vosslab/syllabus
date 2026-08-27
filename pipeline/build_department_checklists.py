#!/usr/bin/env python3
"""Generate one evidence-linked department checklist per live syllabus."""

# Standard Library
import copy
import pathlib
import argparse
import subprocess
import urllib.parse

# PIP3 modules
import yaml

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
	"""Validate evidence link labels and site-relative paths."""
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
def evidence_url(site_base: str, course_route: str, evidence_path: str) -> str:
	"""Resolve one evidence path and require it to remain within the published site."""
	if evidence_path.startswith("/") or ":" in evidence_path.split("/", 1)[0]:
		raise ValueError(f"Evidence path must be site-relative: {evidence_path}")
	course_url = urllib.parse.urljoin(site_base, f"fall_2026/{course_route}/")
	url = urllib.parse.urljoin(course_url, evidence_path)
	# ASVS 2.2.1: evidence links are allowlisted to the configured public syllabus site.
	if not url.startswith(site_base):
		raise ValueError(f"Evidence link escapes the configured site: {evidence_path}")
	return url


#============================================
def render_checklist(
	manifest: build_lib.syllabus_model.SyllabusManifest,
	course_route: str,
	site_base: str,
	items: list[dict[str, object]],
) -> str:
	"""Render one complete department checklist as portable Markdown."""
	lines = [
		f"# {manifest.course_code} {manifest.title} syllabus checklist",
		"",
		f"**Term:** {manifest.term}",
		"",
		f"**Instructor:** {manifest.author}",
		"",
		"**Status key:** `[x]` covered or justified as not applicable; "
		"`[ ]` needs department or instructor review.",
		"",
		"This checklist links to the published student-facing syllabus. Notes labeled **Doubt** identify",
		"items that should not be treated as satisfied until their applicability or wording is confirmed.",
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
		links = []
		for link in item["evidence"]:
			url = evidence_url(site_base, course_route, link["path"])
			links.append(f"[{link['label']}]({url})")
		evidence_text = "; ".join(links)
		note_prefix = "**Doubt:** " if status == "needs_review" else ""
		status_label = "Not applicable" if status == "not_applicable" else "Evidence"
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
def load_configuration(config_path: pathlib.Path) -> dict[object, object]:
	"""Safely deserialize and validate the top-level checklist configuration."""
	# ASVS 1.5.2: safe_load prevents authored YAML from constructing arbitrary Python objects.
	loaded = yaml.safe_load(config_path.read_text(encoding="utf-8"))
	configuration = require_mapping(loaded, str(config_path))
	if set(configuration) != {"site_base", "items", "courses"}:
		raise ValueError(f"{config_path}: expected site_base, items, and courses")
	return configuration


#============================================
def build_checklists(repo_root: pathlib.Path, output_dir: pathlib.Path) -> tuple[pathlib.Path, ...]:
	"""Generate Markdown and DOCX checklists for every configured live course."""
	config_path = repo_root / "pipeline" / "department_checklists.yml"
	configuration = load_configuration(config_path)
	site_base = require_text(configuration, "site_base", str(config_path))
	if not site_base.startswith("https://") or not site_base.endswith("/"):
		raise ValueError(f"{config_path}: site_base must be an HTTPS directory URL")
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
	output_root = (repo_root / "output" / "department_checklists").resolve()
	resolved_output = output_dir.resolve()
	# ASVS 2.2.1: generated writes stay within the documented output boundary.
	if not resolved_output.is_relative_to(output_root):
		raise ValueError(f"Output directory must stay within {output_root}")
	resolved_output.mkdir(parents=True, exist_ok=True)
	generated_paths = []
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
		markdown = render_checklist(manifest, course_route, site_base, course_items)
		basename = f"{manifest.download_basename}_DEPARTMENT_CHECKLIST"
		markdown_path = resolved_output / f"{basename}.md"
		docx_path = resolved_output / f"{basename}.docx"
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
		generated_paths.extend((markdown_path, docx_path))
		print(f"Built {markdown_path.name} and {docx_path.name}")
	return tuple(generated_paths)


#============================================
def parse_args(repo_root: pathlib.Path) -> argparse.Namespace:
	"""Parse the contained output-directory option."""
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument(
		"--output-dir",
		type=pathlib.Path,
		default=repo_root / "output" / "department_checklists",
		help="directory below output/department_checklists",
	)
	return parser.parse_args()


#============================================
def main() -> None:
	"""Build all configured department checklists."""
	repo_root = get_repo_root()
	args = parse_args(repo_root)
	build_checklists(repo_root, args.output_dir)


if __name__ == "__main__":
	main()
