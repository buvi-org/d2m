# Requirement: SMP-039-06
# Source agent: 039
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_039_marine_service_hardware_single_metal_parts.json
# Part: Standing Rigging Tension Reference Gauge - single metal part
# Raw idea: Standing Rigging Tension Reference Gauge
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 110 x 40 x 24 mm in aluminum_6061.
# - Drilled two through mounting holes diameter 8 mm at requirement X=10 and X=100, Y=20 mm.
# - Machined central obround through slot 36 x 12 mm at requirement X=55, Y=20 mm.
# - Milled centered top relief pocket 27 x 18 x 3 mm deep.
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
    Stock.rectangular(110, 40, 24, material="aluminum_6061")
    .drill(diameter=8, depth=24, cx=-45, cy=0, through=True, spot_drill=False)
    .drill(diameter=8, depth=24, cx=45, cy=0, through=True, spot_drill=False)
    .slot(length=36, width=12, depth=24, cx=0, cy=0, through=True)
    .pocket(width=18, length=27, depth=3, cx=0, cy=0, corner_radius=0)
)
