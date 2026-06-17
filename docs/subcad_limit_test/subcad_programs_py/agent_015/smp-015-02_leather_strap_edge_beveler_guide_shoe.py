# Requirement: SMP-015-02
# Source agent: 015
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_015_textile_craft_machine_hardware_single_metal_parts.json
# Part: Leather Strap Edge Beveler Guide Shoe - single metal part
# Raw idea: Leather Strap Edge Beveler Guide Shoe
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 245 x 55 x 6 mm with mapped material steel_a36.
# - Two through mounting holes dia 11 mm at X=11/234, Y=27.
# - Central through obround slot 81 x 10 mm at X=122, Y=27.
# - Top relief pocket 61 x 18 x 3 mm deep, centered between mounting holes.
# - Centered full-length groove mouth 27 mm x depth 3 mm.
# - Angled top reference face over last 49 mm using slope_cut at nominal 36 degree intent.
# - M5 tapped hole represented with threaded_hole near the right side/c. pocket region.
# - 1.0 mm top/outside chamfer represented with Stock.chamfer.
#
# Known gaps:
# - V-groove included angle 90 degrees is approximated as a rectangular groove because Stock.groove has no V profile parameter.
# - Angled reference face is represented as a sloped rectangular cut; exact external wedge/angle verification remains for Stage 4 review.
# - Side tapped hole axis parallel to Y is not represented exactly; program uses a top-face vertical threaded-hole proxy.
# - 0.5 mm chamfers on individual hole and slot mouths are not separately selectable in this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Coordinate conversion used Stock centered XY coordinates from the requirement lower-left origin.

from subcad import Stock

part = (
    Stock.rectangular(245, 55, 6, material="steel_a36")
    .drill(diameter=11, cx=-111.5, cy=-0.5, through=True)
    .drill(diameter=11, cx=111.5, cy=-0.5, through=True)
    .slot(length=81, width=10, cx=-0.5, cy=-0.5, through=True)
    .pocket(width=18, length=61, depth=3, cx=0, cy=0)
    .groove(length=245, width=27, depth=3, cx=0, cy=0)
    .slope_cut(width=55, length=49, start_depth=0, end_depth=6, cx=98, cy=0, slope_axis="X")
    .threaded_hole(diameter=5, depth=27.5, cx=117.5, cy=0)
)
