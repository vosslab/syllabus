"""Behavior tests for the propagated Graphify repository mapping tool."""

# Standard Library
import json
import pathlib

# PIP3 modules
import pytest

# local repo modules
import tools.graphify_map_repo


#============================================


def sample_graph_data() -> dict:
	"""Return a small multi-community graph for orientation behavior tests."""
	graph_data = {
		"built_at_commit": "d7792629abcdef",
		"nodes": [
			{
				"id": "app",
				"label": "App()",
				"_callable": True,
				"community_name": "Game Logic",
				"source_file": "src/app.tsx",
				"source_location": "L10",
			},
			{
				"id": "helper",
				"label": "beginWave()",
				"_callable": True,
				"community_name": "Game Logic",
				"source_file": "src/game.ts",
				"source_location": "L40",
			},
			{
				"id": "tick",
				"label": "tickGame()",
				"_callable": True,
				"community_name": "Game Simulation",
				"source_file": "src/simulation.ts",
				"source_location": "L20",
			},
			{
				"id": "settings",
				"label": "SettingsState",
				"_callable": True,
				"community_name": "Game Settings",
				"source_file": "src/settings.ts",
				"source_location": "L30",
			},
			{
				"id": "compiler",
				"label": "compilerOptions",
				"community_name": "TypeScript Configuration",
				"source_file": "tsconfig.json",
			},
		],
		"links": [
			{"source": "app", "target": "tick"},
			{"source": "app", "target": "settings"},
			{"source": "app", "target": "helper"},
			{"source": "tick", "target": "helper"},
		],
	}
	return graph_data


#============================================


def sample_analysis_data() -> dict:
	"""Return structured Graphify analysis matching the sample graph."""
	return {
		"communities": {
			"0": ["app", "helper"],
			"1": ["tick"],
			"2": ["settings"],
			"3": ["compiler"],
		},
		"cohesion": {},
		"gods": [{"id": "app", "label": "App()", "degree": 3}],
		"questions": [
			{
				"type": "bridge_node",
				"question": (
					"Why does `App()` connect `Game Logic` to `Game Settings`, "
					"`Game Simulation`?"
				),
				"why": "cross-community bridge",
			},
		],
		"surprises": [
			{
				"source": "App()",
				"target": "tickGame()",
				"relation": "calls",
			},
		],
	}


#============================================


def sample_labels_data() -> dict:
	"""Return stable community labels matching the sample analysis."""
	return {
		"0": "Game Logic",
		"1": "Game Simulation",
		"2": "Game Settings",
		"3": "TypeScript Configuration",
	}


#============================================


def test_existing_graph_selects_real_update(tmp_path: pathlib.Path) -> None:
	"""An existing graph uses Graphify's incremental code-map update."""
	output_dir = tmp_path / "graphify-out"
	output_dir.mkdir()
	(output_dir / "graph.json").write_text("{}", encoding="utf-8")
	operation, command, is_fresh = tools.graphify_map_repo.graph_build_command(
		"graphify", tmp_path, tools.graphify_map_repo.MODE_AUTO
	)
	assert (operation, command) == ("UPDATING GRAPHIFY CODE MAP", ["graphify", "update", "."])
	assert is_fresh is False


#============================================


def test_missing_graph_selects_code_extraction(tmp_path: pathlib.Path) -> None:
	"""A missing graph performs a fresh code-only extraction."""
	operation, command, is_fresh = tools.graphify_map_repo.graph_build_command(
		"graphify", tmp_path, tools.graphify_map_repo.MODE_AUTO
	)
	expected = ("EXTRACTING GRAPHIFY CODE MAP", ["graphify", "extract", ".", "--code-only"])
	assert (operation, command) == expected
	assert is_fresh is True


#============================================


def test_fresh_mode_forces_code_extraction(tmp_path: pathlib.Path) -> None:
	"""Fresh mode extracts even when an existing graph could be updated."""
	output_dir = tmp_path / "graphify-out"
	output_dir.mkdir()
	(output_dir / "graph.json").write_text("{}", encoding="utf-8")
	operation, command, is_fresh = tools.graphify_map_repo.graph_build_command(
		"graphify", tmp_path, tools.graphify_map_repo.MODE_FRESH
	)
	expected = ("EXTRACTING GRAPHIFY CODE MAP", ["graphify", "extract", ".", "--code-only"])
	assert (operation, command) == expected
	assert is_fresh is True


