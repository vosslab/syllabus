## 2026-08-27

### Additions and New Features

- Added Dr. Voss's current portrait to the shared instructor-information table so students can
  recognize him outside class. The website uses coordinated light- and dark-mode portraits, while
  the PDF and DOCX use the light-background portrait from the same tracked public asset pair.
  Added descriptive alternative text and a visible 2026 date note, and documented the
  one-image-source and website-only theme-substitution strategy as a durable design decision.
- Added a Fall 2026 syllabus rubric review with a prioritized maintainer todo list, covered
  components, accessibility applicability notes, and links to the three live course authorities.
- Added shared department and program leadership information for Dr. Robert Seiser and Dr. Neil
  Voss, including their Roosevelt profiles and Dr. Voss's Bioinformatics and Computational Biology
  director role.
- Restored explicit course textbook and technology sections: Genetics uses Dr. Voss's required
  free LibreTexts website, Biostatistics lists optional open resources and the former commercial
  reference, and Biotechnology clearly labels the current third-edition Clark text as optional.
- Added a department-checklist generator and tracked rubric evidence model. It produces separate
  Markdown and DOCX checklists for Biostatistics, General Genetics, and Applications of
  Biotechnology, with public evidence links, explicit not-applicable rationales, and unresolved
  doubts left unchecked for department or instructor review.

### Fixes and Maintenance

- Tightened three long owner-guidance bullets to satisfy the vendored three-line entry limit while
  preserving their heading-style, download-presentation, and test-plan review requirements.
- Recorded the durable owner requirement that syllabus content address students directly as its
  audience, even though students may be the least likely readers of the complete syllabus.
- Corrected the rubric review so documenting one program role does not count as proof that every
  course has the applicable program director. Removed an unsupported claim that the department
  chair directs unspecified larger programs; Allied Health and other programs remain excluded
  unless their applicability to a particular course is established.

## 2026-08-26

### Additions and New Features

- Added a documentation roadmap for Fall 2026 maintenance, the planned Spring 2027 rollover, and
  an evidence-backed troubleshooting guide. Refreshed the README student journey and screenshots,
  architecture and file map, installation and usage paths, related-project evidence, release/news
  summaries, and the concise agent-guidance pointers from the current source and build model.
- Added a bounded live HTTP(S) link checker for the active Markdown syllabus authority. It follows
  validated public redirects, detects HTTP failures and common soft-error pages, and reports every
  failure with its source file and line while keeping the fast pytest lane offline.
- Added one canonical `TERM_COURSES.md` fragment for the Fall 2026 course summaries and complete
  PDF/DOCX links. Both the main page and term overview now expand that source.
- Added repository-owned `EXTRA_CREDIT.md` and `EXTRA_CREDIT_MOVIES.md` pages from the two public
  Google Docs that previously held the write-up guide and approved movie list.
- Added one repository-owned Markdown include engine under `pipeline/build_lib/` and a thin MkDocs
  hook so the website and complete-document builder share the same grammar, authorization, path
  resolution, and content expansion.
- Added fast include-contract tests for syntax, target roles, traversal, symlink containment,
  nested includes, MkDocs hook loading, and `exclude_docs` consistency. Added a production E2E that
  checks the relevant website, DOCX, and PDF artifact corpora, and routed it through `all_test.sh`.
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

- Added page numbers and dotted leaders to the generated PDF and DOCX contents lists. Contents
  labels now derive automatically from source page filenames in Title Case, while visible headings
  keep their student-facing titles. Added format-native three-part footers with course and term on
  the left, the current student-facing section in the center, and `Page X of Y` on the right.
- Expanded the Biostatistics optional references with two subject-specific LibreTexts OER books.
  Clarified that the course intentionally emphasizes Google Sheets over R to lower the barrier for
  students meeting a program requirement and make the statistical methods more reusable after the
  course. Addressed students directly rather than describing them in the third person.

- Moved the approved science-movie catalog from the Fall 2026 policy branch to the global
  website-only `site_docs/EXTRA_CREDIT_MOVIES.md` route. Extra credit still links students to the
  catalog, while all three course manifests now omit its niche, verbose content from PDF and DOCX
  syllabi. The Extra credit source uses the canonical public URL so the remaining link works from
  exported documents rather than becoming a filesystem-relative Markdown target.
- Reorganized Help and student services into four explicit student-task groups: academic progress
  and learning; technology and campus life; money and essential needs; and health, identity, and
  safety. General academic services now lead, personal services come later, and Campus Safety leads
  the final group so emergency contacts remain easy to find. Preserved every Chicago and Schaumburg
  contact while shortening repetitive descriptions and clarifying the table-of-contents hierarchy.
