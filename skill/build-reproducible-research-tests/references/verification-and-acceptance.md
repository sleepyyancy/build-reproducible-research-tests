# Verification and acceptance

## Two statuses

Maintain two independent outcomes:

| Status | Question |
|---|---|
| Operational verification | Did the intended test run on the intended inputs, produce complete artifacts, and pass structural/semantic checks? |
| Scientific acceptance | Do the verified results satisfy the predeclared scientific criterion or expectation? |

Allowed scientific states are `PASS`, `FAIL`, and `NOT_DEFINED`. A negative scientific result is valid evidence when operational verification passes.

## Verification ladder

### Level 1: structural

- required files exist and are nonempty;
- schemas, headers, dimensions, keys, and data types match expectations;
- numerical outputs contain no unexpected non-finite values;
- every planned case has one unambiguous status;
- logs contain termination evidence.

### Level 2: identity and semantic alignment

- input and configuration fingerprints match the run record;
- units and coordinate/index/channel orders are explicit;
- joins and mappings are one-to-one or use a justified interpolation rule;
- duplicates, missing keys, and tolerance violations are rejected;
- group, specimen, material, or cohort labels are consistent.

### Level 3: numerical and scientific invariants

- independently recompute selected metrics from lower-level artifacts;
- check conservation, bounds, monotonicity, symmetry, dimensional consistency, or other applicable invariants;
- compare a small fixture or known reference result;
- test edge cases such as zero denominators, missing groups, and failed cases.

### Level 4: presentation and documentation

- tables, JSON/CSV, figures, and prose agree numerically;
- charts are inspected after rendering;
- README instructions match actual entry points and paths;
- report claims appear in the evidence ledger or cite an external source.

## Independent verification

Independence means the check does not merely reread a summary produced by the same code path. Suitable patterns include:

- recomputing a metric directly from raw or lower-level data with a small separate verifier;
- checking a projection against conservation or a known aggregate;
- comparing hashes before and after execution;
- validating a sample with a second implementation or hand calculation;
- checking table values against figure data rather than image labels.

The verifier may share file parsers when unavoidable, but should not share the exact aggregation or decision code being tested without an additional invariant.

## Thresholds

- Define thresholds before looking at the final result when the test is meant to pass or fail.
- State whether inequalities are strict or inclusive.
- Define aggregation, weighting, missing-case behavior, uncertainty, and multiple-comparison handling.
- If no threshold exists, use `NOT_DEFINED` and provide descriptive statistics. Do not infer quality labels from intuition.

## Verification record

Record:

- verifier identity/version;
- time and workspace fingerprint;
- checks executed, expected result, actual result, and status;
- excluded checks and rationale;
- operational status;
- scientific status and supporting criterion;
- unresolved warnings.

Warnings must remain visible until resolved or explicitly accepted. A passing summary must not hide a failed subcheck.
