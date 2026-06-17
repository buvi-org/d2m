# Requirement: SMP-039-30
# Source agent: 039
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_039_marine_service_hardware_single_metal_parts.json
# Part: Marina Hose Bib Anti-Drip Holster - single metal part
# Raw idea: Marina Hose Bib Anti-Drip Holster
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 130 x 110 x 4 mm in steel_a36.
# - Drilled two through mounting holes diameter 7 mm at requirement X=22 and X=108, Y=55 mm.
# - Machined central obround through slot 43 x 11 mm at requirement X=65, Y=55 mm.
# - Milled centered top relief pocket 32 x 36 x 2 mm deep.
# - Applied 1.0 mm outside chamfer operation.
#
# Known gaps:
# - Angled reference face at 27 degrees over 26 mm would need about 13.248 mm drop, exceeding the 4 mm stock height; not modeled.
# - Separate 0.5 mm chamfers on hole and slot mouths are not individually represented; only the general chamfer operation is included.
# - Integral hook lip with projection and undercut is not represented because the current fluent program starts from the finished rectangular envelope and has no explicit bend/undercut lip operation.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft is syntactically generated but not executed; verify geometry against the frozen requirement in Stage 4.

from subcad import Stock

part = (
    Stock.rectangular(130, 110, 4, material="steel_a36")
    .drill(diameter=7, depth=4, cx=-43, cy=0, through=True, spot_drill=False)
    .drill(diameter=7, depth=4, cx=43, cy=0, through=True, spot_drill=False)
    .slot(length=43, width=11, depth=4, cx=0, cy=0, through=True)
    .pocket(width=36, length=32, depth=2, cx=0, cy=0, corner_radius=0)
)
