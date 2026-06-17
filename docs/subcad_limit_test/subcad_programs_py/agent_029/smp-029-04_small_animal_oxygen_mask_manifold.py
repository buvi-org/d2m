# Requirement: SMP-029-04
# Source agent: 029
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_029_pet_veterinary_hardware_single_metal_parts.json
# Part: Small Animal Oxygen Mask Manifold - single metal part
# Raw idea: Small Animal Oxygen Mask Manifold
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 110 x 85 x 46 mm using material steel_a36.
# - Drill two through holes diameter 6 mm on the length centerline at X=17 mm and X=93 mm, Y=42 mm.
# - Machine a central obround slot 36 mm long x 15 mm wide through the part, centered at X=55 mm, Y=42 mm.
# - Mill a rectangular relief pocket 27 mm x 28 mm x 6 mm deep on the top face, centered between the mounting holes.
# - Applied a 1.0 mm top-edge chamfer operation.
# - Added a threaded-hole placeholder at the central pocket location.
#
# Known gaps:
# - 0.5 mm chamfers specifically on individual hole and slot mouths are not separately modeled; only the global/top chamfer is included.
# - Tap one side hole M5 from the right long edge into the central pocket; hole axis is parallel to Y. Side-axis tapped holes from a long edge are not represented exactly by the top-face threaded_hole operation.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - SubCAD stock is centered at the origin; requirement datum coordinates were converted from lower-left-near X/Y values to centered cx/cy values.

from subcad import Stock

part = (
    Stock.rectangular(110, 85, 46, material="steel_a36")
    .drill(diameter=6, cx=-38, cy=-0.5, depth=46, through=True)
    .drill(diameter=6, cx=38, cy=-0.5, depth=46, through=True)
    .slot(length=36, width=15, depth=46, cx=0, cy=-0.5)
    .pocket(width=28, length=27, depth=6, cx=0, cy=0, corner_radius=0.5)
    .threaded_hole(diameter=5, depth=42.5, cx=0, cy=0)
)
