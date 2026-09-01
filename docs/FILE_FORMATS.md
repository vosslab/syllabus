# File formats

## Syllabus manifests

Each course owns one `syllabus.yml` file beside its course Markdown. The manifest is the ordered
contract for a complete PDF and DOCX syllabus.

```yaml
title: General Genetics
short_name: Genetics
course_code: BIOL 351/451
term: Fall 2026
author: Neil R. Voss
language: en-US
assessment_examples_url: https://biologyproblems.org/genetics/
course_point_plan:
  - assessment: Mid-term exam
    points: 100
  - assessment: Final cumulative exam
    points: 100
  - assessment: Five group quizzes
    points: 100
  - assessment: Assignments
    points: 116
  - assessment: Course orientation
    points: 8
sections:
  - index.md
  - COURSE_DETAILS.md
  - ../shared/INSTRUCTOR_INFORMATION.md
  - COURSE_LEARNING_FRAMEWORK.md
  - ASSIGNMENTS_AND_GRADING.md
  - DISCUSSION_MARKS.md
  - SCHEDULE.md
assessments:
  - assignments
  - group_quizzes
  - f2f_exams
discussion: f2f_discussion
lab_status: no_lab
shared_sections:
  - ../shared/policies/index.md
  - ../shared/policies/COURSE_DELIVERY.md
  - ../shared/policies/ASSESSMENT.md
  - ../shared/policies/EXTRA_CREDIT.md
  - ../shared/IMPORTANT_DATES.md
  - ../shared/STUDENT_RESOURCES.md
  - ../shared/student_services/ACADEMIC_ADVISING.md
  - ../shared/student_services/LEARNING_SUPPORT.md
  - ../shared/student_services/PROGRAMS_AND_CAREER.md
  - ../shared/student_services/TECHNOLOGY_AND_CAMPUS.md
  - ../shared/student_services/MONEY_AND_ESSENTIAL_NEEDS.md
  - ../shared/student_services/HEALTH_IDENTITY_AND_SAFETY.md
```

Required scalar fields are `title`, `short_name`, `course_code`, `term`, `author`, `language`, and
`assessment_examples_url`. Each must be a non-empty string.
`short_name` is the concise course label shown in generated PDF footers and may contain at most 40
characters.
The builder derives document filenames from `course_code` and `term`; manifests do not store a
separate output basename. Course codes use an uppercase subject followed by one or more
slash-separated course numbers. Terms use a title-case semester and four-digit year.
`assessment_examples_url` accepts only an HTTPS `biologyproblems.org` subject route with one safe
lowercase slug, such as `https://biologyproblems.org/biochemistry/`.

`course_point_plan` is an optional ordered list for courses whose point values are confirmed. Each
entry contains exactly one unique `assessment` label and one integer `points` value. Labels are
plain ASCII text from 1 through 100 characters. Point values range from 1 through 1,000,000, and a
plan contains at most 100 entries. Include only work that counts toward the final-percentage
denominator; extra credit remains outside this list.

The builder sums the point values for the **Total** row and calculates each **Approximate share**
against that derived total. Shares use half-up rounding to one decimal place and omit a trailing
`.0`; because each detail row is rounded independently, displayed detail shares need not sum to
exactly 100%. The derived Total row always displays `100%`, is visually emphasized as the sum, and
leaves its **Your points** cell blank with the other rows so students can calculate their grade on
screen or in print. A course with `course_point_plan` data must place this marker exactly once in
`ASSIGNMENTS_AND_GRADING.md`:

```markdown
<!-- course point plan from syllabus.yml -->
```

`assessments` is a non-empty ordered list containing one or more of `assignments`,
`group_quizzes`, `f2f_exams`, and `online_exams`, with no duplicates. These are the only assessment
categories across Dr. Voss's classes. The model maps them to the four canonical Markdown files under
`shared/fragments/assessments/`.

Each course's `ASSIGNMENTS_AND_GRADING.md` contains one
`<!-- assessments from syllabus.yml -->` marker. The website, PDF, and DOCX replace it with the
ordered composite assessment sections through the shared include engine. Each section has one H2
root and may attach manifest-derived H3 topic fragments based on category presence or absence. The
resolver includes the overview, explicit notices when a course has no quizzes or no exams,
applicable technology-interruption topics, and the manifest-selected detail sections. Course pages
do not include these fragments separately. Missing, duplicate, or misplaced markers fail
explicitly.

Every assessment section-root fragment begins with exactly one level-two heading and may contain
level-three headings. A separately authored topic fragment begins with exactly one level-three
heading and remains attached to its section root. Level skips and additional roots fail before
rendering. Short assessment-type labels in the overview use bold paragraph lead-ins rather than
headings. The website therefore presents each selected assessment as a major page section, while
complete-document composition demotes the same hierarchy one level beneath Coursework and grades.

