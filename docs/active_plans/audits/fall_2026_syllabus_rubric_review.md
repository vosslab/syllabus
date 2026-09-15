# Fall 2026 syllabus readiness audit

Updated September 14, 2026 for the instructor-approved Biostatistics point plan. The readiness
summary follows the tracked 53-item rubric and live Fall 2026 sources.

## Readiness summary

**Ready** means that all 53 required and suggested rubric items are covered or justified as not
applicable.

| Course | Required gaps | Suggested follow-up | Status |
| --- | ---: | ---: | --- |
| BIOL 480 | 0 | 0 | **READY - all 53 items resolved** |
| BIOL 351/451 | 0 | 0 | **READY - all 53 items resolved** |
| BIOL 318/418 | 1 | 0 | **NOT READY - due dates require confirmation** |

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

The point plan is approved: 50 tutorial-assignment points and three 20-point group quizzes, for
110 total points. The live coursework page now resolves `assignment_points`. The remaining
required item is the dated assessment schedule.

### Name and date major work

- **Rubric item:** `major_due_dates`.
- **Decision:** Confirm tutorial deliverable deadlines and the three group-quiz dates. The
  September 14 correction removed unsupported project and final-work placeholders
  and restored the historical topic sequence, including five hypothesis-testing tutorial sessions.
- **Update:** Add confirmed deliverable names and due dates to
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
