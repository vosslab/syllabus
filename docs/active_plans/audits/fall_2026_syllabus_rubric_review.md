# Fall 2026 syllabus readiness audit

Revalidated August 31, 2026 against the tracked 53-item rubric, the live Fall 2026 sources, and
freshly regenerated department checklists. This document shows course readiness first, then lists
only the work that remains.

## Readiness summary

**Ready** means that all 53 required and suggested rubric items are covered or justified as not
applicable.

| Course | Required gaps | Suggested follow-up | Status |
| --- | ---: | ---: | --- |
| BIOL 480 | 0 | 0 | **READY - all 53 items resolved** |
| BIOL 351/451 | 0 | 0 | **READY - all 53 items resolved** |
| BIOL 318/418 | 2 | 0 | **NOT READY - instructor decisions required** |

## Ready courses

### BIOL 480

BIOL 480 is rubric-complete. Its point plan, dated project sequence, project and talking-point
format requirements, feedback sequence, discussion method, and shared policies provide evidence
for all 53 items. No checklist action remains before Fall 2026 use.

### BIOL 351/451

BIOL 351/451 is rubric-complete and ready for Fall 2026 use. Its point plan, five dated quizzes,
numbered assignments, midterm and final exam dates, lecture-only scope, and separate undergraduate
CORE information cover the required items. The course-specific Biology Problems OER link supplies
representative assignment formats, while each released assignment supplies its exact directions
and settings.

## Required BIOL 318/418 work

These two instructor decisions keep BIOL 318/418 from final rubric readiness.

### 1. Confirm the point plan

- **Rubric item:** `assignment_points`.
- **Decision:** Confirm the number of group quizzes, regular-assignment points, and extra-credit
  cap in [biostats_point_plan.md](../decisions/biostats_point_plan.md).
- **Update:** Add the approved values to
  [syllabus.yml](../../../site_docs/fall_2026/biostats/syllabus.yml) and add the derived-table
  marker to
  [ASSIGNMENTS_AND_GRADING.md](../../../site_docs/fall_2026/biostats/ASSIGNMENTS_AND_GRADING.md).

### 2. Name and date major work

- **Rubric item:** `major_due_dates`.
- **Decision:** Confirm whether December 9 and December 16 are the actual deadlines.
- **Update:** Replace `Project work` and `Final work` with the real deliverable names in
  [SCHEDULE.md](../../../site_docs/fall_2026/biostats/SCHEDULE.md).

Keep exact submission times in assignment directions when they do not belong in the public
syllabus.

## Sources and verification

The private checklist reference is
`raw/Dept_University_Docs/Syllabus_Checklist_Fall_2026_updated.md`. The tracked status source is
[pipeline/department_checklists.yml](../../../pipeline/department_checklists.yml), and the public
evidence authority is [site_docs/fall_2026/](../../../site_docs/fall_2026/).

After an instructor decision, update the live syllabus source first, then update the matching
status, evidence, and note in `pipeline/department_checklists.yml`. Rebuild the ignored department
checklists with:

```bash
source source_me.sh
python3 pipeline/build_department_checklists.py
```

After changing live syllabus content, run the complete local gate:

```bash
./all_test.sh
```
