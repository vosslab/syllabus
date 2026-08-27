"""Check that vendored header regions in consumer-owned docs stay well formed.

Propagation seeds `docs/HUMAN_GUIDANCE.md` and `docs/DESIGN_DECISIONS.md`, then
refreshes the marked region inside each on every sync while this repository's own
entries stay untouched.

Two situations this catches, both of which propagation alone leaves quiet:

- A file whose marker pair became ambiguous (unpaired, duplicated, or reversed).
  Propagation reports an error and leaves such a file alone by design, so the
  file keeps its stale header until somebody notices the error line.
- A file rewritten wholesale, losing its header. The next sync restores it, but
  until then the file carries no statement of what belongs in it.

Scope is deliberately narrow: presence and shape of the region. Section names and
entry length are guidance in `docs/REPO_STYLE.md`, not a contract, and they vary
by repository.
"""

# Standard Library
import os

# PIP3 modules
import pytest

# local repo modules
import file_utils


REPO_ROOT = file_utils.get_repo_root()

# Marker pair written by propagation. Keep these strings in step with the
# template's vendored headers.
HEADER_START_MARKER = '<!-- VENDORED HEADER: START -->'
HEADER_END_MARKER = '<!-- VENDORED HEADER: END -->'

# Consumer-owned docs that carry a vendored header region.
HEADER_DOCS = (
	'docs/HUMAN_GUIDANCE.md',
	'docs/DESIGN_DECISIONS.md',
)


#============================================
def read_doc_lines(file_rel: str) -> list[str]:
	"""
	Return the lines of a header-carrying doc, skipping the test when it is absent.

	A repository that has not synced yet legitimately lacks these files; the next
	propagation run seeds them.

	Args:
		file_rel (str): Repo-relative POSIX path of the doc.

	Returns:
		list[str]: Lines of the file, without line endings.
	"""
	path = os.path.join(REPO_ROOT, file_rel)
	if not os.path.isfile(path):
		pytest.skip(f"{file_rel} is not present yet; propagation seeds it")
	with open(path, 'r', encoding='utf-8') as file_handle:
		text = file_handle.read()
	return text.splitlines()


#============================================
@pytest.mark.parametrize("file_rel", HEADER_DOCS)
def test_vendored_header_is_well_formed(file_rel: str) -> None:
	"""The doc carries exactly one marker pair, in order."""
	lines = read_doc_lines(file_rel)
	start_lines = [num for num, line in enumerate(lines, 1) if line.strip() == HEADER_START_MARKER]
	end_lines = [num for num, line in enumerate(lines, 1) if line.strip() == HEADER_END_MARKER]
	message = (
		f"{file_rel}: expected one vendored header region.\n"
		f"  start markers on lines: {start_lines}\n"
		f"  end markers on lines:   {end_lines}\n"
		f"  Run propagation to restore the header, or repair the markers by hand "
		f"when the pair is ambiguous."
	)
	assert (len(start_lines), len(end_lines)) == (1, 1), message
	assert start_lines[0] < end_lines[0], message


#============================================
@pytest.mark.parametrize("file_rel", HEADER_DOCS)
def test_vendored_header_carries_text(file_rel: str) -> None:
	"""The region holds instruction text rather than an empty shell."""
	lines = read_doc_lines(file_rel)
	start_index = next(num for num, line in enumerate(lines) if line.strip() == HEADER_START_MARKER)
	end_index = next(num for num, line in enumerate(lines) if line.strip() == HEADER_END_MARKER)
	body_lines = [line for line in lines[start_index + 1:end_index] if line.strip()]
	message = f"{file_rel}: vendored header region is empty; run propagation to restore it"
	assert body_lines, message
