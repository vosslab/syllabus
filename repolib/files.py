"""File operations, I/O helpers, and merge logic."""

# Standard Library
import os
import shutil
import filecmp
import fnmatch
import collections.abc

# local repo modules
import repolib.console
import repolib.model
import repolib.repo


#============================================
# META leak guard
#============================================

def is_meta_file(file_rel: str) -> bool:
	"""Return True when a path is template-meta and must never ship.

	A path is meta when it matches META_FILES exactly (by full rel-path or bare
	basename) OR matches any META_FILE_PATTERNS glob (e.g. changelog archives).

	Args:
		file_rel (str): Repo-root-relative file path.

	Returns:
		bool: True when the path must never ship.
	"""
	basename = os.path.basename(file_rel)
	if file_rel in repolib.model.META_FILES or basename in repolib.model.META_FILES:
		return True
	for pattern in repolib.model.META_FILE_PATTERNS:
		if fnmatch.fnmatch(file_rel, pattern):
			return True
	return False


def assert_not_meta_file(file_rel: str) -> None:
	"""
	Fail loud if a path is template-meta and must never ship to a consumer.

	Delegates to is_meta_file, which checks both META_FILES (exact basename or
	full rel-path) AND META_FILE_PATTERNS globs (e.g. changelog archive
	patterns like docs/CHANGELOG-*.md). This is the consumer-path-safe guard:
	it protects per-consumer files the template must never clobber (README.md,
	VERSION, .gitignore, etc.) without rejecting paths that merely traverse a
	META_DIRS component. Legitimate consumer paths from a typed overlay may use
	a directory name that is template metadata at the source root, so the
	apply-time dispatcher uses this check, not the stricter directory-traversal
	check in assert_not_meta.

	Args:
		file_rel: Repo-root-relative file path about to be copied to a consumer.

	Raises:
		RuntimeError: file_rel matches META_FILES by basename or rel-path.
	"""
	if is_meta_file(file_rel):
		raise RuntimeError(
			f"META leak: {file_rel!r} is in META_FILES and must never ship. "
			"Fix the upstream walker or dispatcher branch that produced this entry."
		)


def assert_not_meta(file_rel: str) -> None:
	"""
	Fail loud if a template-relative path would land in any bucket despite being META.

	Called at every UNIVERSAL-walk plan-construction append site. Catches walker
	leaks where a universal-walk branch forgets to filter a META file or a path
	under a META_DIRS directory.

	This is the strict guard: it rejects both META_FILES matches AND any path
	traversing a META_DIRS component. Apply-time and typed-overlay code use
	assert_not_meta_file instead because their paths name consumer destinations.

	Args:
		file_rel: Template-root-relative file path about to be added to a bucket.

	Raises:
		RuntimeError: file_rel matches META_FILES by basename or rel-path,
		              OR any path component matches META_DIRS.
	"""
	assert_not_meta_file(file_rel)
	parts = file_rel.split(os.sep)
	for part in parts:
		if part in repolib.model.META_DIRS:
			raise RuntimeError(
				f"META leak: {file_rel!r} traverses META_DIRS component {part!r} "
				"and must never ship. Fix the upstream walker or dispatcher branch."
			)


#============================================
# Routing overrides
#============================================

def should_ship_override(file_rel: str, repo_lang: str, repo_dir: str) -> bool | None:
	"""
	Apply routing overrides on top of the walker's default routing.

	Location is now the primary propagation determinant, so the only override this
	predicate evaluates is `exclude_repos`: it blocks a file when the destination
	repo basename is on that file's exclusion list. All other keys are unlisted and
	return None (the walker's location-based decision stands).

	The `repo_lang` parameter is retained for caller compatibility but is no longer
	consulted; language gating moved into the template folder layout.

	Args:
		file_rel (str): Repo-root-relative file path.
		repo_lang (str): Repository language type (kept for caller compatibility; unused).
		repo_dir (str): Repository directory path.

	Returns:
		bool or None: False if exclude_repos blocks the file for this destination repo,
		              None if no override applies (the common case).
	"""
	rule = repolib.model.ROUTING_OVERRIDES.get(file_rel)
	if rule is None:
		return None
	# Per-destination-repo exclusion: block when this dest repo is on the exclude list.
	exclude_repos = rule.get('exclude_repos')
	if exclude_repos is not None and os.path.basename(os.path.normpath(repo_dir)) in exclude_repos:
		return False
	return None