#============================================


def test_update_mode_extracts_when_graph_is_missing(tmp_path: pathlib.Path) -> None:
	"""Update mode announces the fresh-extraction fallback from the retired tool."""
	operation, command, is_fresh = tools.graphify_map_repo.graph_build_command(
		"graphify", tmp_path, tools.graphify_map_repo.MODE_UPDATE
	)
	expected = (
		"NO EXISTING GRAPH; EXTRACTING FRESH GRAPHIFY CODE MAP",
		["graphify", "extract", ".", "--code-only"],
	)
	assert (operation, command) == expected
	assert is_fresh is True


#============================================


@pytest.mark.parametrize(
	("flag", "mode"),
	[
		("-F", tools.graphify_map_repo.MODE_FRESH),
		("--fresh", tools.graphify_map_repo.MODE_FRESH),
		("-U", tools.graphify_map_repo.MODE_UPDATE),
		("--update", tools.graphify_map_repo.MODE_UPDATE),
		("-C", tools.graphify_map_repo.MODE_CONTEXT),
		("--context", tools.graphify_map_repo.MODE_CONTEXT),
	],
)
def test_explicit_mode_flags(flag: str, mode: str) -> None:
	"""Each documented flag selects its matching lifecycle mode."""
	args = tools.graphify_map_repo.parse_args([flag])
	assert args.mode == mode


#============================================


@pytest.mark.parametrize("flag", ["-O", "--ollama"])
def test_ollama_flag_selects_local_backend(flag: str) -> None:
	"""The explicit Ollama override selects local community labeling."""
	args = tools.graphify_map_repo.parse_args([flag])
	assert args.label_backend == tools.graphify_map_repo.OLLAMA_BACKEND


#============================================


def test_fresh_claude_labeling_uses_configured_model(
	tmp_path: pathlib.Path,
	monkeypatch: pytest.MonkeyPatch,
) -> None:
	"""Fresh Claude labeling selects its model independently of the interactive default."""
	commands = []

	def record_command(command: list[str], repo_root: pathlib.Path) -> None:
		commands.append((command, repo_root))

	monkeypatch.setattr(tools.graphify_map_repo, "run_command", record_command)
	tools.graphify_map_repo.label_graph(
		"graphify",
		tmp_path,
		tools.graphify_map_repo.LABEL_BACKEND,
	)
	expected = [
		"graphify",
		"label",
		".",
		"--backend=claude-cli",
		f"--model={tools.graphify_map_repo.CLAUDE_LABEL_MODEL}",
	]
	assert commands == [(expected, tmp_path)]


#============================================


def test_fresh_ollama_labeling_uses_configured_model(
	tmp_path: pathlib.Path,
	monkeypatch: pytest.MonkeyPatch,
) -> None:
	"""Fresh Ollama labeling names every community with the configured model."""
	commands = []

	def record_command(command: list[str], repo_root: pathlib.Path) -> None:
		commands.append((command, repo_root))

	monkeypatch.setattr(tools.graphify_map_repo, "run_command", record_command)
	tools.graphify_map_repo.label_graph(
		"graphify",
		tmp_path,
		tools.graphify_map_repo.OLLAMA_BACKEND,
	)
	expected = [
		"graphify",
		"label",
		".",
		"--backend=ollama",
		f"--model={tools.graphify_map_repo.OLLAMA_MODEL}",
	]
	assert commands == [(expected, tmp_path)]


#============================================


def test_context_prints_help_before_first_map(
	tmp_path: pathlib.Path,
	capsys: pytest.CaptureFixture,
) -> None:
	"""Context explains the missing map and prints normal help before first build."""
	tools.graphify_map_repo.print_context(tmp_path)
	output = capsys.readouterr().out
	assert "No Graphify map exists" in output
	assert "usage:" in output and "--fresh" in output


#============================================


