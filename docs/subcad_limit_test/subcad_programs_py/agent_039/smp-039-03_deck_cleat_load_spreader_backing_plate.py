# Requirement: SMP-039-03
# Source agent: 039
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_039_marine_service_hardware_single_metal_parts.json
# Part: Deck Cleat Load Spreader Backing Plate - single metal part
# Raw idea: Deck Cleat Load Spreader Backing Plate
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 145 x 105 x 8 mm in steel_a36.
# - Drilled two through mounting holes diameter 7 mm at requirement X=21 and X=124, Y=52 mm.
# - Machined central obround through slot 48 x 16 mm at requirement X=72, Y=52 mm.
# - Milled centered top relief pocket 36 x 35 x 2 mm deep.
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
    Stock.rectangular(145, 105, 8, material="steel_a36")
    .drill(diameter=7, depth=8, cx=-51.5, cy=-0.5, through=True, spot_drill=False)
    .drill(diameter=7, depth=8, cx=51.5, cy=-0.5, through=True, spot_drill=False)
    .slot(length=48, width=16, depth=8, cx=-0.5, cy=-0.5, through=True)
    .pocket(width=35, length=36, depth=2, cx=0, cy=0, corner_radius=0)
)
