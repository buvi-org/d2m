# Requirement: SMP-037-19
# Source agent: 037
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_037_construction_tools_single_metal_parts.json
# Part: Mortar joint raking depth guide - single metal part
# Raw idea: Mortar joint raking depth guide
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 90 x 80 x 30 mm in steel_a36.
# - Drilled two through mounting holes diameter 11 mm at requirement X=16 and X=74, Y=40 mm.
# - Machined central obround through slot 30 x 12 mm at requirement X=45, Y=40 mm.
# - Milled centered top relief pocket 25 x 26 x 14 mm deep.
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
    Stock.rectangular(90, 80, 30, material="steel_a36")
    .drill(diameter=11, depth=30, cx=-29, cy=0, through=True, spot_drill=False)
    .drill(diameter=11, depth=30, cx=29, cy=0, through=True, spot_drill=False)
    .slot(length=30, width=12, depth=30, cx=0, cy=0, through=True)
    .pocket(width=26, length=25, depth=14, cx=0, cy=0, corner_radius=0)
)
