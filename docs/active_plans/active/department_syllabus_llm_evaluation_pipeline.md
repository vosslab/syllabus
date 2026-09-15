# Plan: Department syllabus LLM evaluation pipeline

## Context

The current repository contains a 53-item department syllabus checklist and a generator for Neil
Voss's three Fall 2026 courses. The checklist decisions and supporting evidence are already stored
in structured YAML, and deterministic code produces Markdown, DOCX, and PDF review sheets.

Bob's problem begins earlier in the process. He needs to evaluate a mixed collection of PDF and
DOCX syllabi from more than 50 professors. The documents will differ in organization, formatting,
terminology, page numbering, and completeness. An LLM must interpret each syllabus against the
same rubric. That evaluation is inherently nondeterministic; the surrounding pipeline must make
its inputs, evidence, decisions, uncertainty, and run provenance inspectable.

The system should reduce repetitive reading while preserving a practical human-review path. It
must distinguish a mechanically valid output from a substantively correct rubric judgment.

## Objectives

- Ingest a department folder containing heterogeneous PDF and DOCX syllabi without requiring
  instructors to rewrite or reformat them.
- Apply one versioned department rubric to every syllabus through a controlled LLM evaluation
  pipeline.
- Require exact, page-addressable evidence for positive findings and an explanation for every
  missing, partial, unclear, or not-applicable classification.
- Produce a department workbook, individual course findings, and a prioritized human-review queue.
- Measure evaluation quality and repeated-run consistency on a representative calibration set.
- Preserve enough provenance to reproduce the inputs and explain how every finding was produced.

## Design philosophy

Follow **Use the scientific method** and **Ground requirements in actual needs**. Treat prompts,
models, extraction methods, and confidence rules as hypotheses evaluated against real department
syllabi. The LLM supplies semantic judgment; deterministic components enforce document identity,
schema completeness, evidence traceability, output construction, and run records.

The pipeline should optimize for trustworthy evidence and efficient review. It should allow
`unclear` rather than force a binary answer, and it should direct human attention to the smallest
set of findings most likely to affect a department decision.

## Scope

- Define a department-wide rubric independent of Neil's course-specific evidence and exceptions.
- Inventory and normalize mixed PDF and DOCX inputs while retaining course and page identity.
- Extract page-aware text, tables, headings, and basic document metadata.
- Evaluate every rubric item for every syllabus with an LLM and a strict structured response.
- Verify quoted evidence against extracted source text.
- Detect incomplete, contradictory, unsupported, and low-confidence findings.
- Re-evaluate or adjudicate only findings that meet documented escalation criteria.
- Export an Excel workbook and machine-readable run artifacts.
- Calibrate quality on a representative human-reviewed sample before department-wide use.
- Document local/private input boundaries, operator commands, limitations, and recovery steps.

## Non-goals

- Eliminate LLM variability or describe semantic evaluation as deterministic.
- Turn the department rubric into a judgment of teaching quality.
- Require all instructors to adopt this repository's Markdown authoring system.
- Publish submitted syllabi, extracted text, prompts containing syllabus content, or evaluation
  results in the public repository.
- Include student records, grades, accommodations, or other student-level data.
- Automatically contact instructors or distribute findings.
- Treat model confidence as proof of correctness.
- Replace department review or policy decisions with an automated score.

## Current state summary

- [pipeline/department_checklists.yml](../../../pipeline/department_checklists.yml) combines the
  ordered rubric with evidence and overrides for three Voss syllabi. It is a useful starting point,
  but its notes and exceptions are not automatically department-wide rules.
- [pipeline/build_department_checklists.py](../../../pipeline/build_department_checklists.py)
  validates structured findings and produces accessible review documents after the evaluation has
  already occurred.
- The current generator relies on known Markdown sources and named PDF destinations. Arbitrary
  department documents will instead need page-aware extraction and source-text verification.
- Generated-output replacement and post-evaluation document construction are already solved. The
  new implementation effort belongs in ingestion, LLM evaluation, calibration, and aggregation.

## Assumptions

- The department can provide one folder of syllabi and enough metadata to identify course,
  section, term, and instructor.
- Most inputs are text-bearing PDF or DOCX files; a smaller OCR path will handle scanned PDFs.
- Department reviewers can manually evaluate a representative calibration sample and resolve
  ambiguous rubric wording.
