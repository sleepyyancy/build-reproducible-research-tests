# Test contract and evidence gates

## Test contract

Record the following before result-producing execution:

| Topic | Required content |
|---|---|
| Question | One answerable scientific question |
| Expectation | Direction, equivalence, difference, bound, or null expectation |
| Objects | Object under test, reference, baseline, and excluded objects |
| Variables | Controlled, independent, measured, nuisance, and derived variables |
| Semantics | Units, coordinate/index order, grouping, sign, normalization, time/state |
| Inputs | Authoritative source, immutable identity, and allowed preprocessing |
| Metrics | Exact definition, weighting, edge cases, uncertainty, and thresholds |
| Cases | Case list, repetitions, random seeds, sampling, exclusions, and failure policy |
| Artifacts | Required inputs, settings, scripts, results, records, figures, and reports |
| Limits | Claims the test cannot support |

Use `Confirmed`, `Proposed`, and `Needs confirmation` where the status matters. Do not promote a proposed item without inspected evidence or user approval.

## Evidence gates

### Meaning gate

Pass when the question, comparison objects, authoritative state, data semantics, transformation rules, primary metric, and intended claim are unambiguous.

### Identity gate

Pass when required inputs exist, schemas and units are validated, source identity is recorded, and result-affecting settings can be reconstructed. A filename alone is not identity evidence.

### Execution-evidence gate

Pass when the run record identifies the actual inputs, settings, procedure, time, status, termination evidence, and outputs. Existing artifacts may be reused only when their complete fingerprint and completeness match.

### Result-evidence gate

Pass when partial or invalid outputs are excluded, alignments and transformations are verified, machine-readable results are complete, and selected values or invariants have an independent check.

### Claim gate

Pass when each substantive conclusion points to verified evidence, operational and scientific outcomes are separate, absent thresholds remain `NOT_DEFINED`, and limitations do not exceed the evidence.

### Release-evidence gate

Pass when release is authorized, licenses and sensitive-data constraints are known, required artifacts have publication classes, and the package contains no unresolved secret, cache, absolute-path dependency, or unexplained orphan artifact.

## Material uncertainty

Obtain clarification before execution when uncertainty concerns the authoritative dataset, iteration, state, reference, model, units, ordering, mapping, interpolation, normalization, weighting, relaxation, aggregation, acceptance threshold, or permission for an external or state-changing action.

Record scientifically neutral implementation choices only when they are reversible, locally inspectable, and cannot alter the intended conclusion.
