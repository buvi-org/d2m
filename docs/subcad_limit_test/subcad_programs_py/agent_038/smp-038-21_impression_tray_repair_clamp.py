# Requirement: SMP-038-21
# Source agent: 038
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_038_dental_lab_fixtures_single_metal_parts.json
# Part: Impression Tray Repair Clamp - single metal part
# Raw idea: Impression Tray Repair Clamp
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 250 x 120 x 12 mm in stainless_316.
# - Drilled two through mounting holes diameter 8 mm at requirement X=24 and X=226, Y=60 mm.
# - Machined central obround through slot 83 x 9 mm at requirement X=125, Y=60 mm.
# - Milled centered top relief pocket 62 x 40 x 1 mm deep.
# - Applied 1.0 mm outside chamfer operation.
#
# Known gaps:
# - Separate 0.5 mm chamfers on hole and slot mouths are not individually represented; only the general chamfer operation is included.
# - Side tapped hole with axis parallel to Y is not represented because Stock tap/threaded_hole operations are top-face axial operations in this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft is syntactically generated but not executed; verify geometry against the frozen requirement in Stage 4.

from subcad import Stock

part = (
    Stock.rectangular(250, 120, 12, material="stainless_316")
    .drill(diameter=8, depth=12, cx=-101, cy=0, through=True, spot_drill=False)
    .drill(diameter=8, depth=12, cx=101, cy=0, through=True, spot_drill=False)
    .slot(length=83, width=9, depth=12, cx=0, cy=0, through=True)
    .pocket(width=40, length=62, depth=1, cx=0, cy=0, corner_radius=0)
)
