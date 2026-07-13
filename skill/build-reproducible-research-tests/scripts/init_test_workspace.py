#!/usr/bin/env python3
"""Create a reproducible research-test workspace without overwriting files.

Edit the configuration block, then run this script directly. The script uses
only the Python standard library and never deletes existing content.
"""

from __future__ import annotations

import shutil
from datetime import date
from pathlib import Path


# ============================ CONFIGURATION ============================
TEST_PARENT = Path.cwd() / "Test"
TEST_DIRECTORY_NAME = "XX_research_test"
TEST_TITLE = "Research Test"
PROFILE = "Standard"  # Compact, Standard, or Extended
CREATE_GITIGNORE = False
# ======================================================================


SKILL_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_ROOT = SKILL_ROOT / "assets" / "workspace-template"

DIRECTORIES = (
    "inputs",
    "config",
    "scripts",
    "intermediate",
    "results",
    "figures/previews",
    "figures/final",
    "logs",
    "records",
    "report",
)

TEMPLATE_MAP = {
    "task_plan.md": "task_plan.md",
    "findings.md": "findings.md",
    "progress.md": "progress.md",
    "test_spec.md": "test_spec.md",
    "README.template.md": "README.md",
    "records/run_record.template.json": "records/run_record.template.json",
    "records/verification_report.template.md": "records/verification_report.template.md",
    "report/report.template.md": "report/report.template.md",
}


def render_template(text: str) -> str:
    """Replace only values known at workspace initialization."""
    return (
        text.replace("{{TEST_TITLE}}", TEST_TITLE)
        .replace("{{DATE}}", date.today().isoformat())
        .replace("{{Compact|Standard|Extended}}", PROFILE)
    )


def validate_configuration() -> None:
    if PROFILE not in {"Compact", "Standard", "Extended"}:
        raise ValueError("PROFILE must be Compact, Standard, or Extended")
    if not TEST_DIRECTORY_NAME.strip() or TEST_DIRECTORY_NAME == "XX_research_test":
        raise ValueError("Set TEST_DIRECTORY_NAME before running the initializer")
    if not TEST_TITLE.strip() or TEST_TITLE == "Research Test":
        raise ValueError("Set TEST_TITLE before running the initializer")
    if Path(TEST_DIRECTORY_NAME).name != TEST_DIRECTORY_NAME:
        raise ValueError("TEST_DIRECTORY_NAME must be one directory name")
    if not TEMPLATE_ROOT.is_dir():
        raise FileNotFoundError(f"Template directory not found: {TEMPLATE_ROOT}")
    missing_templates = [
        relative for relative in TEMPLATE_MAP if not (TEMPLATE_ROOT / relative).is_file()
    ]
    if CREATE_GITIGNORE and not (TEMPLATE_ROOT / "gitignore.template").is_file():
        missing_templates.append("gitignore.template")
    if missing_templates:
        raise FileNotFoundError(f"Missing workspace templates: {missing_templates}")


def initialize_workspace() -> Path:
    validate_configuration()
    target = TEST_PARENT.resolve() / TEST_DIRECTORY_NAME

    if target.exists():
        raise FileExistsError(
            f"Target already exists; nothing was changed: {target}. "
            "Choose a new directory or inspect the existing workspace manually."
        )

    target.mkdir(parents=True)
    for relative_dir in DIRECTORIES:
        (target / relative_dir).mkdir(parents=True, exist_ok=False)

    for source_relative, destination_relative in TEMPLATE_MAP.items():
        source = TEMPLATE_ROOT / source_relative
        destination = target / destination_relative
        content = render_template(source.read_text(encoding="utf-8"))
        destination.write_text(content, encoding="utf-8")

    if CREATE_GITIGNORE:
        shutil.copyfile(TEMPLATE_ROOT / "gitignore.template", target / ".gitignore")

    print(f"Created research-test workspace: {target}")
    print(f"Profile: {PROFILE}")
    print("Next: complete test_spec.md and resolve its authorization gate.")
    return target


def main() -> int:
    initialize_workspace()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
