# Requirement: SMP-001-07
# Source agent: 001
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_001_workshop_fixtures_single_metal_parts.json
# Part: Bench Grinder Tool Rest Angle Block - single metal part
# Raw idea: Bench Grinder Tool Rest Angle Block
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 42 mm x length 37 mm using steel_1045
# - centered axial through bore diameter 14 mm
# - concentric end counterbore diameter 24 mm x 3 mm deep
# - longitudinal milled flat 14 mm wide over 29 mm length
# - two M7 radial tapped clamp holes at axial X=12 and X=24
# - full-length split relief slit width 2 mm
# - transverse cross relief slot width 4 mm at axial X=18, depth 4 mm
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
    Stock.cylindrical(42, 37, material="steel_1045")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=14, depth=37)
    .counterbore(hole_diameter=14, counterbore_diameter=24, counterbore_depth=3, cx=0, cy=0, through=True)
    .pocket(width=14, length=29, depth=1.201, cx=0, cy=0)
    .threaded_hole(diameter=7, depth=21, cx=-6.5, cy=0)
    .threaded_hole(diameter=7, depth=21, cx=5.5, cy=0)
    .slot(length=37, width=2, depth=42, cx=0, cy=0, through=True)
    .slot(length=42, width=4, depth=4, angle=90, cx=-0.5, cy=0)
)
