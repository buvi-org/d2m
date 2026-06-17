# Requirement: SMP-006-08
# Source agent: 006
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_006_automotive_service_tools_single_metal_parts.json
# Part: Fuel Injector Puller Bridge - single metal part
# Raw idea: Fuel Injector Puller Bridge
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 95 x 70 x 49 mm using steel_a36
# - two through mounting holes diameter 9 mm at X=14/81, Y=35
# - central obround through slot 31 x 12 mm at X=47, Y=35
# - centered top rectangular relief pocket 25 x 23 x 11 mm deep
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
    Stock.rectangular(95, 70, 49, material="steel_a36")
    .drill_at(diameter=9, through=True, from_left=14, from_bottom=35, spot_drill=False)
    .drill_at(diameter=9, through=True, from_left=81, from_bottom=35, spot_drill=False)
    .slot_at(length=31, width=12, through=True, from_left=47, from_bottom=35)
    .pocket(width=23, length=25, depth=11, cx=0, cy=0)
    .threaded_hole(diameter=9, depth=35, cx=0, cy=17.5)
)
