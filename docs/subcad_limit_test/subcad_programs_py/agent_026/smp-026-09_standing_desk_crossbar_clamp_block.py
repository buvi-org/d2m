# Requirement: SMP-026-09
# Source agent: 026
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_026_office_equipment_hardware_single_metal_parts.json
# Part: Standing Desk Crossbar Clamp Block - single metal part
# Raw idea: Standing Desk Crossbar Clamp Block
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 220 x 50 x 23 mm.
# - Two through mounting holes diameter 9 mm at X=10 and X=210, Y=25.
# - Central through obround slot 73 x 15 mm at X=110, Y=25.
# - Top relief pocket 55 x 18 x 7 mm centered between mounting holes.
# - Top outside chamfers represented with 1 mm chamfer operation.
#
# Known gaps:
# - 0.5 mm chamfers on individual hole and slot mouths are not separately selectable in this draft; only the general top chamfer is modeled.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated directly from frozen Stage 2 requirement text; not executed or visually reviewed yet.
# - Coordinate conversion uses SubCAD centered stock coordinates while requirement text uses lower-left-near datum coordinates.

from subcad import Stock

part = (
    Stock.rectangular(220, 50, 23, material="steel_1045")
    .drill(diameter=9, through=True, cx=-100, cy=0, spot_drill=False)
    .drill(diameter=9, through=True, cx=100, cy=0, spot_drill=False)
    .slot(length=73, width=15, through=True, cx=0, cy=0)
    .pocket(length=55, width=18, depth=7, cx=0, cy=0, corner_radius=0)
)
