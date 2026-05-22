"""Self-tests for agentic_translator.py — tests all non-LLM components.

Run:  python test_agentic_translator.py

To test with a real LLM, set DEEPSEEK_API_KEY and run:
  python test_agentic_translator.py --live
"""

import json
import os
import sys
import tempfile

# --- Test helpers ---

passed = 0
failed = 0

def check(cond, label):
    global passed, failed
    if cond:
        passed += 1
        print(f"  PASS  {label}")
    else:
        failed += 1
        print(f"  FAIL  {label}")


# =========================================================================
#  Test 1: Imports
# =========================================================================

print("1. Module imports ...")
from src.data.agentic_translator import (
    AgenticTranslator,
    LLMClient,
    extract_code,
    build_system_prompt,
    build_user_prompt,
    build_iteration_prompt,
    translate_exploration_sample,
    translate_batch,
    SUBCAD_API_REFERENCE,
    _extract_measures_block,
    _validate_generated_subcad_code,
)
from src.data.run_agentic_translation import build_dry_run_preview
from src.data.run_zero_to_cad_translations import (
    _apply_match_policy,
    _parse_methods,
    compatibility_report,
)
import src.data.run_zero_to_cad_feature_benchmarks as feature_benchmark_mod
from src.data.pure_subcad_planner import build_deterministic_subcad_code, plan_pure_subcad_features
import src.data.agentic_translator as agentic_mod

from src.data.subcad_repl import run_subcad, compare_to_reference, format_feedback
from src.data.cadquery_to_subcad import reconstruct_chains, classify_chain, _extract_measures

check(True, "all imports successful")


# =========================================================================
#  Test 1b: Correct Zero-to-CAD benchmark runner policy
# =========================================================================

print("\n1b. Zero-to-CAD benchmark runner policy ...")
planned = compatibility_report([{"op_name": "fillet"}, {"op_name": "union"}], "part = workplane.union(other)")
check(planned["compatible"], "compatibility gate plans fillet/union as pure operations")
check(planned["planner"]["coverage_mode"] == "pure_subcad_operations",
      "compatibility gate returns typed pure planner output")
chamfered = compatibility_report([{"op_name": "chamfer"}], "")
check(chamfered["compatible"], "compatibility gate plans local chamfer samples")
planner = plan_pure_subcad_features(
    [{"op_name": "revolve"}, {"op_name": "shell", "function": "part.faces.shell"}, {"op_name": "loft"}],
    '.revolve().faces(">Z").shell(1).loft()',
)
ops = {feature.operation for feature in planner.features}
check({"turn_profile", "thin_wall_pocket", "loft_mill"}.issubset(ops),
      "pure planner maps revolve/shell/loft to CNC operation families")
closed_shell = plan_pure_subcad_features(
    [{"op_name": "shell", "function": "base.shell"}],
    ".box(10, 10, 10).shell(-1)",
)
check(not closed_shell.compatible, "pure planner rejects closed inaccessible shells")
assigned_closed_shell = plan_pure_subcad_features(
    [
        {"op_name": "hole", "function": "cq.Workplane.box.faces.hole"},
        {"op_name": "shell", "function": "solid.shell"},
    ],
    "solid = cq.Workplane('XY').box(30,30,30).faces('>Z').hole(10)\n"
    "result = solid.shell(-2)",
)
check(not assigned_closed_shell.compatible,
      "pure planner rejects assigned closed shells after face-hole construction")
original_iter_rows = feature_benchmark_mod.iter_zero_to_cad_rows
try:
    unsupported_row = {
        "global_index": 123456,
        "uuid": "unsupported-ai-heavy-row",
        "parquet_file": "unit.parquet",
        "row_index": 0,
        "ops_trace": [{"op_name": "shell", "function": "base.shell"}],
        "cadquery_code": "base = cq.Workplane('XY').box(10, 10, 10).shell(1)",
    }

    def _single_unsupported_row(*args, **kwargs):
        yield dict(unsupported_row)

    def _mock_executor(row, context):
        return {"executed": True, "matched": False, "failed": True, "sample_dir": ""}

    feature_benchmark_mod.iter_zero_to_cad_rows = _single_unsupported_row
    skipped_summary = feature_benchmark_mod.run_feature_family_benchmark(
        scan_limit=1,
        dry_run=False,
        executor=_mock_executor,
        write_summary=False,
        max_attempts=1,
    )
    attempted_summary = feature_benchmark_mod.run_feature_family_benchmark(
        scan_limit=1,
        dry_run=False,
        executor=_mock_executor,
        write_summary=False,
        max_attempts=1,
        attempt_unsupported=True,
    )
finally:
    feature_benchmark_mod.iter_zero_to_cad_rows = original_iter_rows
check(skipped_summary["attempted"] == 0,
      "feature runner skips planner-unsupported rows by default")
check(attempted_summary["attempted"] == 1,
      "feature runner can attempt planner-unsupported rows for AI-heavy pilots")
check(attempted_summary["unsupported"] == 1,
      "AI-heavy unsupported attempts keep unsupported accounting")
check(_parse_methods("none") == [], "comparison-methods=none disables rich mesh comparison")

volume_only_false_positive = {
    "success": True,
    "comparison": {"match": True, "volume_ratio": 0.997},
    "mesh_comparison": {
        "score": 0.0,
        "sdf": {"rms_error": 3.3, "max_overcut": 8.7, "max_undercut": -2.2},
        "slice": {"problem_slices": [{"z": 1.0}]},
    },
}
strict_result = _apply_match_policy(
    volume_only_false_positive,
    comparison_methods=["sdf", "slice"],
    trusted_tolerance_mm=0.25,
    min_mesh_score=95.0,
    volume_only_success=False,
)
check(strict_result["translator_success"], "runner preserves raw translator volume success")
check(not strict_result["success"], "runner rejects volume-only false positive as trusted match")
check(strict_result["match_policy"]["status"] == "trusted_fail", "runner records trusted failure reason")

volume_mismatch_result = _apply_match_policy(
    {
        "success": True,
        "comparison": {"match": True, "volume_ratio": 0.914},
        "mesh_comparison": {
            "score": 100.0,
            "sdf": {"rms_error": 0.0, "max_overcut": 0.0, "max_undercut": 0.0},
            "slice": {"problem_slices": []},
        },
    },
    comparison_methods=["sdf", "slice"],
    trusted_tolerance_mm=0.25,
    min_mesh_score=95.0,
    volume_only_success=False,
    volume_tolerance=0.05,
)
check(not volume_mismatch_result["success"],
      "runner rejects mesh-perfect rows outside trusted volume tolerance")
check(volume_mismatch_result["match_policy"]["status"] == "volume_mismatch",
      "runner records strict volume mismatch before mesh trust")
check(_validate_generated_subcad_code("part = Stock.rectangular(10, 10, 5)") is None,
      "generated SubCAD validator accepts concise executable code")
check(_validate_generated_subcad_code("# harmless-looking comment\npart = Stock.rectangular(10, 10, 5)") is not None,
      "generated SubCAD validator rejects all comment lines")
