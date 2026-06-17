# Requirement: SMP-037-30
# Source agent: 037
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_037_construction_tools_single_metal_parts.json
# Part: Masonry opening sill slope gauge - single metal part
# Raw idea: Masonry opening sill slope gauge
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 150 x 50 x 43 mm in steel_a36.
# - Drilled two through mounting holes diameter 7 mm at requirement X=10 and X=140, Y=25 mm.
# - Machined central obround through slot 50 x 18 mm at requirement X=75, Y=25 mm.
# - Milled centered top relief pocket 37 x 18 x 13 mm deep.
# - Approximated top angled reference face using slope_cut over last 30 mm with derived depth 5.29 mm from 10 degrees.
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
    Stock.rectangular(150, 50, 43, material="steel_a36")
    .drill(diameter=7, depth=43, cx=-65, cy=0, through=True, spot_drill=False)
    .drill(diameter=7, depth=43, cx=65, cy=0, through=True, spot_drill=False)
    .slot(length=50, width=18, depth=43, cx=0, cy=0, through=True)
    .pocket(width=18, length=37, depth=13, cx=0, cy=0, corner_radius=0)
    .slope_cut(width=50, length=30, start_depth=0, end_depth=5.29, cx=60, cy=0, slope_axis="X")
)
