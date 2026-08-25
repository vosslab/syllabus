# Installation

## Requirements

- Python 3.12
- Pandoc for DOCX generation
- Pango for WeasyPrint text layout
- Poppler command-line tools
- Ripgrep

Node.js and Playwright Chromium are optional local dependencies for the browser accessibility
audit. They are not part of PDF or DOCX generation.

On macOS with Homebrew, install the system tools from the repository manifest:

```bash
brew bundle
```

Install the Python application and development dependencies in the environment used for this
repository:

```bash
source source_me.sh
python3 -m pip install -r pip_requirements.txt -r pip_requirements-dev.txt
```

Generate the tracked DOCX style reference only after intentionally changing document styles:

```bash
source source_me.sh
python3 pipeline/create_syllabus_reference_docx.py
```

The generated reference file is `templates/syllabus_reference.docx`. Routine course editing does
not require regenerating it.

To run the optional browser accessibility audit locally, install its dependency and Chromium once:

```bash
npm ci
npx playwright install chromium
```

## Bundled web font

The website self-hosts the upright and italic Atkinson Hyperlegible Next variable fonts from the
[official Google Fonts source](https://github.com/googlefonts/atkinson-hyperlegible-next). The two
WOFF2 files cover weights 200 through 800. The distribution includes its required SIL Open Font
License beside the font files. The Material configuration keeps remote fonts disabled. GitHub
Pages serves the font and license files with the rest of the static site.

## Verify the installation

```bash
source source_me.sh
python3 -m pytest tests/
python3 pipeline/build_site.py
./run_playwright_tests.sh
```

The complete build requires every core export tool. Pandoc creates the DOCX from portable assembled
Markdown and the reference document. Python-Markdown reads the extension configuration from
`mkdocs.yml` and creates small semantic HTML for WeasyPrint. WeasyPrint renders the PDF through the
system Pango text stack. The export pipeline requires neither an office suite nor a browser. Missing
converters fail with a direct error because a web-only result would not satisfy the archival
requirement.
