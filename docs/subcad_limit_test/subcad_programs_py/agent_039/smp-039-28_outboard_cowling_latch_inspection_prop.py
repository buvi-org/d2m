# Requirement: SMP-039-28
# Source agent: 039
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_039_marine_service_hardware_single_metal_parts.json
# Part: Outboard Cowling Latch Inspection Prop - single metal part
# Raw idea: Outboard Cowling Latch Inspection Prop
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 175 x 60 x 29 mm in steel_a36.
# - Drilled two through mounting holes diameter 11 mm at requirement X=12 and X=163, Y=30 mm.
# - Machined central obround through slot 58 x 9 mm at requirement X=87, Y=30 mm.
# - Milled centered top relief pocket 43 x 20 x 2 mm deep.
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
    Stock.rectangular(175, 60, 29, material="steel_a36")
    .drill(diameter=11, depth=29, cx=-75.5, cy=0, through=True, spot_drill=False)
    .drill(diameter=11, depth=29, cx=75.5, cy=0, through=True, spot_drill=False)
    .slot(length=58, width=9, depth=29, cx=-0.5, cy=0, through=True)
    .pocket(width=20, length=43, depth=2, cx=0, cy=0, corner_radius=0)
)
