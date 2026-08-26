# Usage

## Content organization

Public course content lives under `site_docs/<term>/<course>/`. Each course contains:

Course directories use subject-based slugs so cross-listed students do not see another section's
number as the path: `biostats` for BIOL 318/418, `genetics` for BIOL 351/451, and `biotech` for
BIOL 480. Official course numbers remain in headings, section tables, metadata, and download names.

- `index.md` for the short overview, task links, course summary, and secondary download links.
- `COURSE_DETAILS.md` for registration, meeting, catalog, and embedded shared instructor
  information.
- `COURSE_LEARNING_FRAMEWORK.md` for Roosevelt learning goals, learning objectives, course
  learning outcomes, and overall learning goals. Its student-facing title is **Learning
  Objectives, Outcomes, and Goals**.
- `ASSIGNMENTS_AND_GRADING.md` for course-specific graded work and grade calculations.
- `SCHEDULE.md` for literal meeting dates and topics.
- `syllabus.yml` for complete-document order and metadata.

See [FILE_FORMATS.md](FILE_FORMATS.md) for the exact manifest, Markdown, include, and generated
document contracts.

Each term keeps its public term-wide pages under `shared/`: important dates, instructor
information, policies, and student resources. The short policy topic index and the canonical
policy categories live together under `shared/policies/`. Every course links to those shared
branches. Its manifest adds the policy overview as a section heading, then appends each policy
topic and the student-resource source once to the complete syllabus. The overview's web-only topic
links are omitted from document exports.

Include-only Markdown under `shared/fragments/` holds facts that students need in more than one
context but the instructor should edit once. The current fragments provide instructor contact
details, including office hours, and Roosevelt learning-goal bullets. Course pages embed them with
the restricted syntax:

```markdown
--8<-- "fall_2026/shared/fragments/INSTRUCTOR_CONTACT_DETAILS.md"
```

Includes use one full-line, double-quoted form and resolve from `site_docs/`. Targets must be
non-empty `.md` files under a directory named `fragments` or `generated`; absolute paths, parent
traversal, remote URLs, symlink escapes, nested includes, and alternate forms are rejected. The
repository-owned engine expands the same source for the website, DOCX, and PDF branches. Files in
either authorized role are excluded from direct website routes. The public
`shared/INSTRUCTOR_INFORMATION.md` page supplies its page heading and embeds the contact-details
fragment; course details embed that same fragment under their own heading. Only public-safe
canonical content belongs in this repository. Do not create an ignored `raw/` tree for private
syllabi, credentials, meeting links, student information, or access-controlled material; transfer
only public facts into the tracked Markdown sources.

## Source and generated boundary

- Edit syllabus content only under the active `site_docs/<term>/` tree.
- Keep course-specific facts in their course folder and each shared fact or policy in one canonical
  term-level file. Link or embed that source wherever students need it.
- Do not create Markdown or YAML syllabus content under `templates/`; the build rejects that second
  authority.
- Treat `pipeline/syllabus_reference.docx` as a tracked renderer asset, not a syllabus-content
  template.
- Treat `site_docs/downloads/`, `site/`, and `output/` as generated, ignored output. Regenerate
  them from the active Markdown instead of editing or committing them.

The tracked `site_docs/fall_2026/shared/IMPORTANT_DATES.md` file is the stable page wrapper. Its
table content comes from the first worksheet of the linked Google Sheet. `pipeline/build_site.py`
runs the synchronization automatically; run only the synchronization step with:

```bash
source source_me.sh && python3 pipeline/sync_important_dates.py
```

