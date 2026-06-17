# Requirement: SMP-016-08
# Source agent: 016
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_016_packaging_machinery_single_metal_parts.json
# Part: Capper chuck insert for ribbed screw caps - single metal part
# Raw idea: Capper chuck insert for ribbed screw caps
# Status: draft_unexecuted
#
# Coverage notes:
# - Cylindrical stock OD 90 mm x length 43 mm with mapped material steel_a36.
# - Centered through bore diameter 30 mm.
# - One concentric counterbore diameter 40 mm x 3 mm deep.
# - Longitudinal top flat intent 30 mm wide over 35 mm length.
# - Two tapped radial clamp-hole callouts M7 at X=14 and X=28 mm represented by threaded_hole operations.
# - Radial split relief slit width 6 mm from OD toward bore represented by a through slot.
# - Transverse top relief slot width 8 mm at X=21 mm, depth 9 mm.
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
    Stock.cylindrical(90, 43, material="steel_a36")
    .bore(diameter=30, through=True)
    .counterbore(hole_diameter=30, counterbore_diameter=40, counterbore_depth=3, cx=0, cy=0)
    .pocket(width=30, length=35, depth=2.574, cx=0, cy=0)
    .threaded_hole(diameter=7, depth=90, cx=-7.5, cy=0, through=True)
    .threaded_hole(diameter=7, depth=90, cx=6.5, cy=0, through=True)
    .slot(length=30, width=6, depth=90, cx=0, cy=15, through=True)
    .slot(length=90, width=8, depth=9, angle=90, cx=-0.5, cy=0)
)
