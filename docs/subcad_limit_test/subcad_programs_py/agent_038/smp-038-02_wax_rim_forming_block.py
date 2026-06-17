# Requirement: SMP-038-02
# Source agent: 038
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_038_dental_lab_fixtures_single_metal_parts.json
# Part: Wax Rim Forming Block - single metal part
# Raw idea: Wax Rim Forming Block
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 85 x 85 x 67 mm in steel_a36.
# - Drilled two through mounting holes diameter 9 mm at requirement X=17 and X=68, Y=42 mm.
# - Machined central obround through slot 30 x 10 mm at requirement X=42, Y=42 mm.
# - Milled centered top relief pocket 25 x 28 x 8 mm deep.
# - Approximated top angled reference face using slope_cut over last 18 mm with derived depth 9.978 mm from 29 degrees.
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
    Stock.rectangular(85, 85, 67, material="steel_a36")
    .drill(diameter=9, depth=67, cx=-25.5, cy=-0.5, through=True, spot_drill=False)
    .drill(diameter=9, depth=67, cx=25.5, cy=-0.5, through=True, spot_drill=False)
    .slot(length=30, width=10, depth=67, cx=-0.5, cy=-0.5, through=True)
    .pocket(width=28, length=25, depth=8, cx=0, cy=0, corner_radius=0)
    .slope_cut(width=85, length=18, start_depth=0, end_depth=9.978, cx=33.5, cy=0, slope_axis="X")
)
