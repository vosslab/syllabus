"""Focused tests for department-checklist validation and evidence rendering."""

# Standard Library
import pathlib

# PIP3 modules
import pytest

# local repo modules
import build_department_checklists
import build_lib.syllabus_model


#============================================
def test_evidence_source_stays_in_active_term(tmp_path: pathlib.Path) -> None:
	"""Course-relative evidence resolves while a traversal escape is rejected."""
	docs_root = tmp_path / "site_docs"
	course_root = docs_root / "fall_2026" / "course"
	course_root.mkdir(parents=True)
	course_index = course_root / "index.md"
	course_index.write_text("# Course title\n", encoding="utf-8")
	outside_source = docs_root / "outside.md"
	outside_source.write_text("# Outside\n", encoding="utf-8")
	manifest = build_lib.syllabus_model.SyllabusManifest(
		path=course_root / "syllabus.yml",
		docs_root=docs_root,
		title="Course title",
		short_name="Course",
		course_code="BIOL 000",
		term="Fall 2026",
		author="Instructor",
		language="en-US",
		course_color="#007849",
		sections=(course_index,),
		shared_sections=(),
		lab_status="no_lab",
	)
	resolved = build_department_checklists.resolve_evidence_source_path(
		manifest,
		"course",
		"./",
	)
	assert resolved == course_index
	with pytest.raises(ValueError, match="no Fall 2026 source page"):
		build_department_checklists.resolve_evidence_source_path(
			manifest,
			"course",
			"../../outside/",
		)


#============================================
def test_covered_item_requires_evidence() -> None:
	"""A completed rubric claim cannot be stored without an evidence link."""
	raw_item = {
		"id": "course_dates",
		"group": "Course information",
		"label": "Course dates",
		"status": "covered",
		"evidence": [],
		"note": "Dates are present.",
	}
	with pytest.raises(ValueError, match="covered items require evidence"):
		build_department_checklists.validate_item(raw_item, "item")


#============================================
def test_render_checklist_keeps_doubt_unchecked(tmp_path: pathlib.Path) -> None:
	"""Unresolved applicability remains visibly unchecked in the submission artifact."""
	course_index = tmp_path / "fall_2026" / "course" / "index.md"
	course_index.parent.mkdir(parents=True)
	course_index.write_text("# Course title\n", encoding="utf-8")
	manifest = build_lib.syllabus_model.SyllabusManifest(
		path=course_index.parent / "syllabus.yml",
		docs_root=tmp_path,
		title="Course title",
		short_name="Course",
		course_code="BIOL 000",
		term="Fall 2026",
		author="Instructor",
		language="en-US",
		course_color="#007849",
		sections=(course_index,),
		shared_sections=(),
		lab_status="no_lab",
	)
	items = [
		{
			"id": "director",
			"group": "Program information",
			"label": "Program director",
			"status": "needs_review",
			"evidence": ({"label": "Leadership", "path": "./"},),
			"note": "Applicability is not established.",
		}
	]
	markdown = build_department_checklists.render_checklist(
		manifest,
		"course",
		items,
		{"course-overview": 2},
	)
	assert "- [ ] **Program director**" in markdown
	assert "Syllabus p. 2 - Course title - Leadership" in markdown
	assert "**Doubt:** Applicability is not established." in markdown


#============================================
def test_evidence_location_uses_authoritative_page_title(tmp_path: pathlib.Path) -> None:
	"""Visible PDF locations combine the source H1 with the evidence topic."""
	docs_root = tmp_path / "site_docs"
	shared_policies = docs_root / "fall_2026" / "shared" / "policies"
	shared_policies.mkdir(parents=True)
	(shared_policies / "index.md").write_text("# Dr. Voss course policies\n", encoding="utf-8")
	manifest = build_lib.syllabus_model.SyllabusManifest(
		path=docs_root / "fall_2026" / "course" / "syllabus.yml",
		docs_root=docs_root,
		title="Course title",
		short_name="Course",
		course_code="BIOL 000",
		term="Fall 2026",
		author="Instructor",
		language="en-US",
		course_color="#007849",
		sections=(),
		shared_sections=(),
		lab_status="no_lab",
	)
	page_title = build_department_checklists.get_source_page_title(
		manifest,
		"course",
		"../shared/policies/",
	)
	location = build_department_checklists.format_evidence_location(
		19,
		page_title,
		"Course policies",
	)
	assert location == "Syllabus p. 19 - Dr. Voss course policies - Course policies"


#============================================
def test_render_checklist_html_escapes_authored_text(tmp_path: pathlib.Path) -> None:
	"""Authored checklist text cannot change the generated HTML structure."""
	docs_root = tmp_path / "site_docs"
	course_root = docs_root / "fall_2026" / "course"
	course_root.mkdir(parents=True)
	(course_root / "index.md").write_text("# Course title\n", encoding="utf-8")
	manifest = build_lib.syllabus_model.SyllabusManifest(
		path=course_root / "syllabus.yml",
		docs_root=docs_root,
		title="Course title",
		short_name="Course",
		course_code="BIOL 000",
		term="Fall 2026",
		author="Instructor",
		language="en-US",
		course_color="#007849",
		sections=(course_root / "index.md",),
		shared_sections=(),
		lab_status="no_lab",
	)
	items = [
		{
			"id": "safe_html",
			"group": "Course information",
			"label": "Text <unsafe>",
			"status": "covered",
			"evidence": ({"label": "Course page", "path": "./"},),
			"note": "Visible <unsafe> note.",
		}
	]
	html_document = build_department_checklists.render_checklist_html(
		manifest,
		"course",
		items,
		{"course-overview": 2},
		tmp_path / "style.css",
	)
	assert "&lt;unsafe&gt;" in html_document
	assert "<unsafe>" not in html_document
	assert "Syllabus p. 2 - Course title - Course page" in html_document
	assert "<a href=" not in html_document