- The chosen LLM service and account are approved for the supplied documents before live use.
- A single syllabus may cover multiple cross-listed sections and must remain one document record
  with multiple section identifiers.

## Architecture boundaries and ownership

### Mapping (milestones / workstreams -> components / patches)

| Milestone / Workstream | Component | Review boundary |
| --- | --- | --- |
| M1 / rubric | Department rubric contract | Meaning, applicability, and required evidence |
| M1 / corpus | Private input inventory | Document identity and representative calibration sample |
| M2 / ingestion | Document normalizer | PDF/DOCX/OCR extraction and page mapping |
| M3 / evaluation | LLM evaluator | Prompt, structured response, and model adapter |
| M3 / validation | Evidence validator | Quote matching, completeness, and escalation rules |
| M4 / quality | Calibration harness | Human reference set, metrics, and repeated-run comparison |
| M5 / reporting | Workbook exporter | Department, course, finding, and review-queue sheets |
| M6 / operations | CLI and run manifest | End-to-end execution, caching, provenance, and recovery |

### Proposed component ownership

- `pipeline/department_syllabus_rubric.yml`: department-wide rubric meaning and applicability.
- `pipeline/department_review/ingest.py`: inventory, conversion, extraction, and page-aware records.
- `pipeline/department_review/evaluate.py`: LLM request construction and structured-result parsing.
- `pipeline/department_review/validate.py`: evidence matching and finding-level quality rules.
- `pipeline/department_review/calibrate.py`: comparison with human reference judgments.
- `pipeline/department_review/export.py`: Excel and per-course output generation.
- `pipeline/evaluate_department_syllabi.py`: operator-facing command coordinator.
- `raw/department_syllabi/`: ignored local input documents and private metadata.
- `output/department_review/`: ignored extracted text, run manifests, findings, and reports.

The exact module split should remain adjustable until the ingestion and evaluation prototypes show
their natural boundaries.

## Data inventory

### Input manifest

Each document receives one stable record before evaluation:

| Field | Meaning |
| --- | --- |
| `document_id` | Stable local identifier independent of filename |
| `source_filename` | Original filename |
| `sha256` | Exact document-content identity |
| `course_codes` | One or more course and section identifiers |
| `term` | Academic term represented by the syllabus |
| `instructor` | Instructor name as department metadata |
| `source_format` | PDF or DOCX |
| `extraction_method` | Native PDF, DOCX conversion, or OCR |
| `page_count` | Canonical review-PDF page count |
| `extraction_warnings` | Empty pages, OCR use, corrupt tables, or conversion differences |

### Rubric contract

Every rubric item should contain:

| Field | Meaning |
| --- | --- |
| `id` | Stable machine identifier |
| `group` | Required or suggested department grouping |
| `label` | Reviewer-facing name |
| `requirement` | Plain-language condition being evaluated |
| `applicability` | Conditions under which the item applies |
| `covered_when` | Minimum evidence required for `covered` |
| `partial_when` | Evidence that supports only part of the requirement |
| `not_applicable_when` | Positive conditions that permit that classification |
| `examples` | Illustrative evidence that does not redefine the rule |

### Finding contract

Each syllabus-rubric pair produces one finding:

| Field | Meaning |
| --- | --- |
| `document_id` | Evaluated syllabus |
| `rubric_id` | Evaluated requirement |
| `status` | `covered`, `partial`, `missing`, `unclear`, or `not_applicable` |
| `evidence` | Zero or more exact quotations with canonical PDF page numbers |
| `explanation` | Concise relationship between evidence and requirement |
| `uncertainty` | Specific ambiguity, conflict, or extraction limitation |
| `review_priority` | `none`, `normal`, or `high` based on explicit rules |
| `evaluation_pass` | Initial, retry, or adjudication pass |
| `prompt_version` | Versioned evaluation instructions |
| `model` | Exact model identifier reported by the provider |
| `run_id` | Evaluation-run provenance |

Confidence may be retained as a diagnostic model output, but escalation should depend primarily on
observable conditions such as missing evidence, extraction warnings, disagreement, or prohibited
status/evidence combinations.

## User-facing contract

The operator supplies an input directory and a metadata file, runs one command, and receives a
complete review bundle. A dry run inventories documents, reports conversion/extraction problems,
counts expected LLM evaluations, and estimates workload without sending syllabus content.

The normal run should support these conceptual stages:

