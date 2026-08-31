# Install

Students use the published [Fall 2026 course syllabi](https://vosslab.github.io/syllabus/) in a
browser and do not install this repository. These steps prepare a maintainer checkout for public
course authoring, PDF and DOCX generation, and local validation.

## Requirements

- Bash, Python 3.12, and a Git work tree.
- Pandoc for DOCX generation.
- Pango for WeasyPrint text layout.
- Poppler command-line tools for PDF verification.
- Ripgrep for repository checks.

The supported maintainer workflow uses macOS and Homebrew. The repository `Brewfile` declares the
required system tools. Node.js and Playwright Chromium are optional and are needed only for the
browser audit.

## Install steps

From the repository root, install the declared system tools and Python dependencies:

```bash
brew bundle
source source_me.sh
python3 -m pip install -r pip_requirements.txt -r pip_requirements-dev.txt
```

`source_me.sh` must be sourced from Bash before local Python commands. It selects the repository
environment settings and makes the shared Markdown extension importable.

For the optional browser audit, install the locked Node dependencies and Playwright browsers once:

```bash
npm ci
./devel/setup_playwright.sh
```

## Renderer asset

The tracked `pipeline/syllabus_reference.docx` file defines DOCX renderer styles. Routine content
editing does not regenerate it. Regenerate it only after an intentional document-style change:

```bash
source source_me.sh
python3 pipeline/create_syllabus_reference_docx.py
```

## Verify install

Run the fast, offline repository lane:

```bash
source source_me.sh
python3 -m pytest tests/
```

To verify the document tools and live important-dates source as well, run the production build:

```bash
source source_me.sh
python3 pipeline/build_site.py
```

The production build refreshes the managed dates fragment, regenerates PDF and DOCX downloads, and
builds the MkDocs site in strict mode. It fails instead of publishing a stale or incomplete result.

## Troubleshooting

- If a build reports missing `pandoc`, `pdfinfo`, or `pdftotext`, rerun `brew bundle`.
- If it reports a missing PDF renderer, reinstall `pip_requirements.txt` and
  `pip_requirements-dev.txt` in the sourced environment.
- If it reports a missing `pipeline/syllabus_reference.docx`, run the renderer-asset command above.

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for date-sync, source-validation, browser, and
publication diagnosis.

## Known gaps

- TODO: Verify and document a supported non-macOS maintainer environment before presenting one as
  an alternative to the Homebrew workflow.

See [USAGE.md](USAGE.md) for authoring, build, review, and validation workflows.
