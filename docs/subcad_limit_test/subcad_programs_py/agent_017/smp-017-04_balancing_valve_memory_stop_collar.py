# Requirement: SMP-017-04
# Source agent: 017
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_017_hvac_plumbing_hardware_single_metal_parts.json
# Part: Balancing Valve Memory Stop Collar - single metal part
# Raw idea: Balancing Valve Memory Stop Collar
# Status: draft_unexecuted
#
# Coverage notes:
# - Cylindrical stock OD 32 mm x length 73 mm with mapped material steel_1045.
# - Centered through bore diameter 10 mm.
# - One concentric counterbore diameter 20 mm x 3 mm deep.
# - Longitudinal top flat intent 10 mm wide over 65 mm length.
# - Two tapped radial clamp-hole callouts M8 at X=24 and X=48 mm represented by threaded_hole operations.
# - Radial split relief slit width 4 mm from OD toward bore represented by a through slot.
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
    Stock.cylindrical(32, 73, material="steel_1045")
    .bore(diameter=10, through=True)
    .counterbore(hole_diameter=10, counterbore_diameter=20, counterbore_depth=3, cx=0, cy=0)
    .pocket(width=10, length=65, depth=1, cx=0, cy=0)
    .threaded_hole(diameter=8, depth=32, cx=-12.5, cy=0, through=True)
    .threaded_hole(diameter=8, depth=32, cx=11.5, cy=0, through=True)
    .slot(length=11, width=4, depth=32, cx=0, cy=5.25, through=True)
)
