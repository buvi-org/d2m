# Requirement: SMP-013-01
# Source agent: 013
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_013_aerospace_uav_hardware_single_metal_parts.json
# Part: UAV Gimbal Vibration-Isolator Yoke - single metal part
# Raw idea: UAV Gimbal Vibration-Isolator Yoke
# Status: draft_unexecuted
#
# Coverage notes:
# - Cylindrical stock OD 84 mm x length 64 mm with mapped material aluminum_6061.
# - Centered through bore diameter 16 mm.
# - One concentric counterbore diameter 26 mm x 3 mm deep.
# - Longitudinal top flat intent 28 mm wide over 56 mm length.
# - Two tapped radial clamp-hole callouts M6 at X=21 and X=42 mm represented by threaded_hole operations.
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

from subcad import Stock

part = (
    Stock.cylindrical(84, 64, material="aluminum_6061")
    .bore(diameter=16, through=True)
    .counterbore(hole_diameter=16, counterbore_diameter=26, counterbore_depth=3, cx=0, cy=0)
    .pocket(width=28, length=56, depth=2.402, cx=0, cy=0)
    .threaded_hole(diameter=6, depth=84, cx=-11, cy=0, through=True)
    .threaded_hole(diameter=6, depth=84, cx=10, cy=0, through=True)
    .slot(length=34, width=2, depth=84, cx=0, cy=12.5, through=True)
)