check(_validate_generated_subcad_code("# Let me try a few approaches\npart = Stock.rectangular(10, 10, 5)") is not None,
      "generated SubCAD validator rejects exploratory reasoning comments")
check(_validate_generated_subcad_code("part = Stock.rectangular(10, 10, 5)\npass") is not None,
      "generated SubCAD validator rejects pass placeholders")
check(_validate_generated_subcad_code("stock = Stock.rectangular(10, 10, 5)") is not None,
      "generated SubCAD validator requires final part assignment")
timeout_result = feature_benchmark_mod._translation_timeout_result(12.5)
check(timeout_result["stop_reason"] == "row_timeout" and not timeout_result["success"],
      "feature runner records row wall-clock timeouts as failed translation results")

trusted_result = _apply_match_policy(
    {
        "success": True,
        "comparison": {"match": True, "volume_ratio": 1.0},
        "mesh_comparison": {
            "score": 99.0,
            "sdf": {"rms_error": 0.01, "max_overcut": 0.02, "max_undercut": -0.01},
            "slice": {"problem_slices": []},
        },
    },
    comparison_methods=["sdf", "slice"],
    trusted_tolerance_mm=0.25,
    min_mesh_score=95.0,
    volume_only_success=False,
)
check(trusted_result["success"], "runner accepts volume and mesh trusted match")

blind_hole_code = build_deterministic_subcad_code(
    "import cadquery as cq\n"
    "result = cq.Workplane('XY').box(10,10,10).faces('>Z').workplane().hole(4,2)",
    [{"op_name": "box"}, {"op_name": "hole"}],
)
check(blind_hole_code is not None and ".drill(4, depth=2, through=False" in blind_hole_code,
      "deterministic box hole preserves explicit blind depth")

through_hole_code = build_deterministic_subcad_code(
    "import cadquery as cq\n"
    "result = cq.Workplane('XY').box(10,10,10).faces('>Z').workplane().hole(4)",
    [{"op_name": "box"}, {"op_name": "hole"}],
)
check(through_hole_code is not None and ".drill(4, through=True" in through_hole_code,
      "deterministic box hole keeps implicit through hole")

panel_loop_code = build_deterministic_subcad_code(
    "\n".join([
        "import cadquery as cq",
        "panel_width = 100",
        "panel_height = 70",
        "panel_thickness = 3",
        "cutout_width = 60",
        "cutout_height = 30",
        "hole_radius = 2",
        "hole_spacing = 12",
        "hole_count = 5",
        "edge_margin = 8",
        "edge_fillet_radius = 1",
        "result = cq.Workplane('XY').box(panel_width, panel_height, panel_thickness)",
        "result = result.faces('>Z').workplane().center(0, 0).rect(cutout_width, cutout_height).cutThruAll()",
        "start_x = -panel_width/2 + edge_margin",
        "for i in range(hole_count):",
        "    result = result.faces('>Z').workplane().center(start_x + i*hole_spacing, panel_height/2 - edge_margin).hole(hole_radius*2)",
        "result = result.faces('>X or <X or >Y or <Y').edges().fillet(edge_fillet_radius)",
    ]),
    [{"op_name": "box"}, {"op_name": "cutThruAll"}, {"op_name": "hole"}, {"op_name": "fillet"}],
)
check(panel_loop_code is not None and ".profile_pocket(" in panel_loop_code,
      "deterministic panel preserves rectangular through cutout")
check(panel_loop_code is not None and panel_loop_code.count(".drill(4, through=True") == 5,
      "deterministic panel expands loop-built hole row")
check(panel_loop_code is not None and ".edge_fillet(\"|Z\", radius=1" in panel_loop_code,
      "deterministic panel preserves side-edge fillet intent")

transformed_csk_code = build_deterministic_subcad_code(
    "\n".join([
        "import cadquery as cq",
        "main_r=15.0",
        "result = (",
        "    cq.Workplane(\"XY\").box(10,10,10)",
        "    .transformed(offset=cq.Vector(0, main_r, 0), rotate=cq.Vector(-90,0,0))",
        "    .cskHole(4,5,90)",
        ")",
    ]),
    [{"op_name": "box"}, {"op_name": "transformed"}, {"op_name": "cskHole"}],
)
check(transformed_csk_code is not None and 'face_selector=">Y"' in transformed_csk_code,
      "deterministic transformed cskHole maps to side-face intent")

side_extrude_hole_code = build_deterministic_subcad_code(
    "\n".join([
        "import cadquery as cq",
        "arm_length=80.0;arm_width=30.0;arm_thickness=10.0;pivot_diameter=8.0",
        "base = cq.Workplane('YZ').rect(arm_width, arm_thickness).extrude(arm_length)",
        "base = base.faces('>X').hole(pivot_diameter)",
        "result = base",
    ]),
    [{"op_name": "rect"}, {"op_name": "extrude"}, {"op_name": "faces"}, {"op_name": "hole"}],
)
check(side_extrude_hole_code is not None and "Stock.rectangular(80" in side_extrude_hole_code,
      "deterministic YZ extrude preserves X-length stock")
check(side_extrude_hole_code is not None and 'face_selector=">X"' in side_extrude_hole_code,
      "deterministic YZ extrude maps hole to side face")

open_shell_code = build_deterministic_subcad_code(
    "import cadquery as cq\n"
    "result = cq.Workplane('XY').box(80,50,30, centered=(True,True,False))\n"
    "result = result.faces('>Z').shell(-3)",
    [{"op_name": "box"}, {"op_name": "faces"}, {"op_name": "shell", "function": "part.faces.shell"}],
)
check(open_shell_code is not None and ".thin_wall_pocket(" in open_shell_code,
      "deterministic open box shell maps to thin-wall pocket")
check(open_shell_code is not None and "depth=30" in open_shell_code,
      "deterministic open shell removes the selected-face cavity through the stock")

profile_side_drill_code = build_deterministic_subcad_code(
    "\n".join([
        "import cadquery as cq",
        "pts=[(-25,-35),(-25,35),(25,35),(25,33),(-23,33),(-23,-33),(25,-33),(25,-35)]",
        "result = (",
        "    cq.Workplane('XY').polyline(pts).close().extrude(80)",
        "    .edges().chamfer(0.5)",
        "    .faces('<X').workplane()",
        "    .rarray(0, 12, 1, 5, center=True)",
        "    .hole(3)",
        ")",
    ]),
    [{"op_name": "polyline"}, {"op_name": "extrude"}, {"op_name": "rarray"}, {"op_name": "hole"}],
)
check(profile_side_drill_code is not None and profile_side_drill_code.count('.drill(3, through=True') == 5,
      "deterministic profile extrude expands side-face rarray holes")
check(profile_side_drill_code is not None and 'face_selector=">X"' in profile_side_drill_code,
      "deterministic profile side holes map mirrored SubCAD side face")

