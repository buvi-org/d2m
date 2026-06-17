# Requirement: SMP-013-03
# Source agent: 013
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_013_aerospace_uav_hardware_single_metal_parts.json
# Part: Drone Battery Quick-Release Rail Saddle - single metal part
# Raw idea: Drone Battery Quick-Release Rail Saddle
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 150 x 110 x 40 mm with mapped material steel_a36.
# - Two through mounting holes dia 7 mm at X=22/128, Y=55.
# - Central through obround slot 50 x 7 mm at X=75, Y=55.
# - Top relief pocket 37 x 36 x 3 mm deep, centered between mounting holes.
# - Top dovetail groove length 126 mm, throat 22 mm, included angle 60 degrees.
# - Angled top reference face over last 30 mm using slope_cut at nominal 36 degree intent.
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
    Stock.rectangular(150, 110, 40, material="steel_a36")
    .drill(diameter=7, cx=-53, cy=0, through=True)
    .drill(diameter=7, cx=53, cy=0, through=True)
    .slot(length=50, width=7, cx=0, cy=0, through=True)
    .pocket(width=36, length=37, depth=3, cx=0, cy=0)
    .dovetail(length=126, width=22, depth=11, angle=60, cx=0, cy=0)
    .slope_cut(width=110, length=30, start_depth=0, end_depth=21.796, cx=60, cy=0, slope_axis="X")
)
