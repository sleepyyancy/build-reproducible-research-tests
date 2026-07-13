# Example adaptations

These are hypothetical examples that demonstrate how to adapt the shared workflow. They are not evidence about any real project.

## Numerical solver comparison

Research question: under the same geometry, material properties, boundary conditions, mesh locations, and source field, how closely does a reduced-order model reproduce a trusted solver?

The test contract fixes the authoritative iteration/state, units, coordinate order, source normalization, mapping rule, and primary error metrics. Preparation validates that both coordinate sets can be aligned. Execution records solver/model versions and configuration fingerprints. Analysis separates native-field error from interpolation or coarse-graining error. Verification independently recomputes selected aggregates and checks conservation or boundary invariants. Operational verification and metric-based scientific acceptance are reported separately.

## Laboratory sensor calibration

Research question: does a sensor satisfy a predeclared accuracy bound over the intended measurement range?

The workspace preserves raw instrument exports, calibration-standard identity, ambient conditions, acquisition settings, specimen or sensor serial identity, and independent repeats. Corrections are applied only in derived data. The test specification defines the error formula, uncertainty treatment, inclusion rule, and acceptance bound before final measurements are analyzed. Verification checks raw-record immutability, calibration validity, units, repeated-measure structure, and an independent calculation for selected points.

## Observational dataset study

Research question: is a measured association stable under predeclared cohort filters and sensitivity analyses?

The input record identifies the dataset version, retrieval time, query, licensing constraints, cohort selection, exclusions, missing-data policy, and transformations. Case identifiers prevent entities from crossing train/test or temporal boundaries. The analysis reports association without adding a causal claim. Verification reproduces cohort counts, duplicate checks, missingness summaries, model inputs, and selected statistics from the frozen data snapshot.

## Parameter sweep

Research question: does the measured response follow an expected trend within a defined parameter interval?

The parameter table is an immutable input with one case identifier per row. The contract defines fixed variables, sampling resolution, repetitions, seeds, invalid-case handling, and trend criterion. Run records retain failed cases rather than silently omitting them. Verification checks planned-versus-completed case coverage and recomputes the trend statistic. Interpretation is limited to the sampled interval and resolution.
