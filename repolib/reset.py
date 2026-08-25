#!/usr/bin/env python3
"""
Bootstrap implementation used by the root reset_repo.py entry point.

Interactive bootstrap tool. Prompts for project type, SPDX licenses, optional
promotion from Python to the PyPI child type, staging, and commit. Writes the REPO_TYPE marker,
installs selected LICENSE files, optionally seeds pyproject.toml, calls
repolib directly to lay down type-dispatched files in bootstrap mode,
truncates README + CHANGELOG, and removes itself. Answers come from either an
interactive interview or a json config (--config); the only other CLI flag is
--dry-run, which previews actions without changing files.
"""

# Standard Library
import os
import sys
import glob
import argparse
import datetime
import tempfile
import subprocess

# local repo modules
import repolib.repo
import repolib.model
import repolib.console
import repolib.process
import repolib.reset_answers

#============================================
def get_repo_root() -> str:
	"""Return the repository root path via git rev-parse.

	Fails with a clear message rather than an obscure subprocess traceback when
	run outside a git repository (or when git is not installed).

	Returns:
		str: Absolute path to the repository root.
	"""
	# Resolve the repo root via git; a non-repo cwd makes git exit non-zero.
	result = subprocess.run(
		["git", "rev-parse", "--show-toplevel"],
		capture_output=True,
		text=True,
		check=False,
	)
	repo_root = result.stdout.strip()
	if result.returncode != 0 or repo_root == "":
		sys.exit(
			"Error: reset_repo must run inside a git repository. "
			"Clone the template, then run reset from the clone root."
		)
	return repo_root


#============================================
def preflight_check(repo_root: str, code_license: str, docs_license: str) -> None:
	"""Verify that selected license files exist before proceeding.

	Args:
		repo_root (str): Repository root containing LICENSES/.
		code_license (str): Selected code-license identifier.
		docs_license (str): Selected documentation-license identifier.
	"""
	code_path = os.path.join(repo_root, f"LICENSES/LICENSE.{code_license}.md")
	if not os.path.isfile(code_path):
		sys.exit(f"license file missing: {code_path}")
	if docs_license != "none":
		docs_path = os.path.join(repo_root, f"LICENSES/LICENSE.{docs_license}.md")
		if not os.path.isfile(docs_path):
			sys.exit(f"license file missing: {docs_path}")


#============================================
def parse_args() -> argparse.Namespace:
	"""Parse command-line arguments and return the populated namespace."""
	parser = argparse.ArgumentParser(
		description="Reset a cloned starter-repo-template to base configuration"
	)
	parser.add_argument(
		"--config",
		dest="config",
		default=None,
		help="Path to a json answers file (non-interactive mode)",
	)
	parser.add_argument(
		"--dry-run",
		dest="dry_run",
		action="store_true",
		help="Print actions without executing",
	)
	return parser.parse_args()


#============================================
# Module-level helpers (extracted from main)
#============================================

#============================================
def dry_run_print(msg: str, dry_run: bool) -> None:
	"""Print a dry-run message when requested.

	Args:
		msg (str): Action description.
		dry_run (bool): Whether the reset is preview-only.
	"""
	if dry_run:
		print(f"DRY-RUN: {msg}")


#============================================
def write_marker(repo_root: str, project_type: str, dry_run: bool) -> int:
	"""Write REPO_TYPE marker atomically via temp + replace.

	The marker is written in canonical form: lowercase types, comma separated,
	no spaces, declaration order preserved, and "all" left as the literal "all"
	rather than expanded. Every caller supplies a project_type that already came
	through normalize_project_type, which produces exactly that form, so this
	writes the value verbatim instead of re-normalizing it here.

	Args:
		repo_root (str): Repository root receiving REPO_TYPE.
		project_type (str): Canonical project-type marker.
		dry_run (bool): Whether to preview the write.

	Returns:
		int: Number of actions taken or announced.
	"""
	marker_path = os.path.join(repo_root, "REPO_TYPE")
	content = f"{project_type}\n"
	if dry_run:
		escaped_content = content.replace('"', '\\"').replace('\n', '\\n')
		dry_run_print(f'write REPO_TYPE ("{escaped_content}")', dry_run)
	else:
		with tempfile.NamedTemporaryFile(
			mode="w", dir=repo_root, delete=False
		) as tmp:
			tmp.write(content)
			tmp_name = tmp.name
		os.replace(tmp_name, marker_path)
	return 1


