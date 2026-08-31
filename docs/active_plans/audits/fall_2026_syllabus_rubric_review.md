# Fall 2026 checklist actions

Reviewed August 31, 2026. This report compares all three live Fall 2026 syllabi with the department
checklist and records only the work that remains.

## Checklist authority

Use `raw/Dept_University_Docs/Syllabus_Checklist_Fall_2026_updated.md` as the current Markdown
checklist. It has the later local modification time, its name matches the updated DOCX, and its 53
items exactly match `raw/Dept_University_Docs/Syllabus_Checklist_Fall_2026_updated.docx`.

`raw/Dept_University_Docs/syllabus_checklist.md` contains the same 53 items with checkbox
formatting. It is not substantively different and does not change the results below. These raw
files are ignored working material, so this report identifies them by path without linking to
targets that will not exist on GitHub.

Reviewed course authorities:

- BIOL 318/418: [site_docs/fall_2026/biostats/index.md](../../../site_docs/fall_2026/biostats/index.md)
- BIOL 351/451: [site_docs/fall_2026/genetics/index.md](../../../site_docs/fall_2026/genetics/index.md)
- BIOL 480: [site_docs/fall_2026/biotech/index.md](../../../site_docs/fall_2026/biotech/index.md)

## Current result

The checklist generator treats an item as resolved when the syllabus covers it or documents why it
does not apply. A resolved item is evidence for review, not department approval.

| Course | Resolved | Open required | Open suggested | Total open |
| --- | ---: | ---: | ---: | ---: |
| BIOL 318/418 | 47 of 53 | 4 | 2 | 6 |
| BIOL 351/451 | 48 of 53 | 2 | 3 | 5 |
| BIOL 480 | 50 of 53 | 2 | 1 | 3 |

The run created current Markdown and DOCX checklists under `output/department_checklists/`. Those
files are generated submission artifacts; edit
[pipeline/department_checklists.yml](../../../pipeline/department_checklists.yml), not the output.

## Leadership decision

The department chair remains covered. The instructor confirmed that no program director overlaps
these three Biology syllabi, so the conditional program-director item is not applicable. CSHP
deans, unrelated program directors, academic advisors, and the Health Professions Program
Coordinator are outside the checklist request and are not used as checklist evidence.
Department-specific advisor and laboratory contacts may still appear as optional student
resources.

The user-confirmed CSHP leadership and advising roster is preserved in the tracked
[CSHP leadership reference](../../CSHP_LEADERSHIP_REFERENCE.md). It is a public maintainer
reference, not a syllabus source.

## CORE Attribute decision

The instructor confirmed that CORE Attributes apply to general-education courses. BIOL 318/418,
BIOL 351/451, and BIOL 480 are upper-level major courses, so the conditional CORE Attribute item
is not applicable to all three syllabi. Catalog labels such as `Lab Course` and `Natural Science`
do not change that course-scope decision.

## Required actions

| Requirement | BIOL 318/418 | BIOL 351/451 | BIOL 480 |
| --- | --- | --- | --- |
| Assignment points or weights | Add point plan | Covered | Covered |
| Major due dates | Clarify major work | Covered | Covered |
| Assignment feedback dates | Add timing | Add timing | Add timing |
| Policy and resource acknowledgment | Add mechanism | Add mechanism | Add mechanism |

### Finalize Biostatistics points

Approve or revise the proposed
[Biostatistics point plan](../decisions/biostats_point_plan.md). The outstanding instructor choices
are the number of group quizzes, the regular assignment total, and the extra-credit cap. Then add
the confirmed `course_point_plan` to
[site_docs/fall_2026/biostats/syllabus.yml](../../../site_docs/fall_2026/biostats/syllabus.yml) and
the required point-plan marker to
[site_docs/fall_2026/biostats/ASSIGNMENTS_AND_GRADING.md](../../../site_docs/fall_2026/biostats/ASSIGNMENTS_AND_GRADING.md).

### Clarify Biostatistics dates

Replace the generic `Project work` and `Final work` entries in
[site_docs/fall_2026/biostats/SCHEDULE.md](../../../site_docs/fall_2026/biostats/SCHEDULE.md) with the
names and public dates of the major deliverables. Exact submission times may remain in the
assignment directions.

### Set feedback timing

Choose a feedback promise the instructor can reliably meet, then state it for all three courses.
The present policy promises feedback but gives neither fixed feedback dates nor a normal turnaround
interval. Confirm with the department whether a turnaround such as a stated number of business
days satisfies its `Assignment feedback dates` item.

Put one shared promise in
[site_docs/fall_2026/shared/policies/COURSE_EXPECTATIONS.md](../../../site_docs/fall_2026/shared/policies/COURSE_EXPECTATIONS.md)
if it is the same for every course. Use course-specific coursework pages if the timing differs.

### Add acknowledgment

Decide how students will acknowledge the policies and resources. A required Blackboard syllabus
acknowledgment or orientation activity is the simplest private mechanism. Add a public statement
describing the requirement, while keeping completion records and student data in Blackboard.

## Suggested decisions

These items do not require invented content. Confirm the real course arrangement, then either add
useful information or mark the item not applicable.

- **Teaching assistant information:** confirm whether each course has a teaching assistant. This is
  still open for all three courses.
- **Assignment formatting:** add a concise general rule or a link to the applicable directions for
  Biostatistics and Genetics. Biotechnology is covered by its project and talking-point pages.
- **Optional resources:** add a separate optional resource for Genetics only if one is genuinely
  recommended; otherwise mark this suggested item not applicable.

## Accessibility status

No accessibility content change is currently required by this checklist. The generated DOCX,
semantic headings, descriptive links, color handling, and table headers are covered. The instructor
portrait has descriptive alt text. Captioned videos are not applicable because the public syllabi
embed no videos; recheck that item if a video is added.

## Rerun after decisions

After updating course content and `pipeline/department_checklists.yml`, regenerate the submission
artifacts:

```bash
source source_me.sh
python3 pipeline/build_department_checklists.py
```

Run the full local gate after changing live syllabus content:

```bash
./all_test.sh
```
