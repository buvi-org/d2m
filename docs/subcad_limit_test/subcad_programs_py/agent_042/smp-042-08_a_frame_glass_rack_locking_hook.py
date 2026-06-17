# Requirement: SMP-042-08
# Source agent: 042
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_042_glass_handling_hardware_single_metal_parts.json
# Part: A-Frame Glass Rack Locking Hook - single metal part
# Raw idea: A-Frame Glass Rack Locking Hook
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 110 x 65 x 37 mm using steel_a36
# - two through mounting holes diameter 5 mm at X=13/97, Y=32
# - central obround through slot 36 x 15 mm at X=55, Y=32
# - centered top rectangular relief pocket 27 x 21 x 14 mm deep
# - angled top reference face over last 22 mm using a sloped-floor cut for 35 degree intent
# - end hook lip/undercut proxy: projection 17 mm, undercut 5 mm
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - Angled reference face is represented as a sloped rectangular floor cut rather than a true exterior face reprofile.
# - Leave an integral hook lip on one short end, projecting 17 mm and undercut 5 mm for registration. A projecting integral hook lip is approximated by an end groove within the rectangular envelope.
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted by this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.
# - Rectangular/sheet X/Y feature placement uses drill_at/slot_at/pocket_at datum offsets from the lower-left requirement origin where applicable.

from subcad import Stock

part = (
    Stock.rectangular(110, 65, 37, material="steel_a36")
    .drill_at(diameter=5, through=True, from_left=13, from_bottom=32, spot_drill=False)
    .drill_at(diameter=5, through=True, from_left=97, from_bottom=32, spot_drill=False)
    .slot_at(length=36, width=15, through=True, from_left=55, from_bottom=32)
    .pocket_at(width=21, length=27, depth=14, from_left=55, from_bottom=32)
    .slope_cut(width=65, length=22, start_depth=0, end_depth=15.405, cx=44, cy=0, slope_axis="X")
    .groove(length=17, width=65, depth=5, cx=-46.5, cy=0)
)
