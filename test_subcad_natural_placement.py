"""Tests for natural X/Y feature placement helpers."""
import sys

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


def _positions(part, operation):
    return [
        tuple(round(value, 6) for value in op["position"])
        for op in part.process_plan()["operations"]
        if op["operation"] == operation and op.get("position") is not None
    ]


def _same_positions(label, natural, explicit, operation):
    natural_positions = _positions(natural, operation)
    explicit_positions = _positions(explicit, operation)
    check(
        label,
        natural_positions == explicit_positions,
        f"{natural_positions} != {explicit_positions}",
    )


print("=" * 60)
print("SubCAD Natural Placement Test")
print("=" * 60)

print("\n1. Edge-offset drill placement ...")
natural = Stock.rectangular(120, 80, 6).drill_at(
    6,
    through=True,
    from_left=10,
    from_top=12,
    spot_drill=False,
)
explicit = Stock.rectangular(120, 80, 6).drill(
    6,
    through=True,
    cx=-50,
    cy=28,
    spot_drill=False,
)
_same_positions("edge-offset drill matches explicit cx/cy", natural, explicit, "drill")

print("\n2. Corner-hole inset pattern ...")
natural = Stock.rectangular(120, 80, 6).corner_holes(
    5,
    through=True,
    inset=10,
    spot_drill=False,
)
explicit = Stock.rectangular(120, 80, 6)
for cx, cy in [(-50, -30), (50, -30), (-50, 30), (50, 30)]:
    explicit = explicit.drill(5, through=True, cx=cx, cy=cy, spot_drill=False)
_same_positions("corner holes match explicit corner coordinates", natural, explicit, "drill")

print("\n3. Symmetric drilling ...")
natural = Stock.rectangular(120, 80, 6).drill_symmetric(
    4,
    through=True,
    from_left=15,
    from_top=20,
    mirror_x=True,
    mirror_y=True,
    spot_drill=False,
)
explicit = Stock.rectangular(120, 80, 6)
for cx, cy in [(-45, 20), (-45, -20), (45, 20), (45, -20)]:
    explicit = explicit.drill(4, through=True, cx=cx, cy=cy, spot_drill=False)
_same_positions("symmetric drilling expands to explicit mirrored coordinates", natural, explicit, "drill")

print("\n4. Rectangular drill pattern ...")
natural = Stock.rectangular(120, 80, 6).drill_pattern(
    3,
    through=True,
    rows=2,
    cols=3,
    spacing=(20, 30),
    center_x=5,
    center_y=-5,
    spot_drill=False,
)
explicit = Stock.rectangular(120, 80, 6)
for cy in [-20, 10]:
    for cx in [-15, 5, 25]:
        explicit = explicit.drill(3, through=True, cx=cx, cy=cy, spot_drill=False)
_same_positions("rectangular drill pattern matches explicit grid", natural, explicit, "drill")

print("\n5. Natural pocket, circular pocket, and slot placement ...")
natural = (
    Stock.rectangular(140, 90, 12)
    .pocket_at(18, 30, 3, from_left=35, center_y=True)
    .circular_pocket_at(12, 2, center_x=True, from_bottom=20)
    .slot_at(38, 6, 4, from_right=25, from_top=18, angle=90)
)
explicit = (
    Stock.rectangular(140, 90, 12)
    .pocket(18, 30, 3, cx=-35, cy=0)
    .circular_pocket(12, 2, cx=0, cy=-25)
    .slot(38, 6, 4, cx=45, cy=27, angle=90)
)
_same_positions("natural pocket position matches explicit", natural, explicit, "pocket")
_same_positions("natural circular pocket position matches explicit", natural, explicit, "circular_pocket")
_same_positions("natural slot position matches explicit", natural, explicit, "slot")

print("\n6. Ambiguous placement is rejected ...")
try:
    Stock.rectangular(40, 30, 5).resolve_xy(from_left=5, from_right=5, center_y=True)
    ambiguous_rejected = False
except ValueError:
    ambiguous_rejected = True
check("ambiguous X references rejected", ambiguous_rejected)

print("\n" + "=" * 60)
print(f"Passed: {passed}")
print(f"Failed: {failed}")
print("=" * 60)

if failed:
    sys.exit(1)
