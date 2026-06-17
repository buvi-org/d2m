# Requirement: SMP-038-20
# Source agent: 038
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_038_dental_lab_fixtures_single_metal_parts.json
# Part: Sintering Bead Containment Dish - single metal part
# Raw idea: Sintering Bead Containment Dish
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 200 x 70 x 21 mm in stainless_316.
# - Drilled two through mounting holes diameter 10 mm at requirement X=14 and X=186, Y=35 mm.
# - Machined central obround through slot 66 x 10 mm at requirement X=100, Y=35 mm.
# - Milled centered top relief pocket 50 x 23 x 3 mm deep.
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
    Stock.rectangular(200, 70, 21, material="stainless_316")
    .drill(diameter=10, depth=21, cx=-86, cy=0, through=True, spot_drill=False)
    .drill(diameter=10, depth=21, cx=86, cy=0, through=True, spot_drill=False)
    .slot(length=66, width=10, depth=21, cx=0, cy=0, through=True)
    .pocket(width=23, length=50, depth=3, cx=0, cy=0, corner_radius=0)
)
