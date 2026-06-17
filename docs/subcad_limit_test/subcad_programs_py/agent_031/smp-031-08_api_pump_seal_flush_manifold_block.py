# Requirement: SMP-031-08
# Source agent: 031
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_031_pumps_rotating_equipment_single_metal_parts.json
# Part: API Pump Seal Flush Manifold Block - single metal part
# Raw idea: API Pump Seal Flush Manifold Block
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 180 x 55 x 45 mm using material steel_a36.
# - Drill two through holes diameter 6 mm on the length centerline at X=11 mm and X=169 mm, Y=27 mm.
# - Machine a central obround slot 60 mm long x 17 mm wide through the part, centered at X=90 mm, Y=27 mm.
# - Mill a rectangular relief pocket 45 mm x 18 mm x 13 mm deep on the top face, centered between the mounting holes.
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
    Stock.rectangular(180, 55, 45, material="steel_a36")
    .drill(diameter=6, cx=-79, cy=-0.5, depth=45, through=True)
    .drill(diameter=6, cx=79, cy=-0.5, depth=45, through=True)
    .slot(length=60, width=17, depth=45, cx=0, cy=-0.5)
    .pocket(width=18, length=45, depth=13, cx=0, cy=0, corner_radius=0.5)
)
