# Requirement: SMP-011-10
# Source agent: 011
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_011_industrial_measurement_fixtures_single_metal_parts.json
# Part: Torque Sensor Reaction Arm Hub - single metal part
# Raw idea: Torque Sensor Reaction Arm Hub
# Status: draft_unexecuted
#
# Coverage notes:
# - Cylindrical stock OD 33 mm x length 92 mm with mapped material steel_a36.
# - Centered through bore diameter 11 mm.
# - One concentric counterbore diameter 21 mm x 3 mm deep.
# - Longitudinal top flat intent 11 mm wide over 84 mm length.
# - Two tapped radial clamp-hole callouts M8 at X=30 and X=61 mm represented by threaded_hole operations.
# - Radial split relief slit width 3 mm from OD toward bore represented by a through slot.
# - Transverse top relief slot width 5 mm at X=46 mm, depth 3 mm.
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
    Stock.cylindrical(33, 92, material="steel_a36")
    .bore(diameter=11, through=True)
    .counterbore(hole_diameter=11, counterbore_diameter=21, counterbore_depth=3, cx=0, cy=0)
    .pocket(width=11, length=84, depth=1, cx=0, cy=0)
    .threaded_hole(diameter=8, depth=33, cx=-16, cy=0, through=True)
    .threaded_hole(diameter=8, depth=33, cx=15, cy=0, through=True)
    .slot(length=11, width=3, depth=33, cx=0, cy=5.5, through=True)
    .slot(length=33, width=5, depth=3, angle=90, cx=0, cy=0)
)
