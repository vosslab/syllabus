## 2026-08-25

### Behavior or Interface Changes

- `devel/rotate_changelog.py` now begins automatic rotation only after the active changelog
  exceeds 800 lines. It partitions older day blocks into 800-900-line target archives, keeps
  every archive strictly below 1000 lines, and refuses an oversized day block before writing.
- Added a vendored-file notice to every root `docs/*.md` file that propagation overwrites in
  consumer repositories. Changelogs and noexist documentation remain consumer-owned.

### Developer Tests and Notes

- `source source_me.sh && python3 -m pytest tests/meta/test_rotate_changelog.py
  tests/test_source_file_line_limit.py` passed: 157 tests. The existing archive files contain
  610, 895, and 914 lines, respectively.
- `source source_me.sh && python3 -m pytest tests/` passed: 1,792 tests.
- `source source_me.sh && python3 -m pytest tests/meta/test_vendored_docs.py
  tests/test_markdown_links.py tests/test_ascii_compliance.py` passed: 204 tests.

## 2026-08-24

### Behavior or Interface Changes

- Preserved prominent phase labels in the Python Graphify tool for graph extraction or update,
  community labeling, and benchmarking.
- Replaced `tools/graphify_map_repo.sh` with the executable Python 3.12 tool
  `tools/graphify_map_repo.py`. It automatically extracts a missing graph or runs the real
  `graphify update .` path for an existing graph. Fresh extraction labels and benchmarks before
  manager-context generation; ordinary updates regenerate manager context immediately.
- Restored explicit Graphify lifecycle controls as `-F`/`--fresh`, `-U`/`--update`, and
  `-C`/`--context` while retaining automatic fresh-or-update selection with no flag. Update mode
  prominently announces and performs a fresh extraction when no graph exists; context prints CLI
  help before the first map exists. Expanded `-h`/`--help` with the complete pipeline,
  requirements, output location, and runnable examples.
- Changed Graphify community labeling to use `claude-cli` by default without an API key. Added
  `-O`/`--ollama` as the explicit local-backend override, retaining the configured model and the
  required Ollama package extra.
- Set fresh Claude CLI labeling to pass `--model=sonnet` explicitly. Graphify community naming now
  uses Sonnet independently of the interactive Claude default, while the Ollama override retains
  its configured local model.
- Fresh builds upgrade `graphifyy[ollama,sql,terraform]`; Ollama-selected fresh builds also pull
  the configured model. Update and context modes perform no package or model setup.
- Made the Graphify pip upgrade quiet and disabled pip's already-unusable local cache. Fresh builds
  no longer print the complete satisfied-dependency inventory or cache-permission warning, while
  installation errors remain visible.
- Replaced the redundant automatic `label --missing-only` update phase with a true fast path:
  existing graphs now run only `graphify update .` before manager-context regeneration. Full
  semantic labeling remains part of fresh extraction instead of a separate relabel lifecycle.
- Limited package upgrades, full labeling, and benchmarking to fresh extraction.
- Replaced generic artifact and policy output with repository-specific manager orientation derived
  from `graphify-out/graph.json`. Context now names the repository, map size, primary domain
  subsystems, highly connected code with source locations, cross-subsystem bridges, and copyable
  queries grounded in the active map. It omits `Corpus Check`, `.graphifyignore` exclusions, and
  generated-file hygiene; the complete Graphify diagnostics remain in `GRAPH_REPORT.md`.
- Capped each cross-area connector at eight displayed community names and appended `and N more` for
  the remainder. This bounds manager-context size without semantically filtering or reordering
  Graphify's connector evidence.
- Strengthened the `Prompt positively` repository principle: lead with the desired action or tool,
  omit irrelevant unwanted actions, and reserve explicit prohibitions for necessary safety or
  correctness boundaries.

### Removals and Deprecations

- Removed the shell tool's positional mode syntax. The Python tool exposes the same lifecycle
  choices as mutually exclusive flags.
- Removed the intermediate `-R`/`--relabel` mode. Fresh extraction is the single intentional route
  for full semantic labeling because labeling already dominates the fresh-build cost.
