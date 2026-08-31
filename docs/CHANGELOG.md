## 2026-08-31

### Additions and New Features

- Added Joshua Campbell's academic advising role, office, phone, email, and public appointment
  route to the shared Fall 2026 student resources. The shared source makes the advising contact
  available in all three course syllabi.
- Added Dr. Nate La Porte (she/her), BCPS Lab Manager, as the department laboratory contact for
  laboratory access, planning, PPE, safety documents, independent study, and research. Added her
  responsibility for hiring and coordinating teaching assistants, plus her WB 813 office.
- Added a lab-only loaner-PPE procedure that sends students to WB 812 with a laboratory assistant
  and uses a Roosevelt ID as return collateral. Students who forget PPE are no longer dismissed or
  charged a rental fee solely for that mistake; preparation-score expectations remain in place.
- Expanded the existing TRIO SSS resource to cover its current STEM and non-STEM services, student
  benefits, eligibility, and public application page.
- Added student-facing English language support that explains placement referral, student
  self-referral, and an instructor's Navigate Early Alert as paths to tutoring through the Office
  of International Programs.
- Added separate McNair Scholars and Chicago STEM Center resources. The McNair section distinguishes
  its research and graduate-school mission from TRIO SSS and summarizes eligibility, services, and
  contact information; the STEM Center section presents AUD 835 as a tutoring, computer, printing,
  coffee, study, and community space.
- Added Fala's 24-hour call, text, and website-chat route and a Lakers athletics resource covering
  NCAA Division II membership, free student admission to home events with an RU ID, and the public
  team and schedule site. Deferred the temporary 30th-anniversary announcements to the planned
  Schaumburg campus section rather than placing dated events in durable shared resources.
- Added Megan Hoppe, the Schaumburg Research and Instruction Librarian, and their student research,
  materials, and library-instruction support to the requirements for the planned Schaumburg-only
  page. Kept the campus-specific contact out of the current all-course student-resources page.
- Split the 25-heading Help and student services page into one recognition-first overview and six
  task-focused pages for advising, learning, programs, technology, essential needs, and health.
  Added every topic to MkDocs navigation, all three course manifests, complete PDF/DOCX syllabi,
  and the browser accessibility route audit.
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
- Added [BIOLOGY_MAJOR_COMPETENCIES.md](BIOLOGY_MAJOR_COMPETENCIES.md) as a tracked, non-MkDocs
  reference for the six Vision and Change/PULSE competency areas, the Roosevelt course-numbering
  levels, and Fall 2026 mappings. Public course-information tables now contain only the applicable
  labels: BIOL 318 has Applying the Process of Science and Quantitative Reasoning, and the BIOL 351
  lecture has Quantitative Reasoning and Communication and Collaboration. Graduate BIOL 418,
  BIOL 451, and BIOL 480 identify the undergraduate mapping as not applicable.
- Expanded every Fall 2026 course learning framework using stable course-specific evidence from
  ignored `raw/` materials. Biostatistics and Biotechnology now have six substantive objectives,
  outcomes, and goals each; Genetics preserves its detailed 17 outcomes and seven goals while
  adding the two objectives needed for six. Restored the canonical colon-bearing section titles
  and their distinct objective, outcome, and goal lead-in sentences.

### Behavior or Interface Changes

- Restored the Genetics schedule's five numbered quiz-coverage groups and Assignments 1-13 due
  labels from the historical online schedule. Matching topic and quiz cells use the original light
  surfaces (`#f4cccc`, `#d9ead3`, `#ffe599`, `#fce5cd`, and `#d9d2e9`) plus measured 7:1 dark-theme
  companions; repeated quiz numbers keep color supplementary. Kept assessments and assignments in
  one compact due column and aligned all five quiz dates with the confirmed point plan.
- Rewrote the STEM Center, TRIO Student Support Services, McNair Scholars, English language support,
  and Career Services descriptions as compact paragraphs instead of short bullet lists. Preserved
  the services, eligibility details, links, and contact information while making the shared page
  read more like a student guide.
- Removed Blackboard as an assignment, quiz, and exam delivery platform throughout the live
  syllabi. Blackboard now owns course information, private links, and the gradebook; assessment
  directions remain platform-neutral while LibreTexts ADAPT and the Peptidyle Learning Engine are
  under consideration.
- Qualified the STEM Center's peer-tutoring description: departmental tutoring covers selected
  introductory and lower-level courses rather than the current 300/400-level courses, while AUD 835
  remains available for studying, computers, printing, coffee, and community. Kept term-specific
  schedules in Blackboard and recorded Spring tutor recruitment as a confirmation-dependent task.
