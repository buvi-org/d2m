# Requirement: SMP-010-06
# Source agent: 010
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_010_outdoor_marine_field_gear_single_metal_parts.json
# Part: Rugged Tripod Ground Spike Foot - single metal part
# Raw idea: Rugged Tripod Ground Spike Foot
# Status: draft_unexecuted
#
# Coverage notes:
# - Cylindrical stock OD 40 mm x length 119 mm with mapped material aluminum_6061.
# - Centered through bore diameter 8 mm.
# - One concentric counterbore diameter 18 mm x 3 mm deep.
# - Longitudinal top flat intent 13 mm wide over 111 mm length.
# - Two tapped radial clamp-hole callouts M7 at X=39 and X=79 mm represented by threaded_hole operations.
# - Radial split relief slit width 3 mm from OD toward bore represented by a through slot.
# - Transverse top relief slot width 5 mm at X=59 mm, depth 4 mm.
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
    Stock.cylindrical(40, 119, material="aluminum_6061")
    .bore(diameter=8, through=True)
    .counterbore(hole_diameter=8, counterbore_diameter=18, counterbore_depth=3, cx=0, cy=0)
    .pocket(width=13, length=111, depth=1.086, cx=0, cy=0)
    .threaded_hole(diameter=7, depth=40, cx=-20.5, cy=0, through=True)
    .threaded_hole(diameter=7, depth=40, cx=19.5, cy=0, through=True)
    .slot(length=16, width=3, depth=40, cx=0, cy=6, through=True)
    .slot(length=40, width=5, depth=4, angle=90, cx=-0.5, cy=0)
)
