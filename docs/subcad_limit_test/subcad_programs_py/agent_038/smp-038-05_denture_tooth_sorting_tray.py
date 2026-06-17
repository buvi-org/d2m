# Requirement: SMP-038-05
# Source agent: 038
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_038_dental_lab_fixtures_single_metal_parts.json
# Part: Denture Tooth Sorting Tray - single metal part
# Raw idea: Denture Tooth Sorting Tray
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 155 x 70 x 8 mm in stainless_316.
# - Drilled two through mounting holes diameter 11 mm at requirement X=14 and X=141, Y=35 mm.
# - Machined central obround through slot 51 x 15 mm at requirement X=77, Y=35 mm.
# - Milled centered top relief pocket 38 x 23 x 1 mm deep.
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
    Stock.rectangular(155, 70, 8, material="stainless_316")
    .drill(diameter=11, depth=8, cx=-63.5, cy=0, through=True, spot_drill=False)
    .drill(diameter=11, depth=8, cx=63.5, cy=0, through=True, spot_drill=False)
    .slot(length=51, width=15, depth=8, cx=-0.5, cy=0, through=True)
    .pocket(width=23, length=38, depth=1, cx=0, cy=0, corner_radius=0)
)