- Clarified that the MkDocs site and generated syllabi are the student-facing boundary. Private
  internal authoring references may remain inside the repository workspace only under ignored
  `raw/`; the publication pipeline still rejects tracked raw files and never reads that directory.
- Corrected the conditional CORE Attribute review to follow official section listings and course
  level. BIOL 351-24A identifies and links its Natural Science CORE attribute, BIOL 318 has no CORE
  attribute listed, and graduate BIOL 418, BIOL 451, and BIOL 480 identify undergraduate CORE as
  not applicable. Updated the Genetics checklist from not applicable to covered without changing
  its resolved-item total. Kept official attribute reporting separate from assumptions about
  students or degree use.
- Made the Fall 2026 delivery formats explicit: every current syllabus has no laboratory component;
  Genetics covers the lecture rather than its separately registered laboratory; Biostatistics has
  a one-hour weekly meeting plus mostly self-paced Google Sheets tutorials; and BIOL 480 is a
  flipped, discussion-based graduate course rather than an instructor-lecture course.
- Replaced the proposed fixed feedback-turnaround promise with the actual update schedule.
  Automatically graded assignments return scores on their platform after submission, and those
  grades are transferred manually to the Blackboard gradebook at midterm and semester end. Quiz
  and exam feedback follows the close of approved testing arrangements. BIOL 480's dated project
  sequence additionally identifies when students receive and apply project feedback.
- Marked the conditional program-director checklist item not applicable for all three Fall 2026
  syllabi after instructor confirmation that no program director overlaps those courses. Retained
  the department chair and did not use deans, unrelated directors, advisors, or coordinators as
  checklist evidence.
- Rebuilt the Coursework and grades hierarchy without changing global heading styles. The one
  assessment marker now composes ordered H2 section roots with manifest-derived H3 topics; compact
  overview labels remain bold paragraph lead-ins. Added explicit No quizzes and No exams topics when
  those categories are absent. Consolidated duplicated quiz and online-exam interruption recovery
  under one composite section, with separate selected guidance for timed, unlimited-retry
  assignments and timed online quizzes or exams. Removed the exam hand-in checklist
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
  typical weekly point range, collaboration, and question-asking guidance used in online work,
  using the instructor's preferred third-person student language.

### Fixes and Maintenance

- Updated department references after the former Biological, Physical and Health Sciences unit
  split into Biological and Physical Sciences and Health Sciences. Current Biology leadership now
  names Biological and Physical Sciences, while academic-advisor descriptions stay general rather
  than presenting obsolete directory titles as current.
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
- Reduced the Fall 2026 syllabus audit to a short unresolved-action list. Removed completed
  leadership, CORE, competency, and accessibility explanations while retaining current open counts,
  direct edit targets, and rebuild commands.
- Rebuilt the production site and recaptured the three managed README views: the Fall 2026 home
  page, dark-mode Genetics navigation, and Biotechnology project expectations.

### Developer Tests and Notes

- Passed all 1,314 fast tests, rebuilt the strict website and all three PDF/DOCX syllabi, passed
  cross-format include parity, and passed the Playwright browser accessibility audit. Visually
  reviewed pages 5-7 of each rebuilt PDF; all three canonical learning sections remain distinct,
  readable, and free of clipping or footer overlap.
- Passed all 1,314 fast tests through a disposable projected Git index without changing the real
  index. Rebuilt the strict website and all PDF/DOCX syllabi, passed cross-format include parity and
  the Playwright accessibility audit, and visually reviewed the Genetics schedule in four browser
  states plus both rendered PDF pages. `tools/calculate_table_widths.py` reported a 75ch schedule
  with 11/20/40/29 percent Week, Date, Topic, and Due-this-date columns.
- Passed all 1,284 fast tests, including department-checklist, Markdown-link, include,
  syllabus-builder, ASCII, and whitespace coverage. Rebuilt the strict website and all three PDF
  and DOCX syllabi, passed cross-format include parity, and regenerated all three department
  checklists.
- Confirmed that the complete six-area Biology competency reference is absent from MkDocs while the
  BIOL 318 and BIOL 351 labels appear in their website, PDF, and DOCX course-information tables.
  Confirmed graduate not-applicable labels in BIOL 418, BIOL 451, and BIOL 480 and verified the
  Natural Science CORE label in the Genetics outputs.
- Regenerated all three department checklists after documenting feedback timing. BIOL 318/418 now
  has 48 of 53 items resolved with five open, BIOL 351/451 has 49 resolved with four open, and
  BIOL 480 has 51 resolved with two open.
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
