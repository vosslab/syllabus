"""Focused unit tests for syllabus composition and publication safety."""

# Standard Library
import pathlib

# PIP3 modules
import pytest

# local repo modules
import build_lib.syllabus_model
import build_lib.syllabus_content
import build_lib.syllabus_rendering


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
	prepared = build_lib.syllabus_content.prepare_section(markdown, True, "course-overview")
	expected = (
		"## Course title {#course-overview}\n\n"
		'!!! warning "Review required"\n\n'
		"    Confirm the grading plan.\n\n"
		"### Course at a glance\n\n"
		"| Course | Term |\n| --- | --- |\n| Test | Fall |\n"
	)
	assert prepared == expected


#============================================
def test_download_links_cover_course_and_term_pages(tmp_path: pathlib.Path) -> None:
	"""Each manifest output is linked from both student landing pages."""
	docs_root = tmp_path / "site_docs"
	term_path = docs_root / "fall_20xx"
	course_path = term_path / "course"
	downloads_dir = docs_root / "downloads"
	course_path.mkdir(parents=True)
	overview_path = course_path / "index.md"
	term_overview_path = term_path / "index.md"
	overview_path.write_text(
		"../../downloads/BIOL_000_SYLLABUS.pdf\n"
		"../../downloads/BIOL_000_SYLLABUS.docx\n",
		encoding="utf-8",
	)
	term_overview_path.write_text(
		"../downloads/BIOL_000_SYLLABUS.pdf\n"
		"../downloads/BIOL_000_SYLLABUS.docx\n",
		encoding="utf-8",
	)
	manifest = build_lib.syllabus_model.SyllabusManifest(
		path=course_path / "syllabus.yml",
		docs_root=docs_root,
		title="Course title",
		course_code="BIOL 000",
		term="Fall 20XX",
		author="Instructor",
		language="en-US",
		download_basename="BIOL_000_SYLLABUS",
		sections=(overview_path,),
		shared_sections=(),
	)
	build_lib.syllabus_content.verify_download_links(manifest, downloads_dir)
	term_overview_path.write_text(
		"../downloads/BIOL_000_SYLLABUS.pdf\n",
		encoding="utf-8",
	)
	with pytest.raises(RuntimeError, match=r"fall_20xx/index\.md: missing complete-download link"):
		build_lib.syllabus_content.verify_download_links(manifest, downloads_dir)


#============================================
def test_normalize_admonitions_for_docx() -> None:
	"""Pandoc receives a portable equivalent of Material admonitions."""
	markdown = '!!! warning "Review required"\n\n    Confirm the grading plan.\n'
	portable = build_lib.syllabus_content.normalize_admonitions(markdown)
	assert portable == "**Review required**\n\nConfirm the grading plan."


#============================================
def test_remove_heading_sections_omits_web_only_policy_routes() -> None:
	"""Complete documents keep the policy branch heading without its route lists."""
	markdown = (
		"# Dr. Voss course policies\n\nShared policy introduction.\n\n"
		"## Policy topics\n\n- [Assessment](ASSESSMENT.md)\n\n"
		"## Student support\n\n- [Resources](../STUDENT_RESOURCES.md)\n"
	)
	prepared = build_lib.syllabus_content.remove_heading_sections(
		markdown,
		("Policy topics", "Student support"),
	)
	assert prepared == "# Dr. Voss course policies\n\nShared policy introduction.\n\n"


#============================================
def test_rewrite_document_links_targets_included_section(tmp_path: pathlib.Path) -> None:
	"""Source-page links become internal links when their target is included."""
	source_path = tmp_path / "course" / "ASSIGNMENTS_AND_GRADING.md"
	target_path = tmp_path / "shared" / "policies" / "ASSESSMENT.md"
	markdown = (
		"See [grade thresholds](../shared/policies/ASSESSMENT.md#grades), "
		"[grading policies](../shared/policies/ASSESSMENT.md), and "
		"[other policies](../shared/policies/OTHER.md)."
	)
	rewritten = build_lib.syllabus_content.rewrite_document_links(
		markdown,
		source_path,
		{target_path.resolve(): "assessment"},
	)
	assert rewritten == (
		"See [grade thresholds](#grades), [grading policies](#assessment), and "
		"[other policies](../shared/policies/OTHER.md)."
	)


