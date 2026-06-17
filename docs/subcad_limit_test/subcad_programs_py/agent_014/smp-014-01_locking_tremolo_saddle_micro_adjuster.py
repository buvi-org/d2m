# Requirement: SMP-014-01
# Source agent: 014
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_014_musical_instrument_hardware_single_metal_parts.json
# Part: Locking Tremolo Saddle Micro-Adjuster - single metal part
# Raw idea: Locking Tremolo Saddle Micro-Adjuster
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 90 x 80 x 46 mm with mapped material steel_a36.
# - Two through mounting holes dia 9 mm at X=16/74, Y=40.
# - Central through obround slot 30 x 9 mm at X=45, Y=40.
# - Top relief pocket 25 x 26 x 2 mm deep, centered between mounting holes.
# - Angled top reference face over last 18 mm using slope_cut at nominal 18 degree intent.
# - M8 tapped hole represented with threaded_hole near the right side/c. pocket region.
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
    Stock.rectangular(90, 80, 46, material="steel_a36")
    .drill(diameter=9, cx=-29, cy=0, through=True)
    .drill(diameter=9, cx=29, cy=0, through=True)
    .slot(length=30, width=9, cx=0, cy=0, through=True)
    .pocket(width=26, length=25, depth=2, cx=0, cy=0)
    .slope_cut(width=80, length=18, start_depth=0, end_depth=5.849, cx=36, cy=0, slope_axis="X")
    .threaded_hole(diameter=8, depth=40, cx=37, cy=0)
)
