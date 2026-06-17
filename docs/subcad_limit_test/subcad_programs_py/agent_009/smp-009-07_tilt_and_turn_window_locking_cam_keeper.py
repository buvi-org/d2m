# Requirement: SMP-009-07
# Source agent: 009
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_009_furniture_architectural_hardware_single_metal_parts.json
# Part: Tilt-and-Turn Window Locking Cam Keeper - single metal part
# Raw idea: Tilt-and-Turn Window Locking Cam Keeper
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 205 x 70 x 62 mm using steel_a36
# - two through mounting holes diameter 5 mm at X=14/191, Y=35
# - central obround through slot 68 x 12 mm at X=102, Y=35
# - centered top rectangular relief pocket 51 x 23 x 3 mm deep
# - end hook lip undercut proxy: projection 13 mm, undercut 2 mm
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - integral projecting hook lip is approximated by an end undercut within the rectangular envelope
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.

from subcad import Stock

part = (
    Stock.rectangular(205, 70, 62, material="steel_a36")
    .drill_at(diameter=5, through=True, from_left=14, from_bottom=35, spot_drill=False)
    .drill_at(diameter=5, through=True, from_left=191, from_bottom=35, spot_drill=False)
    .slot_at(length=68, width=12, through=True, from_left=102, from_bottom=35)
    .pocket(width=23, length=51, depth=3, cx=0, cy=0)
    .groove(length=13, width=70, depth=2, cx=-96, cy=0)
)
