#!/usr/bin/env python3
"""Capture reproducibility-relevant environment facts without modifying them."""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


# ============================ CONFIGURATION ============================
WORKSPACE_ROOT = Path.cwd()
OUTPUT_RELATIVE_PATH = Path("records/environment.json")
ALLOW_OVERWRITE = False
CAPTURE_ALL_INSTALLED_PACKAGES = True
SELECTED_ENVIRONMENT_VARIABLES = (
    "CONDA_DEFAULT_ENV",
    "CONDA_PREFIX",
    "VIRTUAL_ENV",
    "CUDA_VISIBLE_DEVICES",
    "OMP_NUM_THREADS",
)
# ======================================================================


def run_read_only_command(command: list[str]) -> dict[str, object]:
    try:
        completed = subprocess.run(
            command,
            cwd=WORKSPACE_ROOT,
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        return {"available": False, "error": type(exc).__name__}
    return {
        "available": True,
        "returncode": completed.returncode,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
    }


def installed_packages() -> list[dict[str, str]]:
    packages = []
    if not CAPTURE_ALL_INSTALLED_PACKAGES:
        return packages
    for distribution in importlib.metadata.distributions():
        name = distribution.metadata.get("Name") or "unknown"
        packages.append({"name": name, "version": distribution.version})
    return sorted(packages, key=lambda item: item["name"].lower())


def canonical_hash(value: object) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def build_record() -> dict[str, object]:
    environment_variables = {
        name: os.environ[name]
        for name in SELECTED_ENVIRONMENT_VARIABLES
        if name in os.environ
    }
    packages = installed_packages()
    record: dict[str, object] = {
        "schema_version": 1,
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "workspace_root": str(WORKSPACE_ROOT.resolve()),
        "python": {
            "version": sys.version,
            "implementation": platform.python_implementation(),
            "executable": sys.executable,
            "prefix": sys.prefix,
        },
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "processor": platform.processor(),
        },
        "environment_variables": environment_variables,
        "packages": packages,
        "git_head": run_read_only_command(["git", "rev-parse", "HEAD"]),
        "git_status": run_read_only_command(["git", "status", "--short"]),
    }
    record["environment_fingerprint"] = canonical_hash(
        {
            "python": record["python"],
            "platform": record["platform"],
            "environment_variables": environment_variables,
            "packages": packages,
        }
    )
    return record


def write_record(record: dict[str, object]) -> Path:
    output = WORKSPACE_ROOT.resolve() / OUTPUT_RELATIVE_PATH
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() and not ALLOW_OVERWRITE:
        raise FileExistsError(f"Refusing to overwrite existing record: {output}")
    temporary = output.with_suffix(output.suffix + ".tmp")
    temporary.write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    temporary.replace(output)
    return output


def main() -> int:
    output = write_record(build_record())
    print(f"Environment record written: {output}")
    print("This record may contain local paths; classify it before publication.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
