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

Student services use one directly navigable overview at `shared/STUDENT_RESOURCES.md` and six
task-focused pages under `shared/student_services/`. Course manifests list the overview followed by
every topic page, so the website supports quick lookup while PDF and DOCX syllabi retain the
complete resource set without duplicating content.

Each course manifest selects an ordered subset of the four assessment categories Dr. Voss uses:
assignments, group quizzes, face-to-face exams, and online exams. The model maps that closed
vocabulary to an ordered set of composite assessment sections. Each section owns one H2 root and
may attach separately authored H3 topics derived from category presence or absence. The website
hook and complete-document composer materialize the overview, derived notices for absent quizzes or
exams, applicable technology-interruption topics, and selected assessment details at the coursework
marker before calling the shared include engine, so one YAML decision controls all three formats.
The composition boundary validates the H2/H3 contract before rendering. The same manifest owns the
validated official Biology Problems subject URL shown inside the selected Assignments section.

For courses with confirmed point plans, the same manifest owns an ordered `course_point_plan` of
assessment labels and possible points. The website and complete-document composer replace one
coursework marker with a derived Markdown table, calculating the denominator and approximate
shares once for the website, PDF, and DOCX paths. The authored coursework page retains the
student-facing explanation around that generated table.

Discussion marks use a parallel closed manifest choice: no discussion, face-to-face discussion,
or remote/video-conference discussion. Participating courses own a thin Discussion marks page; no
discussion omits the topic. The build adds shared scoring only for modes that award marks.

Lab attendance uses a separate required `lab_status`: `no_lab` or `has_lab`. The status means that
Dr. Voss's syllabus itself does or does not include a lab; a separately taught co-requisite lab is
not enough. A course-details marker receives the canonical lab-attendance fragment only for
`has_lab`, keeping lab rules out of non-lab website pages and complete documents while preserving
one source for future lab courses.

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
- `pipeline/build_lib/table_layouts.py` classifies the closed set of syllabus tables and calculates
  wrap-aware column demand from every visible cell. It emits HTML column hints and supplies the
  same percentages to DOCX post-processing.

## Rendering branches

### Website branch

MkDocs reads `site_docs/`, calls
[pipeline/mkdocs_hooks.py](../pipeline/mkdocs_hooks.py) to validate and normalize inherited course
colors and expand authorized fragments, applies the Material theme, repository overrides, custom
CSS and JavaScript, and copies downloads and assets into `site/`. `mkdocs.yml` owns navigation,
hook registration, theme configuration, social links, and the public site URL.

The registered table-layout Markdown extension examines all header and body cells before emitting
a `colgroup`, content-derived minimum width, and semantic profile hook. CSS consumes those values;
it does not own per-table or per-profile column percentages. Compact tables use their calculated
content width, while prose-dense tables remain readable through the Material scroll wrapper on
narrow screens. Repeated tables with identical headers are calculated as one series, so month-by-
month or otherwise partitioned data keeps the same column boundaries throughout the page.

### DOCX branch

The content library calls the shared include engine, rewrites links between included pages as
document anchors, removes web-only controls, and the rendering library sends portable Markdown to
Pandoc. The tracked
`pipeline/syllabus_reference.docx` owns Word styles. Python post-processing adds metadata,
language, and semantic table properties before output verification.
Table post-processing reruns the shared content calculation over the Word cells so DOCX does not
maintain a parallel width map. Exact-header series use the same combined demand and therefore the
same Word column widths as each other.

### PDF branch

The same composed Markdown is rendered to semantic HTML with the Markdown extension stack loaded
from `mkdocs.yml`. The validated adjacent `.meta.yml` course accent is attached to the standalone
HTML as a CSS custom property so the website and PDF share one color authority. WeasyPrint applies
`site_docs/assets/stylesheets/syllabus_pdf.css` and creates a tagged PDF. Poppler verifies document
metadata, text, tables, and required section titles.

Each manifest's `short_name` supplies the compact left PDF footer. CSS running strings place the
most recent level-two or level-three heading, including important-date month headings, in the wider
center position; the right position owns the page count. The full course code, title, and term stay
in the document title block instead of repeating in the footer.

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

Only public-safe content belongs in tracked sources and the publication pipeline. The document
builder scans source and generated text for common meeting URLs, passwords, passcodes, and
invitation patterns. Private links, student information, grades, and access-controlled materials
remain outside the public MkDocs source and generated syllabi. Assignment-specific directions may
be communicated through course links or in class; public expectations belong in the authoritative
course Markdown.

The ignored local `raw/` directory may hold public or private internal reference material that
supports authoring. It is outside the content pipeline, never supplies a published page or
complete-syllabus section, and the builder rejects any tracked file below it. Move a verified
public fact into the canonical Markdown source rather than linking a course page or manifest to
`raw/`.

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
- Use [pipeline/build_department_checklists.py](../pipeline/build_department_checklists.py) to
  render the tracked rubric and course-specific doubts from
  [pipeline/department_checklists.yml](../pipeline/department_checklists.yml) as separate
  department-submission Markdown and DOCX files under `output/department_checklists/`.
- Add deterministic unit and integration checks under [tests/](../tests/); place production
  builds in [tests/e2e/](../tests/e2e/) and browser checks in
  [tests/playwright/](../tests/playwright/).

## Known gaps

- Define and validate the historical-term snapshot, generated-output, and navigation design before
  creating the Spring 2027 source tree.
