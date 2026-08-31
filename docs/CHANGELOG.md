## 2026-08-31

### Additions and New Features

- Added Joshua Campbell's current Biological, Physical and Health Sciences advising role, office,
  phone, email, and public appointment route to the shared Fall 2026 student resources. The shared
  source makes the department-specific contact available in all three course syllabi.
- Added Nathan La Porte as the department laboratory contact for students planning laboratory
  courses, independent study, or research and seeking access, lab-coat, safety-document, or other
  laboratory support. Expanded the existing TRIO SSS resource to cover its current STEM and
  non-STEM services, student benefits, eligibility, and public application page.
- Added student-facing English language support that explains placement referral, student
  self-referral, and an instructor's Navigate Early Alert as paths to tutoring through the Office
  of International Programs.
- Added separate McNair Scholars and Chicago STEM Center resources. The McNair section distinguishes
  its research and graduate-school mission from TRIO SSS and summarizes eligibility, services, and
  contact information; the STEM Center section presents AUD 835 as a tutoring, computer, printing,
  coffee, study, and community space.
- Added tracked, public-safe CSHP leadership and DBPS Fall 2026 faculty references under `docs/`.
  The exact chair memo remains under ignored `raw/` because it contains active access codes and
  access-controlled links.
- Refreshed the Fall 2026 department-checklist action report against all three current syllabi and
  all 53 items in the department source. Selected the updated Markdown file as the working authority
  after confirming that both Markdown copies and the updated DOCX contain the same item wording.
- Added one shared Python table-layout calculator that reads every visible header and body cell,
  estimates wrap-aware column demand, and supplies the resulting proportions to website, PDF, and
  DOCX rendering without table-specific width percentages.
- Added a read-only Markdown width report and a rendered review gallery covering every syllabus
  table at desktop/mobile widths in light and dark themes.
- Added a manifest-owned short course name for compact PDF identification and an ESL-friendly
  assessment guide in the shared overview, before the selected detail fragments. It explains what
  assignments, quizzes, and exams are, why students complete them, and their typical format.
- Added a required, closed `lab_status` manifest choice and one canonical lab-attendance fragment.
  All Fall 2026 courses declare `no_lab`; a future `has_lab` syllabus will include the fragment on
  its course-details page and in its complete documents from the same YAML decision.

### Behavior or Interface Changes

- Clarified that the MkDocs site and generated syllabi are the student-facing boundary. Private
  internal authoring references may remain inside the repository workspace only under ignored
  `raw/`; the publication pipeline still rejects tracked raw files and never reads that directory.
- Marked the conditional CORE Attribute checklist item not applicable for all three Fall 2026
  syllabi after instructor confirmation that CORE applies to general-education courses and these
  are upper-level major courses.
- Marked the conditional program-director checklist item not applicable for all three Fall 2026
  syllabi after instructor confirmation that no program director overlaps those courses. Retained
  the department chair and did not use deans, unrelated directors, advisors, or coordinators as
  checklist evidence.
- Rebuilt the Coursework and grades hierarchy without changing global heading styles. The one
  assessment marker now composes ordered H2 section roots with manifest-derived H3 topics; compact
  overview labels remain bold paragraph lead-ins. Added explicit No quizzes and No exams topics when
  those categories are absent. Consolidated duplicated quiz and online-exam interruption recovery
  under one composite section, with separate selected guidance for timed, unlimited-retry
  assignments and timed Blackboard quizzes or online exams. Removed the exam hand-in checklist
  because it is exam-day direction rather than syllabus content.
- Prose-heavy columns now receive room in proportion to their content, short numeric columns stay
  compact, content-small tables no longer fill the page, and narrow screens retain deliberate
  horizontal scrolling rather than crushing descriptive text.
- Reworked the PDF footer into a quiet 20/60/20 orientation strip: short course name, current
  section or subsection, and compact page count. Removed the repeated segmented rules and full
  course-title repetition.
- Removed lab attendance, preparation, absence, and make-up rules from the shared general-attendance
  policy so students in this semester's lecture-only courses do not receive lab-only instructions.
- Made repeated tables with identical headers share one content-derived width vector within each
  rendered page or document. All seven monthly University important-dates tables now keep aligned
  Date, Event, and Type columns instead of resizing independently from each month's content.
- Shortened the assessment overview to emphasize the differences among assignments, quizzes, and
  exams. Expanded the Assignments detail with the repeated-practice purpose, unlimited retakes,
  typical weekly point range, collaboration, and question-asking guidance used in Blackboard,
  using the instructor's preferred third-person student language.

### Fixes and Maintenance

- Corrected the department-checklist evidence model now that the shared instructor portrait makes
  image alt text applicable, and recognized Biotechnology's project and talking-point formatting
  requirements instead of leaving that suggested item unresolved.
- Rotated the intact 2026-08-28 through 2026-08-26 day blocks into
  `CHANGELOG-2026-08b.md` after the active changelog crossed its 800-line threshold.
