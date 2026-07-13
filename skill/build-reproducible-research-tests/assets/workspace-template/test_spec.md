# Test Specification: {{TEST_TITLE}}

## Research question
{{ONE_ANSWERABLE_QUESTION}}

## Testable expectation
{{DIRECTION_EQUIVALENCE_BOUND_OR_NULL_EXPECTATION}}

## Test objects
| Role | Object | Version/state | Identity evidence |
|---|---|---|---|
| Object under test | {{OBJECT}} | {{VERSION}} | {{HASH_ID_OR_RECORD}} |
| Reference/baseline | {{REFERENCE}} | {{VERSION}} | {{HASH_ID_OR_RECORD}} |

## Variables
| Class | Variable | Values/range | Units | Control or measurement method |
|---|---|---|---|---|
| Independent | {{VARIABLE}} | {{VALUES}} | {{UNITS}} | {{METHOD}} |
| Controlled | {{VARIABLE}} | {{VALUE}} | {{UNITS}} | {{METHOD}} |
| Measured | {{VARIABLE}} | {{EXPECTED_SCHEMA}} | {{UNITS}} | {{METHOD}} |
| Derived | {{METRIC}} | {{DEFINITION}} | {{UNITS}} | {{METHOD}} |

## Data semantics
- Coordinate/index/channel order: {{ORDER}}
- Group, specimen, material, or cohort meaning: {{SEMANTICS}}
- Sign and normalization conventions: {{CONVENTIONS}}
- Time/state/iteration represented: {{STATE}}
- Missing and invalid data policy: {{POLICY}}

## Inputs and provenance
| Input ID | Source identity | Local representation | Required schema | Fingerprint status |
|---|---|---|---|---|
| {{INPUT_ID}} | {{SOURCE}} | {{RELATIVE_PATH_OR_REFERENCE}} | {{SCHEMA}} | {{Pending|Recorded}} |

## Cases and sampling
- Case list or sampling design: {{DESIGN}}
- Repetitions and independence: {{REPETITIONS}}
- Random seeds: {{SEEDS_OR_NOT_APPLICABLE}}
- Exclusion and failure policy: {{POLICY}}

## Processing and alignment
- Preprocessing: {{STEPS}}
- Alignment/mapping/interpolation: {{RULE}}
- Aggregation/weighting: {{RULE}}
- Validation of transformations: {{CHECK}}

## Metrics and acceptance
| Metric | Exact definition | Aggregation/weighting | Edge cases | Acceptance criterion |
|---|---|---|---|---|
| {{METRIC}} | {{FORMULA_OR_PRECISE_DEFINITION}} | {{RULE}} | {{POLICY}} | {{THRESHOLD_OR_NOT_DEFINED}} |

## Expected artifacts
- Machine-readable results: {{FILES}}
- Intermediate data: {{FILES_AND_RETENTION}}
- Figures: {{FILES_OR_NOT_APPLICABLE}}
- Logs and records: {{FILES}}
- Reader-facing report: {{YES_NO_AND_AUDIENCE}}

## Resource and execution plan
- Environment: {{EXISTING_APPROVED_ENVIRONMENT}}
- Compute/instrument requirements: {{REQUIREMENTS}}
- Estimated runtime and storage: {{ESTIMATE}}
- Resume/checkpoint rule: {{FULL_FINGERPRINT_RULE}}

## Limitations and excluded claims
- {{LIMITATION}}

## Decisions required before execution
- {{QUESTION_OR_NONE}}

## Authorization gate
- Design approved by: {{USER_OR_AUTHORITY}}
- Execution authorized: {{YES_NO_DATE}}
- Environment modification authorized: No, unless separately recorded
- External publication authorized: No, unless separately recorded
