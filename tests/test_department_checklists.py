"""Focused tests for department-checklist validation and evidence rendering."""

# Standard Library
import pathlib

# PIP3 modules
import pytest

# local repo modules
import build_department_checklists
import build_lib.syllabus_model


#============================================
def test_evidence_url_stays_in_published_site() -> None:
	"""Course-relative evidence resolves while a traversal escape is rejected."""
	base = "https://example.edu/syllabus/"
	url = build_department_checklists.evidence_url(base, "course", "DETAILS/#meeting")
	assert url == "https://example.edu/syllabus/fall_2026/course/DETAILS/#meeting"
	with pytest.raises(ValueError, match="escapes the configured site"):
		build_department_checklists.evidence_url(base, "course", "../../../outside")


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
	manifest = build_lib.syllabus_model.SyllabusManifest(
		path=tmp_path / "syllabus.yml",
		docs_root=tmp_path,
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
	items = [
		{
			"id": "director",
			"group": "Program information",
			"label": "Program director",
			"status": "needs_review",
			"evidence": ({"label": "Leadership", "path": "DETAILS/#leadership"},),
			"note": "Applicability is not established.",
		}
	]
	markdown = build_department_checklists.render_checklist(
		manifest,
		"course",
		"https://example.edu/syllabus/",
		items,
	)
	assert "- [ ] **Program director**" in markdown
	assert "**Doubt:** Applicability is not established." in markdown
