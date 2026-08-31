# Design decisions

<!-- VENDORED HEADER: START -->
Record each durable decision about how this code and repository are shaped, once it is settled, with
the reasoning a later reader needs. Guidance Neil Voss states belongs in
[HUMAN_GUIDANCE.md](HUMAN_GUIDANCE.md), dated history in `docs/CHANGELOG.md`, open discussion in
`docs/active_plans/decisions/`. [PROPAGATED HEADER - ENTRIES BELOW ARE YOURS]
<!-- VENDORED HEADER: END -->

Write each decision as a level-three heading with these four fields. `Owner` names the
authoritative code or contract document, rather than a person.

```markdown
### <decision title>

**Decision.** <the durable direction>

**Why.** <the reason it was chosen>

**Consequence.** <the constraint a future change preserves>

**Owner.** <the authoritative code or contract doc>
```

## Software design

### Compose shared and selected assessment hierarchy from one marker

**Decision.** Resolve the manifest's assessment categories into ordered composite sections. Each
section owns one H2 root and may attach separately authored, manifest-derived H3 topic fragments.
Topics may follow selected categories or the absence of quizzes or exams. Materialize the overview,
availability notices, applicable interruption guidance, and selected assessment details from the
coursework marker. Use bold paragraph lead-ins for compact policy cases and the overview's short
glossary labels.

**Why.** The website page H1 needs major assessment sections as H2 peers. Manually including the
overview while injecting only the details split ownership. Policies used by multiple assessment
types also need one core owner rather than copies inside selected detail fragments. Styling global
H3 elements to repair one flattened page would change unrelated syllabus pages without correcting
the content hierarchy.

**Consequence.** Course pages retain one assessment marker and no direct assessment-fragment
includes. The manifest resolver, not the renderer, owns which composite sections and topics apply.
The composition boundary rejects malformed H2 roots, H3 topic fragments, and heading-level skips
before website, PDF, or DOCX rendering. The shared global heading styles remain renderer-wide rather
than acquiring page-specific exceptions.

**Owner.** `pipeline/build_lib/syllabus_model.py`, `pipeline/build_lib/syllabus_content.py`, and
`docs/FILE_FORMATS.md`.

### Select lab attendance by course manifest

**Decision.** Require each course manifest to declare `lab_status` as `no_lab` or `has_lab`.
Materialize the canonical lab-attendance fragment at the course-details marker only for
`has_lab`; keep the general shared attendance policy lab-neutral.

**Why.** Lab rules belong only to a class Dr. Voss teaches as a lab. A global policy URL cannot
vary by referring course, and Genetics co-registration does not mean its lecture syllabus owns the
separately taught lab's attendance policy.

**Consequence.** Every course details page retains one lab marker, every manifest declares an
allowlisted status, and lab wording is edited only in the lab fragment. New lab states require an
explicit model and documentation change rather than being inferred from course names or prose.

**Owner.** `site_docs/fall_2026/*/syllabus.yml`,
`site_docs/fall_2026/shared/fragments/labs/LAB_ATTENDANCE.md`, and
`pipeline/build_lib/syllabus_model.py`.

### Split student services by task behind one overview

**Decision.** Keep `shared/STUDENT_RESOURCES.md` as the established student-services overview and
place the service details in task-focused pages under `shared/student_services/`. List the overview
and every topic page in each course manifest.

**Why.** One 25-heading page forces students to scan unrelated academic, technology, financial,
health, and identity information. A short task list supports recognition and preserves the familiar
entry route without creating course-specific copies.

**Consequence.** New durable services belong in the matching topic page. A new topic requires an
overview link, MkDocs navigation entry, manifest entry for every course, and browser-route coverage.
Complete PDF and DOCX syllabi retain every service topic once.

**Owner.** `site_docs/fall_2026/shared/STUDENT_RESOURCES.md`,
`site_docs/fall_2026/shared/student_services/`, `site_docs/fall_2026/*/syllabus.yml`, and
`mkdocs.yml`.

### Derive table widths from content through one shared calculator

