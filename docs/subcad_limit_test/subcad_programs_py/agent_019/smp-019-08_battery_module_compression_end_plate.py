# Requirement: SMP-019-08
# Source agent: 019
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_019_renewable_energy_hardware_single_metal_parts.json
# Part: Battery Module Compression End Plate - single metal part
# Raw idea: Battery Module Compression End Plate
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 235 x 100 x 6 mm.
# - Two through mounting holes diameter 11 mm at X=20 and X=215, Y=50.
# - Central through obround slot 78 x 15 mm at X=117, Y=50.
# - Top relief pocket 58 x 33 x 3 mm centered between mounting holes.
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
    Stock.rectangular(235, 100, 6, material="steel_1045")
    .drill(diameter=11, through=True, cx=-97.5, cy=0, spot_drill=False)
    .drill(diameter=11, through=True, cx=97.5, cy=0, spot_drill=False)
    .slot(length=78, width=15, through=True, cx=-0.5, cy=0)
    .pocket(length=58, width=33, depth=3, cx=0, cy=0, corner_radius=0)
)
