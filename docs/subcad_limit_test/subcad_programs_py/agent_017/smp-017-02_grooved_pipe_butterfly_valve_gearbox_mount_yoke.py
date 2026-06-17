# Requirement: SMP-017-02
# Source agent: 017
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_017_hvac_plumbing_hardware_single_metal_parts.json
# Part: Grooved Pipe Butterfly Valve Gearbox Mount Yoke - single metal part
# Raw idea: Grooved Pipe Butterfly Valve Gearbox Mount Yoke
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 215 x 60 x 39 mm with mapped material steel_a36.
# - Two through mounting holes dia 8 mm at X=12/203, Y=30.
# - Central through obround slot 71 x 15 mm at X=107, Y=30.
# - Top relief pocket 53 x 20 x 2 mm deep, centered between mounting holes.
# - 1.0 mm top/outside chamfer represented with Stock.chamfer.
#
# Known gaps:
# - 0.5 mm chamfers on individual hole and slot mouths are not separately selectable in this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Coordinate conversion used Stock centered XY coordinates from the requirement lower-left origin.

from subcad import Stock

part = (
    Stock.rectangular(215, 60, 39, material="steel_a36")
    .drill(diameter=8, cx=-95.5, cy=0, through=True)
    .drill(diameter=8, cx=95.5, cy=0, through=True)
    .slot(length=71, width=15, cx=-0.5, cy=0, through=True)
    .pocket(width=20, length=53, depth=2, cx=0, cy=0)
)
