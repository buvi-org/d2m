# Requirement: SMP-037-06
# Source agent: 037
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_037_construction_tools_single_metal_parts.json
# Part: Form brace angle saddle - single metal part
# Raw idea: Form brace angle saddle
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 115 x 65 x 12 mm in steel_a36.
# - Drilled two through mounting holes diameter 8 mm at requirement X=13 and X=102, Y=32 mm.
# - Machined central obround through slot 38 x 7 mm at requirement X=57, Y=32 mm.
# - Milled centered top relief pocket 28 x 21 x 5 mm deep.
# - Approximated top angled reference face using slope_cut over last 23 mm with derived depth 4.889 mm from 12 degrees.
# - Applied 1.0 mm outside chamfer operation.
#
# Known gaps:
# - Separate 0.5 mm chamfers on hole and slot mouths are not individually represented; only the general chamfer operation is included.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Verify angled-face orientation and depth because the requirement specifies angle while SubCAD uses start/end depths.

from subcad import Stock

part = (
    Stock.rectangular(115, 65, 12, material="steel_a36")
    .drill(diameter=8, depth=12, cx=-44.5, cy=-0.5, through=True, spot_drill=False)
    .drill(diameter=8, depth=12, cx=44.5, cy=-0.5, through=True, spot_drill=False)
    .slot(length=38, width=7, depth=12, cx=-0.5, cy=-0.5, through=True)
    .pocket(width=21, length=28, depth=5, cx=0, cy=0, corner_radius=0)
    .slope_cut(width=65, length=23, start_depth=0, end_depth=4.889, cx=46, cy=0, slope_axis="X")
)