#============================================
def copy_license(
	repo_root: str, source_path: str, target_filename: str, dry_run: bool,
) -> int:
	"""Copy a license file to the repo root under the given target_filename.

	The caller chooses target_filename (the reset uses LICENSE.<spdx>.md). The
	source file is guaranteed to exist by preflight_check, and a failed read or
	write raises loudly on its own, so no post-copy verification gate is needed.

	Args:
		repo_root (str): Repository root receiving the license.
		source_path (str): Selected source license path.
		target_filename (str): Destination filename at the repository root.
		dry_run (bool): Whether to preview the copy.

	Returns:
		int: 1 (one action taken or announced), for the main() action counter.
	"""
	target_path = os.path.join(repo_root, target_filename)
	if dry_run:
		dry_run_print(f"copy {source_path} -> {target_path}", dry_run)
	else:
		with open(source_path, "r", encoding="utf-8") as src:
			content = src.read()
		with open(target_path, "w", encoding="utf-8") as dst:
			dst.write(content)
	return 1


#============================================
def path_has_tracked_entry(path: str, repo_root: str) -> bool:
	"""Return True when git tracks path (a file) or any file under it (a directory).

	`git rm` on an untracked pathspec exits 128. Checking first lets git_rm and
	git_rm_recursive skip an already-removed path instead of aborting the reset
	mid-run -- the failure mode when reset is re-run on a partially reset repo.

	Args:
		path (str): Repo-relative file or directory pathspec.
		repo_root (str): Repository root the pathspec is anchored to.

	Returns:
		bool: True if at least one tracked entry matches path.
	"""
	# git ls-files exits 0 with empty output when nothing matches; "--" keeps a
	# path that looks like an option from being misread as one.
	result = subprocess.run(
		["git", "ls-files", "--", path],
		check=True, capture_output=True, text=True, cwd=repo_root,
	)
	return bool(result.stdout.strip())


#============================================
def git_rm(path: str, repo_root: str, dry_run: bool) -> int:
	"""Remove a tracked file via git rm, anchored at repo_root.

	Idempotent: an untracked or already-removed path is skipped, not an error, so
	a reset never aborts mid-run on a path that is simply already gone.

	Args:
		path (str): Repo-relative file path to remove.
		repo_root (str): Repository root containing the path.
		dry_run (bool): Whether to preview the removal.

	Returns:
		int: Number of actions taken or announced.
	"""
	if not path_has_tracked_entry(path, repo_root):
		print(f"{path} not tracked -- skipping git rm")
		return 0
	if dry_run:
		dry_run_print(f"git rm {path}", dry_run)
	else:
		# cwd=repo_root so the relative pathspec resolves against the resolved
		# repo root, not the caller's working directory.
		subprocess.run(["git", "rm", path], check=True, capture_output=True, cwd=repo_root)
	return 1


#============================================
def git_rm_recursive(path: str, repo_root: str, dry_run: bool) -> int:
	"""Remove a tracked directory recursively via git rm -r, anchored at repo_root.

	Idempotent: an untracked or already-removed directory is skipped, not an
	error, so a reset never aborts mid-run on a path that is simply already gone.

	Args:
		path (str): Repo-relative directory path to remove.
		repo_root (str): Repository root containing the directory.
		dry_run (bool): Whether to preview the removal.

	Returns:
		int: Number of actions taken or announced.
	"""
	if not path_has_tracked_entry(path, repo_root):
		print(f"{path} not tracked -- skipping git rm -r")
		return 0
	if dry_run:
		dry_run_print(f"git rm -r {path}", dry_run)
	else:
		# cwd=repo_root so the relative pathspec resolves against the resolved
		# repo root, not the caller's working directory.
		subprocess.run(["git", "rm", "-r", path], check=True, capture_output=True, cwd=repo_root)
	return 1


