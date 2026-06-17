# Requirement: SMP-019-05
# Source agent: 019
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_019_renewable_energy_hardware_single_metal_parts.json
# Part: Cable Tray Expansion Joint Slider - single metal part
# Raw idea: Cable Tray Expansion Joint Slider
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 100 x 90 x 9 mm.
# - Two through mounting holes diameter 10 mm at X=18 and X=82, Y=45.
# - Central through obround slot 33 x 16 mm at X=50, Y=45.
# - Top relief pocket 25 x 30 x 2 mm centered between mounting holes.
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
    Stock.rectangular(100, 90, 9, material="steel_a36")
    .drill(diameter=10, through=True, cx=-32, cy=0, spot_drill=False)
    .drill(diameter=10, through=True, cx=32, cy=0, spot_drill=False)
    .slot(length=33, width=16, through=True, cx=0, cy=0)
    .pocket(length=25, width=30, depth=2, cx=0, cy=0, corner_radius=0)
)