- Replaced the obsolete extra-credit document, SafeAssign, total-word-count, similarity-score, and
  heading workflow with four category-specific Google Forms. Recast the former write-up as the
  forms' actual structured fields: activity evidence, rating, short focus and reflection responses,
  five brief definitions, and category-specific questions. Retained current-semester eligibility,
  the shared deadline, grading timing, and activity-specific requirements.
- Color-coded all four Extra credit category headings and matching Google Form actions with distinct
  accessible blue, purple, orange, and green accents on the website and PDF. Category numbers and
  names remain visible so color reinforces rather than replaces the category labels.
- Added separate self-hosted Font Awesome link marks within syllabus content: Roosevelt-owned
  destinations use the building-columns mark, other HTTP(S) destinations use the external-link
  mark, and internal syllabus navigation remains unmarked. The distinction inherits the existing
  accessible link color in both light and dark modes and requires no extra link text or CSS class.
- Restructured Help and student services for consistent scanning: explanatory prose now introduces
  each service, parallel campuses and contact methods use sibling labeled bullets, and tutoring,
  coaching, and Disability Services are grouped beneath Learning Commons. Corrected the pantry's
  broken mixed paragraph/list structure and the accidental nesting of Schaumburg beneath Chicago.
- Added the same compact, icon-labeled PDF and DOCX links beneath every course on the main student
  homepage. Fragment-relative Markdown and HTML links now rebase for each receiving page while
  remaining contained under `site_docs/`, so shared linked content works at different route depths.
- Added a short accessibility note to the Fall 2026 overview explaining that the online syllabus
  uses Atkinson Hyperlegible Next to make similar characters easier to distinguish, with a link to
  the Braille Institute's English-language font guide. Recorded the same durable presentation
  preference in owner guidance.
- Replaced the external Extra credit Google Docs link with two local student routes directly after
  Discussion marks. Every complete course PDF and DOCX now includes the four categories, write-up
  and submission rules, deductions, FAQ, and categorized movie choices from the same live content
  authority as the rest of the Fall 2026 syllabus.
- Moved the Zoom discussion-mark policy, in-person poker-chip policy, criticism responses, scoring
  rules, and no-make-up rule out of `ASSESSMENT.md` into one canonical
  `shared/policies/DISCUSSION_MARKS.md` page. The new student-facing **Discussion marks** route
  follows **Grades and graded work** in the policy overview, site navigation, and every course's
  PDF/DOCX manifest.
- Added the tracked Important Dates wrapper to all three course manifests after course enrollment
  and before student resources. The synchronized tables now appear near the end of every complete
  PDF and DOCX syllabus, and the long PDF reference section starts on a clean page.
- Changed generated month headings from level two to level three and gave each immediately
  following website/PDF table a restrained month-colored top rule and header surface. Light mode
  and PDF use the Google Sheet's pale swatches; dark mode uses measured deep tints while DOCX keeps
  its format-native neutral table style.
- Replaced Material's default book logo with the protein favicon in the standard upper-left
  home-link position.
- Added the shared Font Awesome PDF icon to Roosevelt's Religious Holidays Policy link and replaced
  the displayed raw URL with a descriptive label that retains visible `(PDF)` text. Consolidated
  term, course, and policy document links onto reusable explicit file-type classes so redirecting
  URLs do not need filename suffixes.
- Moved the Fall 2026 PDF and DOCX links into a compact row directly below each course on the term
  overview. Visible file-format labels now include small, self-hosted Font Awesome PDF or Word
  icons on both the term overview and course landing pages, and the oversized standalone download
  section is gone. The local Font Awesome font and its license follow the established Biology
  Problems website installation.
- Replaced website level-two heading text underlines with a separate course-colored rule spanning
  the reading column, so headings no longer resemble links.
- Gave the Material website and WeasyPrint PDF one shared visual hierarchy: bold small-caps
  level-one headings, bold solid-underlined and slightly left-shifted level-two headings, bold
  paragraph-aligned level-three headings, and italic level-four headings. Course colors now appear
  as restrained heading and rule accents instead of a header-only theme.
- Justified long-form body paragraphs on comfortable website widths and in PDFs with last lines
  returned to the start edge and automatic hyphenation disabled. Narrow web columns and paragraphs
  containing external links fall back to left alignment; URLs and code use emergency wrapping only
  when they would otherwise overflow.
