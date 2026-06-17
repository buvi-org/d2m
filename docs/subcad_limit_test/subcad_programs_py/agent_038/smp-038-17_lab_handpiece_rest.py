# Requirement: SMP-038-17
# Source agent: 038
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_038_dental_lab_fixtures_single_metal_parts.json
# Part: Lab Handpiece Rest - single metal part
# Raw idea: Lab Handpiece Rest
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 145 x 110 x 43 mm in stainless_316.
# - Drilled two through mounting holes diameter 9 mm at requirement X=22 and X=123, Y=55 mm.
# - Machined central obround through slot 48 x 14 mm at requirement X=72, Y=55 mm.
# - Milled centered top relief pocket 36 x 36 x 1 mm deep.
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
    Stock.rectangular(145, 110, 43, material="stainless_316")
    .drill(diameter=9, depth=43, cx=-50.5, cy=0, through=True, spot_drill=False)
    .drill(diameter=9, depth=43, cx=50.5, cy=0, through=True, spot_drill=False)
    .slot(length=48, width=14, depth=43, cx=-0.5, cy=0, through=True)
    .pocket(width=36, length=36, depth=1, cx=0, cy=0, corner_radius=0)
)
