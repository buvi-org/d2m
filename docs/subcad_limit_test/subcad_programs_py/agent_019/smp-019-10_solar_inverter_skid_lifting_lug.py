# Requirement: SMP-019-10
# Source agent: 019
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_019_renewable_energy_hardware_single_metal_parts.json
# Part: Solar Inverter Skid Lifting Lug - single metal part
# Raw idea: Solar Inverter Skid Lifting Lug
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 150 x 60 x 35 mm.
# - Two through mounting holes diameter 10 mm at X=12 and X=138, Y=30.
# - Central through obround slot 50 x 8 mm at X=75, Y=30.
# - Top relief pocket 37 x 20 x 14 mm centered between mounting holes.
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
    Stock.rectangular(150, 60, 35, material="steel_a36")
    .drill(diameter=10, through=True, cx=-63, cy=0, spot_drill=False)
    .drill(diameter=10, through=True, cx=63, cy=0, spot_drill=False)
    .slot(length=50, width=8, through=True, cx=0, cy=0)
    .pocket(length=37, width=20, depth=14, cx=0, cy=0, corner_radius=0)
)
