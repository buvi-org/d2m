# Requirement: SMP-042-24
# Source agent: 042
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_042_glass_handling_hardware_single_metal_parts.json
# Part: Glass Washer Rack Finger Insert - single metal part
# Raw idea: Glass Washer Rack Finger Insert
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 195 x 85 x 69 mm using steel_a36
# - two through mounting holes diameter 7 mm at X=17/178, Y=42
# - central obround through slot 65 x 10 mm at X=97, Y=42
# - centered top rectangular relief pocket 48 x 28 x 14 mm deep
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted by this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.
# - Rectangular/sheet X/Y feature placement uses drill_at/slot_at/pocket_at datum offsets from the lower-left requirement origin where applicable.

from subcad import Stock

part = (
    Stock.rectangular(195, 85, 69, material="steel_a36")
    .drill_at(diameter=7, through=True, from_left=17, from_bottom=42, spot_drill=False)
    .drill_at(diameter=7, through=True, from_left=178, from_bottom=42, spot_drill=False)
    .slot_at(length=65, width=10, through=True, from_left=97, from_bottom=42)
    .pocket_at(width=28, length=48, depth=14, from_left=97, from_bottom=42)
)
