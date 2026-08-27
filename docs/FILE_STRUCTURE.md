# File structure

## Repository map

```text
.
|-- .github/workflows/       GitHub Pages build and deployment
|-- devel/                   Maintainer setup, version, and changelog tools
|-- docs/                    Repository documentation and working records
|-- overrides/               Material theme template overrides
|-- pipeline/                Date synchronization and syllabus renderers
|-- site_docs/               Public website and syllabus source authority
|-- tests/                   Fast, export E2E, and browser validation
|-- all_test.sh              Complete local validation front door
|-- mkdocs.yml               Site, navigation, theme, and Markdown configuration
|-- package.json             Playwright audit dependencies and command
|-- pip_requirements*.txt    Python runtime and development dependencies
|-- Brewfile                 macOS document-rendering tools
|-- run_web_server.sh        Local production-shaped preview
`-- run_playwright_tests.sh  Browser audit front door
```

## Public source tree

```text
site_docs/
|-- index.md                         Student homepage
|-- assets/
|   |-- fonts/                       Self-hosted text/icon fonts and licenses
|   |-- images/favicon.svg           Protein-themed site icon
|   |-- javascripts/accessibility.js Accessible table behavior
|   `-- stylesheets/                 Website and PDF presentation
|-- fall_2026/
|   |-- index.md                     Active-term overview
|   |-- biostats/                    BIOL 318/418 sources
|   |-- genetics/                    BIOL 351/451 sources
|   |-- biotech/                     BIOL 480 sources
|   `-- shared/
|       |-- IMPORTANT_DATES.md       Public wrapper for synchronized dates
|       |-- INSTRUCTOR_INFORMATION.md
|       |-- STUDENT_RESOURCES.md
|       |-- fragments/               Include-only edit-once content
|       `-- policies/                Canonical Dr. Voss policy topics
|-- generated/                       Ignored synchronized fragments
`-- downloads/                       Ignored generated PDF and DOCX files
```

Each course directory contains an `index.md`, `COURSE_DETAILS.md`,
`COURSE_LEARNING_FRAMEWORK.md`, `ASSIGNMENTS_AND_GRADING.md`, `SCHEDULE.md`, a
`syllabus.yml` manifest, and `.meta.yml` website/PDF course-theme metadata.

## Pipeline files

```text
pipeline/
|-- build_site.py                       Production build front door
|-- build_syllabi.py                    Complete DOCX and PDF entry point
|-- mkdocs_hooks.py                     Website metadata/include adapter loaded by MkDocs
|-- sync_important_dates.py             Google Sheets fragment importer
|-- create_syllabus_reference_docx.py   Intentional DOCX style-asset generator
|-- syllabus_reference.docx             Tracked Pandoc reference document
`-- build_lib/
    |-- markdown_includes.py             Shared include grammar and expansion engine
    |-- syllabus_content.py              Source validation and Markdown composition
    |-- syllabus_model.py                Manifest model, loading, and path validation
    `-- syllabus_rendering.py            DOCX/PDF rendering, checks, and publication
```

[pipeline/](../pipeline/) holds runnable or externally loaded entry points.
[pipeline/build_lib/](../pipeline/build_lib/) holds importable library units used by those entry
points; it is found by placing `pipeline/` itself on the Python import path rather than treating
`pipeline/` as a package. Entry points coordinate those units instead of retaining substantial
composition, validation, or rendering implementations.

## Test layout

- `tests/test_*.py` contains the fast pytest lane.
- [tests/e2e/e2e_syllabus_export.sh](../tests/e2e/e2e_syllabus_export.sh) runs the
  production-oriented export gate.
- [tests/e2e/e2e_include_parity.py](../tests/e2e/e2e_include_parity.py) runs that export gate and
  checks include content in the built website, DOCX, and PDF artifact corpora.
- `tests/playwright/syllabus_smoke.mjs` audits the built site in Chromium.
- `tests/playwright/helper_server.mjs` serves the local static build over HTTP.
- `tests/playwright/capture_readme_screenshots.mjs` captures documentation images from the built
  site.

## Documentation layout

Durable reference documents use uppercase names directly under `docs/`. Active plans, audits,
reports, decisions, and workstreams use snake case under `docs/active_plans/`. Completed planning
artifacts move to `docs/archive/`.

The active documentation entry points are:

- [INSTALL.md](INSTALL.md) for clean-machine setup.
- [USAGE.md](USAGE.md) for authoring, building, and validation.
- [CODE_ARCHITECTURE.md](CODE_ARCHITECTURE.md) for component and data flow.
- [FILE_FORMATS.md](FILE_FORMATS.md) for manifest and source contracts.
- [GITHUB_PAGES_BUILD.md](GITHUB_PAGES_BUILD.md) for publication architecture.

## Generated boundaries

The following paths are outputs, not editable sources:

- `site/` - complete MkDocs output uploaded to GitHub Pages.
- `site_docs/downloads/` - generated student PDF and DOCX files.
- `site_docs/generated/` - synchronized important-dates Markdown.
- `output/` - optional local archives and other generated output.
