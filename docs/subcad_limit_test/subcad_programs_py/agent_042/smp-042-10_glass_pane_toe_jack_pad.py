# Requirement: SMP-042-10
# Source agent: 042
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_042_glass_handling_hardware_single_metal_parts.json
# Part: Glass Pane Toe Jack Pad - single metal part
# Raw idea: Glass Pane Toe Jack Pad
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 190 x 110 x 49 mm using steel_a36
# - two through mounting holes diameter 9 mm at X=22/168, Y=55
# - central obround through slot 63 x 10 mm at X=95, Y=55
# - centered top rectangular relief pocket 47 x 36 x 7 mm deep
# - end hook lip/undercut proxy: projection 9 mm, undercut 6 mm
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - Leave an integral hook lip on one short end, projecting 9 mm and undercut 6 mm for registration. A projecting integral hook lip is approximated by an end groove within the rectangular envelope.
# - Tap one side hole M9 from the right long edge into the central pocket; hole axis is parallel to Y. SubCAD has no side-entry tapped-hole axis selection in the inspected Stock API, so this side hole is not modeled.
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted by this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.
# - Rectangular/sheet X/Y feature placement uses drill_at/slot_at/pocket_at datum offsets from the lower-left requirement origin where applicable.

from subcad import Stock

part = (
    Stock.rectangular(190, 110, 49, material="steel_a36")
    .drill_at(diameter=9, through=True, from_left=22, from_bottom=55, spot_drill=False)
    .drill_at(diameter=9, through=True, from_left=168, from_bottom=55, spot_drill=False)
    .slot_at(length=63, width=10, through=True, from_left=95, from_bottom=55)
    .pocket_at(width=36, length=47, depth=7, from_left=95, from_bottom=55)
    .groove(length=9, width=110, depth=6, cx=-90.5, cy=0)
)
