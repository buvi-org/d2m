# Requirement: SMP-001-02
# Source agent: 001
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_001_workshop_fixtures_single_metal_parts.json
# Part: Adjustable Drill Press Depth Stop Collar - single metal part
# Raw idea: Adjustable Drill Press Depth Stop Collar
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 86 mm x length 108 mm using steel_1045
# - centered axial through bore diameter 28 mm
# - concentric end counterbore diameter 38 mm x 3 mm deep
# - longitudinal milled flat 28 mm wide over 100 mm length
# - two M6 radial tapped clamp holes at axial X=36 and X=72
# - full-length split relief slit width 3 mm
# - transverse cross relief slot width 5 mm at axial X=54, depth 8 mm
# - 1.0 mm outside edge chamfer pass
#
# Known gaps:
# - requirement datum says cylinder axis is X; Stock.cylindrical is used with its native cylinder axis for this draft
# - counterbores called from one accessible face; opposite-end counterbore remains an approximation
# - milled cylindrical flat is approximated by a rectangular top pocket/chord cut
# - radial tapped holes through a top flat are represented as top-face threaded holes at matching axial offsets
# - slit from outside to axial bore is approximated by a full top-face through slot
# - internal bore mouth chamfers are noted but not separately modeled with targeted bore-edge selections
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.

from subcad import Stock

part = (
    Stock.cylindrical(86, 108, material="steel_1045")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=28, depth=108)
    .counterbore(hole_diameter=28, counterbore_diameter=38, counterbore_depth=3, cx=0, cy=0, through=True)
    .pocket(width=28, length=100, depth=2.343, cx=0, cy=0)
    .threaded_hole(diameter=6, depth=43, cx=-18, cy=0)
    .threaded_hole(diameter=6, depth=43, cx=18, cy=0)
    .slot(length=108, width=3, depth=86, cx=0, cy=0, through=True)
    .slot(length=86, width=5, depth=8, angle=90, cx=0, cy=0)
)
