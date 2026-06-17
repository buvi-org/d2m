# Requirement: SMP-013-10
# Source agent: 013
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_013_aerospace_uav_hardware_single_metal_parts.json
# Part: UAV Antenna Mast Folding Hinge Knuckle - single metal part
# Raw idea: UAV Antenna Mast Folding Hinge Knuckle
# Status: draft_unexecuted
#
# Coverage notes:
# - Cylindrical stock OD 56 mm x length 30 mm with mapped material aluminum_6061.
# - Centered through bore diameter 14 mm.
# - One concentric counterbore diameter 24 mm x 3 mm deep.
# - Longitudinal top flat intent 18 mm wide over 22 mm length.
# - Two tapped radial clamp-hole callouts M7 at X=10 and X=20 mm represented by threaded_hole operations.
# - Radial split relief slit width 2 mm from OD toward bore represented by a through slot.
# - Transverse top relief slot width 4 mm at X=15 mm, depth 5 mm.
# - 1.0 mm outside circular edge break represented with Stock.chamfer.
#
# Known gaps:
# - Requirement datum says cylinder axis is X; Stock.cylindrical and top-face bore are Z-axis oriented, so axial orientation must be reviewed.
# - Counterbores are required on both ends; this draft only represents the accessible top/end counterbore.
# - Milled flat is approximated by a shallow rectangular pocket on the top of the cylindrical stock, not an exact chordal flat.
# - Radial tapped holes through the top flat are represented in Stock top-face coordinates; true radial orientation and thread sidewall are not exact.
# - Split relief slit is approximated as a top-face through slot; exact OD-to-bore radial cut on datum-B side needs review.
# - Transverse slot on a cylindrical top flat is represented as a straight top-face slot; exact intersection with prior flat is approximate.
# - Internal bore-mouth chamfers are not independently selectable in this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Round-bar programs use Stock.cylindrical(diameter, height) per the generation guide; axis convention may differ from the frozen X-axis requirement text.

from subcad import Stock

part = (
    Stock.cylindrical(56, 30, material="aluminum_6061")
    .bore(diameter=14, through=True)
    .counterbore(hole_diameter=14, counterbore_diameter=24, counterbore_depth=3, cx=0, cy=0)
    .pocket(width=18, length=22, depth=1.486, cx=0, cy=0)
    .threaded_hole(diameter=7, depth=56, cx=-5, cy=0, through=True)
    .threaded_hole(diameter=7, depth=56, cx=5, cy=0, through=True)
    .slot(length=21, width=2, depth=56, cx=0, cy=8.75, through=True)
    .slot(length=56, width=4, depth=5, angle=90, cx=0, cy=0)
)
