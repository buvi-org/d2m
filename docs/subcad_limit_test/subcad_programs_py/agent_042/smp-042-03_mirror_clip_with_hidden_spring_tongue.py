# Requirement: SMP-042-03
# Source agent: 042
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_042_glass_handling_hardware_single_metal_parts.json
# Part: Mirror Clip With Hidden Spring Tongue - single metal part
# Raw idea: Mirror Clip With Hidden Spring Tongue
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 155 x 90 x 3 mm using steel_a36
# - two through mounting holes diameter 12 mm at X=18/137, Y=45
# - central obround through slot 51 x 15 mm at X=77, Y=45
# - centered top rectangular relief pocket 38 x 30 x 2 mm deep
# - end hook lip/undercut proxy: projection 17 mm, undercut 6 mm
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - Leave an integral hook lip on one short end, projecting 17 mm and undercut 6 mm for registration. A projecting integral hook lip is approximated by an end groove within the rectangular envelope.
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted by this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
# - Executable draft omits edge groove serration/hook proxies that caused invalid or envelope-shrinking geometry; those features remain requirement gaps for Stage 4 review.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.
# - Rectangular/sheet X/Y feature placement uses drill_at/slot_at/pocket_at datum offsets from the lower-left requirement origin where applicable.

from subcad import Stock

part = (
    Stock.rectangular(155, 90, 3, material="steel_a36")
    .drill_at(diameter=12, through=True, from_left=18, from_bottom=45, spot_drill=False)
    .drill_at(diameter=12, through=True, from_left=137, from_bottom=45, spot_drill=False)
    .slot_at(length=51, width=15, through=True, from_left=77, from_bottom=45)
    .pocket_at(width=30, length=38, depth=2, from_left=77, from_bottom=45)
)
