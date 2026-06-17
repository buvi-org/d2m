# Requirement: SMP-039-16
# Source agent: 039
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_039_marine_service_hardware_single_metal_parts.json
# Part: Through-Hull Fitting Bedding Scraper - single metal part
# Raw idea: Through-Hull Fitting Bedding Scraper
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 120 x 60 x 37 mm in stainless_316.
# - Drilled two through mounting holes diameter 12 mm at requirement X=12 and X=108, Y=30 mm.
# - Machined central obround through slot 40 x 11 mm at requirement X=60, Y=30 mm.
# - Milled centered top relief pocket 30 x 20 x 15 mm deep.
# - Approximated top angled reference face using slope_cut over last 24 mm with derived depth 23.177 mm from 44 degrees.
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
    Stock.rectangular(120, 60, 37, material="stainless_316")
    .drill(diameter=12, depth=37, cx=-48, cy=0, through=True, spot_drill=False)
    .drill(diameter=12, depth=37, cx=48, cy=0, through=True, spot_drill=False)
    .slot(length=40, width=11, depth=37, cx=0, cy=0, through=True)
    .pocket(width=20, length=30, depth=15, cx=0, cy=0, corner_radius=0)
    .slope_cut(width=60, length=24, start_depth=0, end_depth=23.177, cx=48, cy=0, slope_axis="X")
)