- Added `meta/propagation/deprecated_paths.txt` so propagation removes the retired
  `tools/graphify_map_repo.sh` path from consumer repositories after shipping the Python tool.

### Decisions and Failures

- The first sandboxed Graphify extraction failed with `Operation not permitted` when Graphify
  started its AST workers. The same command completed outside the sandbox; this is an execution
  permission requirement, not a repository parsing failure.
- The `attack-on-cancer` trial has no Graphify ignore policy. Its final orientation correctly
  warned that generated graph files are visible to Git instead of silently presenting a clean
  repository state.
- Graphify 0.9.49 source confirms that `update` replaces stale names with hub-derived labels and
  that `label --missing-only` treats those names as present. The old incremental label phase could
  not improve them, but still repeated clustering, analysis, and report/JSON/HTML generation.
- Benchmark traverses the graph to measure token reduction but does not improve agent-facing graph
  data. It is therefore outside the routine update path.
- A 19,334-node fresh run inherited the interactive Opus default and exhausted the shared Claude
  session allowance while labeling 711 communities. Graphify continued with fallback names for
  failed batches, so the next intentional fresh build should run after the allowance resets with
  the explicit Sonnet model.
- Sonnet is the conservative default for fresh community labeling because semantic label quality
  matters more than the incremental Haiku savings on an occasional fresh build. Haiku remains a
  one-time comparison candidate on a representative large repository.

### Developer Tests and Notes

- Added focused behavior tests for fresh/update command selection, generated artifact inventory,
  concise orientation output, universal tool routing, and traversal-safe deprecated-path cleanup.
- Exercised real fresh and update lifecycles in this template and `attack-on-cancer`, plus real
  updates in `peptidyle-learning-engine` and `ferrum-chemical-forge`. Final maps ranged from 371
  nodes in this template to 19,047 nodes in Ferrum; every run produced the required report and
  graph artifacts and reached the concise orientation.
- An earlier pre-mode validation snapshot passed all 1,751 collected tests plus focused pyflakes,
  typing, indentation, shebang, ASCII, import-requirement, Bandit, source-size, CLI-help,
  rejected-mode, and `git diff --check` validation.
- After the repository-specific context revision, all 18 focused Graphify behavior cases, direct
  `--context` runs against this template and `attack-on-cancer`, `git diff --check`, and the
  complete 1,778-test suite pass.
- A fresh six-pass independent audit of the mode and help revision identified and corrected the
  incomplete-output context boundary, stale documentation wording, and missing alias/fallback
  coverage before final validation.
- The default Claude CLI update path completed against this repository in 1.9 seconds. Graphify
  found no topology changes, the pre-update and post-update label and analysis sidecars had
  identical hashes, and the workflow regenerated reports, benchmarked, and wrote manager context.
- All 27 focused Graphify behavior tests and the complete 1,787-test suite pass after adding the
  Claude CLI default, Ollama override, and missing-only update lifecycle.
- A connected quiet-mode update completed in 2.2 seconds. Its package phase printed only the
  prominent phase heading before continuing to Graphify update, with no dependency inventory or
  cache warning.
- The final connected fast update completed in 0.6 seconds and ran only `graphify update .` before
  regenerating `MANAGER_CONTEXT.md`. It performed no pip, label-backend, labeling, or benchmark
  phase. Fresh extraction remains the intentional route for replacing degraded community labels.
- A permanent-test policy audit retained the offline command-selection, explicit-mode, fresh-label,
  and Ollama behavior cases, and removed two redundant parser-default checks. The connected runs,
  timing, pip-output probes, installed-source inspection, and help/context executions remain
  one-time implementation evidence instead of permanent pytest cases. All 27 focused lifecycle
  tests and the complete 1,787-test suite pass after the audit.
- After removing the intermediate relabel mode and bounding connector output, all 26 focused
  Graphify behavior tests and the complete 1,786-test suite pass. The direct help check exposes
  only fresh, update, context, and the Ollama backend override.
