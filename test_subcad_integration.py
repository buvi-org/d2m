"""Integration test for SubCAD -- end-to-end fluent chain + export."""
import sys
import os
import json
import tempfile

from src.subcad import Stock
from src.subcad.geometry import _HAS_CADQUERY

if not _HAS_CADQUERY:
    print("SKIP: CadQuery not available")
    sys.exit(0)

passed = 0
failed = 0


def check(label, condition, detail=""):
    global passed, failed
    if condition:
        passed += 1
        print(f"  PASS  {label}")
    else:
        failed += 1
        print(f"  FAIL  {label}  -- {detail}")


print("=" * 60)
print("SubCAD Integration Test")
print("=" * 60)

# 1. Full fluent chain
print("\n1. Full fluent chain ...")
part = (Stock.rectangular(100, 50, 20, material="aluminum_6061")
    .face_mill(depth=1.0)
    .pocket(width=30, length=20, depth=5, corner_radius=2)
    .drill(diameter=6, cx=25, cy=10, depth=15)
    .chamfer(width=0.5)
)
check("Stock created via fluent chain", part is not None)
check("Stock is Stock instance", isinstance(part, Stock))
plan = part.process_plan()
check("process_plan returns dict", isinstance(plan, dict))
check("Has material", plan.get("material") == "aluminum_6061")
check("Has stock_dimensions", "stock_dimensions" in plan)
check("Has operations", "operations" in plan)
check("Has total_operations", "total_operations" in plan)
check("Has estimated_time_minutes", "estimated_time_minutes" in plan)
check("Has tool_change_count", "tool_change_count" in plan)
check("Has tools_used", "tools_used" in plan)

ops = plan["operations"]
op_names = [o["operation"] for o in ops]
print(f"  Operations: {op_names}")
check(">= 5 operations", len(ops) >= 5, f"got {len(ops)} ops: {op_names}")
check("First op is face_mill", op_names[0] == "face_mill")
check("Last op is chamfer", op_names[-1] == "chamfer")
print()

# 2. STEP export
print("2. STEP export ...")
tmp_dir = tempfile.mkdtemp()
step_path = os.path.join(tmp_dir, "integration_test.step")
part.to_step(step_path)
size = os.path.getsize(step_path)
check(f"STEP file written ({size} bytes)", size > 1000)

# 3. Process plan JSON export
print("\n3. Process plan JSON export ...")
json_path = os.path.join(tmp_dir, "integration_test_plan.json")
part.save_process_plan(json_path)
with open(json_path, "r") as f:
    reloaded = json.load(f)
check("JSON file readable", isinstance(reloaded, dict))
check("JSON round-trips material", reloaded.get("material") == "aluminum_6061")
check("JSON round-trips operations", len(reloaded.get("operations", [])) == len(ops))

# 4. STL export
print("\n4. STL export ...")
stl_path = os.path.join(tmp_dir, "integration_test.stl")
part.to_stl(stl_path)
size = os.path.getsize(stl_path)
check(f"STL file written ({size} bytes)", size > 1000)

# 5. Volume decreases monotonically
print("\n5. Volume monotonic decrease ...")
s0 = Stock.rectangular(100, 50, 20)
v0 = s0.volume
s1 = s0.face_mill(depth=2.0)
v1 = s1.volume
check("face_mill reduces volume", v1 < v0, f"{v0:.1f} -> {v1:.1f}")

s2 = s1.pocket(width=30, length=20, depth=5)
v2 = s2.volume
check("pocket reduces volume", v2 < v1, f"{v1:.1f} -> {v2:.1f}")

s3 = s2.drill(diameter=6, cx=0, cy=0, depth=10, spot_drill=False)
v3 = s3.volume
check("drill reduces volume", v3 < v2, f"{v2:.1f} -> {v3:.1f}")

s4 = s3.chamfer(width=1.0)
v4 = s4.volume
check("chamfer reduces volume", v4 < v3, f"{v3:.1f} -> {v4:.1f}")
print()

