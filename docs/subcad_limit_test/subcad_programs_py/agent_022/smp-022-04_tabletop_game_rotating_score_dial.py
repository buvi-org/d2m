# Requirement: SMP-022-04
# Source agent: 022
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_022_toys_hobby_mechanisms_single_metal_parts.json
# Part: Tabletop game rotating score dial - single metal part
# Raw idea: Tabletop game rotating score dial
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 230 x 145 x 5 mm.
# - Two through mounting holes diameter 7 mm at X=29 and X=201, Y=72.
# - Central through obround slot 76 x 7 mm at X=115, Y=72.
# - Top relief pocket 57 x 48 x 2 mm centered between mounting holes.
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
    Stock.rectangular(230, 145, 5, material="steel_a36")
    .drill(diameter=7, through=True, cx=-86, cy=-0.5, spot_drill=False)
    .drill(diameter=7, through=True, cx=86, cy=-0.5, spot_drill=False)
    .slot(length=76, width=7, through=True, cx=0, cy=-0.5)
    .pocket(length=57, width=48, depth=2, cx=0, cy=0, corner_radius=0)
)
