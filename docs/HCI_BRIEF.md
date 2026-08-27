# Syllabus site interaction brief

## Primary users and tasks

| User | High-value task | Required outcome |
| --- | --- | --- |
| Student | Find current course expectations quickly | Short pages with clear local navigation |
| Student using assistive technology | Read tables, headings, and links | Semantic structure and keyboard access |
| Instructor | Update one shared fact without finding copies | Canonical topic files and embedded fragments |
| Department archivist | Preserve the complete syllabus | One complete DOCX/PDF pair per course |

The site supports lookup first and continuous reading second. A student should not need to scroll a
30-page web page to find a deadline or grading rule. The complete documents remain available for
offline reading and archival use.

## Interaction decisions

- Make the active semester and its three course choices the homepage's dominant content. A student
  reaches a course in one click without first opening a term overview.
- Put each complete PDF and DOCX directly below its course on both the homepage and term overview.
  Render both entry points from one shared term fragment so their choices cannot drift apart.
- Show archive navigation only after an archived syllabus actually exists.
- Explain Blackboard in terms of the private materials students should expect to find there,
  rather than using an unexplained security-oriented heading.
- Organize navigation by term, course, and task-oriented section.
- Use subject-based course paths so cross-listed students recognize the course topic without one
  section number appearing to own the shared route.
- Use conventional syllabus labels that tell students exactly what each route contains while
  keeping technical filenames internal.
- Keep directly navigable term-wide material together under `shared/`, with policy topics grouped
  under `shared/policies/` and include-only content under `shared/fragments/`. Split Dr. Voss's
  long policy document into recognizable topic pages without creating course-specific alternatives
  or a second overview.
- Use instructor-facing subject names for canonical files and student-facing task language for
  page headings and navigation. Students should recognize the question a page answers without
  knowing terms such as **assessment** or **course delivery**.
- Embed instructor contact details and Roosevelt learning goals from canonical term-level
  fragments. Keep the directly navigable instructor-information page as a student-facing wrapper
  around the same contact fragment used by course-details pages.
- Keep the letter-grade scale once in the shared grading policy; course grading pages link to it.
- Place task-oriented course links immediately after the introduction.
- Place secondary complete PDF and DOCX links after the course summary and label them as complete
  course-syllabus downloads.
- Self-host Atkinson Hyperlegible Next for proportional website text while preserving a monospace
  stack for code and identifiers.
- Use at least 17-pixel course text and 16-pixel navigation text at the standard browser zoom.
- Render tables and notices at the full course-text size, with horizontal scrolling for wide tables
  on narrow screens.
- Use literal schedule dates so every academic-calendar exception remains explicit and reviewable.
- Keep private meeting links and credentials in Blackboard.
- Present complete student-facing candidates; keep editorial uncertainty outside published pages.

## Policy information architecture

The policy overview supports recognition rather than recall: students scan visible task labels,
then choose the page that matches their question. Each subsection belongs to one subject category;
`shared/policies/index.md` is the only overview and the policy branch has no catch-all FAQ.

| Canonical category | Student-facing page | Student question answered |
| --- | --- | --- |
| `INSTRUCTOR_INFORMATION.md` | Contacting Dr. Voss | How and when do I contact the instructor? |
| `COURSE_DELIVERY.md` | Course format and online tools | Where and how does the course operate? |
| `ASSESSMENT.md` | Grades and graded work | How are assignments, quizzes, exams, and grades handled? |
| `DISCUSSION_MARKS.md` | Discussion marks | How is live participation recognized and scored? |
| `EXTRA_CREDIT.md` | Extra credit write-ups | What can earn extra credit, and how do I submit it? |
| `EXTRA_CREDIT_MOVIES.md` | Approved science movies | Which movies may I use for extra credit? |
| `ATTENDANCE_AND_ACCOMMODATIONS.md` | Attendance, absences, and accommodations | What happens if I miss class or need an accommodation? |
| `ACADEMIC_INTEGRITY.md` | Academic integrity and AI | What work must be my own, and how may I use AI? |
| `COURSE_EXPECTATIONS.md` | What students and instructors can expect | What responsibilities and classroom behavior are expected? |
| `INCLUSION_AND_SAFETY.md` | Safety, inclusion, and belonging | What protections, reporting routes, and community commitments apply? |
| `COURSE_ENROLLMENT.md` | Dropping or withdrawing from class | How do withdrawal, late withdrawal, and tuition refunds work? |

