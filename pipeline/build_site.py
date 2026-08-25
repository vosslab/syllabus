"""Build complete syllabus downloads and the strict MkDocs site."""

# Standard Library
import pathlib
import subprocess
import sys


#============================================
def get_repo_root() -> pathlib.Path:
	"""Return the repository root reported by Git."""
	completed = subprocess.run(
		["git", "rev-parse", "--show-toplevel"],
		check=True,
		capture_output=True,
		text=True,
	)
	repo_root = pathlib.Path(completed.stdout.strip())
	return repo_root


#============================================
def main() -> None:
	"""Build verified downloads before building the static site."""
	repo_root = get_repo_root()
	subprocess.run(
		[sys.executable, "pipeline/build_syllabi.py"],
		cwd=repo_root,
		check=True,
	)
	subprocess.run(
		[sys.executable, "-m", "mkdocs", "build", "--strict"],
		cwd=repo_root,
		check=True,
	)
	return None


if __name__ == "__main__":
	main()
