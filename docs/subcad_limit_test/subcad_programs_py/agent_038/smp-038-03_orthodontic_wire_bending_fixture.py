# Requirement: SMP-038-03
# Source agent: 038
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_038_dental_lab_fixtures_single_metal_parts.json
# Part: Orthodontic Wire Bending Fixture - single metal part
# Raw idea: Orthodontic Wire Bending Fixture
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 235 x 145 x 4 mm in stainless_316.
# - Drilled two through mounting holes diameter 8 mm at requirement X=29 and X=206, Y=72 mm.
# - Machined central obround through slot 78 x 9 mm at requirement X=117, Y=72 mm.
# - Milled centered top relief pocket 58 x 48 x 2 mm deep.
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
    Stock.rectangular(235, 145, 4, material="stainless_316")
    .drill(diameter=8, depth=4, cx=-88.5, cy=-0.5, through=True, spot_drill=False)
    .drill(diameter=8, depth=4, cx=88.5, cy=-0.5, through=True, spot_drill=False)
    .slot(length=78, width=9, depth=4, cx=-0.5, cy=-0.5, through=True)
    .pocket(width=48, length=58, depth=2, cx=0, cy=0, corner_radius=0)
)
