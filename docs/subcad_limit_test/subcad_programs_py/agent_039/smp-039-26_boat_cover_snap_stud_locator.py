# Requirement: SMP-039-26
# Source agent: 039
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_039_marine_service_hardware_single_metal_parts.json
# Part: Boat Cover Snap Stud Locator - single metal part
# Raw idea: Boat Cover Snap Stud Locator
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 100 x 45 x 11 mm in steel_a36.
# - Drilled two through mounting holes diameter 12 mm at requirement X=10 and X=90, Y=22 mm.
# - Machined central obround through slot 33 x 16 mm at requirement X=50, Y=22 mm.
# - Milled centered top relief pocket 25 x 18 x 3 mm deep.
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
    Stock.rectangular(100, 45, 11, material="steel_a36")
    .drill(diameter=12, depth=11, cx=-40, cy=-0.5, through=True, spot_drill=False)
    .drill(diameter=12, depth=11, cx=40, cy=-0.5, through=True, spot_drill=False)
    .slot(length=33, width=16, depth=11, cx=0, cy=-0.5, through=True)
    .pocket(width=18, length=25, depth=3, cx=0, cy=0, corner_radius=0)
)
