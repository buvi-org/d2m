# Requirement: SMP-013-09
# Source agent: 013
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_013_aerospace_uav_hardware_single_metal_parts.json
# Part: Ground Charging Dock Alignment Cone - single metal part
# Raw idea: Ground Charging Dock Alignment Cone
# Status: draft_unexecuted
#
# Coverage notes:
# - Cylindrical stock OD 60 mm x length 41 mm with mapped material steel_1045.
# - Centered through bore diameter 20 mm.
# - One concentric counterbore diameter 30 mm x 3 mm deep.
# - Longitudinal top flat intent 20 mm wide over 33 mm length.
# - Two tapped radial clamp-hole callouts M4 at X=13 and X=27 mm represented by threaded_hole operations.
# - Radial split relief slit width 5 mm from OD toward bore represented by a through slot.
# - Transverse top relief slot width 7 mm at X=20 mm, depth 6 mm.
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
# - Material source calls for 4140 alloy steel; mapped to steel_1045 because the requested Stage 3 allowed material set has no 4140 key.

from subcad import Stock

part = (
    Stock.cylindrical(60, 41, material="steel_1045")
    .bore(diameter=20, through=True)
    .counterbore(hole_diameter=20, counterbore_diameter=30, counterbore_depth=3, cx=0, cy=0)
    .pocket(width=20, length=33, depth=1.716, cx=0, cy=0)
    .threaded_hole(diameter=4, depth=60, cx=-7.5, cy=0, through=True)
    .threaded_hole(diameter=4, depth=60, cx=6.5, cy=0, through=True)
    .slot(length=20, width=5, depth=60, cx=0, cy=10, through=True)
    .slot(length=60, width=7, depth=6, angle=90, cx=-0.5, cy=0)
)
