# Requirement: SMP-016-06
# Source agent: 016
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_016_packaging_machinery_single_metal_parts.json
# Part: Bottle anti-rotation clamp jaw for front-back labeling - single metal part
# Raw idea: Bottle anti-rotation clamp jaw for front-back labeling
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 120 x 35 x 16 mm with mapped material stainless_316.
# - Two through mounting holes dia 12 mm at X=10/110, Y=17.
# - Central through obround slot 40 x 13 mm at X=60, Y=17.
# - Top relief pocket 30 x 18 x 1 mm deep, centered between mounting holes.
# - Top dovetail groove length 96 mm, throat 12 mm, included angle 60 degrees.
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
    Stock.rectangular(120, 35, 16, material="stainless_316")
    .drill(diameter=12, cx=-50, cy=-0.5, through=True)
    .drill(diameter=12, cx=50, cy=-0.5, through=True)
    .slot(length=40, width=13, cx=0, cy=-0.5, through=True)
    .pocket(width=18, length=30, depth=1, cx=0, cy=0)
    .dovetail(length=96, width=12, depth=6, angle=60, cx=0, cy=0)
)
