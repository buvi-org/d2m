# Requirement: SMP-029-08
# Source agent: 029
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_029_pet_veterinary_hardware_single_metal_parts.json
# Part: Pet Bath Spray Nozzle Wall Dock - single metal part
# Raw idea: Pet Bath Spray Nozzle Wall Dock
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 235 x 50 x 4 mm using material steel_a36.
# - Drill two through holes diameter 9 mm on the length centerline at X=10 mm and X=225 mm, Y=25 mm.
# - Machine a central obround slot 78 mm long x 17 mm wide through the part, centered at X=117 mm, Y=25 mm.
# - Mill a rectangular relief pocket 58 mm x 18 mm x 1 mm deep on the top face, centered between the mounting holes.
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
    Stock.rectangular(235, 50, 4, material="steel_a36")
    .drill(diameter=9, cx=-107.5, cy=0, depth=4, through=True)
    .drill(diameter=9, cx=107.5, cy=0, depth=4, through=True)
    .slot(length=78, width=17, depth=4, cx=-0.5, cy=0)
    .pocket(width=18, length=58, depth=1, cx=0, cy=0, corner_radius=0.5)
)
