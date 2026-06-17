# Requirement: SMP-031-03
# Source agent: 031
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_031_pumps_rotating_equipment_single_metal_parts.json
# Part: Flexible Spacer Coupling Guard With Inspection Windows - single metal part
# Raw idea: Flexible Spacer Coupling Guard With Inspection Windows
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 205 x 60 x 11 mm using material steel_a36.
# - Drill two through holes diameter 7 mm on the length centerline at X=12 mm and X=193 mm, Y=30 mm.
# - Machine a central obround slot 68 mm long x 16 mm wide through the part, centered at X=102 mm, Y=30 mm.
# - Mill a rectangular relief pocket 51 mm x 20 mm x 4 mm deep on the top face, centered between the mounting holes.
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
    Stock.rectangular(205, 60, 11, material="steel_a36")
    .drill(diameter=7, cx=-90.5, cy=0, depth=11, through=True)
    .drill(diameter=7, cx=90.5, cy=0, depth=11, through=True)
    .slot(length=68, width=16, depth=11, cx=-0.5, cy=0)
    .pocket(width=20, length=51, depth=4, cx=0, cy=0, corner_radius=0.5)
)
