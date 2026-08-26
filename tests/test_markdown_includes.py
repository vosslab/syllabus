"""Behavior tests for the shared Markdown include engine and its MkDocs hook."""

# Standard Library
import sys
import types
import pathlib

# PIP3 modules
import yaml
import pytest
import mkdocs.config
import pathspec.gitignore
import mkdocs.config.config_options

# local repo modules
import file_utils
import build_lib.markdown_includes


REPO_ROOT = pathlib.Path(file_utils.get_repo_root())


#============================================
def write_source(docs_root: pathlib.Path, name: str = "SOURCE.md") -> pathlib.Path:
	"""Write one source page below a nested course directory."""
	source_path = docs_root / "fall_20xx" / "course" / name
	source_path.parent.mkdir(parents=True, exist_ok=True)
	source_path.write_text("# Source\n", encoding="utf-8")
	return source_path


#============================================
def write_include(docs_root: pathlib.Path, relative_name: str, content: str) -> pathlib.Path:
	"""Write one inline include file under the requested authorized role."""
	include_path = docs_root / relative_name
	include_path.parent.mkdir(parents=True, exist_ok=True)
	include_path.write_text(content, encoding="utf-8")
	return include_path


#============================================
def test_expand_includes_uses_docs_root_and_both_authorized_roles(
	tmp_path: pathlib.Path,
) -> None:
	"""Fragments and generated Markdown resolve from docs_root, not the source folder."""
	docs_root = tmp_path / "site_docs"
	source_path = write_source(docs_root)
	write_include(
		docs_root,
		"fall_20xx/shared/fragments/CONTACT.md",
		"\nCanonical contact.\n",
	)
	write_include(docs_root, "generated/DATES.md", "Generated dates.\n\n")
	markdown = (
		"Before.\n\n"
		'--8<-- "fall_20xx/shared/fragments/CONTACT.md"\n\n'
		'--8<-- "generated/DATES.md"\n\n'
		"After.\n"
	)
	expanded = build_lib.markdown_includes.expand_includes(
		markdown,
		source_path,
		docs_root,
	)
	assert expanded == "Before.\n\nCanonical contact.\n\nGenerated dates.\n\nAfter.\n"


#============================================
def test_expand_includes_rejects_a_missing_file(tmp_path: pathlib.Path) -> None:
	"""A valid authorized path still fails when its target is absent."""
	docs_root = tmp_path / "site_docs"
	source_path = write_source(docs_root, "COURSE_DETAILS.md")
	markdown = '--8<-- "generated/MISSING.md"\n'
	with pytest.raises(FileNotFoundError, match=r"COURSE_DETAILS\.md: missing Markdown include"):
		build_lib.markdown_includes.expand_includes(markdown, source_path, docs_root)


#============================================
def test_expand_includes_rejects_an_empty_fragment(tmp_path: pathlib.Path) -> None:
	"""An authorized fragment must contain visible Markdown."""
	docs_root = tmp_path / "site_docs"
	source_path = write_source(docs_root)
	write_include(docs_root, "generated/EMPTY.md", " \n\t\n")
	markdown = '--8<-- "generated/EMPTY.md"\n'
	with pytest.raises(ValueError, match=r"EMPTY\.md: Markdown include must not be empty"):
		build_lib.markdown_includes.expand_includes(markdown, source_path, docs_root)


#============================================
@pytest.mark.parametrize(
	"include_name",
	(
		"/outside/PRIVATE.md",
		"../PRIVATE.md",
		"https://example.com/PRIVATE.md",
	),
	ids=("absolute", "parent-traversal", "remote-url"),
)
def test_expand_includes_rejects_unsafe_paths(
	tmp_path: pathlib.Path,
	include_name: str,
) -> None:
	"""Absolute, parent-relative, and remote include names fail before file access."""
	docs_root = tmp_path / "site_docs"
	source_path = write_source(docs_root, "COURSE_DETAILS.md")
	markdown = f'--8<-- "{include_name}"\n'
	with pytest.raises(ValueError, match=r"COURSE_DETAILS\.md: unsafe Markdown include"):
		build_lib.markdown_includes.expand_includes(markdown, source_path, docs_root)


#============================================
def test_expand_includes_rejects_nested_markers(tmp_path: pathlib.Path) -> None:
	"""Included Markdown cannot open a second expansion pass."""
	docs_root = tmp_path / "site_docs"
	source_path = write_source(docs_root)
	write_include(
		docs_root,
		"generated/NESTED.md",
		'--8<-- "generated/SECOND.md"\n',
	)
	markdown = '--8<-- "generated/NESTED.md"\n'
	with pytest.raises(ValueError, match=r"NESTED\.md: nested Markdown includes"):
		build_lib.markdown_includes.expand_includes(markdown, source_path, docs_root)


#============================================
def test_expand_includes_rejects_a_normal_page(tmp_path: pathlib.Path) -> None:
	"""A directly navigable Markdown page is not an authorized fragment."""
	docs_root = tmp_path / "site_docs"
	source_path = write_source(docs_root)
	write_include(docs_root, "fall_20xx/course/COURSE_DETAILS.md", "# Details\n")
	markdown = '--8<-- "fall_20xx/course/COURSE_DETAILS.md"\n'
	with pytest.raises(ValueError, match=r"unauthorized Markdown include:.*COURSE_DETAILS\.md"):
		build_lib.markdown_includes.expand_includes(markdown, source_path, docs_root)


