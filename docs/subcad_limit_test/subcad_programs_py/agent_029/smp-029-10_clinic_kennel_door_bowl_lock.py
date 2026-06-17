# Requirement: SMP-029-10
# Source agent: 029
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_029_pet_veterinary_hardware_single_metal_parts.json
# Part: Clinic Kennel Door Bowl Lock - single metal part
# Raw idea: Clinic Kennel Door Bowl Lock
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 210 x 70 x 4 mm using material stainless_316.
# - Drill two through holes diameter 7 mm on the length centerline at X=14 mm and X=196 mm, Y=35 mm.
# - Machine a central obround slot 70 mm long x 13 mm wide through the part, centered at X=105 mm, Y=35 mm.
# - Mill a rectangular relief pocket 52 mm x 23 mm x 1 mm deep on the top face, centered between the mounting holes.
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
    Stock.rectangular(210, 70, 4, material="stainless_316")
    .drill(diameter=7, cx=-91, cy=0, depth=4, through=True)
    .drill(diameter=7, cx=91, cy=0, depth=4, through=True)
    .slot(length=70, width=13, depth=4, cx=0, cy=0)
    .pocket(width=23, length=52, depth=1, cx=0, cy=0, corner_radius=0.5)
)
