# Requirement: SMP-038-06
# Source agent: 038
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_038_dental_lab_fixtures_single_metal_parts.json
# Part: Ceramic Crown Glaze Rack - single metal part
# Raw idea: Ceramic Crown Glaze Rack
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 175 x 50 x 6 mm in stainless_316.
# - Drilled two through mounting holes diameter 10 mm at requirement X=10 and X=165, Y=25 mm.
# - Machined central obround through slot 58 x 10 mm at requirement X=87, Y=25 mm.
# - Milled centered top relief pocket 43 x 18 x 3 mm deep.
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
    Stock.rectangular(175, 50, 6, material="stainless_316")
    .drill(diameter=10, depth=6, cx=-77.5, cy=0, through=True, spot_drill=False)
    .drill(diameter=10, depth=6, cx=77.5, cy=0, through=True, spot_drill=False)
    .slot(length=58, width=10, depth=6, cx=-0.5, cy=0, through=True)
    .pocket(width=18, length=43, depth=3, cx=0, cy=0, corner_radius=0)
)
