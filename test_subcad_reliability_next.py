"""Acceptance tests for the next SubCAD reliability slice."""

from __future__ import annotations

import sys
import tempfile

from src.data.translator_benchmark import run_translation_benchmark
from src.subcad import FixtureCatalog, Stock, postprocess
from src.subcad.geometry import _HAS_CADQUERY
from src.subcad.postprocessor import NON_PRODUCTION_NOTICE
from src.subcad.validation import validate_all


if not _HAS_CADQUERY:
    print("SKIP: CadQuery not available")
    sys.exit(0)


passed = failed = 0


def check(label: str, condition: bool, detail: str = "") -> None:
    global passed, failed
    if condition:
        passed += 1
        print(f"  PASS  {label}")
    else:
        failed += 1
        print(f"  FAIL  {label} -- {detail}")


print("=" * 72)
print("SubCAD Reliability Next Acceptance Test")
print("=" * 72)

print("\n1. Target comparison API ...")
target = Stock.rectangular(40, 30, 12, material="aluminum_6061")
same = Stock.rectangular(40, 30, 12, material="aluminum_6061")
smaller = Stock.rectangular(38, 28, 10, material="aluminum_6061")
same_cmp = same.compare_to_target(target, tolerance_mm=0.25)
bad_cmp = smaller.compare_to_target(target, tolerance_mm=0.25)
check("same geometry passes", same_cmp["status"] in ("pass", "warning"), same_cmp)
check("different geometry fails", bad_cmp["status"] == "fail", bad_cmp)
check("comparison has overcut regions list", isinstance(bad_cmp["overcut_regions"], list))
check("comparison has undercut regions list", isinstance(bad_cmp["undercut_regions"], list))
check("comparison has feedback", isinstance(bad_cmp["feedback"], str))

with tempfile.NamedTemporaryFile(suffix=".step", delete=False) as fh:
    step_path = fh.name
target.to_step(step_path)
file_cmp = same.compare_to_target(step_path, tolerance_mm=0.25)
check("STEP target path accepted", file_cmp["status"] in ("pass", "warning"))

print("\n2. Shop-floor validation and setup grouping ...")
fixture = FixtureCatalog.get("kurt_dx6_vise")
part = (
    Stock.rectangular(100, 50, 20, material="aluminum_6061")
    .with_fixture(fixture)
    .new_setup("op1_top", face_selector=">Z", work_offset="G54")
    .face_mill(depth=1)
    .new_setup("op2_bottom", face_selector="<Z", work_offset="G55")
    .drill(diameter=6, cx=0, cy=0, depth=8)
)
report = part.validate_shop_floor(structured=True)
check("validate_shop_floor returns report", hasattr(report, "issues"))
sheet = part.setup_sheet()
check("setup sheet groups operations", "operations_by_setup" in sheet)
check("top setup grouped", "op1_top" in sheet["operations_by_setup"])
check("bottom setup grouped", "op2_bottom" in sheet["operations_by_setup"])

bad_plan = part.process_plan()
bad_plan["operations"][0]["setup"] = "missing_setup"
bad_plan["operations"][0]["face_selector"] = ">A"
bad_plan["operations"][0]["toolpath"] = {
    "moves": [{"type": "feed", "position": [60, 0, -1]}]
}
warnings = validate_all(bad_plan, bad_plan["stock_dimensions"])
text = "\n".join(warnings).lower()
check("unknown setup warned", "unknown setup" in text, text)
check("unsupported face warned", "unsupported face" in text, text)
check("fixture/toolpath clearance warned", "clamping zone" in text, text)

print("\n3. Debug postprocessor foundation ...")
program = part.postprocess()
check("postprocess emits text", isinstance(program, str) and len(program) > 0)
check("postprocess has warning", NON_PRODUCTION_NOTICE in program)
check("postprocess has units", "G21" in program)
try:
    postprocess(part.process_plan(), controller="linuxcnc")
    check("production controller rejected", False)
except ValueError:
    check("production controller rejected", True)

print("\n4. Translator benchmark bookkeeping ...")
payload = run_translation_benchmark(
    [
        {"sample_id": "ok", "cadquery_code": "part = cq.Workplane('XY').box(1,1,1)"},
        {"sample_id": "bad", "cadquery_code": "bad"},
    ],
    lambda sample: (
        {
            "success": True,
            "subcad_code": "part = Stock.rectangular(1,1,1)",
            "exec_result": {"volume": 1},
            "comparison": {"volume_ratio": 1.0},
            "attempts": 1,
        }
        if sample["sample_id"] == "ok"
        else {"success": False, "error": "syntax", "attempts": 2}
    ),
)
summary = payload["summary"]
check("benchmark records all samples", summary["total"] == 2)
check("benchmark pass rate", summary["pass_rate"] == 0.5)
check("benchmark stores generated code", payload["records"][0]["generated_subcad"].startswith("part"))
check("benchmark stores failures", payload["records"][1]["status"] == "error")

total = passed + failed
print("=" * 72)
print(f"Reliability next: {'ALL ' if failed == 0 else ''}{passed}/{total} PASSED")
sys.exit(0 if failed == 0 else 1)
