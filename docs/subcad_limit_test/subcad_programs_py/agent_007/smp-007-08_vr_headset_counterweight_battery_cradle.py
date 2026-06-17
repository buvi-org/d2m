# Requirement: SMP-007-08
# Source agent: 007
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_007_consumer_electronics_single_metal_parts.json
# Part: VR Headset Counterweight Battery Cradle - single metal part
# Raw idea: VR Headset Counterweight Battery Cradle
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 120 x 65 x 3 mm using steel_a36
# - two through mounting holes diameter 7 mm at X=13/107, Y=32
# - central obround through slot 40 x 12 mm at X=60, Y=32
# - centered top rectangular relief pocket 30 x 21 x 1 mm deep
# - end hook lip undercut proxy: projection 7 mm, undercut 3 mm
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
    Stock.rectangular(120, 65, 3, material="steel_a36")
    .drill_at(diameter=7, through=True, from_left=13, from_bottom=32, spot_drill=False)
    .drill_at(diameter=7, through=True, from_left=107, from_bottom=32, spot_drill=False)
    .slot_at(length=40, width=12, through=True, from_left=60, from_bottom=32)
    .pocket(width=21, length=30, depth=1, cx=0, cy=0)
    .groove(length=7, width=65, depth=3, cx=-56.5, cy=0)
)
