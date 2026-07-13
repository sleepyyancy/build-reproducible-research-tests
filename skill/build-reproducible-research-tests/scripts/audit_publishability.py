#!/usr/bin/env python3
"""Report publication risks without deleting or rewriting any artifact."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path


# ============================ CONFIGURATION ============================
WORKSPACE_ROOT = Path.cwd()
OUTPUT_RELATIVE_PATH = Path("records/publishability_audit.json")
ALLOW_OVERWRITE = False
LARGE_FILE_BYTES = 20 * 1024 * 1024
MAX_TEXT_SCAN_BYTES = 2 * 1024 * 1024
EXCLUDED_DIRECTORY_NAMES = {".git"}
# ======================================================================


CACHE_NAMES = {
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ipynb_checkpoints",
    ".DS_Store",
}

SENSITIVE_NAME_PATTERNS = (
    re.compile(r"(^|[._-])(secret|credentials?|token|passwd|password)([._-]|$)", re.I),
    re.compile(r"\.(pem|key|p12|pfx)$", re.I),
)

TEXT_PATTERNS = (
    ("absolute_unix_path", re.compile(r"(?<![\w.])/(?:home|Users|mnt|private|var/tmp)/[^\s'\"`]+")),
    ("absolute_windows_path", re.compile(r"[A-Za-z]:\\(?:Users|Documents and Settings)\\[^\s'\"`]+")),
    ("private_key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("likely_assignment_secret", re.compile(r"(?i)(?:api[_-]?key|access[_-]?token|password)\s*[:=]\s*['\"][^'\"]{8,}['\"]")),
)


def is_probably_text(path: Path) -> bool:
    if path.stat().st_size > MAX_TEXT_SCAN_BYTES:
        return False
    try:
        sample = path.read_bytes()[:8192]
    except OSError:
        return False
    return b"\x00" not in sample


def add_finding(
    findings: list[dict[str, object]],
    severity: str,
    category: str,
    path: Path,
    detail: str,
) -> None:
    findings.append(
        {
            "severity": severity,
            "category": category,
            "path": path.as_posix(),
            "detail": detail,
        }
    )


def audit() -> dict[str, object]:
    root = WORKSPACE_ROOT.resolve()
    output = root / OUTPUT_RELATIVE_PATH
    findings: list[dict[str, object]] = []
    reported_cache_paths: set[Path] = set()

    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if any(part in EXCLUDED_DIRECTORY_NAMES for part in relative.parts):
            continue
        cache_index = next(
            (index for index, part in enumerate(relative.parts) if part in CACHE_NAMES),
            None,
        )
        if cache_index is not None:
            cache_path = Path(*relative.parts[: cache_index + 1])
            if cache_path not in reported_cache_paths:
                add_finding(
                    findings,
                    "warning",
                    "cache_or_temporary",
                    cache_path,
                    "exclude from release",
                )
                reported_cache_paths.add(cache_path)
            continue
        if not path.is_file() or path == output:
            continue
        for pattern in SENSITIVE_NAME_PATTERNS:
            if pattern.search(path.name):
                add_finding(findings, "blocker", "sensitive_filename", relative, "review content and exclude if sensitive")
                break
        size = path.stat().st_size
        if size >= LARGE_FILE_BYTES:
            add_finding(findings, "warning", "large_file", relative, f"{size} bytes; choose publish/local-only/regenerate policy")
        if not is_probably_text(path):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for category, pattern in TEXT_PATTERNS:
            matches = pattern.findall(text)
            if not matches:
                continue
            severity = "blocker" if category in {"private_key", "likely_assignment_secret"} else "warning"
            add_finding(findings, severity, category, relative, f"{len(matches)} match(es); inspect before release")

    blockers = sum(item["severity"] == "blocker" for item in findings)
    warnings = sum(item["severity"] == "warning" for item in findings)
    return {
        "schema_version": 1,
        "audited_at": datetime.now(timezone.utc).isoformat(),
        "status": "BLOCKED" if blockers else "REVIEW" if warnings else "CLEAR",
        "blocker_count": blockers,
        "warning_count": warnings,
        "note": "This audit is heuristic and never deletes files. Review every finding.",
        "findings": findings,
    }


def write_report(report: dict[str, object]) -> Path:
    output = WORKSPACE_ROOT.resolve() / OUTPUT_RELATIVE_PATH
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() and not ALLOW_OVERWRITE:
        raise FileExistsError(f"Refusing to overwrite existing audit: {output}")
    temporary = output.with_suffix(output.suffix + ".tmp")
    temporary.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    temporary.replace(output)
    return output


def main() -> int:
    report = audit()
    output = write_report(report)
    print(f"Publishability audit: {report['status']}")
    print(f"Blockers: {report['blocker_count']}; warnings: {report['warning_count']}")
    print(f"Record: {output}")
    return 1 if report["status"] == "BLOCKED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