#============================================
def test_compose_markdown_links_to_embedded_instructor_section(tmp_path: pathlib.Path) -> None:
	"""Policy routes target instructor information already embedded in course details."""
	term_path = tmp_path / "fall_20xx"
	course_path = term_path / "course"
	shared_path = term_path / "shared"
	policy_path = shared_path / "policies"
	course_path.mkdir(parents=True)
	policy_path.mkdir(parents=True)
	index_path = course_path / "index.md"
	details_path = course_path / "COURSE_DETAILS.md"
	policies_path = policy_path / "index.md"
	instructor_route_path = shared_path / "INSTRUCTOR_INFORMATION.md"
	write_section(index_path, "Course title")
	details_path.write_text(
		"# Meetings and instructor\n\n## Instructor information\n\nContact details.\n",
		encoding="utf-8",
	)
	policies_path.write_text(
		"# Policies\n\nSee [Instructor information](../INSTRUCTOR_INFORMATION.md).\n",
		encoding="utf-8",
	)
	write_section(instructor_route_path, "Instructor information")
	manifest = build_lib.syllabus_model.SyllabusManifest(
		path=course_path / "syllabus.yml",
		docs_root=tmp_path,
		title="Course title",
		course_code="BIOL 000",
		term="Fall 20XX",
		author="Instructor",
		language="en-US",
		download_basename="BIOL_000_SYLLABUS",
		sections=(index_path, details_path),
		shared_sections=(policies_path,),
	)
	combined = build_lib.syllabus_content.compose_markdown(manifest)
	assert "[Instructor information](#instructor-information)" in combined
	assert "(../INSTRUCTOR_INFORMATION.md)" not in combined


#============================================
def test_markdown_html_uses_site_extension_stack(tmp_path: pathlib.Path) -> None:
	"""PDF HTML preserves native admonitions and explicit heading anchors."""
	manifest = build_lib.syllabus_model.SyllabusManifest(
		path=tmp_path / "syllabus.yml",
		docs_root=tmp_path,
		title="Course title",
		course_code="BIOL 000",
		term="Fall 20XX",
		author="Instructor",
		language="en-US",
		download_basename="BIOL_000_SYLLABUS",
		sections=(),
		shared_sections=(),
	)
	stylesheet_path = tmp_path / "print.css"
	stylesheet_path.write_text("body { color: black; }\n", encoding="utf-8")
	html_path = tmp_path / "syllabus.html"
	build_lib.syllabus_rendering.run_markdown_html(
		'## Course overview {#course-overview}\n\n!!! warning "Review"\n\n    Check this.\n\n'
		"| Field | Value |\n| --- | ---: |\n| Points | 10 |\n",
		html_path,
		stylesheet_path,
		manifest,
		("admonition", "attr_list", "tables"),
		{},
	)
	html_text = html_path.read_text(encoding="utf-8")
	assert '<html lang="en-US">' in html_text
	assert (
		'<h2 id="course-overview">Course overview</h2>\n'
		'<div class="admonition warning">\n<p class="admonition-title">Review</p>'
	) in html_text
	assert html_text.count("<table>") == 1


#============================================
def test_secret_scan_rejects_meeting_credentials() -> None:
	"""Credential-shaped public text fails closed."""
	credential_fixture = "".join(
		(
			"Join at https://example.",
			"zoom.",
			"us/j/123456789?",
			"pwd",
			"=synthetic-value",
		)
	)
	with pytest.raises(ValueError, match="prohibited public credential pattern"):
		build_lib.syllabus_content.scan_text_for_secrets(
			credential_fixture,
			"inline test",
		)


#============================================
def test_source_scan_rejects_line_breaking_control_characters() -> None:
	"""Invisible controls cannot silently turn a Markdown table into prose."""
	with pytest.raises(ValueError, match="prohibited control character: U\\+000B"):
		build_lib.syllabus_content.scan_text_for_prohibited_controls(
			"| Included in\vtotal points |",
			"inline test",
		)


#============================================
def test_markdown_table_validation_requires_consistent_columns() -> None:
	"""Every Markdown table has named headers and a rectangular row structure."""
	valid_markdown = "| Absence type | Score |\n| --- | ---: |\n| First communicated | N/A |\n"
	build_lib.syllabus_content.validate_markdown_tables(valid_markdown, "inline test")
	assert build_lib.syllabus_content.count_markdown_tables(valid_markdown) == 1
	markdown = "| Absence type | Score |\n| --- | ---: |\n| First communicated |\n"
	with pytest.raises(ValueError, match="inconsistent table columns"):
		build_lib.syllabus_content.validate_markdown_tables(markdown, "inline test")


#============================================
def write_section(path: pathlib.Path, heading: str) -> None:
	"""Write one minimal inline section for composition testing."""
	path.write_text(f"# {heading}\n\n{heading} body.\n", encoding="utf-8")
	return None


