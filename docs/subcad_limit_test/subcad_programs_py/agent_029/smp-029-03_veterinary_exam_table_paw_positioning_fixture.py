# Requirement: SMP-029-03
# Source agent: 029
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_029_pet_veterinary_hardware_single_metal_parts.json
# Part: Veterinary Exam Table Paw Positioning Fixture - single metal part
# Raw idea: Veterinary Exam Table Paw Positioning Fixture
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 240 x 110 x 4 mm using material steel_a36.
# - Drill two through holes diameter 7 mm on the length centerline at X=22 mm and X=218 mm, Y=55 mm.
# - Machine a central obround slot 80 mm long x 16 mm wide through the part, centered at X=120 mm, Y=55 mm.
# - Mill a rectangular relief pocket 60 mm x 36 mm x 2 mm deep on the top face, centered between the mounting holes.
# - Applied a 1.0 mm top-edge chamfer operation.
# - Machine one top reference face at 26 degrees over the last 48 mm of length.
#
# Known gaps:
# - 0.5 mm chamfers specifically on individual hole and slot mouths are not separately modeled; only the global/top chamfer is included.
# - Angled reference face is approximated as a sloped top cut over the final length; exact edge transitions may need review.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - SubCAD stock is centered at the origin; requirement datum coordinates were converted from lower-left-near X/Y values to centered cx/cy values.

from subcad import Stock

part = (
    Stock.rectangular(240, 110, 4, material="steel_a36")
    .drill(diameter=7, cx=-98, cy=0, depth=4, through=True)
    .drill(diameter=7, cx=98, cy=0, depth=4, through=True)
    .slot(length=80, width=16, depth=4, cx=0, cy=0)
    .pocket(width=36, length=60, depth=2, cx=0, cy=0, corner_radius=0.5)
    .slope_cut(width=110, length=48, start_depth=0, end_depth=3.2, cx=96, cy=0, slope_axis="X")
)
