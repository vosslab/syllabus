"""Validate website metadata and expand includes through shared build libraries."""

# Standard Library
import pathlib
import collections.abc

# local repo modules
import build_lib.syllabus_model
import build_lib.syllabus_content
import build_lib.markdown_includes


#============================================
def on_page_markdown(
	markdown: str,
	page: object,
	config: collections.abc.Mapping[str, str],
	files: object,
) -> str:
	"""Validate course colors and expand authorized fragments before page rendering."""
	docs_root = pathlib.Path(config["docs_dir"])
	source_path = pathlib.Path(page.file.abs_src_path)
	page_metadata = getattr(page, "meta", {})
	if any(key in page_metadata for key in ("course_color", "course_color_dark")):
		course_color, course_color_dark = build_lib.syllabus_model.validate_course_theme(
			page_metadata,
			source_path.parent / ".meta.yml",
		)
		# ASVS 1.1.2 and 1.2.1: templates receive only normalized, allowlisted CSS tokens.
		page_metadata["course_color"] = course_color
		page_metadata["course_color_dark"] = course_color_dark
	if build_lib.syllabus_content.ASSESSMENT_FRAGMENT_MARKER in markdown:
		manifest = build_lib.syllabus_model.load_manifest(
			source_path.parent / "syllabus.yml",
			docs_root,
		)
		markdown = build_lib.syllabus_content.apply_assessment_fragments(
			markdown,
			source_path,
			manifest,
		)
	if build_lib.syllabus_content.DISCUSSION_FRAGMENT_MARKER in markdown:
		manifest = build_lib.syllabus_model.load_manifest(
			source_path.parent / "syllabus.yml",
			docs_root,
		)
		markdown = build_lib.syllabus_content.apply_discussion_fragments(
			markdown,
			source_path,
			manifest,
		)
	expanded = build_lib.markdown_includes.expand_includes(
		markdown,
		source_path,
		docs_root,
	)
	if build_lib.syllabus_content.ASSESSMENT_EXAMPLES_MARKER in expanded:
		manifest = build_lib.syllabus_model.load_manifest(
			source_path.parent / "syllabus.yml",
			docs_root,
		)
		expanded = build_lib.syllabus_content.apply_assessment_examples_link(expanded, manifest)
	return expanded
