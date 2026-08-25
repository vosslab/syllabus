"""Resolve reset configuration from interactive prompts or JSON answers."""

# Standard Library
import dataclasses
import json
import os
import sys

# local repo modules
import repolib.repo
import repolib.model
import meta.tools.detect_repo_type as detect_repo_type

CODE_LICENSES = ["MIT", "Apache-2.0", "LGPL-3.0", "GPL-3.0", "AGPL-3.0", "MPL-2.0"]
DOCS_LICENSES = ["CC-BY-4.0", "CC-BY-SA-4.0", "none"]

CODE_ALIASES = {
	"m": "MIT",
	"a": "Apache-2.0",
	"l": "LGPL-3.0",
	"g": "GPL-3.0",
	"ag": "AGPL-3.0",
	"mp": "MPL-2.0",
}

DOCS_ALIASES = {
	"cb": "CC-BY-4.0",
	"cs": "CC-BY-SA-4.0",
	"n": "none",
}


#============================================
def resolve_license(
	user_input: str,
	canonical: list,
	aliases: dict,
	default: str | None = None,
) -> str:
	"""Resolve a license answer through an alias or unique prefix.

	Args:
		user_input: License answer entered by a person or read from configuration.
		canonical: Available canonical license names.
		aliases: Short license answers mapped to their canonical names.
		default: License used when the answer is empty, if one is available.

	Returns:
		The matching canonical license name.

	Raises:
		ValueError: The answer is empty without a default, unknown, or ambiguous.
	"""
	token = user_input.strip().lower()
	if token == "":
		if default is None:
			raise ValueError("empty license input; no default available")
		return default
	if token in aliases:
		return aliases[token]
	matches = [name for name in canonical if name.lower().startswith(token)]
	if len(matches) == 1:
		return matches[0]
	raise ValueError(f"ambiguous or unknown license: {user_input!r}")


#============================================
def resolve_code_license(user_input: str) -> str:
	"""Resolve a required code license answer.

	Args:
		user_input: Code-license answer to resolve.

	Returns:
		The matching canonical code license.

	Raises:
		ValueError: The answer does not identify one code license.
	"""
	code_license = resolve_license(user_input, CODE_LICENSES, CODE_ALIASES)
	return code_license


#============================================
def resolve_docs_license(user_input: str) -> str:
	"""Resolve an optional documentation license answer.

	Args:
		user_input: Documentation-license answer to resolve.

	Returns:
		The matching canonical documentation license.

	Raises:
		ValueError: The answer does not identify one documentation license.
	"""
	docs_license = resolve_license(user_input, DOCS_LICENSES, DOCS_ALIASES, default="none")
	return docs_license


#============================================
def normalize_project_type(raw: str, default: str) -> str:
	"""Normalize a raw project-type answer to a canonical marker.

	Several types may be declared as a comma-separated list or as a run of
	single-letter aliases. The result preserves declaration order, removes
	duplicates, and leaves ``all`` unexpanded.

	Args:
		raw: Project-type answer to normalize.
		default: Project type offered when the answer is empty.

	Returns:
		A comma-separated canonical project-type marker.

	Raises:
		SystemExit: The supplied answer contains an unknown project type.
	"""
	answer = raw.strip().lower()
	if answer == "":
		answer = default.strip().lower()
	if answer == "":
		return default

	declared_types: list[str] = []
	for piece in answer.split(","):
		piece_types = repolib.repo.expand_choice_piece(piece)
		if piece_types is None:
			sys.exit(f"Invalid project type: {raw!r}")
		for declared_type in piece_types:
			if declared_type not in declared_types:
				declared_types.append(declared_type)
	return ",".join(declared_types)


#============================================
def resolve_project_type(repo_root: str) -> str:
	"""Resolve project type interactively from a marker or detected default.

	Args:
		repo_root: Repository directory containing an optional REPO_TYPE marker.

	Returns:
		A comma-separated canonical project-type marker.

	Raises:
		SystemExit: The entered project type is not valid.
	"""
	marker_path = os.path.join(repo_root, "REPO_TYPE")
	existing_marker = None
	if os.path.isfile(marker_path):
		with open(marker_path, "r") as marker_file:
			marker_text = marker_file.read().strip()
		marker_types = [piece.strip() for piece in marker_text.split(",") if piece.strip()]
		existing_marker = ",".join(marker_types)

	if existing_marker:
		default_type = existing_marker
	else:
		detected_type, confidence, _ = detect_repo_type.detect_repo_type(repo_root)
		if confidence in ('high', 'medium') and detected_type != 'ambiguous':
			default_type = detected_type
		else:
			default_type = "python"

	user_input = input(
		"Project type? [p]ython / pypi / [t]ypescript / [r]ust / [s]wift / [o]ther / "
		"[a]ll / scripted / website / compiled "
		f"(list allowed, e.g. python,rust or pr) [{default_type}]: "
	).strip()
	return normalize_project_type(user_input, default_type)


#============================================
def resolve_pypi(project_type: str) -> bool:
	"""Ask whether a Python-capable project publishes to PyPI.

	Args:
		project_type: Canonical project-type marker selected for the repository.

	Returns:
		True when the selected project publishes to PyPI.
	"""
	declared_types = repolib.model.expand_marker_types(project_type)
	if "pypi" in declared_types:
		return True
	python_capable = "python" in repolib.model.effective_type_chain(project_type)
	if not python_capable:
		return False
	user_input = input("Will this Python project be published as a pypi package? [y/N]: ").strip()
	return user_input.lower() == "y"


