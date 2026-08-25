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
- Snapshot a completed term only when the term closes, before creating the next live term.
- Keep course-specific details, assignments, schedules, and learning statements in their course
  folders while drawing shared facts and policies from canonical term-level sources.

## Policy organization

- Keep **Policies** and **Student resources** as the two top-level branches of the shared material.
- Split the long policy document into student-recognizable topics such as assessment guidelines,
  grading policies, accommodation policies, conduct and behavioral policies, expectations,
  instructor information, and frequently asked questions.
- Maintain Dr. Voss's course policies once per term in `site_docs/<term>/policies/`; use
  `POLICIES.md` only as the student-facing topic index. Link every course to that shared branch and
  append each topic once to every complete syllabus.
- Maintain the complete letter-grade scale only in `site_docs/<term>/policies/GRADING.md`; course
  pages link to that policy and complete syllabi include it once.
- Keep policies and student resources independently editable and merge both into each complete
  course syllabus during the build.

## Shared information

- Follow an edit-once model. Store any fact shared by multiple courses in one canonical source and
  embed it wherever students need the context.
- Maintain term-wide instructor information, office hours, and Roosevelt learning-goal bullets in
  `site_docs/<term>/shared/`.
- Use Markdown embedding when it makes a course page or complete syllabus easier for a student to
  understand. Reusing a canonical fragment is preferable to omitting useful context.
- Keep tables visually and structurally consistent across the website, PDF, and DOCX outputs. Use
  simple semantic tables with named headers, rectangular rows, and no blank-cell layout grids.

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
- Make every course in the active semester directly accessible from the main page. For Fall 2026,
  show BIOL 318/418, BIOL 351/451, and BIOL 480 without requiring a term-page detour.
- Show future-term and archived-term sections only when real content exists. Add the archive route
  when the first archived term exists rather than displaying a placeholder.
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
