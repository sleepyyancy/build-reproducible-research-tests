#!/usr/bin/env python3
"""Validate research-test workspace structure and recorded artifact identity."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


# ============================ CONFIGURATION ============================
WORKSPACE_ROOT = Path.cwd()
PROFILE = "Standard"  # Compact, Standard, or Extended
OUTPUT_RELATIVE_PATH = Path("records/workspace_validation.json")
ALLOW_OVERWRITE = False
CHECK_MANIFEST_HASHES = True
PLACEHOLDER_MARKERS = ("{{", "}}")
# ======================================================================


BASE_REQUIRED_FILES = {
    "task_plan.md",
    "findings.md",
    "progress.md",
    "test_spec.md",
    "README.md",
}

PROFILE_REQUIRED_DIRECTORIES = {
    "Compact": {"inputs", "scripts", "results", "records"},
    "Standard": {
        "inputs",
        "config",
        "scripts",
        "intermediate",
        "results",
        "figures",
        "logs",
        "records",
        "report",
    },
    "Extended": {
        "inputs",
        "config",
        "scripts",
        "intermediate",
        "results",
        "figures",
        "logs",
        "records",
        "report",
    },
}

COMPLETION_REQUIRED_FILES = {
    "Standard": {"records/artifact_manifest.json", "records/verification_report.md"},
    "Extended": {
        "records/artifact_manifest.json",
        "records/environment.json",
        "records/verification_report.md",
    },
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def add_check(
    checks: list[dict[str, str]],
    name: str,
    status: str,
    detail: str,
) -> None:
    checks.append({"check": name, "status": status, "detail": detail})


def check_structure(root: Path, checks: list[dict[str, str]]) -> None:
    required_directories = PROFILE_REQUIRED_DIRECTORIES[PROFILE]
    for relative in sorted(required_directories):
        path = root / relative
        add_check(
            checks,
            f"directory:{relative}",
            "PASS" if path.is_dir() else "FAIL",
            "present" if path.is_dir() else "missing",
        )
    required_files = set(BASE_REQUIRED_FILES)
    required_files.update(COMPLETION_REQUIRED_FILES.get(PROFILE, set()))
    for relative in sorted(required_files):
        path = root / relative
        status = "PASS" if path.is_file() and path.stat().st_size > 0 else "FAIL"
        add_check(checks, f"file:{relative}", status, "present and nonempty" if status == "PASS" else "missing or empty")


def check_placeholders(root: Path, checks: list[dict[str, str]]) -> None:
    candidate_names = {
        "task_plan.md",
        "findings.md",
        "progress.md",
        "test_spec.md",
        "README.md",
        "verification_report.md",
    }
    unresolved = []
    for path in root.rglob("*.md"):
        if path.name not in candidate_names:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if any(marker in text for marker in PLACEHOLDER_MARKERS):
            unresolved.append(path.relative_to(root).as_posix())
    add_check(
        checks,
        "unresolved_placeholders",
        "PASS" if not unresolved else "FAIL",
        "none" if not unresolved else ", ".join(unresolved),
    )


def check_json_records(root: Path, checks: list[dict[str, str]]) -> None:
    invalid = []
    for path in sorted((root / "records").glob("*.json")) if (root / "records").is_dir() else []:
        if path.name == OUTPUT_RELATIVE_PATH.name:
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            invalid.append(path.name)
    add_check(
        checks,
        "json_records_parse",
        "PASS" if not invalid else "FAIL",
        "all JSON records parse" if not invalid else ", ".join(invalid),
    )


def check_manifest(root: Path, checks: list[dict[str, str]]) -> None:
    manifest_path = root / "records/artifact_manifest.json"
    if not manifest_path.is_file():
        status = "WARN" if PROFILE == "Compact" else "FAIL"
        add_check(checks, "manifest_consistency", status, "artifact manifest missing")
        return
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        add_check(checks, "manifest_consistency", "FAIL", f"invalid JSON: {exc}")
        return

    mismatches = []
    for entry in manifest.get("artifacts", []):
        relative = entry.get("path")
        if not isinstance(relative, str):
            mismatches.append("entry without path")
            continue
        path = root / relative
        if not path.exists():
            mismatches.append(f"missing:{relative}")
            continue
        if path.is_symlink() or not path.is_file():
            continue
        if path.stat().st_size != entry.get("size_bytes"):
            mismatches.append(f"size:{relative}")
            continue
        expected_hash = entry.get("sha256")
        if CHECK_MANIFEST_HASHES and expected_hash and sha256_file(path) != expected_hash:
            mismatches.append(f"hash:{relative}")
    add_check(
        checks,
        "manifest_consistency",
        "PASS" if not mismatches else "FAIL",
        "recorded artifacts match" if not mismatches else "; ".join(mismatches[:20]),
    )


def validate() -> dict[str, object]:
    if PROFILE not in PROFILE_REQUIRED_DIRECTORIES:
        raise ValueError("PROFILE must be Compact, Standard, or Extended")
    root = WORKSPACE_ROOT.resolve()
    checks: list[dict[str, str]] = []
    check_structure(root, checks)
    check_placeholders(root, checks)
    check_json_records(root, checks)
    check_manifest(root, checks)
    failures = sum(check["status"] == "FAIL" for check in checks)
    warnings = sum(check["status"] == "WARN" for check in checks)
    return {
        "schema_version": 1,
        "validated_at": datetime.now(timezone.utc).isoformat(),
        "profile": PROFILE,
        "scope": "structural and recorded artifact identity; domain checks remain test-specific",
        "status": "FAIL" if failures else "PASS",
        "failure_count": failures,
        "warning_count": warnings,
        "checks": checks,
    }


def write_report(report: dict[str, object]) -> Path:
    output = WORKSPACE_ROOT.resolve() / OUTPUT_RELATIVE_PATH
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() and not ALLOW_OVERWRITE:
        raise FileExistsError(f"Refusing to overwrite existing validation: {output}")
    temporary = output.with_suffix(output.suffix + ".tmp")
    temporary.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    temporary.replace(output)
    return output


def main() -> int:
    report = validate()
    output = write_report(report)
    print(f"Workspace validation: {report['status']}")
    print(f"Failures: {report['failure_count']}; warnings: {report['warning_count']}")
    print(f"Record: {output}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
