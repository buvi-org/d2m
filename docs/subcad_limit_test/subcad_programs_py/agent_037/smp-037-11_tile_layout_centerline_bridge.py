# Requirement: SMP-037-11
# Source agent: 037
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_037_construction_tools_single_metal_parts.json
# Part: Tile layout centerline bridge - single metal part
# Raw idea: Tile layout centerline bridge
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 195 x 120 x 61 mm in steel_a36.
# - Drilled two through mounting holes diameter 9 mm at requirement X=24 and X=171, Y=60 mm.
# - Machined central obround through slot 65 x 13 mm at requirement X=97, Y=60 mm.
# - Milled centered top relief pocket 48 x 40 x 1 mm deep.
# - Applied 1.0 mm outside chamfer operation.
#
# Known gaps:
# - Separate 0.5 mm chamfers on hole and slot mouths are not individually represented; only the general chamfer operation is included.
# - Triangular rear-edge serrations are not represented exactly; current draft does not add repeated triangular edge cutouts.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft is syntactically generated but not executed; verify geometry against the frozen requirement in Stage 4.

from subcad import Stock

part = (
    Stock.rectangular(195, 120, 61, material="steel_a36")
    .drill(diameter=9, depth=61, cx=-73.5, cy=0, through=True, spot_drill=False)
    .drill(diameter=9, depth=61, cx=73.5, cy=0, through=True, spot_drill=False)
    .slot(length=65, width=13, depth=61, cx=-0.5, cy=0, through=True)
    .pocket(width=40, length=48, depth=1, cx=0, cy=0, corner_radius=0)
)
