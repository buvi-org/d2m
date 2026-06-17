# Requirement: SMP-022-05
# Source agent: 022
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_022_toys_hobby_mechanisms_single_metal_parts.json
# Part: Hobby robot gripper claw - single metal part
# Raw idea: Hobby robot gripper claw
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 150 x 70 x 11 mm.
# - Two through mounting holes diameter 6 mm at X=14 and X=136, Y=35.
# - Central through obround slot 50 x 14 mm at X=75, Y=35.
# - Top relief pocket 37 x 23 x 4 mm centered between mounting holes.
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
    Stock.rectangular(150, 70, 11, material="aluminum_6061")
    .drill(diameter=6, through=True, cx=-61, cy=0, spot_drill=False)
    .drill(diameter=6, through=True, cx=61, cy=0, spot_drill=False)
    .slot(length=50, width=14, through=True, cx=0, cy=0)
    .pocket(length=37, width=23, depth=4, cx=0, cy=0, corner_radius=0)
)
