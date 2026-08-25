# Usage

## Content organization

Public course content lives under `site_docs/<term>/<course>/`. Each course contains:

- `index.md` for the short overview, task links, course summary, and secondary download links.
- `COURSE_DETAILS.md` for registration, meeting, catalog, and embedded shared instructor
  information.
- `COURSE_LEARNING_FRAMEWORK.md` for Roosevelt learning goals, learning objectives, course
  learning outcomes, and overall learning goals. Its student-facing title is **Learning
  Objectives, Outcomes, and Goals**.
- `ASSIGNMENTS_AND_GRADING.md` for assessment and grade calculations.
- `SCHEDULE.md` for literal meeting dates and topics.
- `syllabus.yml` for export order, metadata, and publication state.

Each term keeps a short `POLICIES.md` topic index, canonical topic files under `policies/`, and one
`STUDENT_RESOURCES.md` file for support information. Every course links to the shared policy and
resource branches. Its manifest adds the policy overview as a section heading, then appends each
policy topic and the student-resource source once to the complete syllabus. The overview's web-only
topic links are omitted from document exports.

Term-wide fragments under `shared/` hold facts that students need in more than one context but the
instructor should edit once. The current fragments provide instructor information, including
office hours, and Roosevelt learning-goal bullets. Course pages embed them with the restricted
syntax:

```markdown
--8<-- "fall_2026/shared/INSTRUCTOR_INFORMATION.md"
```

Includes must be non-empty `.md` files below `site_docs/`; absolute paths, parent traversal, remote
URLs, and nested includes are rejected. Shared fragments are excluded from direct website routes.
Only public-safe canonical content belongs in this repository. Do not create an ignored `raw/`
tree for private syllabi, credentials, meeting links, student information, or access-controlled
material; transfer only public facts into the tracked Markdown sources.

## Edit shared content

- Edit a policy in `site_docs/<term>/policies/<topic>.md`.
- Edit the letter-grade scale in `site_docs/<term>/policies/GRADING.md`.
- Edit office hours and instructor facts in `site_docs/<term>/shared/INSTRUCTOR_INFORMATION.md`.
- Edit Roosevelt learning goals in `site_docs/<term>/shared/ROOSEVELT_LEARNING_GOALS.md`.
- Edit shared support information in `site_docs/<term>/STUDENT_RESOURCES.md`.

Course pages link to these sources; they do not keep policy or grade-scale copies.

## Live-term lifecycle

Treat the active term folder as the only live syllabus authority. Do not maintain a parallel
Markdown template tree or a future-term copy while the current term is active. To add a course,
create the standard course files listed under [Content organization](#content-organization)
directly below the active term, use a current course only as a structural guide, and add the new
pages to `mkdocs.yml` navigation. Keep shared policy and resource files at the term level.

At the end of the term, build and preserve the completed term snapshot before creating the next
active term. This is the point when historical duplication becomes intentional archival evidence,
not another live editing target.

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

Every successful push to `main` deploys the verified Pages artifact. A failed source, export, or
site check blocks delivery without requiring a separate human-controlled manifest state.

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

Run the complete production-readiness gate without publishing:

```bash
bash tests/e2e/e2e_syllabus_export.sh
```

The exporter rejects common Zoom meeting URLs, embedded passwords or passcodes, and Discord invite
links in syllabus source or downloadable text. Private or access-controlled content does not belong
anywhere in this repository, including ignored paths.
