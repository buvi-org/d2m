# Requirement: SMP-042-16
# Source agent: 042
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_042_glass_handling_hardware_single_metal_parts.json
# Part: Mirror Backing Pad Locator - single metal part
# Raw idea: Mirror Backing Pad Locator
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 160 x 135 x 4 mm using steel_a36
# - two through mounting holes diameter 7 mm at X=27/133, Y=67
# - central obround through slot 53 x 10 mm at X=80, Y=67
# - centered top rectangular relief pocket 40 x 45 x 1 mm deep
# - end hook lip/undercut proxy: projection 13 mm, undercut 2 mm
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - Leave an integral hook lip on one short end, projecting 13 mm and undercut 2 mm for registration. A projecting integral hook lip is approximated by an end groove within the rectangular envelope.
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted by this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.
# - Rectangular/sheet X/Y feature placement uses drill_at/slot_at/pocket_at datum offsets from the lower-left requirement origin where applicable.

from subcad import Stock

part = (
    Stock.rectangular(160, 135, 4, material="steel_a36")
    .drill_at(diameter=7, through=True, from_left=27, from_bottom=67, spot_drill=False)
    .drill_at(diameter=7, through=True, from_left=133, from_bottom=67, spot_drill=False)
    .slot_at(length=53, width=10, through=True, from_left=80, from_bottom=67)
    .pocket_at(width=45, length=40, depth=1, from_left=80, from_bottom=67)
    .groove(length=13, width=135, depth=2, cx=-73.5, cy=0)
)
