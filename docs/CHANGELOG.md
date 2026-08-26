## 2026-08-26

### Additions and New Features

- Added executable `all_test.sh` as the local validation front door. It prints conspicuous phase
  banners and runs fast pytest, the complete export E2E and strict site build, then the Pages
  production builder and Playwright. Both build paths refresh the live Google Sheets dates.
- Added a custom protein-ribbon SVG favicon using the three greens from Roosevelt University's R
  mark and verified that the built homepage links to the published image.
- Added named GitHub, YouTube, Bluesky, LinkedIn, and Facebook links to the Material footer using
  the student-appropriate social profiles from the Biology Problems website.
- Added an accessible light/dark palette toggle that follows the student's operating-system
  preference on first visit and preserves a manual choice while navigating the site.
- Added `GITHUB_PAGES_BUILD.md` as the canonical deployment reference, with the required artifact
  build path, local-only semantic-test boundary, and zero-job failure triage. Linked it from
  `AGENTS.md` and the README so agents encounter it before changing the workflow.
- Added durable architecture, file-structure, file-format, visitor-focused related-project,
  release-history, and news documentation grounded in current sources, workflows, and authoritative
  project evidence.
- Added two current README screenshots covering the light student homepage and dark General
  Genetics page, plus a reusable Playwright capture harness that serves the real built site.
- Added `pipeline/sync_important_dates.py` to pull the first worksheet of the Fall 2026 planning
  spreadsheet into an ignored Markdown fragment, group its table rows by month, and infer a readable
  event type.
- Added a tracked important-dates page wrapper to the Fall 2026 site navigation and
  shared-information links. It includes the live generated fragment, with the event and inferred
  type placed immediately after the date; personal confirmation, calculated week, update notes, and
  the source-only `X` formula used to gray past spreadsheet rows are omitted.

### Behavior or Interface Changes

- Added `-D`/`--include-docs` to fresh Graphify builds so the repository mapper can include
  Markdown and Graphify's other semantic document inputs. Document extraction uses the same pinned
  Claude CLI or Ollama backend as community labeling and forces semantic re-extraction past an
  existing code-only manifest; code-only remains the default.
- Made the public GitHub Pages site the README's first action after the opening paragraph, with a
  prominent Fall 2026 link, student-facing orientation, current release context, and a broader
  documentation map.
- Changed the main and shared-page theme from Material indigo to Roosevelt green, with the middle
  logo green behind dark controls and an accessibility-adjusted dark green for body links. Each
  course keeps its existing header identity color and white controls.
- Expanded the web layout beyond Material's default desktop limit so wide browsers give more room
  to the reading column and both navigation sidebars while preserving the existing mobile layout.
- Stopped Material's 1600- and 2000-pixel root-font increases from enlarging the entire interface.
  Wider desktop windows now add reading width while body, navigation, and header text stay the same
  size.
- Tightened website typography to 1.25 line spacing, smaller paragraph gaps, and more compact
  heading margins. PDF and DOCX typography remains unchanged.
- Rebuilt the shared policy information architecture so each subsection has one subject-based
  parent: instructor communication, course delivery, assessment, attendance and accommodations,
  academic integrity, course expectations, inclusion and safety, or course enrollment.
- Kept instructor-facing category names in canonical filenames while giving students task-oriented
  page labels such as **Grades and graded work**, **Contacting Dr. Voss**, and **Dropping or
  withdrawing from class**.
- Made `ASSESSMENT.md` the sole shared grading source, including the letter-grade scale and rules
  for assignments, quizzes, exams, discussion marks, make-up work, and Blackboard percentages.
- Kept `shared/policies/index.md` as the only policy overview and removed the competing generic
  overview and catch-all FAQ after routing their content to subject pages.
- Replaced course-number directory paths with subject-based aliases: `biostats` for BIOL 318/418,
  `genetics` for BIOL 351/451, and `biotech` for BIOL 480. Student-facing headings, section details,
  manifest metadata, and download names retain the official course codes.
- Consolidated directly navigable term-wide pages under `shared/`, policy pages under
  `shared/policies/`, and include-only Markdown under `shared/fragments/`. The public instructor
  page now wraps the named instructor-contact fragment that course-details pages also embed.

### Fixes and Maintenance

- Pruned manager-authored architecture, content routing, test doctrine, and implementation details
  from `HUMAN_GUIDANCE.md`. It now contains only explicit durable owner guidance and a provenance
  rule that prevents it from becoming an agent or manager dumping ground.
- Rebuilt `RELATED_PROJECTS.md` around comparable syllabus repositories, publishing alternatives,
  and accessibility guidance after the updated discovery rules excluded implementation
  dependencies.
- Corrected the unreleased 26.08 labeling, documented the exact Pages pending-run semantics,
  limited the Playwright setup helper to the Chromium browser used by both consumers, and repaired
  a stale selector-contract line reference after the six-pass change audit.
- Refreshed installation and usage guidance with the no-install public route, architecture and
  format cross-links, and the exact README screenshot regeneration workflow. Replaced `AGENTS.md`
  prose links with a compact task router to canonical documents.
- Narrowed the GitHub Pages workflow to runtime Python artifact generation, upload, and deployment.
  Pytest, export E2E assertions, and Playwright remain local maintainer checks so semantic or browser
  findings cannot prevent an otherwise buildable site from publishing.
- Restored Poppler to the Pages runner because production syllabus generation directly requires
  `pdfinfo` and `pdftotext`. Unified clean-machine Playwright setup around `npm ci` and the
  repository helper, and clarified that accessibility failures are strong local signals rather
  than Pages deployment gates.
- Moved academic integrity and AI guidance out of grading, and moved withdrawal, late withdrawal,
  and tuition refunds into the course-enrollment category.
