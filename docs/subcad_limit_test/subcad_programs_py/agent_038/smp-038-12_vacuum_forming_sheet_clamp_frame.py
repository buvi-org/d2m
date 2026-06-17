# Requirement: SMP-038-12
# Source agent: 038
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_038_dental_lab_fixtures_single_metal_parts.json
# Part: Vacuum Forming Sheet Clamp Frame - single metal part
# Raw idea: Vacuum Forming Sheet Clamp Frame
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 185 x 140 x 12 mm in stainless_316.
# - Drilled two through mounting holes diameter 7 mm at requirement X=28 and X=157, Y=70 mm.
# - Machined central obround through slot 61 x 12 mm at requirement X=92, Y=70 mm.
# - Milled centered top relief pocket 46 x 46 x 2 mm deep.
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
    Stock.rectangular(185, 140, 12, material="stainless_316")
    .drill(diameter=7, depth=12, cx=-64.5, cy=0, through=True, spot_drill=False)
    .drill(diameter=7, depth=12, cx=64.5, cy=0, through=True, spot_drill=False)
    .slot(length=61, width=12, depth=12, cx=-0.5, cy=0, through=True)
    .pocket(width=46, length=46, depth=2, cx=0, cy=0, corner_radius=0)
)
