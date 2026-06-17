# Requirement: SMP-038-01
# Source agent: 038
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_038_dental_lab_fixtures_single_metal_parts.json
# Part: Articulator Calibration Stand - single metal part
# Raw idea: Articulator Calibration Stand
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 115 x 100 x 70 mm in stainless_316.
# - Drilled two through mounting holes diameter 8 mm at requirement X=20 and X=95, Y=50 mm.
# - Machined central obround through slot 38 x 9 mm at requirement X=57, Y=50 mm.
# - Milled centered top relief pocket 28 x 33 x 19 mm deep.
# - Approximated top angled reference face using slope_cut over last 23 mm with derived depth 10.725 mm from 25 degrees.
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
    Stock.rectangular(115, 100, 70, material="stainless_316")
    .drill(diameter=8, depth=70, cx=-37.5, cy=0, through=True, spot_drill=False)
    .drill(diameter=8, depth=70, cx=37.5, cy=0, through=True, spot_drill=False)
    .slot(length=38, width=9, depth=70, cx=-0.5, cy=0, through=True)
    .pocket(width=33, length=28, depth=19, cx=0, cy=0, corner_radius=0)
    .slope_cut(width=100, length=23, start_depth=0, end_depth=10.725, cx=46, cy=0, slope_axis="X")
)
