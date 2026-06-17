# Requirement: SMP-011-09
# Source agent: 011
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_011_industrial_measurement_fixtures_single_metal_parts.json
# Part: Conductivity Probe Flow Cell Body - single metal part
# Raw idea: Conductivity Probe Flow Cell Body
# Status: draft_unexecuted
#
# Coverage notes:
# - Cylindrical stock OD 69 mm x length 73 mm with mapped material steel_a36.
# - Centered through bore diameter 13 mm.
# - One concentric counterbore diameter 23 mm x 3 mm deep.
# - Longitudinal top flat intent 23 mm wide over 65 mm length.
# - Two tapped radial clamp-hole callouts M4 at X=24 and X=48 mm represented by threaded_hole operations.
# - Radial split relief slit width 6 mm from OD toward bore represented by a through slot.
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
    Stock.cylindrical(69, 73, material="steel_a36")
    .bore(diameter=13, through=True)
    .counterbore(hole_diameter=13, counterbore_diameter=23, counterbore_depth=3, cx=0, cy=0)
    .pocket(width=23, length=65, depth=1.973, cx=0, cy=0)
    .threaded_hole(diameter=4, depth=69, cx=-12.5, cy=0, through=True)
    .threaded_hole(diameter=4, depth=69, cx=11.5, cy=0, through=True)
    .slot(length=28, width=6, depth=69, cx=0, cy=10.25, through=True)
)
