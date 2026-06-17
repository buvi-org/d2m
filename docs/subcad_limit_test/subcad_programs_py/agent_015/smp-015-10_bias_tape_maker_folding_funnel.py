# Requirement: SMP-015-10
# Source agent: 015
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_015_textile_craft_machine_hardware_single_metal_parts.json
# Part: Bias Tape Maker Folding Funnel - single metal part
# Raw idea: Bias Tape Maker Folding Funnel
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 145 x 65 x 40 mm with mapped material steel_a36.
# - Two through mounting holes dia 10 mm at X=13/132, Y=32.
# - Central through obround slot 48 x 8 mm at X=72, Y=32.
# - Top relief pocket 36 x 21 x 20 mm deep, centered between mounting holes.
# - Angled top reference face over last 29 mm using slope_cut at nominal 20 degree intent.
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
    Stock.rectangular(145, 65, 40, material="steel_a36")
    .drill(diameter=10, cx=-59.5, cy=-0.5, through=True)
    .drill(diameter=10, cx=59.5, cy=-0.5, through=True)
    .slot(length=48, width=8, cx=-0.5, cy=-0.5, through=True)
    .pocket(width=21, length=36, depth=20, cx=0, cy=0)
    .slope_cut(width=65, length=29, start_depth=0, end_depth=10.555, cx=58, cy=0, slope_axis="X")
)