#============================================
def promote_pypi_type(project_type: str) -> str:
	"""Replace a declared Python type with its PyPI child type.

	Args:
		project_type: Comma-separated canonical project-type marker.

	Returns:
		Project-type marker with Python declarations promoted to PyPI.
	"""
	promoted_types = []
	for declared_type in project_type.split(","):
		promoted_type = "pypi" if declared_type == "python" else declared_type
		if promoted_type not in promoted_types:
			promoted_types.append(promoted_type)
	return ",".join(promoted_types)


#============================================
def resolve_licenses() -> tuple[str, str]:
	"""Prompt for code and documentation licenses.

	Returns:
		A pair containing the selected code and documentation licenses.

	Raises:
		SystemExit: The documentation license does not identify one choice.
	"""
	while True:
		user_input = input(
			"Code license?\n  [m] MIT\n  [a] Apache-2.0\n  [l] LGPL-3.0\n"
			"  [g] GPL-3.0\n  [ag] AGPL-3.0\n  [mp] MPL-2.0\nChoice: "
		).strip()
		try:
			code_license = resolve_code_license(user_input)
			break
		except ValueError as exc:
			print(f"Error: {exc}. Please try again.")

	user_input = input(
		"Docs license?\n  [cb] CC-BY-4.0\n  [cs] CC-BY-SA-4.0\n"
		"  [n] none\nChoice [n]: "
	).strip()
	try:
		docs_license = resolve_docs_license(user_input)
	except ValueError as exc:
		sys.exit(f"Invalid docs license: {exc}")
	return code_license, docs_license


#============================================
def resolve_stage() -> bool:
	"""Prompt whether to stage changes.

	Returns:
		True unless the answer is ``n``.
	"""
	return input("Stage changes? [Y/n]: ").strip().lower() != "n"


#============================================
def resolve_commit() -> bool:
	"""Prompt whether to create a commit.

	Returns:
		True only when the answer is ``y``.
	"""
	return input("Create a commit? [y/N]: ").strip().lower() == "y"


#============================================
@dataclasses.dataclass
class ResetAnswers:
	"""Resolved bootstrap answers from an interview or configuration file."""

	project_type: str
	code_license: str
	docs_license: str
	pypi: bool
	stage: bool
	commit: bool


#============================================
def answers_from_interview(repo_root: str) -> ResetAnswers:
	"""Collect and normalize answers from interactive prompts.

	Args:
		repo_root: Repository directory used to offer a project-type default.

	Returns:
		Normalized answers for the reset workflow.

	Raises:
		SystemExit: An entered project type or documentation license is invalid.
	"""
	project_type = resolve_project_type(repo_root)
	code_license, docs_license = resolve_licenses()
	pypi = resolve_pypi(project_type)
	if pypi:
		project_type = promote_pypi_type(project_type)
	return ResetAnswers(
		project_type=project_type,
		code_license=code_license,
		docs_license=docs_license,
		pypi=pypi,
		stage=resolve_stage(),
		commit=resolve_commit(),
	)


#============================================
def parse_config_json(raw_text: str, path: str) -> dict:
	"""Parse a JSON configuration object.

	Args:
		raw_text: JSON text read from the configuration file.
		path: Configuration-file path used in error messages.

	Returns:
		The parsed JSON object.

	Raises:
		SystemExit: The JSON text is invalid or does not contain an object.
	"""
	try:
		data = json.loads(raw_text)
	except json.JSONDecodeError as exc:
		sys.exit(f"Error: config file is not valid json: {path} ({exc})")
	if not isinstance(data, dict):
		sys.exit(f"Error: config file must be a json object at the top level: {path}")
	return data


#============================================
def load_config(path: str) -> dict:
	"""Load a JSON answers file and require an object at its top level.

	Args:
		path: JSON configuration-file path.

	Returns:
		The parsed configuration object.

	Raises:
		SystemExit: The file is missing, invalid JSON, or has a non-object top level.
	"""
	if not os.path.isfile(path):
		sys.exit(f"Error: config file not found: {path}")
	with open(path, "r") as config_file:
		raw_text = config_file.read()
	config = parse_config_json(raw_text, path)
	return config


#============================================
def answers_from_config(path: str) -> ResetAnswers:
	"""Build normalized reset answers from a JSON configuration file.

	Args:
		path: JSON configuration-file path.

	Returns:
		Normalized answers for the reset workflow.

	Raises:
		SystemExit: The configuration lacks required keys or contains invalid choices.
	"""
	config = load_config(path)
	if "project_type" not in config:
		sys.exit(f"Error: config missing required key 'project_type': {path}")
	if "code_license" not in config:
		sys.exit(f"Error: config missing required key 'code_license': {path}")

	project_type = normalize_project_type(str(config["project_type"]), "python")
	try:
		code_license = resolve_code_license(str(config["code_license"]))
	except ValueError as exc:
		sys.exit(f"Error: invalid code_license in config: {exc}")
	try:
		docs_license = resolve_docs_license(str(config.get("docs_license", "none")))
	except ValueError as exc:
		sys.exit(f"Error: invalid docs_license in config: {exc}")

	declared_types = repolib.model.expand_marker_types(project_type)
	pypi = "pypi" in declared_types or config.get("pypi", False)
	python_capable = "python" in repolib.model.effective_type_chain(project_type)
	if not python_capable:
		pypi = False
	if pypi:
		project_type = promote_pypi_type(project_type)
	return ResetAnswers(
		project_type=project_type,
		code_license=code_license,
		docs_license=docs_license,
		pypi=bool(pypi),
		stage=bool(config.get("stage", True)),
		commit=bool(config.get("commit", False)),
	)
