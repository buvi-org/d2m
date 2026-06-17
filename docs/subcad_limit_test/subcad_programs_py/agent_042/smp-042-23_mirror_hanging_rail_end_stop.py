# Requirement: SMP-042-23
# Source agent: 042
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_042_glass_handling_hardware_single_metal_parts.json
# Part: Mirror Hanging Rail End Stop - single metal part
# Raw idea: Mirror Hanging Rail End Stop
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 240 x 100 x 8 mm using steel_a36
# - two through mounting holes diameter 5 mm at X=20/220, Y=50
# - central obround through slot 80 x 11 mm at X=120, Y=50
# - centered top rectangular relief pocket 60 x 33 x 1 mm deep
# - end hook lip/undercut proxy: projection 7 mm, undercut 2 mm
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - Leave an integral hook lip on one short end, projecting 7 mm and undercut 2 mm for registration. A projecting integral hook lip is approximated by an end groove within the rectangular envelope.
# - Tap one side hole M8 from the right long edge into the central pocket; hole axis is parallel to Y. SubCAD has no side-entry tapped-hole axis selection in the inspected Stock API, so this side hole is not modeled.
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted by this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.
# - Rectangular/sheet X/Y feature placement uses drill_at/slot_at/pocket_at datum offsets from the lower-left requirement origin where applicable.

from subcad import Stock

part = (
    Stock.rectangular(240, 100, 8, material="steel_a36")
    .drill_at(diameter=5, through=True, from_left=20, from_bottom=50, spot_drill=False)
    .drill_at(diameter=5, through=True, from_left=220, from_bottom=50, spot_drill=False)
    .slot_at(length=80, width=11, through=True, from_left=120, from_bottom=50)
    .pocket_at(width=33, length=60, depth=1, from_left=120, from_bottom=50)
    .groove(length=7, width=100, depth=2, cx=-116.5, cy=0)
)
