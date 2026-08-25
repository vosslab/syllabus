## 2026-08-25

### Additions and New Features

- Added a minimal MkDocs Material configuration and site homepage.
- Added term-first Fall 2026 pages for BIOL 318/418, BIOL 351/451, and BIOL 480 using the supplied
  section, meeting, prerequisite, and catalog information.
- Added separate shared `POLICIES.md` and `STUDENT_RESOURCES.md` sources plus reusable course and
  term templates.
- Added a manifest-driven `pipeline/build_syllabi.py` exporter, accessible Pandoc reference DOCX,
  tagged PDF conversion, optional term ZIP archives, and the `pipeline/build_site.py` build front
  door.
- Added a GitHub Pages workflow, focused exporter tests, a real export E2E gate, and a
  desktop/mobile Playwright and axe accessibility smoke.
- Added installation, authoring, HCI, contrast-audit, implementation-plan, and Fall 2026 content
  review documentation.
- Added self-hosted Atkinson Hyperlegible Next upright and italic variable WOFF2 files with the SIL
  Open Font License.
- Added a print-specific syllabus stylesheet and WeasyPrint renderer for direct PDF output from
  semantic standalone HTML.
- Added direct Python-Markdown rendering that loads the site's extension configuration from
  `mkdocs.yml`, preserving native admonitions and other configured syntax in PDF HTML.
- Added `HUMAN_GUIDANCE.md` as the canonical record of content-first planning, grounded gates,
  advisory accessibility audits, and permanent-test restraint.
- Added recursive per-course metadata and a small Material theme extension for course-colored web
  headers.

### Behavior or Interface Changes

- Changed the public site source from maintainer `docs/` to `site_docs/` and added explicit
  term/course navigation with complete PDF and DOCX download controls.
- Replaced filename-oriented course links with student-facing task labels such as meetings,
  coursework and grades, dates and topics, class expectations, and help.
- Kept schedule dates as literal Markdown for human review rather than applying automatic date
  shifting.
- Marked all Fall 2026 manifests as drafts so complete exports identify content that still needs
  instructor review.
- Changed Pages deployment to run after every successful `main` build; manifest approval remains a
  record of readiness for student distribution rather than a deployment switch.
- Excluded transient enrollment and wait-list totals from public course content.
- Changed the website's proportional text family to Atkinson Hyperlegible Next while retaining
  Material's system monospace stack for code.
- Moved task-oriented course links directly below each course introduction, expanded them with
  student-facing descriptions and shared support routes, and moved secondary complete-syllabus
  downloads below the course summary.
- Changed complete-document generation to sibling branches from one composed Markdown source:
  Pandoc creates DOCX while Python-Markdown semantic HTML and WeasyPrint create PDF directly.
- Made automated accessibility findings advisory rather than publication-blocking while retaining
  accessibility-oriented markup, PDF tags/outlines, responsive checks, and audit commands.
- Applied dark lime, blue, and brick red web-header identities to the current courses while keeping
  shared pages and complete PDF/DOCX downloads neutral; recorded purple for future BCHM 355 pages.

### Fixes and Maintenance

- Wired the complete export E2E into the Pages workflow so shared-resource, credential-scan, and
  strict-build checks are enforced before artifact upload while PDF tag findings remain advisory.
- Separated the optional Playwright accessibility audit into a non-blocking workflow job so the
  publication build no longer downloads or runs a browser.
- Moved complete-section validation into the exporter, where DOCX and PDF text are checked against
  the headings of their current manifest sources without freezing content wording or page layout.
- Derived required PDF and DOCX overview links from each manifest output name instead of freezing
  one course's download paths in the browser audit.
- Declared Ripgrep in the macOS and CI system dependencies because the enforced export E2E uses it
  for PDF and built-site checks.
- Cleared managed PDF/DOCX downloads before each rebuild and added an E2E regression
  check so obsolete generated syllabi cannot remain in the published site.
- Corrected the active plan to require approval of every course manifest, documented Playwright's
  selector contract, and made the local preview helper open the browser and stop after five minutes.
- Removed repository-level MkDocs version ceilings so dependency installation follows the latest
  mutually compatible stable releases; Material retains its own MkDocs compatibility constraint.
- Completed the interrupted website reset by removing the remaining template-only paths.
- Prevented public source, DOCX, PDF, and built-site output from containing common meeting URL,
  password, passcode, or private invitation patterns.
- Replaced the initial incomplete custom DOCX style model after rendered review exposed blank table
  grids and trailing link artifacts; the final Pandoc-derived model preserves readable tables,
  clickable contents, semantic headers, and page flow.
- Added underlined body links, keyboard-focusable overflow tables, visible focus indicators, and a
  higher-contrast footer color.
- Replaced Material's 12.8-pixel table and notice text with a consistent student-facing type scale:
  at least 17-pixel course content and 16-pixel navigation at standard browser zoom.
- Strengthened the complete PDF heading hierarchy so each linked-page section starts on a new page,
  major headings use a restrained rule and color, and nested headings remain visibly distinct from
  bold paragraph lead-ins.
- Standardized complete PDF page margins at `0.8in` on all four sides.
- Located the project-specific palette report under `docs/active_plans/audits/` because it records
  current implementation evidence rather than permanent repository guidance.
