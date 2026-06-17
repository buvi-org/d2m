# Requirement: SMP-012-08
# Source agent: 012
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_012_agriculture_garden_hardware_single_metal_parts.json
# Part: Cultivator Tine Mounting Socket - single metal part
# Raw idea: Cultivator Tine Mounting Socket
# Status: draft_unexecuted
#
# Coverage notes:
# - Cylindrical stock OD 70 mm x length 116 mm with mapped material steel_a36.
# - Centered through bore diameter 14 mm.
# - One concentric counterbore diameter 24 mm x 3 mm deep.
# - Longitudinal top flat intent 23 mm wide over 108 mm length.
# - Two tapped radial clamp-hole callouts M5 at X=38 and X=77 mm represented by threaded_hole operations.
# - Radial split relief slit width 5 mm from OD toward bore represented by a through slot.
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
    Stock.cylindrical(70, 116, material="steel_a36")
    .bore(diameter=14, through=True)
    .counterbore(hole_diameter=14, counterbore_diameter=24, counterbore_depth=3, cx=0, cy=0)
    .pocket(width=23, length=108, depth=1.943, cx=0, cy=0)
    .threaded_hole(diameter=5, depth=70, cx=-20, cy=0, through=True)
    .threaded_hole(diameter=5, depth=70, cx=19, cy=0, through=True)
    .slot(length=28, width=5, depth=70, cx=0, cy=10.5, through=True)
)
