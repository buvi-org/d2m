# Requirement: SMP-012-09
# Source agent: 012
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_012_agriculture_garden_hardware_single_metal_parts.json
# Part: Grafting Knife Folding Lock Bar - single metal part
# Raw idea: Grafting Knife Folding Lock Bar
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 120 x 90 x 32 mm with mapped material steel_a36.
# - Two through mounting holes dia 8 mm at X=18/102, Y=45.
# - Central through obround slot 40 x 17 mm at X=60, Y=45.
# - Top relief pocket 30 x 30 x 11 mm deep, centered between mounting holes.
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
    Stock.rectangular(120, 90, 32, material="steel_a36")
    .drill(diameter=8, cx=-42, cy=0, through=True)
    .drill(diameter=8, cx=42, cy=0, through=True)
    .slot(length=40, width=17, cx=0, cy=0, through=True)
    .pocket(width=30, length=30, depth=11, cx=0, cy=0)
)
