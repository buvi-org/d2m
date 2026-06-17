# Requirement: SMP-022-03
# Source agent: 022
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_022_toys_hobby_mechanisms_single_metal_parts.json
# Part: Mini desktop cable car model - single metal part
# Raw idea: Mini desktop cable car model
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 165 x 100 x 5 mm.
# - Two through mounting holes diameter 8 mm at X=20 and X=145, Y=50.
# - Central through obround slot 55 x 10 mm at X=82, Y=50.
# - Top relief pocket 41 x 33 x 2 mm centered between mounting holes.
# - Top outside chamfers represented with 1 mm chamfer operation.
#
# Known gaps:
# - 0.5 mm chamfers on individual hole and slot mouths are not separately selectable in this draft; only the general top chamfer is modeled.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated directly from frozen Stage 2 requirement text; not executed or visually reviewed yet.
# - Coordinate conversion uses SubCAD centered stock coordinates while requirement text uses lower-left-near datum coordinates.

from subcad import Stock

part = (
    Stock.rectangular(165, 100, 5, material="steel_a36")
    .drill(diameter=8, through=True, cx=-62.5, cy=0, spot_drill=False)
    .drill(diameter=8, through=True, cx=62.5, cy=0, spot_drill=False)
    .slot(length=55, width=10, through=True, cx=-0.5, cy=0)
    .pocket(length=41, width=33, depth=2, cx=0, cy=0, corner_radius=0)
)
