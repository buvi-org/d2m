# Requirement: SMP-016-07
# Source agent: 016
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_016_packaging_machinery_single_metal_parts.json
# Part: Auger timing screw for pouch or bottle infeed - single metal part
# Raw idea: Auger timing screw for pouch or bottle infeed
# Status: draft_unexecuted
#
# Coverage notes:
# - Cylindrical stock OD 90 mm x length 115 mm with mapped material stainless_316.
# - Centered through bore diameter 18 mm.
# - One concentric counterbore diameter 28 mm x 3 mm deep.
# - Longitudinal top flat intent 30 mm wide over 107 mm length.
# - Two tapped radial clamp-hole callouts M6 at X=38 and X=76 mm represented by threaded_hole operations.
# - Radial split relief slit width 3 mm from OD toward bore represented by a through slot.
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
    Stock.cylindrical(90, 115, material="stainless_316")
    .bore(diameter=18, through=True)
    .counterbore(hole_diameter=18, counterbore_diameter=28, counterbore_depth=3, cx=0, cy=0)
    .pocket(width=30, length=107, depth=2.574, cx=0, cy=0)
    .threaded_hole(diameter=6, depth=90, cx=-19.5, cy=0, through=True)
    .threaded_hole(diameter=6, depth=90, cx=18.5, cy=0, through=True)
    .slot(length=36, width=3, depth=90, cx=0, cy=13.5, through=True)
)
