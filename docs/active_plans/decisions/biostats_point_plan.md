# Biostatistics point-plan draft

Status: instructor review required. This draft does not change the live Fall 2026 syllabus.

## Proposed plan

| Assessment | Possible points | Derived share | Your points |
| --- | ---: | ---: | ---: |
| Tutorial assignments | 50 | 45.5% | |
| Three group quizzes | 60 | 54.5% | |
| **Total** | **110** | **100%** | |

Each group quiz is worth 20 points under the current shared group-quiz format. Extra-credit points
remain outside the 110-point denominator. The 50 assignment points are a working estimate; changing
that one YAML value will rederive the total and both shares before the draft is promoted.

## Proposed YAML

If approved, add this ordered list to
[site_docs/fall_2026/biostats/syllabus.yml](../../../site_docs/fall_2026/biostats/syllabus.yml):

```yaml
course_point_plan:
  - assessment: Tutorial assignments
    points: 50
  - assessment: Three group quizzes
    points: 60
```

Retain the current assessment-fragment selection:

```yaml
assessments:
  - assignments
  - group_quizzes
```

The point-plan renderer will calculate the percentages and total for the website, PDF, and DOCX.

## Evidence

- The local Fall 2025 point sheet, printed as modified August 25, 2026, gives Tutorial Assignments
  50 possible points and 12 extra-credit points outside its 50-point denominator. This ignored
  authoring evidence is not itself a publication authority.
- The current
  [site_docs/fall_2026/biostats/SCHEDULE.md](../../../site_docs/fall_2026/biostats/SCHEDULE.md)
  already centers weekly assignments and tutorial work.
- The current shared group-quiz format gives each quiz 20 possible points. Three quizzes therefore
  contribute 60 points without inventing another scoring rule.
- The June CURE redesign assumes a larger, mostly remote course and remains a working draft. Its
  research-project structure is not required for this smaller face-to-face launch plan.

## Student-facing result

The live coursework page would keep its current grading-policy and Blackboard statements, add the
derived table above, and retain the shared assignment and group-quiz explanations. It would also
state that extra-credit opportunities do not increase the denominator used for the final
percentage.

## Decisions before promotion

- [ ] Confirm exactly three group quizzes for Fall 2026.
- [ ] Confirm that all regular tutorial assignments together contribute 50 possible points.
- [ ] Confirm whether 12 is the intended maximum number of extra-credit points; this value remains
  outside `course_point_plan` either way.

## Promotion checklist

1. Add the proposed `course_point_plan` to the Biostatistics manifest.
2. Add the exact course-point-plan marker below the Coursework and grades title.
3. Add the extra-credit denominator sentence to the coursework page.
4. Build the live site and all three PDF/DOCX syllabi.
5. Run the complete fast, export, and Playwright validation lanes.
