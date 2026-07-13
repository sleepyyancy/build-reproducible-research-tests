---
name: build-reproducible-research-tests
description: Design, execute, verify, document, and package reproducible STEM research tests. Use when a task involves a scientific comparison, simulation or model validation, experiment, observational-data analysis, parameter sweep, regression study, or other multi-step technical test that needs an isolated workspace, explicit hypotheses and metrics, traceable inputs and outputs, persistent planning files, independent verification, and reusable artifacts. Also use when reviewing or standardizing an existing research-test workflow. Do not use for a one-off calculation or explanation that does not create or evaluate test artifacts.
---

# Build Reproducible Research Tests

## Purpose

Turn a research question into an auditable test package. Preserve the chain from evidence and decisions to inputs, execution records, numerical results, figures, conclusions, and reproduction instructions.

This skill is self-contained. Do not require planning-with-files, a plotting skill, or any other skill to apply its core workflow.

## Non-negotiable rules

1. Read the applicable project instructions before acting.
2. Base every scientific claim on inspected evidence. If a missing fact can change the design, metric, interpretation, or safety of the work, stop and ask the user. Do not silently invent it.
3. Never delete or overwrite important existing files without explicit approval. Treat source inputs as read-only.
4. Never install, remove, or upgrade packages or modify a conda/virtual environment without the user reviewing and approving that action.
5. Establish an isolated test workspace. Do not mix generated artifacts into source-data or production-code directories.
6. Keep `task_plan.md`, `findings.md`, and `progress.md` in every nontrivial test workspace. Update them during the work, not only at the end.
7. Preserve the scripts and configuration that generated results. A result without a generation path is incomplete.
8. Separate operational verification from scientific acceptance. A run can be technically valid while its scientific hypothesis fails.
9. Do not publish, commit, push, upload, or contact external systems unless the user explicitly authorizes that stage.

## Choose a workflow size

Use the smallest profile that preserves the scientific claim:

- **Compact:** one or two inputs, one analysis script, small outputs, no expensive solver. Keep the three planning files, test specification, README, final result, and verification record.
- **Standard:** multiple stages or cases, generated intermediate data, figures, or reusable results. Use the full directory structure and all workflow gates.
- **Extended:** expensive computation or physical experiments, large data, restarts, parallel jobs, regulated/sensitive inputs, or publication-bound results. Add environment capture, checksums, run manifests, checkpoint/resume validation, independent recalculation, and publishability audit.

Record the chosen profile and any omitted steps in `task_plan.md`. Omit a step only when its absence cannot weaken the intended claim.

## Standard workflow

### 1. Inspect and recover context

- Read project instructions, relevant plans, code, data headers, existing results, and prior logs.
- If a test workspace already exists, read its three planning files before continuing.
- Identify user-owned changes and preserve them.
- Record confirmed facts in `findings.md`; label unresolved items as `待确认` rather than guessing.

### 2. Write the test contract

Create or complete `test_spec.md` before expensive or state-changing execution. Specify:

- research question and falsifiable expectation;
- object under test and reference/baseline;
- controlled, independent, and measured variables;
- units, coordinate/index conventions, material or group semantics, and sign conventions;
- input identity and provenance;
- alignment, preprocessing, aggregation, and normalization rules;
- primary metrics and any thresholds;
- expected artifacts and result location;
- known limitations and decisions still required.

Use [references/workflow-and-gates.md](references/workflow-and-gates.md) for the contract and execution gates. Read [references/scenario-branches.md](references/scenario-branches.md) and apply only the relevant branch.

### 3. Resolve material uncertainty

Ask the user when an unknown could change what is compared, how data are aligned, which output is authoritative, whether a result is acceptable, or whether an external/state-changing action is permitted. Bundle related questions and explain their consequences.

Continue without asking only for reversible implementation details that are discoverable from the workspace and cannot change the scientific meaning. Record material assumptions explicitly and seek confirmation before execution.

### 4. Establish the isolated workspace

For new tests, use `scripts/init_test_workspace.py` after editing its top-level configuration. It creates the standard directories and copies templates without overwriting existing files.

Default responsibilities:

```text
test_workspace/
├── task_plan.md
├── findings.md
├── progress.md
├── test_spec.md
├── README.md
├── inputs/          # immutable copies, links, or input manifests
├── config/          # parameters and frozen run configuration
├── scripts/         # prepare, run, analyze, plot, verify
├── intermediate/    # reusable derived data and checkpoints
├── results/         # compact machine-readable final results
├── figures/         # previews and final exports
├── logs/            # stdout, stderr, solver and job logs
├── records/         # environment, manifests, run and verification records
└── report/          # reader-facing scientific writing, when requested
```

