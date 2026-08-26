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
- Added restricted Markdown fragment embedding so instructor information and Roosevelt learning
  goals can appear in course context while remaining editable once per term.
- Added a canonical term-level letter-grade scale so every course and the grading-policy page use
  the same editable table.
- Added staged download publication so every PDF/DOCX pair is built and validated before current
  managed downloads are replaced.
- Added behavior checks that reject incomplete staged download sets, private `raw/` trees, and
  unfinished editorial markers in the built student site.

### Behavior or Interface Changes

- Removed the parallel Markdown and manifest template tree; the active term under `site_docs/` is
  now the only live syllabus authority.
- Made `site_docs/fall_2026/policies/GRADING.md` the sole source for the shared letter-grade scale;
  course grading pages and the FAQ now link to that policy instead of repeating its thresholds.
- Stopped tracking generated PDF and DOCX downloads under `site_docs/downloads/`, added the
  directory to the ignore policy, and moved the DOCX renderer reference beside the export pipeline.
- Documented the complete source-to-output boundary: active-term Markdown is authoritative, while
  website, PDF, DOCX, and ZIP artifacts are regenerated outputs rather than editable copies.
- Changed the public site source from maintainer `docs/` to `site_docs/` and added explicit
  term/course navigation with complete PDF and DOCX download controls.
- Replaced filename-oriented course links with student-facing task labels such as meetings,
  coursework and grades, dates and topics, class expectations, and help.
- Kept schedule dates as literal Markdown for human review rather than applying automatic date
  shifting.
- Made every successful Fall 2026 build produce a complete student-facing candidate; incomplete
  content is rejected by the automated publication gates rather than labeled as a draft.
- Changed Pages deployment to run after every successful `main` build; automated publication gates
  define readiness without a separate manifest-approval state.
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
- Replaced the generic per-course policy pages with one shared **Dr. Voss course policies** branch,
  split into instructor information, overview, assessment, grading, accommodations, conduct and
  behavior, expectations, and frequently asked questions.
- Preserved the **Dr. Voss course policies** branch heading in complete documents while omitting
  the landing page's web-only topic and student-support link lists.
- Renamed each learning source to `COURSE_LEARNING_FRAMEWORK.md` and changed its student-facing
  title to **Learning Objectives, Outcomes, and Goals**.
- Restored all four distinct learning sections in every current course and the reusable template:
  Roosevelt learning goals, learning objectives, course learning outcomes, and learning goals.
- Enforced the exact expected learning-section labels and lead-ins, including title-case
  **Learning Objectives**, **Course Learning Outcomes**, and **Learning Goals**.
- Reoriented the homepage around the active Fall 2026 semester and linked BIOL 318/418, BIOL
  351/451, and BIOL 480 directly instead of requiring students to enter a term page first.
- Replaced the unexplained **Secure course access** section with contextual **Blackboard and private
  course materials** guidance.
- Standardized source tables around named columns and simple rectangular rows, with consistent
  full-width grid styling in the website and complete PDF outputs.
- Removed manifest `status` and `publication_status` fields, distribution-warning banners, and the
  separate approval command; every successful build now produces one complete reviewable candidate.
- Replaced draft schedule labels and generic confirmation placeholders with complete student-facing
  schedules; BIOL 318/418 uses **Blackboard assignment** where no more specific public deliverable
  is supported by repository evidence.

### Fixes and Maintenance

- Added a build guard that rejects Markdown or YAML below `templates/`, preventing a second live
  content authority from reappearing.
- Rewrote links between manifest-included Markdown files as internal document anchors so course
  pages can link to one shared policy without breaking the complete PDF and DOCX forms.
- Preserved internal instructor-information links when that canonical content is embedded in course
  details instead of appended as a separate manifest section.
- Made the clean-checkout browser audit generate the ignored syllabus downloads and verify that its
  PDF and DOCX links return successfully before reporting accessibility results.
- Updated authoring, installation, HCI, and durable human guidance with the exact shared-content
  edit locations and the active-term lifecycle.
- Expanded `HUMAN_GUIDANCE.md` with the owner's durable session requirements for syllabus
  authority, shared policies, edit-once content, the four-part learning framework, student-facing
  active-term navigation, contextual Blackboard guidance, and consistent cross-format tables.
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
- Staged and validated the complete managed PDF/DOCX set before replacing current downloads, then
  removed obsolete generated syllabi after successful publication.
- Corrected the active plan to use autonomous publication gates, documented Playwright's selector
  contract, and made the local preview helper open the browser and stop after five minutes.
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
  one-source website/DOCX/PDF workflow, provides a verified first build, demonstrates course
  organization, and routes newcomers to maintained documentation.
- Consolidated exact office hours, contact details, and Roosevelt learning-goal bullets into
  term-level fragments; course pages and the policy branch now render those sources instead of
  maintaining copies.
- Added export validation for the required four-part learning framework and safe include-path
  handling, including rejection of traversal, remote, empty, missing, and nested includes.
- Removed the empty **Archived terms** homepage placeholder until an archived syllabus actually
  exists, and removed generic current/future-term scaffolding from the primary student path.
- Fixed the missed-lab table in complete PDFs by removing an invisible vertical-tab character that
  split its final header cell and caused the pipe-table source to print as literal text.
- Added source validation for hidden line-breaking controls and malformed Markdown tables, output
  table-count checks for PDF HTML and DOCX, browser assertions for the policy tables, and an export
  regression that rejects unrendered pipe rows in PDFs.
- Preserved blank-line boundaries after embedded Markdown fragments so following policy prose
  cannot be interpreted as another table row.
