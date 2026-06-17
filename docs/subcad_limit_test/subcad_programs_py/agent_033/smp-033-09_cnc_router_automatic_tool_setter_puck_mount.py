# Requirement: SMP-033-09
# Source agent: 033
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_033_woodworking_machines_single_metal_parts.json
# Part: CNC router automatic tool setter puck mount - single metal part
# Raw idea: CNC router automatic tool setter puck mount
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 100 x 90 x 22 mm using material steel_a36.
# - Drill two through holes diameter 7 mm on the length centerline at X=18 mm and X=82 mm, Y=45 mm.
# - Machine a central obround slot 33 mm long x 15 mm wide through the part, centered at X=50 mm, Y=45 mm.
# - Mill a rectangular relief pocket 25 mm x 30 mm x 6 mm deep on the top face, centered between the mounting holes.
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
    Stock.rectangular(100, 90, 22, material="steel_a36")
    .drill(diameter=7, cx=-32, cy=0, depth=22, through=True)
    .drill(diameter=7, cx=32, cy=0, depth=22, through=True)
    .slot(length=33, width=15, depth=22, cx=0, cy=0)
    .pocket(width=30, length=25, depth=6, cx=0, cy=0, corner_radius=0.5)
)
