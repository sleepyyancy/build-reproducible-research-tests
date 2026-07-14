# Test Specification: Parameter-Trend Evidence Package

## Research question and scope

- Research question: Is the measured response strictly increasing over the sampled parameter values?
- Testable expectation: Every adjacent response difference is greater than zero after sorting by parameter value.
- Included claim: Strict monotonic increase over the four sampled values.
- Excluded claim: Behavior outside the sampled interval or between sampled values.

## Variables and semantics

| Class | Variable | Values | Units |
|---|---|---|---|
| Independent | Parameter value | 1.0, 2.0, 3.0, 4.0 | arbitrary unit |
| Measured | Response value | Recorded in the input table | arbitrary unit |
| Derived | Adjacent response difference | Computed after sorting | arbitrary unit |

- Row identity: unique `case_id`.
- Ordering: ascending `parameter_value`.
- Invalid data: duplicate identifiers, duplicate parameter values, non-finite values, or fewer than two rows fail operational verification.

## Input identity

`inputs/measurements.csv` is an immutable fixture distributed with this repository. Its SHA-256 is recorded in `records/run_record.json` and `records/artifact_manifest.json`.

## Metric and scientific acceptance

For ordered responses, define

\[
\Delta y_k = y_{k+1}-y_k.
\]

其中，\(y_k\)为第\(k\)个有序参数位置的响应值，\(\Delta y_k\)为相邻响应差。

Scientific acceptance is `PASS` only when every\(\Delta y_k>0\); otherwise it is `FAIL`.

## Required artifacts

- Machine-readable result: `results/trend_summary.csv`.
- Run identity: `records/run_record.json`.
- Independent recomputation: indexed adjacent-pair calculation compared with the analysis result.
- Verification: `records/verification_report.md` and `records/workspace_validation.json`.
- Evidence-to-claim mapping: `evidence_ledger.md`.
