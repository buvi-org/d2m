# Requirement: SMP-012-03
# Source agent: 012
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_012_agriculture_garden_hardware_single_metal_parts.json
# Part: Micro-Sprinkler Stake Head Adapter - single metal part
# Raw idea: Micro-Sprinkler Stake Head Adapter
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 155 x 75 x 57 mm with mapped material steel_1045.
# - Two through mounting holes dia 10 mm at X=15/140, Y=37.
# - Central through obround slot 51 x 16 mm at X=77, Y=37.
# - Top relief pocket 38 x 25 x 1 mm deep, centered between mounting holes.
# - Angled top reference face over last 31 mm using slope_cut at nominal 35 degree intent.
# - M4 tapped hole represented with threaded_hole near the right side/c. pocket region.
# - 1.0 mm top/outside chamfer represented with Stock.chamfer.
#
# Known gaps:
# - Angled reference face is represented as a sloped rectangular cut; exact external wedge/angle verification remains for Stage 4 review.
# - Side tapped hole axis parallel to Y is not represented exactly; program uses a top-face vertical threaded-hole proxy.
# - 0.5 mm chamfers on individual hole and slot mouths are not separately selectable in this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Coordinate conversion used Stock centered XY coordinates from the requirement lower-left origin.

from subcad import Stock

part = (
    Stock.rectangular(155, 75, 57, material="steel_1045")
    .drill(diameter=10, cx=-62.5, cy=-0.5, through=True)
    .drill(diameter=10, cx=62.5, cy=-0.5, through=True)
    .slot(length=51, width=16, cx=-0.5, cy=-0.5, through=True)
    .pocket(width=25, length=38, depth=1, cx=0, cy=0)
    .slope_cut(width=75, length=31, start_depth=0, end_depth=21.706, cx=62, cy=0, slope_axis="X")
    .threaded_hole(diameter=4, depth=37.5, cx=73.5, cy=0)
)
