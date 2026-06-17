# Requirement: SMP-038-07
# Source agent: 038
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_038_dental_lab_fixtures_single_metal_parts.json
# Part: Implant Model Analog Organizer - single metal part
# Raw idea: Implant Model Analog Organizer
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock 120 x 95 x 40 mm in stainless_316.
# - Drilled two through mounting holes diameter 8 mm at requirement X=19 and X=101, Y=47 mm.
# - Machined central obround through slot 40 x 16 mm at requirement X=60, Y=47 mm.
# - Milled centered top relief pocket 30 x 31 x 2 mm deep.
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
    Stock.rectangular(120, 95, 40, material="stainless_316")
    .drill(diameter=8, depth=40, cx=-41, cy=-0.5, through=True, spot_drill=False)
    .drill(diameter=8, depth=40, cx=41, cy=-0.5, through=True, spot_drill=False)
    .slot(length=40, width=16, depth=40, cx=0, cy=-0.5, through=True)
    .pocket(width=31, length=30, depth=2, cx=0, cy=0, corner_radius=0)
)
