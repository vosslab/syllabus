"""Build propagation plans from template routing rules."""

# Standard Library
import os

# local repo modules
import repolib.model
import repolib.repo
from repolib.files import (
	is_meta_file,
	assert_not_meta_file,
	assert_not_meta,
	should_ship_override,
	load_gitignore_block,
)


#============================================
def resolve_spec_for_type(repo_type: str, template_root: str | None = None, counters: dict | None = None, repo_dir: str | None = None) -> dict:
	"""Build the propagation spec for a repository marker.

	Args:
		repo_type (str): Repository marker, including comma-separated types.
		template_root (str | None): Template root; resolves the source directory when absent.
		counters (dict | None): Optional progress counters.
		repo_dir (str | None): Optional consumer repository for requirement checks.

	Returns:
		dict: Six-bucket propagation specification.

	Raises:
		ValueError: When repo_type contains an unknown type.
	"""
	# Accept consumer tokens from the shared set plus the internal pseudo-types.
	# Pseudo-types (universal, unknown) are checked here explicitly so they never
	# leak into KNOWN_REPO_TYPES and the consumer-facing token set stays clean.
	if repo_type not in ('universal', repolib.model.LANG_UNKNOWN):
		known_types, unknown_types = repolib.model.partition_known_types(repo_type)
		if not known_types or unknown_types:
			raise ValueError(f"unknown repo type {repo_type!r}")
	if template_root is None:
		template_root = repolib.repo.resolve_source_dir(None)
	if repo_type == 'universal':
		repo_type = 'python'  # 'universal' is an alias for python in the fold scheme
	return compute_propagation_plan(template_root, repo_type, counters=counters, repo_dir=repo_dir)


#============================================
def auto_discover_test_files(template_root: str, repo_type: str) -> list[str]:
	"""Discover unlisted test files for a repository type.

	Args:
		template_root (str): Template root containing test overlays.
		repo_type (str): Repository marker used to select overlay chains.

	Returns:
		list[str]: Test paths relative to the consumer repository.
	"""
	spec = resolve_spec_for_type(repo_type, template_root)
	spec_test_files = set(spec['test_files'])

	discovered = []

	# 'universal' is the python alias in the fold scheme, same as resolve_spec_for_type.
	chain_marker = 'python' if repo_type == 'universal' else repo_type
	known_types, _unknown_types = repolib.model.partition_known_types(chain_marker)

	if known_types:
		test_dirs = []
		for chain_type in repolib.model.effective_type_chain(chain_marker):
			overlay_test_dir = os.path.join(template_root, 'templates', chain_type, 'tests')
			if os.path.isdir(overlay_test_dir):
				test_dirs.append(overlay_test_dir)
		if not test_dirs:
			# No chain member has its own overlay tests dir: fall back to the root.
			test_dirs.append(os.path.join(template_root, 'tests'))
	else:
		# No declared token is known: the LANG_UNKNOWN pseudo-type, which is the only
		# marker that reaches here because resolve_spec_for_type above already raised
		# on any other unrecognized token. No chain to walk and no root fallback,
		# matching pre-chain behavior. A comma marker never lands here.
		test_dirs = [os.path.join(template_root, 'templates', repo_type, 'tests')]

	for test_dir in test_dirs:
		if not os.path.isdir(test_dir):
			continue
		for root, dirs, files in os.walk(test_dir, topdown=True, followlinks=False):
			# Filter walk dirs in-place to skip unwanted directories
			dirs[:] = [d for d in dirs if d not in repolib.model.SKIP_WALK_DIRS and not d.startswith('.')]

			for name in files:
				if not (name.startswith('test_') and (name.endswith('.py') or name.endswith('.mjs'))):
					continue
				# Exclude template-meta tests (propagate/reset_repo/detect_repo_type self-tests)
				if any(name.startswith(p) for p in repolib.model.META_TEST_PREFIXES):
					continue
				rel_path = os.path.relpath(os.path.join(root, name), test_dir)
				# Prepend 'tests/' to make it an absolute path from template_root
				full_rel_path = os.path.join('tests', rel_path)
				if full_rel_path not in spec_test_files and full_rel_path not in discovered:
					discovered.append(full_rel_path)

	return discovered