cross_arm_code = build_deterministic_subcad_code(
    "\n".join([
        "import cadquery as cq",
        "block_width=30.0; block_depth=30.0; block_thickness=10.0",
        "arm_length=40.0; arm_width=15.0; hole_diameter=8.0",
        "chamfer_distance=2.0; tap_depth=block_thickness-2.0; fillet_radius=0.5; epsilon=0.1",
        "result = cq.Workplane('XY').rect(block_width, block_depth).extrude(block_thickness)",
        "for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:",
        "    arm = cq.Workplane('XY').center(dx, dy).rect(arm_length, arm_width).extrude(block_thickness)",
        "    result = result.union(arm)",
        "for direction, face_selector in [((1,0), '>X'),((-1,0), '<X'),((0,1), '>Y'),((0,-1), '<Y')]:",
        "    result = result.faces(face_selector).workplane(centerOption='CenterOfMass').hole(hole_diameter, depth=tap_depth)",
    ]),
    [{"op_name": "rect"}, {"op_name": "union"}, {"op_name": "hole"}],
)
check(cross_arm_code is not None and ".machine_around_profiles(" in cross_arm_code,
      "deterministic looped cross arms map to retained profile islands")
check(cross_arm_code is not None and cross_arm_code.count(".drill(8") == 4,
      "deterministic looped cross arms preserve side-face holes")

rect_cross_code = build_deterministic_subcad_code(
    "\n".join([
        "import cadquery as cq",
        "vertical=cq.Workplane('XY').rect(12,80).extrude(8)",
        "horizontal=cq.Workplane('XY').rect(80,12).extrude(8)",
        "result=vertical.union(horizontal)",
    ]),
    [{"op_name": "rect"}, {"op_name": "extrude"}, {"op_name": "union"}],
)
check(rect_cross_code is not None and ".machine_around_profiles(" in rect_cross_code,
      "deterministic two-rectangle cross union maps to retained profiles")
check(rect_cross_code is not None and "Stock.rectangular(80, 80, 8)" in rect_cross_code,
      "deterministic two-rectangle cross union sizes stock to the combined envelope")

sketch_cross_code = build_deterministic_subcad_code(
    "\n".join([
        "import cadquery as cq",
        "arm_half_length=35; bar_width=15; bar_thickness=10",
        "pilot_diameter=12; pilot_depth=12; hole_diameter=5; hole_depth=8",
        "hole_offset_factor=0.6; fillet_radius=2; edge_fillet_radius=0.5",
        "cross_sketch = cq.Sketch().rect(bar_width, 2 * arm_half_length + bar_width).rect(2 * arm_half_length + bar_width, bar_width)",
        "base = cq.Workplane('XY').placeSketch(cross_sketch).extrude(bar_thickness)",
        "base = base.faces('+Z').workplane().pushPoints([(21,0),(-21,0),(0,21),(0,-21)]).hole(hole_diameter, depth=hole_depth)",
        "pilot = cq.Workplane('XY').circle(pilot_diameter / 2).extrude(pilot_depth).translate((0, 0, bar_thickness))",
        "result = base.union(pilot)",
    ]),
    [{"op_name": "Sketch"}, {"op_name": "rect"}, {"op_name": "circle"}, {"op_name": "union"}],
)
check(sketch_cross_code is not None and ".machine_around_cylinder(12" in sketch_cross_code,
      "deterministic sketch cross preserves center pilot boss")
check(sketch_cross_code is not None and sketch_cross_code.count(".drill(5") == 4,
      "deterministic sketch cross preserves four blind holes")

line_cutout_code = build_deterministic_subcad_code(
    "\n".join([
        "import cadquery as cq",
        "result = cq.Workplane('XY').box(20,20,2)",
        "result = result.faces('>Z').workplane()",
        "result = result.moveTo(-5,-5).lineTo(5,-5).lineTo(5,5).lineTo(-5,5).close().cutThruAll()",
    ]),
    [{"op_name": "box"}, {"op_name": "moveTo"}, {"op_name": "lineTo"}, {"op_name": "cutThruAll"}],
)
check(line_cutout_code is not None and ".profile_pocket(" in line_cutout_code,
      "deterministic box line-chain through cutout maps to profile pocket")
check(line_cutout_code is not None and "through=True" in line_cutout_code,
      "deterministic box line-chain cutout preserves through cut")

panel_rib_holes_code = build_deterministic_subcad_code(
    "\n".join([
        "import cadquery as cq",
        "panel_width=80; panel_height=60; panel_thickness=5; chamfer_size=1",
        "rib_count=3; rib_spacing=panel_height / (rib_count + 1); rib_width=panel_width * 0.9",
        "rib_thickness=1.5; rib_depth=1.5; hole_diameter=4; hole_spacing=8; hole_row_y=panel_height/4",
        "result = cq.Workplane('XY').rect(panel_width, panel_height).extrude(panel_thickness).edges('|Z').chamfer(chamfer_size)",
        "for i in range(rib_count):",
        "    y_pos = -panel_height/2 + (i + 1) * rib_spacing",
        "    result = result.faces('>Z').workplane().center(0, y_pos).rect(rib_width, rib_thickness).cutBlind(rib_depth)",
        "for i in range(8):",
        "    x_pos = -((7/2) * hole_spacing) + i * hole_spacing",
        "    result = result.faces('>Z').workplane().center(x_pos, hole_row_y).hole(hole_diameter)",
    ]),
    [{"op_name": "rect"}, {"op_name": "cutBlind"}, {"op_name": "hole"}],
)
check(panel_rib_holes_code is not None and panel_rib_holes_code.count(".pocket(") == 3,
      "deterministic panel rib builder expands rib pockets")
check(panel_rib_holes_code is not None and panel_rib_holes_code.count(".drill(4") == 8,
      "deterministic panel rib builder expands hole row")

base_rib_cross_code = build_deterministic_subcad_code(
    "\n".join([
        "import cadquery as cq",
        "base_size=50.0; thickness=8.0; rib_width=12.0; rib_length=30.0",
        "central_hole_diameter=20.0; mount_hole_diameter=5.0; mount_hole_offset=15.0; chamfer_size=1.0",
        "base = cq.Workplane('XY').box(base_size, base_size, thickness)",
        "base = base.faces('+Z').workplane().hole(central_hole_diameter)",
        "rib = cq.Workplane('XY').box(rib_length, rib_width, thickness)",
        "rib_pos_x = (base_size/2 + rib_length/2)",
        "rib_x_pos = rib.translate((rib_pos_x, 0, 0))",
        "rib_y_pos = rib.rotate((0,0,0), (0,0,1), 90).translate((0, rib_pos_x, 0))",
        "result = base.union(rib_x_pos).union(rib_y_pos)",
        "result = result.faces('+Z').workplane().pushPoints([(15,15),(-15,15),(-15,-15),(15,-15)]).hole(mount_hole_diameter)",
    ]),
    [{"op_name": "box"}, {"op_name": "union"}, {"op_name": "hole"}],
)
check(base_rib_cross_code is not None and ".machine_around_profiles(" in base_rib_cross_code,
      "deterministic base plus ribs maps retained rib profiles")
check(base_rib_cross_code is not None and base_rib_cross_code.count(".drill(") == 5,
      "deterministic base plus ribs preserves central and mounting holes")

