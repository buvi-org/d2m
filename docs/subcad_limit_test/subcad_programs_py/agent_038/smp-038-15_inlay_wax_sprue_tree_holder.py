# Requirement: SMP-038-15
# Source agent: 038
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_038_dental_lab_fixtures_single_metal_parts.json
# Part: Inlay Wax Sprue Tree Holder - single metal part
# Raw idea: Inlay Wax Sprue Tree Holder
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 75 x 55 x 55 mm in stainless_316.
# - Drilled two through mounting holes diameter 9 mm at requirement X=11 and X=64, Y=27 mm.
# - Machined central obround through slot 30 x 12 mm at requirement X=37, Y=27 mm.
# - Milled centered top relief pocket 25 x 18 x 23 mm deep.
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
    Stock.rectangular(75, 55, 55, material="stainless_316")
    .drill(diameter=9, depth=55, cx=-26.5, cy=-0.5, through=True, spot_drill=False)
    .drill(diameter=9, depth=55, cx=26.5, cy=-0.5, through=True, spot_drill=False)
    .slot(length=30, width=12, depth=55, cx=-0.5, cy=-0.5, through=True)
    .pocket(width=18, length=25, depth=23, cx=0, cy=0, corner_radius=0)
)