#============================================
# File and text mutation helpers
#============================================

def copy_file_safe(src: str, dst: str, dry_run: bool, action: str = 'copy', message: str | None = None) -> bool:
	"""
	Copy a file from src to dst, preserving mode bits (executable bit).

	Returns False on dry-run (logs dry-run line), True on actual copy.
	Raises exception on error (no try/except per code style).

	Args:
		src (str): Source file path.
		dst (str): Destination file path.
		dry_run (bool): If True, only log without copying.
		action (str): Action word for dry-run message (default 'copy').
		message (str): Optional pre-formatted message. If provided, overrides default formatting.

	Returns:
		bool: False on dry-run, True on actual copy.
	"""
	if dry_run:
		if message is None:
			message = f"{src} -> {dst}"
		repolib.console.log_action(action, message, dry_run=True)
		return False
	shutil.copy2(src, dst)
	return True


def make_dir_safe(path: str, dry_run: bool) -> bool:
	"""
	Create a directory if it does not exist.

	Returns False on dry-run, True on actual mkdir.
	"""
	if dry_run:
		repolib.console.log_action("create", path, dry_run=True)
		return False
	os.makedirs(path, exist_ok=True)
	return True


def copy_if_changed(source: str, dest: str, dry_run: bool, counters: dict, action_label: str = 'copy', format_path: collections.abc.Callable | None = None) -> str:
	"""
	Copy source to dest only if they differ; return indicator and suppress or log outcome.

	Args:
		source (str): Path to source file.
		dest (str): Path to destination file.
		dry_run (bool): If True, only log planned action without copying.
		counters (dict): Mutable counter dict to increment for SKIP and NO CHANGE (quiet tags).
			When counters is provided, these tags are counted but not printed.
		action_label (str): Label for dry-run output (default 'copy').
		format_path (callable | None): Optional function to format path pairs.
			Called as format_path(source, dest) and should return formatted path string.
			If None, uses default "{source} -> {dest}" format.

	Returns:
		str: One of 'skipped_source', 'no_change', 'copied', 'updated'.

	Behavior:
		- If source missing: logs SKIP to counters, returns 'skipped_source'.
		- If dest exists and files match: logs NO CHANGE to counters, returns 'no_change'.
		- Otherwise: copies/updates, logs COPIED or UPDATED (non-quiet, always printed),
		  returns 'copied' or 'updated'.

	Note:
		Message-prefix ('source:', 'self:', 'path:') drives counter dispatch via log_action().
		Callers that log non-standard prefixes must ensure log_action() handles them.

	Uses copy_file_safe() and make_dir_safe() underneath.
	"""
	def _default_format_path(s: str, d: str) -> str:
		"""Default path formatter when none provided."""
		return f"{s} -> {d}"

	if format_path is None:
		format_path = _default_format_path

	# Check if source exists
	if not os.path.isfile(source):
		repolib.console.log_action("skip", f"source: {source} (not found)", counters)
		return 'skipped_source'

	# Check if dest exists and compare
	dest_exists = os.path.isfile(dest)
	is_same = False
	if dest_exists:
		is_same = filecmp.cmp(source, dest, shallow=False)
	if is_same:
		repolib.console.log_action("no change", dest, counters)
		return 'no_change'

	# Ensure parent directory exists
	dest_parent = os.path.dirname(dest)
	if dest_parent and not os.path.isdir(dest_parent):
		make_dir_safe(dest_parent, dry_run)

	# Copy the file
	formatted_path = format_path(source, dest)
	action = 'update' if dest_exists else 'copy'
	copy_file_safe(source, dest, dry_run, action=action, message=formatted_path if dry_run else None)
	if not dry_run:
		if dest_exists:
			repolib.console.log_action("update", formatted_path)
			return 'updated'
		else:
			repolib.console.log_action("copy", formatted_path)
			return 'copied'
	else:
		# On dry-run, copy_file_safe() already printed; return the action we would take
		return 'updated' if dest_exists else 'copied'


