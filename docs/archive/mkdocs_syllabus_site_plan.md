# Plan: Build the accessible syllabus site

Status: Complete and archived on 2026-08-25 after the autonomous source, export, browser, and
rendered-document gates passed.

## Context

This repository publishes public Fall 2026 syllabus content through MkDocs Material. The site must
make course content easy to read, keep Dr. Voss's shared course policies separately editable, and
generate complete DOCX and PDF files for students and department archival. Tracked Markdown is the
canonical authority; private or access-controlled source material does not belong in the repository,
including ignored paths.

## Objectives

- Publish the active-term syllabi as static, term-first Markdown content and add archives only when
  an archived term exists.
- Keep course sections, one topic-split Dr. Voss policy branch, shared term fragments, and student
  resources independently editable.
- Merge those sources into complete, readable DOCX and PDF downloads.
- Prevent Zoom credentials and private invite links from entering tracked or built output.
- Audit the site against WCAG 2.2 AA. Treat the repository's 5.5:1 contrast target as a design
  goal rather than a publication gate.

## Design philosophy

Content and publication safety come before presentation. This applies the repository principles
"Focus on important issues" and "Long-term over short-term": establish one durable source model and
one reproducible export path before adding branding or optional features.

- Evidence strategy for uncertain methods: use a full-length representative syllabus to inspect
  DOCX structure, tagged PDF output, page layout, and table rendering during development.

## Scope

- Keep the repository public-only and scan syllabus sources and output for meeting credentials.
- Separate public `site_docs/` from maintainer `docs/`.
- Create Fall 2026 term and course structures for BIOL 318/418, BIOL 351/451, and BIOL 480.
- Create a reusable course template that preserves Dr. Voss's actual four-part learning framework.
- Add manifest-driven DOCX/PDF generation with policies and resources each appended once.
- Add minimal Material navigation, accessible tables, focused tests, and GitHub Pages deployment.
- Document installation, authoring, exporting, and validation.

## Non-goals

- Add broad visual branding, analytics, a CMS, a database, or authentication. Restrained,
  web-only course header identity colors remain in scope.
- Automate or shift academic-calendar dates.
- Publish enrollment or wait-list counts that become stale during registration.
- Claim PDF/UA certification or legal accessibility compliance.
- Invent credentials, private course material, or unsupported institutional claims.

## Current state summary

- The current strict MkDocs build succeeds with MkDocs 1.6.1 and Material 9.7.7.
- The repository suite, complete export E2E, and browser audit provide the autonomous completion
  path; exact test counts remain changelog evidence rather than plan state.
- Pandoc 3.10.2, Python-Markdown 3.10.3, WeasyPrint 69.0, Pango, and Poppler are available locally.
- A probe generated a tagged, seven-page PDF but showed that the raw university DOCX needs a
  purpose-built reference-document cleanup for usable tables and page flow.
- The supplied Fall 2026 registration data defines three public course groups and six sections.
- The implemented pipeline generates semantic DOCX files through Pandoc. Python-Markdown loads the
  site's extension stack from `mkdocs.yml`, creates small standalone HTML, and WeasyPrint renders
  tagged, letter-size PDFs. Both branches use the same manifest-assembled Markdown authority.
- Technical implementation and automated gates are complete. The refinement checklist records
  non-blocking opportunities for later content improvements.

## Milestone plan

| M | Title | Summary | Status |
| --- | --- | --- | --- |
| M1 | Content foundation | Establish public term/course sources | Complete |
| M2 | Complete exports | Merge course and shared sources into DOCX/PDF | Complete |
| M3 | Static publication | Build accessible navigation and automatic Pages output | Complete |
| M4 | Verification | Run content/build gates and accessibility audits | Complete |

### Milestone M1: Content foundation

- Depends on: none.
- Deliverables: public-only canonical inputs, Fall 2026 term pages, three course groups, topic-split policies,
  separate student resources, reusable fragments and templates, and course manifests.
- Exit criteria: no private meeting credentials appear under `site_docs/`; every course section is
  reachable from its term page.
- Parallel-plan ready: no - content structure is a single authority and should be established
  serially.

### Milestone M2: Complete exports

- Depends on: M1.
- Deliverables: Python 3.12 export command, accessible reference DOCX, complete DOCX/PDF files, and
  optional local term archive.
- Exit criteria: each export contains every course section, policy topic, shared fragment, and
  resource source exactly once; both outputs build from the composed Markdown authority.
- Parallel-plan ready: yes - the DOCX and HTML-to-PDF branches are independent sibling outputs.

### Milestone M3: Static publication

- Depends on: M2.
- Deliverables: Material configuration, functional table/download styling, strict build command,
  and official GitHub Pages artifact workflow.
- Exit criteria: the built site serves all pages and complete downloads at the project URL.
- Parallel-plan ready: no - the small site shell integrates directly with the export contract.

### Milestone M4: Verification

- Depends on: M3.
- Deliverables: focused unit checks, slow export E2E check, browser accessibility audit, rendered
  PDF review, documentation, and changelog evidence.
- Exit criteria: source, credential, export, strict-site, and browser behavior checks pass;
  accessibility findings are recorded for improvement.
- Parallel-plan ready: yes - max parallel doers: 2, one for browser evidence and one for document
  evidence, after the implementation is stable.

## Acceptance criteria and gates

- Content gate: current course pages contain no unfinished editorial markers, every manifest source
  resolves, tables are structurally valid, and complete outputs contain every required section.
- Source-of-truth gate: office hours and Roosevelt learning goals each have one editable term
  source; no per-course policy alternatives remain.
- Learning-framework gate: each course contains Roosevelt learning goals, learning objectives,
  course learning outcomes, and learning goals under the formal student-facing title.
- Security gate: tracked Markdown, built HTML, DOCX text, and PDF text contain no meeting secrets.
- Web gate: strict MkDocs build, valid navigation, and working complete-download targets.
- DOCX gate: valid output containing every manifest section and no prohibited secrets.
- PDF gate: valid letter-size output, selectable text, complete content, and no prohibited secrets.
- Delivery gate: every successful `main` build uploads and deploys a valid GitHub Pages artifact.

## Verification classification

Permanent build gates cover public-only source layout, credential exclusion, manifest completeness,
successful document conversion, required section presence, valid downloads, unfinished-marker
exclusion, and a strict static site build. These checks form the complete manager-executable
publication path without a separate approval state.

Repeatable advisory audits cover keyboard use, axe findings, viewport overflow, contrast, DOCX
structure, PDF tags/bookmarks, and rendered page flow. Findings guide improvements but do not block
publication.

One-time or renderer-change evidence includes dependency-size comparisons, plugin experiments,
exact package versions, exact page counts, and representative rendered-page inspection. These
observations belong in the changelog or an audit report, not as permanent equivalence, pixel, or
timing tests.

## Documentation close-out requirements

- Move this plan with `git mv` to `docs/archive/` after the autonomous gates pass.
- Update `docs/CHANGELOG.md` with content, export, validation, and deployment evidence.
- Document authoring and export commands in `docs/USAGE.md` and dependencies in `docs/INSTALL.md`.

## Deferred refinements

- Broader visual branding remains optional because it does not materially improve the current
  student tasks. Course identity stays limited to accessible web-header colors; the syllabus
  stylesheet owns the tested type scale and table overflow behavior.
- Archived-term behavior is added when the first archived syllabus exists; it is not a hidden
  prerequisite for the active Fall 2026 site.
