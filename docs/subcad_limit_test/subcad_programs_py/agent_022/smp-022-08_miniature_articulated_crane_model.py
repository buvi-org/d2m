# Requirement: SMP-022-08
# Source agent: 022
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_022_toys_hobby_mechanisms_single_metal_parts.json
# Part: Miniature articulated crane model - single metal part
# Raw idea: Miniature articulated crane model
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 210 x 65 x 20 mm.
# - Two through mounting holes diameter 8 mm at X=13 and X=197, Y=32.
# - Central through obround slot 70 x 15 mm at X=105, Y=32.
# - Top relief pocket 52 x 21 x 1 mm centered between mounting holes.
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
    Stock.rectangular(210, 65, 20, material="steel_a36")
    .drill(diameter=8, through=True, cx=-92, cy=-0.5, spot_drill=False)
    .drill(diameter=8, through=True, cx=92, cy=-0.5, spot_drill=False)
    .slot(length=70, width=15, through=True, cx=0, cy=-0.5)
    .pocket(length=52, width=21, depth=1, cx=0, cy=0, corner_radius=0)
)
