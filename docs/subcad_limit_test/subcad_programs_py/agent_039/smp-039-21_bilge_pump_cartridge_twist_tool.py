# Requirement: SMP-039-21
# Source agent: 039
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_039_marine_service_hardware_single_metal_parts.json
# Part: Bilge Pump Cartridge Twist Tool - single metal part
# Raw idea: Bilge Pump Cartridge Twist Tool
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 115 x 85 x 33 mm in steel_a36.
# - Drilled two through mounting holes diameter 5 mm at requirement X=17 and X=98, Y=42 mm.
# - Machined central obround through slot 38 x 18 mm at requirement X=57, Y=42 mm.
# - Milled centered top relief pocket 28 x 28 x 1 mm deep.
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
    Stock.rectangular(115, 85, 33, material="steel_a36")
    .drill(diameter=5, depth=33, cx=-40.5, cy=-0.5, through=True, spot_drill=False)
    .drill(diameter=5, depth=33, cx=40.5, cy=-0.5, through=True, spot_drill=False)
    .slot(length=38, width=18, depth=33, cx=-0.5, cy=-0.5, through=True)
    .pocket(width=28, length=28, depth=1, cx=0, cy=0, corner_radius=0)
)
