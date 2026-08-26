# GitHub Pages build

This page is the canonical explanation of the GitHub Pages publication process. The workflow
source of truth is [../.github/workflows/deploy-pages.yml](../.github/workflows/deploy-pages.yml).

## CI boundary

The human owner chose build-only GitHub Pages CI. GitHub Actions generates and deploys the
production artifact; it does not run pytest, the export E2E assertions, or Playwright. Those local
lanes enforce semantic, editorial, privacy, accessibility, and interface expectations without
making them prerequisites for publication. Do not add them back as CI or release gates without a
new explicit human decision.

## Required architecture

Every push to `main` and every manual workflow dispatch runs one publication pipeline:

```text
build job
  |-- check out the repository
  |-- install Python 3.12, runtime dependencies, and document tools
  |-- refresh live important dates
  |-- build and validate every PDF and DOCX syllabus
  |-- build the MkDocs site in strict mode
  |-- upload the site artifact
  `-- success
        `-- deploy job publishes the artifact to GitHub Pages
```

The `deploy` job depends on the `build` job. Pages publishes whenever the deployable artifact can be
generated and uploaded. Local test lanes provide semantic and browser confidence independently.

## Build job

The Python steps generate the publication artifact. Keep all of these steps in the `build` job:

1. `actions/checkout` provides the tracked source tree.
2. `actions/setup-python` selects Python 3.12 and caches `pip_requirements.txt`.
3. The system-package step installs Pandoc, Poppler, and the Pango/Harfbuzz libraries required for
   document rendering and validation.
4. The Python dependency step installs only application dependencies.
5. `actions/configure-pages` prepares GitHub Pages metadata.
6. `python3 pipeline/build_site.py` runs the production build front door.
7. `actions/upload-pages-artifact` uploads only the generated `site/` directory.

The production builder refreshes the ignored important-dates fragment from the live Google Sheet,
rebuilds all syllabus downloads, and runs `mkdocs build --strict`. These operations create files
linked by the public site, so they are part of artifact generation rather than a separate semantic
test lane. The date refresh deliberately fails closed when the canonical remote source is
unavailable.

## Deploy job

The `deploy` job uses the protected `github-pages` environment and runs after `build` succeeds. It
needs `pages: write` and `id-token: write` workflow permissions. Preserve the unconditional path
from a successful artifact build to deployment.

Workflow-level `concurrency` serializes Pages publication. One run owns the `pages` deployment
group while at most one newer run remains pending. Because `cancel-in-progress` is false, the active
run completes; another push can replace an older pending run, retaining the newest candidate rather
than deploying every intermediate push.

## Local test lanes

Run all local maintainer tests through the repository front door:

```bash
./all_test.sh
```

The script runs pytest, the export E2E assertions and strict site build, then the Pages production
builder and Playwright. Both build paths refresh the live Google Sheets dates, which exercises the
E2E orchestration and the production front door. Run the lanes individually for focused diagnosis:

```bash
source source_me.sh && python3 -m pytest tests/
source source_me.sh && python3 tests/e2e/e2e_include_parity.py
```

Install Playwright Chromium once, then run the browser lane explicitly:

```bash
npm ci
./devel/setup_playwright.sh
./run_playwright_tests.sh --build
```

The export/include E2E adds stale-file, extracted-PDF, credential, editorial-marker, and
cross-format include assertions around the production build. The Playwright `--build` form creates
the production-shaped local site and downloads before checking the rendered interface, responsive
behavior, links, and accessibility findings. The browser runner uses a nonzero result as a clear
local maintainer signal. This separation lets artifact generation determine Pages availability
while the local lanes provide broader repository and interface confidence.

## Reproduce publication locally

Run the same artifact builder before changing deployment behavior:

```bash
source source_me.sh && python3 pipeline/build_site.py
```

The builder uses the live important-dates source and creates the same `site/` tree uploaded by the
workflow. Run the three local test lanes separately when validating repository changes.

## Diagnose failed runs

Start with the run state before editing the workflow. Open the repository's **Actions** tab, select
**Build and deploy syllabus site**, and compare the newest run with the last successful run.

- `startup_failure` with zero jobs means no repository command ran. Check
  [GitHub Status](https://www.githubstatus.com/) and compare the workflow file with the last
  successful commit before changing build code.
- A queued run with zero jobs can indicate a GitHub Actions or Pages incident, runner capacity, or
  the workflow concurrency group. Check platform status and other active runs first.
- A failed `build` job is a repository or dependency failure. Open the first failed step and
  reproduce its exact local command.
- A failed `deploy` job after a successful `build` points to Pages permissions, environment state,
  artifact handling, or the deployment action rather than syllabus generation.
- A successful run with an old public site requires checking the deployed run's head SHA, Pages
  repository settings, deployment URL, and browser cache.

For a zero-job platform failure, preserve the Python artifact-generation steps and investigate the
platform state. Use the local runners for pytest, export E2E, and Playwright verification.
