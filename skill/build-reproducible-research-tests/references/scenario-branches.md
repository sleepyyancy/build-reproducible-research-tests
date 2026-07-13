# Scenario branches

Apply the shared workflow in SKILL.md, then add only the relevant branch checks. A test may combine branches.

## Computational simulation or learned-model inference

- Record source revision or code hashes, configuration, model/checkpoint identity, hardware-relevant facts, numerical precision, library/runtime versions, and random seeds.
- Validate mesh, grid, coordinate, index, channel, material, time-step, and boundary-condition semantics.
- Estimate runtime, memory, accelerator, and disk use before large runs.
- Capture stdout/stderr and solver termination status.
- Treat convergence, completion, and physical validity as separate checks.
- When resuming, compare a full fingerprint of inputs, code, configuration, model, and relevant environment.
- For large arrays, prefer streaming reductions and compact derived fields. Retain raw fields only when they are irreplaceable or needed for the claim.

## Physical experiment

- Record apparatus identity, specimen/sample identity, calibration state, operator-relevant procedure version, ambient conditions, acquisition settings, and timestamps.
- Define independent repeats separately from repeated readings of one specimen.
- Preserve raw instrument output unchanged; perform corrections in a derived-data stage.
- Record exclusions, failed runs, missing measurements, and protocol deviations before inspecting outcome-dependent conclusions.
- Include uncertainty propagation and instrument resolution where they affect the claim.
- Never infer an unrecorded experimental condition from a typical value.

## Observational or archival data analysis

- Record source, retrieval date/version, license or access restrictions, query/filter logic, cohort/sample selection, missing-data handling, exclusions, and transformations.
- Distinguish observed associations from causal claims.
- Check duplicated entities, leakage across train/test or time boundaries, selection bias, and unit/schema changes.
- Preserve the raw snapshot or an immutable source identifier and retrieval manifest.
- If the source can change, cache or fingerprint the exact analyzed version when permitted.

## Parameter sweep, sensitivity, or optimization study

- Define the parameter space, sampling design, fixed parameters, constraints, seeds, failure policy, and stopping rule before execution.
- Keep the parameter table as a first-class input and attach a unique case identifier to every artifact.
- Test whether all intended combinations ran exactly once unless repetitions are designed.
- Preserve failed parameter points and distinguish numerical failure from physically invalid configuration.
- Avoid interpreting an optimum beyond the sampled domain or resolution.

## Benchmark or method comparison

- Ensure the compared methods receive equivalent information and compatible preprocessing.
- Separate method error from mapping, interpolation, normalization, or postprocessing error.
- Identify the reference hierarchy: ground truth, trusted solver/instrument, accepted dataset, or relative comparison only.
- Use identical subsets and aggregation rules across methods.
- Report resource cost when the comparison claim includes efficiency.

## Visualization branch

Use when figures are part of evidence, not merely decoration.

- Profile data types, sample sizes, missing values, distributions, outliers, groups, and correlations before choosing a chart.
- Choose the chart to match the claim. Do not hide small-sample distributions behind mean-only bars, connect unordered categories, use dual axes without necessity, use rainbow maps, or truncate axes misleadingly.
- Use colorblind-safe encoding and redundancy such as markers, line styles, labels, or direct annotation.
- Generate a preview, run programmatic checks where possible, inspect the rendered image, correct issues, and rerender.
- Verify text clipping, overlap, glyphs, tick density, units, legend mapping, panel alignment, and grayscale readability.
- Derive plotted values from the same machine-readable tables used by the report; do not manually retype result numbers.
