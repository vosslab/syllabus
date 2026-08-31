# Fall 2026 syllabus checklist actions

Reviewed August 31, 2026. This document lists only unresolved department-checklist work.

## Current open work

| Course | Required open | Suggested open | Total open |
| --- | ---: | ---: | ---: |
| BIOL 318/418 | 3 | 2 | 5 |
| BIOL 351/451 | 1 | 3 | 4 |
| BIOL 480 | 1 | 1 | 2 |

Use `raw/Dept_University_Docs/Syllabus_Checklist_Fall_2026_updated.md` as the 53-item source
checklist. Edit [pipeline/department_checklists.yml](../../../pipeline/department_checklists.yml),
then regenerate the ignored Markdown and DOCX submission artifacts under
`output/department_checklists/`.

## Required actions

### 1. Finalize the BIOL 318/418 point plan

- [ ] Approve or revise the proposed
  [Biostatistics point plan](../decisions/biostats_point_plan.md).
- [ ] Decide the number of group quizzes, regular-assignment total, and extra-credit cap.
- [ ] Add the confirmed `course_point_plan` to
  [biostats/syllabus.yml](../../../site_docs/fall_2026/biostats/syllabus.yml).
- [ ] Add the point-plan marker to
  [biostats/ASSIGNMENTS_AND_GRADING.md](../../../site_docs/fall_2026/biostats/ASSIGNMENTS_AND_GRADING.md).

### 2. Name and date the major BIOL 318/418 work

- [ ] Replace `Project work` and `Final work` in
  [biostats/SCHEDULE.md](../../../site_docs/fall_2026/biostats/SCHEDULE.md) with the actual
  deliverable names and public dates.
- [ ] Keep exact submission times in the assignment directions when they do not belong in the
  public syllabus.

### 3. Add a policy-and-resources acknowledgment

- [ ] Choose one syllabus acknowledgment or orientation activity that works on the selected
  assessment platform for all three courses.
- [ ] Add a short public statement that the activity is required.
- [ ] Keep the submitted activity on the assessment platform and transfer its score to the
  Blackboard gradebook.
- [ ] Add the public statement as checklist evidence for all three courses.

## Suggested decisions

These items may be marked not applicable when that accurately describes the course.

- [ ] **Teaching assistants, all courses:** confirm whether each course has a teaching assistant.
  Add the applicable contact or mark the item not applicable.
- [ ] **Assignment formatting, BIOL 318/418 and BIOL 351/451:** add one concise general rule or link
  to the applicable directions. If formatting is assignment-specific and provided on the current
  assessment platform, record that decision instead of inventing a universal rule.
- [ ] **Optional resources, BIOL 351/451:** add a resource only if one is genuinely recommended;
  otherwise mark the suggested item not applicable.

## Regenerate and verify

After making a decision, update the checklist evidence and rebuild its artifacts:

```bash
source source_me.sh
python3 pipeline/build_department_checklists.py
```

After changing live syllabus content, run the complete local gate:

```bash
./all_test.sh
```
