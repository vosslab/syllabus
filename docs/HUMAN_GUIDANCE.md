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
- Provide a student-accessible light and dark theme toggle.
- Avoid CSS specificity arms races. Keep style ownership and the cascade easy to understand.
- Use my student-appropriate social links in the footer. Do not include PayPal, Patreon, or other
  donation links.
- Keep the public GitHub Pages link prominent in the README.

## Publication and validation

- I want GitHub Pages builds to succeed when the production artifact can be generated, uploaded,
  and deployed. Do not make pytest, export E2E, Playwright, or their semantic findings CI release
  gates; enforce those expectations through local maintainer checks.
- `all_test.sh` means all local validation. It must include the live Google Sheets build as well as
  pytest, export E2E, and Playwright.
