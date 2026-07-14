# Build Reproducible Research Tests

[English](README.md) | [简体中文](README.zh-CN.md)

> 中文简介：这是一个面向理工科科研测试的独立Codex Skill，用于把权威输入、实际设置、运行记录、机器可读结果、独立验证和科学结论组织成可审计证据链。完整中文说明见[README.zh-CN.md](README.zh-CN.md)。

A self-contained Codex Skill for building and auditing evidence chains around multi-stage STEM research tests.

It is designed for scientific comparisons, simulation and model validation, physical experiments, observational-data studies, parameter sweeps, sensitivity studies, and benchmarks that produce reusable artifacts. It does not turn ordinary explanations, one-off calculations, code edits, or plotting-only requests into heavyweight test packages.

## What it builds

```text
source identity → test specification → frozen settings → execution record
→ derived artifacts → machine-readable result → independent verification
→ evidence ledger → scientific claim
```

Core capabilities:

- Defines the scientific question, authoritative state, semantics, metrics, edge cases, thresholds, and excluded claims.
- Preserves input identity, result-affecting settings, execution status, termination evidence, and artifact provenance.
- Separates operational verification from scientific acceptance.
- Requires selected values or invariants to be checked independently of the final summary.
- Links each substantive conclusion to verified evidence through an evidence ledger.
- Retains generation and verification entry points instead of delivering orphan results.
- Adds checksums, environment capture, logs, intermediates, resume fingerprints, and release controls only when the claim needs them.
- Keeps technical reproduction instructions separate from reader-facing scientific prose.
- Audits caches, large files, absolute paths, likely secrets, and release suitability without deleting files.

The bundled utilities use only the Python standard library.

## Minimal evidence package

```text
test_workspace/
├── README.md
├── test_spec.md
├── evidence_ledger.md
├── scripts/
├── results/
└── records/
```

Add `inputs/`, `config/`, `intermediate/`, `figures/`, `logs/`, or `report/` only when the test needs those responsibilities. The initializer records the declared structure in `records/workspace_contract.json`; the validator checks that contract instead of enforcing unused directories.

## Repository layout

```text
.
├── README.md
├── README.zh-CN.md
├── LICENSE
├── skill/
│   └── build-reproducible-research-tests/
│       ├── SKILL.md
│       ├── agents/openai.yaml
│       ├── assets/workspace-template/
│       ├── references/
│       └── scripts/
└── examples/
    └── parameter-trend/
```

The repository documentation, license, and worked example remain outside the distributable Skill directory.

## Installation

Install from this repository with the Codex Skill installer, using:

- repository: `sleepyyancy/build-reproducible-research-tests`
- path: `skill/build-reproducible-research-tests`

Then invoke:

```text
$build-reproducible-research-tests
```

Example request:

```text
Use $build-reproducible-research-tests to build an auditable comparison package for two numerical methods, including identified inputs, machine-readable results, independent verification, and evidence-linked conclusions.
```

## Bundled utilities

Edit each script's visible top-level configuration before use.

| Script | Purpose |
|---|---|
| `init_test_workspace.py` | Create a minimal evidence package and only the optional components declared for the test |
| `capture_environment.py` | Record reproducibility-relevant environment facts without changing the environment |
| `build_artifact_manifest.py` | Inventory files and compute streaming SHA-256 hashes |
| `validate_test_workspace.py` | Validate declared artifacts, nonempty core responsibilities, JSON records, placeholders, and manifest identity |
| `audit_publishability.py` | Report caches, large files, local paths, and likely sensitive content |

These utilities provide structural and provenance checks. Every test still needs domain-specific semantic and numerical verification appropriate to its scientific claim.

## Worked example

[`examples/parameter-trend`](examples/parameter-trend) tests whether a measured response is strictly increasing over four ordered parameter values. It contains an immutable input, explicit test specification, evidence ledger, run record, machine-readable result, independent metric recomputation, artifact manifest, and verification report.

Run it from the example directory:

```bash
python scripts/analyze_and_verify.py
```

## Validation

The Skill passed the official structure validator. All five bundled scripts passed syntax and functional checks covering:

- minimal initialization without unused optional directories;
- selective creation of declared optional components;
- refusal to overwrite an existing package;
- environment capture;
- artifact hashing and manifest consistency;
- contract-driven workspace validation;
- publication-risk reporting;
- local Markdown-link and package-consistency checks.

## License

Released under the [MIT License](LICENSE).
