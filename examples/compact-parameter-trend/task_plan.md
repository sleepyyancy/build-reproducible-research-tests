# Task Plan: Compact Parameter-Trend Example

## Goal
Determine whether the measured response is strictly increasing across the sampled parameter values.

## Profile
- Selected profile: Compact
- Tailoring decisions: No external solver, figure, or environment modification is required.

## Phases
- [x] Define the test contract and immutable input
- [x] Implement the analysis and verification script
- [x] Generate the result and verification record
- [x] Confirm the acceptance criterion

## Completion criteria
- All input rows pass schema, uniqueness, ordering, and finite-value checks.
- Every adjacent response difference is positive.
- Machine-readable and human-readable results agree.
