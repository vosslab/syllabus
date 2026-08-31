## 2026-08-31

### Additions and New Features

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

- Rotated the intact 2026-08-28 through 2026-08-26 day blocks into
  `CHANGELOG-2026-08b.md` after the active changelog crossed its 800-line threshold.
- Pruned implementation-specific table-layout assertions and corrected required manifest access,
  import grouping, and helper docstrings after the six-pass code audit.
- Refreshed the complete documentation set from current repository evidence. Tightened the README
  newcomer path, install and usage workflows, manifest format contract, roadmap, troubleshooting,
  related-project guide, and concise `AGENTS.md` pointers. Retained the course-schedule Google
  Sheets integration in `docs/TODO.md`; the existing importer covers shared University important
  dates, not the three course schedules.
- Rebuilt the production site and recaptured the three managed README views: the Fall 2026 home
  page, dark-mode Genetics navigation, and Biotechnology project expectations.

### Developer Tests and Notes

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
