# Human guidance

<!-- VENDORED HEADER: START -->
Record the durable guidance Neil Voss states, in his own words: first person, one to three lines per
bullet. Material he supplies as a source may inform [DESIGN_DECISIONS.md](DESIGN_DECISIONS.md) once
it is settled. Rules: [REPO_STYLE.md](REPO_STYLE.md). [PROPAGATED HEADER - ENTRIES BELOW ARE YOURS]
<!-- VENDORED HEADER: END -->

This file records only durable guidance that I, Neil Voss, explicitly state or approve. Keep the
wording in first person or as a close paraphrase of my decision. Do not add manager or agent
interpretations, implementation inventories, inferred preferences, review findings, or task
history. Those belong in the appropriate technical documentation or changelog.

## Audience and content

- This website is for my students. Favor student-facing language and navigation over maintainer or
  publication-system concepts.
- Direct the syllabus to students as its audience, even though they are the people least likely to
  read it.
- Treat source page filenames as the concise instructor titles used for generated-document
  navigation. Keep the Markdown headings as student-facing titles, and derive the instructor
  titles mechanically instead of maintaining a separate mapping.
- Make the repository reflect my actual syllabi and teaching practice, not a generic university
  course template.
- Keep the repository and public website free of credentials, private meeting information, student
  information, and access-controlled course material. Blackboard is the home for private content.
- I want shared syllabus information edited once, not copied among courses or maintained in a
  parallel template tree.
- Assignments, group quizzes, face-to-face exams, and online exams are my four assessment
  categories. Keep them as separate shared fragments, with each course YAML selecting only the
  categories used in that course.
- Put my "memorization is not learning" pedagogy on every assessment page. Emphasize using
  scientific knowledge to think, reason, analyze, and communicate instead of regurgitating facts.
- Link each assessment page to sample problems on my official Biology Problems OER. Use its
  biotechnology, genetics, biostatistics, or biochemistry subject route for the matching course.
- Give each course its own Discussion marks page selected from no discussion, face-to-face
  discussion, or remote/video-conference discussion. Share the criticism, scoring, and no-make-up
  wording between the two modes that award marks.
- Keep the complete extra-credit guide and approved science-movie list in this repository instead
  of making students depend on Google Docs.
- Keep the approved science-movie list in a global website-only location outside the active term.
  Link to it from Extra credit, but exclude the niche, verbose catalog from course PDF and DOCX
  syllabi.

## Presentation

- Use Roosevelt University's green palette for the main website and favicon because Roosevelt is
  my employer.
- Keep the favicon protein-themed and use the three greens from Roosevelt University's R logo.
- Use the protein favicon as the MkDocs header logo in Material's standard upper-left position,
  replacing the default book mark.
- Provide a student-accessible light and dark theme toggle.
- Explain the Atkinson Hyperlegible Next choice in the student-facing syllabus and link to an
  English source about the font's accessibility purpose.
- Avoid CSS specificity arms races. Keep style ownership and the cascade easy to understand.
- Use subtle course colors across headings and tables. Use bold, left-aligned small-caps H1s; bold,
  slightly left-shifted H2s with a paragraph-width accent rule instead of a text underline;
  body-aligned bold H3s; and italic H4s.
- Keep term PDF and DOCX links small below each course, never in a large standalone section. Reuse
  one shared course-and-download list on both overview pages. Elsewhere, pair visible format labels
  with small Font Awesome PDF or Word icons instead of using icon-only links.
- Justify long-form paragraphs at comfortable widths without aggressive automatic hyphenation.
  Return narrow screens to left alignment, and allow emergency wrapping for long URLs and code.
- Keep the heading, paragraph, and table design readable in both MkDocs Material and WeasyPrint,
  while allowing renderer-specific spacing where the formats need it.
- Put the shared important dates near the end of every complete course document, before student
  resources. Use level-three month headings without divider rules, and give each month's table a
  restrained version of its spreadsheet color.
- Use my student-appropriate social links in the footer. Do not include PayPal, Patreon, or other
  donation links.
- Keep the public GitHub Pages link prominent in the README.

## Publication and validation

- I want GitHub Pages builds to succeed when the production artifact can be generated, uploaded,
  and deployed. Do not make pytest, export E2E, Playwright, or their semantic findings CI release
  gates; enforce those expectations through local maintainer checks.
- `all_test.sh` means all local validation. It must include the live Google Sheets build as well as
  pytest, export E2E, and Playwright.
- Treat implementation-time and rebuild-only probes as one-time evidence. Keep a test permanently
  only when it satisfies the durable-test checklist in `PYTEST_STYLE.md`; when in doubt, remove it.
- Treat tests as evidence for intended product behavior, not as requirements that justify hacky
  production changes. When a test drives an otherwise-unwanted workaround, remove or redesign the
  test unless an independent user need or durable contract supports the production change.
- Review test plans against `REPO_STYLE.md`, `PYTEST_STYLE.md`, `tests/TESTS_README.md`,
  `devel/DEVEL_README.md`, and relevant style docs. Before implementation, reject fragile or
  unnecessary tests, extraneous fixtures, networked fast tests, and misplaced files.
- I do not actively monitor agent chats. Finish obvious, safe, evidence-backed follow-through and
  validation without waiting for routine confirmation. Stop only when the next action is risky,
  requires new authority, or would materially change the requested outcome.

## Code architecture

- Keep runnable files under `pipeline/` focused on orchestration. Put substantial reusable models,
  composition, validation, and rendering code under `pipeline/build_lib/`; reducing a large entry
  point by only enough lines to stay below the source limit is not structural success.