def read_text(path: str) -> str:
	"""
	Read a UTF-8 text file.

	Returns the file contents as a string.
	"""
	with open(path, 'r', encoding='utf-8') as f:
		return f.read()


def write_text(path: str, content: str, dry_run: bool = False, action: str = 'update') -> bool:
	"""
	Write content to a UTF-8 text file.

	Returns False on dry-run (logs dry-run line), True on actual write.
	"""
	if dry_run:
		repolib.console.log_action(action, path, dry_run=True)
		return False
	with open(path, 'w', encoding='utf-8') as f:
		f.write(content)
	return True


#============================================
def load_gitignore_block(path: str) -> list[str]:
	"""
	Load gitignore block from file, filtering blanks and comments.

	Args:
		path (str): Path to gitignore source file.

	Returns:
		list[str]: List of non-blank, non-comment lines (stripped).
	"""
	if not os.path.isfile(path):
		return []
	content = read_text(path)
	lines = []
	for line in content.split('\n'):
		stripped = line.rstrip('\n').strip()
		if stripped and not stripped.startswith('#'):
			lines.append(stripped)
	return lines


#============================================
def normalize_path(path: str) -> str:
	"""
	Normalize a path for stable filesystem comparisons.
	"""
	return os.path.normcase(os.path.realpath(os.path.abspath(path)))


#============================================
def remove_gitignore_entries(gitignore_path: str, entries: list[str], dry_run: bool) -> int:
	"""
	Remove deprecated entries from .gitignore file.

	Args:
		gitignore_path (str): Path to .gitignore file.
		entries (list[str]): List of gitignore patterns to remove.
		dry_run (bool): If True, do not write changes.

	Returns:
		int: Number of lines removed.
	"""
	if not os.path.isfile(gitignore_path):
		return 0

	content = read_text(gitignore_path)
	lines = [line.rstrip('\n') for line in content.split('\n')]

	entries_set = set(entry.strip() for entry in entries)
	filtered_lines = []
	removed_count = 0

	for line in lines:
		stripped = line.strip()
		if stripped in entries_set:
			removed_count += 1
			continue
		filtered_lines.append(line.rstrip())

	if removed_count == 0:
		return 0

	new_content = '\n'.join(filtered_lines) + '\n' if filtered_lines else ''
	write_text(gitignore_path, new_content, dry_run)

	return removed_count


#============================================
def deduplicate_gitignore(gitignore_path: str, dry_run: bool, counters: dict | None = None) -> None:
	"""
	Remove duplicate lines and trailing whitespace from .gitignore file.
	Preserves all empty lines and comments for visual grouping.

	Updates counters dict in-place if provided: increments 'merged_count' when changes
	are made (duplicates removed and/or whitespace cleaned).

	Args:
		gitignore_path (str): Path to .gitignore file.
		dry_run (bool): If True, do not write changes.
		counters (dict | None): Optional counter dict to update with merged_count.
	"""
	if not os.path.isfile(gitignore_path):
		return

	content = read_text(gitignore_path)
	original_lines = [line.rstrip('\n') for line in content.split('\n')]

	stripped_lines = [line.rstrip() for line in original_lines]

	seen = set()
	unique_lines = []
	for line in stripped_lines:
		if line == '':
			unique_lines.append(line)
		elif line not in seen:
			seen.add(line)
			unique_lines.append(line)

	duplicates_removed = len(stripped_lines) - len(unique_lines)
	whitespace_cleaned = any(orig != stripped for orig, stripped in zip(original_lines, stripped_lines))

	if duplicates_removed == 0 and not whitespace_cleaned:
		return

	new_content = '\n'.join(unique_lines) + '\n' if unique_lines else ''
	write_text(gitignore_path, new_content, dry_run)

	if not dry_run and counters is not None:
		counters['merged_count'] += 1