- Reworked the implementation plan and content-refinement report so every milestone has a complete
  manager-and-subagent path through canonical sources and automated behavior checks, without a
  hidden human approval transition.
- Made the repository public-only: private raw syllabi, credentials, meeting links, invitations,
  student information, and access-controlled content are prohibited even in ignored paths.
- Archived the completed MkDocs syllabus-site implementation plan after its autonomous source,
  export, browser, and rendered-document gates passed.

### Removals and Deprecations

- Removed LibreOffice from the export pipeline, Homebrew manifest, installation instructions, and
  GitHub Actions system packages.
- Removed Playwright Chromium from the document-generation path; it remains optional browser audit
  infrastructure.
- Removed the three generic `COURSE_POLICIES.md` pages and their template because they competed
  with the canonical shared Dr. Voss policy branch.

### Decisions and Failures

- Treat the current term as the live editable version. Create a historical snapshot only when the
  term closes, before starting the next live term, rather than maintaining a parallel snapshot.
- Deferred historical-term archive design and the first term rollover until Spring 2027. Fall 2026
  remains the only term source tree; the current `--archive` flag packages generated documents but
  does not establish a second Markdown authority.
- Removed the `raw/` local-input concept and made tracked public Markdown the only repository
  content authority.
- Kept the implementation plan active through autonomous grading, schedule, policy, export, and
  delivery validation; later editorial refinements do not block plan completion.
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
- Replaced an early academic-approval state with durable gates for credential safety, complete
  valid outputs, and the strict site build; kept accessibility heuristics repeatable but advisory
  and recorded exact page counts, package versions, and rendered comparisons as implementation
  evidence.
- Removed fixed minimum-pixel and exact-font-face-count browser assertions, exact download paths,
  and a table-of-contents-dependent heading count because they constrained implementation details
  rather than stable student-visible behavior.
- Kept shared-environment `pip check` output as diagnostic evidence rather than a repository gate;
  it reports unrelated Torch and Qwen package conflicts while this repository's build and imports
  pass their focused checks.
- Replaced the proposed BIOL 318/418 lime after measurement showed 4.10:1 contrast with white; the
  darker hue-preserving value reaches 5.53:1.
- The independent audit identified non-atomic replacement of generated downloads as a failure-mode
  risk; staged validation and per-file replacement now preserve the current set when generation
  fails before publication.
- The independent audit found that manifest `status` did not change behavior, so the unused status
  and publication-state fields were removed rather than preserved as misleading metadata.
- Private original syllabus sources are not present in the checkout or Git history, so the restored
  four-part learning structure uses the strongest available tracked evidence and remains open to
  later public-source refinement.
- Treated tracked public Markdown as the autonomous content authority. Missing private source
  material does not block plan completion; agents make the most defensible complete proposal and
  record narrow evidence limitations for later editorial refinement.
- Kept security work proportional to a static public site while retaining the owner's absolute
  boundary that credentials and non-public content never enter the repository or generated output.
- Kept the complete shared policy set in every current course because the owner defined one common
  policy authority; later wording refinements continue to edit those canonical topic files once.

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
- `source source_me.sh && python3 -m pytest tests/` passed: 855 tests, including restricted shared
  includes and the four-part learning-framework contract.
- `bash tests/e2e/e2e_syllabus_export.sh` rebuilt all three PDF/DOCX pairs, passed credential and
  completeness checks, and completed a strict MkDocs build.
- `npm run test:playwright` passed the final desktop/mobile accessibility and navigation audit,
  including direct homepage access to all three current courses and removal of future-term stubs.
- Extracted text from all three final PDFs contains the exact office-hours value and each required
  learning-section heading once per syllabus; web-only policy-route lists are absent.
- `source source_me.sh && python3 -m pytest tests/` passed: 867 tests, including hidden-control,
  table-structure, table-render-count, shared-fragment-boundary, and PDF-export regressions.
- `bash tests/e2e/e2e_syllabus_export.sh` rebuilt all three PDF/DOCX pairs, rejected raw Markdown
  pipe rows in PDFs, and completed the strict site build.
- `npm run test:playwright` passed desktop/mobile accessibility and overflow checks on both policy
  table pages and verified their semantic column headers.
- Rendered inspection of the final grading-policy and missed-lab PDF pages found consistent grids,
  intact table boundaries, readable headers, and no clipping or unrendered Markdown.
- `source source_me.sh && python3 -m pytest tests/` passed: 870 tests, including staged-download
  publication, incomplete-stage preservation, and public-only repository regressions.
- `bash tests/e2e/e2e_syllabus_export.sh` rebuilt all three PDF/DOCX pairs, rejected credentials and
  unfinished editorial markers, and completed the strict site build.
- `npm run test:playwright` passed the final desktop/mobile accessibility, navigation, table, and
  course-identity behavior checks.
- Rendered inspection of the finalized BIOL 351/451 grading and schedule pages found fitted tables,
  complete headings, readable text, and no draft or review banners.
- `source source_me.sh && python3 -m pytest tests/` passed: 785 tests after removing the duplicated
  template sources and adding the single-authority and internal-link regressions.
- `bash tests/e2e/e2e_syllabus_export.sh` rebuilt all three PDF/DOCX pairs from the moved renderer
  reference, passed content and credential checks, and completed the strict MkDocs build.
- `npm run test:playwright` passed the desktop/mobile accessibility, navigation, table, and
  course-identity behavior checks against the rebuilt site.
- Extracted text from every generated PDF and DOCX contains the canonical `92.0% and above` scale
  row exactly once; the authored percentage thresholds occur only in the grading-policy source.