- Restyled website and PDF tables with course-colored top and header rules, pale neutral headers,
  and quiet alternating rows. Web tables with four or more columns now retain a readable minimum
  width and use Material's existing horizontal scroller on narrow screens.
- Added direct PDF and DOCX links for every course to the Fall 2026 overview, eliminating the need
  to visit each course page before downloading a complete syllabus.
- Replaced the separate PyMdown and exporter include languages with one exact full-line,
  double-quoted `--8<--` form. Paths resolve from `site_docs/`, and only Markdown below a directory
  named `fragments` or `generated` is authorized.
- Made every unsupported marker form fail before rendering instead of passing raw markup into one
  format. Empty targets, remote or absolute paths, parent traversal, symlink escapes, ordinary page
  targets, and nested includes also fail explicitly.
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
- Gave headings one consistent content gap before paragraphs and tables by removing the table's
  duplicate inner margin. Removed the decorative rules between important-date months and above
  complete-syllabus downloads; headings and whitespace now provide the page structure without
  faint redundant lines.
- Matched generated important-date headings to the Google Sheet's month-specific colors without
  adding colored table fills. Light mode uses accessible hue-preserving companions for January,
  May, and August through December (`#1c61db`, `#866300`, `#ad4a36`, `#476f77`, `#9f560a`,
  `#745aae`, and `#477337`); dark mode uses the exact pastel sheet swatches.
- Rebuilt the shared policy information architecture so each subsection has one subject-based
  parent: instructor communication, course delivery, assessment, attendance and accommodations,
  academic integrity, course expectations, inclusion and safety, or course enrollment.
- Kept instructor-facing category names in canonical filenames while giving students task-oriented
  page labels such as **Grades and graded work**, **Contacting Dr. Voss**, and **Dropping or
  withdrawing from class**.
- Made `ASSESSMENT.md` the sole shared grading source at that stage, including the letter-grade
  scale and rules for assignments, quizzes, exams, discussion marks, make-up work, and Blackboard
  percentages. The later dedicated Discussion marks page supersedes that original grouping.
- Kept `shared/policies/index.md` as the only policy overview and removed the competing generic
  overview and catch-all FAQ after routing their content to subject pages.
- Replaced course-number directory paths with subject-based aliases: `biostats` for BIOL 318/418,
  `genetics` for BIOL 351/451, and `biotech` for BIOL 480. Student-facing headings, section details,
  manifest metadata, and download names retain the official course codes.
- Consolidated directly navigable term-wide pages under `shared/`, policy pages under
  `shared/policies/`, and include-only Markdown under `shared/fragments/`. The public instructor
  page now wraps the named instructor-contact fragment that course-details pages also embed.

### Fixes and Maintenance

- Applied the six-pass pre-merge audit's consistency fixes: expanded the default live-link scan
  from the Fall term tree to all public `site_docs/` Markdown, separated the global website-only
  movie catalog from policy topics promised inside complete syllabi, aligned the primary authority
  wording, and made new source-file references clickable.
- Corrected the public-content build boundary so an ignored local `raw/` directory may hold public
  university reference material without blocking the syllabus build. The build still fails closed
  if Git tracks anything under `raw/`, and it continues scanning the actual `site_docs/` publication
  sources for prohibited credentials and controls.
- Used a temporary rendered-browser probe after a proposed social-link locator failed, then removed
  both the exact five-profile assertion loop and the local Material footer override created to
  satisfy it. The test duplicated current configuration and drove a theme hack rather than exposing
  a failure in the existing route-wide axe accessibility audit, so neither belongs permanently.
- Recorded the durable rule that tests provide evidence for independently intended behavior; they
  do not justify hacky production changes solely to make an assertion pass.
- Expanded the durable plan-review rule to require checking the repository, pytest, test-layout,
  developer-tool, and relevant style guides before approving tests, fixtures, network access, or
  file placement.
- Removed the former permanent pytest that treated the mere existence of `raw/` as an error. That
  assertion encoded the superseded implementation rather than durable behavior; the complete
  production-shaped E2E build now supplies the appropriate tracked-scope proof.
- Replaced four failed live-syllabus destinations found by the new checker: two retired catalog
  academic-integrity routes now use the current policy PDF and student guide, the obsolete Maxient
  accommodations form now uses Roosevelt's AIM request form, and the blocked pandemic-era Illinois
  volunteer page now uses Serve Illinois. Added the current Disability Services page while
  explicitly retaining the newest university template's Schaumburg room, specialist, and phone.
