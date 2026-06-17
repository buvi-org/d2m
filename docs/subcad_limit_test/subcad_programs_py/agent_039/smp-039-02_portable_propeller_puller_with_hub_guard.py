# Requirement: SMP-039-02
# Source agent: 039
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_039_marine_service_hardware_single_metal_parts.json
# Part: Portable Propeller Puller With Hub Guard - single metal part
# Raw idea: Portable Propeller Puller With Hub Guard
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 205 x 55 x 9 mm in steel_a36.
# - Drilled two through mounting holes diameter 7 mm at requirement X=11 and X=194, Y=27 mm.
# - Machined central obround through slot 68 x 9 mm at requirement X=102, Y=27 mm.
# - Milled centered top relief pocket 51 x 18 x 1 mm deep.
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
    Stock.rectangular(205, 55, 9, material="steel_a36")
    .drill(diameter=7, depth=9, cx=-91.5, cy=-0.5, through=True, spot_drill=False)
    .drill(diameter=7, depth=9, cx=91.5, cy=-0.5, through=True, spot_drill=False)
    .slot(length=68, width=9, depth=9, cx=-0.5, cy=-0.5, through=True)
    .pocket(width=18, length=51, depth=1, cx=0, cy=0, corner_radius=0)
)
