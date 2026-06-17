# Requirement: SMP-003-08
# Source agent: 003
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_003_kitchen_food_mechanisms_single_metal_parts.json
# Part: Food Processor Bowl Bayonet Lock Ring - single metal part
# Raw idea: Food Processor Bowl Bayonet Lock Ring
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 120 x 45 x 62 mm using stainless_316
# - two through mounting holes diameter 9 mm at X=10/110, Y=22
# - central obround through slot 40 x 17 mm at X=60, Y=22
# - centered top rectangular relief pocket 30 x 18 x 31 mm deep
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.

from subcad import Stock

part = (
    Stock.rectangular(120, 45, 62, material="stainless_316")
    .drill_at(diameter=9, through=True, from_left=10, from_bottom=22, spot_drill=False)
    .drill_at(diameter=9, through=True, from_left=110, from_bottom=22, spot_drill=False)
    .slot_at(length=40, width=17, through=True, from_left=60, from_bottom=22)
    .pocket(width=18, length=30, depth=31, cx=0, cy=0)
)
