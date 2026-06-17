# Requirement: SMP-038-04
# Source agent: 038
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_038_dental_lab_fixtures_single_metal_parts.json
# Part: Retainer Acrylic Trim Support - single metal part
# Raw idea: Retainer Acrylic Trim Support
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 155 x 55 x 27 mm in steel_a36.
# - Drilled two through mounting holes diameter 7 mm at requirement X=11 and X=144, Y=27 mm.
# - Machined central obround through slot 51 x 18 mm at requirement X=77, Y=27 mm.
# - Milled centered top relief pocket 38 x 18 x 6 mm deep.
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
    Stock.rectangular(155, 55, 27, material="steel_a36")
    .drill(diameter=7, depth=27, cx=-66.5, cy=-0.5, through=True, spot_drill=False)
    .drill(diameter=7, depth=27, cx=66.5, cy=-0.5, through=True, spot_drill=False)
    .slot(length=51, width=18, depth=27, cx=-0.5, cy=-0.5, through=True)
    .pocket(width=18, length=38, depth=6, cx=0, cy=0, corner_radius=0)
)