- Expanded the document builder's landing-page link verifier before checking generated targets, so
  moving the term links into their canonical fragment does not hide them from the build contract.
  Replaced the term page's former raw `index.md` course URLs with working directory routes, and
  refreshed both managed README screenshots from the final built site.
- Applied the final six-pass audit's concrete fixes: removed a dead WBAL volunteering link,
  converted the moved Discussion marks lists to the repository's `-` bullet style, made tracking
  participation a real explanatory label, and refreshed two stale Playwright selector-contract
  pointers.
- Normalized the exported Google Docs headings, lists, raw URLs, Unicode punctuation, and duplicated
  outline text into repository-style Markdown. Removed ten movie titles from the pending list when
  those same titles were already categorized as approved, giving each affected movie one status.
  Corrected the imported `Being John Malkovich` and `Ikiru` title misspellings.
- Updated the owner guidance, author edit map, manifest example, policy information-architecture
  table, public source tree, policy overview, and route audit for the two Extra credit sources.
- Gave compact Material navigation links a 24-pixel minimum block size after the two added routes
  exposed a 23.8-pixel WCAG 2.2 target-spacing failure in the complete browser audit.
- Corrected the Discussion marks criticism introduction from five complaints to four so its stated
  count matches the four numbered concerns that follow. Split the closing run-on sentence so the
  page ends with a direct explanation of the collective-learning benefit.
- Updated the owner guidance, edit map, manifest example, public source tree, and policy
  information-architecture table to identify the dedicated Discussion marks source and its
  student-facing purpose.
- Expanded the production include-parity E2E from a website-only generated-date check to require a
  current synchronized event in every individual DOCX and PDF as well as the website corpus.
- Corrected the header-logo placement after the public-site review clarified that the protein mark
  should replace Material's book mark in its original upper-left position. Removed the custom
  display, sizing, and flex-order rules so Material owns the header layout and the logo no longer
  depends on a separately cached stylesheet to appear in the requested position.
- Audited the rebuild's new browser assertions against the permanent-test checklist. Removed
  computed CSS layout and font-size checks, exact course/link counts, old-heading absence, and
  Font Awesome family, load, and pseudo-element content probes from the permanent Playwright suite.
  The suite retains accessible download discovery, artifact parity, HTTP delivery, focus,
  accessibility, and overflow behavior.
- Corrected the README license links to target the tracked extensionless legal filenames used for
  GitHub license recognition while preserving descriptive Creative Commons and LGPL link text.
- Replaced the PDF's blanket new-page rule for every merged source with a transitional rule that
  starts only the course body and Dr. Voss policy group on new pages. Other sections now flow
  naturally, while each top-level heading's introduction stays with its first subsection. This
  removes sparse continuation pages without tying the stylesheet to the current page numbers.
- Applied the six-pass code audit's shared-ownership fix: both MkDocs and the document builder now
  call one course-theme validator, and the MkDocs hook normalizes allowlisted colors before the
  template receives them. Removed the website-only dark accent from the PDF manifest model.
- Corrected the README and maintained palette audit to show the course-colored PDF accents, dark
  website companions, current Roosevelt link colors, and neutral DOCX boundary.
- Made each course's adjacent `.meta.yml` the validated color authority for both render paths.
  Metadata now requires six-digit light and dark accents; the standalone PDF HTML receives only an
  allowlisted light accent, while Material uses the measured dark companion on its slate surface.
- Refreshed both tracked README screenshots from the final production-shaped site so the documented
  light homepage and dark General Genetics page show the new hierarchy and table treatment.
- Removed the stacked bottom margins and nested horizontal scrolling from website tables. The
  outer Material wrapper now owns both one normal content gap and any narrow-screen overflow,
  while a following section heading retains its deliberate section spacing.
- Kept WeasyPrint unpinned like every other Python dependency. The current 69.0 renderer applies
  the print stylesheet's logical margin and padding properties without compatibility warnings.
- Removed `pymdownx.snippets` from both the MkDocs and PDF extension stack, and removed the now
  unused direct `pymdown-extensions` application dependency. Declared the test-only direct
  `pathspec` import in development requirements.
- Migrated pytest imports to the repository's folder-not-package model by placing `pipeline/` on
  the test import path and loading `build_syllabi` and `sync_important_dates` under one module name.
- Decomposed the complete-document implementation into manifest-model, content-composition, and
  artifact-rendering library modules. `build_syllabi.py` now owns orchestration and CLI flow rather
  than retaining the implementation behind a marginal line-count reduction.
- Refreshed the architecture, file-structure, file-format, usage, and Pages-build references from
  the implemented include flow and artifact-parity boundary.