#============================================
def spaced_block(block_lines: list[str]) -> list[str]:
	"""
	Return a managed block's content with exactly one trailing blank line.

	Stacked managed blocks are easier to scan when a blank line separates them.
	The separator is carried as the LAST line of a block's own content rather than
	emitted before the next header, which is what keeps repeated runs idempotent:
	replace_managed_block swaps a block's whole content region at once, so a
	trailing blank is rewritten each run instead of accumulating one blank per run.
	Any blank lines already at the end are collapsed to exactly one, so a file
	written by an older version converges on the first run.

	Args:
		block_lines (list[str]): Block content lines, without the header.

	Returns:
		list[str]: The same content with exactly one trailing blank line.
	"""
	# Drop any existing trailing blanks first so the result is always exactly one.
	trimmed = list(block_lines)
	while trimmed and trimmed[-1].strip() == '':
		trimmed.pop()
	return trimmed + ['']


#============================================
def replace_managed_block(lines: list[str], header: str, block_lines: list[str]) -> list[str]:
	"""
	Replace or append a named managed block in a line list.

	Finds the named block (starting with header) and replaces it with the new content.
	If the block is absent, appends at end. Idempotent: works correctly on multiple calls.

	Args:
		lines (list[str]): Existing lines.
		header (str): Block header to search for (e.g., '# === UNIVERSAL ===').
		block_lines (list[str]): New block content (without header).

	Returns:
		list[str]: New line list with the block replaced or appended.
	"""
	start_idx = -1
	for i, line in enumerate(lines):
		if line.startswith(header):
			start_idx = i
			break

	if start_idx == -1:
		# Block not found: append
		result = list(lines)
		result.append(header)
		result.extend(block_lines)
		return result

	# Block found: replace
	end_idx = start_idx + 1
	for i in range(start_idx + 1, len(lines)):
		if lines[i].startswith('# ==='):
			end_idx = i
			break
	else:
		end_idx = len(lines)

	result = lines[:start_idx] + [header] + block_lines + lines[end_idx:]
	return result


# MERGE bucket: set-union merge for @-import list files. See meta/docs/MERGE_BUCKET_SPEC.md.

#============================================
def _load_claude_md_deprecated() -> list[str]:
	"""Load the maintainer-curated strip list for CLAUDE.md merges."""
	return load_deprecation_list('meta/propagation/deprecated_claude_md.txt', _get_template_root())


def merge_at_imports_safe(source: str, dest: str, dry_run: bool, counters: dict) -> str:
	"""
	Merge a flat @-import list file by set-union additions + deprecation strips.

	Designed for CLAUDE.md and other files that are nothing more than a list of
	@filename imports plus optional non-@ commentary. No fences required: the
	template content set is added on top of consumer content, and any line
	matching the meta/propagation/deprecated_claude_md.txt list is removed.

	Outcomes:
		'created'   -- dest missing; wrote template verbatim.
		'merged'    -- consumer file updated (additions, removals, or both).
		'unchanged' -- no additions, no removals; consumer already in sync.
		'error'     -- source file missing.
	"""
	if not os.path.isfile(source):
		counters['errors'] += 1
		repolib.console.log_action("error", f"merge source missing: {source}")
		return 'error'

	src_text = read_text(source)

	if not os.path.isfile(dest):
		dest_parent = os.path.dirname(dest)
		if dest_parent and not os.path.isdir(dest_parent):
			make_dir_safe(dest_parent, dry_run)
		write_text(dest, src_text, dry_run, action='create')
		if not dry_run:
			repolib.console.log_action("create", dest)
			counters['created_count'] += 1
		return 'created'

	dest_text = read_text(dest)
	deprecated = set(_load_claude_md_deprecated())

	# split('\n') (not splitlines) preserves trailing-newline state on round-trip.
	src_lines = src_text.split('\n')
	dest_lines = dest_text.split('\n')

	consumer_at_imports = {ln.strip() for ln in dest_lines if ln.strip().startswith('@')}
	pruned_lines = [ln for ln in dest_lines if ln.strip() not in deprecated]

	additions: list[str] = []
	additions_seen: set[str] = set()
	for ln in src_lines:
		stripped = ln.strip()
		if not stripped.startswith('@'):
			continue
		if stripped in consumer_at_imports or stripped in deprecated or stripped in additions_seen:
			continue
		additions.append(stripped)
		additions_seen.add(stripped)

	# Splice additions after the last @-line in the pruned consumer so the
	# new entries cluster with the existing import block.
	if additions:
		insertion_idx = None
		for idx in range(len(pruned_lines) - 1, -1, -1):
			if pruned_lines[idx].strip().startswith('@'):
				insertion_idx = idx + 1
				break
		if insertion_idx is None:
			# No existing @-lines; prepend at top (after any leading blanks).
			insertion_idx = 0
			while insertion_idx < len(pruned_lines) and not pruned_lines[insertion_idx].strip():
				insertion_idx += 1
		new_lines = pruned_lines[:insertion_idx] + additions + pruned_lines[insertion_idx:]
	else:
		new_lines = pruned_lines

	merged = '\n'.join(new_lines)

	# Preserve dest's trailing-newline state.
	if dest_text.endswith('\n') and not merged.endswith('\n'):
		merged += '\n'
	elif not dest_text.endswith('\n') and merged.endswith('\n'):
		merged = merged.rstrip('\n')

	if merged == dest_text:
		repolib.console.log_action("no change", dest, counters)
		return 'unchanged'

	write_text(dest, merged, dry_run, action='merge')
	if not dry_run:
		repolib.console.log_action("merge", dest)
		counters['merged_count'] += 1
	return 'merged'