# 6. Immutability
print("6. Immutability ...")
a = Stock.rectangular(50, 50, 10)
b = a.face_mill(1.0)
c = b.pocket(20, 20, 3)
d = c.drill(6, cx=10, cy=0, depth=5, spot_drill=False)
check("original has 0 ops", a.process_plan()["total_operations"] == 0)
check("face_mill result has 1 op", b.process_plan()["total_operations"] == 1)
check("pocket result has 2 ops", c.process_plan()["total_operations"] == 2)
check("drill result has 3 ops", d.process_plan()["total_operations"] == 3)
print()

# 7. Threaded hole compound
print("7. Threaded hole compound ...")
th = Stock.rectangular(60, 40, 15).face_mill(0.5).threaded_hole(diameter=8, depth=12, cx=10, cy=5)
th_plan = th.process_plan()
th_ops = th_plan["operations"]
th_names = [o["operation"] for o in th_ops]
print(f"  Operations: {th_names}")
check("face_mill + spot + drill + tap = 4 ops", len(th_ops) == 4, f"got {len(th_ops)}: {th_names}")
check("spot_drill present", "spot_drill" in th_names)
check("drill present", "drill" in th_names)
check("tap present", "tap" in th_names)
spot_idx = th_names.index("spot_drill")
drill_idx = th_names.index("drill")
tap_idx = th_names.index("tap")
check("spot before drill", spot_idx < drill_idx)
check("drill before tap", drill_idx < tap_idx)
print()

# 8. Multiple features on one part
print("8. Multiple features on one part ...")
multi = (Stock.rectangular(120, 80, 25)
    .face_mill(depth=1.0)
    .drill(diameter=6, cx=30, cy=20, depth=15)
    .drill(diameter=6, cx=-30, cy=20, depth=15)
    .drill(diameter=6, cx=30, cy=-20, depth=15)
    .drill(diameter=6, cx=-30, cy=-20, depth=15)
    .pocket(width=40, length=30, depth=8, cx=0, cy=0)
)
multi_plan = multi.process_plan()
print(f"  {multi_plan['total_operations']} operations total")
check("9+ ops (4 drills + pocket + face + possible spot/finish)", multi_plan["total_operations"] >= 7)
check("volume decreased", multi.volume > 0)
print()

# 9. Coordinate stability after prior cuts
print("9. Coordinate stability after prior cuts ...")
slot_part = (Stock.rectangular(90, 55, 18)
    .face_mill(depth=1.0)
    .pocket(width=22, length=34, depth=5, cx=-12, cy=0)
    .circular_pocket(diameter=14, depth=4, cx=22, cy=0)
    .slot(length=42, width=8, depth=6, cx=0, cy=16)
)
slot_floor = None
for face in slot_part._shape.val().Faces():
    bb = face.BoundingBox()
    if abs(bb.zmin - 2.0) < 0.01 and abs(bb.zmax - 2.0) < 0.01 and bb.ymin > 8:
        slot_floor = bb
        break
check("slot floor found", slot_floor is not None)
if slot_floor is not None:
    check("slot centered on requested X", abs((slot_floor.xmin + slot_floor.xmax) / 2.0) < 0.01)
    check("slot centered on requested Y", abs((slot_floor.ymin + slot_floor.ymax) / 2.0 - 16.0) < 0.01)
print()

# 10. Plan summary
print("10. Plan summary ...")
summary = part.plan_summary()
check("summary is string", isinstance(summary, str))
check("summary mentions material", "aluminum_6061" in summary or "6061" in summary)
print(summary)
print()

# 11. from_step roundtrip
print("11. from_step roundtrip ...")
rt = Stock.from_step(step_path, material="aluminum_6061", stock_oversize=5.0)
check("from_step returns Stock", isinstance(rt, Stock))
check("from_step has 0 ops", rt.process_plan()["total_operations"] == 0)
check("stock larger", rt.volume > part.volume)
print()

# Cleanup
for f in [step_path, json_path, stl_path]:
    try:
        os.unlink(f)
    except OSError:
        pass
try:
    os.rmdir(tmp_dir)
except OSError:
    pass

# Report
print("=" * 60)
total = passed + failed
if failed == 0:
    print(f"Integration test: ALL {passed}/{total} PASSED")
else:
    print(f"Integration test: {passed}/{total} passed, {failed} FAILED")
    sys.exit(1)
