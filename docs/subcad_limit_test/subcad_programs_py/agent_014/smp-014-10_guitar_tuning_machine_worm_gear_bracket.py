# Requirement: SMP-014-10
# Source agent: 014
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_014_musical_instrument_hardware_single_metal_parts.json
# Part: Guitar Tuning Machine Worm Gear Bracket - single metal part
# Raw idea: Guitar Tuning Machine Worm Gear Bracket
# Status: draft_unexecuted
#
# Coverage notes:
# - Cylindrical stock OD 48 mm x length 82 mm with mapped material steel_a36.
# - Centered through bore diameter 12 mm.
# - One concentric counterbore diameter 22 mm x 3 mm deep.
# - Longitudinal top flat intent 16 mm wide over 74 mm length.
# - Two tapped radial clamp-hole callouts M6 at X=27 and X=54 mm represented by threaded_hole operations.
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
    Stock.cylindrical(48, 82, material="steel_a36")
    .bore(diameter=12, through=True)
    .counterbore(hole_diameter=12, counterbore_diameter=22, counterbore_depth=3, cx=0, cy=0)
    .pocket(width=16, length=74, depth=1.373, cx=0, cy=0)
    .threaded_hole(diameter=6, depth=48, cx=-14, cy=0, through=True)
    .threaded_hole(diameter=6, depth=48, cx=13, cy=0, through=True)
    .slot(length=18, width=2, depth=48, cx=0, cy=7.5, through=True)
)
