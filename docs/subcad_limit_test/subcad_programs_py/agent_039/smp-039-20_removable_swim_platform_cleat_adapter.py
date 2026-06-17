# Requirement: SMP-039-20
# Source agent: 039
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_039_marine_service_hardware_single_metal_parts.json
# Part: Removable Swim Platform Cleat Adapter - single metal part
# Raw idea: Removable Swim Platform Cleat Adapter
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 90 x 70 x 29 mm in steel_a36.
# - Drilled two through mounting holes diameter 7 mm at requirement X=14 and X=76, Y=35 mm.
# - Machined central obround through slot 30 x 7 mm at requirement X=45, Y=35 mm.
# - Milled centered top relief pocket 25 x 23 x 8 mm deep.
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
    Stock.rectangular(90, 70, 29, material="steel_a36")
    .drill(diameter=7, depth=29, cx=-31, cy=0, through=True, spot_drill=False)
    .drill(diameter=7, depth=29, cx=31, cy=0, through=True, spot_drill=False)
    .slot(length=30, width=7, depth=29, cx=0, cy=0, through=True)
    .pocket(width=23, length=25, depth=8, cx=0, cy=0, corner_radius=0)
)
