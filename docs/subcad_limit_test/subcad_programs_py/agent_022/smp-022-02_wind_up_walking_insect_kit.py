# Requirement: SMP-022-02
# Source agent: 022
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_022_toys_hobby_mechanisms_single_metal_parts.json
# Part: Wind-up walking insect kit - single metal part
# Raw idea: Wind-up walking insect kit
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 175 x 40 x 39 mm.
# - Two through mounting holes diameter 8 mm at X=10 and X=165, Y=20.
# - Central through obround slot 58 x 16 mm at X=87, Y=20.
# - Top relief pocket 43 x 18 x 8 mm centered between mounting holes.
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
    Stock.rectangular(175, 40, 39, material="steel_a36")
    .drill(diameter=8, through=True, cx=-77.5, cy=0, spot_drill=False)
    .drill(diameter=8, through=True, cx=77.5, cy=0, spot_drill=False)
    .slot(length=58, width=16, through=True, cx=-0.5, cy=0)
    .pocket(length=43, width=18, depth=8, cx=0, cy=0, corner_radius=0)
)
