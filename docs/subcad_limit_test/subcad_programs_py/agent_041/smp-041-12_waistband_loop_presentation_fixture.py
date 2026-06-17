# Requirement: SMP-041-12
# Source agent: 041
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_041_apparel_production_fixtures_single_metal_parts.json
# Part: Waistband Loop Presentation Fixture - single metal part
# Raw idea: Waistband Loop Presentation Fixture
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 250 x 100 x 6 mm using steel_a36
# - two through mounting holes diameter 8 mm at X=20/230, Y=50
# - central obround through slot 83 x 17 mm at X=125, Y=50
# - centered top rectangular relief pocket 62 x 33 x 2 mm deep
# - end hook lip/undercut proxy: projection 15 mm, undercut 4 mm
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - Leave an integral hook lip on one short end, projecting 15 mm and undercut 4 mm for registration. A projecting integral hook lip is approximated by an end groove within the rectangular envelope.
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted by this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.
# - Rectangular/sheet X/Y feature placement uses drill_at/slot_at/pocket_at datum offsets from the lower-left requirement origin where applicable.

from subcad import Stock

part = (
    Stock.rectangular(250, 100, 6, material="steel_a36")
    .drill_at(diameter=8, through=True, from_left=20, from_bottom=50, spot_drill=False)
    .drill_at(diameter=8, through=True, from_left=230, from_bottom=50, spot_drill=False)
    .slot_at(length=83, width=17, through=True, from_left=125, from_bottom=50)
    .pocket_at(width=33, length=62, depth=2, from_left=125, from_bottom=50)
    .groove(length=15, width=100, depth=4, cx=-117.5, cy=0)
)
