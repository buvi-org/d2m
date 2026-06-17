# Requirement: SMP-037-02
# Source agent: 037
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_037_construction_tools_single_metal_parts.json
# Part: Concrete form tie spacing gauge - single metal part
# Raw idea: Concrete form tie spacing gauge
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 210 x 65 x 70 mm in steel_a36.
# - Drilled two through mounting holes diameter 11 mm at requirement X=13 and X=197, Y=32 mm.
# - Machined central obround through slot 70 x 18 mm at requirement X=105, Y=32 mm.
# - Milled centered top relief pocket 52 x 21 x 25 mm deep.
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
    Stock.rectangular(210, 65, 70, material="steel_a36")
    .drill(diameter=11, depth=70, cx=-92, cy=-0.5, through=True, spot_drill=False)
    .drill(diameter=11, depth=70, cx=92, cy=-0.5, through=True, spot_drill=False)
    .slot(length=70, width=18, depth=70, cx=0, cy=-0.5, through=True)
    .pocket(width=21, length=52, depth=25, cx=0, cy=0, corner_radius=0)
)