cross_slot_plate_code = build_deterministic_subcad_code(
    "\n".join([
        "import cadquery as cq",
        "import math",
        "half_span = 35.0; arm_width = 20.0; thickness = 10.0",
        "slot_width = 5.0; slot_length = 30.0; central_cavity_radius = 12.0",
        "edge_chamfer = 1.5; hole_diameter = 4.0",
        "hole_offset = half_span - arm_width/2 - 5.0",
        "pts = [( half_span, arm_width/2), ( half_span, -arm_width/2),",
        "       ( arm_width/2, -half_span), (-arm_width/2, -half_span),",
        "       (-half_span, -arm_width/2), (-half_span, arm_width/2),",
        "       (-arm_width/2, half_span), (arm_width/2, half_span)]",
        "base = cq.Workplane('XY').polyline(pts).close().extrude(thickness)",
        "base = base.edges().chamfer(edge_chamfer)",
        "for angle in [0, 90, 180, 270]:",
        "    pass",
        "result = base.faces('>Z').workplane().pushPoints([(20,0),(0,20),(-20,0),(0,-20)]).hole(hole_diameter)",
    ]),
    [{"op_name": "polyline"}, {"op_name": "cut"}, {"op_name": "hole"}],
)
check(cross_slot_plate_code is not None and ".profile_cutout(" in cross_slot_plate_code,
      "deterministic cross slot plate maps cross profile blank")
check(cross_slot_plate_code is not None and cross_slot_plate_code.count(".profile_pocket(") == 4,
      "deterministic cross slot plate expands four arm slots")
check(cross_slot_plate_code is not None and cross_slot_plate_code.count(".drill(") == 4,
      "deterministic cross slot plate preserves mounting holes")

cross_slots_back_ribs_code = build_deterministic_subcad_code(
    "\n".join([
        "import cadquery as cq",
        "central_size=30.0; arm_length=30.0; arm_width=12.0; thickness=10.0",
        "cavity_radius=8.0; slot_width=6.0; slot_length=20.0; slot_offset=5.0",
        "chamfer_size=1.0; mounting_hole_dia=5.0; mounting_hole_offset=8.0",
        "rib_width=8.0; rib_height=2.0; rib_offset=4.0",
        "central = cq.Workplane('XY').rect(central_size, central_size).extrude(thickness)",
        "vertical = cq.Workplane('XY').rect(arm_width, central_size + 2 * arm_length).extrude(thickness)",
        "horizontal = cq.Workplane('XY').rect(central_size + 2 * arm_length, arm_width).extrude(thickness)",
        "base = central.union(vertical).union(horizontal)",
        "cav = base.faces('>Z').workplane().hole(cavity_radius * 2)",
        "rib_positions = [(central_size / 2 + rib_offset, rib_offset)]",
        "ribs = cq.Workplane('XY')",
        "for x, y in rib_positions:",
        "    ribs = ribs.union(cq.Workplane('XY').center(x, y).rect(rib_width, rib_width).extrude(-rib_height))",
    ]),
    [{"op_name": "union"}, {"op_name": "hole"}, {"op_name": "profile_pocket"}],
)
check(cross_slots_back_ribs_code is not None and cross_slots_back_ribs_code.count(".machine_around_profiles(") == 2,
      "deterministic cross slots backside ribs maps layered retained profiles")
check(cross_slots_back_ribs_code is not None and cross_slots_back_ribs_code.count(".profile_pocket(") == 4,
      "deterministic cross slots backside ribs expands four slots")


# =========================================================================
#  Test 2: System prompt
# =========================================================================

print("\n2. System prompt ...")
sys_prompt = build_system_prompt()
check("Stock.rectangular" in sys_prompt, "system prompt mentions Stock.rectangular")
check("Stock.cylindrical" in sys_prompt, "system prompt mentions Stock.cylindrical")
check(".face_mill" in sys_prompt, "system prompt mentions face_mill")
check(".pocket" in sys_prompt, "system prompt mentions pocket")
check(".drill" in sys_prompt, "system prompt mentions drill")
check(".slope_cut" in sys_prompt, "system prompt mentions sloped floor cuts")
check(".chamfer" in sys_prompt, "system prompt mentions chamfer")
check(".edge_chamfer" in sys_prompt, "system prompt mentions selected edge chamfer")
check(".machine_around_profile" in sys_prompt, "system prompt mentions retained-material operations")
check("hybrid_feature" in sys_prompt and "Never" in sys_prompt,
      "system prompt forbids hybrid/opaque placeholders")
check("directly with cq.Workplane" in sys_prompt or "cq.Workplane/CadQuery" in sys_prompt,
      "system prompt forbids direct CadQuery reconstruction")
check("choose among the planned" in sys_prompt,
      "system prompt limits ambiguous choices to planner candidates")
check("counterbore(hole_diameter, counterbore_diameter, counterbore_depth" in sys_prompt,
      "system prompt documents exact counterbore signature")
check("pilot_diameter" in sys_prompt and "Never use keyword names" in sys_prompt,
      "system prompt warns against invalid counterbore kwargs")
check("part" in sys_prompt, "system prompt mentions 'part' variable")
check("execute_subcad" in sys_prompt, "system prompt requires execute_subcad tool")
check("markdown fences" in sys_prompt, "system prompt forbids markdown fences in tool code")
check("Python comments" in sys_prompt, "system prompt forbids reasoning comments in generated code")
check(len(sys_prompt) > 500, f"system prompt is substantial ({len(sys_prompt)} chars)")
ai_sys_prompt = build_system_prompt("ai_heavy")
check("AI-Heavy Translation Mode" in ai_sys_prompt,
      "ai-heavy system prompt declares AI-heavy mode")
check("planner is evidence, not a cage" in ai_sys_prompt,
      "ai-heavy system prompt makes planner advisory")


# =========================================================================
#  Test 3: Code extraction
# =========================================================================

print("\n3. Code extraction ...")

# Fenced code block
response1 = """Here's the subCAD code:

```python
from src.subcad import Stock
part = Stock.rectangular(100, 50, 20).face_mill(1.0)
```
"""
code1 = extract_code(response1)
check(code1 is not None, "extracts fenced python code")
check("Stock.rectangular" in code1, "extracted code has Stock.rectangular")
check("```" not in code1, "extracted code has no fence markers")

# Fenced without language
response2 = """```
from src.subcad import Stock
part = Stock.rectangular(80, 40, 15)
```"""
code2 = extract_code(response2)
check(code2 is not None, "extracts fenced code without language tag")
check("Stock.rectangular" in code2, "extracted code has content")

# Bare code
response3 = """Here is the code:

from src.subcad import Stock
part = Stock.rectangular(100, 50, 20).face_mill(1.0)
)"""
code3 = extract_code(response3)
check(code3 is not None, "extracts bare code")
check("Stock.rectangular" in str(code3), "bare code has Stock.rectangular")

# No code
response4 = "I cannot translate this because..."
code4 = extract_code(response4)
check(code4 is None, "returns None when no code present")


# =========================================================================
#  Test 4: User prompt building
# =========================================================================

print("\n4. User prompt building ...")

# Load sample 1
with open("data/zero_to_cad_exploration/sample_1/ops_trace.json") as f:
    ops_trace = json.load(f)
with open("data/zero_to_cad_exploration/sample_1/cadquery_code.py", "r", encoding="utf-8") as f:
    cq_code = f.read()