- Pruned implementation-specific table-layout assertions and corrected required manifest access,
  import grouping, and helper docstrings after the six-pass code audit.
- Removed the audit-driven assessment-category scenario matrix from permanent pytest coverage.
  Retained the compact ordered-composition test and one-assertion heading-contract tests; full
  rebuild, browser, and rendered-PDF checks remain separate integration and review evidence.
- Refreshed the complete documentation set from current repository evidence. Tightened the README
  newcomer path, install and usage workflows, manifest format contract, roadmap, troubleshooting,
  related-project guide, and concise `AGENTS.md` pointers. Retained the course-schedule Google
  Sheets integration in `docs/TODO.md`; the existing importer covers shared University important
  dates, not the three course schedules.
- Rebuilt the production site and recaptured the three managed README views: the Fall 2026 home
  page, dark-mode Genetics navigation, and Biotechnology project expectations.

### Developer Tests and Notes

- Passed 501 focused department-checklist, Markdown-link, include, syllabus-builder, ASCII, and
  whitespace tests. Rebuilt the strict website and all three PDF and DOCX syllabi, passed
  cross-format include parity, confirmed the laboratory, TRIO SSS, McNair Scholars, STEM Center,
  and English-language resources in every generated syllabus, and verified that the chair memo's
  access codes are absent from tracked and published content.
- Regenerated all three department checklists after the CORE decision. BIOL 318/418 now has 47 of
  53 items resolved with six open, BIOL 351/451 has 48 resolved with five open, and BIOL 480 has 50
  resolved with three open.
- Passed 492 focused Markdown-link, include, syllabus-builder, ASCII, and whitespace tests. Rebuilt
  the strict website and all three PDF and DOCX syllabi, passed cross-format include parity, and
  confirmed Joshua Campbell's listing in every generated syllabus document.
- Regenerated all three Markdown and DOCX department checklists, confirmed each contains all 53
  source items, verified the DOCX archives and text extraction, and passed 446 focused checklist,
  Markdown-link, ASCII, and whitespace tests plus `git diff --check`.
- A fresh six-pass structural audit found no code, test, style, legacy, or comment issues and one
  low-severity documentation mismatch. Updated the architecture, decision, format, and changelog
  wording to distinguish selected-category topics from absence-derived No quizzes and No exams
  topics, then reran the 1,269-test fast lane.
- `./all_test.sh` passed all 1,269 fast tests, the live Google Sheets refresh, complete PDF/DOCX
  exports, strict MkDocs and include parity, and the Playwright accessibility audit after the
  composite assessment-section redesign. The first restricted-sandbox run reached Chromium but
  macOS denied process-port registration; each subsequent complete gate passed outside that sandbox
  boundary.
- Captured and visually reviewed the rebuilt Coursework and grades policy on all three course
  websites, then rendered the affected Biostatistics, Genetics, and Biotechnology PDF pages. H2
  section boundaries, H3 topics, derived No quizzes and No exams notices, timed assignment retries,
  and limited-attempt recovery remained clear without clipping or footer overlap. Duplicated
  recovery text, the superseded manual Biotechnology absence sentence, and the exam hand-in
  checklist were absent from source and rendered output.
- `./all_test.sh` passed all 1,236 fast tests, the live Google Sheets refresh, complete PDF/DOCX
  exports, strict MkDocs and include parity, and the production Playwright accessibility and
  responsive-overflow audit.
- Captured and visually reviewed all 26 built tables in four browser states (104 renders), plus
  representative table pages from all three rebuilt PDFs. The calculated widths matched the
  rendered proportions without clipping, header collisions, or excessive numeric-column space.
- Confirmed that all seven University important-dates tables use the same Date, Event, and Type
  widths in the website and in each DOCX, then inspected the three PDF pages containing the series.
- Rendered and reviewed the footer strip from all 102 pages across the three current PDFs, then
  rechecked title and assessment-guide pages from the final full-gate build. Short names, current
  headings, and page counts remained legible and separate without footer/content overlap.
- Refreshed the coordinated documentation set and passed all 1,231 fast tests, both live build
  cycles, complete PDF/DOCX export and include parity, strict MkDocs, and Playwright through a
  disposable alternate index used during the documentation audit. The real Git index remained
  untouched.
- Confirmed all eight live links in the README and related-project guide. Recaptured and visually
  reviewed the three 1440 by 900 README screenshots; a repeat capture produced identical files.

## 2026-08-30

### Behavior or Interface Changes

- Turned each course landing page's "Find what you need" list into a named, responsive contents
  navigation with full-card links, descriptive text, visible focus, and touch-sized targets.

### Fixes and Maintenance

- Synchronized shared style guides, tests, and repository support files from the starter template.

### Developer Tests and Notes

- `./all_test.sh` passed 1,180 fast tests, the live Google Sheets refresh, all PDF and DOCX
  exports, strict MkDocs, include parity, and the Playwright accessibility and interaction audit.
- A first restricted-sandbox run reached the browser phase but macOS denied Chromium's process
  port registration. The identical full gate passed outside that sandbox boundary.
