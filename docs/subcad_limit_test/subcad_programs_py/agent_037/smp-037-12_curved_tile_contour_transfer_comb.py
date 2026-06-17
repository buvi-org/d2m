# Requirement: SMP-037-12
# Source agent: 037
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_037_construction_tools_single_metal_parts.json
# Part: Curved tile contour transfer comb - single metal part
# Raw idea: Curved tile contour transfer comb
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 120 x 85 x 41 mm in steel_a36.
# - Drilled two through mounting holes diameter 9 mm at requirement X=17 and X=103, Y=42 mm.
# - Machined central obround through slot 40 x 10 mm at requirement X=60, Y=42 mm.
# - Milled centered top relief pocket 30 x 28 x 20 mm deep.
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
    Stock.rectangular(120, 85, 41, material="steel_a36")
    .drill(diameter=9, depth=41, cx=-43, cy=-0.5, through=True, spot_drill=False)
    .drill(diameter=9, depth=41, cx=43, cy=-0.5, through=True, spot_drill=False)
    .slot(length=40, width=10, depth=41, cx=0, cy=-0.5, through=True)
    .pocket(width=28, length=30, depth=20, cx=0, cy=0, corner_radius=0)
)
