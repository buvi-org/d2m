# Requirement: SMP-017-07
# Source agent: 017
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_017_hvac_plumbing_hardware_single_metal_parts.json
# Part: Strainer Blowdown Valve Adapter Elbow - single metal part
# Raw idea: Strainer Blowdown Valve Adapter Elbow
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 105 x 40 x 23 mm with mapped material steel_a36.
# - Two through mounting holes dia 10 mm at X=10/95, Y=20.
# - Central through obround slot 35 x 17 mm at X=52, Y=20.
# - Top relief pocket 26 x 18 x 4 mm deep, centered between mounting holes.
# - Angled top reference face over last 21 mm using slope_cut at nominal 45 degree intent.
# - M10 tapped hole represented with threaded_hole near the right side/c. pocket region.
# - 1.0 mm top/outside chamfer represented with Stock.chamfer.
#
# Known gaps:
# - Angled reference face is represented as a sloped rectangular cut; exact external wedge/angle verification remains for Stage 4 review.
# - Side tapped hole axis parallel to Y is not represented exactly; program uses a top-face vertical threaded-hole proxy.
# - 0.5 mm chamfers on individual hole and slot mouths are not separately selectable in this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Coordinate conversion used Stock centered XY coordinates from the requirement lower-left origin.

from subcad import Stock

part = (
    Stock.rectangular(105, 40, 23, material="steel_a36")
    .drill(diameter=10, cx=-42.5, cy=0, through=True)
    .drill(diameter=10, cx=42.5, cy=0, through=True)
    .slot(length=35, width=17, cx=-0.5, cy=0, through=True)
    .pocket(width=18, length=26, depth=4, cx=0, cy=0)
    .slope_cut(width=40, length=21, start_depth=0, end_depth=21, cx=42, cy=0, slope_axis="X")
    .threaded_hole(diameter=10, depth=20, cx=42.5, cy=0)
)
