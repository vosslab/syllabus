# Standard Library
import sys
import pathlib

# PIP3 modules
import pytest

# local repo modules
import devel.bump_version


#============================================
def test_patch_updates_repo_and_cargo_versions(
	tmp_path: pathlib.Path,
	monkeypatch: pytest.MonkeyPatch,
) -> None:
	"""The patch action recognizes equivalent repo and Cargo versions."""
	cargo_toml = tmp_path / "Cargo.toml"
	version_file = tmp_path / "VERSION"
	cargo_toml.write_text(
		'[package]\nname = "demo"\nversion = "26.8.0"\nedition = "2024"\n',
		encoding="utf-8",
	)
	version_file.write_text("26.08\n", encoding="utf-8")
	monkeypatch.setattr(
		sys,
		"argv",
		[
			"bump_version.py",
			"patch",
			"--apply",
			"--base-dir",
			str(tmp_path),
		],
	)

	devel.bump_version.main()

	assert version_file.read_text(encoding="utf-8") == "26.08.1\n"
	assert 'version = "26.8.1"' in cargo_toml.read_text(encoding="utf-8")


#============================================
def test_set_version_synchronizes_rust_versions(
	tmp_path: pathlib.Path,
	monkeypatch: pytest.MonkeyPatch,
) -> None:
	"""An explicit CalVer synchronizes repo and Cargo representations."""
	cargo_toml = tmp_path / "Cargo.toml"
	cargo_lock = tmp_path / "Cargo.lock"
	version_file = tmp_path / "VERSION"
	cargo_toml.write_text(
		'[package]\nname = "demo"\nversion = "26.5.0"\nedition = "2024"\n',
		encoding="utf-8",
	)
	cargo_lock.write_text(
		'version = 4\n\n'
		'[[package]]\n'
		'name = "demo"\n'
		'version = "26.5.0"\n\n'
		'[[package]]\n'
		'name = "dependency"\n'
		'version = "1.2.3"\n',
		encoding="utf-8",
	)
	version_file.write_text("26.06\n", encoding="utf-8")
	monkeypatch.setattr(
		sys,
		"argv",
		[
			"bump_version.py",
			"-A",
			"--set-version",
			"26.07",
			"--base-dir",
			str(tmp_path),
		],
	)

	devel.bump_version.main()

	cargo_outputs = (
		cargo_toml.read_text(encoding="utf-8"),
		cargo_lock.read_text(encoding="utf-8"),
	)
	assert cargo_outputs == (
		'[package]\nname = "demo"\nversion = "26.7.0"\nedition = "2024"\n',
		'version = 4\n\n'
		'[[package]]\n'
		'name = "demo"\n'
		'version = "26.7.0"\n\n'
		'[[package]]\n'
		'name = "dependency"\n'
		'version = "1.2.3"\n',
	)
	assert version_file.read_text(encoding="utf-8") == "26.07\n"


#============================================
def test_set_version_updates_workspace_package_only(
	tmp_path: pathlib.Path,
	monkeypatch: pytest.MonkeyPatch,
) -> None:
	"""Workspace members inheriting a version keep version.workspace = true."""
	workspace_toml = tmp_path / "Cargo.toml"
	cargo_lock = tmp_path / "Cargo.lock"
	member_dir = tmp_path / "crates" / "demo"
	member_dir.mkdir(parents=True)
	member_toml = member_dir / "Cargo.toml"
	workspace_toml.write_text(
		'[workspace]\nmembers = ["crates/demo"]\n\n'
		'[workspace.package]\nversion = "26.5.0"\nedition = "2024"\n',
		encoding="utf-8",
	)
	member_toml.write_text(
		'[package]\nname = "demo"\nversion.workspace = true\n',
		encoding="utf-8",
	)
	cargo_lock.write_text(
		'version = 4\n\n'
		'[[package]]\n'
		'name = "demo"\n'
		'version = "26.5.0"\n',
		encoding="utf-8",
	)
	monkeypatch.setattr(
		sys,
		"argv",
		[
			"bump_version.py",
			"-A",
			"--set-version",
			"26.07",
			"--base-dir",
			str(tmp_path),
		],
	)

	devel.bump_version.main()

	workspace_outputs = (
		workspace_toml.read_text(encoding="utf-8"),
		cargo_lock.read_text(encoding="utf-8"),
	)
	assert workspace_outputs == (
		'[workspace]\nmembers = ["crates/demo"]\n\n'
		'[workspace.package]\nversion = "26.7.0"\nedition = "2024"\n',
		'version = 4\n\n'
		'[[package]]\n'
		'name = "demo"\n'
		'version = "26.7.0"\n',
	)
	assert member_toml.read_text(encoding="utf-8") == (
		'[package]\nname = "demo"\nversion.workspace = true\n'
	)
