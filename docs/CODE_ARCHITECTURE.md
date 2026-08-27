# Code architecture

## System purpose

This repository publishes one active set of public course sources in three student-facing forms:
a navigable website, a complete PDF syllabus, and a complete DOCX syllabus. The architecture keeps
the active Markdown authoritative and treats every rendered artifact as generated output.

## System overview

```text
Google Sheets                    tracked site_docs/
important dates                      |             |
      |                              |             | syllabus.yml manifests
      v                              |             v
sync_important_dates.py              |      build_syllabi.py
      |                              |          |          |
      | generated date fragment -----+          v          v
      |                              |       Pandoc   Python-Markdown
      |                              |          |          |
      |                              |          v          v
      |                              |         DOCX    HTML + WeasyPrint
      |                              |                     |
      |                              |                     v
      |                              |                    PDF
      |                              |                     |
      |                              |                     v
      |                              |             site_docs/downloads/
      v                              v                     |
     tracked dates wrapper ------> MkDocs Material <-------+
                                         |
                                         v
                                       site/
                                         |
                                         v
                                     GitHub Pages
```

## Source authority

The live course-content authority is `site_docs/fall_2026/`. Course directories contain
course-specific pages and one `syllabus.yml` manifest. Shared course information lives under
`shared/`, with directly navigable pages separated from include-only fragments. The niche,
term-independent approved-science-movies catalog lives at
[site_docs/EXTRA_CREDIT_MOVIES.md](../site_docs/EXTRA_CREDIT_MOVIES.md) as a global website-only
reference and is not listed in course manifests.

The active term is intentionally singular. `templates/`, future-term copies, and historical-term
copies cannot become parallel content authorities during Fall 2026. Generated directories are
ignored and must be rebuilt from the tracked source.

## Build pipeline

`pipeline/build_site.py` is the production front door. It runs three fail-fast stages:

1. `pipeline/sync_important_dates.py` downloads and validates the fixed Google Sheets CSV source,
   then atomically replaces the generated important-dates fragment consumed by the tracked dates
   wrapper on the website and in every complete syllabus.
2. `pipeline/build_syllabi.py` coordinates manifest discovery, staged builds, publication, and
   optional archives through the importable units under `pipeline/build_lib/`.
3. MkDocs builds `site/` in strict mode using `mkdocs.yml`.

The document builder stages all generated downloads in a temporary directory. It validates the
complete expected set before replacing the current files under `site_docs/downloads/`, so a failed
course build cannot publish a partial set.

### Complete-document internals

The runnable `pipeline/build_syllabi.py` file owns orchestration and CLI flow. Three library units
own the implementation:

- [pipeline/build_lib/syllabus_model.py](../pipeline/build_lib/syllabus_model.py) loads manifest
  structure, validates shared course-theme metadata and source containment, and defines the
  immutable manifest model.
- [pipeline/build_lib/syllabus_content.py](../pipeline/build_lib/syllabus_content.py) scans public
  sources, validates learning content and Markdown, expands includes, and composes complete-document
  Markdown.
- [pipeline/build_lib/syllabus_rendering.py](../pipeline/build_lib/syllabus_rendering.py) renders,
  verifies, stages, and publishes DOCX and PDF artifacts.

## Rendering branches

### Website branch

MkDocs reads `site_docs/`, calls
[pipeline/mkdocs_hooks.py](../pipeline/mkdocs_hooks.py) to validate and normalize inherited course
colors and expand authorized fragments, applies the Material theme, repository overrides, custom
CSS and JavaScript, and copies downloads and assets into `site/`. `mkdocs.yml` owns navigation,
hook registration, theme configuration, social links, and the public site URL.

### DOCX branch

The content library calls the shared include engine, rewrites links between included pages as
document anchors, removes web-only controls, and the rendering library sends portable Markdown to
Pandoc. The tracked
`pipeline/syllabus_reference.docx` owns Word styles. Python post-processing adds metadata,
language, and semantic table properties before output verification.

### PDF branch

