# Evidence Ledger: Parameter-Trend Evidence Package

## Evidence

| Evidence ID | Fact or measured result | Source artifact | Verification method | Status |
|---|---|---|---|---|
| E001 | Four unique finite parameter-response rows are present. | `inputs/measurements.csv` | Schema, uniqueness, count, and finite-value checks | Verified |
| E002 | The minimum adjacent response difference is 1.3. | `results/trend_summary.csv` | Independent indexed-pair recomputation | Verified |
| E003 | Every adjacent response difference is positive. | `records/verification_report.md` | Independent recomputation and strict inequality check | Verified |

## Claims

| Claim ID | Scientific claim | Supporting evidence | Claim type | Status |
|---|---|---|---|---|
| C001 | The response is strictly increasing over the four sampled parameter values. | E001,E002,E003 | Derived | Supported |

## Limits

- The evidence does not establish behavior outside the sampled interval or between sampled values.
