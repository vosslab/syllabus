"""Tests for reset_repo.py repolib.reset_answers.resolve_license() helper."""

import pytest

import repolib.reset_answers


class TestResolveLicenseCodeLicenses:
	def test_lowercase_aliases(self) -> None:
		assert repolib.reset_answers.resolve_license("m", repolib.reset_answers.CODE_LICENSES, repolib.reset_answers.CODE_ALIASES) == "MIT"
		assert repolib.reset_answers.resolve_license("a", repolib.reset_answers.CODE_LICENSES, repolib.reset_answers.CODE_ALIASES) == "Apache-2.0"
		assert repolib.reset_answers.resolve_license("l", repolib.reset_answers.CODE_LICENSES, repolib.reset_answers.CODE_ALIASES) == "LGPL-3.0"
		assert repolib.reset_answers.resolve_license("g", repolib.reset_answers.CODE_LICENSES, repolib.reset_answers.CODE_ALIASES) == "GPL-3.0"
		assert repolib.reset_answers.resolve_license("ag", repolib.reset_answers.CODE_LICENSES, repolib.reset_answers.CODE_ALIASES) == "AGPL-3.0"
		assert repolib.reset_answers.resolve_license("mp", repolib.reset_answers.CODE_LICENSES, repolib.reset_answers.CODE_ALIASES) == "MPL-2.0"

	def test_uppercase_aliases(self) -> None:
		assert repolib.reset_answers.resolve_license("MIT", repolib.reset_answers.CODE_LICENSES, repolib.reset_answers.CODE_ALIASES) == "MIT"
		assert repolib.reset_answers.resolve_license("A", repolib.reset_answers.CODE_LICENSES, repolib.reset_answers.CODE_ALIASES) == "Apache-2.0"
		assert repolib.reset_answers.resolve_license("AG", repolib.reset_answers.CODE_LICENSES, repolib.reset_answers.CODE_ALIASES) == "AGPL-3.0"
		assert repolib.reset_answers.resolve_license("MP", repolib.reset_answers.CODE_LICENSES, repolib.reset_answers.CODE_ALIASES) == "MPL-2.0"

	def test_case_insensitive_aliases(self) -> None:
		assert repolib.reset_answers.resolve_license("M", repolib.reset_answers.CODE_LICENSES, repolib.reset_answers.CODE_ALIASES) == "MIT"
		assert repolib.reset_answers.resolve_license("Ag", repolib.reset_answers.CODE_LICENSES, repolib.reset_answers.CODE_ALIASES) == "AGPL-3.0"

	def test_unique_prefix(self) -> None:
		assert repolib.reset_answers.resolve_license("mit", repolib.reset_answers.CODE_LICENSES, repolib.reset_answers.CODE_ALIASES) == "MIT"
		assert repolib.reset_answers.resolve_license("apache", repolib.reset_answers.CODE_LICENSES, repolib.reset_answers.CODE_ALIASES) == "Apache-2.0"
		assert repolib.reset_answers.resolve_license("gp", repolib.reset_answers.CODE_LICENSES, repolib.reset_answers.CODE_ALIASES) == "GPL-3.0"
		assert repolib.reset_answers.resolve_license("LGPL", repolib.reset_answers.CODE_LICENSES, repolib.reset_answers.CODE_ALIASES) == "LGPL-3.0"

	def test_ambiguous_prefix_raises(self) -> None:
		with pytest.raises(ValueError):
			repolib.reset_answers.resolve_license("c", repolib.reset_answers.CODE_LICENSES, repolib.reset_answers.CODE_ALIASES)

	def test_unknown_token_raises(self) -> None:
		with pytest.raises(ValueError):
			repolib.reset_answers.resolve_license("z", repolib.reset_answers.CODE_LICENSES, repolib.reset_answers.CODE_ALIASES)
		with pytest.raises(ValueError):
			repolib.reset_answers.resolve_license("xyz", repolib.reset_answers.CODE_LICENSES, repolib.reset_answers.CODE_ALIASES)

	def test_empty_input_no_default_raises(self) -> None:
		with pytest.raises(ValueError):
			repolib.reset_answers.resolve_license("", repolib.reset_answers.CODE_LICENSES, repolib.reset_answers.CODE_ALIASES)

	def test_empty_input_with_default_returns_default(self) -> None:
		assert repolib.reset_answers.resolve_license("", repolib.reset_answers.CODE_LICENSES, repolib.reset_answers.CODE_ALIASES, default="MIT") == "MIT"


class TestResolveLicenseDocsLicenses:
	def test_lowercase_aliases_docs(self) -> None:
		assert repolib.reset_answers.resolve_license("cb", repolib.reset_answers.DOCS_LICENSES, repolib.reset_answers.DOCS_ALIASES) == "CC-BY-4.0"
		assert repolib.reset_answers.resolve_license("cs", repolib.reset_answers.DOCS_LICENSES, repolib.reset_answers.DOCS_ALIASES) == "CC-BY-SA-4.0"
		assert repolib.reset_answers.resolve_license("n", repolib.reset_answers.DOCS_LICENSES, repolib.reset_answers.DOCS_ALIASES) == "none"

	def test_uppercase_aliases_docs(self) -> None:
		assert repolib.reset_answers.resolve_license("CB", repolib.reset_answers.DOCS_LICENSES, repolib.reset_answers.DOCS_ALIASES) == "CC-BY-4.0"
		assert repolib.reset_answers.resolve_license("CS", repolib.reset_answers.DOCS_LICENSES, repolib.reset_answers.DOCS_ALIASES) == "CC-BY-SA-4.0"
		assert repolib.reset_answers.resolve_license("N", repolib.reset_answers.DOCS_LICENSES, repolib.reset_answers.DOCS_ALIASES) == "none"

	def test_unique_prefix_docs(self) -> None:
		assert repolib.reset_answers.resolve_license("cc-by-4", repolib.reset_answers.DOCS_LICENSES, repolib.reset_answers.DOCS_ALIASES) == "CC-BY-4.0"
		assert repolib.reset_answers.resolve_license("none", repolib.reset_answers.DOCS_LICENSES, repolib.reset_answers.DOCS_ALIASES) == "none"

	def test_ambiguous_prefix_cc_raises(self) -> None:
		with pytest.raises(ValueError):
			repolib.reset_answers.resolve_license("cc", repolib.reset_answers.DOCS_LICENSES, repolib.reset_answers.DOCS_ALIASES)

	def test_empty_input_with_docs_default(self) -> None:
		assert repolib.reset_answers.resolve_license("", repolib.reset_answers.DOCS_LICENSES, repolib.reset_answers.DOCS_ALIASES, default="CC-BY-4.0") == "CC-BY-4.0"
