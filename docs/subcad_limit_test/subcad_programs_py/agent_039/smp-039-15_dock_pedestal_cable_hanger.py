# Requirement: SMP-039-15
# Source agent: 039
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_039_marine_service_hardware_single_metal_parts.json
# Part: Dock Pedestal Cable Hanger - single metal part
# Raw idea: Dock Pedestal Cable Hanger
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 120 x 100 x 54 mm in steel_a36.
# - Drilled two through mounting holes diameter 5 mm at requirement X=20 and X=100, Y=50 mm.
# - Machined central obround through slot 40 x 16 mm at requirement X=60, Y=50 mm.
# - Milled centered top relief pocket 30 x 33 x 23 mm deep.
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
    Stock.rectangular(120, 100, 54, material="steel_a36")
    .drill(diameter=5, depth=54, cx=-40, cy=0, through=True, spot_drill=False)
    .drill(diameter=5, depth=54, cx=40, cy=0, through=True, spot_drill=False)
    .slot(length=40, width=16, depth=54, cx=0, cy=0, through=True)
    .pocket(width=33, length=30, depth=23, cx=0, cy=0, corner_radius=0)
)