- Removed bytecode caches created by an unnecessary explicit `py_compile` check; normal validation
  continues through the repository environment and test gates.
- Removed suppression of Material's MkDocs 2.0 compatibility warning from the local preview so the
  theme-override migration risk remains visible.
- Linked `AGENTS.md` to durable human guidance and aligned the active plan with the implemented,
  web-only course identity colors.
- Extended the browser audit to verify that course subpages inherit their header identity, current
  course headers remain distinct, and shared pages keep the default header without freezing hex or
  pixel values.
- Updated the Pages workflow to the current major releases of checkout, Python/Node setup,
  configure-pages, artifact upload, and deployment actions while retaining the syllabus-specific
  export and accessibility checks.
- Removed the repository-variable deployment branch after it allowed successful build jobs to skip
  deployment and leave the project URL at GitHub's Pages 404 response.
- Updated both CI jobs to `setup-python@v7` and limited the advisory Playwright installation to
  Chromium's headless shell, reducing browser download weight without changing test behavior.
- Replaced the thin repository README with a content-first landing page that explains the
  one-source website/DOCX/PDF workflow, exposes draft publication status, provides a verified first
  build, demonstrates course organization, and routes newcomers to maintained documentation.

### Removals and Deprecations

- Removed LibreOffice from the export pipeline, Homebrew manifest, installation instructions, and
  GitHub Actions system packages.
- Removed Playwright Chromium from the document-generation path; it remains optional browser audit
  infrastructure.

### Decisions and Failures

- Kept `raw/` as ignored local input and made tracked Markdown the only public source authority.
- Kept the implementation plan active because grading, schedules, artificial-intelligence rules,
  and the applicability of shared assessment policies still require instructor approval.
- Limited the accessibility claim to WCAG 2.2 AA-oriented behavior and tested tagged documents;
  this project does not claim PDF/UA certification or legal compliance.
- Kept accessibility as an actively audited quality goal while reserving blocking build checks for
  credential safety, successful builds, and valid complete downloads.
- Did not adopt ad hoc Prettier output because this repository's tab-based authored style differs
  from Prettier defaults; the enforced whitespace, indentation, and JavaScript checks pass.
- Rejected `mkdocs-print-site-plugin` for production PDF generation after a course-specific probe
  required Material layout overrides, produced a JavaScript-dependent blank contents page, added
  duplicate pagination, and expanded a 28-page direct PDF to 35 pages.
- Measured the local Playwright browser cache at 1.7 GB and LibreOffice at 800 MB; chose WeasyPrint
  with the existing Pango text stack while documenting Pango as a clean-machine dependency.
- Kept Pandoc as the native DOCX generator and limited Material-specific normalization to that
  branch; routing Python-Markdown HTML through Pandoc would add an intermediate format without
  improving Word structure.
- Classified academic approval as a student-distribution review and credential safety, complete
  valid outputs, and the strict site build as durable build gates; kept accessibility heuristics
  repeatable but advisory and recorded exact page counts, package versions, and rendered
  comparisons as implementation evidence.
- Removed fixed minimum-pixel and exact-font-face-count browser assertions, exact download paths,
  and a table-of-contents-dependent heading count because they constrained implementation details
  rather than stable student-visible behavior.
- Kept shared-environment `pip check` output as diagnostic evidence rather than a repository gate;
  it reports unrelated Torch and Qwen package conflicts while this repository's build and imports
  pass their focused checks.
- Replaced the proposed BIOL 318/418 lime after measurement showed 4.10:1 contrast with white; the
  darker hue-preserving value reaches 5.53:1.
- The independent audit identified non-atomic replacement of generated downloads as an unresolved
  failure-mode risk; a durable fix must stage and validate all outputs before replacing the current
  download set.
- The independent audit found that manifest `status` accepts `current` or `archived` but does not
  yet change behavior; removal or real archive semantics remains an explicit design decision.

### Developer Tests and Notes

- `source source_me.sh && python3 -m pytest tests/` passed: 458 tests.
- `source source_me.sh && python3 -m mkdocs build --strict` completed successfully.
- `source source_me.sh && python3 -m pytest tests/` passed: 729 tests.
- `source source_me.sh && python3 -m pytest tests/` passed: 743 tests.
- `source source_me.sh && python3 -m pytest tests/` passed: 749 tests with Python-Markdown 3.10.3
  and pypdf 6.16.2.
- `bash tests/e2e/e2e_syllabus_export.sh` built all direct PDF and DOCX outputs, passed content and
  credential checks, and completed a strict MkDocs build.
- `npm run test:playwright` passed desktop/mobile axe, viewport, content-order, download-label,
  keyboard-focus, local-font, typography, and course-header inheritance audits.
- The direct PDFs contain 27, 28, and 28 US-letter pages; all report `Tagged: yes`, provide
  multi-level heading bookmarks and page numbers, embed Atkinson Hyperlegible Next, and retain
  selectable text.
- Rendered inspection of title/contents, grading and schedule tables, native admonitions, shared
  policies, and the final resource page found no clipping, overlap, broken tables, missing glyphs,
  or unreadable text.
- Measured authored text pairs range from 5.53:1 to 12.19:1, meeting or exceeding the 5.5:1
  house target.
