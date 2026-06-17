# Requirement: SMP-010-03
# Source agent: 010
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_010_outdoor_marine_field_gear_single_metal_parts.json
# Part: Folding Camp Stove Pot Support Arm - single metal part
# Raw idea: Folding Camp Stove Pot Support Arm
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 140 x 75 x 55 mm with mapped material steel_a36.
# - Two through mounting holes dia 6 mm at X=15/125, Y=37.
# - Central through obround slot 46 x 11 mm at X=70, Y=37.
# - Top relief pocket 35 x 25 x 25 mm deep, centered between mounting holes.
# - 5 triangular rear-edge serrations, each 3 mm deep, represented by repeated triangular profile_cutout operations.
# - 1.0 mm top/outside chamfer represented with Stock.chamfer.
#
# Known gaps:
# - Serration profile_cutout placement needs execution review because the triangles lie on the rear edge boundary.
# - 0.5 mm chamfers on individual hole and slot mouths are not separately selectable in this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
# - Executable draft omits boundary triangular profile_cutout serration proxies because they erased the full solid in OCC; serrations remain a requirement gap for later targeted support.
#
# Review notes:
# - Coordinate conversion used Stock centered XY coordinates from the requirement lower-left origin.

from subcad import Stock

part = (
    Stock.rectangular(140, 75, 55, material="steel_a36")
    .drill(diameter=6, cx=-55, cy=-0.5, through=True)
    .drill(diameter=6, cx=55, cy=-0.5, through=True)
    .slot(length=46, width=11, cx=0, cy=-0.5, through=True)
    .pocket(width=25, length=35, depth=25, cx=0, cy=0)
)
