# Syllabus site interaction brief

## Primary users and tasks

| User | High-value task | Required outcome |
| --- | --- | --- |
| Student | Find current course expectations quickly | Short pages with clear local navigation |
| Student using assistive technology | Read tables, headings, and links | Semantic structure and keyboard access |
| Instructor | Update one fact without duplicating policy text | Section files plus ordered manifests |
| Department archivist | Preserve the complete syllabus | One complete DOCX/PDF pair per course |

The site supports lookup first and continuous reading second. A student should not need to scroll a
30-page web page to find a deadline or grading rule. The complete documents remain available for
offline reading and archival use.

## Interaction decisions

- Organize navigation by term, course, and task-oriented section.
- Label visible routes with student questions and tasks while keeping technical filenames internal.
- Keep policies and student resources on separate pages and append both to complete exports.
- Place task-oriented course links immediately after the introduction.
- Place secondary complete PDF and DOCX links after the course summary and label them as complete
  course-syllabus downloads.
- Self-host Atkinson Hyperlegible Next for proportional website text while preserving a monospace
  stack for code and identifiers.
- Use at least 17-pixel course text and 16-pixel navigation text at the standard browser zoom.
- Render tables and notices at the full course-text size, with horizontal scrolling for wide tables
  on narrow screens.
- Use literal schedule dates so a human reviews every academic-calendar exception.
- Keep private meeting links and credentials in Blackboard.
- Block automatic deployment while any course manifest remains a draft.

## Accessibility baseline

- Target WCAG 2.2 AA behavior and the repository's 5.5:1 text-contrast policy.
- Use one level-one heading per source page and preserve heading order in exports.
- Use real table header rows, repeated DOCX headers, and rows that do not split across PDF pages.
- Use underlined, high-contrast document links and visible keyboard focus on the website.
- Preserve selectable PDF text, document metadata, language, tags, and bookmarks.
- Treat automated checks as advisory defect detectors, not publication gates or certification.

## Evaluation priorities

1. Verify the correctness and completeness of course content with the instructor.
2. Complete the site and export workflows using keyboard-only navigation.
3. Inspect mobile tables and download controls at narrow viewport widths.
4. Check headings, tables, links, and reading order with a screen reader.
5. Render representative pages from each long PDF and inspect every wide table.

Formal PDF/UA conformance and legal-compliance certification are outside the current claim. Any
reported student barrier takes priority over visual refinement.