```text
inventory -> normalize -> extract -> evaluate -> verify evidence
          -> retry or adjudicate -> aggregate -> export
```

An interrupted run resumes from validated cached stages keyed by document hash, rubric version,
prompt version, model configuration, and extraction version. Changing any semantic input invalidates
the affected cache entry. The cache prevents unnecessary calls; it does not make LLM judgments
deterministic.

## Milestone plan

| M | Title | Summary | Goal |
| --- | --- | --- | --- |
| M1 | Establish the rubric and corpus | Separate department rules and select calibration documents | Define what the evaluator must decide |
| M2 | Normalize heterogeneous syllabi | Produce page-aware canonical representations | Give the LLM reliable document input |
| M3 | Build the evaluation loop | Generate and validate structured LLM findings | Complete one inspectable evaluation run |
| M4 | Calibrate quality and consistency | Compare runs with human judgments | Establish evidence-based acceptance thresholds |
| M5 | Produce department reports | Export reviewable Excel and course findings | Make results useful to Bob and reviewers |
| M6 | Operationalize the pipeline | Add resumability, provenance, and documentation | Run 50-plus syllabi safely and repeatably |

### Milestone: M1 establish the rubric and corpus

- Depends on: none.
- Deliverables:
  - A department-only rubric derived from the existing checklist.
  - A decision log for items whose applicability or evidence standard is ambiguous.
  - A private inventory of available syllabi and formats.
  - A representative calibration set spanning course levels, modalities, labs, cross-listings,
    document formats, and instructors.
- Entry criteria: department checklist and sample syllabi are available.
- Exit criteria:
  - Every rubric item has a plain-language requirement and observable evidence rule.
  - Personal Voss evidence and course-specific exceptions are excluded from department defaults.
  - The calibration set represents the document diversity the full run will encounter.
- Parallel-plan ready: yes; rubric clarification and private corpus inventory can proceed as two
  independent workstreams, maximum two.

### Milestone: M2 normalize heterogeneous syllabi

- Depends on: M1 corpus inventory defines actual formats.
- Deliverables:
  - Stable document manifest and hashing.
  - Canonical PDF for page references.
  - Page-aware extracted text and tables.
  - OCR path for scanned pages.
  - Extraction-quality report.
- Entry criteria: representative corpus is inventoried.
- Exit criteria:
  - Every calibration document has a canonical PDF and structured page records.
  - Page citations can be traced back to the visible canonical document.
  - Empty, scanned, encrypted, corrupt, and conversion-sensitive documents fail clearly or enter
    a review queue.
- Parallel-plan ready: yes; native PDF, DOCX conversion, and OCR experiments may run independently,
  maximum three, with one owner integrating the canonical page record.

### Milestone: M3 build the evaluation loop

- Depends on: M1 rubric contract and M2 canonical page records.
- Deliverables:
  - Versioned system and task instructions.
  - Strict structured-output schema.
  - Provider/model adapter with recorded model identity and usage.
  - Evidence verifier and finding validator.
  - Retry and adjudication policy.
- Entry criteria: at least five representative documents extract successfully.
- Exit criteria:
  - Every requested document-rubric pair produces exactly one schema-valid finding.
  - Every positive finding includes evidence that matches an extracted page after documented
    whitespace and line-break normalization.
  - Unsupported quotations, invalid pages, forced not-applicable decisions, and contradictory
    findings enter review or re-evaluation instead of passing.
  - Prompt and model provenance are stored for every result.
- Parallel-plan ready: yes; evaluator, schema/validator, and provider adapter can proceed after the
  contracts are fixed, maximum three.

### Milestone: M4 calibrate quality and consistency

- Depends on: M3 produces complete findings for the calibration set.
- Deliverables:
  - Human reference findings for the selected sample.
  - Per-status agreement and confusion matrix.
  - Evidence-support accuracy measurement.
  - Repeated-run disagreement report.
  - Revised prompts, rubric wording, or escalation rules based on observed failures.
- Entry criteria: two department reviewers can resolve calibration disagreements.
- Exit criteria:
  - All required rubric items meet the department-approved agreement threshold.
  - Unsupported `covered` findings meet a stricter department-approved maximum error rate.
  - Repeated-run disagreements are concentrated in the review queue rather than silently changing
    department conclusions.
  - Failed thresholds have a correction path: improve extraction, clarify the rubric, revise the
    prompt, change the model, or widen human review.
