# Requirement: SMP-014-04
# Source agent: 014
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_014_musical_instrument_hardware_single_metal_parts.json
# Part: Pedalboard Quick-Release Rail Clamp - single metal part
# Raw idea: Pedalboard Quick-Release Rail Clamp
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 230 x 85 x 3 mm with mapped material steel_1045.
# - Two through mounting holes dia 7 mm at X=17/213, Y=42.
# - Central through obround slot 76 x 17 mm at X=115, Y=42.
# - Top relief pocket 57 x 28 x 1 mm deep, centered between mounting holes.
# - Top dovetail groove length 206 mm, throat 17 mm, included angle 60 degrees.
# - 1.0 mm top/outside chamfer represented with Stock.chamfer.
#
# Known gaps:
# - 0.5 mm chamfers on individual hole and slot mouths are not separately selectable in this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Coordinate conversion used Stock centered XY coordinates from the requirement lower-left origin.

from subcad import Stock

part = (
    Stock.rectangular(230, 85, 3, material="steel_1045")
    .drill(diameter=7, cx=-98, cy=-0.5, through=True)
    .drill(diameter=7, cx=98, cy=-0.5, through=True)
    .slot(length=76, width=17, cx=0, cy=-0.5, through=True)
    .pocket(width=28, length=57, depth=1, cx=0, cy=0)
    .dovetail(length=206, width=17, depth=1.35, angle=60, cx=0, cy=0)
)
