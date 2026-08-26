# Plan: Unify Markdown includes behind one repo-owned engine

## Context

The repository expands `--8<-- "path.md"` includes with **two different engines** that do not
implement the same grammar:

- Website: `pymdownx.snippets`, configured at `mkdocs.yml:48`.
- DOCX and PDF composition: a hand-written regex expander,
  `expand_shared_includes()` at `pipeline/build_syllabi.py:275`, called from
  `compose_markdown()` (lines 535 and 543) and `validate_course_learning_framework()` (line 321).
- The PDF path then loads the whole MkDocs extension stack a second time
  (`load_markdown_configuration()` at line 439 feeding `run_markdown_html()` at line 698), so
  `pymdownx.snippets` runs again over already-expanded text.
- DOCX goes straight to Pandoc (`run_pandoc_docx()`, line 674) and never sees that second pass.

This is a real parity hazard, not a theoretical one. `pymdownx.snippets` supports recursive
includes, block syntax, section selection, and alternate marker lengths. The custom expander
recognizes exactly one shape: a full-line, double-quoted `--8<--` directive
(`INCLUDE_LINE_PATTERN`, line 34). Any PyMdown-valid include outside that shape passes through the
custom expander as **raw text**, is then expanded by snippets in the HTML/PDF path, and ships as a
literal `--8<--` line in the DOCX. Silent, per-format divergence.

Two further findings shape the design:

1. `pipeline/build_syllabi.py` is **997 physical lines**. `docs/REPO_STYLE.md` caps tracked source
   at 999 and `tests/test_source_file_line_limit.py` enforces it. Extracting the include engine is
   forced by repo rules, not merely desirable.
2. `mkdocs.yml:6-8` already declares `exclude_docs: */shared/fragments/*` and `generated/*`, so the
   fragment convention exists in the repo but the include path never consults it.

Intended outcome: one strict include grammar, owned by the repository, shared by website, DOCX,
and PDF, with an explicit fragment-authorization rule that is tested for consistency against the
site's nav exclusions.

## Objectives

- Expand every include through exactly one code path for all three outputs.
- Reject unsupported include syntax loudly instead of letting it diverge per format.
- Authorize include targets by an explicit rule, and test that rule against `exclude_docs`.
- Bring `pipeline/build_syllabi.py` back under the 999-line cap by extraction.
- Prove parity with evidence read from the actual HTML, DOCX, and PDF artifacts.

## Design philosophy

Fix the design, not the symptom (`docs/REPO_STYLE.md` core philosophies). The symptom is "DOCX
sometimes shows raw markup"; the design flaw is two include languages. Adding
`mkdocs-include-markdown-plugin` would be a third language with a *larger* grammar (absolute
paths, `../`, globs, recursion, its own template syntax) and is MkDocs-only, so it cannot serve
DOCX or PDF at all. Rejected.

On authorization, an earlier draft of this plan made "excluded from nav" *mean* "includable",
reading the rule straight out of `exclude_docs`. External review identified that as overreach, and
the objection holds: `exclude_docs` answers "is this a page?", which is broader than "may this be
included?". Under that equivalence a future `drafts/*` exclusion would silently authorize drafts
as fragments. So the engine now owns an explicit fragment rule, and a test asserts the rule stays
a **subset** of `exclude_docs` -- every fragment is excluded from nav, but not every exclusion is
a fragment. Explicit authorization, enforced consistency, no duplicated list.

- Evidence strategy for uncertain methods: the parity claim is verified by reading the three built
  artifacts, not by reasoning about the expanders. The MkDocs hook-loading assumption in T5 is
  verified by a permanent test rather than a one-time experiment, so a future MkDocs upgrade that
  invalidates it fails a test instead of silently shipping raw markup.

## Scope

- Create `pipeline/build_lib/markdown_includes.py` holding the include grammar, the fragment
  authorization rule, and path resolution.
- Add `pipeline/mkdocs_hooks.py`, an `on_page_markdown` adapter calling that engine.
- Rewire `pipeline/build_syllabi.py` to call the engine; remove `pymdownx.snippets` from
  `mkdocs.yml`.