- After explicitly selecting Sonnet for fresh Claude CLI labels, all 26 focused Graphify behavior
  tests and the complete 1,786-test suite pass. The direct help check identifies Sonnet as the
  Claude label model while retaining the Ollama override.

## 2026-08-21

### Fixes and Maintenance

- Added a vendored-file header to every propagated `test_*.py` file. It warns that local changes
  can and will be overwritten, without identifying or linking an upstream source location.

## 2026-08-20

### Additions and New Features

- Added a universal `.graphifyignore` seed that excludes `tests/`, `devel/`, `tools/`, and
  `docs/` from Graphify repository maps. It propagates to every repo only when absent,
  preserving repository-specific additions after bootstrap.

### Fixes and Maintenance

- Added `/graphify-out/` to `templates/gitignore.universal`, the canonical source for the
  propagation-managed `UNIVERSAL` `.gitignore` block. This preserves Graphify output ignores
  across future propagation runs.
- Added the `pytestqt` to `pytest-qt` import-distribution alias to
  `tests/test_import_requirements.py`.
- Added canonical import-distribution aliases for `applefoundationmodels`, `bricklink`,
  `exiftool`, `graphify`, `markdown_it`, `material`, `screencapturekit`, and `skimage`.
- Added the canonical `graphifyy[ollama,sql,terraform]` PyPI development requirement. This installs
  Graphify's complete base dependency set plus the Ollama backend used by
  `tools/graphify_map_repo.sh`, the `tree-sitter-sql` parser needed for authored database schemas,
  and the `tree-sitter-hcl` parser needed for Terraform repositories, without unrelated optional
  integrations. This keeps the dependency inventory explicit under ASVS 15.1.2 and 15.2.4.
- Corrected the stale propagation test that still classified root `tools/` as template metadata.
  Root tools are universal consumer tools under the current location-based routing policy.

### Developer Tests and Notes

- Confirmed from the `graphifyy` 0.9.48 wheel metadata that the package requires Python 3.10+,
  its `ollama` extra adds the `openai` client, its `sql` extra adds `tree-sitter-sql`, and its
  `terraform` extra adds `tree-sitter-hcl`.
- Confirmed the native Graphify ignore matcher excludes all four universal paths and the
  propagation plan routes `.graphifyignore` to `noexist_files` for every declared repo type.
- The complete pytest suite passes with 1723 tests. Direct ASCII checks and `git diff --check`
  also pass for the changed files.

## 2026-08-19

### Behavior or Interface Changes

- Updated `tools/graphify_map_repo.sh context` output to be strictly Graphify-focused.
  The context now defines what Graphify is, the key commands for query/explain/affected/path,
  and a manager delegation template that uses Graphify evidence to minimize prompt/context
  size when assigning subagent tasks.

## 2026-08-12

### Behavior or Interface Changes

- `templates/rust/docs/RUST_STYLE.md`: defined a security-focused Cargo version policy. New direct
  dependencies use the manager-selected repository form: wildcard `*` for every stable version,
  or `>=LATEST` for an explicit security floor with newer versions eligible. Dependency refreshes
  advance major, minor, and patch components. The guide treats application repositories as the
  normal case, keeps `Cargo.lock` as their exact tested graph, records the future crates.io wildcard
  constraint, and reserves exact requirements for documented temporary constraints.
- Set the Rust toolchain policy to the latest stable compiler with the current manifest floor
  written as `rust-version = "1.97.1"`, matching the installed
  `rustc 1.97.1 (8bab26f4f 2026-07-14)`. Documented that Cargo requires a bare version, so
  `rust-version = ">=1.97.1"` is invalid, and that this MSRV field does not update dependencies.

### Fixes and Maintenance

- Reformatted the Rust examples in `templates/rust/docs/RUST_STYLE.md` with rustfmt's four-space
  indentation instead of tabs, aligning the examples with the guide's own formatting rule.
- Rephrased Rust directives around the desired implementation behavior: explicit imports, safe
  Rust boundaries, concrete library errors, lifetime elision, and behavior-focused tests.
