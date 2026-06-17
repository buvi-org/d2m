# Requirement: SMP-037-13
# Source agent: 037
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_037_construction_tools_single_metal_parts.json
# Part: Shower niche tile reveal jig - single metal part
# Raw idea: Shower niche tile reveal jig
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 210 x 60 x 30 mm in steel_a36.
# - Drilled two through mounting holes diameter 7 mm at requirement X=12 and X=198, Y=30 mm.
# - Machined central obround through slot 70 x 16 mm at requirement X=105, Y=30 mm.
# - Milled centered top relief pocket 52 x 20 x 12 mm deep.
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
    Stock.rectangular(210, 60, 30, material="steel_a36")
    .drill(diameter=7, depth=30, cx=-93, cy=0, through=True, spot_drill=False)
    .drill(diameter=7, depth=30, cx=93, cy=0, through=True, spot_drill=False)
    .slot(length=70, width=16, depth=30, cx=0, cy=0, through=True)
    .pocket(width=20, length=52, depth=12, cx=0, cy=0, corner_radius=0)
)
