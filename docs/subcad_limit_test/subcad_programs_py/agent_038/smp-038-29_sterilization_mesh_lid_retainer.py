# Requirement: SMP-038-29
# Source agent: 038
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_038_dental_lab_fixtures_single_metal_parts.json
# Part: Sterilization Mesh Lid Retainer - single metal part
# Raw idea: Sterilization Mesh Lid Retainer
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 255 x 90 x 3 mm in steel_a36.
# - Drilled two through mounting holes diameter 6 mm at requirement X=18 and X=237, Y=45 mm.
# - Machined central obround through slot 85 x 14 mm at requirement X=127, Y=45 mm.
# - Milled centered top relief pocket 63 x 30 x 2 mm deep.
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
    Stock.rectangular(255, 90, 3, material="steel_a36")
    .drill(diameter=6, depth=3, cx=-109.5, cy=0, through=True, spot_drill=False)
    .drill(diameter=6, depth=3, cx=109.5, cy=0, through=True, spot_drill=False)
    .slot(length=85, width=14, depth=3, cx=-0.5, cy=0, through=True)
    .pocket(width=30, length=63, depth=2, cx=0, cy=0, corner_radius=0)
)
