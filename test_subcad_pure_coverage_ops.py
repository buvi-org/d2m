"""Tests for pure SubCAD operation families used by STEP coverage."""

import math

from src.subcad import Stock, create_operation
from src.data.pure_subcad_planner import plan_pure_subcad_features


def check(cond, label):
    if not cond:
        raise AssertionError(label)
    print(f"  PASS  {label}")


print("1. Pure planner maps STEP/CadQuery feature families ...")
plan = plan_pure_subcad_features(
    [
        {"op_name": "chamfer"},
        {"op_name": "fillet"},
        {"op_name": "union"},
        {"op_name": "circle"},
        {"op_name": "extrude"},
        {"op_name": "revolve"},
        {"op_name": "shell", "function": "part.faces.shell"},
        {"op_name": "sweep"},
        {"op_name": "loft"},
        {"op_name": "polygon"},
        {"op_name": "rarray"},
    ],
    '.circle(10).extrude(5).union(x).revolve().faces(">Z").shell(1).sweep(p).loft()',
)
ops = {feature.operation for feature in plan.features}
check(plan.compatible, "planner considers mapped pure operations compatible")
check("edge_chamfer" in ops, "planner maps chamfer to edge_chamfer")
check("edge_fillet" in ops, "planner maps fillet to edge_fillet")
check("machine_around_profile" in ops, "planner maps union to retained-material operation")
check("turn_profile" in ops, "planner maps revolve to turn_profile")
check("thin_wall_pocket" in ops, "planner maps shell to thin_wall_pocket")
check("sweep_mill" in ops, "planner maps sweep to sweep_mill")
check("loft_mill" in ops, "planner maps loft to loft_mill")

tapered_plan = plan_pure_subcad_features(
    [{"op_name": "circle"}, {"op_name": "extrude", "keywords": [{"arg": "taper", "value": "-5"}]}],
    ".circle(40).extrude(10, taper=-5)",
)
check(
    any(feature.operation == "turn_profile" and feature.family == "axisymmetric"
        for feature in tapered_plan.features),
    "planner maps tapered circle extrude to turn_profile",
)

closed_shell = plan_pure_subcad_features(
    [{"op_name": "box"}, {"op_name": "shell", "function": "base.shell"}],
    ".box(10, 10, 10).shell(-1)",
)
check(not closed_shell.compatible, "planner rejects closed inaccessible shells")
check(
    any(feature.planner_status == "unsupported_unmachinable" for feature in closed_shell.features),
    "closed shell is labeled unsupported_unmachinable",
)


print("\n2. Fluent pure operation API serializes process-plan records ...")
profile = {"type": "polygon", "points": [(-10, -5), (10, -5), (12, 0), (10, 5), (-10, 5)]}
part = (
    Stock.rectangular(80, 50, 20)
    .edge_chamfer({"face": ">Z", "edge_direction": "X"}, 0.5)
    .edge_fillet({"feature_id": "outer_blend"}, 1.0)
    .profile_pocket(profile, 2.0)
    .profile_cutout(profile, depth=3.0)
    .profile_contour(profile, 4.0)
    .machine_around_profile(profile, 3.0)
    .machine_around_cylinder(12.0, 4.0, cx=5.0, cy=0.0)
    .rib(4.0, 30.0, 5.0, cx=0.0, cy=0.0)
    .pad(profile, 2.0)
    .turn_profile([(0, 0), (10, 0), (10, 20)], stock_diameter=30.0)
    .turn_face(0.0)
    .turn_od(20.0, 40.0)
    .turn_id(10.0, 20.0)
    .turn_groove(2.0, 1.0, 12.0)
    .turn_thread(20.0, 1.5, 15.0)
    .mill_turn_setup()
    .thin_wall_pocket(profile, 1.2, 5.0, open_faces=[">Z"])
    .hollow_bore({"diameter": 10}, {"diameter": 20}, 15.0)
    .tube_profile({"diameter": 20}, {"diameter": 10}, 30.0)
    .surface_mill({"surface": "freeform_patch"})
    .sweep_mill(profile, {"points": [(0, 0), (20, 0)]})
    .loft_mill([profile, {"type": "circle", "diameter": 8}])
    .dome_mill(8.0, 3.0)
    .wire_cut_profile(profile, 6.0)
    .wire_cut_internal(profile, 6.0, start_hole={"diameter": 2})
)
plan_dict = part.process_plan()
operation_names = [op["operation"] for op in plan_dict["operations"]]
expected = {
    "edge_chamfer",
    "edge_fillet",
    "profile_pocket",
    "profile_cutout",
    "profile_contour",
    "machine_around_profile",
    "machine_around_cylinder",
    "rib",
    "pad",
    "turn_profile",
    "turn_face",
    "turn_od",
    "turn_id",
    "turn_groove",
    "turn_thread",
    "mill_turn_setup",
    "thin_wall_pocket",
    "hollow_bore",
    "tube_profile",
    "surface_mill",
    "sweep_mill",
    "loft_mill",
    "dome_mill",
    "wire_cut_profile",
    "wire_cut_internal",
}
check(expected.issubset(set(operation_names)), "all pure coverage operations appear in process plan")
for op in plan_dict["operations"]:
    if op["operation"] in expected:
        check(op.get("manufacturing_completeness") == "pure_operation",
              f"{op['operation']} marks pure operation completeness")
        check("toolpath" in op, f"{op['operation']} emits neutral toolpath")

