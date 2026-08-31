# Rolling publication history

This repository is continuously published rather than formally released. `VERSION` identifies the
current publication series, and the dated entries below record rolling publication milestones;
they do not imply tags or official releases.

## 26.08 publication series - started 2026-08-26

### Highlights

- Built one active Fall 2026 student source tree that produces the public website and complete
  PDF/DOCX syllabi, including shared policies, Important Dates, and direct course downloads.
- Added student-facing Extra credit instructions with category-specific Google Forms and moved the
  verbose movie catalog to a global website-only page outside the complete-syllabus manifests.
- Reorganized Help and student services around student tasks, retaining Chicago and Schaumburg
  contacts and placing academic support before personal services.
- Added accessible Roosevelt-themed presentation details: system-aware light/dark modes, course
  header identities, self-hosted fonts and icons, and clear internal versus external link marks.
- Added a bounded live-link checker for all public `site_docs/` Markdown while retaining offline
  fast tests and a production-shaped build and browser validation path.

### Notable fixes

- Replaced retired university and state destinations, corrected external course links, and retained
  the current Schaumburg Disability Services contact in the shared student-resources page.
- Corrected the public-content boundary so ignored local `raw/` reference material does not block a
  build, while Git-tracked `raw/` content remains a fail-closed error.
- Removed a footer styling override and exact social-profile assertion that were introduced only to
  satisfy a fragile test; route-wide accessibility auditing remains the durable browser evidence.
- Shared the course-theme validation path between MkDocs and document generation, and refreshed
  the source, route, and artifact-parity documentation to match the implemented pipeline.

### Compatibility notes

- Complete syllabi no longer contain the niche Extra credit movie catalog. They link to its public
  website page instead, so students can still reach the approved-list reference.
- The Extra credit workflow now uses category-specific Google Forms rather than submitted
  write-ups, SafeAssign, word-count, or similarity-score requirements.

### Validation

- Ran the local `all_test.sh` front door: offline pytest, live Google Sheets export, strict MkDocs
  build, PDF/DOCX include parity, production rebuild, and Playwright accessibility audit.
- Ran the bounded live-link audit across the public Markdown tree; an authentication-required form
  correctly reports its HTTP 401 boundary rather than a missing destination.
