# Requirement: SMP-039-10
# Source agent: 039
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_039_marine_service_hardware_single_metal_parts.json
# Part: Folding Dock Step With Wet-Grip Tread - single metal part
# Raw idea: Folding Dock Step With Wet-Grip Tread
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 225 x 130 x 6 mm in steel_a36.
# - Drilled two through mounting holes diameter 8 mm at requirement X=26 and X=199, Y=65 mm.
# - Machined central obround through slot 75 x 14 mm at requirement X=112, Y=65 mm.
# - Milled centered top relief pocket 56 x 43 x 2 mm deep.
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
    Stock.rectangular(225, 130, 6, material="steel_a36")
    .drill(diameter=8, depth=6, cx=-86.5, cy=0, through=True, spot_drill=False)
    .drill(diameter=8, depth=6, cx=86.5, cy=0, through=True, spot_drill=False)
    .slot(length=75, width=14, depth=6, cx=-0.5, cy=0, through=True)
    .pocket(width=43, length=56, depth=2, cx=0, cy=0, corner_radius=0)
)
