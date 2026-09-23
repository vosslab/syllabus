"""Refresh every online calendar snapshot from its public Google Sheets source."""

# Standard Library
import os
import sys
import argparse
import pathlib
import subprocess
import tempfile

# local repo modules
import build_lib.biostats_schedule
import build_lib.biotech_schedule
import build_lib.genetics_schedule
import build_lib.important_dates


#============================================
def parse_args() -> argparse.Namespace:
	"""Choose all local sources or the university-only production refresh."""
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument(
		"-c",
		"--calendar",
		dest="calendar",
		choices=("all", "university", "biostats", "biotech", "genetics"),
		default="all",
		help="refresh all configured calendars or only one calendar",
	)
	return parser.parse_args()


#============================================
def get_repo_root() -> pathlib.Path:
	"""Return the repository root reported by Git."""
	completed = subprocess.run(
		["git", "rev-parse", "--show-toplevel"],
		check=True,
		capture_output=True,
		text=True,
	)
	return pathlib.Path(completed.stdout.strip())


#============================================
def write_text_atomically(output_path: pathlib.Path, text: str) -> None:
	"""Replace one fixed calendar snapshot after its staged file is complete."""
	output_path.parent.mkdir(parents=True, exist_ok=True)
	with tempfile.TemporaryDirectory(
		prefix=f".{output_path.name}.",
		dir=output_path.parent,
	) as temporary_directory:
		staged_path = pathlib.Path(temporary_directory) / output_path.name
		staged_path.write_text(text, encoding="utf-8")
		# ASVS 5.3.2: destination paths are fixed by code, never spreadsheet content.
		# ASVS 16.5.2, 16.5.3: preserve the old snapshot until validated text is ready.
		os.replace(staged_path, output_path)
	return None


#============================================
def fix_markdown_ascii_compliance(markdown: str) -> str:
	"""Apply the repository's canonical text fixer to one rendered snapshot."""
	fixer_path = pathlib.Path(__file__).resolve().parents[2] / "tests" / "fix_ascii_compliance.py"
	if not fixer_path.is_file():
		raise FileNotFoundError(f"Missing canonical text fixer: {fixer_path}")
	with tempfile.TemporaryDirectory(prefix="calendar-ascii-fix.") as temporary_directory:
		staged_path = pathlib.Path(temporary_directory) / "calendar.md"
		staged_path.write_text(markdown, encoding="utf-8")
		completed = subprocess.run(
			[sys.executable, str(fixer_path), "--input", str(staged_path)],
			capture_output=True,
			text=True,
			check=False,
		)
		if completed.returncode not in (0, 2):
			diagnostic = completed.stderr.strip()
			raise ValueError(
				diagnostic or "Calendar text could not be made ISO-8859-1 compliant"
			)
		return staged_path.read_text(encoding="utf-8")


#============================================
def main() -> None:
	"""Validate online calendar sources, then publish their Markdown snapshots."""
	args = parse_args()
	repo_root = get_repo_root()
	outputs: list[tuple[pathlib.Path, str, str, int]] = []
	if args.calendar in ("all", "university"):
		markdown, entry_count = build_lib.important_dates.prepare_output()
		markdown = fix_markdown_ascii_compliance(markdown)
		outputs.append((
			repo_root / build_lib.important_dates.OUTPUT_RELATIVE_PATH,
			markdown,
			"university dates",
			entry_count,
		))
	if args.calendar in ("all", "biostats"):
		markdown, entry_count = build_lib.biostats_schedule.prepare_output()
		markdown = fix_markdown_ascii_compliance(markdown)
		outputs.append((
			repo_root / build_lib.biostats_schedule.OUTPUT_RELATIVE_PATH,
			markdown,
			"Biostatistics schedule entries",
			entry_count,
		))
	if args.calendar in ("all", "biotech"):
		markdown, entry_count = build_lib.biotech_schedule.prepare_output()
		markdown = fix_markdown_ascii_compliance(markdown)
		outputs.append((
			repo_root / build_lib.biotech_schedule.OUTPUT_RELATIVE_PATH,
			markdown,
			"BIOL 480 schedule entries",
			entry_count,
		))
	if args.calendar in ("all", "genetics"):
		markdown, entry_count = build_lib.genetics_schedule.prepare_output()
		markdown = fix_markdown_ascii_compliance(markdown)
		outputs.append((
			repo_root / build_lib.genetics_schedule.OUTPUT_RELATIVE_PATH,
			markdown,
			"Genetics schedule entries",
			entry_count,
		))
	for output_path, markdown, label, entry_count in outputs:
		write_text_atomically(output_path, markdown)
		relative_path = output_path.relative_to(repo_root)
		print(f"Updated {relative_path} with {entry_count} {label}.")
	return None


if __name__ == "__main__":
	main()
