# Parameter-Trend Evidence Package

[English](README.md) | [简体中文](README.zh-CN.md)

This worked example tests whether a measured response is strictly increasing over four ordered parameter values.

## Status

- Operational verification: PASS
- Scientific acceptance: PASS
- Acceptance criterion: every adjacent response difference must be greater than zero

## Evidence package

| Location | Responsibility |
|---|---|
| `inputs/measurements.csv` | Immutable four-case input fixture |
| `test_spec.md` | Question, data semantics, metric, and acceptance criterion |
| `scripts/analyze_and_verify.py` | Analysis, independent recomputation, and run-record generation |
| `results/trend_summary.csv` | Machine-readable final metrics |
| `evidence_ledger.md` | Verified evidence linked to the scientific claim |
| `records/` | Workspace contract, run record, artifact manifest, and verification records |

## Reproduce

Run from this directory:

```bash
python scripts/analyze_and_verify.py
python ../../skill/build-reproducible-research-tests/scripts/build_artifact_manifest.py
python ../../skill/build-reproducible-research-tests/scripts/validate_test_workspace.py
```

The first script may replace only its declared generated outputs: `results/trend_summary.csv`, `records/run_record.json`, and `records/verification_report.md`. It never modifies the input, specification, or evidence ledger.
