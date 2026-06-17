# Requirement: SMP-039-11
# Source agent: 039
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_039_marine_service_hardware_single_metal_parts.json
# Part: Fuel Water Separator Bowl Wrench - single metal part
# Raw idea: Fuel Water Separator Bowl Wrench
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 170 x 100 x 59 mm in stainless_316.
# - Drilled two through mounting holes diameter 7 mm at requirement X=20 and X=150, Y=50 mm.
# - Machined central obround through slot 56 x 17 mm at requirement X=85, Y=50 mm.
# - Milled centered top relief pocket 42 x 33 x 6 mm deep.
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
    Stock.rectangular(170, 100, 59, material="stainless_316")
    .drill(diameter=7, depth=59, cx=-65, cy=0, through=True, spot_drill=False)
    .drill(diameter=7, depth=59, cx=65, cy=0, through=True, spot_drill=False)
    .slot(length=56, width=17, depth=59, cx=0, cy=0, through=True)
    .pocket(width=33, length=42, depth=6, cx=0, cy=0, corner_radius=0)
)
