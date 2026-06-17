# Requirement: SMP-035-10
# Source agent: 035
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_035_electronics_manufacturing_single_metal_parts.json
# Part: Thermal Interface Pad Placement Jig - single metal part
# Raw idea: Thermal Interface Pad Placement Jig
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 195 x 45 x 9 mm using material aluminum_6061.
# - Drill two through holes diameter 9 mm on the length centerline at X=10 mm and X=185 mm, Y=22 mm.
# - Machine a central obround slot 65 mm long x 18 mm wide through the part, centered at X=97 mm, Y=22 mm.
# - Mill a rectangular relief pocket 48 mm x 18 mm x 2 mm deep on the top face, centered between the mounting holes.
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
    Stock.rectangular(195, 45, 9, material="aluminum_6061")
    .drill(diameter=9, cx=-87.5, cy=-0.5, depth=9, through=True)
    .drill(diameter=9, cx=87.5, cy=-0.5, depth=9, through=True)
    .slot(length=65, width=18, depth=9, cx=-0.5, cy=-0.5)
    .pocket(width=18, length=48, depth=2, cx=0, cy=0, corner_radius=0.5)
)
