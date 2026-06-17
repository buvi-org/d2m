# Requirement: SMP-035-05
# Source agent: 035
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_035_electronics_manufacturing_single_metal_parts.json
# Part: ESD-Safe Component Reel Inspection Stand - single metal part
# Raw idea: ESD-Safe Component Reel Inspection Stand
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 160 x 70 x 24 mm using material steel_a36.
# - Drill two through holes diameter 9 mm on the length centerline at X=14 mm and X=146 mm, Y=35 mm.
# - Machine a central obround slot 53 mm long x 7 mm wide through the part, centered at X=80 mm, Y=35 mm.
# - Mill a rectangular relief pocket 40 mm x 23 mm x 8 mm deep on the top face, centered between the mounting holes.
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
    Stock.rectangular(160, 70, 24, material="steel_a36")
    .drill(diameter=9, cx=-66, cy=0, depth=24, through=True)
    .drill(diameter=9, cx=66, cy=0, depth=24, through=True)
    .slot(length=53, width=7, depth=24, cx=0, cy=0)
    .pocket(width=23, length=40, depth=8, cx=0, cy=0, corner_radius=0.5)
)
