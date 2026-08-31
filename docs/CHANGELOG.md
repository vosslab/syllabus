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
- Restored the BIOL 351/451 Genetics of Inheritance course-focus explanation directly after the
  catalog description. It distinguishes inheritance genetics from molecular genetics, explains
  why general Genetics textbooks may emphasize different material, and identifies BIOL 453 as
  Roosevelt's molecular-biology course.

### Behavior or Interface Changes

- Renamed all three "Meetings and instructor" pages and navigation entries to "Course information"
  so their section details, delivery format, catalog description, textbooks and technology, and
  instructor information have an accurate umbrella title. Restored Genetics' established
  face-to-face format paragraph from the original syllabus, separated Biostatistics' confirmed
  hybrid-format prose from its catalog entry, and gave Biotechnology's current flipped hybrid
  format a durable course-format heading.
- Made every public Fall 2026 contact email an explicit `mailto:` link instead of relying on
  renderer-specific detection. Website email links now carry the local Font Awesome envelope icon,
  matching the established link-purpose icon treatment without adding a remote dependency.
- Course-information rows shared by both listed sections now display one value spanning the two
  section columns instead of repeating it. Section-specific values remain side by side, and the
  same rule reaches the website, PDF, and DOCX from the registered table profile.
- Delayed online homework until Week 3 so students have time to create accounts and learn the
  external assessment platform. Kept earlier course-orientation work and Week 2 in-class activities,
  and labeled the Biostatistics figure analysis and BIOL 480 talking point as in-class work.
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
- Made the Fall 2026 delivery formats explicit: Genetics covers the lecture rather than its
  separately registered laboratory; Biostatistics has a one-hour weekly meeting plus mostly
  self-paced Google Sheets tutorials; and BIOL 480 is a flipped, discussion-based graduate course
  rather than an instructor-lecture course. Kept the `no_lab` manifest choice as an internal
  composition decision instead of displaying a none-valued table row.
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

- Removed the explicit `Laboratory component: None` rows from all three course-information tables.
  The Genetics page retains its useful prose explaining that the separately registered laboratory
  is outside the lecture syllabus.
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

- Final `./all_test.sh` passed all 1,316 fast tests, the live-date refresh, strict website and
  PDF/DOCX builds, include parity, and the Playwright browser audit.
- Focused rendered review covered the three Course information pages, learning frameworks,
  schedules, coursework hierarchy, table layouts and spans, PDF footers, email-link icons, and the
  managed README screenshots. Department checklists and DOCX structure were also regenerated and
  inspected where their source changes required it.

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