#============================================
def test_learning_framework_requires_all_four_ordered_sections(tmp_path: pathlib.Path) -> None:
	"""Every course preserves the distinct syllabus learning statements in order."""
	framework_path = tmp_path / "COURSE_LEARNING_FRAMEWORK.md"
	framework_path.write_text(
		"# Learning Objectives, Outcomes, and Goals\n\n"
		"## Roosevelt learning goals\n\n- Communication.\n\n"
		"## Learning Objectives\n\n"
		"Students completing this course will have achieved:\n\n- Experience.\n\n"
		"## Course Learning Outcomes\n\n"
		"Students completing this course will be able to:\n\n- Apply knowledge.\n\n"
		"## Learning Goals\n\n"
		"Overall, this course aims to accomplish:\n\n- Growth.\n",
		encoding="utf-8",
	)
	build_lib.syllabus_content.validate_course_learning_framework((framework_path,), tmp_path)


#============================================
def test_compose_markdown_appends_policy_and_resources_once(tmp_path: pathlib.Path) -> None:
	"""The manifest order keeps policies and resources separate and non-duplicated."""
	index_path = tmp_path / "index.md"
	policy_path = tmp_path / "shared" / "policies" / "index.md"
	resource_path = tmp_path / "shared" / "STUDENT_RESOURCES.md"
	policy_path.parent.mkdir(parents=True)
	write_section(index_path, "Course title")
	write_section(policy_path, "Policies")
	write_section(resource_path, "Student resources")
	manifest = build_lib.syllabus_model.SyllabusManifest(
		path=tmp_path / "syllabus.yml",
		docs_root=tmp_path,
		title="Course title",
		course_code="BIOL 000",
		term="Fall 20XX",
		author="Instructor",
		language="en-US",
		download_basename="BIOL_000_SYLLABUS",
		sections=(index_path,),
		shared_sections=(policy_path, resource_path),
	)
	combined = build_lib.syllabus_content.compose_markdown(manifest)
	assert combined.count("## Policies {#policies}") == 1
	assert combined.index("## Policies") < combined.index("## Student resources")


#============================================
def test_publish_downloads_replaces_the_managed_set(tmp_path: pathlib.Path) -> None:
	"""Validated staged downloads replace current files and remove obsolete siblings."""
	staged_dir = tmp_path / "staged"
	downloads_dir = tmp_path / "downloads"
	staged_dir.mkdir()
	downloads_dir.mkdir()
	(staged_dir / "COURSE.pdf").write_text("new PDF", encoding="utf-8")
	(staged_dir / "COURSE.docx").write_text("new DOCX", encoding="utf-8")
	(downloads_dir / "COURSE.pdf").write_text("old PDF", encoding="utf-8")
	(downloads_dir / "STALE.docx").write_text("obsolete", encoding="utf-8")
	(downloads_dir / "README.txt").write_text("preserve", encoding="utf-8")
	build_lib.syllabus_rendering.publish_downloads(
		staged_dir,
		downloads_dir,
		{"COURSE.docx", "COURSE.pdf"},
	)
	managed_state = (
		(downloads_dir / "COURSE.pdf").read_text(encoding="utf-8"),
		(downloads_dir / "COURSE.docx").read_text(encoding="utf-8"),
		(downloads_dir / "STALE.docx").exists(),
	)
	assert managed_state == ("new PDF", "new DOCX", False)
	assert (downloads_dir / "README.txt").read_text(encoding="utf-8") == "preserve"


#============================================
def test_publish_downloads_rejects_an_incomplete_stage(tmp_path: pathlib.Path) -> None:
	"""A partial staged build cannot replace an existing published download."""
	staged_dir = tmp_path / "staged"
	downloads_dir = tmp_path / "downloads"
	staged_dir.mkdir()
	downloads_dir.mkdir()
	(staged_dir / "COURSE.pdf").write_text("new PDF", encoding="utf-8")
	current_path = downloads_dir / "COURSE.pdf"
	current_path.write_text("current PDF", encoding="utf-8")
	with pytest.raises(RuntimeError, match="Staged downloads do not match"):
		build_lib.syllabus_rendering.publish_downloads(
			staged_dir,
			downloads_dir,
			{"COURSE.docx", "COURSE.pdf"},
		)
	assert current_path.read_text(encoding="utf-8") == "current PDF"


#============================================
def test_public_only_repository_rejects_a_raw_tree(tmp_path: pathlib.Path) -> None:
	"""Private or ambiguous raw content cannot live inside the repository."""
	(tmp_path / "raw").mkdir()
	with pytest.raises(RuntimeError, match="only public-safe canonical content"):
		build_lib.syllabus_content.require_public_only_repository(tmp_path)


#============================================
def test_single_content_authority_rejects_markdown_templates(tmp_path: pathlib.Path) -> None:
	"""Live syllabus content cannot compete with a parallel template tree."""
	templates_path = tmp_path / "templates"
	templates_path.mkdir()
	(templates_path / "POLICIES.md").write_text("# Competing policies\n", encoding="utf-8")
	with pytest.raises(RuntimeError, match="content belongs only under site_docs"):
		build_lib.syllabus_content.require_single_content_authority(tmp_path)
