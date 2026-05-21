"""Profile fidelity coverage for pure SubCAD profile operations."""

from src.subcad import Stock


def check(cond, label):
    if not cond:
        raise AssertionError(label)
    print(f"  PASS  {label}")


def pocket_volume(profile, depth=2.0):
    base = Stock.rectangular(80, 60, 20)
    return base.volume, base.profile_pocket(profile, depth).volume


print("1. Polygon and circle profiles cut their own footprint ...")
polygon = {
    "type": "polygon",
    "points": [(-12, -6), (8, -6), (14, 0), (8, 6), (-12, 6)],
}
base_volume, polygon_volume = pocket_volume(polygon, 3.0)
check(polygon_volume < base_volume, "polygon profile pocket removes material")

circle = {"type": "circle", "diameter": 16.0, "cx": 6.0, "cy": -4.0}
_, circle_volume = pocket_volume(circle, 3.0)
circle_rect = {"type": "rectangle", "length": 16.0, "width": 16.0, "cx": 6.0, "cy": -4.0}
_, circle_rect_volume = pocket_volume(circle_rect, 3.0)
check(circle_volume < base_volume, "circle profile pocket removes material")
check(circle_volume > circle_rect_volume, "circle profile is not degraded to its bounding rectangle")


print("\n2. Slot/obround profiles keep rounded ends ...")
slot = {"type": "slot", "length": 34.0, "width": 10.0}
_, slot_volume = pocket_volume(slot, 2.0)
slot_rect = {"type": "rectangle", "length": 34.0, "width": 10.0}
_, slot_rect_volume = pocket_volume(slot_rect, 2.0)
check(slot_volume < base_volume, "slot profile pocket removes material")
check(slot_volume > slot_rect_volume, "slot profile removes less than its bounding rectangle")

slot_plan = Stock.rectangular(80, 60, 20).profile_pocket(slot, 2.0).process_plan()
slot_op = slot_plan["operations"][-1]
check(slot_op["toolpath"]["metadata"]["width_mm"] == 10.0, "slot toolpath width uses normalized profile span")
check(slot_op["toolpath"]["metadata"]["length_mm"] == 34.0, "slot toolpath length uses normalized profile span")


print("\n3. Arc-chain profile approximations execute as real profile cuts ...")
arched_profile = {
    "type": "arc_chain",
    "segments": [
        {"point": (-10.0, -5.0)},
        {"end": (10.0, -5.0)},
        {"end": (10.0, 0.0)},
        {
            "type": "arc",
            "start": (10.0, 0.0),
            "end": (-10.0, 0.0),
            "center": (0.0, 0.0),
            "clockwise": False,
            "segments": 24,
        },
        {"end": (-10.0, -5.0)},
    ],
}
_, arched_volume = pocket_volume(arched_profile, 2.0)
arched_rect = {"type": "rectangle", "length": 20.0, "width": 15.0, "cy": 2.5}
_, arched_rect_volume = pocket_volume(arched_rect, 2.0)
check(arched_volume < base_volume, "arc-chain profile pocket removes material")
check(arched_volume > arched_rect_volume, "arc-chain profile is approximated rather than boxed")

arc_plan = Stock.rectangular(80, 60, 20).profile_pocket(arched_profile, 2.0).process_plan()
arc_op = arc_plan["operations"][-1]
check(arc_op["toolpath"]["metadata"]["width_mm"] > 14.9, "arc-chain path span includes arc height")
check(arc_op["toolpath"]["metadata"]["length_mm"] == 20.0, "arc-chain path span keeps endpoint length")


print("\n4. Cutout, contour, and retained-material operations accept normalized profiles ...")
base = Stock.rectangular(80, 60, 20)
check(base.profile_cutout(slot, depth=3.0).volume < base.volume, "profile_cutout executes slot profile")
check(base.profile_contour(arched_profile, 2.0).volume < base.volume, "profile_contour executes arc profile")
retained = base.machine_around_profile(slot, 2.0)
check(retained.volume < base.volume, "machine_around_profile removes material around slot")
rect_retained = base.machine_around_profile(slot_rect, 2.0)
check(retained.volume < rect_retained.volume, "retained slot island keeps rounded profile boundary")

print("\nALL PASSED")