#============================================
def substitute_typescript_package_json(repo_root: str, dry_run: bool) -> int:
	"""Substitute template values in package.json.

	Args:
		repo_root (str): Repository root containing package.json.
		dry_run (bool): Whether to preview the substitution.

	Returns:
		int: Number of actions taken or announced.
	"""
	package_json_path = os.path.join(repo_root, "package.json")
	if not os.path.isfile(package_json_path):
		return 0
	with open(package_json_path, "r") as f:
		content = f.read()
	# Guard: only substitute when placeholders are present, so an existing
	# consumer-customized package.json is left untouched (noexist bucket
	# already protects against overwrite at copy time; this is belt-and-braces).
	if "__REPO_NAME__" not in content:
		return 0
	repo_name = os.path.basename(repo_root)
	# CalVer: zero-padded month per docs/REPO_STYLE.md (0Y.0M), e.g. 2026.06.0
	now = datetime.datetime.now()
	repo_version = f"{now.year}.{now.month:02d}.0"
	if dry_run:
		dry_run_print(
			f"substitute __REPO_NAME__ -> {repo_name}, __REPO_VERSION__ -> {repo_version} in {package_json_path}", dry_run
		)
		return 1
	content = content.replace("__REPO_NAME__", repo_name)
	content = content.replace("__REPO_VERSION__", repo_version)
	with open(package_json_path, "w") as f:
		f.write(content)
	return 1


#============================================
def run_propagate(repo_root: str, dry_run: bool) -> int:
	"""Lay down type-dispatched template files into repo_root via repolib.

	In dry-run, process_repo previews actions without writing.

	Args:
		repo_root (str): Repository root receiving propagated files.
		dry_run (bool): Whether to preview propagation.

	Returns:
		int: Number of actions taken or announced.

	Raises:
		RuntimeError: When propagation is skipped.
	"""
	# Build a initial-setup context and run the propagator directly.
	# process_repo honors context.dry_run: it logs planned actions and skips
	# all file mutations when dry_run is True.
	context = repolib.process.build_context_for_repo(
		repo_path=repo_root,
		dry_run=dry_run,
		initial_setup=True,
		auto_discover=False,
		write_marker=False,
	)
	counters = repolib.console.init_counters()
	result = repolib.process.process_repo(repo_root, context, counters, emit_per_repo_summary=False)
	# None return means process_repo intentionally skipped this repo (self-skip guard
	# or not a repo dir). During reset, propagation must always run to completion.
	if result is None:
		raise RuntimeError(
			f"initial-setup propagation was skipped for repo: {repo_root}\n"
			"process_repo returned None -- the self-skip guard may have fired. "
			"Ensure repolib is configured with initial_setup=True (initial-setup)."
		)
	return 1


#============================================
def read_stub_version(stub_path: str) -> str:
	"""Read the [project] version string from the pyproject stub.

	The stub is minimal (a [project] table with name + version). Parse the
	version line directly so no toml library dependency is introduced.

	Args:
		stub_path (str): Path to templates/pypi/noexist/pyproject.toml.

	Returns:
		str: The version string, e.g. "26.06".

	Raises:
		RuntimeError: When no version line is found in the stub.
	"""
	with open(stub_path, "r") as f:
		stub_lines = f.read().splitlines()
	for line in stub_lines:
		stripped = line.strip()
		# Match a top-level version assignment: version = "..."
		if stripped.startswith("version") and "=" in stripped:
			# Split on the first '=' and strip surrounding quotes/space.
			value = stripped.split("=", 1)[1].strip()
			version = value.strip('"').strip("'")
			return version
	raise RuntimeError(f"no [project] version found in stub: {stub_path}")