@pytest.mark.parametrize("artifact_name", ["manifest.json", "GRAPH_REPORT.md"])
def test_context_prints_help_for_incomplete_map(
	tmp_path: pathlib.Path,
	capsys: pytest.CaptureFixture,
	artifact_name: str,
) -> None:
	"""Internal or visible partial output is not presented as a usable graph."""
	output_dir = tmp_path / "graphify-out"
	output_dir.mkdir()
	(output_dir / artifact_name).write_text("partial", encoding="utf-8")
	tools.graphify_map_repo.print_context(tmp_path)
	output = capsys.readouterr().out
	assert "No Graphify map exists" in output
	assert "usage:" in output


#============================================


def test_structured_orientation_names_major_areas_and_commit(tmp_path: pathlib.Path) -> None:
	"""Manager context leads with bounded repository facts from structured data."""
	orientation = tools.graphify_map_repo.format_orientation(
		tmp_path,
		sample_graph_data(),
		analysis_data=sample_analysis_data(),
		labels_data=sample_labels_data(),
	)
	assert orientation.startswith("GRAPHIFY CONTEXT\nGraph mapped at commit d7792629abcd.")
	assert "Major repository areas:\n- Game Logic" in orientation


#============================================


def test_bridge_is_cross_community_instead_of_high_degree(tmp_path: pathlib.Path) -> None:
	"""Graphify's bridge result is used instead of its within-area god node."""
	graph_data = {
		"nodes": [
			{"id": "hub", "label": "Hub()", "_callable": True,
				"community_name": "Area A"},
			{"id": "a1", "label": "a1()", "_callable": True,
				"community_name": "Area A"},
			{"id": "a2", "label": "a2()", "_callable": True,
				"community_name": "Area A"},
			{"id": "a3", "label": "a3()", "_callable": True,
				"community_name": "Area A"},
			{"id": "bridge", "label": "Bridge()", "_callable": True,
				"community_name": "Area A"},
			{"id": "b", "label": "b()", "_callable": True,
				"community_name": "Area B"},
			{"id": "c", "label": "c()", "_callable": True,
				"community_name": "Area C"},
		],
		"links": [
			{"source": "hub", "target": "a1"},
			{"source": "hub", "target": "a2"},
			{"source": "hub", "target": "a3"},
			{"source": "bridge", "target": "b"},
			{"source": "bridge", "target": "c"},
		],
	}
	analysis_data = {
		"communities": {
			"0": ["hub", "a1", "a2", "a3", "bridge"],
			"1": ["b"],
			"2": ["c"],
		},
		"gods": [{"id": "hub", "label": "Hub()", "degree": 3}],
		"questions": [
			{
				"type": "bridge_node",
				"question": "Why does `Bridge()` connect `Area A` to `Area B`, `Area C`?",
			},
		],
		"surprises": [],
	}
	labels_data = {"0": "Area A", "1": "Area B", "2": "Area C"}
	orientation = tools.graphify_map_repo.format_orientation(
		tmp_path,
		graph_data,
		analysis_data=analysis_data,
		labels_data=labels_data,
	)
	assert "Bridge() - connects Area A, Area B, and Area C" in orientation
	assert "Hub()" not in orientation


#============================================


def test_cross_area_connector_output_is_bounded(tmp_path: pathlib.Path) -> None:
	"""One large connector summarizes communities beyond the display bound."""
	community_names = tuple(
		f"Area {index:02d}"
		for index in range(tools.graphify_map_repo.MAX_CONNECTOR_COMMUNITIES + 2)
	)
	quoted_names = ", ".join(f"`{name}`" for name in community_names)
	analysis_data = {
		"communities": {"0": ["bridge"]},
		"questions": [
			{
				"type": "bridge_node",
				"question": f"Why does `Bridge()` connect {quoted_names}?",
			},
		],
		"surprises": [],
		"gods": [],
	}
	orientation = tools.graphify_map_repo.format_orientation(
		tmp_path, None, analysis_data=analysis_data, labels_data={"0": "Bridge Area"}
	)
	visible_names = ", ".join(
		community_names[:tools.graphify_map_repo.MAX_CONNECTOR_COMMUNITIES]
	)
	assert f"- Bridge() - connects {visible_names}, and 2 more" in orientation