**Decision.** Classify the supported syllabus table headers fail-closed, but calculate column
widths from every visible cell through one renderer-neutral Python implementation. CSS consumes
generated column hints; DOCX post-processing calls the same calculation. Do not maintain
per-table or per-profile width percentages.

**Why.** Header-only and equal-width layouts routinely over-allocate space to short numbers while
forcing student-facing explanations to wrap. Content-derived demand adapts when rows change and
keeps the layout rule testable and inspectable without coupling it to one course's current text.

**Consequence.** New table shapes must register their semantic headers, while width changes belong
in the generic demand algorithm and must be reviewed through both the calculated report and
rendered browser/PDF evidence. Authors do not add width markup to Markdown content. Repeated tables
with exact matching headers form one layout series and share the maximum demand measured for each
column; tables with different headers remain independent.

**Owner.** `pipeline/build_lib/table_layouts.py`, `docs/FILE_FORMATS.md`, and
`tests/playwright/capture_table_review.mjs`.

### Pair Genetics schedule colors with quiz and assignment numbers

**Decision.** Mark Genetics topic cells and their corresponding quiz dates with one matching color
per quiz, while repeating the quiz number in both cells. List assignments by number on their due
date in the same compact due column as quizzes and exams.

**Why.** The original online schedule let students scan from a quiz to the material it covered and
from a numbered assignment to its deadline. Color alone excludes some readers, while generic
"quiz" and "assignment" labels discard the identity needed to make either relationship clear.

**Consequence.** Quiz numbers are the authoritative coverage cue and color is supplementary. The
website supplies measured light- and dark-theme companions, the PDF retains the light palette, and
DOCX remains understandable from text alone. The compact four-column table keeps assessment and
assignment deadlines visible together rather than pushing a second due column off screen.

**Owner.** `site_docs/fall_2026/genetics/SCHEDULE.md`,
`site_docs/assets/stylesheets/site.css`, `site_docs/assets/stylesheets/syllabus_pdf.css`, and
`pipeline/build_lib/table_layouts.py`.

## Dependencies

## Generated artifacts

### Use the PDF footer as a compact orientation strip

**Decision.** Use a manifest-owned short course name at the left of every PDF page, the most recent
meaningful level-two or level-three heading in the wide center position, and a compact page count at
the right. Keep the full course code, title, and term in the title block. Do not divide the footer
with repeated line segments.

**Why.** Repeating the complete course identity consumed the footer while adding little after the
title page. A short identity plus current heading helps students recognize both the document and
their location, and the wider center position accommodates specific headings without crowding the
page count.

**Consequence.** Every course manifest owns a concise `short_name`. New heading levels do not enter
the footer unless they remain useful and legible across a complete rendered-PDF review.

**Owner.** `site_docs/fall_2026/*/syllabus.yml`, `pipeline/build_lib/syllabus_model.py`, and
`site_docs/assets/stylesheets/syllabus_pdf.css`.

### Use one instructor image source with a website-only dark-theme substitution

**Decision.** Keep one accessible Markdown image in the shared instructor-contact fragment. It
references the light-background portrait used by the light website theme, PDF, and DOCX. When the
Material website uses its `slate` scheme, CSS replaces only the rendered image content with the
matching dark-background portrait.

**Why.** One source image keeps the shared fragment portable across MkDocs, Pandoc, and
WeasyPrint, gives the portrait one text alternative and one semantic table position, and avoids
duplicating theme-specific markup in every generated document. PDF and DOCX have light pages and
therefore do not need the dark variant.

**Consequence.** Preserve both tracked portrait assets, the canonical light-image reference, and
the website's scoped dark-theme substitution as one unit. A future presentation change must still
embed only the light portrait in PDF and DOCX, expose one meaningful text alternative, and avoid
duplicating the portrait in document source.

**Owner.** `docs/FILE_FORMATS.md`,
`site_docs/fall_2026/shared/fragments/INSTRUCTOR_CONTACT_DETAILS.md`, and
`site_docs/assets/stylesheets/site.css`.