Number or date test directories only when required by the host project. Never assume a numbering convention without checking existing practice.

### 5. Build a traceable execution chain

Prefer separate stage scripts when preparation, execution, analysis, plotting, and verification have different failure modes. Use descriptive stage names such as `prepare_*`, `run_*`, `analyze_*`, `plot_*`, and `verify_*`.

At every stage:

- declare configuration in one visible place consistent with project style;
- validate inputs before computation;
- write outputs only inside the test workspace;
- capture the command or entry point, configuration, timestamps, status, and logs;
- fail loudly on missing columns, shape changes, non-finite values, duplicate identifiers, unit conflicts, or invalid mappings;
- make resume/reuse depend on a complete fingerprint of inputs, code, model/calibration, configuration, and relevant environment—not merely file existence;
- write atomic or checkpointed outputs when interruption would leave misleading partial files.

Read [references/provenance-and-artifacts.md](references/provenance-and-artifacts.md) before designing manifests, resume logic, or large-file retention.

### 6. Verify independently

Do not treat “script exited with code 0” as sufficient verification. Apply checks proportional to the claim:

- structural: expected files, schemas, row counts, keys, units, and finite values;
- identity: hashes or equivalent fingerprints for inputs and configurations;
- semantic: coordinate/index alignment, group mappings, conservation laws, invariants, and boundary conditions;
- numerical: independently recompute selected metrics from lower-level outputs;
- regression: compare against a known reference when one exists;
- visual: render previews and inspect labels, clipping, overlap, missing glyphs, misleading axes, and grayscale/color accessibility;
- documentation: confirm README commands, paths, artifact descriptions, and conclusions match the actual workspace.

Use `scripts/build_artifact_manifest.py`, `scripts/validate_test_workspace.py`, and `scripts/audit_publishability.py` after editing their top-level configuration. Read [references/verification-and-acceptance.md](references/verification-and-acceptance.md) for verification depth and PASS/FAIL semantics.

### 7. Interpret evidence

Report measured outcomes separately from interpretation. Preserve unexpected or negative results when the run is valid. State:

- whether execution verification passed;
- whether the scientific acceptance criterion passed, failed, or was not defined;
- which evidence supports each conclusion;
- which limitations are demonstrated by evidence;
- which questions remain unresolved.

Do not replace absent thresholds with an invented judgment. If no acceptance criterion was agreed, provide descriptive results only.

### 8. Document for two audiences

`README.md` is a technical reproduction guide. It may name files, scripts, commands, environment requirements, inputs, outputs, and known operational constraints.

A scientific report in `report/` addresses its stated readers. It must stand alone, explain necessary scientific context, and omit internal conversations, user instructions, edit history, absolute paths, script locations, and other backstage details.

Read [references/scientific-writing.md](references/scientific-writing.md) whenever the user asks for a report, paper section, analysis narrative, or other reader-facing prose.

### 9. Complete and hand off

Before declaring completion:

- regenerate final results from the retained scripts or document why a costly run was not repeated;
- run the workspace validator and record its output;
- run the publishability audit before any proposed Git/GitHub/package handoff;
- update all three planning files;
- summarize what was created, what was verified, the scientific outcome, and any remaining decisions;
- ask before updating project-level README or handoff documents if the project instructions require consent.

## Resource map

- [references/workflow-and-gates.md](references/workflow-and-gates.md): test contract, execution authorization, progress recording, and completion gate.
- [references/scenario-branches.md](references/scenario-branches.md): computational, experimental, observational, parameter-study, and visualization branches.
- [references/provenance-and-artifacts.md](references/provenance-and-artifacts.md): input identity, manifests, large files, intermediates, resume safety, and publishing boundaries.
- [references/verification-and-acceptance.md](references/verification-and-acceptance.md): independent checks, failure semantics, and acceptance records.
- [references/scientific-writing.md](references/scientific-writing.md): evidence-based Chinese and general scientific writing requirements.
- [references/example-adaptations.md](references/example-adaptations.md): hypothetical adaptations across research domains.
- `assets/workspace-template/`: templates copied into a new test workspace.
- `scripts/init_test_workspace.py`: creates a non-destructive workspace.
- `scripts/capture_environment.py`: records environment facts without modifying it.
- `scripts/build_artifact_manifest.py`: inventories artifacts and computes hashes.
- `scripts/validate_test_workspace.py`: checks structure, records, placeholders, and artifact consistency.
- `scripts/audit_publishability.py`: reports caches, large files, absolute paths, likely secrets, and unsuitable publishable artifacts without deleting anything.
