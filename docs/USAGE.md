# Usage

## Content organization

Public course content lives under `site_docs/<term>/<course>/`. Each course contains:

- `index.md` for the short overview, task links, course summary, and secondary download links.
- `COURSE_DETAILS.md` for registration, instructor, and catalog information.
- `LEARNING_OUTCOMES.md` for assessable outcomes.
- `ASSIGNMENTS_AND_GRADING.md` for assessment and grade calculations.
- `SCHEDULE.md` for literal meeting dates and topics.
- `COURSE_POLICIES.md` for rules unique to the course.
- `syllabus.yml` for export order, metadata, and publication state.

Each term keeps `POLICIES.md` and `STUDENT_RESOURCES.md` separate. The manifest appends both files
once to every complete syllabus. Local source material under `raw/` is ignored and must never be
linked from public content.

## Start a course

Copy `templates/course/` to a new term/course folder. Copy `templates/POLICIES.md` and
`templates/STUDENT_RESOURCES.md` when starting a new term. Replace every placeholder, then add the
new pages to `mkdocs.yml` navigation.

Add a `.meta.yml` file to the course folder to give every page in that folder the same web-header
color:

```yaml
course_color: "#1565c0"
```

Choose a dark color that gives white header text and controls at least 5.5:1 contrast. This
metadata affects the Material website only; complete PDF and DOCX exports keep their neutral
document styling.

Use descriptive links and real Markdown heading levels. Keep tables simple: one header row, one
idea per cell, and no merged cells. Store private meeting links, passwords, invitations, grades,
and assignment submissions only in Blackboard.

The PDF branch mirrors the `markdown_extensions` entries in `mkdocs.yml`. MkDocs plugins, macros,
theme hooks, and JavaScript-dependent Material interactions do not transfer automatically. Before
adding one of those features to syllabus content, define and test a readable linear PDF and DOCX
form.

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
minutes. Press `Ctrl-C` to stop it sooner.

Build only the complete documents:

```bash
source source_me.sh
python3 pipeline/build_syllabi.py
```

Create an offline term ZIP in `output/archive/`:

```bash
source source_me.sh
python3 pipeline/build_syllabi.py --archive
```

Generated student downloads live in ignored `site_docs/downloads/`. They are rebuilt before the
site so download links cannot point to stale tracked binaries. Both formats use the same
manifest-assembled Markdown authority. Pandoc creates the DOCX after flattening web-only constructs
such as admonitions. Python-Markdown uses the extension stack from `mkdocs.yml` to create small
semantic HTML, and WeasyPrint renders that HTML directly to PDF.

## Approve publication

New manifests begin with `publication_status: draft`. Draft exports display a distribution warning,
and the Pages workflow refuses to deploy them when publication is enabled.

Before changing a manifest to `publication_status: approved`, confirm:

- section numbers, CRNs, meeting places, and session dates;
- grading categories, totals, rounding, and late-work rules;
- assignment and exam dates, breaks, and final-exam details;
- course-specific artificial-intelligence language;
- current university policy and student-resource language;
- public contact information and the absence of meeting credentials;

After all manifests are approved, set the GitHub Actions repository variable `PUBLISH_SYLLABI` to
`true`. Pushes to `main` then deploy the verified Pages artifact. Remove or unset that variable to
keep building without deployment.

## Validate

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

Accessibility audits promote continuous improvement but do not block publication. Review reported
findings, prioritize barriers affecting students, and record deliberate follow-up work.

Run the production-readiness gate without publishing:

```bash
bash tests/e2e/e2e_syllabus_export.sh --require-approved
```

The exporter rejects common Zoom meeting URLs, embedded passwords or passcodes, and Discord invite
links in public source or downloadable text. A passing security scan is not a substitute for human
review of each public page.
