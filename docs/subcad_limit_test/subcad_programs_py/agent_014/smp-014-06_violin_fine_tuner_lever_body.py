# Requirement: SMP-014-06
# Source agent: 014
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_014_musical_instrument_hardware_single_metal_parts.json
# Part: Violin Fine Tuner Lever Body - single metal part
# Raw idea: Violin Fine Tuner Lever Body
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 80 x 80 x 32 mm with mapped material steel_a36.
# - Two through mounting holes dia 11 mm at X=16/64, Y=40.
# - Central through obround slot 30 x 12 mm at X=40, Y=40.
# - Top relief pocket 25 x 26 x 6 mm deep, centered between mounting holes.
# - M7 tapped hole represented with threaded_hole near the right side/c. pocket region.
# - Integral hook lip projection 15 mm with 5 mm undercut represented by profile_contour outline intent.
# - 1.0 mm top/outside chamfer represented with Stock.chamfer.
#
# Known gaps:
# - Side tapped hole axis parallel to Y is not represented exactly; program uses a top-face vertical threaded-hole proxy.
# - Hook lip changes the outside outline beyond the nominal rectangular envelope; profile_contour intent may not actually add material from the starting rectangle.
# - 0.5 mm chamfers on individual hole and slot mouths are not separately selectable in this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
# - Executable draft omits profile_contour hook-lip proxy because it shrank the output envelope; hook-lip geometry remains a requirement gap for Stage 4 review.
#
# Review notes:
# - Coordinate conversion used Stock centered XY coordinates from the requirement lower-left origin.

from subcad import Stock

part = (
    Stock.rectangular(80, 80, 32, material="steel_a36")
    .drill(diameter=11, cx=-24, cy=0, through=True)
    .drill(diameter=11, cx=24, cy=0, through=True)
    .slot(length=30, width=12, cx=0, cy=0, through=True)
    .pocket(width=26, length=25, depth=6, cx=0, cy=0)
    .threaded_hole(diameter=7, depth=40, cx=33, cy=0)
)
