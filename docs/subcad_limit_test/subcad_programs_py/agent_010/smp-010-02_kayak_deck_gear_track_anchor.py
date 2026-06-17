# Requirement: SMP-010-02
# Source agent: 010
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_010_outdoor_marine_field_gear_single_metal_parts.json
# Part: Kayak Deck Gear Track Anchor - single metal part
# Raw idea: Kayak Deck Gear Track Anchor
# Status: draft_unexecuted
#
# Coverage notes:
# - Cylindrical stock OD 49 mm x length 68 mm with mapped material steel_1045.
# - Centered through bore diameter 16 mm.
# - One concentric counterbore diameter 26 mm x 3 mm deep.
# - Longitudinal top flat intent 16 mm wide over 60 mm length.
# - Two tapped radial clamp-hole callouts M7 at X=22 and X=45 mm represented by threaded_hole operations.
# - Radial split relief slit width 2 mm from OD toward bore represented by a through slot.
# - Transverse top relief slot width 4 mm at X=34 mm, depth 4 mm.
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
    Stock.cylindrical(49, 68, material="steel_1045")
    .bore(diameter=16, through=True)
    .counterbore(hole_diameter=16, counterbore_diameter=26, counterbore_depth=3, cx=0, cy=0)
    .pocket(width=16, length=60, depth=1.343, cx=0, cy=0)
    .threaded_hole(diameter=7, depth=49, cx=-12, cy=0, through=True)
    .threaded_hole(diameter=7, depth=49, cx=11, cy=0, through=True)
    .slot(length=16.5, width=2, depth=49, cx=0, cy=8.125, through=True)
    .slot(length=49, width=4, depth=4, angle=90, cx=0, cy=0)
)
