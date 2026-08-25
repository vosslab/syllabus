"""Focused unit tests for syllabus composition and publication safety."""

# Standard Library
import pathlib

# PIP3 modules
import pytest

# local repo modules
import pipeline.build_syllabi


#============================================
def test_prepare_section_removes_web_only_content() -> None:
	"""The archival source excludes web controls while retaining extension syntax."""
	markdown = (
		"# Course title\n\n"
		'<div class="syllabus-downloads"><a href="file.pdf">Download PDF</a></div>\n\n'
		'!!! warning "Review required"\n\n    Confirm the grading plan.\n\n'
		"## Course pages\n\n- [Details](COURSE_DETAILS.md)\n\n"
		"## Course at a glance\n\n| Course | Term |\n| --- | --- |\n| Test | Fall |\n"
	)
	prepared = pipeline.build_syllabi.prepare_section(markdown, True, "course-overview")
	expected = (
		"## Course title {#course-overview}\n\n"
		'!!! warning "Review required"\n\n'
		"    Confirm the grading plan.\n\n"
		"### Course at a glance\n\n"
		"| Course | Term |\n| --- | --- |\n| Test | Fall |\n"
	)
	assert prepared == expected


#============================================
def test_normalize_admonitions_for_docx() -> None:
	"""Pandoc receives a portable equivalent of Material admonitions."""
	markdown = '!!! warning "Review required"\n\n    Confirm the grading plan.\n'
	portable = pipeline.build_syllabi.normalize_admonitions(markdown)
	assert portable == "**Review required**\n\nConfirm the grading plan."


#============================================
def test_markdown_html_uses_site_extension_stack(tmp_path: pathlib.Path) -> None:
	"""PDF HTML preserves native admonitions and explicit heading anchors."""
	manifest = pipeline.build_syllabi.SyllabusManifest(
		path=tmp_path / "syllabus.yml",
		title="Course title",
		course_code="BIOL 000",
		term="Fall 20XX",
		author="Instructor",
		language="en-US",
		status="current",
		publication_status="approved",
		download_basename="BIOL_000_SYLLABUS",
		sections=(),
		shared_sections=(),
	)
	stylesheet_path = tmp_path / "print.css"
	stylesheet_path.write_text("body { color: black; }\n", encoding="utf-8")
	html_path = tmp_path / "syllabus.html"
	pipeline.build_syllabi.run_markdown_html(
		'## Course overview {#course-overview}\n\n!!! warning "Review"\n\n    Check this.\n',
		html_path,
		stylesheet_path,
		manifest,
		("admonition", "attr_list"),
		{},
	)
	html_text = html_path.read_text(encoding="utf-8")
	assert '<html lang="en-US">' in html_text
	assert (
		'<h2 id="course-overview">Course overview</h2>\n'
		'<div class="admonition warning">\n<p class="admonition-title">Review</p>'
	) in html_text


#============================================
def test_secret_scan_rejects_meeting_credentials() -> None:
	"""Credential-shaped public text fails closed."""
	with pytest.raises(ValueError, match="prohibited public credential pattern"):
		pipeline.build_syllabi.scan_text_for_secrets(
			"Join at https://example.zoom.us/j/123456789?pwd=secret",
			"inline test",
		)


#============================================
def write_section(path: pathlib.Path, heading: str) -> None:
	"""Write one minimal inline section for composition testing."""
	path.write_text(f"# {heading}\n\n{heading} body.\n", encoding="utf-8")
	return None


#============================================
def test_compose_markdown_appends_policy_and_resources_once(tmp_path: pathlib.Path) -> None:
	"""The manifest order keeps policies and resources separate and non-duplicated."""
	index_path = tmp_path / "index.md"
	policy_path = tmp_path / "POLICIES.md"
	resource_path = tmp_path / "STUDENT_RESOURCES.md"
	write_section(index_path, "Course title")
	write_section(policy_path, "Policies")
	write_section(resource_path, "Student resources")
	manifest = pipeline.build_syllabi.SyllabusManifest(
		path=tmp_path / "syllabus.yml",
		title="Course title",
		course_code="BIOL 000",
		term="Fall 20XX",
		author="Instructor",
		language="en-US",
		status="current",
		publication_status="approved",
		download_basename="BIOL_000_SYLLABUS",
		sections=(index_path,),
		shared_sections=(policy_path, resource_path),
	)
	combined = pipeline.build_syllabi.compose_markdown(manifest)
	assert combined.count("## Policies {#policies}") == 1
	assert combined.index("## Policies") < combined.index("## Student resources")
