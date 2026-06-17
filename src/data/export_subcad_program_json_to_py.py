"""Export Stage 3 SubCAD program JSON records to standalone .py files."""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROGRAM_JSON_DIR = ROOT / "docs" / "subcad_limit_test" / "subcad_programs"
PROGRAM_PY_DIR = ROOT / "docs" / "subcad_limit_test" / "subcad_programs_py"


def slugify(value: str, limit: int = 72) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_").lower()
    return slug[:limit].rstrip("_") or "part"


def validate_code(requirement_id: str, code: str) -> None:
    tree = ast.parse(code)
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
        raise ValueError(f"{requirement_id}: program must import Stock from subcad")
    if not assigns_part:
        raise ValueError(f"{requirement_id}: program must assign variable part")


def executable_code_and_notes(program: dict) -> tuple[str, list[str]]:
    """Return executable code plus added gaps from defensive sanitization.

    The parallel generation pass put a global `.chamfer(width=1.0)` at the end
    of every draft. In current SubCAD/OCC this often fails after otherwise
    valid cuts, preventing STEP/STL export entirely. The frozen requirement
    still asks for chamfers; the executable corpus records that as a gap rather
    than keeping a known-fatal call in every file.
    """

    code_lines = program["subcad_program"].strip().splitlines()
    kept_lines: list[str] = []
    removed_chamfer = False
    for line in code_lines:
        if ".chamfer(" in line:
            removed_chamfer = True
            continue
        kept_lines.append(line)
    added_gaps = []
    if removed_chamfer:
        added_gaps.append(
            "Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable."
        )
    return "\n".join(kept_lines).strip() + "\n", added_gaps


def render_py(agent_number: int, source_file: str, program: dict) -> str:
    requirement_id = program["requirement_id"]
    code, added_gaps = executable_code_and_notes(program)
    validate_code(requirement_id, code)
    coverage = program.get("coverage_notes") or []
    gaps = list(program.get("known_gaps") or []) + added_gaps
    review = program.get("review_notes") or []
    lines = [
        f"# Requirement: {requirement_id}",
        f"# Source agent: {agent_number:03d}",
        f"# Source requirements file: {source_file}",
        f"# Part: {program.get('part_name', '')}",
        f"# Raw idea: {program.get('source_raw_idea_title', '')}",
        f"# Status: {program.get('program_status', 'draft_unexecuted')}",
        "#",
        "# Coverage notes:",
    ]
    lines.extend(f"# - {item}" for item in coverage)
    lines.extend(["#", "# Known gaps:"])
    if gaps:
        lines.extend(f"# - {item}" for item in gaps)
    else:
        lines.append("# - None recorded.")
    lines.extend(["#", "# Review notes:"])
    if review:
        lines.extend(f"# - {item}" for item in review)
    else:
        lines.append("# - Not reviewed yet.")
    return "\n".join(lines).rstrip() + "\n\n" + code


def main() -> None:
    PROGRAM_PY_DIR.mkdir(parents=True, exist_ok=True)
    written = 0
    agents = 0
    index_lines = [
        "# SubCAD Program Python Files",
        "",
        "Each `.py` file defines one variable named `part` for one frozen single-metal-part requirement.",
        "",
    ]

    for json_path in sorted(PROGRAM_JSON_DIR.glob("agent_*_subcad_programs.json")):
        data = json.loads(json_path.read_text(encoding="utf-8"))
        agent_number = int(data["agent_number"])
        agent_dir = PROGRAM_PY_DIR / f"agent_{agent_number:03d}"
        agent_dir.mkdir(parents=True, exist_ok=True)
        agents += 1
        source_file = data.get("source_requirements_file", "")
        programs = data.get("programs", [])
        index_lines.append(f"## Agent {agent_number:03d}")
        index_lines.append("")

        for program in programs:
            requirement_id = program["requirement_id"]
            filename = f"{requirement_id.lower()}_{slugify(program.get('source_raw_idea_title', 'part'))}.py"
            py_path = agent_dir / filename
            py_path.write_text(
                render_py(agent_number, source_file, program),
                encoding="utf-8",
            )
            written += 1
            rel_path = py_path.relative_to(ROOT).as_posix()
            index_lines.append(f"- `{requirement_id}`: `{rel_path}`")
        index_lines.append("")

    (PROGRAM_PY_DIR / "README.md").write_text("\n".join(index_lines).rstrip() + "\n", encoding="utf-8")
    print(json.dumps({
        "agents": agents,
        "python_files": written,
        "output_dir": str(PROGRAM_PY_DIR),
    }, indent=2))


if __name__ == "__main__":
    main()
