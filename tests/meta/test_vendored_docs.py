"""Verify overwrite-propagated root docs identify themselves as vendored."""

# Standard Library
import pathlib

# local repo modules
import file_utils
import repolib.plan


VENDORED_NOTICE = (
	"> This file is vendored. Local changes can and will be overwritten by propagation."
)
REPO_ROOT = pathlib.Path(file_utils.get_repo_root())


#============================================

def test_overwrite_propagated_root_docs_include_vendored_notice() -> None:
	"""Every root doc delivered through overwrite warns consumer-side editors."""
	plan = repolib.plan.compute_propagation_plan(str(REPO_ROOT), "python")
	doc_paths = [
		rel for rel in plan["overwrite_files"]
		if rel.startswith("docs/") and (REPO_ROOT / rel).is_file()
	]
	missing = [
		rel for rel in doc_paths
		if VENDORED_NOTICE not in (REPO_ROOT / rel).read_text(encoding="utf-8")
	]
	assert not missing, f"Overwrite-propagated docs missing vendored notice: {missing}"
