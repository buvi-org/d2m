# Requirement: SMP-008-02
# Source agent: 008
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_008_creator_rigging_hardware_single_metal_parts.json
# Part: Dual Cold-Shoe Audio Receiver Bridge - single metal part
# Raw idea: Dual Cold-Shoe Audio Receiver Bridge
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 195 x 115 x 38 mm using aluminum_6061
# - two through mounting holes diameter 5 mm at X=23/172, Y=57
# - central obround through slot 65 x 11 mm at X=97, Y=57
# - centered top rectangular relief pocket 48 x 38 x 1 mm deep
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.

from subcad import Stock

part = (
    Stock.rectangular(195, 115, 38, material="aluminum_6061")
    .drill_at(diameter=5, through=True, from_left=23, from_bottom=57, spot_drill=False)
    .drill_at(diameter=5, through=True, from_left=172, from_bottom=57, spot_drill=False)
    .slot_at(length=65, width=11, through=True, from_left=97, from_bottom=57)
    .pocket(width=38, length=48, depth=1, cx=0, cy=0)
)
