# Provenance and artifact management

## Traceability model

Every final claim should trace through this chain:

```text
source identity → immutable input → frozen configuration → execution record
→ intermediate transformation → analysis result → figure/table → verification → claim
```

Record the link explicitly with manifests, case identifiers, relative paths, hashes, configuration snapshots, and generation scripts. Relative paths keep the workspace relocatable.

## Input policy

- Do not edit original inputs in place.
- Use one of three patterns: immutable copy, read-only link/reference plus checksum, or retrieval manifest for externally stored data.
- Record source URI/path only in technical records, not reader-facing scientific prose.
- Capture schema, units, ordering, row/shape counts, and semantic version where applicable.
- A copied input without source identity is not full provenance.

## Configuration policy

- Keep run-defining values in one visible configuration surface.
- Freeze the resolved configuration used for each run.
- Include defaults that affect results, not only values manually changed.
- Do not rely on undocumented shell state or working-directory assumptions.
- Record secrets by name/source, never by value.

## Manifest fields

A useful artifact entry includes:

- relative path;
- artifact role and producing stage;
- size and modification time;
- content hash when feasible;
- source/derived/final classification;
- generating script or external process;
- case identifier and configuration fingerprint;
- retention and publication class.

The provided manifest script supplies file-level inventory and hashes. Add domain-specific stage, case, and semantic fields in the test's own run records.

Self-referential audit outputs—the artifact manifest itself, workspace validation output, and publishability audit output—are excluded from the file manifest so rerunning a checker does not invalidate the manifest it checks. Their generation time and status remain in their own records.

## Resume and cache safety

Reuse an existing output only when all result-affecting fingerprints match:

- every authoritative input;
- source code or executable version;
- model, calibration, geometry, or instrument state;
- resolved configuration and random seed;
- relevant runtime environment;
- expected schema and completeness marker.

Line counts and timestamps alone are insufficient. If complete identity cannot be established, rerun or mark the artifact as unverified reuse.

## Intermediate-data retention

Retain an intermediate when it is expensive to regenerate, needed for independent verification, required to isolate transformation error, or necessary to resume safely. Do not retain it merely because it was generated.

For each large intermediate, choose and record one policy:

- retain in the local workspace;
- retain externally with immutable identity;
- regenerate from retained lower-level inputs and scripts;
- discard after user approval because it has no reproducibility value.

Never delete automatically as a cleanup step.

## Large data

- Estimate storage before execution.
- Stream or chunk calculations when full materialization is unnecessary.
- Prefer compact sufficient statistics or scientifically meaningful reduced fields over duplicate raw copies.
- Keep checksums and source references for raw data stored elsewhere.
- Distinguish local reproducibility from repository portability. A Git repository should usually contain scripts, small fixtures, schemas, manifests, and compact results—not multi-gigabyte generated fields.

## Publication classes

Classify artifacts before release:

- `publish`: required and safe to distribute;
- `local-only`: required for local reproduction but too large, licensed, or sensitive;
- `regenerate`: omit from release because scripts recreate it;
- `exclude`: cache, temporary, secret, unrelated, invalid, or superseded artifact.

The publishability audit only reports risks. Resolve them through explicit decisions; do not let an automated tool delete or rewrite user data.
