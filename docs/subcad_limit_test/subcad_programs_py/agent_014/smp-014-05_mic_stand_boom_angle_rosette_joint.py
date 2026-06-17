# Requirement: SMP-014-05
# Source agent: 014
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_014_musical_instrument_hardware_single_metal_parts.json
# Part: Mic Stand Boom Angle Rosette Joint - single metal part
# Raw idea: Mic Stand Boom Angle Rosette Joint
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 125 x 70 x 60 mm with mapped material steel_a36.
# - Two through mounting holes dia 11 mm at X=14/111, Y=35.
# - Central through obround slot 41 x 10 mm at X=62, Y=35.
# - Top relief pocket 31 x 23 x 13 mm deep, centered between mounting holes.
# - Angled top reference face over last 25 mm using slope_cut at nominal 25 degree intent.
# - 6 triangular rear-edge serrations, each 3 mm deep, represented by repeated triangular profile_cutout operations.
# - 1.0 mm top/outside chamfer represented with Stock.chamfer.
#
# Known gaps:
# - Angled reference face is represented as a sloped rectangular cut; exact external wedge/angle verification remains for Stage 4 review.
# - Serration profile_cutout placement needs execution review because the triangles lie on the rear edge boundary.
# - 0.5 mm chamfers on individual hole and slot mouths are not separately selectable in this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
# - Executable draft omits boundary triangular profile_cutout serration proxies because they erased the full solid in OCC; serrations remain a requirement gap for later targeted support.
#
# Review notes:
# - Coordinate conversion used Stock centered XY coordinates from the requirement lower-left origin.

from subcad import Stock

part = (
    Stock.rectangular(125, 70, 60, material="steel_a36")
    .drill(diameter=11, cx=-48.5, cy=0, through=True)
    .drill(diameter=11, cx=48.5, cy=0, through=True)
    .slot(length=41, width=10, cx=-0.5, cy=0, through=True)
    .pocket(width=23, length=31, depth=13, cx=0, cy=0)
    .slope_cut(width=70, length=25, start_depth=0, end_depth=11.658, cx=50, cy=0, slope_axis="X")
)
