# Usage

Maintain the public Fall 2026 syllabus sources, then rebuild the student website and complete
documents. Students only use the published site; these commands are for maintainers.

## Source ownership

- `site_docs/fall_2026/` is the only live course and complete-syllabus authority.
- Each course contains `index.md`, course-specific Markdown, `syllabus.yml`, and `.meta.yml`.
- Term-wide policies, dates, instructor information, and student resources live under
  `site_docs/fall_2026/shared/` and are linked or included rather than copied.
- [site_docs/EXTRA_CREDIT_MOVIES.md](../site_docs/EXTRA_CREDIT_MOVIES.md) is the one global,
  website-only exception. It is deliberately omitted from complete PDF and DOCX manifests.
- `site_docs/downloads/`, `site/`, and `output/` are generated outputs. Regenerate them; do not
  edit or commit them as content sources.

The ignored local `raw/` tree may hold public reference material. It is never a live authority;
the build rejects tracked files inside it. Keep private syllabi, credentials, meeting links,
student information, and access-controlled material in Blackboard.

See [FILE_FORMATS.md](FILE_FORMATS.md) for manifest, Markdown table, and restricted include rules.

## Edit content

- Edit course-specific details, assignments, and schedules in that course folder.
- Edit one shared policy in `site_docs/fall_2026/shared/policies/`; do not copy it into courses.
- Edit shared instructor contact facts in
  `site_docs/fall_2026/shared/fragments/INSTRUCTOR_CONTACT_DETAILS.md`.
- Edit shared support information in `site_docs/fall_2026/shared/STUDENT_RESOURCES.md`.
- Edit dates as literal Markdown in course details and schedules. Confirm calendar changes before
  publishing; the build never shifts dates automatically.
- Select `assignments`, `group_quizzes`, `f2f_exams`, and `online_exams` in each course manifest's
  ordered `assessments` list. Edit their shared wording under `shared/fragments/assessments/`.
- Set `assessment_examples_url` to the matching official `https://biologyproblems.org/<subject>/`
  route. The coursework page publishes that practice-problem link before its assessment types.
- Set `discussion` to `no_discussion`, `f2f_discussion`, or `remote_discussion`. Edit mode-specific
  and shared discussion wording under `shared/fragments/discussions/`.

Use the exact, full-line include form when a public fact must appear in more than one place:

```markdown
--8<-- "fall_2026/shared/fragments/INSTRUCTOR_CONTACT_DETAILS.md"
```

## Build and preview

Build complete DOCX and PDF downloads plus the strict static website:

```bash
source source_me.sh
python3 pipeline/build_site.py
```

The build refreshes the managed important-dates fragment from its fixed Google Sheets source,
regenerates all downloads, and fails rather than publishing stale date data.

Preview the generated site locally:

```bash
./run_web_server.sh
```

The preview refreshes important dates, opens in the default browser, and stops after five minutes.
Press `Ctrl-C` to stop it sooner.

Build only DOCX and PDF files when the site itself is unchanged:

```bash
source source_me.sh
python3 pipeline/build_syllabi.py
```

Use `--archive` with that command to package current generated documents under `output/archive/`.

## Build department checklists

Generate one evidence-linked Markdown and DOCX checklist for each Fall 2026 course:

```bash
source source_me.sh
python3 pipeline/build_department_checklists.py
```

The files are written under `output/department_checklists/`. Each checklist follows the university
rubric, links to the published evidence, and keeps unresolved questions visibly unchecked. Edit the
tracked [pipeline/department_checklists.yml](../pipeline/department_checklists.yml) evidence and
course overrides, then regenerate; do not edit the output files.

## Validate

Check public external HTTP(S) links as an explicit live maintainer task:

```bash
source source_me.sh
python3 pipeline/check_links.py
```

The checker reports source locations and follows redirects. It remains outside pytest because it
uses the network; pass Markdown files or directories to check separately held public references.

Run all local validation lanes before publishing a significant change:

```bash
./all_test.sh
```

The runner executes fast offline pytest, export and include-parity E2E checks, a strict production
build, and Playwright. For focused work, run `source source_me.sh && python3 -m pytest tests/`,
`source source_me.sh && python3 tests/e2e/e2e_include_parity.py`, or
`./run_playwright_tests.sh --build`.

## Term lifecycle

The Spring 2027 rollover must define the archival source location, generated boundary, and pipeline
behavior before another term tree is added. Until then, do not create future-term or archive source
trees.

## Known gaps

- TODO: Define and document the Spring 2027 archival and rollover workflow before creating its
  source tree.
