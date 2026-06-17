# Requirement: SMP-009-01
# Source agent: 009
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_009_furniture_architectural_hardware_single_metal_parts.json
# Part: Concealed Soft-Close Cabinet Hinge Cup - single metal part
# Raw idea: Concealed Soft-Close Cabinet Hinge Cup
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 215 x 70 x 54 mm using steel_a36
# - two through mounting holes diameter 11 mm at X=14/201, Y=35
# - central obround through slot 71 x 18 mm at X=107, Y=35
# - centered top rectangular relief pocket 53 x 23 x 14 mm deep
# - M4 side tapped hole intent included as threaded hole proxy
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
    Stock.rectangular(215, 70, 54, material="steel_a36")
    .drill_at(diameter=11, through=True, from_left=14, from_bottom=35, spot_drill=False)
    .drill_at(diameter=11, through=True, from_left=201, from_bottom=35, spot_drill=False)
    .slot_at(length=71, width=18, through=True, from_left=107, from_bottom=35)
    .pocket(width=23, length=53, depth=14, cx=0, cy=0)
    .threaded_hole(diameter=4, depth=35, cx=0, cy=17.5)
)