#============================================
def seed_pyproject(repo_root: str, dry_run: bool) -> int:
	"""Seed pyproject.toml from the PyPI template and sync VERSION.

	PyPI is a real repo type whose overlay ships independently of this marker
	file. Seeding remains a reset responsibility because a new PyPI package needs
	a minimal pyproject.toml. An existing consumer file is left untouched.
	VERSION is written to match the stub's [project] version.

	Args:
		repo_root (str): Repository root path.
		dry_run (bool): When True, log the actions without writing.

	Returns:
		int: Count of actions taken or announced.
	"""
	pyproject_path = os.path.join(repo_root, "pyproject.toml")
	# A consumer-supplied pyproject already selects the overlay; leave it alone.
	if os.path.isfile(pyproject_path):
		dry_run_print("pyproject.toml already present -- skip seeding", dry_run)
		return 0
	# Anchor the stub on the template checkout, independent of the caller's cwd.
	stub_path = os.path.join(repo_root, "templates/pypi/noexist/pyproject.toml")
	with open(stub_path, "r") as src:
		stub_content = src.read()
	version = read_stub_version(stub_path)
	version_path = os.path.join(repo_root, "VERSION")
	if dry_run:
		dry_run_print(f"seed pyproject.toml from {stub_path}", dry_run)
		dry_run_print(f"write VERSION ({version})", dry_run)
		return 2
	# Write the seed pyproject and a VERSION file holding the same version string.
	with open(pyproject_path, "w") as dst:
		dst.write(stub_content)
	with open(version_path, "w") as vf:
		vf.write(f"{version}\n")
	return 2


# Template-owned root-level directories that must be absent after reset cleanup.
# Only the specific template convention locations for "meta" are checked:
# root meta/ and tests/meta/. Legitimate consumer meta/ elsewhere is not rejected.
# Root tools/ is consumer-facing universal content and remains after reset.
# Legacy template-owned tracked root tools may still be present in template
# history (for example, tools/detect_repo_type.py), so cleanup removes tracked
# root tools while allowing propagated untracked files to stay in place.
TEMPLATE_OWNED_PREFIXES = [
	"templates/",
	"repolib/",
	"LICENSES/",
	"meta/",
	"tests/meta/",
]

# Sentinel scaffold paths that must exist after successful propagation, by project type.
# Each entry is (project_type, relative_path). Rust, swift, other, and the base
# types with no dedicated overlay (scripted, compiled) are skipped (no sentinel).
SCAFFOLD_SENTINELS: dict[str, str] = {
	"typescript": "eslint.config.js",
	"python": "docs/PYTHON_STYLE.md",
	"website": "mkdocs.yml",
}


#============================================
def verify_clean_end_state(repo_root: str, dry_run: bool) -> int:
	"""Verify no template-owned paths remain after cleanup.

	In dry-run, logs the check that would be performed.
	In live mode, checks (a) git ls-files and (b) disk for each TEMPLATE_OWNED_PREFIXES
	entry. Raises RuntimeError listing every leftover path found. Root tools/ is
	not part of TEMPLATE_OWNED_PREFIXES because universal and typed consumer
	tools are expected to remain after reset.

	Returns:
		int: 1 (action taken or announced).

	Raises:
		RuntimeError: When any template-owned path remains tracked or on disk.
	"""
	if dry_run:
		print("DRY-RUN: verify: would check for leftover template-owned paths")
		return 1

	# (a) Check git ls-files for any tracked path under template-owned prefixes
	ls_result = subprocess.run(
		["git", "ls-files"], check=True, capture_output=True, text=True, cwd=repo_root,
	)
	tracked_paths = ls_result.stdout.splitlines()
	leftover_tracked: list[str] = []
	for tracked_path in tracked_paths:
		for prefix in TEMPLATE_OWNED_PREFIXES:
			if tracked_path.startswith(prefix) or tracked_path == prefix.rstrip("/"):
				leftover_tracked.append(f"tracked: {tracked_path}")
				break

	# (b) Check that root-level template-owned directories are absent on disk.
	# For nested entries like tests/meta/, check the full path.
	leftover_disk: list[str] = []
	for prefix in TEMPLATE_OWNED_PREFIXES:
		# strip trailing slash for os.path.isdir check
		check_path = os.path.join(repo_root, prefix.rstrip("/"))
		if os.path.isdir(check_path):
			leftover_disk.append(f"on disk: {prefix}")

	all_leftovers = leftover_tracked + leftover_disk
	if all_leftovers:
		leftover_list = "\n  ".join(all_leftovers)
		raise RuntimeError(
			f"template-owned paths remain after cleanup:\n  {leftover_list}"
		)
	return 1


