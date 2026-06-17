# Requirement: SMP-010-10
# Source agent: 010
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_010_outdoor_marine_field_gear_single_metal_parts.json
# Part: Field Radio Mast Guyline Tensioner - single metal part
# Raw idea: Field Radio Mast Guyline Tensioner
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 135 x 90 x 8 mm with mapped material steel_a36.
# - Two through mounting holes dia 7 mm at X=18/117, Y=45.
# - Central through obround slot 45 x 11 mm at X=67, Y=45.
# - Top relief pocket 33 x 30 x 3 mm deep, centered between mounting holes.
# - Angled top reference face over last 27 mm using slope_cut at nominal 45 degree intent.
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
    Stock.rectangular(135, 90, 8, material="steel_a36")
    .drill(diameter=7, cx=-49.5, cy=0, through=True)
    .drill(diameter=7, cx=49.5, cy=0, through=True)
    .slot(length=45, width=11, cx=-0.5, cy=0, through=True)
    .pocket(width=30, length=33, depth=3, cx=0, cy=0)
    .slope_cut(width=90, length=27, start_depth=0, end_depth=8, cx=54, cy=0, slope_axis="X")
)
