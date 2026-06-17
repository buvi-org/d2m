# Requirement: SMP-039-25
# Source agent: 039
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_039_marine_service_hardware_single_metal_parts.json
# Part: Cockpit Drain Strainer Lift Tool - single metal part
# Raw idea: Cockpit Drain Strainer Lift Tool
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 150 x 110 x 33 mm in steel_a36.
# - Drilled two through mounting holes diameter 11 mm at requirement X=22 and X=128, Y=55 mm.
# - Machined central obround through slot 50 x 17 mm at requirement X=75, Y=55 mm.
# - Milled centered top relief pocket 37 x 36 x 1 mm deep.
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
    Stock.rectangular(150, 110, 33, material="steel_a36")
    .drill(diameter=11, depth=33, cx=-53, cy=0, through=True, spot_drill=False)
    .drill(diameter=11, depth=33, cx=53, cy=0, through=True, spot_drill=False)
    .slot(length=50, width=17, depth=33, cx=0, cy=0, through=True)
    .pocket(width=36, length=37, depth=1, cx=0, cy=0, corner_radius=0)
)
