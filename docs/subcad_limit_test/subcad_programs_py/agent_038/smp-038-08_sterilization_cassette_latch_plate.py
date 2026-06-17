# Requirement: SMP-038-08
# Source agent: 038
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_038_dental_lab_fixtures_single_metal_parts.json
# Part: Sterilization Cassette Latch Plate - single metal part
# Raw idea: Sterilization Cassette Latch Plate
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 110 x 75 x 5 mm in aluminum_6061.
# - Drilled two through mounting holes diameter 6 mm at requirement X=15 and X=95, Y=37 mm.
# - Machined central obround through slot 36 x 7 mm at requirement X=55, Y=37 mm.
# - Milled centered top relief pocket 27 x 25 x 1 mm deep.
# - Applied 1.0 mm outside chamfer operation.
#
# Known gaps:
# - Separate 0.5 mm chamfers on hole and slot mouths are not individually represented; only the general chamfer operation is included.
# - Integral hook lip with projection and undercut is not represented because the current fluent program starts from the finished rectangular envelope and has no explicit bend/undercut lip operation.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft is syntactically generated but not executed; verify geometry against the frozen requirement in Stage 4.

from subcad import Stock

part = (
    Stock.rectangular(110, 75, 5, material="aluminum_6061")
    .drill(diameter=6, depth=5, cx=-40, cy=-0.5, through=True, spot_drill=False)
    .drill(diameter=6, depth=5, cx=40, cy=-0.5, through=True, spot_drill=False)
    .slot(length=36, width=7, depth=5, cx=0, cy=-0.5, through=True)
    .pocket(width=25, length=27, depth=1, cx=0, cy=0, corner_radius=0)
)
