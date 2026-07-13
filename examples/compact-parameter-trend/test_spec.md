# Test Specification: Compact Parameter-Trend Example

## Research question
Is the measured response strictly increasing over the sampled parameter values?

## Testable expectation
Every adjacent response difference is greater than zero after sorting by parameter value.

## Variables
| Class | Variable | Values | Units |
|---|---|---|---|
| Independent | Parameter value | 1.0, 2.0, 3.0, 4.0 | arbitrary unit |
| Measured | Response value | Recorded in the input table | arbitrary unit |
| Derived | Adjacent response difference | Computed after sorting | arbitrary unit |

## Inputs and provenance
The example input is a small immutable fixture distributed with the repository. Each row has a unique case identifier.

## Processing and acceptance
- Parse the declared columns.
- Reject duplicate identifiers, non-finite values, duplicate parameter values, or fewer than two rows.
- Sort rows by parameter value.
- Compute every adjacent response difference.
- Scientific acceptance is PASS only when every difference is strictly positive.

## Authorization gate
- The example is self-contained and writes only its two declared generated outputs.
- It performs no deletion, package installation, environment modification, or external action.
