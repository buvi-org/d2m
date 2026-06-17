"""Execute standalone SubCAD corpus programs and export review artifacts.

This runner executes generated .py programs one at a time, captures runtime
errors, exports STEP/STL/process-plan outputs where possible, and performs a
basic envelope check against the frozen Stage 2 requirement dimensions.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import os
import re
import sys
import time
import traceback
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = ROOT / "src"
REQ_DIR = ROOT / "docs" / "subcad_limit_test" / "single_metal_parts"
PROGRAM_PY_DIR = ROOT / "docs" / "subcad_limit_test" / "subcad_programs_py"
DEFAULT_OUTPUT_DIR = ROOT / "runs" / "subcad_limit_test_execution"


def requirement_index() -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    for path in sorted(REQ_DIR.glob("agent_*_single_metal_parts.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for req in data.get("requirements", []):
            index[req["requirement_id"]] = req
    return index


def requirement_id_from_file(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    match = re.search(r"^# Requirement: (SMP-\d{3}-\d{2})$", text, re.MULTILINE)
    if not match:
        raise ValueError(f"{path}: missing '# Requirement: SMP-###-##' header")
    return match.group(1)


def load_part(path: Path):
    sys.path.insert(0, str(SRC_DIR))
    module_name = f"_subcad_corpus_{path.stem}_{os.getpid()}"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module spec for {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "part"):
        raise RuntimeError(f"{path}: program did not define 'part'")
    return module.part


def get_bounding_box(part) -> dict[str, float]:
    bbox = getattr(part, "bounding_box", None)
    if callable(bbox):
        value = bbox()
    else:
        value = bbox
    if not isinstance(value, dict):
        return {}
    return {str(key): float(val) for key, val in value.items() if isinstance(val, (int, float))}


def bbox_dimensions(bbox: dict[str, float]) -> list[float]:
    if {"xlen", "ylen", "zlen"} <= set(bbox):
        return [bbox["xlen"], bbox["ylen"], bbox["zlen"]]
    if {"xmin", "xmax", "ymin", "ymax", "zmin", "zmax"} <= set(bbox):
        return [
            bbox["xmax"] - bbox["xmin"],
            bbox["ymax"] - bbox["ymin"],
            bbox["zmax"] - bbox["zmin"],
        ]
    if {"length", "width", "height"} <= set(bbox):
        return [bbox["length"], bbox["width"], bbox["height"]]
    return []


def expected_dimensions(req: dict[str, Any]) -> list[float]:
    dims = req.get("overall_envelope_mm", {})
    if {"length_mm", "width_mm", "height_mm"} <= set(dims):
        return [float(dims["length_mm"]), float(dims["width_mm"]), float(dims["height_mm"])]
    if {"length_mm", "width_mm", "thickness_mm"} <= set(dims):
        return [float(dims["length_mm"]), float(dims["width_mm"]), float(dims["thickness_mm"])]
    if {"outer_diameter_mm", "overall_length_mm"} <= set(dims):
        od = float(dims["outer_diameter_mm"])
        length = float(dims["overall_length_mm"])
        return [od, od, length]
    return []


def envelope_check(req: dict[str, Any], bbox: dict[str, float], tolerance_mm: float = 0.75) -> dict[str, Any]:
    actual = bbox_dimensions(bbox)
    expected = expected_dimensions(req)
    if not actual or not expected:
        return {
            "status": "not_checked",
            "reason": "missing actual or expected envelope dimensions",
            "expected_mm": expected,
            "actual_mm": actual,
        }
    expected_sorted = sorted(expected)
    actual_sorted = sorted(actual)
    deltas = [abs(a - e) for a, e in zip(actual_sorted, expected_sorted)]
    max_delta = max(deltas) if deltas else math.inf
    return {
        "status": "pass" if max_delta <= tolerance_mm else "fail",
        "expected_mm_sorted": expected_sorted,
        "actual_mm_sorted": actual_sorted,
        "deltas_mm": deltas,
        "tolerance_mm": tolerance_mm,
    }


def safe_process_plan(part) -> dict[str, Any] | None:
    plan = getattr(part, "process_plan", None)
    if callable(plan):
        return plan()
    if isinstance(plan, dict):
        return plan
    return None


def run_one(path: Path, reqs: dict[str, dict[str, Any]], output_root: Path, export_step: bool, export_stl: bool) -> dict[str, Any]:
    rid = requirement_id_from_file(path)
    req = reqs.get(rid)
    rel = path.relative_to(PROGRAM_PY_DIR)
    stem = path.stem
    out_dir = output_root / rel.parent / stem
    out_dir.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    result: dict[str, Any] = {
        "requirement_id": rid,
        "program_file": str(path.relative_to(ROOT)).replace("\\", "/"),
        "output_dir": str(out_dir.relative_to(ROOT)).replace("\\", "/"),
        "status": "unknown",
        "compile_ok": False,
        "run_ok": False,
        "exports": {},
        "envelope_check": {"status": "not_checked"},
        "elapsed_sec": 0.0,
    }
    try:
        source = path.read_text(encoding="utf-8")
        compile(source, str(path), "exec")
        result["compile_ok"] = True
        part = load_part(path)
        result["run_ok"] = True

        bbox = get_bounding_box(part)
        result["bounding_box"] = bbox
        if req:
            result["envelope_check"] = envelope_check(req, bbox)

        plan = safe_process_plan(part)
        if plan is not None:
            plan_path = out_dir / "process_plan.json"
            plan_path.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
            result["exports"]["process_plan"] = str(plan_path.relative_to(ROOT)).replace("\\", "/")

        if export_step:
            step_path = out_dir / f"{stem}.step"
            part.to_step(str(step_path))
            result["exports"]["step"] = str(step_path.relative_to(ROOT)).replace("\\", "/")
        if export_stl:
            stl_path = out_dir / f"{stem}.stl"
            part.to_stl(str(stl_path))
            result["exports"]["stl"] = str(stl_path.relative_to(ROOT)).replace("\\", "/")

        result["status"] = "pass" if result["envelope_check"].get("status") in {"pass", "not_checked"} else "mismatch"
    except Exception as exc:  # noqa: BLE001 - corpus runner must keep going
        result["status"] = "error"
        result["error_type"] = type(exc).__name__
        result["error"] = str(exc)
        result["traceback"] = traceback.format_exc(limit=8)
    finally:
        result["elapsed_sec"] = round(time.perf_counter() - started, 3)
        (out_dir / "result.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


def write_summary(output_root: Path, results: list[dict[str, Any]]) -> None:
    counts: dict[str, int] = {}
    envelope_counts: dict[str, int] = {}
    for result in results:
        counts[result["status"]] = counts.get(result["status"], 0) + 1
        envelope_status = result.get("envelope_check", {}).get("status", "missing")
        envelope_counts[envelope_status] = envelope_counts.get(envelope_status, 0) + 1
    summary = {
        "total": len(results),
        "status_counts": dict(sorted(counts.items())),
        "envelope_counts": dict(sorted(envelope_counts.items())),
        "results": results,
    }
    output_root.mkdir(parents=True, exist_ok=True)
    (output_root / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    (output_root / "summary.jsonl").write_text(
        "".join(json.dumps(result, sort_keys=True) + "\n" for result in results),
        encoding="utf-8",
    )
    print(json.dumps({
        "total": len(results),
        "status_counts": summary["status_counts"],
        "envelope_counts": summary["envelope_counts"],
        "summary": str((output_root / "summary.json").relative_to(ROOT)).replace("\\", "/"),
    }, indent=2))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--limit", type=int, default=0, help="Run only the first N programs.")
    parser.add_argument("--pattern", default="agent_*/*.py", help="Glob under subcad_programs_py.")
    parser.add_argument("--no-step", action="store_true", help="Skip STEP export.")
    parser.add_argument("--no-stl", action="store_true", help="Skip STL export.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.output_dir.is_absolute():
        args.output_dir = ROOT / args.output_dir
    args.output_dir = args.output_dir.resolve()
    reqs = requirement_index()
    files = sorted(PROGRAM_PY_DIR.glob(args.pattern))
    if args.limit:
        files = files[: args.limit]
    results = [
        run_one(
            path,
            reqs,
            args.output_dir,
            export_step=not args.no_step,
            export_stl=not args.no_stl,
        )
        for path in files
    ]
    write_summary(args.output_dir, results)
    if any(result["status"] == "error" for result in results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
