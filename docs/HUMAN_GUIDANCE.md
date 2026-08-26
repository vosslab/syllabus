# Human guidance

## Syllabus authority

- Make the repository reflect Dr. Voss's actual syllabi and teaching practice, not a generic
  university-course template.
- Treat supplied public-safe source syllabi as semantic evidence. Preserve intentional labels,
  distinctions, and requirements even when they appear repetitive to a developer.
- Keep this repository public-only. Do not store credentials, meeting links, private invitations,
  student information, access-controlled content, or private raw sources anywhere in the tree,
  including ignored paths.
- Label instructor-authored requirements as **Dr. Voss course policies**. Use **University
  policies** only for material that is genuinely an institutional Roosevelt University policy.
- Maintain one shared policy authority for all of Dr. Voss's courses. Do not create competing
  course-specific policy documents that ask students or maintainers to reconcile two versions.
- Treat the active term under `site_docs/` as the only live content authority. Do not maintain a
  parallel Markdown template tree or a future-term copy during the active term.
- During Fall 2026, do not create an archived-term source tree. Defer archive design and the first
  historical rollover until Spring 2027.
- Generate `site_docs/downloads/`, `site/`, and `output/` from the live Markdown. Never edit or
  commit generated output as a competing content source.
- Keep course-specific details, assignments, schedules, and learning statements in their course
  folders while drawing shared facts and policies from canonical term-level sources.
- Use subject-based course-directory slugs: `biostats` for BIOL 318/418, `genetics` for BIOL
  351/451, and `biotech` for BIOL 480. Keep official course numbers in student-facing headings,
  section information, manifest metadata, and download names rather than directory paths.

## Policy organization

- Keep public term-wide pages under `site_docs/<term>/shared/`, with policy categories grouped under
  `shared/policies/` and reusable include-only Markdown grouped under `shared/fragments/`.
- Name canonical policy files with instructor-facing subject categories while giving each page a
  student-facing title. For example, `ASSESSMENT.md` appears to students as **Grades and graded
  work**, following the same pattern as `COURSE_LEARNING_FRAMEWORK.md` and **Learning Objectives,
  Outcomes, and Goals**.
- Keep `shared/policies/index.md` as the only policy overview. Do not add a second overview or a
  catch-all FAQ; assign every policy subsection to one subject category.
- Organize the shared policy branch around instructor communication, course delivery, assessment,
  attendance and accommodations, academic integrity, course expectations, inclusion and safety,
  and course enrollment.
- Maintain Dr. Voss's course policies once per term in `site_docs/<term>/shared/policies/`; use
  `shared/policies/index.md` only as the student-facing topic index. Link every course to that
  shared branch and append each topic once to every complete syllabus.
- Maintain the complete letter-grade scale only in
  `site_docs/<term>/shared/policies/ASSESSMENT.md`; label that route **Grades and graded work** for
  students. Course pages link to that source and complete syllabi include it once.
- Keep policies and student resources independently editable and merge both into each complete
  course syllabus during the build.

## Shared information

- Follow an edit-once model. Store any fact shared by multiple courses in one canonical source and
  embed it wherever students need the context.
- Maintain directly navigable term-wide pages for important dates, instructor information, and
  student resources in `site_docs/<term>/shared/`.
- Maintain the canonical instructor contact body and Roosevelt learning-goal bullets under
  `site_docs/<term>/shared/fragments/`. Keep the public
  `site_docs/<term>/shared/INSTRUCTOR_INFORMATION.md` page as a heading wrapper around the contact
  fragment, and embed that fragment in course-details pages.
- Use Markdown embedding when it makes a course page or complete syllabus easier for a student to
  understand. Reusing a canonical fragment is preferable to omitting useful context.
- Keep tables visually and structurally consistent across the website, PDF, and DOCX outputs. Use
  simple semantic tables with named headers, rectangular rows, and no blank-cell layout grids.
