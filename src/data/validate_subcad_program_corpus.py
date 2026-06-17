"""Validate draft SubCAD programs generated for the limit-test corpus."""

from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REQ_DIR = ROOT / "docs" / "subcad_limit_test" / "single_metal_parts"
PROGRAM_DIR = ROOT / "docs" / "subcad_limit_test" / "subcad_programs"

REQUIRED_PROGRAM_KEYS = {
    "requirement_id",
    "part_name",
    "source_raw_idea_title",
    "program_status",
    "subcad_program",
    "coverage_notes",
    "known_gaps",
    "review_notes",
}


def expected_requirements() -> dict[str, dict]:
    expected: dict[str, dict] = {}
    for path in sorted(REQ_DIR.glob("agent_*_single_metal_parts.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for req in data.get("requirements", []):
            rid = req["requirement_id"]
            expected[rid] = {
                "source_agent": int(data["agent_number"]),
                "part_name": req["part_name"],
                "source_raw_idea_title": req["source"]["raw_idea_title"],
            }
    return expected


def validate_program_code(requirement_id: str, code: str) -> list[str]:
    errors: list[str] = []
    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        return [f"{requirement_id}: subcad_program syntax error: {exc}"]

    imports_stock = False
    assigns_part = False
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.module == "subcad":
            imports_stock = imports_stock or any(alias.name == "Stock" for alias in node.names)
        if isinstance(node, ast.Assign):
            assigns_part = assigns_part or any(isinstance(target, ast.Name) and target.id == "part" for target in node.targets)
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == "part":
            assigns_part = True

    if not imports_stock:
        errors.append(f"{requirement_id}: subcad_program must import Stock from subcad")
    if not assigns_part:
        errors.append(f"{requirement_id}: subcad_program must assign variable part")
    if "from_step" in code or "import_step" in code:
        errors.append(f"{requirement_id}: subcad_program must not import opaque geometry")
    return errors


def main() -> None:
    expected = expected_requirements()
    seen: dict[str, Path] = {}
    errors: list[str] = []
    files = sorted(PROGRAM_DIR.glob("agent_*_subcad_programs.json"))

    for path in files:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{path.name}: invalid JSON: {exc}")
            continue

        if data.get("stage") != "subcad_program_generation":
            errors.append(f"{path.name}: stage must be subcad_program_generation")
        programs = data.get("programs")
        if not isinstance(programs, list):
            errors.append(f"{path.name}: programs must be a list")
            continue

        for index, program in enumerate(programs, start=1):
            if not isinstance(program, dict):
                errors.append(f"{path.name}: program {index} must be an object")
                continue
            missing = REQUIRED_PROGRAM_KEYS - set(program)
            if missing:
                errors.append(f"{path.name}: program {index} missing {sorted(missing)}")
            rid = program.get("requirement_id")
            if not rid:
                errors.append(f"{path.name}: program {index} missing requirement_id")
                continue
            if rid in seen:
                errors.append(f"{rid}: duplicate in {seen[rid].name} and {path.name}")
            seen[rid] = path
            if rid not in expected:
                errors.append(f"{rid}: unknown requirement id")
            if program.get("program_status") != "draft_unexecuted":
                errors.append(f"{rid}: program_status must be draft_unexecuted")
            code = program.get("subcad_program")
            if not isinstance(code, str) or not code.strip():
                errors.append(f"{rid}: subcad_program must be non-empty string")
            else:
                errors.extend(validate_program_code(rid, code))
            for list_key in ("coverage_notes", "known_gaps"):
                if not isinstance(program.get(list_key), list):
                    errors.append(f"{rid}: {list_key} must be a list")

    missing_ids = sorted(set(expected) - set(seen))
    if missing_ids:
        errors.append(f"missing {len(missing_ids)} requirement ids; first 20: {missing_ids[:20]}")

    print(json.dumps({
        "program_files": len(files),
        "expected_requirements": len(expected),
        "programs_seen": len(seen),
        "missing_requirements": len(missing_ids),
        "errors": len(errors),
    }, indent=2))
    if errors:
        print("\n".join(errors[:80]))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