#============================================


def test_large_analysis_hard_caps_major_areas(tmp_path: pathlib.Path) -> None:
	"""A large graph cannot expand manager context past the configured area cap."""
	communities = {}
	labels = {}
	for index in range(tools.graphify_map_repo.MAX_COMMUNITIES + 2):
		community_id = str(index)
		communities[community_id] = [f"node-{index}-a", f"node-{index}-b"]
		labels[community_id] = f"Area {index:02d}"
	analysis_data = {
		"communities": communities,
		"questions": [],
		"surprises": [],
		"gods": [],
	}
	orientation = tools.graphify_map_repo.format_orientation(
		tmp_path, None, analysis_data=analysis_data, labels_data=labels
	)
	assert "- Area 07" in orientation
	assert "- Area 08" not in orientation


#============================================


def test_small_graph_without_sidecars_still_produces_context(tmp_path: pathlib.Path) -> None:
	"""Graph JSON alone is sufficient for useful deterministic context."""
	first_output = tools.graphify_map_repo.format_orientation(tmp_path, sample_graph_data())
	second_output = tools.graphify_map_repo.format_orientation(tmp_path, sample_graph_data())
	assert "Major repository areas:" in first_output
	assert "- Game Logic" in first_output
	assert "Cross-area connectors:" not in first_output
	assert first_output == second_output


#============================================


def test_report_is_last_resort_context_source(tmp_path: pathlib.Path) -> None:
	"""A report alone supplies minimal orientation when structured files are absent."""
	output_dir = tmp_path / "graphify-out"
	output_dir.mkdir()
	report_text = """# Graph Report

## Graph Freshness
- Built from commit: `abc12345`

## Communities

### Community 0 - "Scene Linting"
Cohesion: 0.20
Nodes (12): Finding

### Community 1 - "State Management"
Cohesion: 0.30
Nodes (8): StateMap

## Suggested Questions
- **Why does `Finding` connect `Scene Linting` to `State Management`?**
"""
	(output_dir / "GRAPH_REPORT.md").write_text(report_text, encoding="utf-8")
	orientation = tools.graphify_map_repo.manager_context(tmp_path)
	assert orientation is not None
	assert "Graph mapped at commit abc12345." in orientation
	assert "Finding - connects Scene Linting and State Management" in orientation


#============================================


def test_orientation_omits_graphify_diagnostics(tmp_path: pathlib.Path) -> None:
	"""Context contains repository structure, not artifact or maintenance diagnostics."""
	orientation = tools.graphify_map_repo.format_orientation(
		tmp_path,
		sample_graph_data(),
		analysis_data=sample_analysis_data(),
		labels_data=sample_labels_data(),
	)
	for unwanted_text in (
		"Corpus Check",
		"Graph scope excludes",
		"graph.html",
		"graph.json",
		"Token cost",
		"git ignored",
	):
		assert unwanted_text not in orientation


#============================================


def test_manager_context_file_matches_terminal_context(tmp_path: pathlib.Path) -> None:
	"""Build output saves the exact deterministic context shown to managers."""
	output_dir = tmp_path / "graphify-out"
	output_dir.mkdir()
	context = tools.graphify_map_repo.format_orientation(tmp_path, sample_graph_data())
	context_path = tools.graphify_map_repo.write_manager_context(tmp_path, context)
	assert context_path.name == "MANAGER_CONTEXT.md"
	assert context_path.read_text(encoding="utf-8") == f"{context}\n"


#============================================


def test_graph_data_loader_rejects_missing_links(tmp_path: pathlib.Path) -> None:
	"""A partial graph JSON fails before producing misleading orientation."""
	output_dir = tmp_path / "graphify-out"
	output_dir.mkdir()
	graph_text = json.dumps({"nodes": []})
	(output_dir / "graph.json").write_text(graph_text, encoding="utf-8")
	with pytest.raises(RuntimeError, match="no links list"):
		tools.graphify_map_repo.load_graph_data(tmp_path)


# Vendored pytest file. Local changes can and will be overwritten.
