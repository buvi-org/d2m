# Requirement: SMP-039-12
# Source agent: 039
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_039_marine_service_hardware_single_metal_parts.json
# Part: Stern Drive Bellows Clamp Positioning Tool - single metal part
# Raw idea: Stern Drive Bellows Clamp Positioning Tool
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 135 x 115 x 68 mm in steel_1045.
# - Drilled two through mounting holes diameter 6 mm at requirement X=23 and X=112, Y=57 mm.
# - Machined central obround through slot 45 x 11 mm at requirement X=67, Y=57 mm.
# - Milled centered top relief pocket 33 x 38 x 33 mm deep.
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
    Stock.rectangular(135, 115, 68, material="steel_1045")
    .drill(diameter=6, depth=68, cx=-44.5, cy=-0.5, through=True, spot_drill=False)
    .drill(diameter=6, depth=68, cx=44.5, cy=-0.5, through=True, spot_drill=False)
    .slot(length=45, width=11, depth=68, cx=-0.5, cy=-0.5, through=True)
    .pocket(width=38, length=33, depth=33, cx=0, cy=0, corner_radius=0)
)
