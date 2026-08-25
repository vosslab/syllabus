# starter_repo_template
Canonical bootstrap scaffolding for new Python repositories: ready-to-use repo policy docs, Python style rules, licensing boundaries, and pytest lint checks so projects start consistent before any project-specific code is added.

Only `README.md` and `docs/CHANGELOG.md` are intentionally repository-specific; every other file is designed to remain generic for downstream template users.

## Documentation

- [meta/docs/REPO_TYPE.md](meta/docs/REPO_TYPE.md): Repository type marker format, available
  types, inheritance, and multi-type behavior.
- [docs/REPO_STYLE.md](docs/REPO_STYLE.md): Repository structure, naming, versioning, dependency manifest, and licensing conventions.
- [docs/PYTHON_STYLE.md](docs/PYTHON_STYLE.md): Python implementation rules for formatting, structure, imports, argparse, and testing.
- [docs/PYTEST_STYLE.md](docs/PYTEST_STYLE.md): Pytest test-writing rules, commands, and failure triage.
- [templates/website/docs/PLAYWRIGHT_USAGE.md](templates/website/docs/PLAYWRIGHT_USAGE.md): Browser-driven tests using Playwright in `tests/playwright/`.
- [docs/E2E_TESTS.md](docs/E2E_TESTS.md): End-to-end test conventions; shell/Python E2E lives in `tests/e2e/`, browser E2E in `tests/playwright/`.
- [docs/MARKDOWN_STYLE.md](docs/MARKDOWN_STYLE.md): Markdown writing and formatting conventions for repository documentation.
- [docs/AUTHORS.md](docs/AUTHORS.md): Canonical authorship and attribution metadata for template maintenance.
- [docs/CHANGELOG.md](docs/CHANGELOG.md): Repository-specific history of updates to this template.

## Template layout

File location is the primary routing determinant. Files under `docs/`, `tests/`, `devel/`, and `tools/` ship universally to every consumer repo. Files under `templates/<type>/` (e.g., `templates/typescript/`, `templates/python/`, `templates/rust/`) ship only to repos of that type. Root-level files ship only when listed in `ROOT_PROPAGATE_ALLOWLIST`. Template-only tooling lives under `meta/tools/`; it never propagates and is removed by `reset_repo.py` at consumer bootstrap. Propagation manifests live in `meta/propagation/manifests.yaml` (template-only; never ships to consumers).

## Quick start

Bootstrap a fresh clone (sets project type + licenses, installs canonical files):

```bash
python3 reset_repo.py
```

The interview asks for repo types, licenses, PyPI packaging, staging, and commit choices.
Repo types accept names, comma-separated lists, or letter runs (`python`, `python,rust`, or `pr`).
`--dry-run` previews the reset; `--config <file>` loads answers from JSON.

Run the fast test suite:

```bash
pytest tests/
```

Non-browser end-to-end tests live under `tests/e2e/` per [docs/E2E_TESTS.md](docs/E2E_TESTS.md) when present; this repo does not currently ship any. Each runner is self-contained -- invoke them individually with `bash tests/e2e/e2e_<name>.sh`.

Run browser-driven Playwright tests (see [templates/website/docs/PLAYWRIGHT_USAGE.md](templates/website/docs/PLAYWRIGHT_USAGE.md)):

```bash
node tests/playwright/test_example.mjs
```
