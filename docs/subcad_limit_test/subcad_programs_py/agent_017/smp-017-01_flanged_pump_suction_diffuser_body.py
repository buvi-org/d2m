# Requirement: SMP-017-01
# Source agent: 017
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_017_hvac_plumbing_hardware_single_metal_parts.json
# Part: Flanged Pump Suction Diffuser Body - single metal part
# Raw idea: Flanged Pump Suction Diffuser Body
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 100 x 60 x 4 mm with mapped material steel_a36.
# - Two through mounting holes dia 6 mm at X=12/88, Y=30.
# - Central through obround slot 33 x 17 mm at X=50, Y=30.
# - Top relief pocket 25 x 20 x 1 mm deep, centered between mounting holes.
# - Angled top reference face over last 20 mm using slope_cut at nominal 27 degree intent.
# - 1.0 mm top/outside chamfer represented with Stock.chamfer.
#
# Known gaps:
# - Angled reference face is represented as a sloped rectangular cut; exact external wedge/angle verification remains for Stage 4 review.
# - 0.5 mm chamfers on individual hole and slot mouths are not separately selectable in this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Coordinate conversion used Stock centered XY coordinates from the requirement lower-left origin.

from subcad import Stock

part = (
    Stock.rectangular(100, 60, 4, material="steel_a36")
    .drill(diameter=6, cx=-38, cy=0, through=True)
    .drill(diameter=6, cx=38, cy=0, through=True)
    .slot(length=33, width=17, cx=0, cy=0, through=True)
    .pocket(width=20, length=25, depth=1, cx=0, cy=0)
    .slope_cut(width=60, length=20, start_depth=0, end_depth=4, cx=40, cy=0, slope_axis="X")
)
