# Requirement: SMP-002-08
# Source agent: 002
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_002_mobility_hardware_single_metal_parts.json
# Part: Recumbent trike steering bellcrank - single metal part
# Raw idea: Recumbent trike steering bellcrank
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 180 x 100 x 51 mm using steel_a36
# - two through mounting holes diameter 9 mm at X=20/160, Y=50
# - central obround through slot 60 x 11 mm at X=90, Y=50
# - centered top rectangular relief pocket 45 x 33 x 23 mm deep
# - angled top reference face over last 36 mm using sloped-floor cut for 28 degree intent
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - angled reference face is represented as a sloped rectangular floor cut rather than a full exterior face reprofile
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.

from subcad import Stock

part = (
    Stock.rectangular(180, 100, 51, material="steel_a36")
    .drill_at(diameter=9, through=True, from_left=20, from_bottom=50, spot_drill=False)
    .drill_at(diameter=9, through=True, from_left=160, from_bottom=50, spot_drill=False)
    .slot_at(length=60, width=11, through=True, from_left=90, from_bottom=50)
    .pocket(width=33, length=45, depth=23, cx=0, cy=0)
    .slope_cut(width=100, length=36, start_depth=0, end_depth=19.142, cx=72, cy=0, slope_axis="X")
)
