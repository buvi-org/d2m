# Requirement: SMP-038-18
# Source agent: 038
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_038_dental_lab_fixtures_single_metal_parts.json
# Part: Orthodontic Elastic Sorting Carousel - single metal part
# Raw idea: Orthodontic Elastic Sorting Carousel
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 135 x 65 x 8 mm in stainless_316.
# - Drilled two through mounting holes diameter 6 mm at requirement X=13 and X=122, Y=32 mm.
# - Machined central obround through slot 45 x 17 mm at requirement X=67, Y=32 mm.
# - Milled centered top relief pocket 33 x 21 x 3 mm deep.
# - Applied 1.0 mm outside chamfer operation.
#
# Known gaps:
# - Separate 0.5 mm chamfers on hole and slot mouths are not individually represented; only the general chamfer operation is included.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft is syntactically generated but not executed; verify geometry against the frozen requirement in Stage 4.

from subcad import Stock

part = (
    Stock.rectangular(135, 65, 8, material="stainless_316")
    .drill(diameter=6, depth=8, cx=-54.5, cy=-0.5, through=True, spot_drill=False)
    .drill(diameter=6, depth=8, cx=54.5, cy=-0.5, through=True, spot_drill=False)
    .slot(length=45, width=17, depth=8, cx=-0.5, cy=-0.5, through=True)
    .pocket(width=21, length=33, depth=3, cx=0, cy=0, corner_radius=0)
)
