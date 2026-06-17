# Requirement: SMP-038-19
# Source agent: 038
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_038_dental_lab_fixtures_single_metal_parts.json
# Part: Temporary Crown Shell Holder - single metal part
# Raw idea: Temporary Crown Shell Holder
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 95 x 40 x 67 mm in stainless_316.
# - Drilled two through mounting holes diameter 9 mm at requirement X=10 and X=85, Y=20 mm.
# - Machined central obround through slot 31 x 18 mm at requirement X=47, Y=20 mm.
# - Milled centered top relief pocket 25 x 18 x 24 mm deep.
# - Approximated top angled reference face using slope_cut over last 19 mm with derived depth 14.318 mm from 37 degrees.
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
    Stock.rectangular(95, 40, 67, material="stainless_316")
    .drill(diameter=9, depth=67, cx=-37.5, cy=0, through=True, spot_drill=False)
    .drill(diameter=9, depth=67, cx=37.5, cy=0, through=True, spot_drill=False)
    .slot(length=31, width=18, depth=67, cx=-0.5, cy=0, through=True)
    .pocket(width=18, length=25, depth=24, cx=0, cy=0, corner_radius=0)
    .slope_cut(width=40, length=19, start_depth=0, end_depth=14.318, cx=38, cy=0, slope_axis="X")
)
