#!/usr/bin/env python3
"""Inventory workspace artifacts and compute streaming SHA-256 hashes."""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path


# ============================ CONFIGURATION ============================
WORKSPACE_ROOT = Path.cwd()
OUTPUT_RELATIVE_PATH = Path("records/artifact_manifest.json")
ALLOW_OVERWRITE = False
HASH_CHUNK_BYTES = 8 * 1024 * 1024
HASH_FILE_SIZE_LIMIT_BYTES = None  # Set an integer to omit hashes above a limit.
EXCLUDED_DIRECTORY_NAMES = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ipynb_checkpoints",
}
EXCLUDED_FILE_NAMES = {".DS_Store"}
EXCLUDED_RELATIVE_PATHS = {
    Path("records/artifact_manifest.json"),
    Path("records/workspace_validation.json"),
    Path("records/publishability_audit.json"),
}
# ======================================================================


ROLE_BY_TOP_DIRECTORY = {
    "inputs": ("source", "local-only"),
    "config": ("configuration", "publish"),
    "scripts": ("code", "publish"),
    "intermediate": ("derived", "regenerate"),
    "results": ("final-result", "publish"),
    "figures": ("figure", "publish"),
    "logs": ("execution-log", "local-only"),
    "records": ("record", "publish-review"),
    "report": ("reader-facing-report", "publish"),
}


def should_exclude(relative_path: Path) -> bool:
    if any(part in EXCLUDED_DIRECTORY_NAMES for part in relative_path.parts[:-1]):
        return True
    return relative_path.name in EXCLUDED_FILE_NAMES


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(HASH_CHUNK_BYTES), b""):
            digest.update(chunk)
    return digest.hexdigest()


def artifact_role(relative_path: Path) -> tuple[str, str]:
    top = relative_path.parts[0] if relative_path.parts else ""
    return ROLE_BY_TOP_DIRECTORY.get(top, ("workspace-document", "publish-review"))


def build_entry(root: Path, path: Path) -> dict[str, object]:
    relative = path.relative_to(root)
    stat = path.lstat()
    role, publication_class = artifact_role(relative)
    entry: dict[str, object] = {
        "path": relative.as_posix(),
        "role": role,
        "publication_class": publication_class,
        "size_bytes": stat.st_size,
        "modified_ns": stat.st_mtime_ns,
        "is_symlink": path.is_symlink(),
    }
    if path.is_symlink():
        entry["symlink_target"] = os.readlink(path)
        entry["sha256"] = None
        entry["hash_status"] = "not_hashed_symlink"
    elif (
        HASH_FILE_SIZE_LIMIT_BYTES is not None
        and stat.st_size > HASH_FILE_SIZE_LIMIT_BYTES
    ):
        entry["sha256"] = None
        entry["hash_status"] = "omitted_above_size_limit"
    else:
        entry["sha256"] = sha256_file(path)
        entry["hash_status"] = "complete"
    return entry


def build_manifest() -> dict[str, object]:
    root = WORKSPACE_ROOT.resolve()
    output = root / OUTPUT_RELATIVE_PATH
    artifacts = []
    total_size = 0
    for path in sorted(root.rglob("*")):
        if not (path.is_file() or path.is_symlink()):
            continue
        relative = path.relative_to(root)
        if relative in EXCLUDED_RELATIVE_PATHS or should_exclude(relative):
            continue
        entry = build_entry(root, path)
        artifacts.append(entry)
        total_size += int(entry["size_bytes"])
    return {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "workspace_name": root.name,
        "hash_algorithm": "sha256",
        "artifact_count": len(artifacts),
        "total_size_bytes": total_size,
        "artifacts": artifacts,
    }


def write_manifest(manifest: dict[str, object]) -> Path:
    output = WORKSPACE_ROOT.resolve() / OUTPUT_RELATIVE_PATH
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() and not ALLOW_OVERWRITE:
        raise FileExistsError(f"Refusing to overwrite existing manifest: {output}")
    temporary = output.with_suffix(output.suffix + ".tmp")
    temporary.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    temporary.replace(output)
    return output


def main() -> int:
    manifest = build_manifest()
    output = write_manifest(manifest)
    print(f"Artifact manifest written: {output}")
    print(f"Artifacts: {manifest['artifact_count']}")
    print(f"Total bytes: {manifest['total_size_bytes']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
