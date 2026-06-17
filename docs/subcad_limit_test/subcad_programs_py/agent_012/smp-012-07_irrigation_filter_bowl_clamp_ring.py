# Requirement: SMP-012-07
# Source agent: 012
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_012_agriculture_garden_hardware_single_metal_parts.json
# Part: Irrigation Filter Bowl Clamp Ring - single metal part
# Raw idea: Irrigation Filter Bowl Clamp Ring
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 105 x 75 x 65 mm with mapped material steel_1045.
# - Two through mounting holes dia 8 mm at X=15/90, Y=37.
# - Central through obround slot 35 x 18 mm at X=52, Y=37.
# - Top relief pocket 26 x 25 x 21 mm deep, centered between mounting holes.
# - 1.0 mm top/outside chamfer represented with Stock.chamfer.
#
# Known gaps:
# - 0.5 mm chamfers on individual hole and slot mouths are not separately selectable in this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Coordinate conversion used Stock centered XY coordinates from the requirement lower-left origin.

from subcad import Stock

part = (
    Stock.rectangular(105, 75, 65, material="steel_1045")
    .drill(diameter=8, cx=-37.5, cy=-0.5, through=True)
    .drill(diameter=8, cx=37.5, cy=-0.5, through=True)
    .slot(length=35, width=18, cx=-0.5, cy=-0.5, through=True)
    .pocket(width=25, length=26, depth=21, cx=0, cy=0)
)
