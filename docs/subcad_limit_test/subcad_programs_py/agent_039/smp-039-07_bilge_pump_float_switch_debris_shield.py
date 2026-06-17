# Requirement: SMP-039-07
# Source agent: 039
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_039_marine_service_hardware_single_metal_parts.json
# Part: Bilge Pump Float Switch Debris Shield - single metal part
# Raw idea: Bilge Pump Float Switch Debris Shield
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 185 x 100 x 10 mm in steel_a36.
# - Drilled two through mounting holes diameter 7 mm at requirement X=20 and X=165, Y=50 mm.
# - Machined central obround through slot 61 x 17 mm at requirement X=92, Y=50 mm.
# - Milled centered top relief pocket 46 x 33 x 3 mm deep.
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
    Stock.rectangular(185, 100, 10, material="steel_a36")
    .drill(diameter=7, depth=10, cx=-72.5, cy=0, through=True, spot_drill=False)
    .drill(diameter=7, depth=10, cx=72.5, cy=0, through=True, spot_drill=False)
    .slot(length=61, width=17, depth=10, cx=-0.5, cy=0, through=True)
    .pocket(width=33, length=46, depth=3, cx=0, cy=0, corner_radius=0)
)