- Parallel-plan ready: no; a common frozen evaluation configuration and reference set are required
  before measurements are comparable.

### Milestone: M5 produce department reports

- Depends on: M3 finding schema is stable and M4 establishes usable review flags.
- Deliverables:
  - Excel workbook with `Department Summary`, `All Findings`, `Needs Review`, `Rubric`, and `Run
    Information` sheets.
  - Optional individual course reports generated from the same findings.
  - Filters and stable identifiers that support correction without rerunning unrelated syllabi.
- Entry criteria: finding semantics and escalation rules are accepted.
- Exit criteria:
  - Workbook counts reconcile exactly with the machine-readable findings.
  - Every summary value can be traced to course-level rows and source evidence.
  - Missing, partial, unclear, and not-applicable statuses remain distinct.
  - Spreadsheet formulas and formatting do not alter source findings.
- Parallel-plan ready: yes; workbook and individual-report exporters may proceed independently,
  maximum two, with one owner for shared status semantics.

### Milestone: M6 operationalize the pipeline

- Depends on: M2 through M5 pass their acceptance gates.
- Deliverables:
  - Dry-run, full-run, resume, and targeted-rerun commands.
  - Cache invalidation and run manifest.
  - Cost/usage summary and failure recovery.
  - Operator documentation and private-data boundary checks.
  - Full 50-plus-syllabus pilot.
- Entry criteria: calibration results meet the approved thresholds.
- Exit criteria:
  - A clean full run produces the complete expected finding matrix and workbook.
  - An interrupted run resumes without repeating validated work.
  - A changed syllabus reruns only that document; a changed rubric item reruns that item across all
    affected documents.
  - No private input or generated evaluation artifact becomes tracked or published.
- Parallel-plan ready: yes; CLI/resume behavior, documentation, and privacy-boundary verification
  may proceed independently, maximum three, after the pipeline interfaces stabilize.

## Workstream breakdown

### Workstream: rubric and policy

- Goal: define fair, department-wide evaluation semantics.
- Owner: department rubric lead.
- Work packages: WP-R1, WP-R2, WP-R3.
- Needs: official checklist and department interpretation decisions.
- Provides: versioned rubric and calibration reference rules.
- Review boundary, when modifying the repository: rubric and decision documentation only.

### Workstream: document ingestion

- Goal: turn heterogeneous files into reliable page-addressable records.
- Owner: ingestion implementer.
- Work packages: WP-I1, WP-I2, WP-I3.
- Needs: representative private corpus.
- Provides: canonical PDFs, extracted page records, and warnings.
- Review boundary, when modifying the repository: ingestion modules and fixtures without live
  syllabus content.

### Workstream: LLM evaluation

- Goal: produce complete structured findings with traceable evidence.
- Owner: evaluation implementer.
- Work packages: WP-E1, WP-E2, WP-E3.
- Needs: rubric contract and extracted page records.
- Provides: validated findings and escalation records.
- Review boundary, when modifying the repository: prompts, schemas, adapters, and validators.

### Workstream: calibration and reporting

- Goal: measure usefulness and deliver reviewable department outputs.
- Owner: quality and reporting implementer.
- Work packages: WP-Q1, WP-Q2, WP-O1.
- Needs: evaluation results and human reference judgments.
- Provides: quality report, workbook, and review queue.
- Review boundary, when modifying the repository: calibration and exporter modules plus synthetic
  fixtures.

## Work packages

### Work package: WP-R1 separate the department rubric

- Owner: department rubric lead.
- Touch points: new rubric YAML and rubric documentation.
- Depends on: none.
- Acceptance criteria: all 53 current items are retained, intentionally revised, or explicitly
  excluded with a recorded reason; Voss-specific evidence is not a department default.
- Evidence or review, when useful: Bob and one additional department reviewer approve ambiguous
  applicability rules.
- Obvious follow-ons: WP-R2 and WP-E1.

### Work package: WP-R2 define status and evidence semantics

- Owner: department rubric lead.
- Touch points: rubric schema and reviewer guide.
- Depends on: WP-R1 because item meaning must be stable.
- Acceptance criteria: `covered`, `partial`, `missing`, `unclear`, and `not_applicable` each have
  distinct decision rules and examples.
- Evidence or review, when useful: reviewers independently classify a small shared sample and
  reconcile differences.
- Obvious follow-ons: WP-Q1.

