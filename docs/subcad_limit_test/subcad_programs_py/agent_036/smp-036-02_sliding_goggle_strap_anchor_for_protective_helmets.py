# Requirement: SMP-036-02
# Source agent: 036
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_036_sports_safety_gear_single_metal_parts.json
# Part: Sliding goggle strap anchor for protective helmets - single metal part
# Raw idea: Sliding goggle strap anchor for protective helmets
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 215 x 65 x 7 mm using material steel_a36.
# - Drill two through holes diameter 8 mm on the length centerline at X=13 mm and X=202 mm, Y=32 mm.
# - Machine a central obround slot 71 mm long x 7 mm wide through the part, centered at X=107 mm, Y=32 mm.
# - Mill a rectangular relief pocket 53 mm x 21 mm x 2 mm deep on the top face, centered between the mounting holes.
# - Applied a 1.0 mm top-edge chamfer operation.
# - Added a short-end groove to indicate the hook-lip undercut region.
#
# Known gaps:
# - 0.5 mm chamfers specifically on individual hole and slot mouths are not separately modeled; only the global/top chamfer is included.
# - Leave an integral hook lip on one short end, projecting 8 mm and undercut 6 mm for registration. An integral projecting hook lip beyond/within the stock end is only approximated as a machined groove.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - SubCAD stock is centered at the origin; requirement datum coordinates were converted from lower-left-near X/Y values to centered cx/cy values.

from subcad import Stock

part = (
    Stock.rectangular(215, 65, 7, material="steel_a36")
    .drill(diameter=8, cx=-94.5, cy=-0.5, depth=7, through=True)
    .drill(diameter=8, cx=94.5, cy=-0.5, depth=7, through=True)
    .slot(length=71, width=7, depth=7, cx=-0.5, cy=-0.5)
    .pocket(width=21, length=53, depth=2, cx=0, cy=0, corner_radius=0.5)
    .groove(length=8, width=52, depth=6, cx=-103.5, cy=0)
)
