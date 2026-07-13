# Build Reproducible Research Tests

[English](README.md) | [简体中文](README.zh-CN.md)

> 中文简介：这是一个面向理工科科研测试的独立Codex Skill，用于建立计划、执行、验证、文档和产物之间可追溯、可复现的完整链路。完整中文说明见[README.zh-CN.md](README.zh-CN.md)。

A self-contained Codex Skill for designing, executing, verifying, documenting, and packaging reproducible STEM research tests.

It is intended for scientific comparisons, simulation and model validation, physical experiments, observational-data analysis, parameter sweeps, sensitivity studies, and research workflow reviews. The Skill turns a research question into a traceable package linking inputs, configuration, execution records, intermediate transformations, results, figures, verification, and evidence-supported conclusions.

## Core capabilities

- Establishes an isolated test workspace with clear artifact responsibilities.
- Fixes `task_plan.md`, `findings.md`, and `progress.md` as persistent records.
- Requires a test contract before expensive or state-changing execution.
- Distinguishes confirmed facts, proposals, unresolved questions, and scientific interpretations.
- Supports Compact, Standard, and Extended workflow profiles.
- Adds conditional guidance for computation, physical experiments, observational studies, parameter sweeps, method comparisons, and scientific visualization.
- Separates operational verification from scientific acceptance.
- Preserves scripts, configuration, logs, manifests, checksums, and verification records.
- Includes evidence-based scientific writing rules and separate guidance for technical README files.
- Audits caches, large files, absolute paths, likely secrets, and release suitability without deleting files.

The Skill has no dependency on planning-with-files, plotting Skills, MCP servers, or third-party Python packages. Its bundled utilities use the Python standard library.

## Repository layout

```text
.
├── README.md
├── LICENSE
├── skill/
│   └── build-reproducible-research-tests/
│       ├── SKILL.md
│       ├── agents/openai.yaml
│       ├── assets/workspace-template/
│       ├── references/
│       └── scripts/
└── examples/
    └── compact-parameter-trend/
```

The repository README and license remain outside the distributable Skill directory. This keeps the Skill package compatible with the standard Skill structure.

## Installation

Copy the Skill directory into the Codex Skills directory:

```bash
cp -R skill/build-reproducible-research-tests "$CODEX_HOME/skills/"
```

Then invoke it explicitly:

```text
$build-reproducible-research-tests
```

Example request:

```text
Use $build-reproducible-research-tests to design a reproducible comparison between two numerical methods. Plan first, identify missing scientific decisions, and wait for approval before execution.
```

## Bundled utilities

The scripts use visible top-level configuration blocks rather than command-line arguments. Review and edit those blocks before execution.

| Script | Purpose |
|---|---|
| `init_test_workspace.py` | Create a non-destructive research-test workspace from templates |
| `capture_environment.py` | Record environment facts without modifying the environment |
| `build_artifact_manifest.py` | Inventory files and compute streaming SHA-256 hashes |
| `validate_test_workspace.py` | Validate structure, placeholders, JSON records, and manifest identity |
| `audit_publishability.py` | Report caches, large files, local paths, and likely sensitive content |

These utilities provide generic structural and provenance checks. Every research test must still implement domain-specific semantic and numerical verification.

## Example

[`examples/compact-parameter-trend`](examples/compact-parameter-trend) is a small, fully reproducible parameter-trend test. It contains an immutable input table, a global-configuration analysis script, a machine-readable result, a verification report, and the three persistent planning files.

Run it from the example directory:

```bash
python scripts/analyze_and_verify.py
```

## Safety model

The workflow does not authorize package installation, environment changes, deletion, overwriting of important source files, external publication, or unsupported scientific claims. Material uncertainty is surfaced to the user before execution. Automated publication checks report risks and never delete artifacts.

## Validation

The Skill passed the official Skill structure validator. Its five bundled scripts passed syntax checks and functional tests covering:

- non-destructive initialization;
- rejection of incomplete templates;
- Compact, Standard, and Extended workspace validation;
- environment capture;
- artifact hashing and manifest consistency;
- publication-risk reporting;
- final release audit with no blockers or warnings.

## License

Released under the [MIT License](LICENSE).
