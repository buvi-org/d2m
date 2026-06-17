# Requirement: SMP-038-28
# Source agent: 038
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_038_dental_lab_fixtures_single_metal_parts.json
# Part: Alginate Mixing Bowl Stabilizer - single metal part
# Raw idea: Alginate Mixing Bowl Stabilizer
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 155 x 55 x 50 mm in stainless_316.
# - Drilled two through mounting holes diameter 13 mm at requirement X=11 and X=144, Y=27 mm.
# - Machined central obround through slot 51 x 16 mm at requirement X=77, Y=27 mm.
# - Milled centered top relief pocket 38 x 18 x 7 mm deep.
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
    Stock.rectangular(155, 55, 50, material="stainless_316")
    .drill(diameter=13, depth=50, cx=-66.5, cy=-0.5, through=True, spot_drill=False)
    .drill(diameter=13, depth=50, cx=66.5, cy=-0.5, through=True, spot_drill=False)
    .slot(length=51, width=16, depth=50, cx=-0.5, cy=-0.5, through=True)
    .pocket(width=18, length=38, depth=7, cx=0, cy=0, corner_radius=0)
)
