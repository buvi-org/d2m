# Requirement: SMP-028-04
# Source agent: 028
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_028_small_engine_service_hardware_single_metal_parts.json
# Part: Portable Generator Exhaust Deflector Bracket - single metal part
# Raw idea: Portable Generator Exhaust Deflector Bracket
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 120 x 110 x 3 mm using material steel_1045.
# - Drill two through holes diameter 5 mm on the length centerline at X=22 mm and X=98 mm, Y=55 mm.
# - Machine a central obround slot 40 mm long x 18 mm wide through the part, centered at X=60 mm, Y=55 mm.
# - Mill a rectangular relief pocket 30 mm x 36 mm x 1 mm deep on the top face, centered between the mounting holes.
# - Applied a 1.0 mm top-edge chamfer operation.
# - Machine one top reference face at 36 degrees over the last 24 mm of length.
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
    Stock.rectangular(120, 110, 3, material="steel_1045")
    .drill(diameter=5, cx=-38, cy=0, depth=3, through=True)
    .drill(diameter=5, cx=38, cy=0, depth=3, through=True)
    .slot(length=40, width=18, depth=3, cx=0, cy=0)
    .pocket(width=36, length=30, depth=1, cx=0, cy=0, corner_radius=0.5)
    .slope_cut(width=110, length=24, start_depth=0, end_depth=2.4, cx=48, cy=0, slope_axis="X")
)
