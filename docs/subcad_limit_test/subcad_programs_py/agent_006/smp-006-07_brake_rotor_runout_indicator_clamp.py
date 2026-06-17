# Requirement: SMP-006-07
# Source agent: 006
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_006_automotive_service_tools_single_metal_parts.json
# Part: Brake Rotor Runout Indicator Clamp - single metal part
# Raw idea: Brake Rotor Runout Indicator Clamp
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 200 x 85 x 17 mm using steel_1045
# - two through mounting holes diameter 8 mm at X=17/183, Y=42
# - central obround through slot 66 x 18 mm at X=100, Y=42
# - centered top rectangular relief pocket 50 x 28 x 7 mm deep
# - full-length centered groove mouth 42 mm and depth 5 mm
# - M4 side tapped hole intent included as threaded hole proxy
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - 90 degree V-groove is approximated by the available rectangular groove operation
# - side tapped hole axis parallel to Y is approximated by a top-face threaded hole because side-axis drilling is not directly expressed
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.

from subcad import Stock

part = (
    Stock.rectangular(200, 85, 17, material="steel_1045")
    .drill_at(diameter=8, through=True, from_left=17, from_bottom=42, spot_drill=False)
    .drill_at(diameter=8, through=True, from_left=183, from_bottom=42, spot_drill=False)
    .slot_at(length=66, width=18, through=True, from_left=100, from_bottom=42)
    .pocket(width=28, length=50, depth=7, cx=0, cy=0)
    .groove(length=200, width=42, depth=5, cx=0, cy=0)
    .threaded_hole(diameter=4, depth=42.5, cx=0, cy=21.25)
)
