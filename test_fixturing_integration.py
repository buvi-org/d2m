"""Integration test for SubCAD fixturing + multi-setup."""
import sys, os, json, tempfile
from src.subcad import Stock, FixtureCatalog
from src.subcad.geometry import _HAS_CADQUERY

if not _HAS_CADQUERY:
    print("SKIP: CadQuery not available")
    sys.exit(0)

passed = failed = 0
def check(label, cond, detail=""):
    global passed, failed
    if cond: passed += 1; print(f"  PASS  {label}")
    else: failed += 1; print(f"  FAIL  {label} -- {detail}")

print("=== Fixture/Setup Integration Test ===\n")

print("1. Multi-setup chain ...")
part = (Stock.rectangular(100, 50, 20, material="aluminum_6061")
    .with_fixture(FixtureCatalog.get("kurt_dx6_vise"))
    .new_setup("op1_top", face_selector=">Z", work_offset="G54")
    .face_mill(depth=1.0)
    .pocket(width=30, length=20, depth=5)
    .drill(diameter=6, cx=25, cy=10, depth=15)
)

plan = part.process_plan()
check("fixture in plan", plan.get("fixture") is not None)
check("fixture name", plan["fixture"]["name"] == "kurt_dx6_vise")
check("setups in plan", "setups" in plan)
check("1 setup", len(plan["setups"]) == 1)
check("setup has face_selector", plan["setups"]["op1_top"]["face_selector"] == ">Z")

ops = plan["operations"]
check("ops have setup key", all("setup" in o for o in ops))
check("ops have face_selector", all("face_selector" in o for o in ops))
check("all ops in op1_top", all(o.get("setup") == "op1_top" for o in ops))
print()

print("2. Multi-setup flip ...")
part2 = (Stock.rectangular(100, 50, 20, material="aluminum_6061")
    .with_fixture(FixtureCatalog.get("kurt_dx6_vise"))
    .new_setup("op1_top", face_selector=">Z", work_offset="G54")
    .face_mill(depth=1.0)
    .new_setup("op2_bottom", face_selector="<Z", work_offset="G55")
    .face_mill(depth=0.5)
)

plan2 = part2.process_plan()
check("2 setups", len(plan2["setups"]) == 2)
check("op1_top uses >Z", plan2["setups"]["op1_top"]["face_selector"] == ">Z")
check("op2_bottom uses <Z", plan2["setups"]["op2_bottom"]["face_selector"] == "<Z")
check("op2_bottom uses G55", plan2["setups"]["op2_bottom"]["work_offset"] == "G55")

ops2 = plan2["operations"]
check("first op in op1_top", ops2[0]["setup"] == "op1_top")
check("second op in op2_bottom", ops2[-1]["setup"] == "op2_bottom")
print()

print("3. Fixture clearance validation ...")
warnings = part.validate_fixture_clearance()
check("returns list", isinstance(warnings, list))
check("warns about face_mill", any("face_mill" in w for w in warnings))
print()

print("4. Plan JSON round-trip ...")
json_str = json.dumps(plan, indent=2)
reloaded = json.loads(json_str)
check("fixture survives round-trip", reloaded.get("fixture") is not None)
check("setups survive round-trip", len(reloaded.get("setups", {})) == 1)
print()

print("5. Error handling ...")
try:
    Stock.rectangular(50, 50, 10).new_setup("test")
    check("new_setup without fixture should raise", False)
except ValueError as e:
    check("raises ValueError", "No fixture" in str(e))

total = passed + failed
print(f"\n=== {'ALL PASSED' if failed == 0 else 'FAILURES'} ({passed}/{total}) ===")
sys.exit(0 if failed == 0 else 1)