#============================================
def verify_scaffold_sentinel(repo_root: str, project_type: str) -> None:
	"""Assert that at least one required scaffold path exists after propagation.

	This guards against a "successful but empty" propagation regression, where
	process_repo returns a dict but wrote nothing. Only checked for project types
	that have a known sentinel (typescript, python). Raises RuntimeError on failure.

	Args:
		repo_root (str): Repository root path.
		project_type (str): The project type marker (e.g. 'typescript', 'python,rust').

	Raises:
		RuntimeError: When the sentinel path is absent after propagation.
	"""
	sentinel = None
	for chain_type in repolib.model.effective_type_chain(project_type):
		if chain_type in SCAFFOLD_SENTINELS:
			sentinel = SCAFFOLD_SENTINELS[chain_type]
			break
	if sentinel is None:
		# rust and other have no sentinel defined; skip silently
		return
	sentinel_path = os.path.join(repo_root, sentinel)
	if not os.path.isfile(sentinel_path):
		raise RuntimeError(
			f"propagation completed but required scaffold path is missing: {sentinel}\n"
			f"Expected at: {sentinel_path}\n"
			"process_repo returned success but may have written nothing."
		)


#============================================
def truncate_file(path: str, repo_root: str, dry_run: bool) -> int:
	"""Truncate a repository file.

	Args:
		path (str): Repo-relative file path.
		repo_root (str): Repository root containing the file.
		dry_run (bool): Whether to preview the truncation.

	Returns:
		int: Number of actions taken or announced.
	"""
	full_path = os.path.join(repo_root, path)
	if dry_run:
		dry_run_print(f"truncate {path}", dry_run)
	else:
		open(full_path, "w").close()
	return 1


#============================================
def is_template_source_dir(repo_root: str) -> bool:
	"""Return True when repo_root is the template source checkout.

	Detects the template by folder name only (no remote/origin inspection) so
	the refuse-guard is deterministic and unit-testable.

	Args:
		repo_root (str): Repository root path.

	Returns:
		bool: True when the basename is "starter-repo-template".
	"""
	# normpath strips a trailing slash so basename cannot return "" and bypass the guard
	return os.path.basename(os.path.normpath(repo_root)) == "starter-repo-template"


#============================================
def confirm_plan(
	answers: repolib.reset_answers.ResetAnswers,
	dry_run: bool,
	skip_confirm: bool,
) -> None:
	"""Print the plan summary and prompt the user to confirm before applying.

	Args:
		answers: The resolved bootstrap answers describing what will be applied.
		dry_run: When True, prefix the mode label with DRY-RUN for clarity.
		skip_confirm: When True, skip printing and the Proceed prompt entirely.
			Set to True in config mode (bool(args.config)) because config runs
			are non-interactive; interactive mode passes False so the user sees
			the summary and must type 'y' to proceed.
	"""
	if not skip_confirm:
		mode = "DRY-RUN" if dry_run else "LIVE"
		print("")
		print("Summary:")
		print(f"  type:         {answers.project_type}")
		print(f"  code license: {answers.code_license}")
		print(f"  docs license: {answers.docs_license}")
		print(f"  pypi:         {'yes' if answers.pypi else 'no'}")
		print(f"  stage:        {'yes' if answers.stage else 'no'}")
		print(f"  commit:       {'yes' if answers.commit else 'no'}")
		print(f"  mode:         {mode}")
		confirm_input = input("Proceed? [y/N]: ").strip()
		if not confirm_input or confirm_input.lower() != "y":
			sys.exit("Aborted")