- After the six-pass implementation audit, corrected comments to distinguish the website hook from
  its shared engine and HTML text nodes from browser-visible text. Updated the README's focused E2E
  command to run the include-parity wrapper rather than its narrower export-only child runner.
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

- Recorded the owner's durable autonomy rule: assume the chat is not actively monitored, finish
  obvious safe follow-through and validation without routine confirmation, and stop only for risk,
  new authority, or a material change in outcome.
- The first full gate failed because the download verifier scanned the term wrapper before include
  expansion. Fixed the verifier to inspect the same expanded source model as MkDocs instead of
  duplicating links in the wrapper. Kept the two fragment-rebasing unit tests and the two-entry-page
  browser download check as permanent logic and student-behavior contracts; screenshot review was
  one-time evidence.
- The repository is now the only live authority for Extra credit instructions and approved movie
  choices; the imported Google Docs are neither linked nor synchronized. Exact categories, movie
  titles, deadlines, and prose remain editable content rather than permanent test constants. The
  durable gates cover local-link integrity, both public routes, accessibility, and inclusion of
  every manifest section in each PDF/DOCX pair.
- Treated the five requested Discussion marks headings and their exact wording as editable content,
  not a permanent test contract. The durable suite instead covers the route in the all-page browser
  audit and lets the document builder verify every manifest section in all three PDF/DOCX pairs.
- Classified the compact-row screenshots and the computed layout, relative font size, Font Awesome
  load, font family, and distinct-glyph checks as one-time rebuild evidence. Those checks proved the
  requested presentation during implementation but describe the current technique rather than a
  stable student-facing contract, so they do not remain as permanent tests.
- Kept the pagination repair deliberately narrow ahead of the planned content-order review. The
  current stable `course-overview` and `policies` anchors provide the two certain document
  boundaries; manifest-owned semantic document groups remain the durable follow-up after the order
  is settled.
- CSS provides no interoperable per-line word-stretch cutoff, and adding JavaScript would make the
  Material and WeasyPrint behavior diverge. The implemented fail-safe is content- and
  viewport-based: URL-bearing paragraphs and narrow screens use start alignment, while ordinary
  long-form prose retains justification.
- The initial one-green month-heading pass misunderstood the Google Sheet's color system. Replaced
  it with code-owned month-number classes and distinct theme-aware colors for every published
  month; the current sheet has no May rule, so May uses its unused `#fff2cc` yellow swatch.
- Kept one logical spacing declaration per PDF rule with the current WeasyPrint renderer. The
  website and PDF retain separate, format-appropriate spacing rather than duplicating values that
  would have to remain synchronized across two stylesheets or adding a package-version constraint.
- Treated the original 997-to-972-line include extraction as an incomplete architectural step, not
  a success criterion. The completed split leaves reusable implementation in `build_lib/` and the
  136-line `build_syllabi.py` entry point focused on orchestration; line count is evidence of that
  responsibility boundary, not the goal itself.
- Kept include authorization explicit in the engine. `exclude_docs` remains a broader navigation
  rule, and the permanent consistency test enforces only that every authorized Markdown fragment
  is excluded from direct routes.
- Scoped the initial artifact evidence to outputs that contained each source at that stage.
  Instructor-contact text reached the website, DOCX, and PDF corpora; generated important dates
  initially reached only the website because no course manifest yet included the term-wide page.
- Classified exact generated heading syntax, palette-token values, computed CSS colors, and
  screenshots as one-time rebuild evidence. The permanent E2E retains the student-facing contract:
  one current synchronized event must reach the website and every complete DOCX/PDF syllabus.
- The first Important Dates PDF page-break selector used the automatic heading slug, but composed
  documents use the explicit manifest anchor `#important-dates`. Rendered review exposed the
  no-op selector; targeting the owned anchor produced the clean section start.
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

- Rebuilt the strict site and reviewed the reordered Help and student services page at 1440 by 900
  light and 390 by 844 dark viewports. Both rendered the four groups in the intended order with no
  horizontal overflow; all 15 page links passed, and all 1,012 fast tests passed. A focused axe scan
  found no content-specific serious or critical violation; its one serious finding in both views
  was the pre-existing unnamed Material `.md-search` dialog, outside this content-ordering change.
- Audited the five offline link-checker tests against every permanent-test criterion in
  `PYTEST_STYLE.md`. They remain permanent because they cover durable parser, encoding, soft-error,
  source-location, and input-boundary behavior with inline `tmp_path` data, no network, no timing,
  and one or two meaningful assertions. Live URL visits, redirect/title inspection, form-status
  checks, screenshots, computed CSS glyph checks, and viewport overflow probes remain one-time
  implementation evidence; their temporary scripts were removed rather than added to the suite.
