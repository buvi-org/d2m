# Requirement: SMP-039-27
# Source agent: 039
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_039_marine_service_hardware_single_metal_parts.json
# Part: Dock Ladder Standoff Foot - single metal part
# Raw idea: Dock Ladder Standoff Foot
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 215 x 150 x 6 mm in steel_a36.
# - Drilled two through mounting holes diameter 10 mm at requirement X=30 and X=185, Y=75 mm.
# - Machined central obround through slot 71 x 18 mm at requirement X=107, Y=75 mm.
# - Milled centered top relief pocket 53 x 50 x 2 mm deep.
# - Applied 1.0 mm outside chamfer operation.
#
# Known gaps:
# - Separate 0.5 mm chamfers on hole and slot mouths are not individually represented; only the general chamfer operation is included.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft is syntactically generated but not executed; verify geometry against the frozen requirement in Stage 4.

from subcad import Stock

part = (
    Stock.rectangular(215, 150, 6, material="steel_a36")
    .drill(diameter=10, depth=6, cx=-77.5, cy=0, through=True, spot_drill=False)
    .drill(diameter=10, depth=6, cx=77.5, cy=0, through=True, spot_drill=False)
    .slot(length=71, width=18, depth=6, cx=-0.5, cy=0, through=True)
    .pocket(width=50, length=53, depth=2, cx=0, cy=0, corner_radius=0)
)
