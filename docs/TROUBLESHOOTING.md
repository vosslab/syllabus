# Troubleshooting

Use this guide to diagnose local builds, exports, link checks, browser checks, and Pages
publication. Run commands from the repository root with the configured Python environment.

## Find the failing lane

`all_test.sh` stops at its first failed phase. Read that phase banner, then rerun only the
corresponding command so the original error remains visible:

```bash
source source_me.sh && python3 -m pytest tests/
source source_me.sh && python3 tests/e2e/e2e_include_parity.py
./run_playwright_tests.sh --build
```

The fast pytest lane is offline. The export E2E and production build refresh the important dates
from Google Sheets, and the Playwright lane needs the generated static site. See
[TESTS_README.md](../tests/TESTS_README.md) and [GITHUB_PAGES_BUILD.md](GITHUB_PAGES_BUILD.md) for
the test-tier and build-boundary details.

## Repair build prerequisites

If document generation reports a missing `pandoc`, `pdfinfo`, or `pdftotext`, install the
repository's Homebrew requirements and retry the build:

```bash
brew bundle
source source_me.sh && python3 -m pip install -r pip_requirements.txt -r pip_requirements-dev.txt
```

If it reports a missing PDF renderer, install the Python requirements with the second command.
If it reports a missing `pipeline/syllabus_reference.docx`, regenerate that tracked renderer asset:

```bash
source source_me.sh && python3 pipeline/create_syllabus_reference_docx.py
```

See [INSTALL.md](INSTALL.md) for the supported maintainer environment and
[USAGE.md](USAGE.md) for the export workflow.

## Refresh important dates

The production builder fails closed when it cannot retrieve or validate the fixed Google Sheets
CSV export. Run the importer directly to expose its specific message:

```bash
source source_me.sh && python3 pipeline/sync_important_dates.py
```

For a schema, date, weekday, checkbox, or chronological-order error, correct the first worksheet
of the canonical Google Sheet rather than editing
`site_docs/generated/FALL_2026_IMPORTANT_DATES.md`. That fragment is ignored generated output and
is replaced only after the complete response validates. For an unavailable export, restore network
access or Google Sheets availability, then rerun the importer; do not publish an older calendar.

## Correct source validation errors

Complete-syllabus content must remain under `site_docs/fall_2026/`, apart from the documented
global movie catalog. A build error about tracked `raw/` content means a local reference file was
added to Git; remove it from version control while retaining the ignored local reference if needed.
A build error about `templates/` means Markdown or YAML syllabus content was placed in a second
authority tree; move the canonical content into `site_docs/`.

For an include, table, manifest, or required-learning-section error, correct the named source file
instead of editing generated DOCX, PDF, download, or site output. The allowed include form, table
rules, and manifest contract are documented in [FILE_FORMATS.md](FILE_FORMATS.md); authoring
locations are listed in [USAGE.md](USAGE.md).

## Diagnose link failures

Check public HTTP(S) links without adding network work to pytest:

```bash
source source_me.sh && python3 pipeline/check_links.py
```

The report identifies every failing URL and source line. Replace or correct failed destinations in
the tracked Markdown source, then rerun the checker. `AUTH 401` means the destination requires
authentication; it is reported separately and does not by itself mark the link as failed. The
checker follows redirects and also detects common error pages that return HTTP 200. See
[USAGE.md](USAGE.md) for scope and command options.

## Run browser checks

If Playwright reports that `npm` is missing, install Node.js. If its dependencies or Chromium are
missing, prepare them once:

```bash
npm ci
./devel/setup_playwright.sh
```

Then rerun `./run_playwright_tests.sh --build`. The `--build` option refreshes dates and creates a
production-shaped site before the browser opens it. Treat reported accessibility findings as
maintainer work to review, then confirm the rendered result with the same browser command.

If macOS denies Chromium's test-server port while this runner starts, rerun the browser lane outside
the restricted sandbox. This is an execution-environment failure, not evidence of a syllabus-site
failure; the same full local gate has passed outside that boundary.

## Investigate Pages publication

For a failed or stale public deployment, first inspect the newest **Build and deploy syllabus
site** run in GitHub Actions and compare it with the last successful run. A failed `build` job
should be reproduced locally using its first failed command. A failed `deploy` job after a
successful build points to Pages permissions, environment state, or artifact handling. A successful
run with an old site requires checking the deployed commit SHA, Pages settings, deployment URL, and
browser cache. The detailed decision path is in
[GITHUB_PAGES_BUILD.md](GITHUB_PAGES_BUILD.md).
