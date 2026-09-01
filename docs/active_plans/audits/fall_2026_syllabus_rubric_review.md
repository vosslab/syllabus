# Fall 2026 syllabus checklist actions

Revalidated August 31, 2026 against the tracked 53-item rubric, the live Fall 2026 sources, and
freshly regenerated department checklists. This document lists only unresolved checklist work.
One shared decision may close the same item for more than one course.

## Current open work

| Course | Resolved | Required open | Suggested open | Total open |
| --- | ---: | ---: | ---: | ---: |
| BIOL 318/418 | 48 of 53 | 3 | 2 | 5 |
| BIOL 351/451 | 49 of 53 | 1 | 3 | 4 |
| BIOL 480 | 51 of 53 | 1 | 1 | 2 |

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

### 3. Add a policy-and-resources acknowledgment

- Checklist item: `policy_acknowledgment` for all three courses.
- [ ] Decide whether each existing Week 1 `Course orientation` activity will include acknowledgment
  of the syllabus policies and student resources, or choose another activity on the selected
  assessment platform.
- [ ] Add a short public statement that the activity is required.
- [ ] Keep the submitted activity on the assessment platform and transfer its score to the
  Blackboard gradebook.
- [ ] Add the public statement as checklist evidence for all three courses.

## Suggested decisions

These items may be marked not applicable when that accurately describes the course. Do not add
student-facing content solely to fill a suggested item.

- [ ] **`teaching_assistant`, all courses:** confirm whether each course has a teaching assistant.
  Add the assigned person's public contact information or mark the item not applicable. Dr. Nate
  La Porte's coordination role does not establish that a teaching assistant is assigned.
- [ ] **`assignment_formatting`, BIOL 318/418 and BIOL 351/451:** add one concise general rule or
  link to the applicable directions. If formatting is assignment-specific and provided on the
  current assessment platform, mark the suggested item not applicable and record that rationale.
- [ ] **`optional_resources`, BIOL 351/451:** add a resource only if one is genuinely recommended;
  otherwise mark the suggested item not applicable. The required free OER does not also count as
  an optional resource.

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