The same composed Markdown is rendered to semantic HTML with the Markdown extension stack loaded
from `mkdocs.yml`. The validated adjacent `.meta.yml` course accent is attached to the standalone
HTML as a CSS custom property so the website and PDF share one color authority. WeasyPrint applies
`site_docs/assets/stylesheets/syllabus_pdf.css` and creates a tagged PDF. Poppler verifies document
metadata, text, tables, and required section titles.

## Shared includes

[pipeline/build_lib/markdown_includes.py](../pipeline/build_lib/markdown_includes.py) is the only
include grammar and expansion engine. The complete-document content library calls it before the
DOCX/PDF rendering split, and the website reaches it through
[pipeline/mkdocs_hooks.py](../pipeline/mkdocs_hooks.py). The hook imports its shared build libraries
while MkDocs temporarily exposes `pipeline/` during hook loading, so page rendering does not depend
on a lasting path mutation.

The engine accepts one full-line, double-quoted `--8<--` form with paths resolved from `site_docs/`.
Targets must be local, non-empty `.md` files under a directory named `fragments` or `generated`.
Traversal, remote paths, symlink escapes, nested includes, and every unsupported marker form fail
before rendering. Relative Markdown and HTML links inside a fragment are rebased from that
fragment's directory to the receiving page while remaining contained by `site_docs/`; this lets the
main page and term overview consume one canonical course-and-download block. `exclude_docs` remains
a navigation rule; tests require every authorized Markdown fragment to be excluded without treating
every exclusion as authorization.

## Validation boundaries

- `source source_me.sh && python3 -m pytest tests/` is the fast repository lane.
- `source source_me.sh && python3 tests/e2e/e2e_include_parity.py` exercises the production export
  boundary, stale-output cleanup, credential checks, strict site build, and include parity across
  the website, DOCX, and PDF corpora.
- `./run_playwright_tests.sh --build` serves the production-shaped `site/` tree and checks real
  routes, downloads, accessibility, responsive behavior, theme state, and navigation.
- `.github/workflows/deploy-pages.yml` runs the production builder and deploys only after the Pages
  artifact uploads successfully.

The browser audit is a local maintainer signal. Publication requires a complete buildable artifact;
the detailed separation is documented in
[GITHUB_PAGES_BUILD.md](GITHUB_PAGES_BUILD.md).

## Privacy boundary

Only public-safe content belongs in the repository. The document builder scans source and generated
text for common meeting URLs, passwords, passcodes, and invitation patterns. Private links,
student information, assignments, grades, and access-controlled materials remain in Blackboard.

The ignored local `raw/` directory may hold public reference material that supports authoring. It
is outside the content pipeline, never supplies a published page or complete-syllabus section, and
the builder rejects any tracked file below it. Move a verified public fact into the canonical
Markdown source rather than linking a course page or manifest to `raw/`.

## Extension points

- Add or revise student-facing course and shared content in
  [site_docs/fall_2026/](../site_docs/fall_2026/); keep the website-only movie catalog in
  [site_docs/EXTRA_CREDIT_MOVIES.md](../site_docs/EXTRA_CREDIT_MOVIES.md).
- Add a complete-syllabus section by updating the owning course `syllabus.yml` manifest and the
  public Markdown source it names. The manifest contract is documented in
  [FILE_FORMATS.md](FILE_FORMATS.md).
- Put reusable manifest, content, include, or renderer behavior in
  [pipeline/build_lib/](../pipeline/build_lib/). Keep runnable entry points in
  [pipeline/](../pipeline/) as small coordinators.
- Use [pipeline/check_links.py](../pipeline/check_links.py) for an on-demand live audit of every
  external URL in `site_docs/`. It is a maintainer command, not a fast pytest dependency.
- Add deterministic unit and integration checks under [tests/](../tests/); place production
  builds in [tests/e2e/](../tests/e2e/) and browser checks in
  [tests/playwright/](../tests/playwright/).

## Known gaps

- Define and validate the historical-term snapshot, generated-output, and navigation design before
  creating the Spring 2027 source tree.