#============================================
def merge_conftest(source_file: str, dest_file: str) -> str | None:
	"""
	Inject the canonical managed blocks into a destination conftest.py.

	The canonical source tests/conftest.py carries three managed blocks:
	  1. the collect_ignore block (everything before the REPO_HYGIENE_FILTERS
	     marker), which excludes the e2e and playwright tiers from pytest.
	  2. the REPO_HYGIENE_FILTERS block (the documented comment block ending in
	     REPO_HYGIENE_FILTERS = {}), the repo-local hygiene-exclusion registry.
	  3. the optional helpers menu block, introduced by a line containing
	     OPTIONAL_HELPERS_MENU, which documents optional conftest helpers.

	Detection tokens:
	  - Block 1: presence of 'collect_ignore' in dest text.
	  - Block 2: presence of 'REPO_HYGIENE_FILTERS' in dest text.
	  - Block 3: presence of 'OPTIONAL_HELPERS_MENU' in dest text.

	All three blocks ship additively. Any other consumer content (imports,
	fixtures, consumer-set values) is preserved verbatim. A missing block is
	appended in canonical order; an existing or edited block is never
	overwritten.

	Graceful degradation when the source is missing a marker:
	  - All three markers present -> three-way split.
	  - Marker 3 absent -> two-way split, ship blocks 1-2 only (back-compat).
	  - Marker 2 absent, marker 3 present -> block 1 is pre-menu text; block 3
	    follows; block 2 is empty.
	  - Neither marker 2 nor marker 3 -> entire source is block 1; no crash.

	Args:
		source_file (str): Path to the canonical tests/conftest.py.
		dest_file (str): Path to the consumer repo's tests/conftest.py.

	Returns:
		str | None: Merged content when an update is needed, None when the
		consumer already carries all managed blocks present in the source.
	"""
	source_text = read_text(source_file)
	if not os.path.isfile(dest_file):
		return source_text

	# --- split the canonical source into up to three managed blocks ---
	# Locate marker 2: first line that starts '# REPO_HYGIENE_FILTERS'.
	# Locate marker 3: first line that contains 'OPTIONAL_HELPERS_MENU'.
	source_lines = source_text.split('\n')
	marker2_idx = None
	marker3_idx = None
	for idx, line in enumerate(source_lines):
		if marker2_idx is None and line.startswith('# REPO_HYGIENE_FILTERS'):
			marker2_idx = idx
		if marker3_idx is None and 'OPTIONAL_HELPERS_MENU' in line:
			marker3_idx = idx

	# Build the three block strings according to which markers were found.
	if marker2_idx is not None and marker3_idx is not None:
		# Full three-way split.
		collect_ignore_block = '\n'.join(source_lines[:marker2_idx]).rstrip()
		filters_block = '\n'.join(source_lines[marker2_idx:marker3_idx]).rstrip()
		menu_block = '\n'.join(source_lines[marker3_idx:]).rstrip()
	elif marker2_idx is not None:
		# Marker 3 absent: two-way split only; no menu block.
		collect_ignore_block = '\n'.join(source_lines[:marker2_idx]).rstrip()
		filters_block = '\n'.join(source_lines[marker2_idx:]).rstrip()
		menu_block = ''
	elif marker3_idx is not None:
		# Marker 2 absent but marker 3 present: pre-menu text is block 1.
		collect_ignore_block = '\n'.join(source_lines[:marker3_idx]).rstrip()
		filters_block = ''
		menu_block = '\n'.join(source_lines[marker3_idx:]).rstrip()
	else:
		# Neither marker present: entire source is the collect_ignore block.
		collect_ignore_block = source_text.rstrip()
		filters_block = ''
		menu_block = ''

	dest_text = read_text(dest_file)
	if dest_text.strip() == '':
		return source_text

	# Determine which blocks the destination is missing.
	# Each "need" flag is only True when the source carries that block AND the
	# destination does not yet have the detection token.  Checking block content
	# here means a source that lacks a marker will never falsely trigger an
	# append for that block, and the function returns None correctly.
	need_collect = 'collect_ignore' not in dest_text
	need_filters = bool(filters_block) and ('REPO_HYGIENE_FILTERS' not in dest_text)
	need_menu = bool(menu_block) and ('OPTIONAL_HELPERS_MENU' not in dest_text)

	if not need_collect and not need_filters and not need_menu:
		return None

	# Preserve all existing consumer content; append only the missing block(s)
	# in canonical order: collect_ignore, REPO_HYGIENE_FILTERS, menu.
	merged = dest_text.rstrip()
	if need_collect:
		merged += '\n\n' + collect_ignore_block
	if need_filters:
		merged += '\n\n' + filters_block
	if need_menu:
		merged += '\n\n' + menu_block
	merged += '\n'
	return merged


