# File formats

## Syllabus manifests

Each course owns one `syllabus.yml` file beside its course Markdown. The manifest is the ordered
contract for a complete PDF and DOCX syllabus.

```yaml
title: General Genetics
course_code: BIOL 351/451
term: Fall 2026
author: Neil R. Voss
language: en-US
download_basename: BIOL_351_451_FALL_2026_SYLLABUS
sections:
  - index.md
  - COURSE_DETAILS.md
  - COURSE_LEARNING_FRAMEWORK.md
  - ASSIGNMENTS_AND_GRADING.md
  - SCHEDULE.md
shared_sections:
  - ../shared/policies/index.md
  - ../shared/policies/COURSE_DELIVERY.md
  - ../shared/policies/ASSESSMENT.md
  - ../shared/policies/DISCUSSION_MARKS.md
  - ../shared/policies/EXTRA_CREDIT.md
  - ../shared/IMPORTANT_DATES.md
  - ../shared/STUDENT_RESOURCES.md
```

Required scalar fields are `title`, `course_code`, `term`, `author`, `language`, and
`download_basename`. Each must be a non-empty string. `download_basename` accepts only uppercase
ASCII letters, digits, and underscores.

`sections` and `shared_sections` are non-empty ordered lists of local source paths. Every path must
resolve to an existing file below `site_docs/`. The order becomes the section order in complete
documents. The course list must contain exactly one `COURSE_LEARNING_FRAMEWORK.md` with the four
required learning-statement sections.

The global [site_docs/EXTRA_CREDIT_MOVIES.md](../site_docs/EXTRA_CREDIT_MOVIES.md) catalog is
website-only. Extra-credit policy pages may link to it, but course manifests omit it so the verbose
catalog does not enter PDF or DOCX syllabi.

## Course Markdown

Every complete-document source starts with one level-one heading. The website may add Material
admonitions, attributes, tables, and repository-owned restricted includes. The document renderer
converts supported web-only constructs into portable linear content.

Tables use a named header in every column, a valid separator row, and the same cell count in every
row. Hidden line-breaking controls are rejected. Links between manifest-included Markdown pages are
rewritten as internal document anchors in PDF and DOCX output.

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

`pipeline/sync_important_dates.py` reads a fixed six-column Google Sheets CSV source. The source
columns are date, confirmation, week, `X`, event, and notes. The generated Markdown publishes only
the date, event, and inferred event type; the remaining columns are validated maintainer metadata.

The generated fragment lives at `site_docs/generated/FALL_2026_IMPORTANT_DATES.md`. It is ignored
output included by the tracked `site_docs/fall_2026/shared/IMPORTANT_DATES.md` wrapper. Edit the
spreadsheet or importer, not the generated fragment. Every course manifest places that wrapper
near the end of the complete PDF and DOCX, immediately before student resources.

## Generated documents

Each manifest creates two files under `site_docs/downloads/` using `download_basename`:

- `<download_basename>.docx` from Pandoc and `pipeline/syllabus_reference.docx`.
- `<download_basename>.pdf` from Python-Markdown HTML and WeasyPrint.

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
for department-review checklists. It contains the published site base URL, the complete ordered
rubric, and course-specific overrides. Every item has a unique ID, group, label, one of three
statuses (`covered`, `needs_review`, or `not_applicable`), a list of site-relative evidence links,
and an explanatory note. Covered items require at least one evidence link.

The generator validates the complete schema, allows only the three documented statuses, resolves
evidence within the published syllabus site, and restricts writes to
`output/department_checklists/`. Generated Markdown and DOCX files remain ignored output.
