# Requirement: SMP-017-08
# Source agent: 017
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_017_hvac_plumbing_hardware_single_metal_parts.json
# Part: Pressure Reducing Valve Pilot Tubing Bracket - single metal part
# Raw idea: Pressure Reducing Valve Pilot Tubing Bracket
# Status: draft_unexecuted
#
# Coverage notes:
# - Cylindrical stock OD 59 mm x length 24 mm with mapped material steel_1045.
# - Centered through bore diameter 11 mm.
# - One concentric counterbore diameter 21 mm x 3 mm deep.
# - Longitudinal top flat intent 19 mm wide over 16 mm length.
# - Two tapped radial clamp-hole callouts M5 at X=8 and X=16 mm represented by threaded_hole operations.
# - Radial split relief slit width 5 mm from OD toward bore represented by a through slot.
# - Transverse top relief slot width 7 mm at X=12 mm, depth 5 mm.
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
    Stock.cylindrical(59, 24, material="steel_1045")
    .bore(diameter=11, through=True)
    .counterbore(hole_diameter=11, counterbore_diameter=21, counterbore_depth=3, cx=0, cy=0)
    .pocket(width=19, length=16, depth=1.572, cx=0, cy=0)
    .threaded_hole(diameter=5, depth=59, cx=-4, cy=0, through=True)
    .threaded_hole(diameter=5, depth=59, cx=4, cy=0, through=True)
    .slot(length=24, width=5, depth=59, cx=0, cy=8.75, through=True)
    .slot(length=59, width=7, depth=5, angle=90, cx=0, cy=0)
)