- Give pytest access to `pipeline/` through `tests/conftest.py`.
- Add `tests/test_markdown_includes.py` (grammar and authorization) and
  `tests/e2e/e2e_include_parity.py` (built-artifact parity).
- Record the change in `docs/CHANGELOG.md`; refresh `docs/CODE_ARCHITECTURE.md`,
  `docs/FILE_STRUCTURE.md`, and `docs/FILE_FORMATS.md`.

## Non-goals

- Adopt `mkdocs-include-markdown-plugin` or any other inclusion plugin.
- Support recursive includes, globs, partial-file selection, or block syntax.
- Change the eight live include sites' content or location.
- Decompose the rest of `pipeline/build_syllabi.py` into further `build_lib/` modules.
- Add an orphan-fragment completeness test, or a second fragments-are-not-pages assertion.

## Current state summary

Eight live include sites, all already conforming to the strict grammar and the fragment-directory
rule:

| Include target | Included by |
| --- | --- |
| `generated/FALL_2026_IMPORTANT_DATES.md` | `fall_2026/shared/IMPORTANT_DATES.md` |
| `fall_2026/shared/fragments/INSTRUCTOR_CONTACT_DETAILS.md` | `shared/INSTRUCTOR_INFORMATION.md`, and `COURSE_DETAILS.md` in biotech / genetics / biostats |
| `fall_2026/shared/fragments/ROOSEVELT_LEARNING_GOALS.md` | `COURSE_LEARNING_FRAMEWORK.md` in biotech / genetics / biostats |

Existing include tests: `tests/test_syllabus_builder.py:202` (happy path) and `:223` (parent
traversal). Nothing covers empty, absolute, URL, nested, non-fragment target, symlink escape, or
unsupported PyMdown syntax.

## User-facing contract

The include language, stated once so all three consumers agree:

- One supported form, on a line of its own: `--8<-- "<path>"`, double-quoted, nothing else on the
  line.
- `<path>` is **always resolved relative to `docs_root`** (`site_docs/`), never relative to the
  including document. `"fall_2026/shared/fragments/X.md"` means `site_docs/fall_2026/shared/
  fragments/X.md` no matter which file includes it. This matches both the current expander
  (`resolved_docs_root / include_name`, line 292) and the current `pymdownx.snippets`
  `base_path: site_docs`, so no live content changes.
- A target is includable only when its `docs_root`-relative path contains a directory named
  `fragments` or `generated`.
- Included files are inlined once. They may not themselves contain includes.
- Any line containing the `--8<--` marker that is not exactly the supported form is an error.

## Architecture boundaries and ownership

`pipeline/` holds runnable and externally-invoked entry points. `build_lib/` holds library units,
imported only by scripts inside `pipeline/`.

```text
pipeline/
  build_site.py          <- front door, runnable
  build_syllabi.py       <- runnable: main(), parse_args()
  mkdocs_hooks.py        <- loaded by MkDocs by file path
  build_lib/
    markdown_includes.py <- this plan, the only include engine
```

`pipeline/` is a folder, never an importable package. Callers write
`import build_lib.markdown_includes`, which needs `pipeline/` on the import path. Each entry point
supplies that itself, so `source_me.sh` needs no change:

- `python3 pipeline/build_syllabi.py` puts `pipeline/` at `sys.path[0]` by running the script from
  that directory.
- MkDocs supplies it for the hook: `Hooks._load_hook`
  (`mkdocs/config/config_options.py:1202-1207` in the installed 3.12 site-packages) inserts
  `os.path.dirname(hook_path)` onto `sys.path` around `exec_module`, then restores it. Placing the
  hook at `pipeline/mkdocs_hooks.py` puts `pipeline/` on the path exactly while the hook loads.
- pytest gets it from `tests/conftest.py`, beside the existing repo-root insert at lines 8-10.

Because MkDocs restores `sys.path` right after loading the hook, the hook imports
`build_lib.markdown_includes` **at module level**; T5 covers this with a test.

## Work packages

Each task below is independently verifiable. `Depends on: none` means it can start immediately.

