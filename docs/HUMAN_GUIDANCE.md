# Human guidance

This file records only durable guidance that I, Neil Voss, explicitly state or approve. Keep the
wording in first person or as a close paraphrase of my decision. Do not add manager or agent
interpretations, implementation inventories, inferred preferences, review findings, or task
history. Those belong in the appropriate technical documentation or changelog.

## Audience and content

- This website is for my students. Favor student-facing language and navigation over maintainer or
  publication-system concepts.
- Make the repository reflect my actual syllabi and teaching practice, not a generic university
  course template.
- Keep the repository and public website free of credentials, private meeting information, student
  information, and access-controlled course material. Blackboard is the home for private content.
- I want shared syllabus information edited once, not copied among courses or maintained in a
  parallel template tree.

## Presentation

- Use Roosevelt University's green palette for the main website and favicon because Roosevelt is
  my employer.
- Keep the favicon protein-themed and use the three greens from Roosevelt University's R logo.
- Use the protein favicon as the MkDocs header logo in Material's standard upper-left position,
  replacing the default book mark.
- Provide a student-accessible light and dark theme toggle.
- Avoid CSS specificity arms races. Keep style ownership and the cascade easy to understand.
- Use subtle course color themes across headings and tables. Keep level-one headings left-aligned,
  bold, and in small caps; keep level-two headings bold and slightly left-shifted, with a separate
  paragraph-width accent rule below instead of a text underline; keep level-three headings bold and
  aligned with body paragraphs; and keep level-four headings italic.
- Keep term-level PDF and DOCX links small and directly below their course instead of giving
  downloads a large standalone section. On both the term overview and course landing pages, pair
  visible file-format labels with small Font Awesome PDF or Word icons rather than relying on
  icon-only links.
- Justify long-form paragraphs at comfortable widths without aggressive automatic hyphenation.
  Return narrow screens to left alignment, and allow emergency wrapping for long URLs and code.
- Keep the heading, paragraph, and table design readable in both MkDocs Material and WeasyPrint,
  while allowing renderer-specific spacing where the formats need it.
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

## Code architecture

- Keep runnable files under `pipeline/` focused on orchestration. Put substantial reusable models,
  composition, validation, and rendering code under `pipeline/build_lib/`; reducing a large entry
  point by only enough lines to stay below the source limit is not structural success.