step_path = "data/zero_to_cad_exploration/sample_1/model.step"

measures_block = _extract_measures_block(cq_code)
check("hole=Measures" in measures_block, "measures extractor keeps nested Measures block")
check(measures_block.rstrip().endswith(")"), "measures extractor keeps closing parenthesis")

stock_dims = {"length": 90.0, "width": 40.0, "height": 25.0}
prompt = build_user_prompt(cq_code, ops_trace, step_path, stock_dims)

check("CadQuery" in prompt, "user prompt mentions CadQuery")
check(cq_code[:40] in prompt, "user prompt contains CadQuery code snippet")
check("90" in prompt or "90.0" in prompt, "user prompt includes stock length")
check("STEP-derived stock dimensions above are hard evidence" in prompt,
      "user prompt forbids overriding STEP stock envelope")
check("Trust STEP bbox/volume over symmetry assumptions" in prompt,
      "user prompt prevents rotation-loop symmetry overreach")
check("part" in prompt, "user prompt mentions 'part' variable")
check("execute_subcad" in prompt, "user prompt asks for execute_subcad call")
check("Extracted Numeric Measures" in prompt, "user prompt includes extracted measures section")
check("STEP volume: 0.0" not in prompt, "user prompt computes nonzero STEP volume")
check("Pure SubCAD Operation Plan" in prompt, "user prompt includes planner candidate section")
check("CadQuery Variable Volume Evidence" in prompt,
      "user prompt includes CadQuery variable volume evidence")
check("coverage_mode: pure_subcad_operations" in prompt,
      "user prompt identifies pure SubCAD planner mode")
check("choose among those planned operation candidates only" in prompt,
      "user prompt limits ambiguity decisions to planner candidates")
ai_prompt = build_user_prompt(cq_code, ops_trace, step_path, stock_dims, translation_mode="ai_heavy")
check("AI-heavy mode is active" in ai_prompt,
      "ai-heavy user prompt identifies advisory planner mode")
check("You may add pure SubCAD operations absent from the planner" in ai_prompt,
      "ai-heavy user prompt permits source-backed operations outside planner candidates")
check("choose among those planned operation candidates only" not in ai_prompt,
      "ai-heavy user prompt removes planner-only restriction")
check("target is the original STEP reference geometry" in prompt,
      "user prompt names original STEP as target geometry")
check("hybrid_feature" in prompt and "direct CadQuery reconstruction" in prompt,
      "user prompt rejects hybrid and direct CadQuery reconstruction fallbacks")
check("CadQuery `.rect(x_size," in prompt and "y_size)` maps to SubCAD" in prompt,
      "user prompt explains CadQuery rect to SubCAD XY mapping")
check(".pocket(width=y_size, length=x_size" in prompt,
      "user prompt prevents rectangular pocket width/length swaps")
check("SubCAD `width` always means Y span" in prompt,
      "user prompt defines SubCAD width as Y span")
check("SubCAD `length` always means X span" in prompt,
      "user prompt defines SubCAD length as X span")
check('edge_chamfer("all_edges"' in prompt,
      "user prompt maps unqualified CadQuery edge chamfer to all_edges")
check("do not narrow it" in prompt,
      "user prompt prevents all-edge chamfer from becoming top-only")
check('edge_chamfer("|Z"' in prompt,
      "user prompt preserves CadQuery directional edge chamfer selectors")
check("machine_around_profile" in prompt and "cx=..." in prompt and "cy=..." in prompt,
      "user prompt allows retained feature placement through cx/cy kwargs")
check("machine_around_profiles" in sys_prompt and "do not face_mill away" in sys_prompt,
      "system prompt teaches multi-island retained features and stock height")
check("fully inside" in prompt and "existing base stock" in prompt,
      "user prompt avoids machining around construction-only internal unions")
check("translate((x, y, z))" in prompt and "literally" in prompt,
      "user prompt preserves CadQuery translated feature coordinates literally")
check("Never use bare measure names" in prompt and "m.flange_thickness" in prompt,
      "user prompt prevents undefined bare measure variables")
check("Stock.cylindrical" in prompt and ".cylinder" in prompt,
      "user prompt maps CadQuery cylindrical blanks to cylindrical stock")
check(".slope_cut" in prompt and "sloped floor" in prompt,
      "user prompt exposes sloped trough machining")
check("extrude(..., taper=...)" in prompt and "tapered_cylinder" in prompt,
      "user prompt maps tapered extrudes to turn_profile")
check("second `.circle(...)`" in prompt and "center bore" in prompt,
      "user prompt avoids hallucinating bores from nested sketch circles")
check(".polygon(n, diameter)" in prompt and "circumdiameter" in prompt and "hex_radius" in prompt,
      "user prompt maps CadQuery polygon diameter to SubCAD circumdiameter")
check("Copy the exact second argument" in prompt and "do not multiply it by" in prompt,
      "user prompt forbids recomputing CadQuery polygon dimensions")
check("no volume change" in prompt or "variable volume evidence" in prompt.lower(),
      "user prompt can warn about no-op CadQuery source operations")
check("omit the corresponding" in prompt and "omit those hole operations" in prompt,
      "user prompt requires omitting no-volume-change source operations")


# =========================================================================
#  Test 5: Iteration prompt building
# =========================================================================

print("\n5. Iteration prompt ...")

prev_code = "from src.subcad import Stock\npart = Stock.rectangular(100,50,20).face_mill(2.0)"
exec_result = {
    "success": True,
    "volume": 12000.0,
    "bbox": {"length": 100, "width": 50, "height": 18},
    "faces": 12,
    "plan": {"operations": [{"operation": "face_mill", "tool_type": "flat_endmill"}]},
}
comparison = {
    "match": False,
    "volume_ratio": 0.75,
    "iou_estimate": 0.75,
}

iter_prompt = build_iteration_prompt(prev_code, exec_result, comparison, 16000.0)
check("Previous Attempt" in iter_prompt, "iteration prompt references previous attempt")
check("too small" in iter_prompt or "0.75" in iter_prompt, "iteration prompt shows mismatch")
check("Stock.rectangular" in iter_prompt, "iteration prompt has API reference")
check(prev_code in iter_prompt, "iteration prompt includes previous code")
check("original STEP reference" in iter_prompt,
      "iteration prompt repairs against original STEP target")
check("hybrid_feature" in iter_prompt and "CadQuery reconstruction" in iter_prompt,
      "iteration prompt rejects hybrid/direct reconstruction repairs")

mesh_comp = {"feedback": "RMS deviation: 0.250 mm near top pocket", "score": 91.0}
feature_comp = {"feedback": "Hole at (0, 0): MISSING", "score": 75.0}
rich_iter_prompt = build_iteration_prompt(
    prev_code,
    exec_result,
    comparison,
    16000.0,
    mesh_comparison=mesh_comp,
    feature_comparison=feature_comp,
)
check("Localized Shape Deviation" in rich_iter_prompt,
      "iteration prompt includes mesh comparison section")
check("RMS deviation" in rich_iter_prompt,
      "iteration prompt includes mesh feedback text")