- Visited all supplied Extra credit forms after submissions opened and inspected the public field
  definitions for Categories 1, 3, and 4. Category 2 correctly requires Google sign-in. Confirmed
  that the first two originally supplied short links resolve to the same Category 4 form, so the
  duplicate is omitted, and verified the later Category 1 link against its live seminar title and
  field structure.
- Classified HTTP 401 as a reachable, authentication-required link in the live checker while
  retaining failures for forbidden, missing, and soft-error destinations. This lets the restricted
  Category 2 course form report its access boundary without being mislabeled as a dead link.
- Rebuilt the strict website and reviewed the revised Extra credit guide at 1440 by 900 light and
  390 by 844 dark viewports with no horizontal overflow. Rendered a one-time four-page letter-size
  PDF through the production Markdown extensions and print stylesheet and visually confirmed all
  four category colors and matching form actions. The active tree passed all 53 live links with
  zero failures and one expected authentication boundary; all 1,012 fast tests passed.
- Rebuilt the strict site and verified the domain marks on Help and student services at 1440 by 900
  in light mode and 390 by 844 in dark mode. Computed pseudo-element inspection confirmed the
  building-columns glyph on `roosevelt.edu` and its subdomains, the external-link glyph on
  third-party hosts, and no horizontal overflow in either viewport. All 1,012 fast tests passed.
  The all-route Playwright run stopped before the affected route checks on a pre-existing generated
  artifact mismatch: ignored `STALE_SYLLABUS.pdf` and `.docx` files were present in the download
  source but correctly absent from the freshly rebuilt site; those generated files were left alone.
- Rebuilt the strict MkDocs site and reviewed Help and student services at 1440 by 900 and 390 by
  844 after the content-structure pass. Both views retained a clear service/contact hierarchy with
  no horizontal overflow. All 15 external links on the page passed the live checker, and the
  focused Markdown, ASCII, and syllabus-builder suites passed all 220 tests. The complete fast lane
  passed all 1,012 tests after aligning the link checker's executable bit with its shebang.
- Verified all 49 unique HTTP(S) links in the active Fall 2026 authority and all 39 links in the
  supplied 2026-2027 university reference with zero failures. All 989 fast tests passed. The full
  `all_test.sh` then stopped at the public-source boundary before document rendering because the
  locally present ignored `raw/` directory is explicitly prohibited by the production builder;
  the reference was preserved for the owner rather than moved or deleted.
- Passed the shared term-course fragment through the complete material-tree `all_test.sh` gate:
  all 984 pytest checks, both live Google Sheets build cycles, all three DOCX/PDF pairs,
  export/include parity, both strict site builds, and the all-route Playwright accessibility audit
  passed. The refreshed 1440 by 900 light homepage and dark Genetics captures are below 200 KB and
  visually show readable hierarchy without clipping or overflow.
- Passed the accessibility-font note through the complete material-tree `all_test.sh` gate: all
  977 pytest checks, both live Google Sheets build cycles, all three DOCX/PDF pairs,
  export/include parity, both strict site builds, and the all-route Playwright accessibility audit
  passed. A one-time built-HTML inspection confirmed the visible note and Braille Institute link;
  no permanent exact-wording or external-page test was added for editable prose.
- Ran the requested six-pass audit across the complete working tree. Test and documentation
  reviewers found no issues; style, legacy, and comment reviewers found the dead WBAL link,
  ambiguous Discussion marks list structure, nonpreferred bullet markers, and stale selector
  pointers corrected above. The plan reviewer requested a separate approved plan, but the
  coordinator found that the cited repository rule requires atomic tasks with outcomes and
  verification, all of which the directly authorized queued requests supplied.
- Passed the post-audit material tree through the complete `all_test.sh` gate: all 977 pytest
  checks, both live Google Sheets build cycles, all three DOCX/PDF pairs, export/include parity,
  both strict site builds, and the Playwright accessibility audit passed.
- Passed the repository-owned Extra credit tree through the complete material-tree `all_test.sh`
  gate: all 977 pytest checks, both live Google Sheets build cycles, all three DOCX/PDF pairs,
  export/include parity, both strict site builds, and the all-route Playwright accessibility audit
  passed.
- A one-time DOCX-source inventory compared the imported movie guide with the repository page:
  all 255 unique title/year entries were present, no local-only titles remained, and no approved
  title also remained pending. This exact inventory is migration evidence, not a permanent test.
