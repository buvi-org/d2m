# Requirement: SMP-042-26
# Source agent: 042
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_042_glass_handling_hardware_single_metal_parts.json
# Part: Glass Edge Inspection Light Clip - single metal part
# Raw idea: Glass Edge Inspection Light Clip
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 135 x 50 x 3 mm using steel_a36
# - two through mounting holes diameter 7 mm at X=10/125, Y=25
# - central obround through slot 45 x 13 mm at X=67, Y=25
# - centered top rectangular relief pocket 33 x 18 x 2 mm deep
# - angled top reference face over last 27 mm using a sloped-floor cut for 27 degree intent
# - end hook lip/undercut proxy: projection 18 mm, undercut 2 mm
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - Angled reference face is represented as a sloped rectangular floor cut rather than a true exterior face reprofile.
# - Computed 27 degree slope over 27 mm would remove 13.757 mm, exceeding the 3 mm stock height; draft clamps slope depth to 2.5 mm.
# - Leave an integral hook lip on one short end, projecting 18 mm and undercut 2 mm for registration. A projecting integral hook lip is approximated by an end groove within the rectangular envelope.
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted by this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.
# - Rectangular/sheet X/Y feature placement uses drill_at/slot_at/pocket_at datum offsets from the lower-left requirement origin where applicable.

from subcad import Stock

part = (
    Stock.rectangular(135, 50, 3, material="steel_a36")
    .drill_at(diameter=7, through=True, from_left=10, from_bottom=25, spot_drill=False)
    .drill_at(diameter=7, through=True, from_left=125, from_bottom=25, spot_drill=False)
    .slot_at(length=45, width=13, through=True, from_left=67, from_bottom=25)
    .pocket_at(width=18, length=33, depth=2, from_left=67, from_bottom=25)
    .slope_cut(width=50, length=27, start_depth=0, end_depth=2.5, cx=54, cy=0, slope_axis="X")
    .groove(length=18, width=50, depth=2, cx=-58.5, cy=0)
)
