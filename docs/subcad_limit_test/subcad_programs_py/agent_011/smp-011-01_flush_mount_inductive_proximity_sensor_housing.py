# Requirement: SMP-011-01
# Source agent: 011
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_011_industrial_measurement_fixtures_single_metal_parts.json
# Part: Flush-Mount Inductive Proximity Sensor Housing - single metal part
# Raw idea: Flush-Mount Inductive Proximity Sensor Housing
# Status: draft_unexecuted
#
# Coverage notes:
# - Cylindrical stock OD 83 mm x length 115 mm with mapped material steel_1045.
# - Centered through bore diameter 27 mm.
# - One concentric counterbore diameter 37 mm x 3 mm deep.
# - Longitudinal top flat intent 27 mm wide over 107 mm length.
# - Two tapped radial clamp-hole callouts M7 at X=38 and X=76 mm represented by threaded_hole operations.
# - Radial split relief slit width 4 mm from OD toward bore represented by a through slot.
# - Opposed wrench flats intent leaving 75 mm across flats over the middle third.
# - 1.0 mm outside circular edge break represented with Stock.chamfer.
#
# Known gaps:
# - Requirement datum says cylinder axis is X; Stock.cylindrical and top-face bore are Z-axis oriented, so axial orientation must be reviewed.
# - Counterbores are required on both ends; this draft only represents the accessible top/end counterbore.
# - Milled flat is approximated by a shallow rectangular pocket on the top of the cylindrical stock, not an exact chordal flat.
# - Radial tapped holes through the top flat are represented in Stock top-face coordinates; true radial orientation and thread sidewall are not exact.
# - Split relief slit is approximated as a top-face through slot; exact OD-to-bore radial cut on datum-B side needs review.
# - Opposed wrench flats are approximated as a single top flat/pocket; the opposite flat and exact across-flats geometry are not represented.
# - Internal bore-mouth chamfers are not independently selectable in this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Round-bar programs use Stock.cylindrical(diameter, height) per the generation guide; axis convention may differ from the frozen X-axis requirement text.
# - Material source calls for 4140 alloy steel; mapped to steel_1045 because the requested Stage 3 allowed material set has no 4140 key.

from subcad import Stock

part = (
    Stock.cylindrical(83, 115, material="steel_1045")
    .bore(diameter=27, through=True)
    .counterbore(hole_diameter=27, counterbore_diameter=37, counterbore_depth=3, cx=0, cy=0)
    .pocket(width=27, length=107, depth=2.257, cx=0, cy=0)
    .threaded_hole(diameter=7, depth=83, cx=-19.5, cy=0, through=True)
    .threaded_hole(diameter=7, depth=83, cx=18.5, cy=0, through=True)
    .slot(length=28, width=4, depth=83, cx=0, cy=13.75, through=True)
    .pocket(width=83, length=38.333, depth=4, cx=0, cy=0)
)
