# Requirement: SMP-038-27
# Source agent: 038
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_038_dental_lab_fixtures_single_metal_parts.json
# Part: Crown Margin Inspection Turntable - single metal part
# Raw idea: Crown Margin Inspection Turntable
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 150 x 75 x 48 mm in stainless_316.
# - Drilled two through mounting holes diameter 10 mm at requirement X=15 and X=135, Y=37 mm.
# - Machined central obround through slot 50 x 12 mm at requirement X=75, Y=37 mm.
# - Milled centered top relief pocket 37 x 25 x 7 mm deep.
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
    Stock.rectangular(150, 75, 48, material="stainless_316")
    .drill(diameter=10, depth=48, cx=-60, cy=-0.5, through=True, spot_drill=False)
    .drill(diameter=10, depth=48, cx=60, cy=-0.5, through=True, spot_drill=False)
    .slot(length=50, width=12, depth=48, cx=0, cy=-0.5, through=True)
    .pocket(width=25, length=37, depth=7, cx=0, cy=0, corner_radius=0)
)