Each package lists an **implementation dependency**: the work it cannot be *finished* without.
That is distinct from when drafting can begin. Four lanes can start immediately: **T4** (import
topology) touches only `tests/`; **T7** can draft its test module against the interface T1
declares in this plan, then finish once T1 and T2 land; the documentation work in the close-out
section needs only the User-facing contract above; and **T1**/**T2** proceed as the critical path. **T3**, **T5**, **T6**, and **T9** serialize behind
them in that order. Maximum useful parallelism is four doers; the shared file
`tests/test_markdown_includes.py` is owned by T7, with T5 and T8 appending their own test
functions to it after T7 establishes the module.

### Work package: T1 -- engine module with grammar and resolution

- Depends on: none
- Touch points: `pipeline/build_lib/markdown_includes.py` (new)
- Move `INCLUDE_LINE_PATTERN` and the body of `expand_shared_includes()` into
  `expand_includes(markdown_text, source_path, docs_root)`. Preserve today's guarantees: resolve
  under `docs_root`, reject `..`, reject missing, reject empty, reject nested.
- Fix the validation order explicitly, because the T7 matrix distinguishes `ValueError` from
  `FileNotFoundError` and that distinction becomes accidental if the filesystem is touched too
  early. The order is: (1) validate syntax and path safety -- shape, absolute paths, `..`, URLs;
  (2) authorize the target against T2's fragment rule; (3) only then touch the filesystem for
  existence, symlink resolution, and content. Without this, `https://example.com/x.md` or
  `../missing.md` would surface as a misleading `FileNotFoundError` instead of naming the real
  problem.
- Implement the single unsupported-syntax rule. Rather than enumerating PyMdown forms, apply one
  invariant to the content the engine scans: every occurrence of the `--8<--` marker must be part
  of a line that fully matches `INCLUDE_LINE_PATTERN`, otherwise raise `ValueError` naming file
  and line. This covers fences, section selects, alternate marker lengths, and single-quoted or
  unquoted paths with one rule instead of a second approximate PyMdown parser.
- This invariant was checked against the repository before adopting it, since it makes the marker
  illegal in prose. A repo-wide search finds **zero** prose or code-fence occurrences inside
  `site_docs/`: the only non-directive hits are fenced documentation examples in
  `docs/USAGE.md:37` and `docs/FILE_FORMATS.md:52`, which the engine never scans. Should a
  syllabus page ever need to discuss the syntax literally, that is a deliberate future change to
  the language, not a silent breakage.
- Acceptance criteria: `expand_includes` inlines a conforming include and raises a distinct,
  message-bearing exception for every other case in the T7 matrix.

### Work package: T2 -- fragment authorization rule

- Depends on: T1
- Touch points: `pipeline/build_lib/markdown_includes.py`
- Add `FRAGMENT_DIRECTORY_NAMES = ("fragments", "generated")` and authorize a target only when its
  `docs_root`-relative parts contain one of those names. Explicit, term-independent: a future
  `spring_2027/shared/fragments/` works with no edit.
- Both names carry an inclusion role, confirmed as a content decision: `generated/` holds
  machine-written Markdown fragments meant to be included, which is exactly what
  `FALL_2026_IMPORTANT_DATES.md` (written by `pipeline/sync_important_dates.py`, consumed only by
  `fall_2026/shared/IMPORTANT_DATES.md`) is. If non-Markdown artifacts ever land under
  `generated/`, that signals the directory's role has broadened and the rule should be revisited
  then, rather than being pre-emptively narrowed now.
- Acceptance criteria: all eight live include targets authorize; a real page such as
  `fall_2026/biotech/COURSE_DETAILS.md` is rejected.

### Work package: T3 -- exporter integration

- Depends on: T1, T2
- Touch points: `pipeline/build_syllabi.py`
- Import `build_lib.markdown_includes` under a `# local repo modules` heading, delete lines 34-35
  and 274-305, and update the three call sites (321, 535, 543).
- Acceptance criteria: `tests/test_source_file_line_limit.py` passes, which is the authoritative
  gate; `pytest tests/` stays green.

### Work package: T4 -- pytest import path and test import model

- Depends on: none
- Touch points: `tests/conftest.py`, `tests/test_syllabus_builder.py`, `tests/test_important_dates.py`
- Insert `<repo_root>/pipeline` on `sys.path` beside the existing repo-root insert at lines 8-10.
- Convert **every** package-form import repo-wide, not just the one this plan touches: a search
  finds `import pipeline.build_syllabi` (`tests/test_syllabus_builder.py:10`, with 22 call sites)
  and `import pipeline.sync_important_dates` (`tests/test_important_dates.py:7`). Leaving either
  behind would let Python load the same source under two module names and keep duplicate module
  state -- the exact hazard that makes a half-migration worse than none.
- Rationale: the user's stated model is that `pipeline/` is a folder, not an importable package,
  and that pytest gets its path through `conftest.py`. External review correctly noted that
  namespace-package imports are defined Python behavior, so this is a deliberate architecture
  decision, not a bug fix.
- Acceptance criteria: `pytest tests/` passes from a shell that never sourced `source_me.sh`, and
  no `import pipeline.` form remains anywhere in the repository.

### Work package: T5 -- MkDocs hook and its loading test

- Depends on: T1, T2
- Touch points: `pipeline/mkdocs_hooks.py` (new), `tests/test_markdown_includes.py`
- Define `on_page_markdown(markdown, page, config, files)`, take `docs_root` from
  `config["docs_dir"]`, and call `expand_includes`. Keep the engine import at module level.
- Add a permanent test that drives **MkDocs' own loader**, not a reproduction of it. Reproducing
  `spec_from_file_location` plus a `sys.path` insert would only test the plan's simulation of
  MkDocs and would keep passing after MkDocs changed. Instead, call
  `mkdocs.config.load_config(str(repo_root / "mkdocs.yml"))`, retrieve the loaded hook from the
  resulting config, and invoke its `on_page_markdown` against a fixture include, asserting the
  expansion. `load_config` runs the actual `Hooks._load_hook`, so a MkDocs release that changes
  hook loading fails here.
- Keep the assertions on **behavior** -- the hook loaded and expands Markdown after MkDocs restored
  its temporary import path -- rather than on the internal shape of `config["plugins"]`, which
  MkDocs could restructure without breaking the hook contract.
- This is fast: config load only, no site build, so it belongs in the pytest lane rather than
  `tests/e2e/`.
- Acceptance criteria: the hook test passes; it fails if the engine import is moved inside the
  handler, and it fails if `mkdocs.yml` stops registering the hook.

### Work package: T6 -- retire the second grammar

- Depends on: T3, T5
- Touch points: `mkdocs.yml`
- Add `hooks: [pipeline/mkdocs_hooks.py]` (MkDocs resolves hook paths relative to the config
  file). Delete the `pymdownx.snippets` block at lines 48-53. Because
  `load_markdown_configuration()` reads that same list, this removes snippets from the PDF render
  stack in the same edit, leaving one expander repo-wide.
- **Convergence audit**, the acceptance condition that proves this plan's central claim. After the
  edit, enumerate every production reference to `expand_includes`, `expand_shared_includes`,
  `pymdownx.snippets`, and the `--8<--` marker, and confirm exactly one expansion path remains:
  `expand_includes`, reached by the exporter (T3) and the hook (T5), with no residual second
  expander anywhere. Record the enumeration in the changelog entry. This single check is worth
  more than any individual edge case, because it verifies the architectural objective directly
  rather than sampling its consequences.
- Acceptance criteria: the convergence audit finds one expansion path;
  `python3 pipeline/build_site.py` succeeds; `site/` contains no `--8<--`.

### Work package: T7 -- grammar and authorization tests

- Depends on: T1, T2, T4
- Touch points: `tests/test_markdown_includes.py` (new), `tests/test_syllabus_builder.py`
- Build the matrix below against a `tmp_path` fixture docs tree. Remove the two superseded include
  tests at `tests/test_syllabus_builder.py:202-231`.

| Case | Expected |
| --- | --- |
| Conforming include of a fragment | inlined, stripped |
| Path resolved against `docs_root`, not the including file | inlines the `docs_root`-relative target |
| Missing file | `FileNotFoundError` |
| Empty / whitespace-only fragment | `ValueError` |
| Absolute path | `ValueError` |
| Parent traversal (`../x.md`) | `ValueError` |
| Remote URL | `ValueError` |
| Nested include inside a fragment | `ValueError` |
| Target outside a fragment directory (a real page) | `ValueError` |
| Symlink pointing outside `site_docs` | `ValueError` |
| PyMdown block form, section select, alternate marker, single-quoted or unquoted path | `ValueError`, unsupported syntax |

- Acceptance criteria: every row asserts its specific exception type and a message naming the
  offending file.

### Work package: T8 -- authorization/exclusion consistency test

- Depends on: T2
- Touch points: `tests/test_markdown_includes.py`, `pip_requirements-dev.txt`
- Assert the subset relation that replaces the rejected equivalence: every **Markdown** file under
  a `fragments` or `generated` directory in `site_docs/` is matched by the `exclude_docs` spec in
  `mkdocs.yml`. The population is `*.md` specifically, matching what the engine can actually
  include (`SAFE_INCLUDE_PATH_PATTERN` already requires a `.md` suffix), so a future image or JSON
  asset under those directories does not make the assertion ambiguous.
- Use `pathspec.gitignore.GitIgnoreSpec.from_lines`, the same matcher MkDocs' own
  `PathSpec` option uses (`config_options.py:1217-1224`), so the test cannot drift from MkDocs
  semantics. `pathspec` arrives transitively with MkDocs; declare it in
  `pip_requirements-dev.txt` since only tests import it (`tests/test_import_requirements.py`
  enforces declaration).
- Acceptance criteria: passes today; fails if a fragment directory is added without a matching
  `exclude_docs` entry.

### Work package: T9 -- built-artifact parity evidence

- Depends on: T6
- Touch points: `tests/e2e/e2e_include_parity.py` (new)
- This belongs in `tests/e2e/` per `docs/E2E_TESTS.md`: it runs real builds and needs `pandoc`,
  `weasyprint`, and `pdftotext`, so it stays out of the fast pytest lane. `tests/conftest.py:17`
  already excludes the subtree.
- Scope this to artifact behavior only: build the site and the downloads, then assert zero
  `--8<--` occurrences in `site/`, in the DOCX (via the existing `scan_docx_xml_text` path at
  `pipeline/build_syllabi.py:810`), and in `pdftotext` output. Then assert that **both authorized
  directory roles** actually reach the artifacts: a sentence unique to
  `fall_2026/shared/fragments/INSTRUCTOR_CONTACT_DETAILS.md` and a distinctive value from
  `generated/FALL_2026_IMPORTANT_DATES.md` each appear in all three outputs. Checking only the
  shared fragment would leave the `generated/` role -- an explicit design decision in T2 --
  unexercised, at negligible extra cost.
- The same-failure claim is **not** tested here. `main()` hardcodes
  `docs_root = repo_root / "site_docs"` (line 937), so pointing the three entry points at a
  fixture tree would mean widening a production API purely for a test. It is also unnecessary:
  after T3 and T5, all three outputs reach `expand_includes` as their only expander, so T7's unit
  assertions on that function *are* the same-failure proof, and T3/T5 prove the wiring. Fix the
  design rather than grow an injection seam to observe it.
- Acceptance criteria: `python3 tests/e2e/e2e_include_parity.py` exits zero. The absence of
  `pymdownx.snippets` is asserted separately and cheaply in the pytest lane (a config assertion
  that `mkdocs.yml`'s `markdown_extensions` declares no snippets extension), keeping this E2E test
  about artifacts rather than configuration lines.

## Implementation conventions

Stated affirmatively, per the positive-prompting rule in `docs/REPO_STYLE.md`:

- Indent with tabs; use ASCII only; separate functions with `#====` comment rules; write
  Google-style docstrings; annotate every parameter and return
  (`tests/test_function_typing.py`).
- Treat both new files as library modules: importable, with no shebang and no executable bit
  (`tests/test_shebangs.py`). `mkdocs_hooks.py` is invoked by MkDocs.
- Use module-form absolute imports (`import pathspec.gitignore`, then
  `pathspec.gitignore.GitIgnoreSpec`), per `tests/test_import_dot.py`.
- Let validation failures propagate directly as raised exceptions, and use explicit key access
  (`config["docs_dir"]`) so a malformed MkDocs config surfaces immediately.
- Annotate the MkDocs-fixed hook signature with `object` for `page` and `files`, keeping MkDocs
  internals out of the repo's type surface.

## Test and verification strategy

Split by the repo's own tiers (`docs/E2E_TESTS.md`), so the fast lane stays fast:

- **Permanent pytest** (`tests/test_markdown_includes.py`): the T7 grammar and authorization
  matrix, the T8 subset relation, and the T5 hook-loading contract. All operate on `tmp_path`
  fixtures, need no external tools, and run in milliseconds.
- **Permanent E2E** (`tests/e2e/e2e_include_parity.py`): artifact parity only -- the T9 greps and
  fragment-content checks against built `site/`, DOCX, and PDF. Slow, tool-dependent, run
  deliberately. It deliberately contains no same-failure check; see T9 for why that would require
  a production injection seam.
- **Close-out evidence, run once at implementation time**: `pytest tests/`,
  `python3 pipeline/build_site.py`, `python3 pipeline/build_syllabi.py`, plus the repo-wide gates
  `tests/test_source_file_line_limit.py`, `tests/test_pyflakes_code_lint.py`,
  `tests/test_function_typing.py`, `tests/test_indentation.py`,
  `tests/test_ascii_compliance.py`, `tests/test_import_dot.py`, `tests/test_shebangs.py`.

## Risk register

| Risk | Impact | Trigger | Owner | Mitigation |
| --- | --- | --- | --- | --- |
| MkDocs changes hook `sys.path` handling | Hook cannot import the engine; site build fails | MkDocs upgrade | implementer | T5's permanent loading test fails loudly at that upgrade, before any release |
| Hook imports the engine lazily inside the handler | Build fails at render time, after config validation passes | First `mkdocs build` after T5 | implementer | Module-level import; T5 asserts it, T9 greps built `site/` |
| Fragment rule and `exclude_docs` drift apart | An authorized fragment renders as its own page | New fragment directory added without a matching `exclude_docs` entry | implementer | T8 subset test. Note this guards one direction only; the converse (a page becoming includable) is prevented by `FRAGMENT_DIRECTORY_NAMES` in T2, not by T8 |
| Removing `pymdownx.snippets` breaks an unnoticed non-include use | Site render regression | `mkdocs build --strict` after T6 | implementer | Only eight `--8<--` sites exist repo-wide; re-run the grep immediately before the edit |
| `build_lib` unimportable under bare `pytest tests/` | Suite errors at collection | First run in a fresh shell | implementer | T4 conftest insert; acceptance criterion runs pytest without sourcing `source_me.sh` |

## Documentation close-out requirements

- `docs/CHANGELOG.md` entry under today's date with the canonical subsection headings, covering
  the new engine, the retired snippets grammar, the explicit fragment rule and its subset test,
  and the parity evidence. Record two decisions for later readers: the 997-line cap as the forcing
  reason for extraction, and the rejection of the `exclude_docs`-equivalence design in favor of an
  explicit rule plus a subset test.
- `docs/CODE_ARCHITECTURE.md`: the single include engine and its two entry points.
- `docs/FILE_STRUCTURE.md`: add `pipeline/build_lib/` and state the boundary -- `pipeline/` holds
  entry points, `build_lib/` holds importable library units.
- `docs/FILE_FORMATS.md`: the include grammar and the fragment-directory rule, from the
  User-facing contract section above.

## Resolved decisions

- **Authorization is explicit, not derived.** `exclude_docs` is not the authorization boundary;
  the engine owns `FRAGMENT_DIRECTORY_NAMES` and T8 enforces the subset relation.
- **`generated/` is an inclusion-role directory** and is authorized whole. Revisit only if
  non-fragment artifacts start living there.
- **The same-failure claim is proven at the convergence point**, `expand_includes`, not by driving
  three entry points against a fixture tree that would require new production configuration.
- **Include paths resolve against `docs_root`**, never against the including document.
- **Orphan-fragment completeness testing is out of scope.** Useful, independent of this work.
- **Further decomposition of `pipeline/build_syllabi.py` is out of scope.** The file will drift
  back toward the 999-line cap; that is a follow-on plan, and `build_lib/` now exists to receive
  it.
- **No extra fragments-are-not-pages assertion in the hook.** T8 already covers it from the
  authoritative side.