### Work package: WP-R3 select the calibration corpus

- Owner: department corpus steward.
- Touch points: ignored input manifest and private sample documents.
- Depends on: none.
- Acceptance criteria: sample diversity is documented and filenames map unambiguously to course,
  section, instructor, and term.
- Evidence or review, when useful: inventory report with no syllabus content committed.
- Obvious follow-ons: WP-I1.

### Work package: WP-I1 prototype page-aware extraction

- Owner: ingestion implementer.
- Touch points: ingestion module and synthetic fixtures.
- Depends on: WP-R3 because actual document formats determine experiments.
- Acceptance criteria: native PDFs and converted DOCX files yield page records with stable page
  numbers and readable text.
- Evidence or review, when useful: compare extracted pages with visible originals across the sample.
- Obvious follow-ons: WP-I2 and WP-E1.

### Work package: WP-I2 handle difficult documents

- Owner: ingestion implementer.
- Touch points: OCR/conversion adapter and warning model.
- Depends on: WP-I1 defines canonical page records.
- Acceptance criteria: scanned, empty, encrypted, malformed, and table-heavy files either extract
  acceptably or produce actionable warnings.
- Evidence or review, when useful: extraction-quality report by failure class.
- Obvious follow-ons: WP-E3.

### Work package: WP-I3 implement identity and cache keys

- Owner: ingestion implementer.
- Touch points: manifest, hashes, version fields, and cache layout.
- Depends on: WP-I1 provides normalized artifacts.
- Acceptance criteria: identical semantic inputs reuse results; changed documents, rubrics, prompts,
  models, or extraction versions invalidate the correct scope.
- Evidence or review, when useful: targeted invalidation scenarios.
- Obvious follow-ons: WP-O1.

### Work package: WP-E1 design the structured evaluation request

- Owner: evaluation implementer.
- Touch points: prompt templates and finding schema.
- Depends on: WP-R1, WP-R2, and WP-I1.
- Acceptance criteria: the model receives explicit rubric meaning, allowed statuses, full relevant
  document context, evidence requirements, and permission to return `unclear`.
- Evidence or review, when useful: inspect raw responses for a diverse five-document slice.
- Obvious follow-ons: WP-E2.

### Work package: WP-E2 validate findings and quotations

- Owner: evaluation implementer.
- Touch points: finding validator and evidence matcher.
- Depends on: WP-E1 and WP-I1.
- Acceptance criteria: schema errors, nonexistent quotations, invalid pages, incomplete findings,
  and invalid status/evidence combinations cannot enter accepted results.
- Evidence or review, when useful: adversarial synthetic findings and real extraction edge cases.
- Obvious follow-ons: WP-E3 and WP-Q1.

### Work package: WP-E3 implement selective retry and adjudication

- Owner: evaluation implementer.
- Touch points: orchestration and escalation policy.
- Depends on: WP-E2 identifies observable failure conditions.
- Acceptance criteria: retries address transient/schema failures; adjudication compares conflicting
  supported findings; persistent uncertainty reaches human review.
- Evidence or review, when useful: run logs show why each additional LLM call occurred.
- Obvious follow-ons: WP-Q2 and WP-O1.

### Work package: WP-Q1 build the human reference set

- Owner: department quality lead.
- Touch points: private reference findings and calibration documentation.
- Depends on: WP-R2 and WP-R3.
- Acceptance criteria: two reviewers independently evaluate the sample, reconcile differences, and
  preserve the final rationale.
- Evidence or review, when useful: inter-reviewer agreement before LLM comparison.
- Obvious follow-ons: WP-Q2.

### Work package: WP-Q2 measure and improve evaluation quality

- Owner: department quality lead.
- Touch points: calibration harness and reports.
- Depends on: WP-E2, WP-E3, and WP-Q1.
- Acceptance criteria: report status agreement, unsupported-positive rate, evidence accuracy,
  review-queue capture, and repeated-run disagreement by rubric item.
- Evidence or review, when useful: frozen comparison runs and recorded corrective decisions.
- Obvious follow-ons: approve or block the department pilot.

### Work package: WP-O1 export and operate the full review

- Owner: reporting implementer.
- Touch points: workbook exporter, CLI, run manifest, and operator guide.
- Depends on: WP-I3, WP-E3, and WP-Q2.
- Acceptance criteria: dry run, full run, resume, targeted rerun, reconciliation, and private output
  boundaries work on the department pilot.
