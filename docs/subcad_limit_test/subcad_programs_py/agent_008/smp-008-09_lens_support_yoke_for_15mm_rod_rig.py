# Requirement: SMP-008-09
# Source agent: 008
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_008_creator_rigging_hardware_single_metal_parts.json
# Part: Lens Support Yoke for 15mm Rod Rig - single metal part
# Raw idea: Lens Support Yoke for 15mm Rod Rig
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 80 x 60 x 68 mm using steel_a36
# - two through mounting holes diameter 12 mm at X=12/68, Y=30
# - central obround through slot 30 x 16 mm at X=40, Y=30
# - centered top rectangular relief pocket 25 x 20 x 11 mm deep
# - M9 side tapped hole intent included as threaded hole proxy
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - side tapped hole axis parallel to Y is approximated by a top-face threaded hole because side-axis drilling is not directly expressed
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.

from subcad import Stock

part = (
    Stock.rectangular(80, 60, 68, material="steel_a36")
    .drill_at(diameter=12, through=True, from_left=12, from_bottom=30, spot_drill=False)
    .drill_at(diameter=12, through=True, from_left=68, from_bottom=30, spot_drill=False)
    .slot_at(length=30, width=16, through=True, from_left=40, from_bottom=30)
    .pocket(width=20, length=25, depth=11, cx=0, cy=0)
    .threaded_hole(diameter=9, depth=30, cx=0, cy=15)
)
