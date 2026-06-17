# Requirement: SMP-037-15
# Source agent: 037
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_037_construction_tools_single_metal_parts.json
# Part: Tile edge trim miter marking saddle - single metal part
# Raw idea: Tile edge trim miter marking saddle
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 215 x 120 x 50 mm in steel_a36.
# - Drilled two through mounting holes diameter 8 mm at requirement X=24 and X=191, Y=60 mm.
# - Machined central obround through slot 71 x 16 mm at requirement X=107, Y=60 mm.
# - Milled centered top relief pocket 53 x 40 x 14 mm deep.
# - Approximated top angled reference face using slope_cut over last 43 mm with derived depth 18.252 mm from 23 degrees.
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
    Stock.rectangular(215, 120, 50, material="steel_a36")
    .drill(diameter=8, depth=50, cx=-83.5, cy=0, through=True, spot_drill=False)
    .drill(diameter=8, depth=50, cx=83.5, cy=0, through=True, spot_drill=False)
    .slot(length=71, width=16, depth=50, cx=-0.5, cy=0, through=True)
    .pocket(width=40, length=53, depth=14, cx=0, cy=0, corner_radius=0)
    .slope_cut(width=120, length=43, start_depth=0, end_depth=18.252, cx=86, cy=0, slope_axis="X")
)
