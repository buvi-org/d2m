# Requirement: SMP-037-17
# Source agent: 037
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_037_construction_tools_single_metal_parts.json
# Part: Brick bond pattern spacer rail - single metal part
# Raw idea: Brick bond pattern spacer rail
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 165 x 70 x 16 mm in steel_a36.
# - Drilled two through mounting holes diameter 13 mm at requirement X=14 and X=151, Y=35 mm.
# - Machined central obround through slot 55 x 11 mm at requirement X=82, Y=35 mm.
# - Milled centered top relief pocket 41 x 23 x 3 mm deep.
# - Applied 1.0 mm outside chamfer operation.
#
# Known gaps:
# - Separate 0.5 mm chamfers on hole and slot mouths are not individually represented; only the general chamfer operation is included.
# - Integral hook lip with projection and undercut is not represented because the current fluent program starts from the finished rectangular envelope and has no explicit bend/undercut lip operation.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft is syntactically generated but not executed; verify geometry against the frozen requirement in Stage 4.

from subcad import Stock

part = (
    Stock.rectangular(165, 70, 16, material="steel_a36")
    .drill(diameter=13, depth=16, cx=-68.5, cy=0, through=True, spot_drill=False)
    .drill(diameter=13, depth=16, cx=68.5, cy=0, through=True, spot_drill=False)
    .slot(length=55, width=11, depth=16, cx=-0.5, cy=0, through=True)
    .pocket(width=23, length=41, depth=3, cx=0, cy=0, corner_radius=0)
)
