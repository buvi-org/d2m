# Requirement: SMP-035-01
# Source agent: 035
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_035_electronics_manufacturing_single_metal_parts.json
# Part: ESD-Safe Wafer Cassette Transfer Cradle - single metal part
# Raw idea: ESD-Safe Wafer Cassette Transfer Cradle
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 135 x 85 x 47 mm using material steel_a36.
# - Drill two through holes diameter 5 mm on the length centerline at X=17 mm and X=118 mm, Y=42 mm.
# - Machine a central obround slot 45 mm long x 12 mm wide through the part, centered at X=67 mm, Y=42 mm.
# - Mill a rectangular relief pocket 33 mm x 28 mm x 12 mm deep on the top face, centered between the mounting holes.
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
    Stock.rectangular(135, 85, 47, material="steel_a36")
    .drill(diameter=5, cx=-50.5, cy=-0.5, depth=47, through=True)
    .drill(diameter=5, cx=50.5, cy=-0.5, depth=47, through=True)
    .slot(length=45, width=12, depth=47, cx=-0.5, cy=-0.5)
    .pocket(width=28, length=33, depth=12, cx=0, cy=0, corner_radius=0.5)
)
