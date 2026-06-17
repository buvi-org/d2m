# Requirement: SMP-031-06
# Source agent: 031
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_031_pumps_rotating_equipment_single_metal_parts.json
# Part: Stuffing Box Lantern Ring Extraction Tool - single metal part
# Raw idea: Stuffing Box Lantern Ring Extraction Tool
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 155 x 50 x 45 mm using material steel_a36.
# - Drill two through holes diameter 12 mm on the length centerline at X=10 mm and X=145 mm, Y=25 mm.
# - Machine a central obround slot 51 mm long x 15 mm wide through the part, centered at X=77 mm, Y=25 mm.
# - Mill a rectangular relief pocket 38 mm x 18 mm x 9 mm deep on the top face, centered between the mounting holes.
# - Applied a 1.0 mm top-edge chamfer operation.
# - Added a short-end groove to indicate the hook-lip undercut region.
#
# Known gaps:
# - 0.5 mm chamfers specifically on individual hole and slot mouths are not separately modeled; only the global/top chamfer is included.
# - Leave an integral hook lip on one short end, projecting 14 mm and undercut 2 mm for registration. An integral projecting hook lip beyond/within the stock end is only approximated as a machined groove.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - SubCAD stock is centered at the origin; requirement datum coordinates were converted from lower-left-near X/Y values to centered cx/cy values.

from subcad import Stock

part = (
    Stock.rectangular(155, 50, 45, material="steel_a36")
    .drill(diameter=12, cx=-67.5, cy=0, depth=45, through=True)
    .drill(diameter=12, cx=67.5, cy=0, depth=45, through=True)
    .slot(length=51, width=15, depth=45, cx=-0.5, cy=0)
    .pocket(width=18, length=38, depth=9, cx=0, cy=0, corner_radius=0.5)
    .groove(length=14, width=40, depth=2, cx=-70.5, cy=0)
)
