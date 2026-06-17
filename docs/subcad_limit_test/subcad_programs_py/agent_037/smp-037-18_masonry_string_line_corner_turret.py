# Requirement: SMP-037-18
# Source agent: 037
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_037_construction_tools_single_metal_parts.json
# Part: Masonry string line corner turret - single metal part
# Raw idea: Masonry string line corner turret
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 115 x 55 x 55 mm in steel_a36.
# - Drilled two through mounting holes diameter 7 mm at requirement X=11 and X=104, Y=27 mm.
# - Machined central obround through slot 38 x 10 mm at requirement X=57, Y=27 mm.
# - Milled centered top relief pocket 28 x 18 x 5 mm deep.
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
    Stock.rectangular(115, 55, 55, material="steel_a36")
    .drill(diameter=7, depth=55, cx=-46.5, cy=-0.5, through=True, spot_drill=False)
    .drill(diameter=7, depth=55, cx=46.5, cy=-0.5, through=True, spot_drill=False)
    .slot(length=38, width=10, depth=55, cx=-0.5, cy=-0.5, through=True)
    .pocket(width=18, length=28, depth=5, cx=0, cy=0, corner_radius=0)
)
