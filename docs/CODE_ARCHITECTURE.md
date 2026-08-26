# Code architecture

## System purpose

This repository publishes one active set of public course sources in three student-facing forms:
a navigable website, a complete PDF syllabus, and a complete DOCX syllabus. The architecture keeps
the active Markdown authoritative and treats every rendered artifact as generated output.

## System overview

```text
Google Sheets                       tracked site_docs/
important dates                         |             |
      |                                 |             | syllabus.yml manifests
      v                                 |             v
sync_important_dates.py                 |      build_syllabi.py
      |                                 |          |          |
      | generated date fragment         |          v          v
      +----------------------------+    |       Pandoc   Python-Markdown
                                   |    |          |          |
                                   |    |          v          v
                                   |    |         DOCX    HTML + WeasyPrint
                                   |    |                     |
                                   |    |                     v
                                   |    |                    PDF
                                   |    |                     |
                                   |    |                     v
                                   |    |             site_docs/downloads/
                                   v    v                     |
                                  MkDocs Material <-----------+
                                         |
                                         v
                                       site/
                                         |
                                         v
                                     GitHub Pages
```

## Source authority

The live content authority is `site_docs/fall_2026/`. Course directories contain course-specific
pages and one `syllabus.yml` manifest. Shared information lives under `shared/`, with directly
navigable pages separated from include-only fragments.

The active term is intentionally singular. `templates/`, future-term copies, and historical-term
copies cannot become parallel content authorities during Fall 2026. Generated directories are
ignored and must be rebuilt from the tracked source.

## Build pipeline

`pipeline/build_site.py` is the production front door. It runs three fail-fast stages:

1. `pipeline/sync_important_dates.py` downloads and validates the fixed Google Sheets CSV source,
   then atomically replaces the website's generated important-dates fragment.
2. `pipeline/build_syllabi.py` loads every manifest, validates public content, composes course and
   shared sources, and publishes a complete PDF/DOCX pair per course.
3. MkDocs builds `site/` in strict mode using `mkdocs.yml`.

The document builder stages all generated downloads in a temporary directory. It validates the
complete expected set before replacing the current files under `site_docs/downloads/`, so a failed
course build cannot publish a partial set.

## Rendering branches

### Website branch

MkDocs reads `site_docs/`, applies the Material theme, repository overrides, custom CSS and
JavaScript, and copies downloads and assets into `site/`. `mkdocs.yml` owns navigation, theme
configuration, the restricted Markdown include settings, social links, and the public site URL.

### DOCX branch

The document builder expands approved Markdown fragments, rewrites links between included pages as
document anchors, removes web-only controls, and sends portable Markdown to Pandoc. The tracked
`pipeline/syllabus_reference.docx` owns Word styles. Python post-processing adds metadata,
language, and semantic table properties before output verification.

### PDF branch

The same composed Markdown is rendered to semantic HTML with the Markdown extension stack loaded
from `mkdocs.yml`. WeasyPrint applies
`site_docs/assets/stylesheets/syllabus_pdf.css` and creates a tagged PDF. Poppler verifies document
metadata, text, tables, and required section titles.

## Shared includes

The website uses `pymdownx.snippets` with `site_docs/` as its restricted base path. The document
builder implements the same one-level include notation for its non-MkDocs branches. It accepts only
local `.md` paths below `site_docs/`, rejects traversal and remote URLs, and disallows nested or
empty fragments. This narrow contract preserves edit-once content without introducing a general
template engine.

## Validation boundaries

- `source source_me.sh && python3 -m pytest tests/` is the fast repository lane.
- `bash tests/e2e/e2e_syllabus_export.sh` exercises the production export boundary, stale-output
  cleanup, credential checks, and rendered artifact checks.
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
