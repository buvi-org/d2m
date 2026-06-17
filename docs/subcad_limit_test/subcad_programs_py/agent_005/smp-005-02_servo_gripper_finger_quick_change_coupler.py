# Requirement: SMP-005-02
# Source agent: 005
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_005_robotics_automation_single_metal_parts.json
# Part: Servo Gripper Finger Quick-Change Coupler - single metal part
# Raw idea: Servo Gripper Finger Quick-Change Coupler
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 155 x 85 x 27 mm using steel_a36
# - two through mounting holes diameter 10 mm at X=17/138, Y=42
# - central obround through slot 51 x 11 mm at X=77, Y=42
# - centered top rectangular relief pocket 38 x 28 x 11 mm deep
# - dovetail groove length 131 mm, throat 17 mm, included angle 60 degrees
# - M8 side tapped hole intent included as threaded hole proxy
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - side tapped hole axis parallel to Y is approximated by a top-face threaded hole because side-axis drilling is not directly expressed
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Dovetail depth was inferred because the requirement gives throat and angle but not groove depth.
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.

from subcad import Stock

part = (
    Stock.rectangular(155, 85, 27, material="steel_a36")
    .drill_at(diameter=10, through=True, from_left=17, from_bottom=42, spot_drill=False)
    .drill_at(diameter=10, through=True, from_left=138, from_bottom=42, spot_drill=False)
    .slot_at(length=51, width=11, through=True, from_left=77, from_bottom=42)
    .pocket(width=28, length=38, depth=11, cx=0, cy=0)
    .dovetail(length=131, width=17, depth=5.94, angle=60, cx=0, cy=0)
    .threaded_hole(diameter=8, depth=42.5, cx=0, cy=21.25)
)
