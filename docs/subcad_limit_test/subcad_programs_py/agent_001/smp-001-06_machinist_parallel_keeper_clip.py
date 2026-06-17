# Requirement: SMP-001-06
# Source agent: 001
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_001_workshop_fixtures_single_metal_parts.json
# Part: Machinist Parallel Keeper Clip - single metal part
# Raw idea: Machinist Parallel Keeper Clip
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 130 x 50 x 11 mm using steel_1045
# - two through mounting holes diameter 11 mm at X=10/120, Y=25
# - central obround through slot 43 x 9 mm at X=65, Y=25
# - centered top rectangular relief pocket 32 x 18 x 1 mm deep
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
    Stock.rectangular(130, 50, 11, material="steel_1045")
    .drill_at(diameter=11, through=True, from_left=10, from_bottom=25, spot_drill=False)
    .drill_at(diameter=11, through=True, from_left=120, from_bottom=25, spot_drill=False)
    .slot_at(length=43, width=9, through=True, from_left=65, from_bottom=25)
    .pocket(width=18, length=32, depth=1, cx=0, cy=0)
    .groove(length=7, width=50, depth=3, cx=-61.5, cy=0)
)
