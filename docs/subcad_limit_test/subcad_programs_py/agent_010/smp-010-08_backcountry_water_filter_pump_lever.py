# Requirement: SMP-010-08
# Source agent: 010
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_010_outdoor_marine_field_gear_single_metal_parts.json
# Part: Backcountry Water Filter Pump Lever - single metal part
# Raw idea: Backcountry Water Filter Pump Lever
# Status: draft_unexecuted
#
# Coverage notes:
# - Cylindrical stock OD 62 mm x length 83 mm with mapped material steel_a36.
# - Centered through bore diameter 12 mm.
# - One concentric counterbore diameter 22 mm x 3 mm deep.
# - Longitudinal top flat intent 20 mm wide over 75 mm length.
# - Two tapped radial clamp-hole callouts M8 at X=27 and X=55 mm represented by threaded_hole operations.
# - Radial split relief slit width 5 mm from OD toward bore represented by a through slot.
# - Transverse top relief slot width 7 mm at X=41 mm, depth 6 mm.
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
    Stock.cylindrical(62, 83, material="steel_a36")
    .bore(diameter=12, through=True)
    .counterbore(hole_diameter=12, counterbore_diameter=22, counterbore_depth=3, cx=0, cy=0)
    .pocket(width=20, length=75, depth=1.657, cx=0, cy=0)
    .threaded_hole(diameter=8, depth=62, cx=-14.5, cy=0, through=True)
    .threaded_hole(diameter=8, depth=62, cx=13.5, cy=0, through=True)
    .slot(length=25, width=5, depth=62, cx=0, cy=9.25, through=True)
    .slot(length=62, width=7, depth=6, angle=90, cx=-0.5, cy=0)
)
