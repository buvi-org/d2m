# Requirement: SMP-039-08
# Source agent: 039
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_039_marine_service_hardware_single_metal_parts.json
# Part: Bilge Hose Anti-Kink Bulkhead Guide - single metal part
# Raw idea: Bilge Hose Anti-Kink Bulkhead Guide
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 130 x 95 x 10 mm in stainless_316.
# - Drilled two through mounting holes diameter 8 mm at requirement X=19 and X=111, Y=47 mm.
# - Machined central obround through slot 43 x 17 mm at requirement X=65, Y=47 mm.
# - Milled centered top relief pocket 32 x 31 x 2 mm deep.
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
    Stock.rectangular(130, 95, 10, material="stainless_316")
    .drill(diameter=8, depth=10, cx=-46, cy=-0.5, through=True, spot_drill=False)
    .drill(diameter=8, depth=10, cx=46, cy=-0.5, through=True, spot_drill=False)
    .slot(length=43, width=17, depth=10, cx=0, cy=-0.5, through=True)
    .pocket(width=31, length=32, depth=2, cx=0, cy=0, corner_radius=0)
)
