# Requirement: SMP-037-14
# Source agent: 037
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_037_construction_tools_single_metal_parts.json
# Part: Tile adhesive notch checker - single metal part
# Raw idea: Tile adhesive notch checker
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 155 x 90 x 3 mm in steel_a36.
# - Drilled two through mounting holes diameter 10 mm at requirement X=18 and X=137, Y=45 mm.
# - Machined central obround through slot 51 x 15 mm at requirement X=77, Y=45 mm.
# - Milled centered top relief pocket 38 x 30 x 2 mm deep.
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
    Stock.rectangular(155, 90, 3, material="steel_a36")
    .drill(diameter=10, depth=3, cx=-59.5, cy=0, through=True, spot_drill=False)
    .drill(diameter=10, depth=3, cx=59.5, cy=0, through=True, spot_drill=False)
    .slot(length=51, width=15, depth=3, cx=-0.5, cy=0, through=True)
    .pocket(width=30, length=38, depth=2, cx=0, cy=0, corner_radius=0)
)
