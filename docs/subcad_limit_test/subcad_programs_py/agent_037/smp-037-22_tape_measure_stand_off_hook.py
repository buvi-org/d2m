# Requirement: SMP-037-22
# Source agent: 037
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_037_construction_tools_single_metal_parts.json
# Part: Tape measure stand-off hook - single metal part
# Raw idea: Tape measure stand-off hook
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 215 x 95 x 4 mm in steel_a36.
# - Drilled two through mounting holes diameter 10 mm at requirement X=19 and X=196, Y=47 mm.
# - Machined central obround through slot 71 x 12 mm at requirement X=107, Y=47 mm.
# - Milled centered top relief pocket 53 x 31 x 1 mm deep.
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
    Stock.rectangular(215, 95, 4, material="steel_a36")
    .drill(diameter=10, depth=4, cx=-88.5, cy=-0.5, through=True, spot_drill=False)
    .drill(diameter=10, depth=4, cx=88.5, cy=-0.5, through=True, spot_drill=False)
    .slot(length=71, width=12, depth=4, cx=-0.5, cy=-0.5, through=True)
    .pocket(width=31, length=53, depth=1, cx=0, cy=0, corner_radius=0)
)