check("original-STEP comparison" in rich_iter_prompt,
      "mesh repair feedback references original STEP comparison")
check("Per-Feature Comparison" in rich_iter_prompt,
      "iteration prompt includes feature comparison section")
check("MISSING" in rich_iter_prompt,
      "iteration prompt includes feature feedback text")


# Check if CadQuery is available for REPL-dependent tests
try:
    from src.subcad.geometry import create_rectangular_stock
    _test_shape = create_rectangular_stock(10, 10, 10)
    _HAS_CADQUERY_REPL = True
except Exception:
    _HAS_CADQUERY_REPL = False

# =========================================================================
#  Test 6: REPL integration (run_subcad with valid code)
# =========================================================================

print("\n6. REPL integration ...")

valid_code = """from src.subcad import Stock
part = (Stock.rectangular(100, 50, 20, material=\"aluminum_6061\")
    .face_mill(depth=2.0)
    .drill(diameter=8, cx=0, cy=0, depth=15)
)"""

if _HAS_CADQUERY_REPL:
    result = run_subcad(valid_code)
    check(result["success"], "valid subcad code executes successfully")
    check(result.get("volume", 0) > 0, f"volume > 0 ({result.get('volume', 0):.1f})")
    check(result.get("faces", 0) > 0, f"faces > 0 ({result.get('faces', 0)})")
    check(result.get("step_path") is not None, "STEP file exported")
    check(result.get("stl_path") is not None, "STL file exported")
    check(result.get("process_plan", {}).get("operations"), "process plan has operations")

    _repl_result = result
    _repl_code = valid_code
    # NOTE: do NOT clean up temp files here — test 8 needs them
else:
    print("  SKIP  CadQuery not available — skipping REPL integration tests")
    _repl_result = None
    _repl_code = None


# =========================================================================
#  Test 7: REPL with invalid code (does not need Stock to succeed)
# =========================================================================

print("\n7. REPL error handling ...")

# Missing 'part' variable — code that creates nothing should fail
bad_code = """x = 42\ny = "hello\""""  # no Stock or Workplane at all
result = run_subcad(bad_code)
check(not result["success"], "fails when no 'part' variable")
check(result.get("error") is not None, "error message present")

# Syntax error — always detectable regardless of CadQuery
bad_code2 = """from src.subcad import Stock
part = Stock.rectangular(100, 50, 20
    .face_mill(1.0)"""
result = run_subcad(bad_code2)
check(not result["success"], "fails on syntax error")
check("Syntax" in result.get("error", ""), "error message says Syntax")

bad_sequence = run_subcad(
    "part = Stock.rectangular(40, 20, 10)"
    ".machine_around_profile({'length': 10, 'width': 4}, height=2)"
    ".face_mill(5)"
)
check(not bad_sequence["success"], "rejects face_mill after retained features")
check("face_mill appears after retained" in bad_sequence.get("error", ""),
      "retained sequencing guard returns actionable error")

bad_pre_face = run_subcad(
    "part = Stock.rectangular(80, 35, 20)"
    ".face_mill(depth=12)"
    ".machine_around_cylinder(20, 12, cx=10, cy=10, base_height=7.5)"
)
check(not bad_pre_face["success"], "rejects face_mill below retained z-band height")
check("retained operations require material" in bad_pre_face.get("error", ""),
      "retained height guard returns actionable error")


# =========================================================================
#  Test 8: compare_to_reference with real files
# =========================================================================

print("\n8. Geometry comparison ...")

if _HAS_CADQUERY_REPL and _repl_result is not None and _repl_result.get("success"):
    subcad_step = _repl_result["step_path"]
    if subcad_step and os.path.exists(subcad_step):
        # Compare to itself — should match (ratio = 1.0)
        comp = compare_to_reference(subcad_step, subcad_step)
        check(comp.get("match"), "self-comparison matches")
        check(abs(comp.get("volume_ratio", 0) - 1.0) < 0.001,
              f"self-comparison volume ratio is ~1.0 (got {comp.get('volume_ratio', 0)})")

        # Compare to a different part (sample_1 STEP)
        sample1_step = "data/zero_to_cad_exploration/sample_1/model.step"
        if os.path.exists(sample1_step):
            comp2 = compare_to_reference(subcad_step, sample1_step)
            # Different parts, so may or may not match — just check no error
            check("error" not in comp2 or comp2.get("error") is None,
                  "cross-part comparison has no error")
            check(isinstance(comp2.get("volume_ratio"), (int, float)),
                  "volume_ratio is numeric")

    # Clean up temp files (deferred from test 6)
    for k in ("step_path", "stl_path"):
        if _repl_result.get(k) and os.path.exists(_repl_result[k]):
            os.unlink(_repl_result[k])
else:
    print("  SKIP  CadQuery not available — skipping geometry comparison")

# =========================================================================
#  Test 9: format_feedback
# =========================================================================

print("\n9. Feedback formatting ...")

# format_feedback takes (code, exec_result, comparison)
comparison = {"match": False, "volume_ratio": 0.85, "target_volume": 5000.0,
              "candidate_volume": 4250.0, "volume_diff": 750.0}
exec_result = {"success": True, "volume": 4250.0, "faces": 42,
               "step_path": "/tmp/test.step", "stl_path": "/tmp/test.stl",
               "process_plan": {"operations": ["face_mill", "pocket", "drill"]}}
feedback = format_feedback(valid_code, exec_result, comparison)
check(len(feedback) > 0, "format_feedback returns non-empty string")
check("[OK]" in feedback or "[FAIL]" in feedback or "MATCH" in feedback or "MISMATCH" in feedback,
      "feedback has status marker (OK/FAIL/MATCH/MISMATCH)")


# =========================================================================
#  Test 10: translate_exploration_sample (import only — requires API key)
# =========================================================================

print("\n10. translate_exploration_sample ...")
check(callable(translate_exploration_sample), "translate_exploration_sample is callable")
check(callable(translate_batch), "translate_batch is callable")


# =========================================================================
#  Test 10b: Live-run dry-run wrapper
# =========================================================================

print("\n10b. live-run dry-run wrapper ...")
preview = build_dry_run_preview("data/zero_to_cad_exploration/sample_1")
check(preview["cadquery_chars"] > 100, "dry-run preview reads CadQuery code")
check(preview["ops_trace_count"] > 0, "dry-run preview reads ops trace")
check(preview["stock_dims"]["length"] > 0, "dry-run preview computes stock dims")
check(preview["system_prompt_chars"] > 500, "dry-run preview builds system prompt")
check(preview["user_prompt_chars"] > 500, "dry-run preview builds user prompt")


# =========================================================================
#  Test 11: Agentic loop rich comparison feedback wiring (mocked)
# =========================================================================

print("\n11. Agentic loop rich comparison feedback ...")

_orig_llm_client = agentic_mod.LLMClient
_orig_run_subcad = agentic_mod.run_subcad
_orig_compare_to_reference = agentic_mod.compare_to_reference
_orig_step_to_stock_dims = agentic_mod.step_to_stock_dims
_orig_load_step_mesh = agentic_mod._load_step_mesh
_orig_compare_meshes = agentic_mod.compare_meshes
_orig_compare_with_features = agentic_mod.compare_with_features
_orig_has_mesh_compare = agentic_mod._HAS_MESH_COMPARE
_orig_has_feature_compare = agentic_mod._HAS_FEATURE_COMPARE


