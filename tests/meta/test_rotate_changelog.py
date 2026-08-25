"""Tests for changelog archive partitioning and its line-count policy."""

# Standard Library
import pathlib

# PIP3 modules
import pytest

# local repo modules
import changelog_lib
import rotate_changelog


#============================================

def make_block(date: str, line_count: int) -> changelog_lib.DayBlock:
	"""Build a day block with a controlled physical line count.

	Args:
		date: Valid day-block date.
		line_count: Physical line count to place in the raw block.

	Returns:
		DayBlock whose raw text contains the requested number of lines.
	"""
	if line_count < 1:
		raise ValueError("line_count must be at least one.")
	filler_count = line_count - 1
	raw_text = f"## {date}\n" + ("filler\n" * filler_count)
	return changelog_lib.DayBlock(
		date=date,
		raw_text=raw_text,
		source="<test>",
		lineno=1,
	)


#============================================

@pytest.mark.parametrize(
	("line_count", "expected"),
	((800, False), (801, True)),
	ids=("800-lines-waits", "801-lines-rotates"),
)
def test_rotation_needed_starts_only_above_default_threshold(
		line_count: int, expected: bool,
		) -> None:
	"""Rotation begins after, rather than at, the 800-line default."""
	result = rotate_changelog.rotation_needed(
		line_count, rotate_changelog.THRESHOLD_DEFAULT,
	)
	assert result is expected


#============================================

def test_partition_archive_blocks_targets_range_without_hitting_limit() -> None:
	"""Whole blocks form two 850-line archives when the target permits it."""
	blocks = [
		make_block("2026-08-04", 450),
		make_block("2026-08-03", 400),
		make_block("2026-08-02", 450),
		make_block("2026-08-01", 400),
	]
	groups = rotate_changelog.partition_archive_blocks(blocks)
	line_counts = [rotate_changelog.count_archive_lines(group) for group in groups]
	assert line_counts == [850, 850]
	assert max(line_counts) < rotate_changelog.ARCHIVE_LINE_LIMIT


#============================================

def test_partition_archive_blocks_refuses_an_oversized_day_block() -> None:
	"""A 1000-line day block fails before an invalid archive can be written."""
	blocks = [make_block("2026-08-04", 1000)]
	with pytest.raises(RuntimeError, match="cannot be archived"):
		rotate_changelog.partition_archive_blocks(blocks)


#============================================

def test_compute_archive_path_reserves_letters_for_same_month(tmp_path: pathlib.Path) -> None:
	"""Multiple groups from one month receive different archive paths."""
	group = [make_block("2026-08-04", 800)]
	first_path = rotate_changelog.compute_archive_path(group, str(tmp_path))
	second_path = rotate_changelog.compute_archive_path(group, str(tmp_path), [first_path])
	assert [first_path, second_path] == [
		str(tmp_path / "CHANGELOG-2026-08a.md"),
		str(tmp_path / "CHANGELOG-2026-08b.md"),
	]
