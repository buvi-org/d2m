# Requirement: SMP-031-01
# Source agent: 031
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_031_pumps_rotating_equipment_single_metal_parts.json
# Part: Split Pump Bearing Housing With Sight Glass Bosses - single metal part
# Raw idea: Split Pump Bearing Housing With Sight Glass Bosses
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 90 x 85 x 42 mm using material steel_a36.
# - Drill two through holes diameter 10 mm on the length centerline at X=17 mm and X=73 mm, Y=42 mm.
# - Machine a central obround slot 30 mm long x 16 mm wide through the part, centered at X=45 mm, Y=42 mm.
# - Mill a rectangular relief pocket 25 mm x 28 mm x 19 mm deep on the top face, centered between the mounting holes.
# - Applied a 1.0 mm top-edge chamfer operation.
#
# Known gaps:
# - 0.5 mm chamfers specifically on individual hole and slot mouths are not separately modeled; only the global/top chamfer is included.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - SubCAD stock is centered at the origin; requirement datum coordinates were converted from lower-left-near X/Y values to centered cx/cy values.

from subcad import Stock

part = (
    Stock.rectangular(90, 85, 42, material="steel_a36")
    .drill(diameter=10, cx=-28, cy=-0.5, depth=42, through=True)
    .drill(diameter=10, cx=28, cy=-0.5, depth=42, through=True)
    .slot(length=30, width=16, depth=42, cx=0, cy=-0.5)
    .pocket(width=28, length=25, depth=19, cx=0, cy=0, corner_radius=0.5)
)
