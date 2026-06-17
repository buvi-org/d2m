# Requirement: SMP-039-18
# Source agent: 039
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_039_marine_service_hardware_single_metal_parts.json
# Part: Scupper Flap Replacement Fixture - single metal part
# Raw idea: Scupper Flap Replacement Fixture
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 95 x 55 x 49 mm in steel_a36.
# - Drilled two through mounting holes diameter 7 mm at requirement X=11 and X=84, Y=27 mm.
# - Machined central obround through slot 31 x 15 mm at requirement X=47, Y=27 mm.
# - Milled centered top relief pocket 25 x 18 x 10 mm deep.
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
    Stock.rectangular(95, 55, 49, material="steel_a36")
    .drill(diameter=7, depth=49, cx=-36.5, cy=-0.5, through=True, spot_drill=False)
    .drill(diameter=7, depth=49, cx=36.5, cy=-0.5, through=True, spot_drill=False)
    .slot(length=31, width=15, depth=49, cx=-0.5, cy=-0.5, through=True)
    .pocket(width=18, length=25, depth=10, cx=0, cy=0, corner_radius=0)
)
