#!/usr/bin/env python3
"""Create a minimal research evidence package without overwriting files.

Edit the configuration block, then run this script directly. The script uses
only the Python standard library and never deletes existing content.
"""

from __future__ import annotations

import json
import shutil
from datetime import date
from pathlib import Path


# ============================ CONFIGURATION ============================
TEST_PARENT = Path.cwd()
TEST_DIRECTORY_NAME = "research_test"
TEST_TITLE = "Research Test"
ENABLED_OPTIONAL_COMPONENTS = ("inputs", "config", "logs")
REQUIRE_ARTIFACT_MANIFEST = True
REQUIRE_ENVIRONMENT_RECORD = False
CREATE_GITIGNORE = False
# ======================================================================


SKILL_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_ROOT = SKILL_ROOT / "assets" / "workspace-template"

CORE_DIRECTORIES = ("scripts", "results", "records")
OPTIONAL_COMPONENT_DIRECTORIES = {
    "inputs": ("inputs",),
    "config": ("config",),
    "intermediate": ("intermediate",),
    "figures": ("figures/previews", "figures/final"),
    "logs": ("logs",),
    "report": ("report",),
}

CORE_TEMPLATE_MAP = {
    "README.template.md": "README.md",
    "test_spec.md": "test_spec.md",
    "evidence_ledger.md": "evidence_ledger.md",
    "records/run_record.template.json": "records/run_record.template.json",
    "records/verification_report.template.md": "records/verification_report.md",
}


def render_template(text: str) -> str:
    """Replace only values known at workspace initialization."""
    return text.replace("{{TEST_TITLE}}", TEST_TITLE).replace("{{DATE}}", date.today().isoformat())


def enabled_directories() -> tuple[str, ...]:
    directories = list(CORE_DIRECTORIES)
    for component in ENABLED_OPTIONAL_COMPONENTS:
        directories.extend(OPTIONAL_COMPONENT_DIRECTORIES[component])
    return tuple(dict.fromkeys(directories))


def template_map() -> dict[str, str]:
    mapping = dict(CORE_TEMPLATE_MAP)
    if "report" in ENABLED_OPTIONAL_COMPONENTS:
        mapping["report/report.template.md"] = "report/report.template.md"
    return mapping


def validate_configuration() -> None:
    if not TEST_DIRECTORY_NAME.strip() or TEST_DIRECTORY_NAME == "research_test":
        raise ValueError("Set TEST_DIRECTORY_NAME before running the initializer")
    if not TEST_TITLE.strip() or TEST_TITLE == "Research Test":
        raise ValueError("Set TEST_TITLE before running the initializer")
    if Path(TEST_DIRECTORY_NAME).name != TEST_DIRECTORY_NAME:
        raise ValueError("TEST_DIRECTORY_NAME must be one directory name")
    unknown = sorted(set(ENABLED_OPTIONAL_COMPONENTS) - set(OPTIONAL_COMPONENT_DIRECTORIES))
    if unknown:
        raise ValueError(f"Unknown optional components: {unknown}")
    if len(set(ENABLED_OPTIONAL_COMPONENTS)) != len(ENABLED_OPTIONAL_COMPONENTS):
        raise ValueError("ENABLED_OPTIONAL_COMPONENTS contains duplicates")
    if not TEMPLATE_ROOT.is_dir():
        raise FileNotFoundError(f"Template directory not found: {TEMPLATE_ROOT}")
    missing_templates = [
        relative for relative in template_map() if not (TEMPLATE_ROOT / relative).is_file()
    ]
    if CREATE_GITIGNORE and not (TEMPLATE_ROOT / "gitignore.template").is_file():
        missing_templates.append("gitignore.template")
    if missing_templates:
        raise FileNotFoundError(f"Missing workspace templates: {missing_templates}")


def build_contract() -> dict[str, object]:
    required_files = [
        "README.md",
        "test_spec.md",
        "evidence_ledger.md",
        "records/workspace_contract.json",
        "records/verification_report.md",
    ]
    if REQUIRE_ARTIFACT_MANIFEST:
        required_files.append("records/artifact_manifest.json")
    if REQUIRE_ENVIRONMENT_RECORD:
        required_files.append("records/environment.json")
    return {
        "schema_version": 1,
        "test_title": TEST_TITLE,
        "enabled_optional_components": list(ENABLED_OPTIONAL_COMPONENTS),
        "required_files": required_files,
        "required_nonempty_directories": list(CORE_DIRECTORIES),
        "artifact_manifest_required": REQUIRE_ARTIFACT_MANIFEST,
        "environment_record_required": REQUIRE_ENVIRONMENT_RECORD,
        "note": "Add test-specific final artifacts to required_files before final validation.",
    }


def initialize_workspace() -> Path:
    validate_configuration()
    target = TEST_PARENT.resolve() / TEST_DIRECTORY_NAME
    if target.exists():
        raise FileExistsError(
            f"Target already exists; nothing was changed: {target}. "
            "Choose a new directory or inspect the existing package manually."
        )

    target.mkdir(parents=True)
    for relative_dir in enabled_directories():
        (target / relative_dir).mkdir(parents=True, exist_ok=False)

    for source_relative, destination_relative in template_map().items():
        source = TEMPLATE_ROOT / source_relative
        destination = target / destination_relative
        content = render_template(source.read_text(encoding="utf-8"))
        destination.write_text(content, encoding="utf-8")

    contract_path = target / "records" / "workspace_contract.json"
    contract_path.write_text(
        json.dumps(build_contract(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    if CREATE_GITIGNORE:
        shutil.copyfile(TEMPLATE_ROOT / "gitignore.template", target / ".gitignore")

    print(f"Created research evidence package: {target}")
    print(f"Optional components: {', '.join(ENABLED_OPTIONAL_COMPONENTS) or 'none'}")
    print("Next: complete test_spec.md and declare test-specific required artifacts.")
    return target


def main() -> int:
    initialize_workspace()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
