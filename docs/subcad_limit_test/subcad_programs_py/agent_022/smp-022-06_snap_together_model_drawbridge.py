# Requirement: SMP-022-06
# Source agent: 022
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_022_toys_hobby_mechanisms_single_metal_parts.json
# Part: Snap-together model drawbridge - single metal part
# Raw idea: Snap-together model drawbridge
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 155 x 75 x 52 mm.
# - Two through mounting holes diameter 8 mm at X=15 and X=140, Y=37.
# - Central through obround slot 51 x 18 mm at X=77, Y=37.
# - Top relief pocket 38 x 25 x 16 mm centered between mounting holes.
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
    Stock.rectangular(155, 75, 52, material="steel_a36")
    .drill(diameter=8, through=True, cx=-62.5, cy=-0.5, spot_drill=False)
    .drill(diameter=8, through=True, cx=62.5, cy=-0.5, spot_drill=False)
    .slot(length=51, width=18, through=True, cx=-0.5, cy=-0.5)
    .pocket(length=38, width=25, depth=16, cx=0, cy=0, corner_radius=0)
)
