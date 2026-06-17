# Requirement: SMP-026-04
# Source agent: 026
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_026_office_equipment_hardware_single_metal_parts.json
# Part: Office Chair Height Lever Bracket - single metal part
# Raw idea: Office Chair Height Lever Bracket
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 145 x 125 x 4 mm.
# - Two through mounting holes diameter 13 mm at X=25 and X=120, Y=62.
# - Central through obround slot 48 x 11 mm at X=72, Y=62.
# - Top relief pocket 36 x 41 x 2 mm centered between mounting holes.
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
    Stock.rectangular(145, 125, 4, material="steel_a36")
    .drill(diameter=13, through=True, cx=-47.5, cy=-0.5, spot_drill=False)
    .drill(diameter=13, through=True, cx=47.5, cy=-0.5, spot_drill=False)
    .slot(length=48, width=11, through=True, cx=-0.5, cy=-0.5)
    .pocket(length=36, width=41, depth=2, cx=0, cy=0, corner_radius=0)
)
