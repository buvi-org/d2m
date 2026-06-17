# Requirement: SMP-039-13
# Source agent: 039
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_039_marine_service_hardware_single_metal_parts.json
# Part: Mast Base Wiring Drip Loop Organizer - single metal part
# Raw idea: Mast Base Wiring Drip Loop Organizer
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 255 x 65 x 5 mm in steel_a36.
# - Drilled two through mounting holes diameter 11 mm at requirement X=13 and X=242, Y=32 mm.
# - Machined central obround through slot 85 x 7 mm at requirement X=127, Y=32 mm.
# - Milled centered top relief pocket 63 x 21 x 2 mm deep.
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
    Stock.rectangular(255, 65, 5, material="steel_a36")
    .drill(diameter=11, depth=5, cx=-114.5, cy=-0.5, through=True, spot_drill=False)
    .drill(diameter=11, depth=5, cx=114.5, cy=-0.5, through=True, spot_drill=False)
    .slot(length=85, width=7, depth=5, cx=-0.5, cy=-0.5, through=True)
    .pocket(width=21, length=63, depth=2, cx=0, cy=0, corner_radius=0)
)
