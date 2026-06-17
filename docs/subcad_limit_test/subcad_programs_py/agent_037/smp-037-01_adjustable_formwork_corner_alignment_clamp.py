# Requirement: SMP-037-01
# Source agent: 037
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_037_construction_tools_single_metal_parts.json
# Part: Adjustable formwork corner alignment clamp - single metal part
# Raw idea: Adjustable formwork corner alignment clamp
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 205 x 80 x 4 mm in steel_1045.
# - Drilled two through mounting holes diameter 12 mm at requirement X=16 and X=189, Y=40 mm.
# - Machined central obround through slot 68 x 16 mm at requirement X=102, Y=40 mm.
# - Milled centered top relief pocket 51 x 26 x 1 mm deep.
# - Applied 1.0 mm outside chamfer operation.
#
# Known gaps:
# - Separate 0.5 mm chamfers on hole and slot mouths are not individually represented; only the general chamfer operation is included.
# - Side tapped hole with axis parallel to Y is not represented because Stock tap/threaded_hole operations are top-face axial operations in this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft is syntactically generated but not executed; verify geometry against the frozen requirement in Stage 4.

from subcad import Stock

part = (
    Stock.rectangular(205, 80, 4, material="steel_1045")
    .drill(diameter=12, depth=4, cx=-86.5, cy=0, through=True, spot_drill=False)
    .drill(diameter=12, depth=4, cx=86.5, cy=0, through=True, spot_drill=False)
    .slot(length=68, width=16, depth=4, cx=-0.5, cy=0, through=True)
    .pocket(width=26, length=51, depth=1, cx=0, cy=0, corner_radius=0)
)
