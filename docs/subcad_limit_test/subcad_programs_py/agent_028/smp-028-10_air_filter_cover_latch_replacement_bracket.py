# Requirement: SMP-028-10
# Source agent: 028
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_028_small_engine_service_hardware_single_metal_parts.json
# Part: Air Filter Cover Latch Replacement Bracket - single metal part
# Raw idea: Air Filter Cover Latch Replacement Bracket
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 105 x 105 x 3 mm using material steel_a36.
# - Drill two through holes diameter 13 mm on the length centerline at X=21 mm and X=84 mm, Y=52 mm.
# - Machine a central obround slot 35 mm long x 7 mm wide through the part, centered at X=52 mm, Y=52 mm.
# - Mill a rectangular relief pocket 26 mm x 35 mm x 1 mm deep on the top face, centered between the mounting holes.
# - Applied a 1.0 mm top-edge chamfer operation.
# - Added a short-end groove to indicate the hook-lip undercut region.
#
# Known gaps:
# - 0.5 mm chamfers specifically on individual hole and slot mouths are not separately modeled; only the global/top chamfer is included.
# - Leave an integral hook lip on one short end, projecting 6 mm and undercut 3 mm for registration. An integral projecting hook lip beyond/within the stock end is only approximated as a machined groove.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - SubCAD stock is centered at the origin; requirement datum coordinates were converted from lower-left-near X/Y values to centered cx/cy values.

from subcad import Stock

part = (
    Stock.rectangular(105, 105, 3, material="steel_a36")
    .drill(diameter=13, cx=-31.5, cy=-0.5, depth=3, through=True)
    .drill(diameter=13, cx=31.5, cy=-0.5, depth=3, through=True)
    .slot(length=35, width=7, depth=3, cx=-0.5, cy=-0.5)
    .pocket(width=35, length=26, depth=1, cx=0, cy=0, corner_radius=0.5)
    .groove(length=6, width=84, depth=3, cx=-49.5, cy=0)
)