- Rendered and reviewed the complete 14-page Extra credit sequence in the BIOL 318/418 PDF. The
  guide, approved choices, excluded and pending lists, links, page numbers, and transition into
  Attendance showed no clipping, overlap, broken wrapping, or unreadable hierarchy.
- The first post-import Playwright run exposed a 23.8-pixel navigation target-spacing failure after
  the two new routes expanded the sidebar. The shared 24-pixel minimum target fix passed the focused
  browser rerun and the final complete gate; no accessibility assertion was suppressed or weakened.
- Ran the requested six-pass audit on the standalone Discussion marks change. Plan, test,
  documentation, and legacy reviewers found no issues; style and comment reviewers independently
  found the four-item complaint-count mismatch, and the comment reviewer also found the closing
  run-on. Both content issues were corrected before the final gate.
- Passed the dedicated Discussion marks page through a temporary material-tree Git index: all 967
  pytest checks, both live Google Sheets build cycles, all three DOCX/PDF pairs, export/include
  parity, both strict site builds, and the Playwright accessibility/browser audit passed. The real
  index remains untouched for the human-only staging workflow; its pre-stage link check therefore
  reports the new untracked target as absent until a human adds it.
- A one-time normalized comparison confirmed that all five moved policy sections retained their
  prior wording before the inherited complaint-count mismatch and closing run-on were corrected.
  Rendered review of the three-page BIOL 318/418 PDF sequence found readable hierarchy, clean page
  numbering, and no clipping, overlap, or broken transition into the following policy.
- Passed the final Important Dates tree through `all_test.sh`: all 962 pytest checks, both live
  Google Sheets build cycles, all three DOCX/PDF pairs, per-artifact generated-date parity, both
  strict site builds, and the Playwright accessibility/browser audit.
- One-time Chromium review covered the Important Dates page at 390 and 1280 pixels in light and
  dark modes. All generated month headings rendered as level three with no divider; computed coral
  heading/table colors matched the new tokens. Measured rendered header text against all 14 light
  and dark month surfaces at the 5.5:1 house target; ratios ranged from 5.69:1 to 14.75:1.
- Rendered the complete three-page Important Dates sequence from the BIOL 318/418 PDF and the clean
  section-start page from both other course PDFs. The section begins on a fresh page, tables repeat
  headers across page breaks, and no clipping, overlap, broken wrapping, or unreadable color was
  found before the document flows into student resources.
- Passed the reusable file-link change through the complete `all_test.sh` gate: all 962 pytest
  checks, both live build cycles, all three DOCX/PDF pairs, export/include parity, both strict site
  builds, and the Playwright accessibility/browser audit. One-time screenshots covered the
  Religious Holidays PDF link at 1280 and 390 pixels in light and dark modes; extracted PDF and
  DOCX text retained `Religious Holidays Policy (PDF)` without depending on the web icon.
- Ran the requested six-pass audit against `0a5c6ea..aa972bd`. Plan and test reviewers found no
  issues; style, docs, legacy, and comment reviewers identified the custom Material flex ordering,
  separately cached visibility rule, local-versus-deployed evidence wording, incomplete file-map
  description, and selector-contract overclaim corrected above.
- Passed the corrected tree through the complete `all_test.sh` gate: all 962 pytest checks, both
  live build cycles, all three DOCX/PDF pairs, export/include parity, both strict site builds, and
  the Playwright accessibility/browser audit. A separate one-time production-shaped render at
  `/syllabus/` loaded every header asset with HTTP 200 and showed the SVG in Material's original
  upper-left logo position; no layout-specific permanent assertion was added. After commit
  `7d81267` deployed, a fresh public Pages capture confirmed the same left-side logo and confirmed
  that the former custom right-edge CSS was absent.
- The initial right-edge implementation passed 962 pytest checks, the live builds, export/include
  parity, and local Playwright. Its one-time review used a root-served local site at 1280 and 390
  pixels rather than the deployed `/syllabus/` path; public review then exposed both the unwanted
  right-edge interpretation and the transient HTML/CSS cache mismatch. The temporary position
  checker was removed rather than added to the suite.
- After removing rebuild-only assertions, passed all 962 pytest checks, the live Google Sheets
  refresh, all three DOCX/PDF pairs, export/include parity, and both strict site builds through
  `all_test.sh`. Its Chromium launch was denied by the macOS sandbox before assertions ran; the
  same final `npm run test:playwright` lane passed with browser permission.
