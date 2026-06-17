# Requirement: SMP-015-05
# Source agent: 015
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_015_textile_craft_machine_hardware_single_metal_parts.json
# Part: Serger Looper Carrier Arm - single metal part
# Raw idea: Serger Looper Carrier Arm
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 195 x 75 x 40 mm with mapped material steel_a36.
# - Two through mounting holes dia 13 mm at X=15/180, Y=37.
# - Central through obround slot 65 x 11 mm at X=97, Y=37.
# - Top relief pocket 48 x 25 x 7 mm deep, centered between mounting holes.
# - Angled top reference face over last 39 mm using slope_cut at nominal 19 degree intent.
# - 1.0 mm top/outside chamfer represented with Stock.chamfer.
#
# Known gaps:
# - Angled reference face is represented as a sloped rectangular cut; exact external wedge/angle verification remains for Stage 4 review.
# - 0.5 mm chamfers on individual hole and slot mouths are not separately selectable in this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Coordinate conversion used Stock centered XY coordinates from the requirement lower-left origin.

from subcad import Stock

part = (
    Stock.rectangular(195, 75, 40, material="steel_a36")
    .drill(diameter=13, cx=-82.5, cy=-0.5, through=True)
    .drill(diameter=13, cx=82.5, cy=-0.5, through=True)
    .slot(length=65, width=11, cx=-0.5, cy=-0.5, through=True)
    .pocket(width=25, length=48, depth=7, cx=0, cy=0)
    .slope_cut(width=75, length=39, start_depth=0, end_depth=13.429, cx=78, cy=0, slope_axis="X")
)