- Evidence or review, when useful: end-to-end run receipt and workbook inspection.
- Obvious follow-ons: archive the completed plan and schedule rubric/model recalibration.

## Acceptance criteria and gates

- Per-patch gate: focused behavior tests, type/lint checks, private-data boundary inspection, and
  `git diff --check` pass.
- Ingestion gate: every calibration file either produces a page-addressable canonical record or a
  clearly classified failure; silent empty or truncated extraction blocks evaluation.
- Finding gate: the expected matrix contains exactly one finding for each document-rubric pair.
- Evidence gate: every `covered` and `partial` finding includes at least one source-matching quote
  and valid canonical page number.
- Applicability gate: every `not_applicable` finding cites the applicable rubric condition and a
  document fact or approved metadata value.
- Calibration gate: department reviewers approve measured thresholds before the 50-plus-syllabus
  pilot. Thresholds must be based on the calibration evidence rather than invented in advance.
- Reporting gate: workbook totals reconcile with machine-readable findings and preserve every
  unresolved item.
- Privacy gate: Git status and publication checks show no input syllabus, extraction, prompt
  payload, or evaluation result under tracked/public paths.
- Integration gate: the repository's applicable aggregate tests pass after implementation.

## Test and verification strategy

### Deterministic component tests

- Validate rubric, manifest, page-record, finding, and run-manifest schemas.
- Test PDF extraction, DOCX conversion, OCR routing, and explicit failure classes with synthetic
  documents.
- Verify whitespace-aware exact quotations across line wraps and hyphenation without allowing
  unsupported paraphrases to pass as quotations.
- Test complete matrix reconciliation, cache invalidation, resume behavior, and workbook totals.
- Confirm ignored input/output boundaries and prevent public builds from reading private review
  directories.

### LLM evaluation tests

- Freeze a small human-reviewed corpus outside the public repository.
- Compare status decisions and evidence against the human reference set.
- Run the same frozen configuration multiple times to measure disagreement rather than assume
  reproducibility.
- Report metrics by rubric item and document class; an aggregate score must not hide a weak
  required item.
- Track unsupported positive findings separately because they create a larger review risk than
  conservative `unclear` findings.
- Recalibrate after changes to the rubric, extraction method, prompt, model, or provider behavior.

### Pilot verification

- Start with five diverse syllabi, then expand to 15, then run the complete collection only after
  the prior stage passes.
- Review all high-priority findings and a random sample of accepted findings at each stage.
- Record extraction failures, LLM failures, disagreements, operator corrections, usage, and elapsed
  time.
- Stop expansion when the same failure class repeats; correct the extraction, rubric, or evaluation
  design before processing more documents.

## Migration and compatibility policy

- Preserve the existing Voss checklist and generator while the department pipeline is developed.
- Copy only genuinely department-wide rubric meaning into the new rubric; retain Voss-specific
  statuses and evidence in the current file.
- Use converters or adapters for old result files only if a real retained result must be migrated.
  Early prototypes may be discarded and rerun while their schemas remain experimental.
- Version rubric, prompt, extraction, and result schemas independently so a run manifest states
  exactly which combination produced each result.
- Treat a changed semantic version as a reason to reevaluate affected findings, not merely reformat
  old output.

## Risk register

| Risk | Impact | Trigger | Owner | Mitigation |
| --- | --- | --- | --- | --- |
| Rubric ambiguity | Different instructors receive inconsistent classifications | Human reviewers disagree on the same item | Rubric lead | Clarify applicability and evidence rules before prompt tuning |
| Unsupported positive finding | Missing requirement appears covered | Quote does not support the explanation | Evaluation owner | Exact evidence verification, calibration metric, and conservative escalation |
| Extraction failure | LLM judges incomplete or scrambled content | Empty pages, poor OCR, broken tables, or conversion drift | Ingestion owner | Quality warnings, visible canonical PDF, and block-on-failure rules |
| LLM run variability | Repeated runs change department conclusions | Supported findings disagree across frozen runs | Quality lead | Measure disagreement, adjudicate material conflicts, and route unstable items to review |
| Context overload | Long syllabi cause omitted evidence or shallow decisions | Findings cluster as missing despite visible content | Evaluation owner | Compare full-document, section-retrieval, and rubric-batch strategies on calibration data |
| Cost or quota exhaustion | Full run stops partway | Dry-run estimate exceeds available allowance or calls fail | Operator | Cache validated work, batch carefully, resume safely, and stage the rollout |
| Personal rules become department rules | Evaluation is unfair across instructors | Voss-specific notes appear in generic findings | Rubric lead | Separate rubric meaning from course evidence and approve the department rubric |
| Private content is published | Instructor documents or evaluations enter the public site/repository | Tracked or build-visible private artifact appears | Corpus steward | Ignored private roots, repository boundary tests, and pre-publication inspection |
| Workbook summary hides uncertainty | Leaders act on oversimplified counts | Partial and unclear findings collapse into missing or covered | Reporting owner | Preserve statuses and provide direct evidence and review queues |
| Model or provider drift | Prior calibration no longer represents current behavior | Model identifier or provider behavior changes | Quality lead | Pin recorded configuration and require recalibration on change |

