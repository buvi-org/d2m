# Requirement: SMP-014-07
# Source agent: 014
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_014_musical_instrument_hardware_single_metal_parts.json
# Part: Cymbal Stand Memory Lock - single metal part
# Raw idea: Cymbal Stand Memory Lock
# Status: draft_unexecuted
#
# Coverage notes:
# - Cylindrical stock OD 66 mm x length 112 mm with mapped material steel_1045.
# - Centered through bore diameter 13 mm.
# - One concentric counterbore diameter 23 mm x 3 mm deep.
# - Longitudinal top flat intent 22 mm wide over 104 mm length.
# - Two tapped radial clamp-hole callouts M6 at X=37 and X=74 mm represented by threaded_hole operations.
# - Radial split relief slit width 3 mm from OD toward bore represented by a through slot.
# - Transverse top relief slot width 5 mm at X=56 mm, depth 6 mm.
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
    Stock.cylindrical(66, 112, material="steel_1045")
    .bore(diameter=13, through=True)
    .counterbore(hole_diameter=13, counterbore_diameter=23, counterbore_depth=3, cx=0, cy=0)
    .pocket(width=22, length=104, depth=1.887, cx=0, cy=0)
    .threaded_hole(diameter=6, depth=66, cx=-19, cy=0, through=True)
    .threaded_hole(diameter=6, depth=66, cx=18, cy=0, through=True)
    .slot(length=26.5, width=3, depth=66, cx=0, cy=9.875, through=True)
    .slot(length=66, width=5, depth=6, angle=90, cx=0, cy=0)
)
