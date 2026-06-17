# Requirement: SMP-016-03
# Source agent: 016
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_016_packaging_machinery_single_metal_parts.json
# Part: Nozzle centering cone for multi-head liquid filler - single metal part
# Raw idea: Nozzle centering cone for multi-head liquid filler
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 125 x 75 x 3 mm with mapped material steel_a36.
# - Two through mounting holes dia 13 mm at X=15/110, Y=37.
# - Central through obround slot 41 x 9 mm at X=62, Y=37.
# - Top relief pocket 31 x 25 x 1 mm deep, centered between mounting holes.
# - Angled top reference face over last 25 mm using slope_cut at nominal 21 degree intent.
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
    Stock.rectangular(125, 75, 3, material="steel_a36")
    .drill(diameter=13, cx=-47.5, cy=-0.5, through=True)
    .drill(diameter=13, cx=47.5, cy=-0.5, through=True)
    .slot(length=41, width=9, cx=-0.5, cy=-0.5, through=True)
    .pocket(width=25, length=31, depth=1, cx=0, cy=0)
    .slope_cut(width=75, length=25, start_depth=0, end_depth=3, cx=50, cy=0, slope_axis="X")
)
