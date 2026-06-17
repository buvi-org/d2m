# Requirement: SMP-039-05
# Source agent: 039
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_039_marine_service_hardware_single_metal_parts.json
# Part: Rigging Turnbuckle Safety Clip Installer - single metal part
# Raw idea: Rigging Turnbuckle Safety Clip Installer
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 90 x 75 x 6 mm in steel_a36.
# - Drilled two through mounting holes diameter 13 mm at requirement X=15 and X=75, Y=37 mm.
# - Machined central obround through slot 30 x 15 mm at requirement X=45, Y=37 mm.
# - Milled centered top relief pocket 25 x 25 x 2 mm deep.
# - Approximated top angled reference face using slope_cut over last 18 mm with derived depth 3.499 mm from 11 degrees.
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
    Stock.rectangular(90, 75, 6, material="steel_a36")
    .drill(diameter=13, depth=6, cx=-30, cy=-0.5, through=True, spot_drill=False)
    .drill(diameter=13, depth=6, cx=30, cy=-0.5, through=True, spot_drill=False)
    .slot(length=30, width=15, depth=6, cx=0, cy=-0.5, through=True)
    .pocket(width=25, length=25, depth=2, cx=0, cy=0, corner_radius=0)
    .slope_cut(width=75, length=18, start_depth=0, end_depth=3.499, cx=36, cy=0, slope_axis="X")
)
