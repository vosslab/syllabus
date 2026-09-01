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
|-- tools/                   Optional repository-analysis utilities
|-- all_test.sh              Complete local validation front door
|-- capture_table_review.sh  Build and capture every rendered Markdown table
|-- mkdocs.yml               Site, navigation, theme, and Markdown configuration
|-- package.json             Playwright audit dependencies and command
|-- pip_requirements*.txt    Python runtime and development dependencies
|-- Brewfile                 macOS document-rendering tools
|-- run_web_server.sh        Local production-shaped preview
|-- source_me.sh             Python 3.12 environment bootstrap
`-- run_playwright_tests.sh  Browser audit front door
```

## Public source tree

```text
site_docs/
|-- index.md                         Student homepage
|-- EXTRA_CREDIT_MOVIES.md           Global website-only approved movie catalog
|-- assets/
|   |-- fonts/                       Self-hosted text/icon fonts and licenses
|   |-- images/                      Protein logo and light/dark instructor portraits
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
|       |-- STUDENT_RESOURCES.md     Student-services overview
|       |-- student_services/        Task-focused student-service topics
|       |-- fragments/               Edit-once term, contact, assessment, discussion, and lab content
|       `-- policies/                Canonical Dr. Voss policy topics
|-- generated/                       Ignored synchronized fragments
`-- downloads/                       Ignored generated PDF and DOCX files
```

Each course directory contains an `index.md`, `COURSE_DETAILS.md`,
`COURSE_LEARNING_FRAMEWORK.md`, `ASSIGNMENTS_AND_GRADING.md`, `SCHEDULE.md`, a `syllabus.yml`
manifest, and `.meta.yml` website/PDF course-theme metadata. Courses that award discussion marks
also contain `DISCUSSION_MARKS.md`. Biotechnology additionally has
[site_docs/fall_2026/biotech/PROJECTS.md](../site_docs/fall_2026/biotech/PROJECTS.md) and
[site_docs/fall_2026/biotech/TALKING_POINTS.md](../site_docs/fall_2026/biotech/TALKING_POINTS.md)
for its course-specific project and presentation expectations.
The shared `INSTRUCTOR_INFORMATION.md` is linked from every course landing page and listed once in
each course manifest; instructor facts remain in its include-only fragments rather than in course
directories.

## Pipeline files

```text
pipeline/
|-- department_checklist_pdf.css        Print layout for generated rubric checklists
|-- build_department_checklists.py      Page-referenced department checklist generator
|-- build_site.py                       Production build front door
|-- build_syllabi.py                    Complete DOCX and PDF entry point
|-- check_links.py                      Live external-link audit with source locations
|-- mkdocs_hooks.py                     Website metadata/include adapter loaded by MkDocs
|-- sync_important_dates.py             Google Sheets fragment importer
|-- create_syllabus_reference_docx.py   Intentional DOCX style-asset generator
|-- syllabus_reference.docx             Tracked Pandoc reference document
|-- department_checklists.yml           Rubric evidence and course-specific doubts
|-- pandoc_filters/
|   |-- docx_image_layout.lua            Portable image metadata to native DOCX sizing
|   `-- docx_line_breaks.lua             Documented HTML breaks to native DOCX breaks
`-- build_lib/
    |-- markdown_includes.py             Shared include grammar and expansion engine
    |-- syllabus_content.py              Source validation and Markdown composition
    |-- syllabus_model.py                Manifest model, loading, and path validation
    |-- syllabus_rendering.py            DOCX/PDF rendering, checks, and publication
    `-- table_layouts.py                  Content-derived cross-format table sizing
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
- `tests/playwright/capture_table_review.mjs` captures every built table and records its calculated
  and rendered widths under ignored `output/table_review/`.
- `tools/calculate_table_widths.py` reports the shared width calculation directly from selected
  Markdown files or directories.

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
- [BIOLOGY_MAJOR_COMPETENCIES.md](BIOLOGY_MAJOR_COMPETENCIES.md) for the six undergraduate Biology
  competency areas and the maintained Fall 2026 course mappings.
- [CSHP_LEADERSHIP_REFERENCE.md](CSHP_LEADERSHIP_REFERENCE.md) for the public-safe college
  leadership, advisor, and laboratory-contact roster used during syllabus review.
- [DBPS_FALL_2026_REFERENCE.md](DBPS_FALL_2026_REFERENCE.md) for the public-safe department chair
  update, contacts, Fall 2026 dates, and faculty procedures.

## Generated boundaries

The following paths are outputs, not editable sources:

- `site/` - complete MkDocs output uploaded to GitHub Pages.
- `site_docs/downloads/` - generated student PDF and DOCX files.
- `site_docs/generated/` - synchronized important-dates Markdown.
- `output/` - optional local archives and other generated output.

The ignored top-level `raw/` directory is not a generated artifact or a source subtree. It may
hold local public or private internal reference material, but no tracked file may live there and it
is never read by the publication pipeline. Copy confirmed public facts into the tracked
`site_docs/` authority.
