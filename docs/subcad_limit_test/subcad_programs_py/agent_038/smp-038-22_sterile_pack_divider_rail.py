# Requirement: SMP-038-22
# Source agent: 038
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_038_dental_lab_fixtures_single_metal_parts.json
# Part: Sterile Pack Divider Rail - single metal part
# Raw idea: Sterile Pack Divider Rail
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 150 x 90 x 20 mm in stainless_316.
# - Drilled two through mounting holes diameter 8 mm at requirement X=18 and X=132, Y=45 mm.
# - Machined central obround through slot 50 x 17 mm at requirement X=75, Y=45 mm.
# - Milled centered top relief pocket 37 x 30 x 3 mm deep.
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
    Stock.rectangular(150, 90, 20, material="stainless_316")
    .drill(diameter=8, depth=20, cx=-57, cy=0, through=True, spot_drill=False)
    .drill(diameter=8, depth=20, cx=57, cy=0, through=True, spot_drill=False)
    .slot(length=50, width=17, depth=20, cx=0, cy=0, through=True)
    .pocket(width=30, length=37, depth=3, cx=0, cy=0, corner_radius=0)
)
