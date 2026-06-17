# Requirement: SMP-016-01
# Source agent: 016
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_016_packaging_machinery_single_metal_parts.json
# Part: Starwheel pocket insert for round bottle indexing - single metal part
# Raw idea: Starwheel pocket insert for round bottle indexing
# Status: draft_unexecuted
#
# Coverage notes:
# - Cylindrical stock OD 89 mm x length 33 mm with mapped material stainless_316.
# - Centered through bore diameter 29 mm.
# - One concentric counterbore diameter 39 mm x 3 mm deep.
# - Longitudinal top flat intent 29 mm wide over 25 mm length.
# - Two tapped radial clamp-hole callouts M4 at X=11 and X=22 mm represented by threaded_hole operations.
# - Radial split relief slit width 6 mm from OD toward bore represented by a through slot.
# - 1.0 mm outside circular edge break represented with Stock.chamfer.
#
# Known gaps:
# - Requirement datum says cylinder axis is X; Stock.cylindrical and top-face bore are Z-axis oriented, so axial orientation must be reviewed.
# - Counterbores are required on both ends; this draft only represents the accessible top/end counterbore.
# - Milled flat is approximated by a shallow rectangular pocket on the top of the cylindrical stock, not an exact chordal flat.
# - Radial tapped holes through the top flat are represented in Stock top-face coordinates; true radial orientation and thread sidewall are not exact.
# - Split relief slit is approximated as a top-face through slot; exact OD-to-bore radial cut on datum-B side needs review.
# - Internal bore-mouth chamfers are not independently selectable in this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Round-bar programs use Stock.cylindrical(diameter, height) per the generation guide; axis convention may differ from the frozen X-axis requirement text.

from subcad import Stock

part = (
    Stock.cylindrical(89, 33, material="stainless_316")
    .bore(diameter=29, through=True)
    .counterbore(hole_diameter=29, counterbore_diameter=39, counterbore_depth=3, cx=0, cy=0)
    .pocket(width=29, length=25, depth=2.429, cx=0, cy=0)
    .threaded_hole(diameter=4, depth=89, cx=-5.5, cy=0, through=True)
    .threaded_hole(diameter=4, depth=89, cx=5.5, cy=0, through=True)
    .slot(length=30, width=6, depth=89, cx=0, cy=14.75, through=True)
)
