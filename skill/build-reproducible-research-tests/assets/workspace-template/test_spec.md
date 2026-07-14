# Test Specification: {{TEST_TITLE}}

## Research question and scope

- Research question: {{ONE_ANSWERABLE_QUESTION}}
- Testable expectation: {{DIRECTION_EQUIVALENCE_BOUND_OR_NULL_EXPECTATION}}
- Included claim: {{CLAIM_THE_ARTIFACTS_CAN_SUPPORT}}
- Excluded claim: {{CLAIM_OUTSIDE_THE_TEST}}

## Test objects

| Role | Object | Version/state | Identity evidence |
|---|---|---|---|
| Object under test | {{OBJECT}} | {{VERSION_OR_STATE}} | {{HASH_ID_OR_RECORD}} |
| Reference/baseline | {{REFERENCE}} | {{VERSION_OR_STATE}} | {{HASH_ID_OR_RECORD}} |

## Variables and semantics

| Class | Variable | Values/range | Units | Control or measurement method |
|---|---|---|---|---|
| Independent | {{VARIABLE}} | {{VALUES}} | {{UNITS}} | {{METHOD}} |
| Controlled | {{VARIABLE}} | {{VALUE}} | {{UNITS}} | {{METHOD}} |
| Measured | {{VARIABLE}} | {{EXPECTED_SCHEMA}} | {{UNITS}} | {{METHOD}} |
| Derived | {{METRIC}} | {{DEFINITION}} | {{UNITS}} | {{METHOD}} |

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
- Transformation validation: {{CHECK}}

## Metrics and scientific acceptance

| Metric | Exact definition | Aggregation/weighting | Edge cases | Acceptance criterion |
|---|---|---|---|---|
| {{METRIC}} | {{FORMULA_OR_PRECISE_DEFINITION}} | {{RULE}} | {{POLICY}} | {{THRESHOLD_OR_NOT_DEFINED}} |

## Required evidence and artifacts

- Machine-readable results: {{FILES}}
- Independent verification: {{METHOD_AND_RECORD}}
- Run and identity records: {{FILES}}
- Optional intermediates and retention: {{FILES_POLICY_OR_NOT_APPLICABLE}}
- Optional figures or report: {{FILES_OR_NOT_APPLICABLE}}
- Test-specific required paths added to `records/workspace_contract.json`: {{YES_NO}}

## Reproduction constraints

- Approved environment or apparatus: {{EXISTING_APPROVED_ENVIRONMENT_OR_APPARATUS}}
- Compute, instrument, software, and data requirements: {{REQUIREMENTS}}
- Estimated runtime and storage: {{ESTIMATE}}
- Resume/reuse rule: {{FULL_FINGERPRINT_RULE_OR_NOT_APPLICABLE}}

## Decisions required before result-producing execution

- {{QUESTION_OR_NONE}}
