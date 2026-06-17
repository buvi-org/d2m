# Requirement: SMP-019-03
# Source agent: 019
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_019_renewable_energy_hardware_single_metal_parts.json
# Part: Battery Rack Seismic Foot Anchor - single metal part
# Raw idea: Battery Rack Seismic Foot Anchor
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 180 x 130 x 9 mm.
# - Two through mounting holes diameter 10 mm at X=26 and X=154, Y=65.
# - Central through obround slot 60 x 17 mm at X=90, Y=65.
# - Top relief pocket 45 x 43 x 2 mm centered between mounting holes.
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
    Stock.rectangular(180, 130, 9, material="steel_a36")
    .drill(diameter=10, through=True, cx=-64, cy=0, spot_drill=False)
    .drill(diameter=10, through=True, cx=64, cy=0, spot_drill=False)
    .slot(length=60, width=17, through=True, cx=0, cy=0)
    .pocket(length=45, width=43, depth=2, cx=0, cy=0, corner_radius=0)
)