#============================================
def test_expand_includes_rejects_a_symlink_escape(tmp_path: pathlib.Path) -> None:
	"""An authorized-looking symlink cannot read outside the documentation root."""
	docs_root = tmp_path / "site_docs"
	source_path = write_source(docs_root, "COURSE_DETAILS.md")
	private_path = tmp_path / "PRIVATE.md"
	private_path.write_text("Private text.\n", encoding="utf-8")
	include_path = docs_root / "generated" / "PRIVATE.md"
	include_path.parent.mkdir()
	include_path.symlink_to(private_path)
	markdown = '--8<-- "generated/PRIVATE.md"\n'
	with pytest.raises(ValueError, match=r"COURSE_DETAILS\.md: include escapes site_docs"):
		build_lib.markdown_includes.expand_includes(markdown, source_path, docs_root)


#============================================
@pytest.mark.parametrize(
	"markdown",
	(
		'--8<--\n"generated/FRAGMENT.md"\n',
		'--8<-- "generated/FRAGMENT.md:1:2"\n',
		'---8<--- "generated/FRAGMENT.md"\n',
		"--8<-- 'generated/FRAGMENT.md'\n",
		"--8<-- generated/FRAGMENT.md\n",
	),
	ids=("block", "section", "alternate-marker", "single-quoted", "unquoted"),
)
def test_expand_includes_rejects_unsupported_syntax(
	tmp_path: pathlib.Path,
	markdown: str,
) -> None:
	"""Former PyMdown-only forms cannot pass through to one output branch."""
	docs_root = tmp_path / "site_docs"
	source_path = write_source(docs_root, "COURSE_DETAILS.md")
	with pytest.raises(ValueError, match=r"COURSE_DETAILS\.md"):
		build_lib.markdown_includes.expand_includes(markdown, source_path, docs_root)


#============================================
def test_mkdocs_loader_keeps_shared_libraries_available_after_restoring_sys_path(
	tmp_path: pathlib.Path,
	monkeypatch: pytest.MonkeyPatch,
) -> None:
	"""MkDocs loads both shared hook libraries before its temporary import path disappears."""
	docs_root = tmp_path / "site_docs"
	source_path = write_source(docs_root)
	write_include(docs_root, "generated/HOOK.md", "Loaded through MkDocs.\n")
	pipeline_root = (REPO_ROOT / "pipeline").resolve()
	isolated_sys_path = [
		entry
		for entry in sys.path
		if pathlib.Path(entry).resolve() != pipeline_root
	]
	monkeypatch.setattr(sys, "path", isolated_sys_path)
	monkeypatch.delitem(sys.modules, "build_lib.markdown_includes", raising=False)
	monkeypatch.delitem(sys.modules, "build_lib.syllabus_model", raising=False)
	monkeypatch.delitem(sys.modules, "build_lib", raising=False)
	mkdocs.config.config_options.Hooks._load_hook.cache_clear()
	config = mkdocs.config.load_config(
		str(REPO_ROOT / "mkdocs.yml"),
		docs_dir=str(docs_root),
	)
	loaded_hook = next(iter(config["hooks"].values()))
	page = types.SimpleNamespace(
		file=types.SimpleNamespace(abs_src_path=str(source_path)),
		meta={"course_color": "#1565C0", "course_color_dark": "#8AB4F8"},
	)
	expanded = loaded_hook.on_page_markdown(
		'--8<-- "generated/HOOK.md"\n',
		page,
		config,
		object(),
	)
	assert expanded == "Loaded through MkDocs.\n"
	page.meta["course_color"] = "red; display: none"
	with pytest.raises(ValueError, match="course_color must be a six-digit hex color"):
		loaded_hook.on_page_markdown("No includes.\n", page, config, object())


#============================================
def test_authorized_markdown_is_excluded_from_direct_site_routes() -> None:
	"""Every includable Markdown role remains a subset of MkDocs exclusions."""
	config_data = yaml.safe_load((REPO_ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
	exclude_spec = pathspec.gitignore.GitIgnoreSpec.from_lines(
		config_data["exclude_docs"].splitlines()
	)
	docs_root = REPO_ROOT / "site_docs"
	unmatched_paths = []
	for markdown_path in sorted(docs_root.rglob("*.md")):
		relative_path = markdown_path.relative_to(docs_root)
		if not any(
			part in build_lib.markdown_includes.FRAGMENT_DIRECTORY_NAMES
			for part in relative_path.parts
		):
			continue
		if not exclude_spec.match_file(relative_path.as_posix()):
			unmatched_paths.append(relative_path.as_posix())
	assert not unmatched_paths, f"Authorized fragments missing from exclude_docs: {unmatched_paths}"


#============================================
def test_mkdocs_configuration_has_no_second_include_engine() -> None:
	"""The Markdown extension stack cannot run PyMdown snippets after the hook."""
	config_data = yaml.safe_load((REPO_ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
	extension_names = []
	for entry in config_data["markdown_extensions"]:
		if isinstance(entry, str):
			extension_names.append(entry)
		else:
			extension_names.extend(entry)
	assert "pymdownx.snippets" not in extension_names
