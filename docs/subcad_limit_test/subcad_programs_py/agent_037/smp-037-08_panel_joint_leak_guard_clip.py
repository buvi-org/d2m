# Requirement: SMP-037-08
# Source agent: 037
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_037_construction_tools_single_metal_parts.json
# Part: Panel joint leak guard clip - single metal part
# Raw idea: Panel joint leak guard clip
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 140 x 90 x 12 mm in steel_a36.
# - Drilled two through mounting holes diameter 11 mm at requirement X=18 and X=122, Y=45 mm.
# - Machined central obround through slot 46 x 14 mm at requirement X=70, Y=45 mm.
# - Milled centered top relief pocket 35 x 30 x 4 mm deep.
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
    Stock.rectangular(140, 90, 12, material="steel_a36")
    .drill(diameter=11, depth=12, cx=-52, cy=0, through=True, spot_drill=False)
    .drill(diameter=11, depth=12, cx=52, cy=0, through=True, spot_drill=False)
    .slot(length=46, width=14, depth=12, cx=0, cy=0, through=True)
    .pocket(width=30, length=35, depth=4, cx=0, cy=0, corner_radius=0)
)
