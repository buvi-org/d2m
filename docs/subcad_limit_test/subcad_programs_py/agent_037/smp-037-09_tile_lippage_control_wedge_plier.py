# Requirement: SMP-037-09
# Source agent: 037
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_037_construction_tools_single_metal_parts.json
# Part: Tile lippage control wedge plier - single metal part
# Raw idea: Tile lippage control wedge plier
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 185 x 95 x 25 mm in steel_a36.
# - Drilled two through mounting holes diameter 5 mm at requirement X=19 and X=166, Y=47 mm.
# - Machined central obround through slot 61 x 7 mm at requirement X=92, Y=47 mm.
# - Milled centered top relief pocket 46 x 31 x 8 mm deep.
# - Applied 1.0 mm outside chamfer operation.
#
# Known gaps:
# - Angled reference face at 39 degrees over 37 mm would need about 29.962 mm drop, exceeding the 25 mm stock height; not modeled.
# - Separate 0.5 mm chamfers on hole and slot mouths are not individually represented; only the general chamfer operation is included.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft is syntactically generated but not executed; verify geometry against the frozen requirement in Stage 4.

from subcad import Stock

part = (
    Stock.rectangular(185, 95, 25, material="steel_a36")
    .drill(diameter=5, depth=25, cx=-73.5, cy=-0.5, through=True, spot_drill=False)
    .drill(diameter=5, depth=25, cx=73.5, cy=-0.5, through=True, spot_drill=False)
    .slot(length=61, width=7, depth=25, cx=-0.5, cy=-0.5, through=True)
    .pocket(width=31, length=46, depth=8, cx=0, cy=0, corner_radius=0)
)
