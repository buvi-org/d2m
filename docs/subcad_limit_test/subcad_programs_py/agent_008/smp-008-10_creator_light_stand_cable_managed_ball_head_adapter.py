# Requirement: SMP-008-10
# Source agent: 008
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_008_creator_rigging_hardware_single_metal_parts.json
# Part: Creator Light Stand Cable-Managed Ball Head Adapter - single metal part
# Raw idea: Creator Light Stand Cable-Managed Ball Head Adapter
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 85 x 80 x 67 mm using steel_a36
# - two through mounting holes diameter 5 mm at X=16/69, Y=40
# - central obround through slot 30 x 13 mm at X=42, Y=40
# - centered top rectangular relief pocket 25 x 26 x 19 mm deep
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
    Stock.rectangular(85, 80, 67, material="steel_a36")
    .drill_at(diameter=5, through=True, from_left=16, from_bottom=40, spot_drill=False)
    .drill_at(diameter=5, through=True, from_left=69, from_bottom=40, spot_drill=False)
    .slot_at(length=30, width=13, through=True, from_left=42, from_bottom=40)
    .pocket(width=26, length=25, depth=19, cx=0, cy=0)
    .threaded_hole(diameter=9, depth=40, cx=0, cy=20)
)
