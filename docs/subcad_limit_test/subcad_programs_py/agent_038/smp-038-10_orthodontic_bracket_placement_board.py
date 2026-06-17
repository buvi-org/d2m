# Requirement: SMP-038-10
# Source agent: 038
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_038_dental_lab_fixtures_single_metal_parts.json
# Part: Orthodontic Bracket Placement Board - single metal part
# Raw idea: Orthodontic Bracket Placement Board
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 190 x 135 x 12 mm in steel_a36.
# - Drilled two through mounting holes diameter 5 mm at requirement X=27 and X=163, Y=67 mm.
# - Machined central obround through slot 63 x 11 mm at requirement X=95, Y=67 mm.
# - Milled centered top relief pocket 47 x 45 x 1 mm deep.
# - Approximated top angled reference face using slope_cut over last 38 mm with derived depth 6.7 mm from 10 degrees.
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
    Stock.rectangular(190, 135, 12, material="steel_a36")
    .drill(diameter=5, depth=12, cx=-68, cy=-0.5, through=True, spot_drill=False)
    .drill(diameter=5, depth=12, cx=68, cy=-0.5, through=True, spot_drill=False)
    .slot(length=63, width=11, depth=12, cx=0, cy=-0.5, through=True)
    .pocket(width=45, length=47, depth=1, cx=0, cy=0, corner_radius=0)
    .slope_cut(width=135, length=38, start_depth=0, end_depth=6.7, cx=76, cy=0, slope_axis="X")
)
