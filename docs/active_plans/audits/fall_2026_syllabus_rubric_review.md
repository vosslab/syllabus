# Fall 2026 syllabus checklist actions

Revalidated August 31, 2026 against the tracked 53-item rubric, the live Fall 2026 sources, and
freshly regenerated department checklists. This document lists only unresolved checklist work.
One shared decision may close the same item for more than one course.

## Current open work

| Course | Resolved | Required open | Suggested open | Total open |
| --- | ---: | ---: | ---: | ---: |
| BIOL 318/418 | 50 of 53 | 2 | 1 | 3 |
| BIOL 351/451 | 52 of 53 | 0 | 1 | 1 |
| BIOL 480 | 53 of 53 | 0 | 0 | 0 |

Use `raw/Dept_University_Docs/Syllabus_Checklist_Fall_2026_updated.md` as the private 53-item
reference checklist. The tracked status source is
[pipeline/department_checklists.yml](../../../pipeline/department_checklists.yml), and the public
evidence authority is [site_docs/fall_2026/](../../../site_docs/fall_2026/). Regenerate the ignored
Markdown and DOCX submission artifacts under `output/department_checklists/`; do not edit those
artifacts directly.

## Required actions

### 1. Finalize the BIOL 318/418 point plan

- Checklist item: `assignment_points`.
- [ ] Approve or revise the proposed
  [Biostatistics point plan](../decisions/biostats_point_plan.md).
- [ ] Decide the number of group quizzes, regular-assignment total, and extra-credit cap.
- [ ] Add the confirmed `course_point_plan` to
  [biostats/syllabus.yml](../../../site_docs/fall_2026/biostats/syllabus.yml).
- [ ] Add the point-plan marker to
  [biostats/ASSIGNMENTS_AND_GRADING.md](../../../site_docs/fall_2026/biostats/ASSIGNMENTS_AND_GRADING.md).

### 2. Name and date the major BIOL 318/418 work

- Checklist item: `major_due_dates`.
- [ ] Confirm whether the existing December 9 and December 16 schedule rows are the actual due
  dates.
- [ ] Replace `Project work` and `Final work` in
  [biostats/SCHEDULE.md](../../../site_docs/fall_2026/biostats/SCHEDULE.md) with the actual
  deliverable names.
- [ ] Keep exact submission times in the assignment directions when they do not belong in the
  public syllabus.

## Suggested decisions

These items may be marked not applicable when that accurately describes the course. Do not add
student-facing content solely to fill a suggested item.

- [ ] **`assignment_formatting`, BIOL 318/418 and BIOL 351/451:** revisit this after the assignment
  platform is selected. Add a concise general rule only if one applies across assignments;
  otherwise keep formatting in assignment-specific directions and mark the item not applicable.

## Regenerate and verify

After making an instructor decision, update the live source first, then update the matching status,
evidence, and note in `pipeline/department_checklists.yml`. Rebuild the checklist artifacts:

```bash
source source_me.sh
python3 pipeline/build_department_checklists.py
```

After changing live syllabus content, run the complete local gate:

```bash
./all_test.sh
```
