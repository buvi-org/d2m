# Requirement: SMP-037-28
# Source agent: 037
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_037_construction_tools_single_metal_parts.json
# Part: Rebar chair placement comb - single metal part
# Raw idea: Rebar chair placement comb
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 140 x 100 x 5 mm in steel_a36.
# - Drilled two through mounting holes diameter 5 mm at requirement X=20 and X=120, Y=50 mm.
# - Machined central obround through slot 46 x 14 mm at requirement X=70, Y=50 mm.
# - Milled centered top relief pocket 35 x 33 x 1 mm deep.
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
    Stock.rectangular(140, 100, 5, material="steel_a36")
    .drill(diameter=5, depth=5, cx=-50, cy=0, through=True, spot_drill=False)
    .drill(diameter=5, depth=5, cx=50, cy=0, through=True, spot_drill=False)
    .slot(length=46, width=14, depth=5, cx=0, cy=0, through=True)
    .pocket(width=33, length=35, depth=1, cx=0, cy=0, corner_radius=0)
)
