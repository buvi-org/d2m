# Requirement: SMP-018-10
# Source agent: 018
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_018_sports_fitness_rehab_single_metal_parts.json
# Part: Resistance Sled Harness Tow Cleat - single metal part
# Raw idea: Resistance Sled Harness Tow Cleat
# Status: draft_unexecuted
#
# Coverage notes:
# - Cylindrical stock OD 52 mm x length 44 mm with mapped material steel_1045.
# - Centered through bore diameter 17 mm.
# - One concentric counterbore diameter 27 mm x 3 mm deep.
# - Longitudinal top flat intent 17 mm wide over 36 mm length.
# - Two tapped radial clamp-hole callouts M8 at X=14 and X=29 mm represented by threaded_hole operations.
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
# - Material source calls for 4140 alloy steel; mapped to steel_1045 because the requested Stage 3 allowed material set has no 4140 key.

from subcad import Stock

part = (
    Stock.cylindrical(52, 44, material="steel_1045")
    .bore(diameter=17, through=True)
    .counterbore(hole_diameter=17, counterbore_diameter=27, counterbore_depth=3, cx=0, cy=0)
    .pocket(width=17, length=36, depth=1.429, cx=0, cy=0)
    .threaded_hole(diameter=8, depth=52, cx=-8, cy=0, through=True)
    .threaded_hole(diameter=8, depth=52, cx=7, cy=0, through=True)
    .slot(length=17.5, width=2, depth=52, cx=0, cy=8.625, through=True)
)
