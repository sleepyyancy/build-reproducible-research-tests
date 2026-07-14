# Scenario-specific evidence

Apply only the branch checks that affect the intended scientific claim.

## Computational simulation or learned-model inference

- Record source revision or code fingerprint, resolved settings, model/checkpoint identity, numerical precision, relevant runtime/library versions, random seeds, and hardware facts when they affect results.
- Validate mesh, grid, coordinate, index, channel, material, time-step, and boundary-condition semantics.
- Capture stdout/stderr or equivalent termination evidence.
- Treat completion, convergence, numerical validity, and physical validity as separate facts.
- For large arrays, prefer streaming reductions and compact scientific fields; retain raw fields only when irreplaceable or required for verification.

## Physical experiment

- Record apparatus, specimen/sample, calibration state, procedure version, ambient conditions, acquisition settings, operator-relevant facts, and timestamps.
- Distinguish independent repeats from repeated readings of one specimen.
- Preserve raw instrument output; apply corrections only in derived artifacts.
- Record exclusions, failed runs, missing measurements, and protocol deviations before outcome-dependent interpretation.
- Include instrument resolution and uncertainty propagation when they affect the claim.

## Observational or archival data analysis

- Record source, retrieval date/version, license or access restrictions, query/filter logic, cohort or sample selection, exclusions, missing-data policy, and transformations.
- Preserve the analyzed snapshot or an immutable source identifier and retrieval record.
- Check duplicated entities, leakage across train/test or time boundaries, selection effects, and unit/schema changes.
- Distinguish measured association from causal interpretation.

## Parameter sweep, sensitivity, or optimization study

- Make the parameter table an identified input with one case ID per planned run.
- Record the sampling design, fixed parameters, constraints, seeds, repetitions, failure policy, and stopping rule.
- Verify planned-versus-completed coverage and preserve failed parameter points.
- Distinguish execution failure from invalid physical or mathematical configuration.
- Limit conclusions to the sampled domain and resolution.

## Benchmark or method comparison

- Identify the reference hierarchy: ground truth, trusted solver/instrument, accepted dataset, or relative comparison only.
- Ensure methods receive equivalent information, subsets, preprocessing, and aggregation.
- Separate method error from mapping, interpolation, normalization, coarse-graining, and postprocessing error.
- Record resource cost only when efficiency is part of the comparison claim.
