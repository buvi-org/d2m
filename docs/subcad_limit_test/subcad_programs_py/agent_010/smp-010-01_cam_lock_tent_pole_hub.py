# Requirement: SMP-010-01
# Source agent: 010
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_010_outdoor_marine_field_gear_single_metal_parts.json
# Part: Cam-Lock Tent Pole Hub - single metal part
# Raw idea: Cam-Lock Tent Pole Hub
# Status: draft_unexecuted
#
# Coverage notes:
# - Cylindrical stock OD 61 mm x length 57 mm with mapped material steel_a36.
# - Centered through bore diameter 20 mm.
# - One concentric counterbore diameter 30 mm x 3 mm deep.
# - Longitudinal top flat intent 20 mm wide over 49 mm length.
# - Two tapped radial clamp-hole callouts M4 at X=19 and X=38 mm represented by threaded_hole operations.
# - Radial split relief slit width 2 mm from OD toward bore represented by a through slot.
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
    Stock.cylindrical(61, 57, material="steel_a36")
    .bore(diameter=20, through=True)
    .counterbore(hole_diameter=20, counterbore_diameter=30, counterbore_depth=3, cx=0, cy=0)
    .pocket(width=20, length=49, depth=1.686, cx=0, cy=0)
    .threaded_hole(diameter=4, depth=61, cx=-9.5, cy=0, through=True)
    .threaded_hole(diameter=4, depth=61, cx=9.5, cy=0, through=True)
    .slot(length=20.5, width=2, depth=61, cx=0, cy=10.125, through=True)
)
