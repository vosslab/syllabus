"""Expand website includes through the engine shared with complete syllabi."""

# Standard Library
import pathlib
import collections.abc

# local repo modules
import build_lib.markdown_includes


#============================================
def on_page_markdown(
	markdown: str,
	page: object,
	config: collections.abc.Mapping[str, str],
	files: object,
) -> str:
	"""Expand authorized Markdown fragments before MkDocs renders a page."""
	docs_root = pathlib.Path(config["docs_dir"])
	source_path = pathlib.Path(page.file.abs_src_path)
	expanded = build_lib.markdown_includes.expand_includes(
		markdown,
		source_path,
		docs_root,
	)
	return expanded