bottom_face_part = (
    Stock.rectangular(40, 30, 10)
    .pocket(8, 12, 2, face_selector="<Z")
    .circular_pocket(6, 1, face_selector="<Z")
    .drill(3, through=True, face_selector="<Z")
    .machine_around_cylinder(5, 2, face_selector="<Z")
)
bottom_ops = bottom_face_part.process_plan()["operations"]
check(all(op.get("face_selector") == "<Z" for op in bottom_ops),
      "fluent core operations preserve bottom face_selector in process plan")


print("\n3. Operation factory exposes new families ...")
factory_op = create_operation("surface_mill", surface_ref={"id": "patch_1"})
check(factory_op.to_dict()["operation"] == "surface_mill",
      "create_operation can build surface_mill")

print("\n4. Geometry-backed pure ops remove material ...")
base = Stock.rectangular(80, 50, 20)
base_volume = base.volume
profile_part = base.profile_pocket(profile, 3.0)
check(profile_part.volume < base_volume, "profile_pocket changes B-Rep volume")
cutout_part = base.profile_cutout(profile, depth=4.0)
check(cutout_part.volume < base_volume, "profile_cutout changes B-Rep volume")
through_cutout = base.profile_cutout(profile, through=True)
check(through_cutout.volume < base_volume, "through profile_cutout retains profile outline")
after_cutout_pocket = through_cutout.pocket(width=2.0, length=4.0, depth=1.0, cx=0.0, cy=0.0)
check(after_cutout_pocket.volume < through_cutout.volume,
      "profile_cutout keeps a usable top face for later operations")
hex_cutout = Stock.rectangular(100, 90, 12).profile_cutout(
    {"type": "polygon", "n_sides": 6, "circumradius": 30.0},
    through=True,
)
check(hex_cutout.volume > 20000, "profile_cutout supports regular polygon profile dicts")
hex_depth_cutout = Stock.rectangular(100, 90, 12).profile_cutout(
    {"type": "polygon", "n_sides": 6, "circumradius": 30.0},
    depth=12.0,
)
check(hex_depth_cutout.volume > 20000,
      "profile_cutout treats full-depth outline cuts as through cutouts")
hex_diameter_cutout = Stock.rectangular(100, 90, 12).profile_cutout(
    {"type": "polygon", "n_sides": 6, "circumdiameter": 60.0},
    through=True,
)
check(abs(hex_diameter_cutout.volume - hex_cutout.volume) < 1e-6,
      "regular polygon profiles support circumdiameter")
contour_part = base.profile_contour(profile, 3.0)
check(contour_part.volume < base_volume, "profile_contour changes B-Rep volume")
around_profile = base.machine_around_profile(profile, 3.0)
check(around_profile.volume < base_volume, "machine_around_profile removes surrounding material")
around_cylinder = base.machine_around_cylinder(10.0, 3.0)
check(around_cylinder.volume < base_volume, "machine_around_cylinder removes surrounding material")
selected_chamfer = base.edge_chamfer({"face": ">Z", "edge_direction": "X"}, 0.5)
check(selected_chamfer.volume < base_volume, "edge_chamfer changes selected-edge geometry")
selected_fillet = base.edge_fillet({"face": ">Z", "edge_direction": "X"}, 0.5)
check(selected_fillet.volume <= base_volume, "edge_fillet executes without adding material")

taper_delta = 10.0 * math.tan(math.radians(5.0))
tapered = (
    Stock.cylindrical(2 * (40.0 + taper_delta), 10.0)
    .turn_profile(
        {
            "type": "tapered_cylinder",
            "bottom_diameter": 80.0,
            "top_diameter": 2 * (40.0 + taper_delta),
            "height": 10.0,
        },
        stock_diameter=2 * (40.0 + taper_delta),
    )
)
check(tapered.volume < Stock.cylindrical(2 * (40.0 + taper_delta), 10.0).volume,
      "turn_profile tapered_cylinder changes B-Rep volume")

print("\nALL PASSED")
