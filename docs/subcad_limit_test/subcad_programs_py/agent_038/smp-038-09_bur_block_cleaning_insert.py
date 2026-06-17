# Requirement: SMP-038-09
# Source agent: 038
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_038_dental_lab_fixtures_single_metal_parts.json
# Part: Bur Block Cleaning Insert - single metal part
# Raw idea: Bur Block Cleaning Insert
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 120 x 110 x 35 mm in stainless_316.
# - Drilled two through mounting holes diameter 5 mm at requirement X=22 and X=98, Y=55 mm.
# - Machined central obround through slot 40 x 10 mm at requirement X=60, Y=55 mm.
# - Milled centered top relief pocket 30 x 36 x 7 mm deep.
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
    Stock.rectangular(120, 110, 35, material="stainless_316")
    .drill(diameter=5, depth=35, cx=-38, cy=0, through=True, spot_drill=False)
    .drill(diameter=5, depth=35, cx=38, cy=0, through=True, spot_drill=False)
    .slot(length=40, width=10, depth=35, cx=0, cy=0, through=True)
    .pocket(width=36, length=30, depth=7, cx=0, cy=0, corner_radius=0)
)
