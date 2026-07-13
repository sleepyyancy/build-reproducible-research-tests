#!/usr/bin/env python3
"""Analyze and verify the compact parameter-trend example."""

from __future__ import annotations

import csv
import math
from pathlib import Path


# ============================ CONFIGURATION ============================
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
INPUT_PATH = WORKSPACE_ROOT / "inputs/measurements.csv"
RESULT_PATH = WORKSPACE_ROOT / "results/trend_summary.csv"
VERIFICATION_PATH = WORKSPACE_ROOT / "records/verification_report.md"
ALLOW_OVERWRITE_GENERATED_OUTPUTS = True
# ======================================================================


EXPECTED_COLUMNS = {"case_id", "parameter_value", "response_value"}


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


def ensure_output_policy() -> None:
    existing = [path for path in (RESULT_PATH, VERIFICATION_PATH) if path.exists()]
    if existing and not ALLOW_OVERWRITE_GENERATED_OUTPUTS:
        raise FileExistsError(f"Generated outputs already exist: {existing}")


def write_outputs(summary: dict[str, object]) -> None:
    ensure_output_policy()
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    VERIFICATION_PATH.parent.mkdir(parents=True, exist_ok=True)
    with RESULT_PATH.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(["metric", "value"])
        writer.writerow(["case_count", summary["case_count"]])
        writer.writerow(
            ["minimum_adjacent_difference", summary["minimum_adjacent_difference"]]
        )
        writer.writerow(
            [
                "all_adjacent_differences_positive",
                str(summary["all_adjacent_differences_positive"]).lower(),
            ]
        )

    operational_status = "PASS"
    scientific_status = (
        "PASS" if summary["all_adjacent_differences_positive"] else "FAIL"
    )
    report = f"""# Verification Report: Compact Parameter-Trend Example

## Checks
| Check | Expected | Actual | Status |
|---|---|---|---|
| Unique and finite input rows | Valid | Valid | PASS |
| Case count | 4 | {summary['case_count']} | {'PASS' if summary['case_count'] == 4 else 'FAIL'} |
| Minimum adjacent response difference | Greater than 0 | {summary['minimum_adjacent_difference']:.6g} | {scientific_status} |

## Outcomes
- Operational verification: {operational_status}
- Scientific acceptance: {scientific_status}
- Acceptance criterion: every adjacent response difference is strictly positive
"""
    VERIFICATION_PATH.write_text(report, encoding="utf-8")


def main() -> int:
    rows = load_rows()
    summary = analyze(rows)
    write_outputs(summary)
    print(f"Operational verification: PASS")
    print(
        "Scientific acceptance: "
        + ("PASS" if summary["all_adjacent_differences_positive"] else "FAIL")
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
