#!/usr/bin/env python3
"""Analyze, independently verify, and record the parameter-trend example."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path


# ============================ CONFIGURATION ============================
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
INPUT_PATH = WORKSPACE_ROOT / "inputs/measurements.csv"
RESULT_PATH = WORKSPACE_ROOT / "results/trend_summary.csv"
RUN_RECORD_PATH = WORKSPACE_ROOT / "records/run_record.json"
VERIFICATION_PATH = WORKSPACE_ROOT / "records/verification_report.md"
ALLOW_OVERWRITE_GENERATED_OUTPUTS = True
# ======================================================================


EXPECTED_COLUMNS = {"case_id", "parameter_value", "response_value"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_rows() -> list[dict[str, object]]:
    with INPUT_PATH.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if set(reader.fieldnames or []) != EXPECTED_COLUMNS:
            raise ValueError(f"Unexpected columns: {reader.fieldnames}")
        rows = []
        for raw in reader:
            parameter = float(raw["parameter_value"])
            response = float(raw["response_value"])
            if not math.isfinite(parameter) or not math.isfinite(response):
                raise ValueError(f"Non-finite value in {raw['case_id']}")
            rows.append(
                {
                    "case_id": raw["case_id"],
                    "parameter_value": parameter,
                    "response_value": response,
                }
            )
    if len(rows) < 2:
        raise ValueError("At least two rows are required")
    case_ids = [str(row["case_id"]) for row in rows]
    parameters = [float(row["parameter_value"]) for row in rows]
    if len(case_ids) != len(set(case_ids)):
        raise ValueError("Duplicate case_id values")
    if len(parameters) != len(set(parameters)):
        raise ValueError("Duplicate parameter values")
    return sorted(rows, key=lambda row: float(row["parameter_value"]))


def analyze(rows: list[dict[str, object]]) -> dict[str, object]:
    differences = [
        float(current["response_value"]) - float(previous["response_value"])
        for previous, current in zip(rows, rows[1:])
    ]
    return {
        "case_count": len(rows),
        "minimum_adjacent_difference": min(differences),
        "all_adjacent_differences_positive": all(value > 0.0 for value in differences),
    }


def independently_verify(
    rows: list[dict[str, object]], summary: dict[str, object]
) -> dict[str, object]:
    independent_differences = []
    for index in range(1, len(rows)):
        previous = float(rows[index - 1]["response_value"])
        current = float(rows[index]["response_value"])
        independent_differences.append(current - previous)
    independent_minimum = min(independent_differences)
    independent_positive = min(independent_differences) > 0.0
    metric_match = math.isclose(
        independent_minimum,
        float(summary["minimum_adjacent_difference"]),
        rel_tol=0.0,
        abs_tol=1.0e-12,
    ) and independent_positive == bool(summary["all_adjacent_differences_positive"])
    if not metric_match:
        raise RuntimeError("Independent recomputation disagrees with analysis")
    return {
        "minimum_adjacent_difference": independent_minimum,
        "all_adjacent_differences_positive": independent_positive,
        "matches_analysis": metric_match,
    }


def ensure_output_policy() -> None:
    generated = (RESULT_PATH, RUN_RECORD_PATH, VERIFICATION_PATH)
    existing = [path for path in generated if path.exists()]
    if existing and not ALLOW_OVERWRITE_GENERATED_OUTPUTS:
        raise FileExistsError(f"Generated outputs already exist: {existing}")


def write_outputs(
    summary: dict[str, object], verification: dict[str, object], started_at: str
) -> None:
    ensure_output_policy()
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    VERIFICATION_PATH.parent.mkdir(parents=True, exist_ok=True)
    with RESULT_PATH.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(["metric", "value"])
        writer.writerow(["case_count", summary["case_count"]])
        writer.writerow(["minimum_adjacent_difference", summary["minimum_adjacent_difference"]])
        writer.writerow(
            [
                "all_adjacent_differences_positive",
                str(summary["all_adjacent_differences_positive"]).lower(),
            ]
        )

    scientific_status = "PASS" if summary["all_adjacent_differences_positive"] else "FAIL"
    report = f"""# Verification Report: Parameter-Trend Evidence Package

## Checks
| Check | Expected | Actual | Status |
|---|---|---|---|
| Unique and finite input rows | Valid | Valid | PASS |
| Case count | 4 | {summary['case_count']} | {'PASS' if summary['case_count'] == 4 else 'FAIL'} |
| Minimum adjacent response difference | Greater than 0 | {summary['minimum_adjacent_difference']:.6g} | {scientific_status} |
| Independent recomputation | Matches analysis | {verification['matches_analysis']} | PASS |

## Outcomes
- Operational verification: PASS
- Scientific acceptance: {scientific_status}
- Acceptance criterion: every adjacent response difference is strictly positive
"""
    VERIFICATION_PATH.write_text(report, encoding="utf-8")

    finished_at = datetime.now(timezone.utc).isoformat()
    run_record = {
        "schema_version": 1,
        "run_id": "parameter-trend-analysis",
        "started_at": started_at,
        "finished_at": finished_at,
        "status": "complete",
        "entry_point": "scripts/analyze_and_verify.py",
        "input": {
            "path": "inputs/measurements.csv",
            "sha256": sha256_file(INPUT_PATH),
        },
        "code_sha256": sha256_file(Path(__file__)),
        "termination_evidence": "process exit 0 and records/verification_report.md",
        "outputs": [
            "results/trend_summary.csv",
            "records/verification_report.md",
        ],
    }
    RUN_RECORD_PATH.write_text(
        json.dumps(run_record, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    started_at = datetime.now(timezone.utc).isoformat()
    rows = load_rows()
    summary = analyze(rows)
    verification = independently_verify(rows, summary)
    write_outputs(summary, verification, started_at)
    print("Operational verification: PASS")
    print(
        "Scientific acceptance: "
        + ("PASS" if summary["all_adjacent_differences_positive"] else "FAIL")
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
