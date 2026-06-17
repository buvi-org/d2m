# Requirement: SMP-017-03
# Source agent: 017
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_017_hvac_plumbing_hardware_single_metal_parts.json
# Part: Condensate Trap Cleanout Union Body - single metal part
# Raw idea: Condensate Trap Cleanout Union Body
# Status: draft_unexecuted
#
# Coverage notes:
# - Cylindrical stock OD 94 mm x length 65 mm with mapped material steel_a36.
# - Centered through bore diameter 23 mm.
# - One concentric counterbore diameter 33 mm x 3 mm deep.
# - Longitudinal top flat intent 31 mm wide over 57 mm length.
# - Two tapped radial clamp-hole callouts M6 at X=21 and X=43 mm represented by threaded_hole operations.
# - Radial split relief slit width 2 mm from OD toward bore represented by a through slot.
# - Opposed wrench flats intent leaving 86 mm across flats over the middle third.
# - 1.0 mm outside circular edge break represented with Stock.chamfer.
#
# Known gaps:
# - Requirement datum says cylinder axis is X; Stock.cylindrical and top-face bore are Z-axis oriented, so axial orientation must be reviewed.
# - Counterbores are required on both ends; this draft only represents the accessible top/end counterbore.
# - Milled flat is approximated by a shallow rectangular pocket on the top of the cylindrical stock, not an exact chordal flat.
# - Radial tapped holes through the top flat are represented in Stock top-face coordinates; true radial orientation and thread sidewall are not exact.
# - Split relief slit is approximated as a top-face through slot; exact OD-to-bore radial cut on datum-B side needs review.
# - Opposed wrench flats are approximated as a single top flat/pocket; the opposite flat and exact across-flats geometry are not represented.
# - Internal bore-mouth chamfers are not independently selectable in this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Round-bar programs use Stock.cylindrical(diameter, height) per the generation guide; axis convention may differ from the frozen X-axis requirement text.

from subcad import Stock

part = (
    Stock.cylindrical(94, 65, material="steel_a36")
    .bore(diameter=23, through=True)
    .counterbore(hole_diameter=23, counterbore_diameter=33, counterbore_depth=3, cx=0, cy=0)
    .pocket(width=31, length=57, depth=2.629, cx=0, cy=0)
    .threaded_hole(diameter=6, depth=94, cx=-11.5, cy=0, through=True)
    .threaded_hole(diameter=6, depth=94, cx=10.5, cy=0, through=True)
    .slot(length=35.5, width=2, depth=94, cx=0, cy=14.625, through=True)
    .pocket(width=94, length=21.667, depth=4, cx=0, cy=0)
)