Cross-assessment guidance belongs in a composite section, not inside one selected assessment type.
`TECHNOLOGY_INTERRUPTION.md` owns the shared H2 introduction. Its assignment topic appears only when
`assignments` is selected; its timed-assessment topic appears when `group_quizzes` or `online_exams`
is selected and describes limited-attempt Blackboard work without naming an unused category. The
availability section derives `No quizzes` and `No exams` topics from categories that are absent.
Assignment attempts remain timed even though students may retry without a set limit.

The shared `ASSIGNMENTS.md` fragment contains one
`<!-- assessment examples from syllabus.yml -->` marker. After the selected assessment fragments
are expanded, the builder replaces it with the manifest's `assessment_examples_url` as the
course-specific Biology Problems practice link. Keep this marker in the shared Assignments fragment
instead of copying a subject URL into course Markdown.

`discussion` is exactly one of `no_discussion`, `f2f_discussion`, or `remote_discussion`. Each
participating course's `DISCUSSION_MARKS.md` contains one
`<!-- discussion from syllabus.yml -->` marker. `no_discussion` omits that page and content;
face-to-face and remote discussion include the selected format plus the shared criticism, scoring,
and no-make-up fragment.

`lab_status` is required and is exactly `no_lab` or `has_lab`. It describes whether this syllabus
includes a lab taught by Dr. Voss; co-registration in a separately taught lab does not make a
lecture syllabus `has_lab`. Every `COURSE_DETAILS.md` contains one
`<!-- lab attendance from syllabus.yml -->` marker. `no_lab` removes the marker without adding
content. `has_lab` replaces it with the canonical lab attendance and preparation policy under
`shared/fragments/labs/`. The same selection is applied to the website, PDF, and DOCX.

`sections` and `shared_sections` are non-empty ordered lists of local source paths. Every path must
resolve to an existing file below `site_docs/`. The order becomes the section order in complete
documents. `sections` owns the opening course flow and may reference the shared instructor page so
it follows `COURSE_DETAILS.md` without copying its content. The course flow must contain exactly one
`COURSE_LEARNING_FRAMEWORK.md` with the four required learning-statement sections.

The global [site_docs/EXTRA_CREDIT_MOVIES.md](../site_docs/EXTRA_CREDIT_MOVIES.md) catalog is
website-only. Extra-credit policy pages may link to it, but course manifests omit it so the verbose
catalog does not enter PDF or DOCX syllabi.

## Course Markdown

Every complete-document source starts with one level-one heading. The website may add Material
admonitions, attributes, tables, and repository-owned restricted includes. The document renderer
converts supported web-only constructs into portable linear content.

The coursework source retains the student-facing prose around a manifest-derived point table. It
uses the exact course-point-plan marker documented above instead of duplicating totals and
percentages in Markdown.

Tables use a named header in every column, a valid separator row, and the same cell count in every
row. Hidden line-breaking controls are rejected. A visible `<br>` may separate long section
mappings inside a course-information cell. The website and PDF render the tag directly;
`pipeline/pandoc_filters/docx_line_breaks.lua` converts that exact token to a native DOCX line
break. The build classifies the closed set of table
headers, examines every visible cell, and derives wrap-aware relative column widths for website,
PDF, and DOCX output. Authors do not add width markup to individual Markdown tables. A new header
shape must be registered explicitly so an unknown table cannot silently receive arbitrary layout.
Short identifier columns are detected from their complete visible content and use compact padding;
schedule layouts give additional line length to prose columns. Inline HTML styling hooks do not
count toward visible width demand.
Within one rendered page or document, tables with the exact same headers form a series: the widest
demand for each column across the full series supplies one shared width vector to every table. The
monthly University important-dates tables therefore align even when one month has much longer event
text than another. Course-information tables use `Field | Information`: shared facts appear once,
while distinct facts use bold course-section labels. Short mappings remain semicolon-separated;
long mappings place each section on a new line with `<br>`. Omit an inapplicable section mapping,
and omit the entire row when none of the listed sections use that field.
These key-value tables wrap inside the website reading column instead of scrolling horizontally.
The section-information table stays together as one block in PDF when it fits on a page.
Links between manifest-included Markdown pages are rewritten as internal document anchors in PDF
and DOCX output.

A five-column schedule may use `Week | Date | Topic | Quiz | Due this date`. The Quiz cells carry
the numbered coverage cue while Topic remains course-content prose. A bold Topic with an empty Quiz
cell is a major schedule milestone; the renderer spans it across the Topic and Quiz columns while
keeping Due this date independent in the website, PDF, and DOCX.

## Shared fragments

Include-only Markdown lives under a `fragments` or `generated` directory below `site_docs/` and
uses this exact one-line notation:

```markdown
--8<-- "fall_2026/shared/fragments/INSTRUCTOR_CONTACT_DETAILS.md"
```

The quoted path is always relative to `site_docs/`, never to the including page. It must name a
non-empty `.md` file whose relative path contains a directory named `fragments` or `generated`.
The engine in [pipeline/build_lib/markdown_includes.py](../pipeline/build_lib/markdown_includes.py)
expands the file once for the website, DOCX, and PDF paths.