- Removed the Spring 2026 withdrawal date from the Fall 2026 policy source. The policy now routes
  students to the canonical term dates and current Roosevelt withdrawal and refund information.
- Removed the unrelated university important-dates link from the instructor-information table;
  the term dates page remains the student-facing authority for shared deadlines.

### Decisions and Failures

- Treat `--include-docs` as an explicit source-egress operation: unlike the code-only default, it
  sends every nonignored semantic input to the selected Claude CLI or Ollama backend. Automated
  validation therefore stops at local corpus and command construction; a connected extraction is
  an explicit maintainer action.
- Human review approved removing pytest, export E2E, and Playwright release gates from GitHub
  Actions. This is settled release governance: Pages publishes whenever the production artifact
  can be generated and uploaded, while semantic validation remains a local maintainer
  responsibility.
- Kept the R mark's exact three green fills in the favicon. The first browser render also used the
  middle green for text links and a translucent search surface; the accessibility audit rejected
  both. The final theme separates middle-green surfaces, pale-green fields, and a darkened
  `#007849` link color that reaches the 5.5:1 house target on white.
- Bounded the desktop grid at 78rem instead of filling the entire viewport. This gives policy prose
  substantially longer lines on wide displays without turning it into edge-to-edge monitor text.
- Kept date and event wording faithful to the worksheet. The current source includes Fall 2025 and
  Spring 2026 wording within rows dated Fall 2026 or later; those labels should be corrected in the
  spreadsheet rather than silently rewritten by the synchronization script.
- Made every complete site build depend on a successful Google Sheets refresh. The build fails
  instead of using a previously generated table when the canonical source is unavailable; the
  local MkDocs preview applies the same freshness rule.
- A config-only dark-mode pass retained the light scheme's `#007849` links, which were unreadable
  on the dark surface. The final scheme uses Roosevelt middle green for links and tints Material's
  slate surfaces toward the Roosevelt green hue while retaining each course's header color.

### Developer Tests and Notes

- Ran `./all_test.sh` end to end after adding the aggregate runner: the fast repository lane, both
  live Google Sheets refresh and build paths, the export E2E, and the Playwright browser
  accessibility audit passed.
- Passed all 869 fast tests, Python compilation, focused ASCII checks, and `git diff --check` after
  adding six Graphify CLI contract tests. Graphify 0.9.50's local detector found the intended 35
  repository Markdown inputs: five root documents and all 30 live `site_docs/` Markdown sources;
  `docs/` and generated output remain excluded.
- Verified that the prominent GitHub Pages target returns HTTP 200. Passed all 863 fast tests
  against an isolated material-tree Git index, the complete syllabus export E2E, the strict MkDocs
  build, and the Playwright accessibility audit without changing the user's real staging state.
- Visually reviewed both 1440 by 900 README captures and regenerated them from the final built site;
  the tracked and regenerated PNG checksums match exactly.
- Added a browser regression check for the five footer profiles, including their accessible names,
  exact destinations, new-tab behavior, and `noopener` protection.
- Measured the dark palette's key pairs at the 5.5:1 house target: `#73c167` links reach 6.84:1 on
  the `#1e2923` page surface, `#bddeb1` accents reach 10.20:1, and `#231f20` header controls reach
  7.41:1 on the `#73c167` brand header.
- Expanded the browser audit across every published route at 390 and 1280 pixels in both light and
  dark modes. It also exercises the visible toggle, verifies the manual choice across navigation,
  and checks the dark course-header foreground; reviewed screenshots at 390, 1280, and 2004 pixels.
- Parsed the favicon as XML, resolved its local references, and rendered and visually inspected it
  at 16, 32, and 64 pixels. The light-green ribbon reaches 3.07:1 against the dark-green tile.
- Added browser checks for the favicon URL, response, and SVG media type, plus the Roosevelt main
  header and link colors. Reviewed the real homepage at 390, 1280, and 2004 pixels.
- Passed all 822 fast tests, the live production build, the complete syllabus export E2E gate, and
  the final Playwright accessibility and responsive-overflow audit after the favicon and palette
  changes.
- Added a Playwright regression check that compares the academic-integrity page at 1280 and 2004
  pixels. It requires identical body, navigation, and header font sizes and a larger wide-screen
  reading measure.
- Confirmed the new regression failed before the fix because body text grew from 17 to 20.4 pixels.
  After the fix, body text stays 17 pixels while the reading column grows from 686 to 992 pixels
  between the 1254- and 2004-pixel screenshot widths.
- Passed all 822 fast tests, the strict production site build, and the Playwright accessibility and
  responsive-overflow audit after the website layout and typography changes.
- Added focused offline tests for worksheet schema and date validation, month separation, category
  inference, maintainer-metadata omission, Google redirect restrictions, and safe Markdown
  rendering of remote cell text. Kept inputs inline and removed duplicate row-format coverage and
  repetitive category examples during the permanent-test audit.
- Added the important-dates route to the built-site browser accessibility and responsive-overflow
  smoke.
- Kept the fast pytest lane offline; the complete build and its E2E gate intentionally use the live
  Google Sheets source.
- Classified the live worksheet's 45-event/seven-month category census, repeat-sync checksum, and
  responsive screenshot review as one-time implementation evidence rather than permanent tests.
- Confirmed the live first worksheet currently has no `Other` category fallbacks.
- Passed all 822 fast tests on the final moved content tree, the strict production site build, the
  Playwright accessibility audit, and the complete syllabus export E2E gate.

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

- Replaced the generic AI-use paragraph with one shared Fall 2026 honor-system policy that asks
  students to build expertise before relying on AI, keeps the instructor's responsibility boundary
  concise, and includes the refined forklift analogy and AI-writing caution across all courses.
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
