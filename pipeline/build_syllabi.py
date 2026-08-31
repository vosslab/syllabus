"""Build complete DOCX and PDF syllabi from course manifests."""

# Standard Library
import re
import sys
import pathlib
import zipfile
import argparse
import tempfile
import subprocess

# local repo modules
import build_lib.syllabus_model
import build_lib.syllabus_content
import build_lib.syllabus_rendering


ACTIVE_TERM_DIRECTORY = "fall_2026"


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
	"""Parse the optional archive switch."""
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument(
		"--archive",
		action="store_true",
		help="also create one ZIP archive per term under output/archive",
	)
	args = parser.parse_args()
	return args


#============================================
def main() -> None:
	"""Build active course manifests into complete downloadable files."""
	args = parse_args()
	repo_root = get_repo_root()
	# The shared Markdown configuration names its extension from the repository root so
	# MkDocs and the standalone document renderer load the same implementation.
	repo_root_text = str(repo_root)
	if repo_root_text not in sys.path:
		sys.path.insert(0, repo_root_text)
	docs_root = repo_root / "site_docs"
	# ASVS 2.1.1 and 2.2.1: select the documented source authority directly.
	active_term_root = docs_root / ACTIVE_TERM_DIRECTORY
	downloads_dir = docs_root / "downloads"
	reference_path = repo_root / "pipeline" / "syllabus_reference.docx"
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
	build_lib.syllabus_rendering.check_tools()
	build_lib.syllabus_content.require_public_only_repository(repo_root)
	build_lib.syllabus_content.scan_public_sources(docs_root)
	markdown_extensions, markdown_extension_configs = (
		build_lib.syllabus_content.load_markdown_configuration(mkdocs_config_path)
	)
	manifest_paths = sorted(active_term_root.rglob("syllabus.yml"))
	if not manifest_paths:
		raise RuntimeError(
			f"No syllabus.yml manifests found under site_docs/{ACTIVE_TERM_DIRECTORY}"
		)
	manifests = [
		build_lib.syllabus_model.load_manifest(manifest_path, docs_root)
		for manifest_path in manifest_paths
	]
	for manifest in manifests:
		build_lib.syllabus_content.validate_course_learning_framework(
			manifest.sections,
			docs_root,
		)
		build_lib.syllabus_content.verify_download_links(manifest, downloads_dir)
	expected_names = {
		f"{manifest.download_basename}{suffix}"
		for manifest in manifests
		for suffix in build_lib.syllabus_rendering.MANAGED_DOWNLOAD_SUFFIXES
	}
	outputs_by_term: dict[str, list[pathlib.Path]] = {}
	with tempfile.TemporaryDirectory(
		prefix=".syllabus_build_",
		dir=docs_root,
	) as temporary_name:
		temporary_dir = pathlib.Path(temporary_name)
		staged_downloads_dir = temporary_dir / "downloads"
		staged_downloads_dir.mkdir()
		for manifest in manifests:
			outputs = build_lib.syllabus_rendering.build_one_syllabus(
				manifest,
				staged_downloads_dir,
				reference_path,
				pdf_stylesheet_path,
				markdown_extensions,
				markdown_extension_configs,
				temporary_dir,
			)
			if manifest.term not in outputs_by_term:
				outputs_by_term[manifest.term] = []
			final_outputs = [downloads_dir / output.name for output in outputs]
			outputs_by_term[manifest.term].extend(final_outputs)
		build_lib.syllabus_rendering.publish_downloads(
			staged_downloads_dir,
			downloads_dir,
			expected_names,
		)
	if args.archive:
		archive_outputs(outputs_by_term, repo_root / "output" / "archive")
	return None


if __name__ == "__main__":
	main()
