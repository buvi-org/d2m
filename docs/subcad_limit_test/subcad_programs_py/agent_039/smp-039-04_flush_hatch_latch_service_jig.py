# Requirement: SMP-039-04
# Source agent: 039
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_039_marine_service_hardware_single_metal_parts.json
# Part: Flush Hatch Latch Service Jig - single metal part
# Raw idea: Flush Hatch Latch Service Jig
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 120 x 105 x 57 mm in stainless_316.
# - Drilled two through mounting holes diameter 8 mm at requirement X=21 and X=99, Y=52 mm.
# - Machined central obround through slot 40 x 9 mm at requirement X=60, Y=52 mm.
# - Milled centered top relief pocket 30 x 35 x 1 mm deep.
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
    Stock.rectangular(120, 105, 57, material="stainless_316")
    .drill(diameter=8, depth=57, cx=-39, cy=-0.5, through=True, spot_drill=False)
    .drill(diameter=8, depth=57, cx=39, cy=-0.5, through=True, spot_drill=False)
    .slot(length=40, width=9, depth=57, cx=0, cy=-0.5, through=True)
    .pocket(width=35, length=30, depth=1, cx=0, cy=0, corner_radius=0)
)
