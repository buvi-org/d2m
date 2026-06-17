# Requirement: SMP-041-30
# Source agent: 041
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_041_apparel_production_fixtures_single_metal_parts.json
# Part: Apparel Work Ticket Clip Rail - single metal part
# Raw idea: Apparel Work Ticket Clip Rail
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 135 x 120 x 10 mm using steel_a36
# - two through mounting holes diameter 5 mm at X=24/111, Y=60
# - central obround through slot 45 x 10 mm at X=67, Y=60
# - centered top rectangular relief pocket 33 x 40 x 5 mm deep
# - angled top reference face over last 27 mm using a sloped-floor cut for 21 degree intent
# - end hook lip/undercut proxy: projection 16 mm, undercut 3 mm
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - Angled reference face is represented as a sloped rectangular floor cut rather than a true exterior face reprofile.
# - Computed 21 degree slope over 27 mm would remove 10.364 mm, exceeding the 10 mm stock height; draft clamps slope depth to 9.5 mm.
# - Leave an integral hook lip on one short end, projecting 16 mm and undercut 3 mm for registration. A projecting integral hook lip is approximated by an end groove within the rectangular envelope.
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted by this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.
# - Rectangular/sheet X/Y feature placement uses drill_at/slot_at/pocket_at datum offsets from the lower-left requirement origin where applicable.

from subcad import Stock

part = (
    Stock.rectangular(135, 120, 10, material="steel_a36")
    .drill_at(diameter=5, through=True, from_left=24, from_bottom=60, spot_drill=False)
    .drill_at(diameter=5, through=True, from_left=111, from_bottom=60, spot_drill=False)
    .slot_at(length=45, width=10, through=True, from_left=67, from_bottom=60)
    .pocket_at(width=40, length=33, depth=5, from_left=67, from_bottom=60)
    .slope_cut(width=120, length=27, start_depth=0, end_depth=9.5, cx=54, cy=0, slope_axis="X")
    .groove(length=16, width=120, depth=3, cx=-59.5, cy=0)
)
