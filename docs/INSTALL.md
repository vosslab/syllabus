# Install

The public student site requires no installation. Open the
[Fall 2026 course syllabi](https://vosslab.github.io/syllabus/) in a browser. The steps below set up
a maintainer checkout for authoring, document generation, and validation.

## Requirements

- Python 3.12
- Pandoc for DOCX generation
- Pango for WeasyPrint text layout
- Poppler command-line tools
- Ripgrep

Node.js and Playwright Chromium are optional local dependencies for the browser accessibility
audit and README screenshot capture. They are not part of PDF or DOCX generation.

On macOS with Homebrew, install the system tools from the repository manifest:

```bash
brew bundle
```

Install the runtime and local validation dependencies in the repository Python environment:

```bash
source source_me.sh
python3 -m pip install -r pip_requirements.txt -r pip_requirements-dev.txt
```

Generate the tracked DOCX style reference only after intentionally changing document styles:

```bash
source source_me.sh
python3 pipeline/create_syllabus_reference_docx.py
```

The generated reference file is `pipeline/syllabus_reference.docx`. It is a DOCX renderer asset,
not syllabus content, and routine course editing does not require regenerating it.

Course content is maintained only in the active term under `site_docs/`. The build regenerates
`site_docs/downloads/` and `site/`; both directories are ignored outputs and are never editing
sources.

To run the optional browser accessibility audit locally, install its dependencies and Chromium
once:

```bash
npm ci
./devel/setup_playwright.sh
```

## Bundled web fonts

The website self-hosts the upright and italic Atkinson Hyperlegible Next variable fonts from the
[official Google Fonts source](https://github.com/googlefonts/atkinson-hyperlegible-next). The two
WOFF2 files cover weights 200 through 800. The distribution includes its required SIL Open Font
License beside the font files.

The website also self-hosts the Font Awesome 6 Free solid font used for the PDF and Word file-type
icons beside complete-syllabus links. Its WOFF2 file matches the established local installation in
the Biology Problems website, and its Font Awesome Free license is stored beside the font. The
Material configuration keeps remote fonts disabled. GitHub Pages serves the fonts and license files
with the rest of the static site.

## Verify install

```bash
source source_me.sh
python3 -m pytest tests/
```

This fast, offline lane verifies the installed Python dependencies. Run the production build when
the document tools and live Google Sheets connection also need verification:

```bash
source source_me.sh
python3 pipeline/build_site.py
```

The production build refreshes important dates from Google Sheets, generates DOCX and PDF files,
and builds the MkDocs site in strict mode. Missing converters or an unavailable spreadsheet fail
directly so publication cannot use incomplete or stale output.

See [CODE_ARCHITECTURE.md](CODE_ARCHITECTURE.md) for the full component flow and
[USAGE.md](USAGE.md) for authoring and maintenance workflows.
