"""Validate website metadata and expand includes through shared build libraries."""

# Standard Library
import pathlib
import collections.abc

# local repo modules
import build_lib.markdown_includes
import build_lib.syllabus_model


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
	expanded = build_lib.markdown_includes.expand_includes(
		markdown,
		source_path,
		docs_root,
	)
	return expanded
