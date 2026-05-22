"""Tests for side-face profile cutouts."""

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


print("SubCAD side profile cutout tests")

stock = Stock.rectangular(20, 10, 20)
triangle_xz = {"type": "polygon", "points": [(-10, -10), (-10, 10), (10, -10)]}
cut = stock.profile_cutout(triangle_xz, through=True, face_selector=">Y")

check(cut.volume < stock.volume, "side-face triangular cutout reduces volume")
check(abs(cut.volume - 2000.0) < 250.0, f"side-face cutout volume is plausible ({cut.volume:.1f})")
op = cut.process_plan()["operations"][-1]
check(op["operation"] == "profile_cutout", "process plan records profile_cutout")
check(op["face_selector"] == ">Y", "process plan preserves side face selector")

stock2 = Stock.rectangular(10, 20, 20)
triangle_yz = {"type": "polygon", "points": [(-10, -10), (10, -10), (10, 10)]}
cut2 = stock2.profile_cutout(triangle_yz, through=True, face_selector=">X")
check(cut2.volume < stock2.volume, "X-side triangular cutout reduces volume")
check(cut2.process_plan()["operations"][-1]["face_selector"] == ">X",
      "X-side process plan preserves face selector")

side_stock = Stock.rectangular(40, 20, 20).machine_around_cylinder(
    diameter=12, height=10, cx=0, cy=0, base_height=5
)
side_pocket = side_stock.circular_pocket(
    diameter=6, depth=4, cx=0, cy=10, face_selector=">Y"
)
check(side_pocket.volume < side_stock.volume, "side circular pocket fallback reduces volume")
check(side_pocket.process_plan()["operations"][-1]["face_selector"] == ">Y",
      "side circular pocket preserves face selector")

side_rect = side_stock.pocket(
    width=5, length=8, depth=3, cx=0, cy=10, face_selector=">Y"
)
check(side_rect.volume < side_stock.volume, "side rectangular pocket fallback reduces volume")
check(side_rect.process_plan()["operations"][-1]["face_selector"] == ">Y",
      "side rectangular pocket preserves face selector")

side_slot = side_stock.slot(
    width=4, length=14, depth=3, cx=0, cy=10, face_selector=">Y"
)
check(side_slot.volume < side_stock.volume, "side slot fallback reduces volume")
check(side_slot.process_plan()["operations"][-1]["face_selector"] == ">Y",
      "side slot preserves face selector")

print("\n" + "=" * 60)
if failed:
    print(f"FAILED: {failed} failed, {passed} passed")
    raise SystemExit(1)
print(f"ALL PASSED: {passed}/{passed} tests passed")
