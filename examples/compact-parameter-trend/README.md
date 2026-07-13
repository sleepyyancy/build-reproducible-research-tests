# Compact Parameter-Trend Example

This worked example tests whether a measured response is strictly increasing over four ordered parameter values.

## Reproduce

Run from this directory:

```bash
python scripts/analyze_and_verify.py
```

The script validates the input schema, uniqueness, finite values, and parameter ordering. It then regenerates:

- `results/trend_summary.csv`
- `records/verification_report.md`

Both files are declared generated artifacts and may be replaced by this script. The input file and planning documents are never modified.

## Status

- Operational verification: PASS
- Scientific acceptance: PASS
- Acceptance criterion: every adjacent response difference must be greater than zero