The importer requires the expected six-column `Date`, confirmation, week, `X`, event, and notes
schema. It validates chronological dates and worksheet markers, groups the resulting tables by
month, and infers a student-scanning type from each event name. Confirmation, calculated week, and
notes are personal maintainer aids, while the `X` formula controls whether Google Sheets grays out a
past event. The importer validates but omits all four metadata cells from Markdown. It downloads
only from the fixed Google Sheets HTTPS source and replaces the ignored
`site_docs/generated/FALL_2026_IMPORTANT_DATES.md` fragment only after the complete response passes
validation. Every complete site build requires that live refresh and fails rather than publishing
the previous table when Google Sheets is unavailable. The fast pytest lane remains offline.

`pipeline/build_syllabi.py` coordinates the manifest, content, and rendering units under
`pipeline/build_lib/` to create one DOCX and one PDF per course. `pipeline/build_site.py` refreshes
the important dates, runs that document generation, and then performs the strict MkDocs build, so
the website publishes neither stale dates nor download links without their generated targets.

## Edit shared content

- Edit a policy in `site_docs/<term>/shared/policies/<topic>.md`.
- Edit shared assessment rules and the letter-grade scale in
  `site_docs/<term>/shared/policies/ASSESSMENT.md`. Its student-facing title is **Grades and graded
  work**.
- Edit office hours and instructor facts in
  `site_docs/<term>/shared/fragments/INSTRUCTOR_CONTACT_DETAILS.md`. The public
  `shared/INSTRUCTOR_INFORMATION.md` page embeds this canonical body.
- Edit Roosevelt learning goals in
  `site_docs/<term>/shared/fragments/ROOSEVELT_LEARNING_GOALS.md`.
- Edit shared support information in `site_docs/<term>/shared/STUDENT_RESOURCES.md`.

Course pages link to these sources; they do not keep policy or grade-scale copies.

## Live-term lifecycle

