# Requirement: SMP-039-22
# Source agent: 039
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_039_marine_service_hardware_single_metal_parts.json
# Part: Lifeline Gate Latch Alignment Spacer - single metal part
# Raw idea: Lifeline Gate Latch Alignment Spacer
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 155 x 110 x 8 mm in steel_a36.
# - Drilled two through mounting holes diameter 13 mm at requirement X=22 and X=133, Y=55 mm.
# - Machined central obround through slot 51 x 12 mm at requirement X=77, Y=55 mm.
# - Milled centered top relief pocket 38 x 36 x 1 mm deep.
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
    Stock.rectangular(155, 110, 8, material="steel_a36")
    .drill(diameter=13, depth=8, cx=-55.5, cy=0, through=True, spot_drill=False)
    .drill(diameter=13, depth=8, cx=55.5, cy=0, through=True, spot_drill=False)
    .slot(length=51, width=12, depth=8, cx=-0.5, cy=0, through=True)
    .pocket(width=36, length=38, depth=1, cx=0, cy=0, corner_radius=0)
)
