# Requirement: SMP-037-04
# Source agent: 037
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_037_construction_tools_single_metal_parts.json
# Part: Form panel lifting handle with wedge lock - single metal part
# Raw idea: Form panel lifting handle with wedge lock
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 225 x 75 x 12 mm in steel_a36.
# - Drilled two through mounting holes diameter 6 mm at requirement X=15 and X=210, Y=37 mm.
# - Machined central obround through slot 75 x 14 mm at requirement X=112, Y=37 mm.
# - Milled centered top relief pocket 56 x 25 x 5 mm deep.
# - Applied 1.0 mm outside chamfer operation.
#
# Known gaps:
# - Angled reference face at 41 degrees over 45 mm would need about 39.118 mm drop, exceeding the 12 mm stock height; not modeled.
# - Separate 0.5 mm chamfers on hole and slot mouths are not individually represented; only the general chamfer operation is included.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft is syntactically generated but not executed; verify geometry against the frozen requirement in Stage 4.

from subcad import Stock

part = (
    Stock.rectangular(225, 75, 12, material="steel_a36")
    .drill(diameter=6, depth=12, cx=-97.5, cy=-0.5, through=True, spot_drill=False)
    .drill(diameter=6, depth=12, cx=97.5, cy=-0.5, through=True, spot_drill=False)
    .slot(length=75, width=14, depth=12, cx=-0.5, cy=-0.5, through=True)
    .pocket(width=25, length=56, depth=5, cx=0, cy=0, corner_radius=0)
)
