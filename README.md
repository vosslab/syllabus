# Syllabus

An accessibility-focused publishing system that turns separately maintained course pages,
policies, and resources into a navigable student website plus complete PDF and DOCX syllabi for
departmental archives.

## One source, three student-ready forms

Students should not need to navigate a 30-page document to find one deadline or policy. This
project keeps web pages short and task-oriented while preserving a complete downloadable syllabus.
Shared policy topics and resources stay independently editable and are assembled once during each
build. Repeated context such as office hours is embedded from one canonical Markdown fragment.

```text
course Markdown + shared policies + student resources
  |-- MkDocs Material --------------------> navigable static website
  |-- Pandoc + reference document --------> complete DOCX
  `-- Python-Markdown + WeasyPrint -------> complete tagged PDF
```

- Course schedules, grading, learning frameworks, and policies remain ordinary Markdown.
- Course-specific header colors provide a restrained web identity; downloads remain neutral.
- Atkinson Hyperlegible Next is self-hosted for predictable, readable website typography.
- Credential scanning rejects common meeting links, passcodes, and private invitations.
- Every successful build produces complete student-facing candidates without draft-state banners.

<!-- screenshots:begin (managed by screenshot-docs) -->
<!-- screenshots:end -->

## Quick start

The primary local workflow uses macOS, Homebrew, and Python 3.12. Install the document tools and
Python dependencies, then build all downloads and the strict static site:

```bash
brew bundle
source source_me.sh
python3 -m pip install -r pip_requirements.txt -r pip_requirements-dev.txt
python3 pipeline/build_site.py
```

A successful build creates `site/index.html` and complete course documents under the ignored
`site_docs/downloads/` directory. Preview the result in a temporary local server:

```bash
./run_web_server.sh
```

The preview opens in the default browser and stops after five minutes. See
[docs/INSTALL.md](docs/INSTALL.md) for system dependencies, optional browser-audit setup, and the
document-rendering stack.

## Authoring a course

Public content is organized by term. Each course owns its short student pages and a manifest that
defines the complete-document order; term-level policies and resources remain shared:

```text
site_docs/fall_2026/
|-- POLICIES.md
|-- STUDENT_RESOURCES.md
|-- policies/
|   |-- ASSESSMENT.md
|   |-- GRADING.md
|   `-- ...
|-- shared/
|   |-- INSTRUCTOR_INFORMATION.md
|   |-- LETTER_GRADE_SCALE.md
|   `-- ROOSEVELT_LEARNING_GOALS.md
`-- biol_318_418/
    |-- index.md
    |-- COURSE_DETAILS.md
    |-- COURSE_LEARNING_FRAMEWORK.md
    |-- ASSIGNMENTS_AND_GRADING.md
    |-- SCHEDULE.md
    `-- syllabus.yml
```

Copy `templates/course/` when starting a course, replace every placeholder, and add the new pages
to `mkdocs.yml`. Dates remain literal Markdown so calendar exceptions are explicit rather than
hidden behind automatic shifting. See [docs/USAGE.md](docs/USAGE.md) for the complete authoring,
export, archival, and validation workflow.

## Verification

The production-oriented E2E command builds every DOCX/PDF pair, removes stale generated downloads,
scans public output for credentials, and performs a strict MkDocs build:

```bash
bash tests/e2e/e2e_syllabus_export.sh
```

Fast repository tests and the optional browser accessibility audit run separately:

```bash
source source_me.sh
python3 -m pytest tests/
./run_playwright_tests.sh
```

Accessibility findings guide improvement but do not claim legal or PDF/UA compliance.

## Documentation

- [docs/INSTALL.md](docs/INSTALL.md) - system tools, Python dependencies, fonts, and audit setup.
- [docs/USAGE.md](docs/USAGE.md) - course authoring, builds, archives, and validation.
- [docs/HCI_BRIEF.md](docs/HCI_BRIEF.md) - student navigation and accessibility design rationale.
- [docs/active_plans/reports/fall_2026_content_review.md](docs/active_plans/reports/fall_2026_content_review.md)
  - non-blocking editorial refinement checklist.
- [docs/CHANGELOG.md](docs/CHANGELOG.md) - implementation decisions, failures, and verification
  evidence.

## License

Course materials are available under the
[Creative Commons Attribution 4.0 International license](LICENSE.CC-BY-4.0.md).
