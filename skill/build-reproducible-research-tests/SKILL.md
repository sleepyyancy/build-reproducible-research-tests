---
name: build-reproducible-research-tests
description: Build and audit evidence chains for multi-stage STEM tests that create reusable artifacts. Use when designing, executing, repairing, or packaging a scientific comparison, simulation or model validation, physical experiment, observational-data study, parameter sweep, sensitivity study, or benchmark whose claims must trace to identified inputs, frozen settings, run records, machine-readable results, independent verification, and reproduction instructions. Do not use for conceptual explanations, read-only result summaries, one-off calculations, ordinary code changes, or plotting-only requests that do not create or standardize a research-test package.
---

# Build Reproducible Research Tests

## Purpose

Turn a scientific test into an auditable evidence package. Preserve this chain:

```text
source identity → test specification → frozen settings → execution record
→ derived artifacts → machine-readable result → independent verification
→ evidence ledger → scientific claim
```

Use only the controls needed to support the intended claim. Add structure when it protects provenance, interpretation, reruns, or release safety; do not create empty directories or documents for appearance.

## Required evidence

Every completed test package must provide:

- a precise research question, comparison scope, data semantics, metrics, and acceptance status;
- authoritative input identity and the settings that affect results;
- retained scripts or an exact external procedure that regenerates derived results;
- machine-readable results separated from reader-facing interpretation;
- an execution record sufficient to identify completed, failed, reused, and partial artifacts;
- verification that does more than reread the final summary;
- an evidence ledger connecting each substantive conclusion to checked evidence;
- reproduction instructions that match the actual package.

Treat original inputs as read-only. Do not silently delete, overwrite, install dependencies, alter environments, or publish artifacts. Obtain explicit authorization when an action changes those states.

## Build the evidence chain

### 1. Define the test contract

Complete `test_spec.md` before expensive execution. Fix the object under test, reference or baseline, authoritative state or iteration, controlled and measured variables, units, ordering conventions, preprocessing, alignment, aggregation, metrics, edge cases, cases or sampling, thresholds, and excluded claims.

Ask the user when a missing fact can change scientific meaning or acceptance. Mark absent thresholds as `NOT_DEFINED`; do not invent a quality judgment.

Read [references/workflow-and-gates.md](references/workflow-and-gates.md) for the contract and evidence gates. Apply only the relevant checks from [references/scenario-branches.md](references/scenario-branches.md).

### 2. Establish artifact responsibilities

Keep the test package isolated from source data and production code. Use project naming conventions when they exist.

The minimum package is:

```text
test_workspace/
├── README.md
├── test_spec.md
├── evidence_ledger.md
├── scripts/       # generation and verification entry points
├── results/       # compact machine-readable final results
└── records/       # contract, run, manifest, and verification records
```

Add `inputs/`, `config/`, `intermediate/`, `figures/`, `logs/`, or `report/` only when the test needs those responsibilities. Existing projects may use different names; preserve clear boundaries and record the mapping in README.

For a new package, edit the top-level configuration in `scripts/init_test_workspace.py` and run it. The initializer creates only declared components, refuses to overwrite an existing workspace, and writes `records/workspace_contract.json` for later validation.

### 3. Preserve identity and provenance

Identify each source by content hash, immutable version, retrieval record, specimen/instrument identity, or another domain-appropriate fingerprint. Freeze every result-affecting setting, including defaults. Record code, model, geometry, calibration, random seed, precision, and relevant environment when they can change the result.

Resume or reuse an artifact only when its complete result-affecting fingerprint matches and completeness is verified. File existence, timestamp, or row count alone is insufficient.

Read [references/provenance-and-artifacts.md](references/provenance-and-artifacts.md) when designing fingerprints, manifests, retention, large-data handling, or release classes.

### 4. Generate traceable artifacts

Separate stages when they have different inputs, costs, failure modes, or rerun needs. Each executed stage must record its entry point or procedure, resolved settings, input identity, start and finish time, status, log or termination evidence, and outputs.

