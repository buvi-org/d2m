# Requirement: SMP-042-05
# Source agent: 042
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_042_glass_handling_hardware_single_metal_parts.json
# Part: Window Sash Alignment Spacer Comb - single metal part
# Raw idea: Window Sash Alignment Spacer Comb
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 180 x 45 x 41 mm using steel_a36
# - two through mounting holes diameter 5 mm at X=10/170, Y=22
# - central obround through slot 60 x 9 mm at X=90, Y=22
# - centered top rectangular relief pocket 45 x 18 x 2 mm deep
# - 10 rear-edge serration positions with 3 mm depth intent
# - angled top reference face over last 36 mm using a sloped-floor cut for 41 degree intent
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - Triangular serration tooth form is approximated by repeated rectangular groove cuts.
# - Angled reference face is represented as a sloped rectangular floor cut rather than a true exterior face reprofile.
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted by this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.
# - Rectangular/sheet X/Y feature placement uses drill_at/slot_at/pocket_at datum offsets from the lower-left requirement origin where applicable.

from subcad import Stock

part = (
    Stock.rectangular(180, 45, 41, material="steel_a36")
    .drill_at(diameter=5, through=True, from_left=10, from_bottom=22, spot_drill=False)
    .drill_at(diameter=5, through=True, from_left=170, from_bottom=22, spot_drill=False)
    .slot_at(length=60, width=9, through=True, from_left=90, from_bottom=22)
    .pocket_at(width=18, length=45, depth=2, from_left=90, from_bottom=22)
    .groove(length=3, width=2.925, depth=3, cx=-88.5, cy=-20.25, angle=90)
    .groove(length=3, width=2.925, depth=3, cx=-88.5, cy=-15.75, angle=90)
    .groove(length=3, width=2.925, depth=3, cx=-88.5, cy=-11.25, angle=90)
    .groove(length=3, width=2.925, depth=3, cx=-88.5, cy=-6.75, angle=90)
    .groove(length=3, width=2.925, depth=3, cx=-88.5, cy=-2.25, angle=90)
    .groove(length=3, width=2.925, depth=3, cx=-88.5, cy=2.25, angle=90)
    .groove(length=3, width=2.925, depth=3, cx=-88.5, cy=6.75, angle=90)
    .groove(length=3, width=2.925, depth=3, cx=-88.5, cy=11.25, angle=90)
    .groove(length=3, width=2.925, depth=3, cx=-88.5, cy=15.75, angle=90)
    .groove(length=3, width=2.925, depth=3, cx=-88.5, cy=20.25, angle=90)
    .slope_cut(width=45, length=36, start_depth=0, end_depth=31.294, cx=72, cy=0, slope_axis="X")
)