Relative Markdown links, images, and HTML `href` or `src` attributes inside a fragment resolve from
the fragment's own directory. During expansion, the engine rebases them for the receiving page so
one linked fragment can render correctly at different page depths. A relative target that escapes
`site_docs/` fails the build.

The instructor-contact fragment references the tracked light-background portrait as its one
canonical Markdown image. Keep both portrait variants under `site_docs/assets/images/`; the
cross-format rendering strategy is recorded in [DESIGN_DECISIONS.md](DESIGN_DECISIONS.md).
An image that needs a fixed physical width in complete documents may declare a positive
`data-document-width` using `in`, `cm`, `mm`, or `pt`. The website safely ignores that data
attribute, PDF sizing remains in CSS, and `pipeline/pandoc_filters/docx_image_layout.lua` translates
it into Pandoc's native DOCX width. Do not infer image layout from captions, table labels, or file
names.

Absolute paths, `..` traversal, remote URLs, symlink escapes, nested includes, single-quoted or
unquoted paths, block form, section selection, and alternate marker lengths are invalid. Any line
containing `--8<--` that does not match the exact form fails the build. Authorized Markdown remains
excluded from direct website routes through `exclude_docs`; that navigation exclusion does not
authorize any additional directory.

## Course metadata

A required `.meta.yml` beside each course manifest supplies one light and one dark course accent:

```yaml
course_color: "#1565c0"
course_color_dark: "#8ab4f8"
```

Both values must use six-digit hex notation. `course_color` controls the Material header, light
website accents, and PDF accents; choose it to give both white header controls and dark PDF text at
least 5.5:1 contrast. `course_color_dark` controls content accents on the slate website surface and
must also reach at least 5.5:1 there. DOCX output retains its format-native neutral styling.

## Synchronized dates

`pipeline/sync_important_dates.py` reads a fixed six-column Google Sheets CSV source. Its normalized
headers are `date`, `confirmed`, `wk`, `x`, `event`, and `notes`; a `Confirmed for YYYY` header
normalizes to `confirmed`. The generated Markdown publishes only the date, event, and inferred event
type; the remaining columns are validated maintainer metadata.

The generated fragment lives at `site_docs/generated/FALL_2026_IMPORTANT_DATES.md`. It is ignored
output included by the tracked `site_docs/fall_2026/shared/IMPORTANT_DATES.md` wrapper. Edit the
spreadsheet or importer, not the generated fragment. Every course manifest places that wrapper
near the end of the complete PDF and DOCX, immediately before student resources.

## Generated documents

Each manifest creates two files under `site_docs/downloads/` using this fixed contract:

- `Voss-SUBJ_NUM[_NUM]-Semester_YYYY-Syllabus.docx` from Pandoc and
  `pipeline/syllabus_reference.docx`.
- `Voss-SUBJ_NUM[_NUM]-Semester_YYYY-Syllabus.pdf` from Python-Markdown HTML and WeasyPrint.

For example, BIOL 351/451 in Fall 2026 produces
`Voss-BIOL_351_451-Fall_2026-Syllabus.pdf`. `Voss` and `Syllabus` are fixed title-case labels;
slashes between course numbers become underscores, and the title case of `Fall` is preserved.

Complete syllabi include a linked, page-numbered contents list. Its concise instructor labels are
derived mechanically from source page filenames in Title Case, while the visible section headings
retain their student-facing wording. PDF footers use running strings and page counters; DOCX
footers use standard Word fields. Both place course and term information on the left, the current
student-facing section heading in the center, and `Page X of Y` on the right.

The builder verifies that all expected files exist before publishing them and removes obsolete
managed downloads. `--archive` packages the current generated documents as ZIP files under
`output/archive/`; it does not create a historical Markdown source tree.

## Department checklist data

[pipeline/department_checklists.yml](../pipeline/department_checklists.yml) is the tracked source
for department-review checklists. It contains the complete ordered rubric and course-specific
overrides. Every item has a unique ID, group, label, one of three statuses (`covered`,
`needs_review`, or `not_applicable`), a list of site-relative evidence routes, and an explanatory
note. Covered items require at least one evidence route.

The generator validates the complete schema, allows only the three documented statuses, resolves
evidence within the Fall 2026 source authority, and restricts writes to
repository-root `department_checklists/`. It first rebuilds the separate complete syllabus PDFs.
Each course then produces matching Markdown, DOCX, and tagged, letter-size checklist files.
Evidence routes map through the syllabus PDF's named destinations to visible references containing
the syllabus filename, one-based page number, source page title, and checklist topic. The checklist
does not depend on web links. Checklist PDFs embed Atkinson Hyperlegible Next from the repository's
licensed font assets. Checklist and syllabus DOCX files use the Arial-based
`pipeline/syllabus_reference.docx` and do not embed fonts. Generated checklist files remain ignored
output.
