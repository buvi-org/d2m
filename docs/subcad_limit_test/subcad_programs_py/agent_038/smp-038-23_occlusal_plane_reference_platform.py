# Requirement: SMP-038-23
# Source agent: 038
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_038_dental_lab_fixtures_single_metal_parts.json
# Part: Occlusal Plane Reference Platform - single metal part
# Raw idea: Occlusal Plane Reference Platform
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 110 x 85 x 10 mm in stainless_316.
# - Drilled two through mounting holes diameter 13 mm at requirement X=17 and X=93, Y=42 mm.
# - Machined central obround through slot 36 x 10 mm at requirement X=55, Y=42 mm.
# - Milled centered top relief pocket 27 x 28 x 4 mm deep.
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
    Stock.rectangular(110, 85, 10, material="stainless_316")
    .drill(diameter=13, depth=10, cx=-38, cy=-0.5, through=True, spot_drill=False)
    .drill(diameter=13, depth=10, cx=38, cy=-0.5, through=True, spot_drill=False)
    .slot(length=36, width=10, depth=10, cx=0, cy=-0.5, through=True)
    .pocket(width=28, length=27, depth=4, cx=0, cy=0, corner_radius=0)
)
