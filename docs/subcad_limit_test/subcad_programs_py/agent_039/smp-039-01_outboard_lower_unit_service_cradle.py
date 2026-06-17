# Requirement: SMP-039-01
# Source agent: 039
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_039_marine_service_hardware_single_metal_parts.json
# Part: Outboard Lower Unit Service Cradle - single metal part
# Raw idea: Outboard Lower Unit Service Cradle
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 90 x 75 x 61 mm in stainless_316.
# - Drilled two through mounting holes diameter 11 mm at requirement X=15 and X=75, Y=37 mm.
# - Machined central obround through slot 30 x 18 mm at requirement X=45, Y=37 mm.
# - Milled centered top relief pocket 25 x 25 x 29 mm deep.
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
    Stock.rectangular(90, 75, 61, material="stainless_316")
    .drill(diameter=11, depth=61, cx=-30, cy=-0.5, through=True, spot_drill=False)
    .drill(diameter=11, depth=61, cx=30, cy=-0.5, through=True, spot_drill=False)
    .slot(length=30, width=18, depth=61, cx=0, cy=-0.5, through=True)
    .pocket(width=25, length=25, depth=29, cx=0, cy=0, corner_radius=0)
)
