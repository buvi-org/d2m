"""Validate standalone .py files for the SubCAD limit-test program corpus."""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REQ_DIR = ROOT / "docs" / "subcad_limit_test" / "single_metal_parts"
PROGRAM_PY_DIR = ROOT / "docs" / "subcad_limit_test" / "subcad_programs_py"


def expected_requirement_ids() -> set[str]:
    ids: set[str] = set()
    for path in sorted(REQ_DIR.glob("agent_*_single_metal_parts.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for req in data.get("requirements", []):
            ids.add(req["requirement_id"])
    return ids


def inspect_py(path: Path) -> tuple[str | None, list[str]]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    match = re.search(r"^# Requirement: (SMP-\d{3}-\d{2})$", text, re.MULTILINE)
    requirement_id = match.group(1) if match else None
    if requirement_id is None:
        errors.append(f"{path}: missing requirement header")

    try:
        tree = ast.parse(text, filename=str(path))
    except SyntaxError as exc:
        return requirement_id, [f"{path}: syntax error: {exc}"]

    imports_stock = False
    assigns_part = False
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.module == "subcad":
            imports_stock = imports_stock or any(alias.name == "Stock" for alias in node.names)
        if isinstance(node, ast.Assign):
            assigns_part = assigns_part or any(
                isinstance(target, ast.Name) and target.id == "part"
                for target in node.targets
            )
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            assigns_part = assigns_part or node.target.id == "part"

    if not imports_stock:
        errors.append(f"{path}: must import Stock from subcad")
    if not assigns_part:
        errors.append(f"{path}: must assign variable part")
    if "from_step" in text or "import_step" in text:
        errors.append(f"{path}: must not import opaque geometry")
    return requirement_id, errors


def main() -> None:
    expected = expected_requirement_ids()
    seen: dict[str, Path] = {}
    errors: list[str] = []
    files = sorted(PROGRAM_PY_DIR.glob("agent_*/*.py"))
    for path in files:
        requirement_id, file_errors = inspect_py(path)
        errors.extend(file_errors)
        if requirement_id:
            if requirement_id in seen:
                errors.append(f"{requirement_id}: duplicate in {seen[requirement_id]} and {path}")
            seen[requirement_id] = path

    missing = sorted(expected - set(seen))
    unknown = sorted(set(seen) - expected)
    if missing:
        errors.append(f"missing {len(missing)} requirement ids; first 20: {missing[:20]}")
    if unknown:
        errors.append(f"unknown {len(unknown)} requirement ids; first 20: {unknown[:20]}")

    print(json.dumps({
        "python_files": len(files),
        "expected_requirements": len(expected),
        "programs_seen": len(seen),
        "missing_requirements": len(missing),
        "unknown_requirements": len(unknown),
        "errors": len(errors),
    }, indent=2))
    if errors:
        print("\n".join(errors[:80]))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
