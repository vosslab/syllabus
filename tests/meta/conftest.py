"""Template-only pytest collection settings.

Root ``pytest.ini`` supplies the import paths used by the template test suite.
Meta tests can therefore import repo modules and shared test helpers normally.

DUAL-CONFTEST MAP -- this repo carries two conftest.py files with distinct
roles. Read this before touching either one.

  tests/conftest.py (the SHIPPING seed)
    - Handled by repolib.files.merge_conftest, which additively appends its
      three managed blocks (collect_ignore, REPO_HYGIENE_FILTERS,
      OPTIONAL_HELPERS_MENU) into every consumer repo's tests/conftest.py.
    - Because its literal text is the consumer seed, it must hold NO
      repo-specific data. In particular REPO_HYGIENE_FILTERS stays {} here:
      a populated registry would bake this template's glob paths into every
      freshly bootstrapped consumer. Cross-overlay doc references are fixed
      by the backticked-name convention (see docs/MARKDOWN_STYLE.md usage in
      templates/), never by adding exclusions to that registry.

  tests/meta/conftest.py (THIS file, template-meta, never ships)
    - The whole tests/meta/ subtree is excluded from propagation ('meta' is
      a META_DIRS path component), as is root pytest.ini. Neither ships to a
      consumer repo.
    - This file must NOT define REPO_HYGIENE_FILTERS. The Layer-2 registry
      loader (file_utils._load_repo_hygiene_filters) reads tests/conftest.py
      by explicit file path precisely because this same-basename file once
      shadowed sys.modules["conftest"] under full-suite collection order
      ("meta" sorts before "test_") and silently emptied the registry.
"""
# Exclude the template-meta E2E harness from the template's own pytest run.
# This lives here (template-meta, never propagated) rather than in the root
# tests/conftest.py, whose collect_ignore block ships to consumer repos that
# have no tests/meta/ tree.
collect_ignore = ["e2e"]

import file_utils

REPO_ROOT = file_utils.get_repo_root()
