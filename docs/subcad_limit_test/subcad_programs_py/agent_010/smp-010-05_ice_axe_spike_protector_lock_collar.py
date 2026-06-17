# Requirement: SMP-010-05
# Source agent: 010
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_010_outdoor_marine_field_gear_single_metal_parts.json
# Part: Ice Axe Spike Protector Lock Collar - single metal part
# Raw idea: Ice Axe Spike Protector Lock Collar
# Status: draft_unexecuted
#
# Coverage notes:
# - Cylindrical stock OD 34 mm x length 29 mm with mapped material steel_1045.
# - Centered through bore diameter 11 mm.
# - One concentric counterbore diameter 21 mm x 3 mm deep.
# - Longitudinal top flat intent 11 mm wide over 21 mm length.
# - Two tapped radial clamp-hole callouts M5 at X=9 and X=19 mm represented by threaded_hole operations.
# - Radial split relief slit width 3 mm from OD toward bore represented by a through slot.
# - Transverse top relief slot width 5 mm at X=14 mm, depth 3 mm.
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
    Stock.cylindrical(34, 29, material="steel_1045")
    .bore(diameter=11, through=True)
    .counterbore(hole_diameter=11, counterbore_diameter=21, counterbore_depth=3, cx=0, cy=0)
    .pocket(width=11, length=21, depth=1, cx=0, cy=0)
    .threaded_hole(diameter=5, depth=34, cx=-5.5, cy=0, through=True)
    .threaded_hole(diameter=5, depth=34, cx=4.5, cy=0, through=True)
    .slot(length=11.5, width=3, depth=34, cx=0, cy=5.625, through=True)
    .slot(length=34, width=5, depth=3, angle=90, cx=-0.5, cy=0)
)