- Baked the repository's source-file ceiling into `templates/rust/docs/RUST_STYLE.md`: use 999
  physical lines as the inclusive maximum and keep generic crate roots, module roots, and test
  indexes as concise routing stubs for descriptively named implementation files.
- Applied the six-pass audit corrections: added a canonical Rust filename map, identified
  `docs.rs` as the hosted documentation service, directed reusable binary behavior into focused
  library modules, reserved generic Cargo filenames for thin entry stubs, made `Cargo.toml` the
  direct source for the selected dependency form, and expressed the quick-start and public-
  documentation rules as positive implementation guidance.
- Condensed the new toolchain and dependency policy to its executable contract: current compiler,
  latest stable direct dependencies, the manager-selected `*` or `>=LATEST` form, lockfile refresh,
  and Cargo gates.
- Aligned the guide with the `rust-code-expert` reference workflow. Existing-project work now names
  the owning crate and module, callers, features, target triple, error contract, and value flow;
  greenfield work starts with domain types plus one success and error test. The completion baseline
  now includes `cargo fmt --check`, `cargo check`, `cargo test`, and Clippy, followed by the matching
  CLI, Tokio, unsafe/FFI, PyO3, or performance oracle.
- Completed a whole-document Rust review against the skill references and current official sources.
  Corrected modern module paths and the private-module `pub use` example; narrowed Python-style
  carryover to repo philosophies; made `Result`, panic, library/application errors, and CLI testing
  precise; added enum/trait/generic selection and explicit async task ownership; updated unsafe for
  2024 extern blocks and unsafe attributes; and added narrow FFI adapters with links to the focused
  Python and WebAssembly guides at their relevant boundaries.
- Split Python binding guidance into `templates/rust/docs/RUST_PYO3_STYLE.md` so
  `RUST_STYLE.md` stays focused on Rust. The new guide owns PyO3 boundary architecture, extension
  and embedding shapes, `cdylib`/`rlib`, current maturin linking, ABI selection, interpreter-bound
  values, domain-error to Python-exception translation, task ownership, and Python integration
  proof. The Rust guide retains the general FFI contract and links to the focused guide.
- Added `templates/rust/docs/RUST_WASM_STYLE.md` for the browser and WASI boundary. It covers
  target and tool selection, a Rust-core/thin-export architecture, `wasm-bindgen` API design,
  JavaScript ownership and error translation, browser and WASI validation, size and performance
  measurement, and current project-owned wasm-bindgen references. `RUST_STYLE.md` links exactly
  twice to each focused guide: at the general FFI boundary and at the foreign-caller proof point.
- Rotated `docs/CHANGELOG.md` after it crossed 1000 lines. Kept the two newest day blocks active
  and moved the 2026-08-07 through 2026-06-30 blocks into `docs/CHANGELOG-2026-08a.md`.

### Developer Tests and Notes

- Confirmed the documented compiler floor against
  `rustc 1.97.1 (8bab26f4f 2026-07-14)`.
- After the six-pass audit corrections, Markdown links, ASCII compliance, whitespace, and the
  source-file line limit pass: 501 targeted tests. The complete `pytest tests/` suite passes with
  1717 tests.

## 2026-08-10

### Additions and New Features

- Added the universal `tests/test_source_file_line_limit.py` hygiene gate. It scans Git-tracked
  authored source files through `file_utils.discover_files`, accepts 999 physical lines, fails at
  1000, and writes the standard complete violation report. Scope includes common programming,
  build, query, template, and authored-document formats (including `.md`) plus conventional names
  such as `Makefile` and `Dockerfile`; generic `.txt`, data, config, generated, notebook, and binary
  formats remain outside the gate.
- Added the optional manager-owned `tests/source_file_line_limit_overrides.txt` contract for exact
  paths to tracked sources outside local control, such as a downloaded normative specification.
  Blank lines and full-line comments are accepted; globs and paths escaping the repo are rejected.
  The propagation manifest marks the file as template-meta so one repo's approvals never ship to
  another repo.

### Behavior or Interface Changes

- `devel/bump_version.py patch` now prepares the next patch release. It treats repo versions such
  as `26.08` and Cargo versions such as `26.8.0` as the same release, previews the affected files,
  and uses plain `Current version` and `Next version` labels.
