# Requirement: SMP-025-05
# Source agent: 025
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_025_jewelry_watchmaking_fixtures_single_metal_parts.json
# Part: Micro Screw Slot Dressing Holder - single metal part
# Raw idea: Micro Screw Slot Dressing Holder
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 230 x 50 x 11 mm.
# - Two through mounting holes diameter 11 mm at X=10 and X=220, Y=25.
# - Central through obround slot 76 x 15 mm at X=115, Y=25.
# - Top relief pocket 57 x 18 x 1 mm centered between mounting holes.
# - Top outside chamfers represented with 1 mm chamfer operation.
# - Central counterbored seat diameter 23 mm x 3 mm deep around the center feature.
#
# Known gaps:
# - 0.5 mm chamfers on individual hole and slot mouths are not separately selectable in this draft; only the general top chamfer is modeled.
# - Side tapped hole M5 with axis parallel to Y is not modeled; current threaded_hole/tap operations are top-face axial in this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated directly from frozen Stage 2 requirement text; not executed or visually reviewed yet.
# - Coordinate conversion uses SubCAD centered stock coordinates while requirement text uses lower-left-near datum coordinates.

from subcad import Stock

part = (
    Stock.rectangular(230, 50, 11, material="aluminum_6061")
    .drill(diameter=11, through=True, cx=-105, cy=0, spot_drill=False)
    .drill(diameter=11, through=True, cx=105, cy=0, spot_drill=False)
    .slot(length=76, width=15, through=True, cx=0, cy=0)
    .pocket(length=57, width=18, depth=1, cx=0, cy=0, corner_radius=0)
    .circular_pocket(diameter=23, depth=3, cx=0, cy=0)
)
