"""Tests for SubCAD tube_profile geometry."""

import math

from src.subcad import Stock


passed = 0
failed = 0


def check(condition, label):
    global passed, failed
    if condition:
        passed += 1
        print(f"  PASS  {label}")
    else:
        failed += 1
        print(f"  FAIL  {label}")


print("SubCAD tube_profile tests")

outer = 10.0
inner = 5.0
length = 20.0
expected_volume = math.pi * ((outer / 2.0) ** 2 - (inner / 2.0) ** 2) * length

part = Stock.rectangular(1, 1, 1).tube_profile(
    {"diameter": outer, "axis": "X", "start": -10, "end": 10, "cy": 0, "cz": 0},
    {"diameter": inner},
    length,
    combine="replace",
)
check(abs(part.volume - expected_volume) / expected_volume < 0.01,
      f"X-axis tube volume matches annulus formula ({part.volume:.1f})")
op = part.process_plan()["operations"][-1]
check(op["operation"] == "tube_profile", "process plan records tube_profile")
check(op["axis"] == "X", "process plan records tube axis")
check(op["combine"] == "replace", "process plan records combine mode")

base = Stock.rectangular(20, 20, 8).machine_around_profile(
    {"length": 8, "width": 8},
    height=6,
    base_height=0,
)
with_tube = base.tube_profile(
    {"diameter": 6, "axis": "Y", "start": -12, "end": 12, "cx": 0, "cz": 2},
    {"diameter": 3},
    24,
)
check(with_tube.volume > base.volume, "union tube can add retained tube intent after base pad")
check(with_tube.process_plan()["total_operations"] == base.process_plan()["total_operations"] + 1,
      "tube operation preserves fluent chain")

outer_rect = {"type": "polygon", "points": [(-5, -3), (5, -3), (5, 3), (-5, 3)]}
inner_rect = {"type": "polygon", "points": [(-3, -1), (3, -1), (3, 1), (-3, 1)]}
profile_tube = Stock.rectangular(1, 1, 1).tube_profile(
    outer_rect,
    inner_rect,
    20,
    axis="X",
    combine="replace",
)
expected_profile_volume = ((10 * 6) - (6 * 2)) * 20
check(abs(profile_tube.volume - expected_profile_volume) < 1.0,
      f"profile tube volume matches polygon annulus ({profile_tube.volume:.1f})")
profile_op = profile_tube.process_plan()["operations"][-1]
check(profile_op["operation"] == "tube_profile", "profile tube records tube_profile operation")

print("\n" + "=" * 60)
if failed:
    print(f"FAILED: {failed} failed, {passed} passed")
    raise SystemExit(1)
print(f"ALL PASSED: {passed}/{passed} tests passed")