class _FakePart:
    def to_mesh(self):
        return "candidate-mesh"


class _FakeLLMClient:
    instances = []

    def __init__(self, *args, **kwargs):
        self.calls = 0
        self.messages_seen = []
        _FakeLLMClient.instances.append(self)

    def tool_chat(self, messages, tools, temperature=0.2, max_tokens=4096):
        self.calls += 1
        self.messages_seen.append(list(messages))
        return {
            "id": f"call-{self.calls}",
            "name": "execute_subcad",
            "arguments": {"code": "part = Stock.rectangular(10, 10, 10)"},
        }


try:
    comparisons = [
        {
            "match": False,
            "volume_ratio": 0.5,
            "target_volume": 2000.0,
            "candidate_volume": 1000.0,
        },
        {
            "match": True,
            "volume_ratio": 1.0,
            "target_volume": 1000.0,
            "candidate_volume": 1000.0,
        },
    ]

    def _fake_run_subcad(code):
        return {
            "success": True,
            "volume": 1000.0,
            "faces": 6,
            "part": _FakePart(),
            "step_path": "candidate.step",
            "stl_path": None,
            "process_plan": {"operations": []},
        }

    def _fake_compare_to_reference(candidate, reference):
        return comparisons.pop(0)

    def _fake_compare_meshes(ref_mesh, cand_mesh, methods=None, **kwargs):
        return {
            "feedback": "RMS deviation: 0.125 mm around pocket floor",
            "score": 88.0,
            "sdf": {"per_vertex_deviation": [0.1, -0.1]},
        }

    def _fake_compare_with_features(ref_step_path, candidate_mesh, ops_trace=None,
                                    tolerance_mm=0.1):
        return {
            "feedback": "Pocket at (0, 0): depth 2.0mm instead of 3.0mm --- WRONG SIZE",
            "score": 72.0,
            "feature_comparisons": [{
                "ref_feature": {
                    "type": "pocket",
                    "face_indices": [1, 2, 3],
                    "submesh": "heavy",
                },
                "match_type": "wrong_size",
                "status": "error",
            }],
        }

    agentic_mod.LLMClient = _FakeLLMClient
    agentic_mod.run_subcad = _fake_run_subcad
    agentic_mod.compare_to_reference = _fake_compare_to_reference
    agentic_mod.step_to_stock_dims = lambda step_bytes: {
        "length": 10.0, "width": 10.0, "height": 10.0
    }
    agentic_mod._load_step_mesh = lambda step_path: "reference-mesh"
    agentic_mod.compare_meshes = _fake_compare_meshes
    agentic_mod.compare_with_features = _fake_compare_with_features
    agentic_mod._HAS_MESH_COMPARE = True
    agentic_mod._HAS_FEATURE_COMPARE = True

    with tempfile.NamedTemporaryFile(suffix=".step", delete=False) as tf:
        tf.write(b"mock-step")
        mock_step_path = tf.name

    try:
        translator = AgenticTranslator(
            provider="mock",
            verbose=False,
            tolerance=0.01,
            safety_cap=3,
            comparison_methods=["sdf"],
            feature_aware=True,
        )
        loop_result = translator.translate(
            {
                "cadquery_file": "part = cq.Workplane('XY').box(10, 10, 10)",
                "cadquery_ops_json": "[]",
            },
            step_path=mock_step_path,
        )
    finally:
        if os.path.exists(mock_step_path):
            os.unlink(mock_step_path)

    fake_client = _FakeLLMClient.instances[-1]
    second_call_messages = fake_client.messages_seen[1]
    tool_messages = [m for m in second_call_messages if m.get("role") == "tool"]
    user_messages = [m for m in second_call_messages if m.get("role") == "user"]

    check(loop_result["success"], "mocked loop converges on second attempt")
    check(loop_result["mesh_comparison"]["score"] == 88.0,
          "final result includes mesh comparison")
    check(loop_result["feature_comparison"]["score"] == 72.0,
          "final result includes feature comparison")
    check(loop_result["history"][0]["mesh_comparison"]["score"] == 88.0,
          "history includes mesh comparison")
    check("per_vertex_deviation" in loop_result["history"][0]["mesh_comparison"]["sdf"],
          "history keeps compact mesh comparison fields")
    check(any("mesh_feedback" in m.get("content", "") for m in tool_messages),
          "tool feedback includes mesh feedback")
    check(any("feature_feedback" in m.get("content", "") for m in tool_messages),
          "tool feedback includes feature feedback")
    check(any("Localized Shape Deviation" in m.get("content", "")
              for m in user_messages),
          "next iteration prompt includes mesh comparison feedback")
    check(any("Per-Feature Comparison" in m.get("content", "")
              for m in user_messages),
          "next iteration prompt includes feature comparison feedback")
finally:
    agentic_mod.LLMClient = _orig_llm_client
    agentic_mod.run_subcad = _orig_run_subcad
    agentic_mod.compare_to_reference = _orig_compare_to_reference
    agentic_mod.step_to_stock_dims = _orig_step_to_stock_dims
    agentic_mod._load_step_mesh = _orig_load_step_mesh
    agentic_mod.compare_meshes = _orig_compare_meshes
    agentic_mod.compare_with_features = _orig_compare_with_features
    agentic_mod._HAS_MESH_COMPARE = _orig_has_mesh_compare
    agentic_mod._HAS_FEATURE_COMPARE = _orig_has_feature_compare


# =========================================================================
#  Test 12: Best executable attempt survives failed final repair
# =========================================================================

print("\n12. Best executable attempt retention ...")

_orig_llm_client = agentic_mod.LLMClient
_orig_run_subcad = agentic_mod.run_subcad
_orig_compare_to_reference = agentic_mod.compare_to_reference
_orig_step_to_stock_dims = agentic_mod.step_to_stock_dims
_orig_has_mesh_compare = agentic_mod._HAS_MESH_COMPARE


class _FailingFinalLLMClient:
    def __init__(self, *args, **kwargs):
        self.calls = 0

    def tool_chat(self, messages, tools, temperature=0.2, max_tokens=4096):
        self.calls += 1
        return {
            "id": f"best-call-{self.calls}",
            "name": "execute_subcad",
            "arguments": {"code": "part = Stock.rectangular(10, 10, 10)"},
        }


