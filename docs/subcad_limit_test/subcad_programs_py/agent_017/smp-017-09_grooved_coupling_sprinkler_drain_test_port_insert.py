# Requirement: SMP-017-09
# Source agent: 017
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_017_hvac_plumbing_hardware_single_metal_parts.json
# Part: Grooved Coupling Sprinkler Drain Test Port Insert - single metal part
# Raw idea: Grooved Coupling Sprinkler Drain Test Port Insert
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 160 x 85 x 43 mm with mapped material steel_a36.
# - Two through mounting holes dia 9 mm at X=17/143, Y=42.
# - Central through obround slot 53 x 13 mm at X=80, Y=42.
# - Top relief pocket 40 x 28 x 8 mm deep, centered between mounting holes.
# - M8 tapped hole represented with threaded_hole near the right side/c. pocket region.
# - 1.0 mm top/outside chamfer represented with Stock.chamfer.
#
# Known gaps:
# - Side tapped hole axis parallel to Y is not represented exactly; program uses a top-face vertical threaded-hole proxy.
# - 0.5 mm chamfers on individual hole and slot mouths are not separately selectable in this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Coordinate conversion used Stock centered XY coordinates from the requirement lower-left origin.

from subcad import Stock

part = (
    Stock.rectangular(160, 85, 43, material="steel_a36")
    .drill(diameter=9, cx=-63, cy=-0.5, through=True)
    .drill(diameter=9, cx=63, cy=-0.5, through=True)
    .slot(length=53, width=13, cx=0, cy=-0.5, through=True)
    .pocket(width=28, length=40, depth=8, cx=0, cy=0)
    .threaded_hole(diameter=8, depth=42.5, cx=72, cy=0)
)