#============================================
def _route_overlay_file(plan: dict, file_rel: str, name: str) -> None:
	"""Route one selected overlay file into its consumer-plan bucket.

	Both typed and shared overlays use the same consumer-path conventions. This
	helper keeps their noexist, devel, test, gitignore, and overwrite handling in
	one place while their separate selection rules remain with their filesystem
	walks.

	Args:
		plan (dict): Propagation plan receiving the routed path.
		file_rel (str): File path relative to its selected overlay root.
		name (str): File basename used to recognize gitignore templates.
	"""
	if file_rel.startswith('noexist/'):
		# Strip 'noexist/' prefix for the consumer path.
		consumer_path = file_rel[8:]
		if not consumer_path:
			return
		if is_meta_file(consumer_path):
			return
		if consumer_path not in plan['noexist_files']:
			assert_not_meta_file(consumer_path)
			plan['noexist_files'].append(consumer_path)
	elif file_rel.startswith('devel/'):
		bare_name = os.path.basename(file_rel)
		if bare_name not in plan['devel_files']:
			assert_not_meta_file(bare_name)
			plan['devel_files'].append(bare_name)
	elif file_rel.startswith('tests/'):
		if file_rel not in plan['test_files']:
			assert_not_meta_file(file_rel)
			plan['test_files'].append(file_rel)
	elif name.startswith('gitignore.'):
		# Gitignore blocks load separately after both overlay walks.
		return
	else:
		# Overlay files shadow universal files at the same consumer destination.
		if file_rel in plan['overwrite_files']:
			plan['overwrite_files'].remove(file_rel)
		assert_not_meta_file(file_rel)
		plan['overwrite_files'].append(file_rel)