try:
    run_calls = []
    comparisons = [
        {"match": True, "volume_ratio": 0.91, "target_volume": 1000.0, "candidate_volume": 910.0},
        {"match": True, "volume_ratio": 0.92, "target_volume": 1000.0, "candidate_volume": 920.0},
    ]

    def _fake_run_subcad_best(code):
        run_calls.append(code)
        if len(run_calls) == 3:
            return {"success": False, "error": "No 'part' variable found"}
        return {
            "success": True,
            "volume": 900.0 + len(run_calls) * 10.0,
            "faces": 6,
            "part": _FakePart(),
            "step_path": f"candidate-{len(run_calls)}.step",
            "stl_path": None,
            "process_plan": {"operations": []},
        }

    def _fake_compare_best(candidate, reference):
        return comparisons.pop(0)

    agentic_mod.LLMClient = _FailingFinalLLMClient
    agentic_mod.run_subcad = _fake_run_subcad_best
    agentic_mod.compare_to_reference = _fake_compare_best
    agentic_mod.step_to_stock_dims = lambda step_bytes: {
        "length": 10.0, "width": 10.0, "height": 10.0
    }
    agentic_mod._HAS_MESH_COMPARE = False

    with tempfile.NamedTemporaryFile(suffix=".step", delete=False) as tf:
        tf.write(b"mock-step")
        mock_step_path = tf.name

    try:
        translator = AgenticTranslator(
            provider="mock",
            verbose=False,
            tolerance=0.01,
            safety_cap=3,
            strict_mesh_convergence=True,
            comparison_methods=["slice"],
        )
        best_result = translator.translate(
            {
                "cadquery_file": "part = cq.Workplane('XY').box(10, 10, 10)",
                "cadquery_ops_json": "[]",
            },
            step_path=mock_step_path,
        )
    finally:
        if os.path.exists(mock_step_path):
            os.unlink(mock_step_path)

    check(best_result["returned_best_attempt"], "returns best executable attempt after failed final repair")
    check(best_result["best_attempt"] == 2, "best executable attempt index is recorded")
    check(best_result["exec_result"]["success"], "returned best attempt keeps successful execution result")
    check(best_result["comparison"]["volume_ratio"] == 0.92,
          "returned best attempt keeps best comparison metrics")
finally:
    agentic_mod.LLMClient = _orig_llm_client
    agentic_mod.run_subcad = _orig_run_subcad
    agentic_mod.compare_to_reference = _orig_compare_to_reference
    agentic_mod.step_to_stock_dims = _orig_step_to_stock_dims
    agentic_mod._HAS_MESH_COMPARE = _orig_has_mesh_compare


# =========================================================================
#  Test 13: AI-heavy mode bypasses deterministic builders
# =========================================================================

print("\n13. AI-heavy mode ...")

_orig_llm_client = agentic_mod.LLMClient
_orig_run_subcad = agentic_mod.run_subcad
_orig_compare_to_reference = agentic_mod.compare_to_reference
_orig_step_to_stock_dims = agentic_mod.step_to_stock_dims
_orig_build_deterministic = agentic_mod.build_deterministic_subcad_code
_orig_has_mesh_compare = agentic_mod._HAS_MESH_COMPARE


class _AIHeavyLLMClient:
    def __init__(self, *args, **kwargs):
        self.calls = 0

    def tool_chat(self, messages, tools, temperature=0.2, max_tokens=4096):
        self.calls += 1
        return {
            "id": f"ai-heavy-call-{self.calls}",
            "name": "execute_subcad",
            "arguments": {"code": "part = Stock.rectangular(10, 10, 10)"},
        }


try:
    def _deterministic_should_not_run(*args, **kwargs):
        raise AssertionError("deterministic builder should be skipped in ai_heavy mode")

    agentic_mod.LLMClient = _AIHeavyLLMClient
    agentic_mod.build_deterministic_subcad_code = _deterministic_should_not_run
    agentic_mod.run_subcad = lambda code: {
        "success": True,
        "volume": 1000.0,
        "faces": 6,
        "part": _FakePart(),
        "step_path": "candidate.step",
        "stl_path": None,
        "process_plan": {"operations": []},
    }
    agentic_mod.compare_to_reference = lambda candidate, reference: {
        "match": True,
        "volume_ratio": 1.0,
        "target_volume": 1000.0,
        "candidate_volume": 1000.0,
    }
    agentic_mod.step_to_stock_dims = lambda step_bytes: {
        "length": 10.0, "width": 10.0, "height": 10.0
    }
    agentic_mod._HAS_MESH_COMPARE = False

    with tempfile.NamedTemporaryFile(suffix=".step", delete=False) as tf:
        tf.write(b"mock-step")
        mock_step_path = tf.name

    try:
        translator = AgenticTranslator(
            provider="mock",
            verbose=False,
            tolerance=0.01,
            safety_cap=1,
            comparison_methods=None,
            translation_mode="ai_heavy",
        )
        ai_heavy_result = translator.translate(
            {
                "cadquery_file": "part = cq.Workplane('XY').box(10, 10, 10)",
                "cadquery_ops_json": "[]",
            },
            step_path=mock_step_path,
        )
    finally:
        if os.path.exists(mock_step_path):
            os.unlink(mock_step_path)

    check(ai_heavy_result["success"], "ai-heavy mode can translate through the LLM path")
    check(ai_heavy_result["translation_mode"] == "ai_heavy",
          "ai-heavy result records translation mode")

    class _ToolChoiceRejectingCompletions:
        def __init__(self):
            self.calls = []

        def create(self, **kwargs):
            self.calls.append(kwargs)
            if "tool_choice" in kwargs:
                raise RuntimeError("deepseek-reasoner does not support this tool_choice")

            class _Function:
                name = "execute_subcad"
                arguments = json.dumps({"code": "part = Stock.rectangular(10, 10, 10)"})

            class _ToolCall:
                id = "fallback-tool-call"
                function = _Function()

            class _Message:
                tool_calls = [_ToolCall()]

            class _Choice:
                message = _Message()

            class _Response:
                choices = [_Choice()]

            return _Response()

    class _ToolChoiceRejectingClient:
        def __init__(self):
            self.chat = type("Chat", (), {})()
            self.chat.completions = _ToolChoiceRejectingCompletions()

    fallback_client = object.__new__(_orig_llm_client)
    fallback_client._is_anthropic = False
    fallback_client.model = "deepseek-v4-pro"
    fallback_client._client = _ToolChoiceRejectingClient()
    fallback_tool = fallback_client.tool_chat(
        [{"role": "user", "content": "call execute_subcad"}],
        [agentic_mod.EXECUTE_SUBCAD_TOOL],
    )
    calls = fallback_client._client.chat.completions.calls
    check(fallback_tool is not None and fallback_tool["arguments"]["code"].startswith("part = Stock"),
          "tool-chat falls back when model rejects forced tool_choice")
    check("tool_choice" in calls[0] and "tool_choice" not in calls[1],
          "tool-chat retry removes unsupported tool_choice")
finally:
    agentic_mod.LLMClient = _orig_llm_client
    agentic_mod.run_subcad = _orig_run_subcad
    agentic_mod.compare_to_reference = _orig_compare_to_reference
    agentic_mod.step_to_stock_dims = _orig_step_to_stock_dims
    agentic_mod.build_deterministic_subcad_code = _orig_build_deterministic
    agentic_mod._HAS_MESH_COMPARE = _orig_has_mesh_compare


# =========================================================================
#  Summary
# =========================================================================

total = passed + failed
print(f"\n{'='*60}")
print(f"  {'ALL PASSED' if failed == 0 else 'FAILURES PRESENT'}")
print(f"  {passed}/{total} tests passed")
print(f"{'='*60}")

if failed > 0:
    sys.exit(1)
