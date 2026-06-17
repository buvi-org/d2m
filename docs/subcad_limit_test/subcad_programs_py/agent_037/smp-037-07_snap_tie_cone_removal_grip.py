# Requirement: SMP-037-07
# Source agent: 037
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_037_construction_tools_single_metal_parts.json
# Part: Snap-tie cone removal grip - single metal part
# Raw idea: Snap-tie cone removal grip
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 215 x 105 x 64 mm in steel_a36.
# - Drilled two through mounting holes diameter 12 mm at requirement X=21 and X=194, Y=52 mm.
# - Machined central obround through slot 71 x 18 mm at requirement X=107, Y=52 mm.
# - Milled centered top relief pocket 53 x 35 x 32 mm deep.
# - Applied 1.0 mm outside chamfer operation.
#
# Known gaps:
# - Separate 0.5 mm chamfers on hole and slot mouths are not individually represented; only the general chamfer operation is included.
# - Triangular rear-edge serrations are not represented exactly; current draft does not add repeated triangular edge cutouts.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft is syntactically generated but not executed; verify geometry against the frozen requirement in Stage 4.

from subcad import Stock

part = (
    Stock.rectangular(215, 105, 64, material="steel_a36")
    .drill(diameter=12, depth=64, cx=-86.5, cy=-0.5, through=True, spot_drill=False)
    .drill(diameter=12, depth=64, cx=86.5, cy=-0.5, through=True, spot_drill=False)
    .slot(length=71, width=18, depth=64, cx=-0.5, cy=-0.5, through=True)
    .pocket(width=35, length=53, depth=32, cx=0, cy=0, corner_radius=0)
)