#============================================
def merge_gitignore_blocks(repo_dir: str, repo_type: str, template_root: str, context: 'repolib.model.PropagateContext', counters: dict | None = None) -> None:
	"""
	Manage .gitignore as a sequence of named blocks delimited by '# === <NAME> ==='.
	Blocks: UNIVERSAL (always), then one <TYPE_UPPERCASE> block per declared type
	whose gitignore template is non-empty, in declaration order.
	If block header exists, replace just that block. If not, append at end.
	User-added lines OUTSIDE any managed block stay untouched.

	Updates counters dict in-place if provided: increments 'created_count' or 'merged_count'
	depending on whether .gitignore was newly created or updated.

	Args:
		repo_dir (str): Repository directory path.
		repo_type (str): Repository type marker; may declare several comma-separated
			types (for example 'python,rust'), or 'all' for every type.
		template_root (str): Template root directory for gitignore sources.
		context (PropagateContext): Context with dry_run and path formatting info.
		counters (dict | None): Optional counter dict to update with created/merged counts.
	"""
	gitignore_path = os.path.join(repo_dir, '.gitignore')

	file_exists = os.path.isfile(gitignore_path)
	existing_lines = []
	if file_exists:
		content = read_text(gitignore_path)
		existing_lines = [line.rstrip('\n') for line in content.split('\n')]

	# Load universal and type-specific gitignore blocks from files.
	# Universal source lives under templates/ (not a canonical consumer-root filename).
	gitignore_universal_path = os.path.join(template_root, 'templates', 'gitignore.universal')
	universal_lines = load_gitignore_block(gitignore_universal_path)

	universal_header = '# === UNIVERSAL ==='

	# Build new content
	new_lines = list(existing_lines)
	new_lines = replace_managed_block(new_lines, universal_header, spaced_block(universal_lines))

	# One managed block per declared type that has a non-empty source, in
	# declaration order. 'all' expands to every type here, so an 'all' repo
	# receives every typed block rather than only the universal one.
	# replace_managed_block replaces-or-appends per header, so repeated runs on the
	# same marker leave the file byte-identical.
	for declared_type in repolib.model.expand_marker_types(repo_type):
		gitignore_typed_path = os.path.join(
			template_root, 'templates', declared_type, f'gitignore.{declared_type}',
		)
		type_lines = load_gitignore_block(gitignore_typed_path)
		if not type_lines:
			continue
		type_header = f"# === {declared_type.upper()} ==="
		new_lines = replace_managed_block(new_lines, type_header, spaced_block(type_lines))

	# Build content with proper trailing newline
	content = '\n'.join(new_lines)
	if content and not content.endswith('\n'):
		content += '\n'

	existing_content = '\n'.join(existing_lines)
	if existing_lines and not existing_content.endswith('\n'):
		existing_content += '\n'

	# Write if needed
	if not file_exists:
		display_path = repolib.model.format_path_pair(gitignore_path, gitignore_path, repo_dir, context)
		if context.dry_run:
			repolib.console.log_action("create", display_path, dry_run=True)
		else:
			with open(gitignore_path, 'w', encoding='utf-8') as f:
				f.write(content)
			repolib.console.log_action("create", display_path)
			if counters is not None:
				counters['created_count'] += 1
	elif content != existing_content:
		display_path = repolib.model.format_path_pair(gitignore_path, gitignore_path, repo_dir, context)
		if context.dry_run:
			repolib.console.log_action("update", display_path, dry_run=True)
		else:
			with open(gitignore_path, 'w', encoding='utf-8') as f:
				f.write(content)
			repolib.console.log_action("update", display_path)
			if counters is not None:
				counters['merged_count'] += 1



