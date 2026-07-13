# Workflow and gates

## Test contract

The contract closes the gap between a broad research request and an executable test. It should answer:

| Topic | Required content |
|---|---|
| Question | One research question that the outputs can answer |
| Expectation | Directional trend, equivalence, difference, bound, or null expectation |
| Objects | Object under test, reference, baseline, and excluded objects |
| Variables | Controlled, independent, measured, nuisance, and derived variables |
| Semantics | Units, coordinate/index order, grouping, sign, normalization, time/state |
| Data | Authoritative source, immutable identity, allowed preprocessing |
| Metrics | Formula/definition, aggregation, weighting, edge cases, thresholds |
| Cases | Case list, repetitions, random seeds, and sampling rule |
| Outputs | Tables, figures, logs, intermediate fields, report, manifest |
| Limits | Known omissions and claims the test cannot support |

Use explicit labels for `Confirmed`, `Proposed`, and `Needs confirmation`. Move a proposed item to confirmed only after evidence or user approval.

## Gates

### Design gate

Pass when the research question, comparison objects, data meaning, primary metric, and expected output are unambiguous. Read-only inspection and planning may proceed before this gate. Expensive runs and irreversible/state-changing actions may not.

### Input gate

Pass when all required inputs exist, schemas and units are validated, authoritative versions are identified, and input fingerprints are recorded. A filename alone is not an identity check.

### Execution gate

Pass when the user has authorized execution or the request already clearly contains that authorization, the environment is known, expected resource use is acceptable, output paths are isolated, and restart behavior is defined.

### Analysis gate

Pass when executions are complete, partial files are excluded, alignment and preprocessing checks pass, and the metric implementation has a reference calculation or test.

### Evidence gate

Pass when final numbers can be traced to retained inputs and scripts, selected results have been recomputed independently, plots agree with machine-readable tables, and operational status is separated from scientific status.

### Release gate

Pass when the user authorizes release, publishability audit findings are resolved or accepted, licenses and sensitive-data constraints are known, and the package contains no secret, cache, absolute-path dependency, or unexplained orphan artifact.

## Persistent records

### task_plan.md

Record goal, scope, phases, current status, decisions, completion criteria, and errors. Keep at most one phase in progress. Mark a phase complete only after its outputs are checked.

### findings.md

Record inspected evidence, data semantics, interfaces, validated mappings, scientific observations, decisions and unresolved questions. Distinguish evidence from interpretation.

### progress.md

Record dated actions, files created or changed, commands or entry points, run status, test results, failures and resolutions. Preserve failed attempts when they explain the final method.

Update the records immediately after a material discovery, decision, failed command, completed phase, or verification result. Their purpose is recovery and audit, not retrospective decoration.

## Handling uncertainty

Stop and ask when uncertainty concerns:

- which dataset, iteration, state, reference, or model is authoritative;
- units, coordinate order, index order, group/material meaning, or sign convention;
- matching, interpolation, normalization, weighting, relaxation, or aggregation;
- acceptance thresholds or whether a claim should be pass/fail;
- permission to delete, overwrite, modify an environment, publish, or contact an external system.

Proceed with a recorded implementation choice when it is reversible, locally inspectable, scientifically neutral, and within authorized scope. Examples include internal helper names or a temporary cache location under the test workspace.

## Error protocol

When a command or stage fails:

1. Preserve the error and partial-state description in `progress.md`.
2. Check whether any output is incomplete or misleading; quarantine by marking it incomplete, not by silently deleting it.
3. Identify the cause using evidence.
4. Change one relevant factor at a time when practical.
5. Re-run the smallest check that proves the issue resolved.
6. Record the resolution and whether prior outputs remain valid.
