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
  - ../shared/STUDENT_RESOURCES.md
```

Required scalar fields are `title`, `course_code`, `term`, `author`, `language`, and
`download_basename`. Each must be a non-empty string. `download_basename` accepts only uppercase
ASCII letters, digits, and underscores.

`sections` and `shared_sections` are non-empty ordered lists of local source paths. Every path must
resolve to an existing file below `site_docs/`. The order becomes the section order in complete
documents. The course list must contain exactly one `COURSE_LEARNING_FRAMEWORK.md` with the four
required learning-statement sections.

## Course Markdown

Every complete-document source starts with one level-one heading. The website may add Material
admonitions, attributes, tables, and restricted snippet includes configured in `mkdocs.yml`. The
document renderer converts supported web-only constructs into portable linear content.

Tables use a named header in every column, a valid separator row, and the same cell count in every
row. Hidden line-breaking controls are rejected. Links between manifest-included Markdown pages are
rewritten as internal document anchors in PDF and DOCX output.

## Shared fragments

Include-only Markdown lives under `site_docs/<term>/shared/fragments/` and uses this exact one-line
notation:

```markdown
--8<-- "fall_2026/shared/fragments/INSTRUCTOR_CONTACT_DETAILS.md"
```

The path must name a non-empty `.md` file below `site_docs/`. Absolute paths, `..` traversal,
remote URLs, and nested includes are invalid. Fragments do not receive direct website routes.

## Course metadata

An optional `.meta.yml` beside course pages supplies the website-only course header color:

```yaml
course_color: "#1565c0"
```

This value does not change the neutral PDF or DOCX styles. Choose a dark color that gives white
header text and controls at least 5.5:1 contrast.

## Synchronized dates

`pipeline/sync_important_dates.py` reads a fixed six-column Google Sheets CSV source. The source
columns are date, confirmation, week, `X`, event, and notes. The generated Markdown publishes only
the date, event, and inferred event type; the remaining columns are validated maintainer metadata.

The generated fragment lives at `site_docs/generated/FALL_2026_IMPORTANT_DATES.md`. It is ignored
output included by the tracked `site_docs/fall_2026/shared/IMPORTANT_DATES.md` wrapper. Edit the
spreadsheet or importer, not the generated fragment.

## Generated documents

Each manifest creates two files under `site_docs/downloads/` using `download_basename`:

- `<download_basename>.docx` from Pandoc and `pipeline/syllabus_reference.docx`.
- `<download_basename>.pdf` from Python-Markdown HTML and WeasyPrint.

The builder verifies that all expected files exist before publishing them and removes obsolete
managed downloads. `--archive` packages the current generated documents as ZIP files under
`output/archive/`; it does not create a historical Markdown source tree.