- Treat the first worksheet of the Fall 2026 important-dates Google Sheet as the current source for
  the important-dates page. Every complete site build must refresh the ignored table fragment and
  fail rather than publish stale dates when the source is unavailable. Confirmation, calculated
  week, and notes are personal semester-update aids, and the `X` formula exists only to gray past
  rows in Google Sheets. Validate those source cells but do not publish them in Markdown.

## Learning framework

- Include all four distinct learning-statement sections in every course, in this order:
  1. **Roosevelt learning goals**, presented as bullet points.
  2. **Learning Objectives**, introduced by "Students completing this course will have achieved:"
  3. **Course Learning Outcomes**, introduced by "Students completing this course will be able to:"
  4. **Learning Goals**, introduced by "Overall, this course aims to accomplish:"
- Preserve each original list even when the objectives, outcomes, and goals appear redundant. They
  represent different expected statements and are not interchangeable.
- Name the source `COURSE_LEARNING_FRAMEWORK.md` and use **Learning Objectives, Outcomes, and
  Goals** as its conventional student-facing title.

## Student experience

- Design navigation and labels for students rather than exposing repository, publication, or
  system-administration concepts.
- Link to a readable parent page instead of directly to a PDF when both are available. A link
  should not unexpectedly open or download a PDF.
- Make every course in the active semester directly accessible from the main page. For Fall 2026,
  show BIOL 318/418, BIOL 351/451, and BIOL 480 without requiring a term-page detour.
- Keep future-term and archive navigation absent during Fall 2026. Add archive routes only after
  the Spring 2027 rollover defines and creates the first historical snapshot.
- Explain Blackboard as the location for private meeting links, assignments, grades, and course
  announcements. Use that concrete context instead of an unexplained **Secure course access**
  label.
- Give students one obvious policy authority and short task-oriented pages, while retaining the
  complete PDF and DOCX syllabi for continuous reading and archival use.

## Review priorities

- Apply "Focus on important issues" from [REPO_STYLE.md](REPO_STYLE.md): prioritize content,
  correctness, maintainability, validation, and delivery over cosmetic details.
- Treat security as a narrow static-site boundary rather than the primary design concern. Enforce
  the absolute prohibition on credentials and private content, then focus review time on student
  content, maintainability, validation, and delivery.
- Promote accessibility through semantic source, readable output, and regular audits without
  making every accessibility heuristic a publication gate.
- Verify that every table renders as a table in the website, PDF, and DOCX; literal Markdown pipes
  or prose captured inside a table are release defects.

## Plans and validation

- Make every milestone completable by the manager and subagents without waiting for human input.
  Capture decisions in canonical sources, fixtures, explicit defaults, synthetic state transitions,
  debug harnesses, or automated behavior tests.
- Produce a complete, polished candidate using the best repository and authoritative-source
  evidence available. Do not hold back behind generic draft warnings, placeholders, approval flags,
  or review gates merely because a human may refine the content later.
- Record a specific evidence limitation when a fact cannot be recovered. Continue with the best
  defensible assumption unless that assumption would change the requested outcome or create a real
  correctness risk.
- Ground each release gate in a real user, archival, security, or delivery requirement.
- Separate durable publication gates, repeatable advisory audits, and one-time implementation
  evidence.
- Do not require byte, pixel, page-count, timing, or renderer equivalence unless the product has a
  documented need for that exact property.
- Apply the permanent-test checklist in [PYTEST_STYLE.md](PYTEST_STYLE.md). Prefer deleting a
  fragile test over preserving an implementation detail.
- Keep temporary experiments and rendered comparisons out of the permanent suite. Record useful
  conclusions in the changelog or an active-plan audit.

## Course identity colors

- Use course colors as a restrained web-header cue while keeping page bodies and downloaded
  documents neutral.
- Use dark lime `#477427` for BIOL 318/418, blue `#1565c0` for BIOL 351/451, brick red `#9e3d32`
  for BIOL 480, and purple `#7b1fa2` for BCHM 355.
- Preserve at least 5.5:1 contrast between course headers and white header text or controls.
