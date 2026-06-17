# Requirement: SMP-011-08
# Source agent: 011
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_011_industrial_measurement_fixtures_single_metal_parts.json
# Part: Micrometer Calibration Step Gauge Block - single metal part
# Raw idea: Micrometer Calibration Step Gauge Block
# Status: draft_unexecuted
#
# Coverage notes:
# - Cylindrical stock OD 73 mm x length 49 mm with mapped material steel_a36.
# - Centered through bore diameter 24 mm.
# - One concentric counterbore diameter 34 mm x 3 mm deep.
# - Longitudinal top flat intent 24 mm wide over 41 mm length.
# - Two tapped radial clamp-hole callouts M5 at X=16 and X=32 mm represented by threaded_hole operations.
# - Radial split relief slit width 4 mm from OD toward bore represented by a through slot.
# - Transverse top relief slot width 6 mm at X=24 mm, depth 7 mm.
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

from subcad import Stock

part = (
    Stock.cylindrical(73, 49, material="steel_a36")
    .bore(diameter=24, through=True)
    .counterbore(hole_diameter=24, counterbore_diameter=34, counterbore_depth=3, cx=0, cy=0)
    .pocket(width=24, length=41, depth=2.029, cx=0, cy=0)
    .threaded_hole(diameter=5, depth=73, cx=-8.5, cy=0, through=True)
    .threaded_hole(diameter=5, depth=73, cx=7.5, cy=0, through=True)
    .slot(length=24.5, width=4, depth=73, cx=0, cy=12.125, through=True)
    .slot(length=73, width=6, depth=7, angle=90, cx=-0.5, cy=0)
)
