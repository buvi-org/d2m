# Requirement: SMP-013-04
# Source agent: 013
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_013_aerospace_uav_hardware_single_metal_parts.json
# Part: Pitot Tube Heated Mount Block - single metal part
# Raw idea: Pitot Tube Heated Mount Block
# Status: draft_unexecuted
#
# Coverage notes:
# - Cylindrical stock OD 76 mm x length 56 mm with mapped material aluminum_6061.
# - Centered through bore diameter 15 mm.
# - One concentric counterbore diameter 25 mm x 3 mm deep.
# - Longitudinal top flat intent 25 mm wide over 48 mm length.
# - Two tapped radial clamp-hole callouts M8 at X=18 and X=37 mm represented by threaded_hole operations.
# - Radial split relief slit width 2 mm from OD toward bore represented by a through slot.
# - Transverse top relief slot width 4 mm at X=28 mm, depth 7 mm.
# - Opposed wrench flats intent leaving 68 mm across flats over the middle third.
# - 1.0 mm outside circular edge break represented with Stock.chamfer.
#
# Known gaps:
# - Requirement datum says cylinder axis is X; Stock.cylindrical and top-face bore are Z-axis oriented, so axial orientation must be reviewed.
# - Counterbores are required on both ends; this draft only represents the accessible top/end counterbore.
# - Milled flat is approximated by a shallow rectangular pocket on the top of the cylindrical stock, not an exact chordal flat.
# - Radial tapped holes through the top flat are represented in Stock top-face coordinates; true radial orientation and thread sidewall are not exact.
# - Split relief slit is approximated as a top-face through slot; exact OD-to-bore radial cut on datum-B side needs review.
# - Transverse slot on a cylindrical top flat is represented as a straight top-face slot; exact intersection with prior flat is approximate.
# - Opposed wrench flats are approximated as a single top flat/pocket; the opposite flat and exact across-flats geometry are not represented.
# - Internal bore-mouth chamfers are not independently selectable in this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Round-bar programs use Stock.cylindrical(diameter, height) per the generation guide; axis convention may differ from the frozen X-axis requirement text.

from subcad import Stock

part = (
    Stock.cylindrical(76, 56, material="aluminum_6061")
    .bore(diameter=15, through=True)
    .counterbore(hole_diameter=15, counterbore_diameter=25, counterbore_depth=3, cx=0, cy=0)
    .pocket(width=25, length=48, depth=2.115, cx=0, cy=0)
    .threaded_hole(diameter=8, depth=76, cx=-10, cy=0, through=True)
    .threaded_hole(diameter=8, depth=76, cx=9, cy=0, through=True)
    .slot(length=30.5, width=2, depth=76, cx=0, cy=11.375, through=True)
    .slot(length=76, width=4, depth=7, angle=90, cx=0, cy=0)
    .pocket(width=76, length=18.667, depth=4, cx=0, cy=0)
)
