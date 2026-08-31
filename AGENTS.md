# Required guidance

- docs/REPO_STYLE.md, docs/HUMAN_GUIDANCE.md, docs/CHANGELOG.md
- docs/PYTHON_STYLE.md, docs/PYTEST_STYLE.md, docs/MARKDOWN_STYLE.md
- docs/CODE_ARCHITECTURE.md, docs/FILE_STRUCTURE.md, docs/USAGE.md
- docs/FILE_FORMATS.md, docs/GITHUB_PAGES_BUILD.md

# Repository boundaries

- `site_docs/fall_2026/` is the only live course and complete-syllabus authority.
- `site_docs/EXTRA_CREDIT_MOVIES.md` is the approved global website-only exception.
- Keep tracked sources and published MkDocs content public-only. Ignored `raw/` may hold private
  internal references; never track or publish them. Private course delivery belongs in Blackboard.
- Treat `site/`, `site_docs/downloads/`, `site_docs/generated/`, and `output/` as generated output.
- Only humans commit.

# Python runtime

- Use Python 3.12 through `source source_me.sh && python3`.
- Homebrew modules: `/opt/homebrew/lib/python3.12/site-packages/`.