## Rollout and release checklist

- [ ] Confirm the department rubric source and decision owners.
- [ ] Establish the ignored private input and output directories.
- [ ] Inventory formats and select the calibration corpus.
- [ ] Approve the finding statuses and evidence contract.
- [ ] Validate native PDF, DOCX, and OCR extraction on representative files.
- [ ] Complete the structured evaluator and evidence validator.
- [ ] Produce the reconciled human reference set.
- [ ] Measure calibration quality and repeated-run disagreement.
- [ ] Record approved thresholds and correction paths.
- [ ] Pass the five-document pilot.
- [ ] Pass the 15-document pilot.
- [ ] Complete the full department run and reconcile all expected findings.
- [ ] Inspect the review queue and a random sample of accepted findings.
- [ ] Deliver the workbook and operator notes through an approved private channel.
- [ ] Run repository validation and confirm that private artifacts remain untracked.

## Documentation close-out requirements

- Active plan / progress tracker: update this file with milestone status and evidence during
  implementation.
- `docs/CHANGELOG.md` entry: record durable pipeline behavior, validation evidence, and any rejected
  approach without including private syllabus content.
- Architecture and usage: update `docs/CODE_ARCHITECTURE.md`, `docs/FILE_STRUCTURE.md`,
  `docs/FILE_FORMATS.md`, and `docs/USAGE.md` once interfaces stabilize.
- Privacy boundary: document exactly which directories are ignored, which data is sent to an LLM
  provider, and which artifacts may be shared.
- Archive / closure notes: move this plan to `docs/archive/` with `git mv` after the calibrated full
  workflow is accepted and no planned implementation work remains.

## Patch plan and reporting format

- Patch 1: department rubric schema, private manifest contract, and synthetic fixtures.
- Patch 2: PDF/DOCX normalization, page-aware extraction, and quality warnings.
- Patch 3: LLM adapter, prompts, structured finding schema, and evidence verification.
- Patch 4: retry/adjudication orchestration, cache keys, and run provenance.
- Patch 5: calibration harness, repeated-run report, and documented acceptance decisions.
- Patch 6: workbook exporter, operator CLI, resume behavior, and full documentation.
- Patch 7: repository-required integration checks, pilot evidence, and plan closeout.

Each patch report should state the behavior delivered, files changed, focused verification, private
data handling, current calibration evidence, and remaining dependency. Do not report a successful
semantic evaluation merely because extraction, schema validation, or workbook generation passed.

## Open questions and decisions needed

- LLM provider and execution environment:
  - Decision owner or dedicated class: department data owner and implementation lead.
  - Evidence and decision rule: compare approved data handling, document limits, structured-output
    support, batch/resume capability, model quality on the calibration set, and actual cost.
- Document-context strategy:
  - Decision owner or dedicated class: evaluation implementer and quality lead.
  - Evidence and decision rule: compare full-document evaluation, page/section retrieval, and
    rubric-item batching using evidence accuracy, required-item agreement, latency, and cost.
- Adjudication strategy:
  - Decision owner or dedicated class: quality lead.
  - Evidence and decision rule: compare one-pass review, selective second pass, and independent
    dual evaluation only on findings where calibration shows material benefit.
- Department reporting audience:
  - Decision owner or dedicated class: Bob and department leadership.
  - Evidence and decision rule: define who receives aggregate results, course-level results, and
    instructor-identifiable review notes before designing workbook access and distribution.
- Non-blocking follow-up: decide whether corrected human findings should become future calibration
  examples after the first complete run.
