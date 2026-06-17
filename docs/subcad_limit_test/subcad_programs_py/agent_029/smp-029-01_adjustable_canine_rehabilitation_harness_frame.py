# Requirement: SMP-029-01
# Source agent: 029
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_029_pet_veterinary_hardware_single_metal_parts.json
# Part: Adjustable Canine Rehabilitation Harness Frame - single metal part
# Raw idea: Adjustable Canine Rehabilitation Harness Frame
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 180 x 110 x 26 mm using material steel_a36.
# - Drill two through holes diameter 12 mm on the length centerline at X=22 mm and X=158 mm, Y=55 mm.
# - Machine a central obround slot 60 mm long x 11 mm wide through the part, centered at X=90 mm, Y=55 mm.
# - Mill a rectangular relief pocket 45 mm x 36 mm x 9 mm deep on the top face, centered between the mounting holes.
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
    Stock.rectangular(180, 110, 26, material="steel_a36")
    .drill(diameter=12, cx=-68, cy=0, depth=26, through=True)
    .drill(diameter=12, cx=68, cy=0, depth=26, through=True)
    .slot(length=60, width=11, depth=26, cx=0, cy=0)
    .pocket(width=36, length=45, depth=9, cx=0, cy=0, corner_radius=0.5)
)