#============================================
def remove_changelog_archives(repo_root: str, dry_run: bool) -> int:
	"""Remove tracked changelog archives from the template history.

	Args:
		repo_root (str): Repository root containing the template history files.
		dry_run (bool): When True, announce removals without changing files.

	Returns:
		int: Number of archive removals taken or announced.
	"""
	action_count = 0
	for pattern in repolib.model.META_FILE_PATTERNS:
		for archive_path in sorted(glob.glob(os.path.join(repo_root, pattern))):
			archive_rel = os.path.relpath(archive_path, repo_root)
			action_count += git_rm(archive_rel, repo_root, dry_run)
	return action_count


#============================================
def remove_templates_directory(repo_root: str, dry_run: bool) -> int:
	"""Remove tracked template files after propagation has finished.

	Args:
		repo_root (str): Repository root containing the template directory.
		dry_run (bool): When True, announce removal without changing files.

	Returns:
		int: Number of actions taken or announced.
	"""
	templates_dir = os.path.join(repo_root, "templates")
	if dry_run:
		if os.path.isdir(templates_dir):
			dry_run_print("git rm -r templates/", dry_run)
			return 1
		dry_run_print("templates/ absent -- skip removal", dry_run)
		return 0

	ls_templates = subprocess.run(
		["git", "ls-files", "templates/"],
		check=True, capture_output=True, text=True, cwd=repo_root,
	)
	if ls_templates.stdout.strip():
		return git_rm_recursive("templates/", repo_root, dry_run)
	if os.path.isdir(templates_dir):
		print("templates/ is untracked -- skipping git rm (directory left on disk)")
	else:
		print("templates/ absent -- nothing to remove")
	return 0


#============================================
def remove_root_tools(repo_root: str, dry_run: bool) -> int:
	"""Remove tracked root tools while retaining freshly propagated tools.

	Args:
		repo_root (str): Repository root containing the root tools directory.
		dry_run (bool): When True, announce removal without changing files.

	Returns:
		int: Number of actions taken or announced.
	"""
	if dry_run:
		dry_run_print("git rm -r tools/", dry_run)
		return 1
	ls_tools = subprocess.run(
		["git", "ls-files", "tools/"],
		check=True, capture_output=True, text=True, cwd=repo_root,
	)
	if ls_tools.stdout.strip():
		return git_rm_recursive("tools/", repo_root, dry_run)
	print("tools/ has no tracked files -- skipping git rm (any propagated files left on disk)")
	return 0


#============================================
def find_tracked_meta_directories(repo_root: str) -> list[str]:
	"""Return shallowest tracked directories named ``meta`` in the repository.

	Args:
		repo_root (str): Repository root whose Git index is inspected.

	Returns:
		list[str]: Repo-relative directory paths ending with a slash.
	"""
	ls_result = subprocess.run(
		["git", "ls-files"], check=True, capture_output=True, text=True, cwd=repo_root
	)
	meta_dirs: list[str] = []
	seen = set()
	for tracked_path in ls_result.stdout.splitlines():
		parts = tracked_path.split("/")
		for idx, part in enumerate(parts):
			if part == "meta":
				meta_dir = "/".join(parts[: idx + 1]) + "/"
				if meta_dir not in seen:
					seen.add(meta_dir)
					meta_dirs.append(meta_dir)
				break
	meta_dirs.sort(key=len)
	pruned: list[str] = []
	for candidate in meta_dirs:
		covered = any(candidate.startswith(ancestor) and candidate != ancestor for ancestor in pruned)
		if not covered:
			pruned.append(candidate)
	return pruned


#============================================
def remove_tracked_meta_directories(repo_root: str, dry_run: bool) -> int:
	"""Remove every shallowest tracked directory named ``meta``.

	Args:
		repo_root (str): Repository root whose template meta directories are removed.
		dry_run (bool): When True, announce removals without changing files.

	Returns:
		int: Number of actions taken or announced.
	"""
	action_count = 0
	for meta_dir in find_tracked_meta_directories(repo_root):
		action_count += git_rm_recursive(meta_dir, repo_root, dry_run)
	return action_count


