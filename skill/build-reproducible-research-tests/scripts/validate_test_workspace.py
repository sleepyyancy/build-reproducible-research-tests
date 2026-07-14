#!/usr/bin/env python3
"""Validate declared research-package artifacts and recorded identity."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


# ============================ CONFIGURATION ============================
WORKSPACE_ROOT = Path.cwd()
CONTRACT_RELATIVE_PATH = Path("records/workspace_contract.json")
OUTPUT_RELATIVE_PATH = Path("records/workspace_validation.json")
ALLOW_OVERWRITE = False
CHECK_MANIFEST_HASHES = True
PLACEHOLDER_MARKERS = ("{{", "}}")
# ======================================================================


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_hash(value: object) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def safe_relative_path(value: object, field: str) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} contains a non-string or empty path")
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"{field} must contain workspace-relative paths: {value}")
    return path


def load_contract(root: Path) -> dict[str, object]:
    path = root / CONTRACT_RELATIVE_PATH
    if not path.is_file():
        raise FileNotFoundError(f"Workspace contract is missing: {path}")
    contract = json.loads(path.read_text(encoding="utf-8"))
    if contract.get("schema_version") != 1:
        raise ValueError("Unsupported workspace contract schema_version")
    for field in ("required_files", "required_nonempty_directories"):
        if not isinstance(contract.get(field), list):
            raise ValueError(f"Workspace contract field must be a list: {field}")
        for value in contract[field]:
            safe_relative_path(value, field)
    return contract


def add_check(
    checks: list[dict[str, str]],
    name: str,
    status: str,
    detail: str,
) -> None:
    checks.append({"check": name, "status": status, "detail": detail})


def check_declared_artifacts(
    root: Path,
    contract: dict[str, object],
    checks: list[dict[str, str]],
) -> list[Path]:
    declared_markdown: list[Path] = []
    for value in contract["required_files"]:
        relative = safe_relative_path(value, "required_files")
        path = root / relative
        status = "PASS" if path.is_file() and path.stat().st_size > 0 else "FAIL"
        add_check(
            checks,
            f"file:{relative.as_posix()}",
            status,
            "present and nonempty" if status == "PASS" else "missing or empty",
        )
        if relative.suffix.lower() == ".md" and path.is_file():
            declared_markdown.append(path)

    for value in contract["required_nonempty_directories"]:
        relative = safe_relative_path(value, "required_nonempty_directories")
        path = root / relative
        nonempty = path.is_dir() and any(path.iterdir())
        add_check(
            checks,
            f"directory:{relative.as_posix()}",
            "PASS" if nonempty else "FAIL",
            "present and nonempty" if nonempty else "missing or empty",
        )
    return declared_markdown


def check_placeholders(paths: list[Path], root: Path, checks: list[dict[str, str]]) -> None:
    unresolved = []
    for path in paths:
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
    records_dir = root / "records"
    for path in sorted(records_dir.glob("*.json")) if records_dir.is_dir() else []:
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


def check_manifest(
    root: Path,
    required: bool,
    checks: list[dict[str, str]],
) -> None:
    manifest_path = root / "records" / "artifact_manifest.json"
    if not manifest_path.is_file():
        add_check(
            checks,
            "manifest_consistency",
            "FAIL" if required else "PASS",
            "required manifest missing" if required else "manifest not declared",
        )
        return
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        add_check(checks, "manifest_consistency", "FAIL", f"invalid JSON: {exc}")
        return

    mismatches = []
    for entry in manifest.get("artifacts", []):
        relative_value = entry.get("path")
        try:
            relative = safe_relative_path(relative_value, "manifest.artifacts.path")
        except ValueError as exc:
            mismatches.append(str(exc))
            continue
        path = root / relative
        if not path.exists():
            mismatches.append(f"missing:{relative.as_posix()}")
            continue
        if path.is_symlink() or not path.is_file():
            continue
        if path.stat().st_size != entry.get("size_bytes"):
            mismatches.append(f"size:{relative.as_posix()}")
            continue
        expected_hash = entry.get("sha256")
        if CHECK_MANIFEST_HASHES and expected_hash and sha256_file(path) != expected_hash:
            mismatches.append(f"hash:{relative.as_posix()}")
    add_check(
        checks,
        "manifest_consistency",
        "PASS" if not mismatches else "FAIL",
        "recorded artifacts match" if not mismatches else "; ".join(mismatches[:20]),
    )


def validate() -> dict[str, object]:
    root = WORKSPACE_ROOT.resolve()
    contract = load_contract(root)
    checks: list[dict[str, str]] = []
    declared_markdown = check_declared_artifacts(root, contract, checks)
    check_placeholders(declared_markdown, root, checks)
    check_json_records(root, checks)
    check_manifest(root, bool(contract.get("artifact_manifest_required", False)), checks)
    failures = sum(check["status"] == "FAIL" for check in checks)
    warnings = sum(check["status"] == "WARN" for check in checks)
    return {
        "schema_version": 1,
        "validated_at": datetime.now(timezone.utc).isoformat(),
        "workspace_contract_sha256": canonical_hash(contract),
        "scope": "declared package structure and recorded artifact identity; domain checks remain test-specific",
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
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
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
