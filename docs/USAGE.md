# Usage

Maintain public Fall 2026 syllabus sources, then regenerate the student website and complete PDF
and DOCX documents. Students use the published site; these commands are for maintainers.

## Source ownership

- `site_docs/fall_2026/` is the only live course and complete-syllabus authority.
- The document builder selects this tree directly rather than searching for other syllabus copies.
- Each course owns its Markdown pages, `syllabus.yml`, and `.meta.yml`.
- Shared policies, dates, instructor information, and student resources live in
  `site_docs/fall_2026/shared/` and are linked or included rather than copied.
- [site_docs/EXTRA_CREDIT_MOVIES.md](../site_docs/EXTRA_CREDIT_MOVIES.md) is the one global,
  website-only exception. It is deliberately omitted from complete PDF and DOCX manifests.
- `site/`, `site_docs/downloads/`, `site_docs/generated/`, `department_checklists/`, and `output/`
  are generated outputs. Regenerate them; do not edit them as content sources.

See [FILE_FORMATS.md](FILE_FORMATS.md) for manifest, Markdown table, and restricted include rules.

## Edit content

- Edit course-specific details, assignments, and schedules in that course's folder.
- Edit a shared policy once under `shared/policies/`; do not copy it into course folders.
- Edit shared instructor facts in `shared/fragments/INSTRUCTOR_CONTACT_DETAILS.md`. Edit the
  student-services route list in `shared/STUDENT_RESOURCES.md` and service details in the matching
  `shared/student_services/` topic page.
- Edit dates as literal Markdown in course schedules and details; confirm calendar changes before
  publishing because the build never shifts them automatically.
- Edit assessment choices, discussion mode, lab status, and confirmed point-plan names and values
  in the course `syllabus.yml`. The build derives point totals, approximate shares, applicable
  interruption guidance, and notices when the course has no quizzes or exams.

## Build and preview

Run the production front door to refresh important dates, generate complete downloads, and build
the strict static site:

```bash
source source_me.sh
python3 pipeline/build_site.py
```

Preview the current source locally. The script refreshes important dates, opens MkDocs in the
default browser, and stops after five minutes; use `Ctrl-C` to stop it earlier.

```bash
./run_web_server.sh
```

To rebuild only the current PDF and DOCX outputs after dates have already been refreshed, run:

```bash
source source_me.sh
python3 pipeline/build_syllabi.py
```

Add `--archive` to also create one ZIP file per term under `output/archive/`.

## Review tables and checklists

Inspect the shared table-width calculation without writing outputs:

```bash
source source_me.sh
python3 tools/calculate_table_widths.py
```

Pass Markdown files or directories to narrow the report, or add `--json` for machine-readable
output. Capture every rendered table after a production build with:

```bash
./capture_table_review.sh
```

Open `output/table_review/index.html` for desktop/mobile, light/dark screenshots and calculated
width evidence.

Generate department-review checklists from the tracked rubric source:

```bash
source source_me.sh
python3 pipeline/build_department_checklists.py
```

The generated Markdown, DOCX, and tagged PDF files belong under
repository-root `department_checklists/`. The command first rebuilds the complete syllabus PDFs,
then uses their named destinations to print references such as
`Syllabus p. 8 - Coursework and grades` in the separate checklist files. Checklist PDFs embed
Atkinson Hyperlegible Next; DOCX files use the Arial-based syllabus reference document and do not
embed fonts. No web link is required. Edit `pipeline/department_checklists.yml`, not the generated
outputs.

## Validate

Run all local validation lanes before publishing a significant change:

```bash
./all_test.sh
```
It runs fast offline pytest, export and include-parity E2E checks, a strict production build, and
Playwright. For focused diagnosis, use one of these commands:

```bash
source source_me.sh && python3 -m pytest tests/
source source_me.sh && python3 tests/e2e/e2e_include_parity.py
./run_playwright_tests.sh --build
```

Check public external links as a separate live maintainer task:

```bash
source source_me.sh
python3 pipeline/check_links.py
```

It defaults to `site_docs/`; pass Markdown paths or directories to narrow its scope. Use
`--timeout` and `--workers` only when the checked network workload needs adjustment.

## Term lifecycle

The Spring 2027 rollover must define the archival source location, generated boundary, and pipeline
behavior before another term tree is added. Until then, do not create future-term or archive source
trees.

## Known gaps

- TODO: Define and document the Spring 2027 archival and rollover workflow before creating its
  source tree.