#============================================
def remove_non_pypi_submitter(repo_root: str, project_type: str, dry_run: bool) -> int:
	"""Remove the PyPI upload script when the selected type does not use PyPI.

	Args:
		repo_root (str): Repository root containing the upload script.
		project_type (str): Canonical project type marker.
		dry_run (bool): When True, announce removal without changing files.

	Returns:
		int: Number of actions taken or announced.
	"""
	declared_types = repolib.model.expand_marker_types(project_type)
	if "pypi" in declared_types:
		return 0
	if dry_run:
		dry_run_print("git rm -f devel/submit_to_pypi.py", dry_run)
		return 1
	ls_pypi = subprocess.run(
		["git", "ls-files", "devel/submit_to_pypi.py"],
		check=True, capture_output=True, text=True, cwd=repo_root,
	)
	if not ls_pypi.stdout.strip():
		print("devel/submit_to_pypi.py untracked -- skipping git rm")
		return 0
	subprocess.run(
		["git", "rm", "-f", "devel/submit_to_pypi.py"],
		check=True, capture_output=True, text=True, cwd=repo_root,
	)
	return 1


#============================================
def clean_template_files(repo_root: str, project_type: str, dry_run: bool) -> int:
	"""Remove template-only files after selected project files are propagated.

	Args:
		repo_root (str): Repository root receiving the reset.
		project_type (str): Canonical project type marker.
		dry_run (bool): When True, announce cleanup without changing files.

	Returns:
		int: Number of cleanup actions taken or announced.
	"""
	action_count = remove_changelog_archives(repo_root, dry_run)
	action_count += remove_templates_directory(repo_root, dry_run)
	action_count += git_rm("propagate_style_guides.py", repo_root, dry_run)
	action_count += git_rm_recursive("repolib/", repo_root, dry_run)
	action_count += git_rm("pip_requirements-meta.txt", repo_root, dry_run)
	action_count += remove_root_tools(repo_root, dry_run)
	action_count += remove_tracked_meta_directories(repo_root, dry_run)
	action_count += remove_non_pypi_submitter(repo_root, project_type, dry_run)
	action_count += git_rm("reset_repo.py", repo_root, dry_run)
	return action_count


#============================================
def print_next_steps(project_type: str) -> None:
	"""Print the first setup command appropriate for the selected project type."""
	type_chain = repolib.model.effective_type_chain(project_type)
	if "python" in type_chain:
		print("\nNext steps:")
		print("  pip install -r pip_requirements.txt && pip install -r pip_requirements-dev.txt")
	elif project_type == "typescript":
		print("\nNext steps:")
		print("  npm install && bash devel/setup_playwright.sh")
		print("  pip install -r pip_requirements-dev.txt")
	elif project_type == "rust":
		print("\nNext steps:")
		print("  cargo build")
		print("  pip install -r pip_requirements-dev.txt")
	else:
		print("\nNext steps:")
		print("  pip install -r pip_requirements-dev.txt")


#============================================
def complete_reset(
	repo_root: str,
	project_type: str,
	dry_run: bool,
	stage: bool,
	commit: bool,
	action_count: int,
) -> None:
	"""Verify the reset, optionally stage or commit it, then print its outcome.

	Args:
		repo_root (str): Repository root receiving the reset.
		project_type (str): Canonical project type marker.
		dry_run (bool): When True, announce actions without changing files.
		stage (bool): Whether to stage all reset changes.
		commit (bool): Whether to commit the staged reset changes.
		action_count (int): Completed action count before verification.
	"""
	action_count += verify_clean_end_state(repo_root, dry_run)
	if stage:
		action_count += 1
		if dry_run:
			dry_run_print("git add -A", dry_run)
		else:
			subprocess.run(["git", "add", "-A"], check=True, capture_output=True, cwd=repo_root)
	if commit:
		action_count += 1
		commit_msg = f"initial commit: reset repo to base template ({project_type})"
		if dry_run:
			dry_run_print(f"git commit -m {repr(commit_msg)}", dry_run)
		else:
			subprocess.run(
				["git", "commit", "-m", commit_msg], check=True, capture_output=True, cwd=repo_root
			)
	if dry_run:
		print(f"DRY-RUN: {action_count} actions planned. No files changed.")
	else:
		if commit:
			print("Committed.")
		elif not stage:
			print("Working tree modified. Run 'git add -A && git commit' when ready.")
		else:
			print("Staged. Run 'git commit' when ready.")
		subprocess.run(["git", "status", "--short"], check=False, cwd=repo_root)
	print_next_steps(project_type)


