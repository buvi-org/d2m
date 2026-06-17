# Requirement: SMP-017-06
# Source agent: 017
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_017_hvac_plumbing_hardware_single_metal_parts.json
# Part: Duct-Mounted Static Pressure Probe Compression Fitting - single metal part
# Raw idea: Duct-Mounted Static Pressure Probe Compression Fitting
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 220 x 90 x 3 mm with mapped material steel_1045.
# - Two through mounting holes dia 13 mm at X=18/202, Y=45.
# - Central through obround slot 73 x 16 mm at X=110, Y=45.
# - Top relief pocket 55 x 30 x 2 mm deep, centered between mounting holes.
# - Angled top reference face over last 44 mm using slope_cut at nominal 34 degree intent.
# - M4 tapped hole represented with threaded_hole near the right side/c. pocket region.
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
    Stock.rectangular(220, 90, 3, material="steel_1045")
    .drill(diameter=13, cx=-92, cy=0, through=True)
    .drill(diameter=13, cx=92, cy=0, through=True)
    .slot(length=73, width=16, cx=0, cy=0, through=True)
    .pocket(width=30, length=55, depth=2, cx=0, cy=0)
    .slope_cut(width=90, length=44, start_depth=0, end_depth=3, cx=88, cy=0, slope_axis="X")
    .threaded_hole(diameter=4, depth=45, cx=106, cy=0)
)