- Passed the complete `all_test.sh` gate after the term-overview, heading-divider, and Font Awesome
  changes: all 959 fast tests, the live dates refresh, all three final DOCX/PDF pairs, the export
  and include-parity E2E, both strict site builds, and the Playwright accessibility/browser audit.
  Rendered review covered the Fall 2026 overview and General Genetics landing page at mobile and
  desktop widths in light and dark modes.
- Rebuilt all three final PDF/DOCX pairs after the transitional pagination repair. The PDFs now
  use 27, 28, and 28 pages instead of 33, 34, and 33; rendered contact-sheet review covered all 83
  pages plus full-size section transitions and found no isolated headings, clipping, overlap,
  broken tables, or unreadable wrapping.
- After correcting the README license targets, passed the 200-test focused Markdown-link, README,
  and ASCII lane and a clean full `all_test.sh`: all 958 fast tests, the live complete-export and
  include-parity E2E, the strict site build, the production rebuild, and the Playwright browser
  accessibility audit.
- Ran the requested six-pass audit with independent plan, test, style, documentation, legacy, and
  comment reviewers. Plan, test, and comment passes returned no findings; the other passes found
  the split MkDocs validation owner, stale neutral-PDF documentation, and unused dark manifest
  field corrected above. The post-audit `all_test.sh` run passed all 967 fast tests, both live build
  cycles, export/include parity, and the Playwright accessibility audit.
- Measured every light course accent against white and every dark companion against Material's
  `#1e2923` slate surface at the 5.5:1 house target. Light accents reach 5.53:1 to 6.63:1; dark
  accents reach 6.29:1 to 8.99:1. Browser review covered light/dark desktop pages, 390-pixel course
  and schedule views, URL-heavy policy prose, and refreshed README captures.
- Rendered and reviewed contact sheets for all 100 pages across the three final PDFs, then inspected
  full-size title, heading, prose, URL, and table pages. No clipping, overlap, broken wrapping, or
  table overflow was found. The complete `all_test.sh` gate passed with 967 fast tests, two live
  dates/build cycles, export/include parity, and the Playwright accessibility audit; Chromium's
  first sandboxed launch was denied by macOS, and the identical permission-enabled rerun passed.
- Extended manifest validation so every generated basename must appear on both its course landing
  page and the term overview. Added the term route to the responsive accessibility matrix and a
  browser check that its unique, descriptive download links match and load every published file.
- Measured table-to-paragraph and table-to-heading gaps after a strict MkDocs rebuild. Chromium
  checks covered two-, three-, and four-column tables at 390-, 768-, and 1440-pixel viewports;
  only the four-column schedule required horizontal overflow at the mobile width.
- Classified the Google Sheet rule extraction, exact seven-color inventory, contrast measurements,
  computed browser colors, and responsive screenshot review as one-time rebuild evidence. Kept no
  permanent palette or CSS-class assertion; the existing offline renderer test covers only visible
  month grouping without decorative rules and safe escaping of remote worksheet text.
- Rebuilt all three DOCX/PDF pairs with WeasyPrint 69.0 without CSS compatibility warnings. As
  one-time implementation evidence, rendered and reviewed all 33 pages of the BIOL 318/418 PDF and
  compared representative pages with the physical-property probe; no clipping, overlap, broken
  tables, or material spacing regression was found.
- Passed all 965 fast tests against a temporary material-tree index after the decomposition. The
  live export/include-parity lane rebuilt every DOCX and PDF and passed the strict site build; the
  Playwright accessibility audit passed outside the filesystem sandbox required by Chromium.
- The production convergence audit found one `expand_includes` definition and exactly two runtime
  routes: `syllabus_content.py` with three pre-render call sites and `mkdocs_hooks.py` with one.
  It found no `expand_shared_includes` or `pymdownx.snippets` production reference, ruling out a
  second include grammar and the former PDF double-expansion path.
- Passed all 17 focused include tests. A mutation that deferred the hook import failed the isolated
  MkDocs-loader test with `ModuleNotFoundError` after MkDocs restored `sys.path`; restoring the
  module-level import passed, proving pytest's own `pipeline/` path does not invalidate the test.
- Ran `python3 tests/e2e/e2e_include_parity.py`: the live dates refresh, all three PDF/DOCX builds,
  strict MkDocs build, zero-marker scans, shared-fragment corpus checks, and generated-date website
  check passed.
- Passed all 927 fast tests against a disposable material-tree Git index, including the new files
  without changing the maintainer's real staging area. This covered Bandit, ASCII, typing, import,
  indentation, Markdown-link, pyflakes, shebang, whitespace, and source-line-limit gates.
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
