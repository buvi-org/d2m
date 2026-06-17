# Requirement: SMP-037-10
# Source agent: 037
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_037_construction_tools_single_metal_parts.json
# Part: Tile spacer removal hook - single metal part
# Raw idea: Tile spacer removal hook
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 130 x 80 x 11 mm in steel_a36.
# - Drilled two through mounting holes diameter 10 mm at requirement X=16 and X=114, Y=40 mm.
# - Machined central obround through slot 43 x 15 mm at requirement X=65, Y=40 mm.
# - Milled centered top relief pocket 32 x 26 x 3 mm deep.
# - Approximated top angled reference face using slope_cut over last 26 mm with derived depth 6.483 mm from 14 degrees.
# - Applied 1.0 mm outside chamfer operation.
#
# Known gaps:
# - Separate 0.5 mm chamfers on hole and slot mouths are not individually represented; only the general chamfer operation is included.
# - Integral hook lip with projection and undercut is not represented because the current fluent program starts from the finished rectangular envelope and has no explicit bend/undercut lip operation.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Verify angled-face orientation and depth because the requirement specifies angle while SubCAD uses start/end depths.

from subcad import Stock

part = (
    Stock.rectangular(130, 80, 11, material="steel_a36")
    .drill(diameter=10, depth=11, cx=-49, cy=0, through=True, spot_drill=False)
    .drill(diameter=10, depth=11, cx=49, cy=0, through=True, spot_drill=False)
    .slot(length=43, width=15, depth=11, cx=0, cy=0, through=True)
    .pocket(width=26, length=32, depth=3, cx=0, cy=0, corner_radius=0)
    .slope_cut(width=80, length=26, start_depth=0, end_depth=6.483, cx=52, cy=0, slope_axis="X")
)
