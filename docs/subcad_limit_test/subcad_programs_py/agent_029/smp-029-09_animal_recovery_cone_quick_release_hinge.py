# Requirement: SMP-029-09
# Source agent: 029
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_029_pet_veterinary_hardware_single_metal_parts.json
# Part: Animal Recovery Cone Quick-Release Hinge - single metal part
# Raw idea: Animal Recovery Cone Quick-Release Hinge
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 215 x 110 x 6 mm using material steel_a36.
# - Drill two through holes diameter 7 mm on the length centerline at X=22 mm and X=193 mm, Y=55 mm.
# - Machine a central obround slot 71 mm long x 9 mm wide through the part, centered at X=107 mm, Y=55 mm.
# - Mill a rectangular relief pocket 53 mm x 36 mm x 1 mm deep on the top face, centered between the mounting holes.
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
    Stock.rectangular(215, 110, 6, material="steel_a36")
    .drill(diameter=7, cx=-85.5, cy=0, depth=6, through=True)
    .drill(diameter=7, cx=85.5, cy=0, depth=6, through=True)
    .slot(length=71, width=9, depth=6, cx=-0.5, cy=0)
    .pocket(width=36, length=53, depth=1, cx=0, cy=0, corner_radius=0.5)
)