For Fall 2026, `site_docs/fall_2026/` is the only live syllabus authority. Do not maintain a
parallel Markdown template tree, archived-term tree, or future-term copy. To add a course, create
the standard course files listed under [Content organization](#content-organization) directly
below that term, use a current course only as a structural guide, and add the new pages to
`mkdocs.yml` navigation. Keep public term-wide material under `shared/` and include-only Markdown
under `shared/fragments/`.

Historical-term archive support is intentionally deferred until the Spring 2027 rollover. Until
that work begins, do not add another term source tree or an archive navigation branch. The Spring
rollover must define the snapshot location, tracked/generated boundary, and pipeline behavior
before a second term is introduced.

Add a `.meta.yml` file to the course folder to give every page in that folder the same web-header
color:

```yaml
course_color: "#1565c0"
```

Choose a dark color that gives white header text and controls at least 5.5:1 contrast. This
metadata affects the Material website only; complete PDF and DOCX exports keep their neutral
document styling.

Use descriptive links and real Markdown heading levels. Keep tables simple: use a named header for
every column, one idea per cell, the same number of cells in every row, and no merged cells. Align
long text left, numbers right, and short categories such as letter grades in the center. Do not use
blank table cells for visual layout. The build rejects malformed tables and hidden control
characters that can change Markdown line structure. Store private meeting links, passwords,
invitations, grades, and assignment submissions only in Blackboard.

The shared include engine runs before each renderer. After expansion, the PDF branch mirrors the
`markdown_extensions` entries in `mkdocs.yml`. Other MkDocs plugins, macros, theme hooks, and
JavaScript-dependent Material interactions do not transfer automatically. Before adding one of
those features to syllabus content, define and test a readable linear PDF and DOCX form.

## Edit dates

Dates are literal Markdown content. Edit `COURSE_DETAILS.md` and `SCHEDULE.md`, verify them against
the official academic calendar, and review every affected row. The build intentionally does not
shift dates because breaks, finals, and campus closures require academic judgment.

## Build and preview

Build the complete DOCX/PDF downloads and strict static site:

```bash
source source_me.sh
python3 pipeline/build_site.py
```

Preview the site locally:

```bash
source source_me.sh
python3 pipeline/build_syllabi.py
./run_web_server.sh
```

The preview opens in the default browser and stops automatically after five
minutes. `run_web_server.sh` refreshes the important-dates table before starting MkDocs. Press
`Ctrl-C` to stop it sooner.

Build only the complete documents:

```bash
source source_me.sh
python3 pipeline/build_syllabi.py
```

Optionally package the current generated documents into a ZIP under `output/archive/`:

```bash
source source_me.sh
python3 pipeline/build_syllabi.py --archive
```

This flag bundles the current generated PDF/DOCX files only. It does not create an archived-term
Markdown source tree or implement the deferred historical-term rollover.

Generated student downloads live in ignored, untracked `site_docs/downloads/`. The pipeline stages
and validates the complete set before replacing current downloads, then builds the site so links
cannot point to stale or partial output. Both formats use the same manifest-assembled Markdown
authority. Pandoc creates the DOCX after flattening web-only constructs such as admonitions.
Python-Markdown uses the extension stack from `mkdocs.yml` to create small semantic HTML, and
WeasyPrint renders that HTML directly to PDF.

## Refine course content

Tracked public Markdown is the working authority. Managers and agents produce a complete,
student-facing candidate from repository evidence rather than exposing draft-state warnings or
waiting for an approval transition. Record narrow evidence limitations in the refinement report,
not in the student syllabus.

Use the refinement checklist to improve:

- section numbers, CRNs, meeting places, and session dates;
- grading categories, totals, rounding, and late-work rules;
- assignment and exam dates, breaks, and final-exam details;
- Dr. Voss's shared course-policy language, including artificial-intelligence rules;
- current university-source statements and student-resource language;
- public contact information and the absence of meeting credentials.

A successful push to `main` that reaches the deploy job publishes the verified Pages artifact. If
several pushes arrive while a deployment runs, GitHub retains only the newest pending candidate. A
failed source, export, or site check blocks that candidate without requiring a separate
human-controlled manifest state.

## Validate

Run every local semantic-validation lane in dependency order:

```bash
./all_test.sh
```

The runner prints a phase banner and stops at the first failure. Both the export E2E and the Pages
production builder refresh the live Google Sheets dates; the final production rebuild is followed
by Playwright. Use the commands below for focused validation.

Run the fast repository checks:

```bash
source source_me.sh
python3 -m pytest tests/
```

After a site build, optionally run the desktop/mobile accessibility audit:

```bash
./run_playwright_tests.sh
```

Use `./run_playwright_tests.sh --build` to rebuild first.

Accessibility audits promote continuous improvement. The local runner returns a nonzero result so
findings receive maintainer attention, while Pages publication remains governed by artifact
generation. Review reported findings, prioritize barriers affecting students, and record deliberate
follow-up work.

## Refresh README screenshots

Build the production-shaped static site, then run the durable documentation capture harness:

```bash
source source_me.sh
python3 -m mkdocs build --strict
node tests/playwright/capture_readme_screenshots.mjs
mkdir -p docs/screenshots
cp /tmp/syllabus_readme_screenshots/fall_2026_home_light.png docs/screenshots/
cp /tmp/syllabus_readme_screenshots/general_genetics_dark.png docs/screenshots/
```

The harness captures the current local `site/` output over HTTP at a fixed desktop viewport. It
writes temporary PNGs under `/tmp/syllabus_readme_screenshots/`; the final two commands replace the
tracked README images. Review both images before keeping them. The README visual block is managed by
the screenshot workflow and should contain only current, tracked captures.

Run the complete production-readiness gate without publishing:

```bash
source source_me.sh && python3 tests/e2e/e2e_include_parity.py
```

This runner invokes the export E2E and strict site build, then checks include expansion across the
relevant website, DOCX, and PDF artifact corpora. The exporter rejects common Zoom meeting URLs,
embedded passwords or passcodes, and Discord invite links in syllabus source or downloadable text.
Private or access-controlled content does not belong anywhere in this repository, including ignored
paths.