#============================================
def ensure_changelog_file(changelog_path: str, dry_run: bool) -> bool:
	"""
	Create docs/CHANGELOG.md if missing.

	Args:
		changelog_path (str): Path to docs/CHANGELOG.md.
		dry_run (bool): If True, do not write changes.

	Returns:
		bool: True if file was created, False otherwise.
	"""
	if os.path.exists(changelog_path):
		return False

	write_text(changelog_path, '', dry_run, action='create')
	return True


#============================================
def ensure_tests_dir(tests_dir: str, dry_run: bool) -> bool:
	"""
	Create the tests directory if missing.

	Args:
		tests_dir (str): Path to tests directory.
		dry_run (bool): If True, do not write changes.

	Returns:
		bool: True if directory was created, False otherwise.
	"""
	if os.path.isdir(tests_dir):
		return False
	if dry_run:
		return True
	os.makedirs(tests_dir, exist_ok=True)
	return True


#============================================
def load_deprecation_list(rel_path: str, template_root: str) -> list[str]:
	"""Read newline-delimited deprecation entries from meta/propagation/.

	Skips blank lines and comment lines (those starting with '#').
	Raises FileNotFoundError if the file is missing; loud failure beats
	silent missing-deprecation scrub.
	"""
	full_path = os.path.join(template_root, rel_path)
	with open(full_path) as f:
		return [ln.strip() for ln in f if ln.strip() and not ln.lstrip().startswith('#')]


#============================================
# Module-level constants for testing
#============================================
def _get_template_root() -> str:
	"""Compute template root directory lazily."""
	return repolib.repo.resolve_source_dir(None)


def _get_deprecated_test_scripts() -> list[str]:
	"""Load deprecated test scripts list lazily."""
	return load_deprecation_list('meta/propagation/deprecated_tests.txt', _get_template_root())


def _get_deprecated_gitignore_entries() -> list[str]:
	"""Load deprecated gitignore entries list lazily."""
	return load_deprecation_list('meta/propagation/deprecated_gitignore.txt', _get_template_root())


# Lazy-loaded module-level exports for test access
TEMPLATE_ROOT = None
DEPRECATED_TEST_SCRIPTS = None
DEPRECATED_GITIGNORE_ENTRIES = None


def _init_module_constants() -> None:
	"""Initialize module-level constants once on first access."""
	global TEMPLATE_ROOT, DEPRECATED_TEST_SCRIPTS, DEPRECATED_GITIGNORE_ENTRIES
	if TEMPLATE_ROOT is not None:
		return  # Already initialized
	TEMPLATE_ROOT = _get_template_root()
	DEPRECATED_TEST_SCRIPTS = _get_deprecated_test_scripts()
	DEPRECATED_GITIGNORE_ENTRIES = _get_deprecated_gitignore_entries()


# Initialize on first import
_init_module_constants()
