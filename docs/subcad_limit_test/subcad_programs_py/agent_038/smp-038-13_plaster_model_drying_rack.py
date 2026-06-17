# Requirement: SMP-038-13
# Source agent: 038
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_038_dental_lab_fixtures_single_metal_parts.json
# Part: Plaster Model Drying Rack - single metal part
# Raw idea: Plaster Model Drying Rack
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 135 x 100 x 41 mm in stainless_316.
# - Drilled two through mounting holes diameter 10 mm at requirement X=20 and X=115, Y=50 mm.
# - Machined central obround through slot 45 x 12 mm at requirement X=67, Y=50 mm.
# - Milled centered top relief pocket 33 x 33 x 18 mm deep.
# - Approximated top angled reference face using slope_cut over last 27 mm with derived depth 15.588 mm from 30 degrees.
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
    Stock.rectangular(135, 100, 41, material="stainless_316")
    .drill(diameter=10, depth=41, cx=-47.5, cy=0, through=True, spot_drill=False)
    .drill(diameter=10, depth=41, cx=47.5, cy=0, through=True, spot_drill=False)
    .slot(length=45, width=12, depth=41, cx=-0.5, cy=0, through=True)
    .pocket(width=33, length=33, depth=18, cx=0, cy=0, corner_radius=0)
    .slope_cut(width=100, length=27, start_depth=0, end_depth=15.588, cx=54, cy=0, slope_axis="X")
)