- Shortened source file line-limit report entries to `path: N lines`; the report header carries
  the shared policy context once.
- Promoted PyPI packaging from the file-presence-driven `templates/python/_pypi/` conditional
  overlay to the real `pypi` repo type under `templates/pypi/`. The inheritance declaration
  `pypi: python` gives packages the complete Python rule set plus publishing-specific files.
  Declaring `python` selects Python tooling; declaring `pypi` adds publishing files.
  Legacy reset configs using `project_type: python` with `pypi: true` normalize to the canonical
  `pypi` marker.

### Fixes and Maintenance

- Split repository classification from repository style: `meta/docs/REPO_TYPE.md` now owns
  marker format, names, inheritance, and multi-type behavior, while `docs/REPO_STYLE.md`
  contains no type-marker contract. Updated human-guidance and propagation references.
- Recorded plan-gate guidance: ground exactness and performance requirements in measured product
  contracts, separate one-time implementation probes from permanent tests, and apply the
  permanent-test checklist before adding suite coverage.
- `tests/test_shebangs.py` now treats exact `#!perl` lines in `.conf` files as WeBWorK
  configuration markers rather than executable shebangs, covered with inline `tmp_path` input.
- Added template-local pytest import paths so `pytest tests/` resolves the template's helper
  modules without adding `PYTHONPATH` or custom commands to the downstream `source_me.sh` seed.
- Removed the fragile reset self-propagation pytest; the whole reset workflow remains in the
  clone-based E2E runner.
- Removed the unused `repolib.files.safe_walk` helper and corrected release-routing documentation.
- Condensed the source-file-size rules to the boundary, scope owner, and override path.
- Reduced `reset_repo.py` to an executable CLI stub. Filesystem mutation and orchestration now
  live in `repolib/reset.py`, while interview and JSON-answer resolution live in
  `repolib/reset_answers.py`.
- Split propagation planning from file mutation: `repolib/files.py` retains file and merge
  operations, and `repolib/plan.py` owns plan construction, typed overlays, and source buckets.
- Split the version command into the small `devel/bump_version.py` CLI,
  `devel/version_lib.py` for shared version behavior, and `devel/version_files.py` for repository
  discovery and updates. `make_release.py` and the PyPI publisher now use the same version library.
- Split PyPI authentication/repository resolution and console/subprocess helpers into
  `pypi_auth.py` and `pypi_support.py`. All three files propagate together into a package repo's
  `devel/` directory and use normal sibling imports; template tests provide those source overlay
  paths through a test-only `PYTHONPATH`.
- Extracted shared overlay routing into `repolib/plan.py`.
- Extracted reset cleanup and completion phases into focused helpers.
- Clarified reset answer parsing and aligned the extracted helpers with repository style.

### Decisions and Failures

- Untracked `local-only/` reference books need no path exception because hygiene discovery already
  uses `git ls-files`. The source selector deliberately does not exclude that directory, preventing
  it from becoming a loophole for tracked oversized code.

### Developer Tests and Notes

- Added an explicit boundary case proving that 999 lines passes and 1000 lines fails.
- Added an inline `tmp_path` behavior case proving the optional override list loads an exact path
  while ignoring comments and blank lines.
- The boundary cases pass, and direct pyflakes validation is clean. The complete new gate reports
  four existing source debts instead of weakening the rule: `devel/bump_version.py` (1329),
  `repolib/files.py` (1332), `reset_repo.py` (1126), and
  `templates/python/_pypi/devel/submit_to_pypi.py` (1349).
- Resolved all four debts above without overrides. The largest replacement module is now
  `templates/pypi/devel/submit_to_pypi.py` at 988 lines. The complete pytest suite passes with
  1727 tests and 2 environment-dependent skips; the standalone real-Git release E2E also passes.
- Exported the staged index into an isolated temporary Git repository and completed a live `pypi`
  reset. The canonical marker, Python inheritance, PyPI support trio, shared version modules, and
  source-release helper were present afterward; template/repolib/reset infrastructure was removed.
