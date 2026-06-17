# Requirement: SMP-012-02
# Source agent: 012
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_012_agriculture_garden_hardware_single_metal_parts.json
# Part: Pruning Shear Blade Pivot Carrier - single metal part
# Raw idea: Pruning Shear Blade Pivot Carrier
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 145 x 70 x 46 mm with mapped material steel_a36.
# - Two through mounting holes dia 13 mm at X=14/131, Y=35.
# - Central through obround slot 48 x 17 mm at X=72, Y=35.
# - Top relief pocket 36 x 23 x 13 mm deep, centered between mounting holes.
# - Angled top reference face over last 29 mm using slope_cut at nominal 12 degree intent.
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
    Stock.rectangular(145, 70, 46, material="steel_a36")
    .drill(diameter=13, cx=-58.5, cy=0, through=True)
    .drill(diameter=13, cx=58.5, cy=0, through=True)
    .slot(length=48, width=17, cx=-0.5, cy=0, through=True)
    .pocket(width=23, length=36, depth=13, cx=0, cy=0)
    .slope_cut(width=70, length=29, start_depth=0, end_depth=6.164, cx=58, cy=0, slope_axis="X")
)