#============================================
def main() -> None:
	"""Run the interactive bootstrap flow."""
	args = parse_args()
	repo_root = get_repo_root()

	# === phase: source-repo refuse guard (SAFETY CRITICAL) ===
	# Run FIRST, before any phase and regardless of --dry-run/--config: refuse to
	# reset the template source checkout itself.
	if is_template_source_dir(repo_root):
		sys.exit(
			"This repo is named starter-repo-template. Clone or rename it to "
			"the consumer project name before running reset."
		)

	# === phase: gather answers (config or interview) ===
	# Config mode (--config) is non-interactive; the interview asks, in order:
	# project type, code license, docs license, PyPI (python only), stage
	# changes, create a commit. Staging and commit are driven by these answers.
	if args.config:
		answers = repolib.reset_answers.answers_from_config(args.config)
	else:
		answers = repolib.reset_answers.answers_from_interview(repo_root)

	# Pull the resolved answers into locals for the phase bodies below.
	project_type = answers.project_type
	code_license = answers.code_license
	docs_license = answers.docs_license
	publish_pypi = answers.pypi
	stage = answers.stage
	commit = answers.commit

	preflight_check(repo_root, code_license, docs_license)

	# === phase: summary and confirmation ===
	# Config mode auto-skips the Proceed prompt; interactive mode keeps it.
	skip_confirm = bool(args.config)
	confirm_plan(answers, args.dry_run, skip_confirm)

	action_count = 0

	# === phase: marker write ===
	action_count += write_marker(repo_root, project_type, args.dry_run)

	# === phase: license install ===
	code_source = os.path.join(repo_root, f"LICENSES/LICENSE.{code_license}.md")
	action_count += copy_license(repo_root, code_source, f"LICENSE.{code_license}.md", args.dry_run)

	if docs_license != "none":
		docs_source = os.path.join(repo_root, f"LICENSES/LICENSE.{docs_license}.md")
		action_count += copy_license(repo_root, docs_source, f"LICENSE.{docs_license}.md", args.dry_run)

	# === phase: cleanup LICENSES/ ===
	action_count += git_rm_recursive("LICENSES/", repo_root, args.dry_run)

	# === phase: seed pyproject (BEFORE propagate) ===
	# A PyPI repo receives its publishing overlay from the pypi type. Seed its
	# minimal pyproject.toml before propagation so all later phases see it.
	if publish_pypi:
		action_count += seed_pyproject(repo_root, args.dry_run)

	# === phase: propagate (direct repolib call) ===
	action_count += run_propagate(repo_root, args.dry_run)

	# === phase: scaffold sentinel check ===
	# After propagation completes (live only), assert that the required per-type
	# scaffold path exists. Guards against "successful but empty" propagation.
	if not args.dry_run:
		verify_scaffold_sentinel(repo_root, project_type)

	# === phase: typescript-specific work ===
	# Must run AFTER propagate so the noexist bucket has placed package.json at repo root.
	if project_type == "typescript":
		action_count += substitute_typescript_package_json(repo_root, args.dry_run)

	# === phase: truncate boilerplate ===
	action_count += truncate_file("README.md", repo_root, args.dry_run)
	action_count += truncate_file("docs/CHANGELOG.md", repo_root, args.dry_run)

	# === phase: cleanup template-only files ===
	# Run after propagation and changelog truncation, while the template source
	# paths are still available to the helpers that enumerate them.
	action_count += clean_template_files(repo_root, project_type, args.dry_run)

	# === phase: verify, stage, commit, and hand off ===
	complete_reset(
		repo_root,
		project_type,
		args.dry_run,
		stage,
		commit,
		action_count,
	)


if __name__ == "__main__":
	main()
