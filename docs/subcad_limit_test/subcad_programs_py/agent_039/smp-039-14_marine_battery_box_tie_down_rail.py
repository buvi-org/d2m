# Requirement: SMP-039-14
# Source agent: 039
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_039_marine_service_hardware_single_metal_parts.json
# Part: Marine Battery Box Tie-Down Rail - single metal part
# Raw idea: Marine Battery Box Tie-Down Rail
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 230 x 115 x 6 mm in stainless_316.
# - Drilled two through mounting holes diameter 10 mm at requirement X=23 and X=207, Y=57 mm.
# - Machined central obround through slot 76 x 14 mm at requirement X=115, Y=57 mm.
# - Milled centered top relief pocket 57 x 38 x 3 mm deep.
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
    Stock.rectangular(230, 115, 6, material="stainless_316")
    .drill(diameter=10, depth=6, cx=-92, cy=-0.5, through=True, spot_drill=False)
    .drill(diameter=10, depth=6, cx=92, cy=-0.5, through=True, spot_drill=False)
    .slot(length=76, width=14, depth=6, cx=0, cy=-0.5, through=True)
    .pocket(width=38, length=57, depth=3, cx=0, cy=0, corner_radius=0)
)
