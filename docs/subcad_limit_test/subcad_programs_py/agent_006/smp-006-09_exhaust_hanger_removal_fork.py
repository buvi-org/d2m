# Requirement: SMP-006-09
# Source agent: 006
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_006_automotive_service_tools_single_metal_parts.json
# Part: Exhaust Hanger Removal Fork - single metal part
# Raw idea: Exhaust Hanger Removal Fork
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 190 x 85 x 24 mm using steel_1045
# - two through mounting holes diameter 10 mm at X=17/173, Y=42
# - central obround through slot 63 x 11 mm at X=95, Y=42
# - centered top rectangular relief pocket 47 x 28 x 6 mm deep
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
    Stock.rectangular(190, 85, 24, material="steel_1045")
    .drill_at(diameter=10, through=True, from_left=17, from_bottom=42, spot_drill=False)
    .drill_at(diameter=10, through=True, from_left=173, from_bottom=42, spot_drill=False)
    .slot_at(length=63, width=11, through=True, from_left=95, from_bottom=42)
    .pocket(width=28, length=47, depth=6, cx=0, cy=0)
)
