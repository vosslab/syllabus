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

### Derive course-document filenames from semantic metadata

**Decision.** Build course-document basenames from the fixed owner `Voss`, validated `course_code`
and `term` metadata, and a title-case document label. Complete syllabi use
`Voss-SUBJ_NUM[_NUM]-Semester_YYYY-Syllabus`; do not store a free-form basename in course YAML.

**Why.** A repeated output string can drift from the course identity, website links, and expected
build set. The instructor filename label is stable in this single-instructor repository, while
course and term metadata already own the changing parts.

**Consequence.** A course code or term that cannot produce the documented safe filename fails at
the manifest boundary. Renderers, publication checks, and related document generators call the
same formatter; changes to the filename convention belong in that formatter and this contract.

**Owner.** `pipeline/build_lib/syllabus_model.py` and `docs/FILE_FORMATS.md`.

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

### Use one information column for multi-section course facts

**Decision.** Course-information tables use `Field | Information`. State a fact once when it
applies to every listed section. When values differ, prefix each value with the applicable bold
course-section label. Keep short mappings on one line with a semicolon; separate longer mappings
with a visible `<br>`. Omit inapplicable section mappings and omit a row when none apply.

**Why.** Parallel section columns make shared values look comparative, consume scarce reading
width, and force horizontal scrolling on narrow screens. One information column gives the facts
visual priority while preserving an explicit section-to-value mapping only where students need it.
New lines make long mappings easier to scan, while omitted not-applicable labels avoid distracting
graduate students with undergraduate-only frameworks.

**Consequence.** The canonical GFM remains the portable two-column representation used by the
website, PDF, and DOCX; the renderers do not reconstruct or merge section columns. Website
key-value tables wrap inside the reading column at every supported viewport rather than owning a
horizontal scrollbar. Authors use an explicit `<br>` only when a long section mapping benefits
from a stable cross-format new line. The DOCX renderer converts that exact token to a native line
break instead of passing arbitrary HTML through to Word.

**Owner.** `site_docs/fall_2026/*/COURSE_DETAILS.md`,
`site_docs/assets/stylesheets/site.css`, `pipeline/pandoc_filters/docx_line_breaks.lua`, and
`docs/FILE_FORMATS.md`.

### Separate course facts from instructor information

**Decision.** Keep course logistics, format, catalog description, textbooks, and technology on each
course's `COURSE_DETAILS.md`. Keep contact methods, office hours, response expectations, and
department leadership on the one shared `INSTRUCTOR_INFORMATION.md` route. Link that route directly
from every course landing page and list it explicitly in every complete-document manifest.

**Why.** Students looking for course facts and students trying to contact the instructor have
different goals. Combining both makes long course-information pages harder to scan and duplicates
the same instructor material across courses.

**Consequence.** Instructor facts remain editable once in shared fragments, course-information pages
end after their course-specific content, and PDF/DOCX composition includes the shared page as a
normal ordered section rather than using an embedded-heading link exception.

**Owner.** `site_docs/fall_2026/shared/INSTRUCTOR_INFORMATION.md`, the three course landing pages and
manifests, `mkdocs.yml`, and `pipeline/build_lib/syllabus_content.py`.

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
duplicating the portrait in document source. The image's `data-document-width` attribute owns its
physical document width without changing browser layout. Website and PDF CSS consume the semantic
class; the DOCX Pandoc filter translates the generic width metadata into Pandoc's native image
width. No renderer infers presentation from surrounding table text.

**Owner.** `docs/FILE_FORMATS.md`,
`site_docs/fall_2026/shared/fragments/INSTRUCTOR_CONTACT_DETAILS.md`, and
`pipeline/pandoc_filters/docx_image_layout.lua` plus the website/PDF stylesheets.