#============================================
def compute_propagation_plan(template_root: str, repo_type: str, counters: dict | None = None, repo_dir: str | None = None) -> dict:
	"""
	Compute the six-bucket propagation plan by walking the filesystem.

	Walks template_root and returns a dict with:
	- 'overwrite_files': repo-root-relative paths that overwrite at consumer
	- 'noexist_files': repo-root-relative paths that ship only when missing
	- 'merge_files': paths routed to the set-union @-import merge bucket
	- 'devel_files': bare filenames under devel/ at consumer
	- 'test_files': paths under tests/ at consumer
	- 'gitignore_block': pattern lines for .gitignore

	Args:
		template_root (str): Root directory of template files to scan.
		repo_type (str): Repository type marker. One token (python, typescript, rust,
			swift, other, unknown), several comma-separated tokens (for example
			'python,rust'), or 'all', which expands to every concrete type.
		counters (dict | None): Optional counter dict for progress tracking.
		repo_dir (str | None): Optional repository directory for requirement checks.
			Falls back to template_root for requirement predicate evaluation.

	Precedence (apply in this order; earlier rules win on conflict):
	  1. META_FILES / META_DIRS              -> never ship (drop from all buckets)
	  2. ROUTING_OVERRIDES (via should_ship_override) -> exclude_repos gate only
	  3. UNIVERSAL_NOEXIST                   -> override universal overwrite -> noexist
	  4. templates/<type>/noexist/<path>     -> override typed overlay overwrite -> noexist
	  5. Type overlay wins over universal     -> when both target the same consumer destination,
	                                            the typed overlay version ships (overwrite, devel,
	                                            AND noexist buckets; source resolution in
	                                            find_source_for_bucket checks typed roots first).
	                                            Example: universal Brewfile ships to all types, but
	                                            templates/python/noexist/Brewfile (brew python@3.12)
	                                            shadows it for python repos.

	Routing rules:
	- Universal docs/ (not in META_FILES/META_DIRS) -> overwrite_files
	- Universal tests/ (denylist): ship all non-meta tests/ files by location;
	  skip dotfiles, `_`-scratch, conftest.py (merge-owned), and META_TEST_PREFIXES
	- Universal devel/ -> devel_files
	- Universal tools/ -> overwrite_files
	- Root files in ROOT_PROPAGATE_ALLOWLIST -> overwrite_files
	- ROUTING_OVERRIDES (via should_ship_override) applies to routing decisions
	- Paths in UNIVERSAL_NOEXIST override overwrite_files -> noexist_files
	- templates/<repo_type>/<path> (not noexist) -> overwrite_files
	- templates/<repo_type>/devel/<X> -> devel_files
	- templates/<repo_type>/tests/<X> -> test_files
	- templates/<repo_type>/noexist/<path> -> noexist_files
	- templates/gitignore.universal -> universal gitignore_block
	- templates/<type>/gitignore.<type> for every declared type -> typed gitignore_block
	- templates/shared/<path> -> bucket per shared_overlays rule (ships when repo_type
	  is listed and the optional lacks_file marker is absent); routed by subdirectory
	  like a typed overlay. An uncovered templates/shared/ file raises.
	"""
	plan = {
		'overwrite_files': [],
		'noexist_files': [],
		'merge_files': [],
		'devel_files': [],
		'test_files': [],
		'gitignore_block': [],
	}

	# Recognized types for this marker, in declaration order. 'all' expands here to
	# every concrete type, so it rides the same multi-type path as any other marker
	# instead of a separate aggregation branch. Unrecognized types are dropped: they
	# have no templates/<type>/ overlay and no gitignore source, so carrying them
	# further would add lookups that can never resolve.
	known_types, _unknown_types = repolib.model.partition_known_types(repo_type)

	# Default repo_dir to template_root if not provided (for requirement checks)
	if repo_dir is None:
		repo_dir = template_root

	# Helper: check if a path is under a meta directory
	def is_in_meta_dir(rel_path: str) -> bool:
		parts = rel_path.split(os.sep)
		for part in parts:
			if part in repolib.model.META_DIRS:
				return True
		return False

	# 1. Walk universal files at template root. A marker naming at least one known
	# consumer type receives the universal walk, as does the 'unknown' pseudo-type;
	# derive from the shared set so a future type is covered without editing this.
	if known_types or repo_type == repolib.model.LANG_UNKNOWN:
		for root, dirs, files in os.walk(template_root, topdown=True, followlinks=False):
			# Skip directories: meta, templates (we walk it separately)
			dirs[:] = [d for d in dirs if d not in repolib.model.META_DIRS]

			rel_root = os.path.relpath(root, template_root)
			if rel_root == '.':
				rel_root = ''

			# Process files in this directory
			for name in files:
				file_rel = os.path.join(rel_root, name) if rel_root else name
				# Root dotfiles ship only when the manifest explicitly allowlists them.
				if name.startswith('.') and file_rel not in repolib.model.ROOT_PROPAGATE_ALLOWLIST:
					continue

				# Skip META_FILES (matches by full rel-path OR bare basename for
				# entries that may appear at any depth). docs/active_plans and
				# docs/archive are caught by is_in_meta_dir().
				if is_meta_file(file_rel):
					continue

				# Skip if under a meta directory
				if is_in_meta_dir(file_rel):
					continue

				# Apply routing overrides (exclude_repos gate only)
				override = should_ship_override(file_rel, repo_type, repo_dir)
				if override is False:
					continue

				# Route by prefix/location
				if file_rel.startswith('docs/'):
					assert_not_meta(file_rel)
					plan['overwrite_files'].append(file_rel)
				elif file_rel.startswith('devel/'):
					bare_name = os.path.basename(file_rel)
					if bare_name not in plan['devel_files']:
						assert_not_meta(bare_name)
						plan['devel_files'].append(bare_name)
				elif file_rel.startswith('tests/'):
					bare_name = os.path.basename(file_rel)
					# Denylist routing: ship all non-meta tests/ files by location.
					# Skip underscore-prefixed scratch files (repo convention: _temp
					# = scratch, safe to delete).
					if bare_name.startswith('_'):
						continue
					# conftest.py is owned by merge_conftest (process.py), which
					# additively merges collect_ignore/REPO_HYGIENE_FILTERS; it is
					# not bucket-routed.
					if bare_name == 'conftest.py':
						continue
					# Skip template-meta test prefixes (defensive: template-meta
					# tests must never ship even if one appears at tests/ root).
					if any(bare_name.startswith(p) for p in repolib.model.META_TEST_PREFIXES):
						continue
					# Ship everything else by location.
					if file_rel not in plan['test_files']:
						assert_not_meta(file_rel)
						plan['test_files'].append(file_rel)
				elif file_rel.startswith('tools/'):
					assert_not_meta(file_rel)
					plan['overwrite_files'].append(file_rel)
				elif file_rel in repolib.model.ROOT_PROPAGATE_ALLOWLIST:
					assert_not_meta(file_rel)
					plan['overwrite_files'].append(file_rel)



	# 2. Walk the SELECTED SET of typed overlays under templates/.
	#
	# select_overlay_dirs() returns ordered overlay path segments: the base
	# repo_type folder first (e.g. 'python'), then each conditional overlay
	# '<type>/_<name>' whose configured marker file exists at repo_dir.
	# Overlay SELECTION is what gates conditional content -- a _<name> folder ships
	# only when its marker is present, so the typed-overlay walk does NOT call
	# should_ship_override (the universal walk in block 1 still applies the
	# exclude_repos gate).
	#
	# Standard: EVERY file under a selected overlay ships at its relative path to
	# consumers of that type. The genuine walk-efficiency skips (node_modules,
	# build, dist, caches, .git) still apply. `meta` is removed from the trim so a
	# typed overlay may use that consumer-facing directory name when needed.
	#
	# In the BASE overlay walk (segment == repo_type, no '/'), underscore-prefixed
	# subdirectories are conditional overlays. They are skipped here so the base
	# walk never ships their content wholesale; instead they ride in as their own
	# selected overlay segment when their marker is present.
	typed_overlay_skip_dirs = repolib.model.SKIP_WALK_DIRS - {'meta'}

	overlay_segments = repolib.model.select_overlay_dirs(repo_type, repo_dir)
	for segment in overlay_segments:
		# segment is one element of the effective type chain (e.g. 'python'), which
		# may differ from the raw repo_type marker (e.g. 'python,rust'). A base
		# overlay segment is a bare chain type with no path separator; a
		# A conditional overlay segment contains '/', e.g. 'python/_ci'.
		is_base_overlay = '/' not in segment
		overlay_root = os.path.join(template_root, 'templates', segment)
		if not os.path.isdir(overlay_root):
			continue
		for root, dirs, files in os.walk(overlay_root, topdown=True, followlinks=False):
			# Standard walk-efficiency skips plus dotdirs. In the BASE overlay,
			# also skip underscore-prefixed conditional-overlay folders so they are
			# never shipped wholesale by the base walk.
			dirs[:] = [
				d for d in dirs
				if d not in typed_overlay_skip_dirs and not d.startswith('.')
				and not (is_base_overlay and d.startswith('_'))
			]

			rel_root = os.path.relpath(root, overlay_root)
			if rel_root == '.':
				rel_root = ''

			for name in files:
				# Ship every file under the selected overlay; the META filter below
				# handles exclusions.
				file_rel = os.path.join(rel_root, name) if rel_root else name

				# META guard: typed overlays must filter template-internal files so a stray
				# templates/<type>/README.md (or any META name) cannot ship to consumers.
				# Standard: every file under the overlay ships at its relative path.
				# Only the META_FILES basename/path guard applies here; subdirectories such
				# as tools/ ship verbatim (no META_DIRS directory-segment filtering).
				if is_meta_file(file_rel):
					continue

				# Conditional and base overlays share the same consumer-path routing.
				_route_overlay_file(plan, file_rel, name)

	# 2b. Walk templates/shared/: canonical files routed to a SET of repo types.
	#
	# Unlike the typed overlay (one repo_type per templates/<type>/ folder), a
	# shared file lives once under templates/shared/ and a named shared_overlays
	# rule decides which repo types receive it, plus an optional lacks_file
	# condition. The walk mirrors the typed-overlay routing branches so a shared
	# file lands in the same bucket it would from a typed overlay.
	#
	# Coverage guard: every file under templates/shared/ must be named by at least
	# one rule's paths. An uncovered shared file routes nowhere, which is a config
	# bug, so the walk raises loudly. An empty or absent templates/shared/ tree is a
	# no-op (the isdir guard and the empty covered-paths union both fall through).
	shared_root = os.path.join(template_root, 'templates', 'shared')
	if os.path.isdir(shared_root):
		# Union of every path any rule names, computed once for the coverage guard.
		covered_shared_paths = repolib.model.all_shared_overlay_paths()
		for root, dirs, files in os.walk(shared_root, topdown=True, followlinks=False):
			# Same walk-efficiency skips as the typed overlay; no underscore-folder
			# skip because templates/shared/ has no conditional sub-overlays.
			dirs[:] = [
				d for d in dirs
				if d not in typed_overlay_skip_dirs and not d.startswith('.')
			]

			rel_root = os.path.relpath(root, shared_root)
			if rel_root == '.':
				rel_root = ''

			for name in files:
				# file_rel is the path relative to templates/shared/ (a leading
				# noexist/ prefix is stripped below to yield the consumer path).
				file_rel = os.path.join(rel_root, name) if rel_root else name

				# META guard: a stray META name under templates/shared/ never ships.
				if is_meta_file(file_rel):
					continue

				# Coverage guard: fail loud on a shared file no rule names.
				if file_rel not in covered_shared_paths:
					raise RuntimeError(
						f"shared overlay leak: templates/shared/{file_rel} is not "
						"named by any shared_overlays rule in manifests.yaml; add it "
						"to a rule's paths or remove the file."
					)

				# Does any applicable rule ship this file to this consumer type?
				if not repolib.model.shared_path_ships(file_rel, repo_type, repo_dir):
					continue

				# Shared overlays use the same consumer-path routing as typed overlays.
				_route_overlay_file(plan, file_rel, name)

	# 3. Load gitignore blocks from files
	gitignore_block = []

	# Load universal gitignore block
	universal_gitignore_path = os.path.join(template_root, 'templates', 'gitignore.universal')
	gitignore_block.extend(load_gitignore_block(universal_gitignore_path))

	# Load one typed gitignore block per declared type, in declaration order, so a
	# multi-type marker (and 'all', which expands to every type) carries the union
	# of its families' patterns. A type with no gitignore template contributes
	# nothing: load_gitignore_block returns empty for a missing path.
	for declared_type in known_types:
		typed_gitignore_path = os.path.join(
			template_root, 'templates', declared_type, f'gitignore.{declared_type}',
		)
		gitignore_block.extend(load_gitignore_block(typed_gitignore_path))

	# Deduplicate gitignore block
	plan['gitignore_block'] = list(dict.fromkeys(gitignore_block))

	# 4. Apply UNIVERSAL_NOEXIST overrides
	# Any path in UNIVERSAL_NOEXIST must move from overwrite/test buckets to noexist.
	# Covers tests/TESTS_README.md, which the tests-walker routes to test_files by default.
	for path in repolib.model.UNIVERSAL_NOEXIST:
		if path in plan['overwrite_files']:
			plan['overwrite_files'].remove(path)
		if path in plan['test_files']:
			plan['test_files'].remove(path)
		if path not in plan['noexist_files']:
			plan['noexist_files'].append(path)

	# 5. Apply typed noexist overrides (rule 4: typed noexist shadows typed overwrite)
	# Any path in plan['noexist_files'] that is also in plan['overwrite_files'] must be removed from overwrite
	for path in list(plan['noexist_files']):
		if path in plan['overwrite_files']:
			plan['overwrite_files'].remove(path)

	# 6. Apply MERGE_FILES routing. MERGE wins over OVERWRITE and NOEXIST for the same path.
	# META still wins over MERGE: assert_not_meta() fails loud if a MERGE-tagged file is META.
	for path in repolib.model.MERGE_FILES:
		if path in plan['overwrite_files']:
			plan['overwrite_files'].remove(path)
		if path in plan['noexist_files']:
			plan['noexist_files'].remove(path)
		if path not in plan['merge_files']:
			assert_not_meta(path)
			plan['merge_files'].append(path)

	return plan