Reject missing fields, incompatible units, duplicate identifiers, invalid mappings, unexpected shapes, non-finite values, and incomplete cases before they enter final results. Mark partial outputs explicitly so they cannot be mistaken for completed evidence.

Derive tables, figures, and prose from retained machine-readable results. When figures support a claim, verify their source data, labels, units, direction, and rendered readability; keep chart-design choices outside the evidence record unless they affect interpretation.

### 5. Verify independently

Match verification depth to claim risk and regeneration cost. Cover the applicable layers:

- structural: artifacts, schemas, dimensions, keys, finite values, case coverage, and termination evidence;
- identity: inputs, settings, code/model/instrument state, and reused-output fingerprints;
- semantic: units, coordinate/index/channel order, mapping, normalization, groups, and boundary conditions;
- numerical: recompute selected metrics from lower-level artifacts or check an independent invariant;
- consistency: machine-readable results, figures, README, and scientific prose agree.

Report two separate outcomes:

- `Operational verification`: whether the intended test ran on the intended evidence and produced valid artifacts;
- `Scientific acceptance`: `PASS`, `FAIL`, or `NOT_DEFINED` against the declared criterion.

Read [references/verification-and-acceptance.md](references/verification-and-acceptance.md) before designing the verifier or interpreting failure states.

### 6. Connect evidence to claims

Use `evidence_ledger.md` to assign evidence IDs, record how each item was checked, and list the claims it supports. Keep measured values, derived results, interpretation, recommendations, and unresolved questions distinguishable.

Preserve verified negative and null results. State only limitations demonstrated by evidence. If the user requests a report or paper section, read [references/scientific-writing.md](references/scientific-writing.md).

### 7. Package and validate

README must state the test scope, statuses, required environment or apparatus, real reproduction sequence, input identity, output meanings, verification method, and known constraints.

Edit the top-level configuration before using the bundled utilities:

- `scripts/build_artifact_manifest.py`: inventory artifacts and compute streaming hashes;
- `scripts/capture_environment.py`: record reproducibility-relevant environment facts without changing them;
- `scripts/validate_test_workspace.py`: validate declared package contents and recorded artifact identity;
- `scripts/audit_publishability.py`: report caches, large files, absolute paths, and likely sensitive content without deleting anything.

Run the package validator after final artifacts are generated. Run the publication audit only when release is proposed, and publish only after explicit authorization.

## Evidence controls by risk

Always keep the minimum package and an independent verification record. Add the following only when relevant:

- checksums and artifact manifests for external, mutable, reused, or release-bound inputs and outputs;
- environment capture for software-sensitive or hardware-sensitive computation;
- logs and termination records for solvers, instruments, batch jobs, or expensive inference;
- checkpoints and full resume fingerprints for interruptible work;
- retained intermediates when regeneration is expensive or transformation error must be isolated;
- independent repeats, calibration and uncertainty records for physical measurements;
- release classification and publishability audit for shared packages.

Record omitted high-risk controls and why their absence does not weaken the intended claim.

## Resource map

- [references/workflow-and-gates.md](references/workflow-and-gates.md): test contract and evidence gates.
- [references/scenario-branches.md](references/scenario-branches.md): domain-specific provenance and verification checks.
- [references/provenance-and-artifacts.md](references/provenance-and-artifacts.md): identity, manifests, reuse, retention, large data, and release classes.
- [references/verification-and-acceptance.md](references/verification-and-acceptance.md): verification depth, independence, thresholds, and outcome states.
- [references/scientific-writing.md](references/scientific-writing.md): evidence-based scientific writing and Chinese-language requirements.
- [references/example-adaptations.md](references/example-adaptations.md): hypothetical adaptations across research domains.
- [references/quickstart-zh-CN.md](references/quickstart-zh-CN.md): concise Chinese usage guide.
- `assets/workspace-template/`: minimal evidence-package templates.
- `scripts/`: non-destructive initialization, provenance, validation, environment, and release-audit utilities.
