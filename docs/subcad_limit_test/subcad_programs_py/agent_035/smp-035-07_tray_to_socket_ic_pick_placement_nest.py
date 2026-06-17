# Requirement: SMP-035-07
# Source agent: 035
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_035_electronics_manufacturing_single_metal_parts.json
# Part: Tray-to-Socket IC Pick Placement Nest - single metal part
# Raw idea: Tray-to-Socket IC Pick Placement Nest
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 135 x 120 x 5 mm using material steel_a36.
# - Drill two through holes diameter 13 mm on the length centerline at X=24 mm and X=111 mm, Y=60 mm.
# - Machine a central obround slot 45 mm long x 12 mm wide through the part, centered at X=67 mm, Y=60 mm.
# - Mill a rectangular relief pocket 33 mm x 40 mm x 1 mm deep on the top face, centered between the mounting holes.
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
    Stock.rectangular(135, 120, 5, material="steel_a36")
    .drill(diameter=13, cx=-43.5, cy=0, depth=5, through=True)
    .drill(diameter=13, cx=43.5, cy=0, depth=5, through=True)
    .slot(length=45, width=12, depth=5, cx=-0.5, cy=0)
    .pocket(width=40, length=33, depth=1, cx=0, cy=0, corner_radius=0.5)
)