The inspection scenario starts at the policy overview with one of those questions. Success means
the matching link is recognizable without opening competing pages, its target contains the answer,
and the same category appears once in each complete syllabus.

## Task models

### Instructor: update a shared fact

1. Open the topic named for the fact: for example, instructor information or grading policies.
2. Edit the fact once in that canonical source.
3. Build the site and complete syllabi.
4. Confirm that each course view and export reflects the edit.

The normal path never asks the instructor to find or reconcile course-specific copies. Office
hours and Roosevelt learning goals use embedded Markdown fragments. The letter-grade scale lives
directly in the grading policy because every website course page can link there and each complete
syllabus already includes that policy once.

### Student: find authoritative course information

1. Enter the course landing page.
2. Choose a literal, conventional label such as **Learning Objectives, Outcomes, and Goals**,
   **Dr. Voss course policies**, or **Help and student services**.
3. Use the policy topic list when a narrower question remains.

The student should encounter one policy authority, not decide whether a generic per-course page or
Dr. Voss's shared policy branch controls.

## Source-of-truth acceptance criteria

| Need | Acceptance criterion |
| --- | --- |
| Edit office hours once | Exact office-hour times occur only in the term instructor-information fragment |
| Preserve Roosevelt goals | Every course renders the bullets from one term learning-goals fragment |
| Maintain one grade scale | Only the grading-policy source contains thresholds; course pages link to it |
| Find learning statements | Every course exposes all four required sections under the formal page label |
| Find a policy | Navigation uses student-facing task labels and contains no second overview, catch-all FAQ, or competing course policy page |
| Preserve complete syllabi | Each shared policy topic and student-resource source appears once in every export |

## Homepage UX delta

The primary homepage task is **open or download the syllabus for my current course**. The old path
required two links: homepage to term, then term to course or download. The revised path offers each
course page, PDF, and DOCX directly and removes placeholder sections that did not help a Fall 2026
student.

| Nielsen heuristic | Before | After | Evidence |
| --- | ---: | ---: | --- |
| Visibility of system status | 2 | 4 | The page title and opening sentence identify Fall 2026 as active |
| Match with the real world | 2 | 4 | Students see their course codes and titles instead of site-lifecycle labels |
| User control and freedom | 3 | 4 | Every current course is directly selectable from the homepage |
| Consistency and standards | 4 | 4 | Course names match the term page and navigation |
| Error prevention | 3 | 4 | Blackboard content is described before students search the public site for it |
| Recognition rather than recall | 2 | 4 | All current course choices are visible together |
| Flexibility and efficiency | 2 | 4 | Course entry and complete downloads are one link away |
| Aesthetic and minimalist design | 2 | 4 | Future archive copy and the ambiguous access section are removed |
| Error recovery | 3 | 3 | The static landing page has no transactional error state |
| Help and documentation | 2 | 4 | Policies, student services, and Blackboard each have explicit context |

## Accessibility baseline

- Target WCAG 2.2 AA behavior and the repository's 5.5:1 text-contrast policy.
- Use one level-one heading per source page and preserve heading order in exports.
- Use real table header rows, repeated DOCX headers, and rows that do not split across PDF pages.
- Use underlined, high-contrast document links and visible keyboard focus on the website.
- Preserve selectable PDF text, document metadata, language, tags, and bookmarks.
- Treat automated checks as advisory defect detectors, not publication gates or certification.

## Evaluation priorities

1. Verify course-content completeness against tracked sources and current authoritative references.
2. Complete the site and export workflows using keyboard-only navigation.
3. Inspect mobile tables and download controls at narrow viewport widths.
4. Check headings, tables, links, and reading order with a screen reader.
5. Render representative pages from each long PDF and inspect every wide table.

Formal PDF/UA conformance and legal-compliance certification are outside the current claim. Any
reported student barrier takes priority over visual refinement.
