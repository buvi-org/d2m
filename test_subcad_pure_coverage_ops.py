"""Tests for pure SubCAD operation families used by STEP coverage."""

import math

from src.subcad import Stock, create_operation
from src.data.pure_subcad_planner import build_deterministic_subcad_code, plan_pure_subcad_features
from src.data.subcad_repl import run_subcad


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

side_gusset = plan_pure_subcad_features(
    [
        {"op_name": "box"},
        {"op_name": "faces"},
        {"op_name": "workplane"},
        {"op_name": "polyline"},
        {"op_name": "extrude"},
    ],
    """
    cq.Workplane("XY")
      .box(40, 30, 10)
      .faces(">X").workplane()
      .polyline([(0, 0), (12, 0), (0, 8)])
      .close()
      .extrude(4)
    """,
)
check(not side_gusset.compatible, "planner rejects side-face additive gussets")
check(
    any(feature.planner_status == "needs_manual_review"
        and feature.operation == "oriented_retained_material"
        for feature in side_gusset.features),
    "side-face additive gusset is labeled needs_manual_review",
)

bottom_cut = plan_pure_subcad_features(
    [
        {"op_name": "box"},
        {"op_name": "faces"},
        {"op_name": "workplane"},
        {"op_name": "rect"},
        {"op_name": "cutBlind"},
    ],
    """
    cq.Workplane("XY")
      .box(40, 30, 10)
      .faces("<Z").workplane()
      .rect(8, 12)
      .cutBlind(2)
    """,
)
check(bottom_cut.compatible, "planner preserves bottom-face cutBlind compatibility")
check(
    not any(feature.operation == "oriented_retained_material" for feature in bottom_cut.features),
    "bottom-face cutBlind is not treated as retained additive material",
)

top_rib_extrude = plan_pure_subcad_features(
    [
        {"op_name": "box"},
        {"op_name": "faces"},
        {"op_name": "workplane"},
        {"op_name": "rect"},
        {"op_name": "extrude"},
    ],
    """
    cq.Workplane("XY")
      .box(40, 30, 5)
      .faces(">Z").workplane()
      .rect(8, 20)
      .extrude(4)
    """,
)
check(top_rib_extrude.compatible, "planner accepts top-face additive retained material")
check(
    any(feature.operation == "machine_around_profile"
        and feature.family == "retained_material"
        for feature in top_rib_extrude.features),
    "top-face additive extrude maps to retained-material operation",
)

retained_pattern_plan = plan_pure_subcad_features(
    [],
    """
    flange_thickness = 8.0
    fusion_overlap = 0.5
    rib_count = 3
    rib_spacing = 12.0
    rib_width = 6.0
    rib_height = 4.0
    boss_height = 12.0
    boss_diameter = 20.0
    boss = (
        cq.Workplane("XY")
        .center(10.0, 10.0)
        .circle(boss_diameter / 2.0)
        .extrude(boss_height)
        .translate((0, 0, flange_thickness - fusion_overlap))
    )
    result = result.union(boss)
    for i in range(rib_count):
        rib_x = -4.0 + i * rib_spacing
        rib = (
            cq.Workplane("XY")
            .center(rib_x, 2.0)
            .rect(rib_spacing * 0.8, rib_width)
            .extrude(rib_height)
            .translate((0, 0, flange_thickness - fusion_overlap))
        )
        result = result.union(rib)
    """,
)
pattern_evidence = [
    feature.evidence for feature in retained_pattern_plan.features
    if feature.operation == "machine_around_profiles"
    and feature.evidence.get("suggested_subcad")
]
check(bool(pattern_evidence), "planner extracts multi-rib retained-pattern evidence")
check(
    [round(profile["cx"], 6) for profile in pattern_evidence[0]["profiles"]] == [-4.0, 8.0, 20.0],
    "retained-pattern evidence preserves loop-derived rib centers",
)
level_evidence = [
    feature.evidence for feature in retained_pattern_plan.features
    if feature.evidence.get("suggested_sequence")
]
check(bool(level_evidence), "planner suggests mixed-height retained operation sequence")
check(
    "base_height=11.5" in level_evidence[0]["suggested_subcad"]
    and "base_height=7.5" in level_evidence[0]["suggested_subcad"],
    "mixed-height retained sequence preserves upper and lower z bands",
)

base_cut_plan = plan_pure_subcad_features(
    [],
    """
    flange_leg_length = 80.0
    flange_leg_width = 30.0
    flange_thickness = 8.0
    inner_cut_width = 20.0
    cut = (
        cq.Workplane('XY')
        .rect(flange_leg_length - inner_cut_width, flange_leg_width - inner_cut_width)
        .translate((inner_cut_width / 2.0, inner_cut_width / 2.0))
        .extrude(flange_thickness)
    )
    l_shape = base.cut(cut)
    """,
)
base_cut_evidence = [
    feature.evidence for feature in base_cut_plan.features
    if feature.operation == "pocket" and feature.evidence.get("suggested_subcad")
]
check(bool(base_cut_evidence), "planner extracts base-band rectangular cut evidence")
check("base_height=0.0" in base_cut_evidence[0]["suggested_subcad"],
      "base-band rectangular cut suggests z-band pocket")

layered_part_plan = plan_pure_subcad_features(
    [],
    """
    flange_leg_length = 80.0
    flange_leg_width = 30.0
    flange_thickness = 8.0
    inner_cut_width = 20.0
    boss_diameter = 20.0
    boss_height = 12.0
    rib_height = 4.0
    rib_width = 6.0
    rib_spacing = 12.0
    fusion_overlap = 0.5
    base = cq.Workplane('XY').rect(flange_leg_length, flange_leg_width).extrude(flange_thickness)
    cut = (
        cq.Workplane('XY')
        .rect(flange_leg_length - inner_cut_width, flange_leg_width - inner_cut_width)
        .translate((inner_cut_width / 2.0, inner_cut_width / 2.0))
        .extrude(flange_thickness)
    )
    l_shape = base.cut(cut)
    boss = (
        cq.Workplane('XY')
        .center(inner_cut_width / 2.0, inner_cut_width / 2.0)
        .circle(boss_diameter / 2.0)
        .extrude(boss_height)
        .translate((0, 0, flange_thickness - fusion_overlap))
    )
    result = l_shape.union(boss)
    for i in range(3):
        rib_x = -4.0 + i * rib_spacing
        rib = (
            cq.Workplane('XY')
            .center(rib_x, 2.0)
            .rect(rib_spacing * 0.8, rib_width)
            .extrude(rib_height)
            .translate((0, 0, flange_thickness - fusion_overlap))
        )
        result = result.union(rib)
    """,
)
layered_evidence = [
    feature.evidence for feature in layered_part_plan.features
    if feature.operation == "layered_retained_profile_plan"
]
check(bool(layered_evidence), "planner emits full layered retained-profile plan")
check(
    "Stock.rectangular(80, 40, 19.5)" in layered_evidence[0]["suggested_subcad"],
    "layered retained-profile plan expands stock to full boss envelope",
)
layered_with_holes_code = """
flange_leg_length = 80.0
flange_leg_width = 30.0
flange_thickness = 8.0
inner_cut_width = 20.0
boss_diameter = 20.0
boss_height = 12.0
rib_height = 4.0
rib_width = 6.0
rib_spacing = 12.0
fusion_overlap = 0.5
hole_diameter = 5.5
hole_positions = [(-20.0, 5.0), (20.0, 5.0), (30.0, -20.0), (30.0, 20.0)]
base = cq.Workplane('XY').rect(flange_leg_length, flange_leg_width).extrude(flange_thickness)
cut = (
    cq.Workplane('XY')
    .rect(flange_leg_length - inner_cut_width, flange_leg_width - inner_cut_width)
    .translate((inner_cut_width / 2.0, inner_cut_width / 2.0))
    .extrude(flange_thickness)
)
l_shape = base.cut(cut)
boss = (
    cq.Workplane('XY')
    .center(inner_cut_width / 2.0, inner_cut_width / 2.0)
    .circle(boss_diameter / 2.0)
    .extrude(boss_height)
    .translate((0, 0, flange_thickness - fusion_overlap))
)
result = l_shape.union(boss)
for i in range(3):
    rib_x = -4.0 + i * rib_spacing
    rib = (
        cq.Workplane('XY')
        .center(rib_x, 2.0)
        .rect(rib_spacing * 0.8, rib_width)
        .extrude(rib_height)
        .translate((0, 0, flange_thickness - fusion_overlap))
    )
    result = result.union(rib)
for (x, y) in hole_positions:
    result = result.faces('>Z').workplane().center(x, y).hole(hole_diameter)
"""
deterministic_code = build_deterministic_subcad_code(layered_with_holes_code, [])
check(deterministic_code is not None, "planner builds deterministic layered-retained SubCAD code")
check(
    ".drill(5.5, through=True, cx=30, cy=20)" in deterministic_code,
    "deterministic layered-retained code includes source-derived drill positions",
)
deterministic_exec = run_subcad(deterministic_code)
check(deterministic_exec["success"], "deterministic layered-retained SubCAD code executes")

box_chamfer_code = "result = cq.Workplane('XY').box(20,20,2).faces('>Z').edges().chamfer(1,1)"
box_chamfer_subcad = build_deterministic_subcad_code(box_chamfer_code, [])
check(box_chamfer_subcad is not None, "planner builds deterministic box-chamfer SubCAD code")
check(
    "Stock.rectangular(20, 20, 2)" in box_chamfer_subcad
    and '.edge_chamfer(">Z", width=1)' in box_chamfer_subcad,
    "deterministic box-chamfer code preserves dimensions and top chamfer",
)
box_chamfer_exec = run_subcad(box_chamfer_subcad)
check(box_chamfer_exec["success"], "deterministic box-chamfer SubCAD code executes")

top_rib_code = """
plate_length = 80.0
plate_width = 60.0
plate_thickness = 5.0
rib_height = 6.0
rib_width = 20.0
rib_margin = 10.0
mount_hole_diameter = 6.0
mount_hole_spacing_x = 60.0
mount_hole_spacing_y = 40.0
chamfer_size = 1.0
fillet_radius = 0.5
base_sketch = cq.Sketch().rect(plate_length, plate_width)
result = cq.Workplane("XY").placeSketch(base_sketch).extrude(plate_thickness)
rib_sketch = cq.Sketch().rect(rib_width, plate_width - 2 * rib_margin)
rib_center_x = plate_length/2 - rib_margin - rib_width/2
result = (
    result
    .faces(">Z")
    .workplane()
    .center(rib_center_x, 0)
    .placeSketch(rib_sketch)
    .extrude(rib_height)
)
mount_points = [
    (-mount_hole_spacing_x/2, -mount_hole_spacing_y/2),
    ( mount_hole_spacing_x/2, -mount_hole_spacing_y/2),
    ( mount_hole_spacing_x/2,  mount_hole_spacing_y/2),
    (-mount_hole_spacing_x/2,  mount_hole_spacing_y/2),
]
result = result.faces(">Z").workplane().pushPoints(mount_points).hole(mount_hole_diameter)
result = result.edges("|Z").chamfer(chamfer_size)
result = result.edges(">Z").fillet(fillet_radius)
"""
top_rib_subcad = build_deterministic_subcad_code(top_rib_code, [])
check(top_rib_subcad is not None, "planner builds deterministic top-rib SubCAD code")
check(
    "Stock.rectangular(80, 60, 11)" in top_rib_subcad
    and ".rib(width=40, length=20, height=6, cx=20, cy=0)" in top_rib_subcad,
    "deterministic top-rib code preserves stock and rib dimensions",
)
check(".drill(6, through=True, cx=-30, cy=-20)" in top_rib_subcad,
      "deterministic top-rib code includes source pushPoint drills")
top_rib_exec = run_subcad(top_rib_subcad)
check(top_rib_exec["success"], "deterministic top-rib SubCAD code executes")

polar_plan = plan_pure_subcad_features(
    [],
    """
    rib_radius = 36.0
    rib_count = 6
    rib_width = 4.0
    rib_thickness = 1.5
    result = (
        result.faces(">Z")
        .workplane()
        .polarArray(radius=rib_radius, count=rib_count, startAngle=0, angle=360)
        .rect(rib_width, rib_thickness)
        .extrude(2.0)
    )
    """,
)
polar_evidence = [
    feature.evidence for feature in polar_plan.features
    if feature.evidence.get("suggested_subcad")
]
check(
    polar_evidence and len(polar_evidence[0].get("profiles", [])) == 6,
    "planner extracts polarArray retained-rib evidence",
)
polar_rib_code = """
outer_diameter = 80.0
inner_diameter = 30.0
plate_thickness = 8.0
rib_width = 4.0
rib_height = 2.0
rib_thickness = 1.5
rib_count = 6
mount_hole_dia = 5.0
mount_hole_offset = 20.0
base = cq.Workplane("XY").circle(outer_diameter / 2).extrude(plate_thickness)
rib_radius = outer_diameter / 2 - rib_width / 2 - 2.0
result = (
    base.faces(">Z").workplane()
    .polarArray(radius=rib_radius, count=rib_count, startAngle=0, angle=360)
    .rect(rib_width, rib_thickness)
    .extrude(rib_height)
)
result = result.faces("<Z").workplane().hole(inner_diameter)
mount_radius = inner_diameter / 2 + mount_hole_offset
result = (
    result.faces("<Z").workplane()
    .polarArray(radius=mount_radius, count=4, startAngle=0, angle=360)
    .hole(mount_hole_dia)
)
"""
polar_rib_subcad = build_deterministic_subcad_code(polar_rib_code, [])
check(polar_rib_subcad is not None, "planner builds deterministic cylindrical polar-rib SubCAD code")
check(
    "Stock.cylindrical(80, 10)" in polar_rib_subcad
    and ".machine_around_profiles(" in polar_rib_subcad,
    "deterministic polar-rib code preserves cylindrical stock and retained ribs",
)
check(".drill(30, through=True, cx=0.0, cy=0.0)" in polar_rib_subcad,
      "deterministic polar-rib code includes center bore")
check(".drill(5, through=True, cx=35, cy=0)" in polar_rib_subcad,
      "deterministic polar-rib code includes polar mount holes")
polar_rib_exec = run_subcad(polar_rib_subcad)
check(polar_rib_exec["success"], "deterministic cylindrical polar-rib SubCAD code executes")

shell_cover_code = """
outer_radius = 40
cover_height = 10
shell_thickness = 2
sensor_pocket_width = 15
sensor_pocket_length = 20
sensor_pocket_depth = 5
sensor_offset = 20
fillet_radius = 1
hole_diameter = 5
mount_radius = 30
cable_hole_diameter = 3
outer = cq.Workplane('XY').circle(outer_radius).extrude(cover_height)
inner = cq.Workplane('XY').circle(outer_radius - shell_thickness).extrude(cover_height)
cover_shell = outer.cut(inner)
pocketed = cover_shell.faces('>Z').workplane().center(sensor_offset, 0).rect(sensor_pocket_width, sensor_pocket_length).cutBlind(-sensor_pocket_depth)
holes = pocketed.faces('>Z').workplane().polarArray(mount_radius, 0, 360/3, 3).hole(hole_diameter)
cable = holes.faces('>Z').workplane().center(sensor_offset, 0).circle(cable_hole_diameter/2).cutBlind(-sensor_pocket_depth)
result = cable.edges('|Z').fillet(fillet_radius)
"""
shell_cover_subcad = build_deterministic_subcad_code(shell_cover_code, [])
check(shell_cover_subcad is not None, "planner builds deterministic cylindrical shell-cover SubCAD code")
check(
    "Stock.cylindrical(80, 10)" in shell_cover_subcad
    and ".circular_pocket(76, depth=10" in shell_cover_subcad
    and ".edge_fillet(\"|Z\", radius=1)" in shell_cover_subcad,
    "deterministic shell-cover code preserves hollow shell and vertical fillets",
)
shell_cover_exec = run_subcad(shell_cover_subcad)
check(shell_cover_exec["success"], "deterministic cylindrical shell-cover SubCAD code executes")

inner_rib_cage_code = """
cage_length = 80.0
outer_diameter = 70.0
wall_thickness = 5.0
inner_diameter = outer_diameter - 2 * wall_thickness
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
rib_width = 3.0
rib_height = (outer_radius - inner_radius) - 2.0
rib_spacing_angle = 30.0
fillet_radius = 4.0
outer_cyl = cq.Workplane("XY").circle(outer_radius).extrude(cage_length).edges(">Z").fillet(fillet_radius).edges("<Z").fillet(fillet_radius)
inner_hole = cq.Workplane("XY").circle(inner_radius).extrude(cage_length)
cage_base = outer_cyl.cut(inner_hole)
rib_center_offset = inner_radius + rib_height / 2.0
single_rib = cq.Workplane("XY").rect(rib_width, rib_height).extrude(cage_length).translate((rib_center_offset, 0, 0))
num_ribs = int(360.0 / rib_spacing_angle)
result = cage_base
for i in range(num_ribs):
    angle = i * rib_spacing_angle
    rib = single_rib.rotate((0, 0, 0), (0, 0, 1), angle)
    result = result.union(rib)
"""
inner_rib_cage_subcad = build_deterministic_subcad_code(inner_rib_cage_code, [])
check(inner_rib_cage_subcad is not None, "planner builds deterministic inner-rib cage SubCAD code")
check(
    "Stock.cylindrical(70, 80)" in inner_rib_cage_subcad
    and ".circular_pocket(60, depth=80" in inner_rib_cage_subcad
    and "'type': 'rib'" not in inner_rib_cage_subcad,
    "deterministic inner-rib cage code preserves bore and omits absorbed ribs",
)
inner_rib_cage_exec = run_subcad(inner_rib_cage_subcad)
check(inner_rib_cage_exec["success"], "deterministic cylindrical inner-rib cage SubCAD code executes")

annular_rib_code = """
plate_diameter = 80.0
plate_thickness = 5.0
blind_hole_diameter = 20.0
blind_hole_depth = 3.5
rib_offset = 5.0
rib_width = 6.0
rib_height = 3.0
mount_hole_diameter = 5.0
mount_hole_radius = 30.0
chamfer_distance = 0.5
base = cq.Workplane("XY").circle(plate_diameter/2).extrude(plate_thickness)
base = base.faces(">Z").workplane().hole(blind_hole_diameter, blind_hole_depth)
outer_rib_radius = plate_diameter/2 - rib_offset
inner_rib_radius = outer_rib_radius - rib_width
rib = cq.Workplane("XY").circle(outer_rib_radius).extrude(rib_height)
inner_cut = cq.Workplane("XY").circle(inner_rib_radius).extrude(rib_height)
rib = rib.cut(inner_cut)
rib = rib.translate((0, 0, plate_thickness))
result = base.union(rib)
result = result.faces("<Z").workplane().pushPoints([
    (mount_hole_radius, 0),
    (0, mount_hole_radius),
    (-mount_hole_radius, 0),
    (0, -mount_hole_radius)
]).hole(mount_hole_diameter)
result = result.edges(">Z").chamfer(chamfer_distance)
"""
annular_rib_subcad = build_deterministic_subcad_code(annular_rib_code, [])
check(annular_rib_subcad is not None, "planner builds deterministic annular-rib SubCAD code")
check(
    "Stock.cylindrical(80, 8)" in annular_rib_subcad
    and ".machine_around_cylinder(70, height=3" in annular_rib_subcad
    and ".circular_pocket(58, depth=3" in annular_rib_subcad,
    "deterministic annular-rib code preserves ring dimensions",
)
check("base_height=1.5" in annular_rib_subcad,
      "deterministic annular-rib code places blind center recess in the base band")
annular_rib_exec = run_subcad(annular_rib_subcad)
check(annular_rib_exec["success"], "deterministic annular-rib SubCAD code executes")

grid_boss_code = """
outer_diameter = 80.0
plate_thickness = 8.0
central_hole_diameter = 30.0
blind_hole_depth = 5.0
vent_hole_diameter = 8.0
vent_hole_radius = 30.0
emboss_diameter = 5.0
emboss_height = 2.0
emboss_grid_rows = 5
emboss_grid_cols = 5
emboss_spacing = 10.0
edge_chamfer = 1.0
base = cq.Workplane("XY").circle(outer_diameter / 2).extrude(plate_thickness)
blind = cq.Workplane("XY").circle(central_hole_diameter / 2).extrude(blind_hole_depth)
base = base.cut(blind)
base = (
    base.faces(">Z").workplane()
    .polarArray(count=4, startAngle=0, angle=360, radius=vent_hole_radius)
    .hole(vent_hole_diameter)
)
base = base.edges(">Z").chamfer(edge_chamfer)
emboss = (
    base.faces(">Z").workplane()
    .rarray(emboss_spacing, emboss_spacing, emboss_grid_cols, emboss_grid_rows, center=True)
    .circle(emboss_diameter / 2)
    .extrude(emboss_height)
)
result = base.union(emboss)
"""
grid_boss_subcad = build_deterministic_subcad_code(grid_boss_code, [])
check(grid_boss_subcad is not None, "planner builds deterministic cylindrical grid-boss SubCAD code")
check(
    "Stock.cylindrical(80, 10)" in grid_boss_subcad
    and grid_boss_subcad.count("'type': 'circle'") == 25,
    "deterministic grid-boss code preserves stock and 5x5 boss array",
)
check("machine_around_cylinder(78, height=0.8" in grid_boss_subcad,
      "deterministic grid-boss code adds cylindrical chamfer relief")
grid_boss_exec = run_subcad(grid_boss_subcad)
check(grid_boss_exec["success"], "deterministic cylindrical grid-boss SubCAD code executes")

washer_code = """
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 6.0
mounting_hole_diameter = 5.0
mount_radius = outer_diameter/2 - 8.0
chamfer_dist = 0.7
base = (
    cq.Workplane("XY")
    .circle(outer_diameter/2)
    .circle(inner_diameter/2)
    .extrude(thickness)
)
base = (
    base.faces(">Z").workplane()
    .polarArray(radius=mount_radius, count=4, startAngle=0, angle=360)
    .hole(mounting_hole_diameter)
)
base = base.edges().chamfer(chamfer_dist)
result = base
"""
washer_subcad = build_deterministic_subcad_code(washer_code, [])
check(washer_subcad is not None, "planner builds deterministic cylindrical washer SubCAD code")
check(
    "Stock.cylindrical(80, 6)" in washer_subcad
    and ".drill(30, through=True, cx=0.0, cy=0.0)" in washer_subcad,
    "deterministic washer code preserves outer and inner diameters",
)
check(".edge_chamfer(\"all_edges\", width=0.7)" in washer_subcad,
      "deterministic washer code preserves global chamfer")
washer_exec = run_subcad(washer_subcad)
check(washer_exec["success"], "deterministic cylindrical washer SubCAD code executes")

star_plate_code = """
import math
outer_diameter = 100.0
plate_thickness = 6.0
star_points = 5
star_outer_radius = 35.0
star_inner_radius = 15.0
blind_hole_diameter = 9.0
blind_hole_depth = plate_thickness * 0.8
chamfer_size = 0.8
mount_hole_diameter = 6.0
mount_hole_radius = outer_diameter/2 - 12.0
rib_width = 8.0
rib_depth = plate_thickness * 0.5
rib_spacing_angle = 30.0
result = cq.Workplane("XY").circle(outer_diameter/2).extrude(plate_thickness)
angle_step = math.pi / star_points
pts = []
for i in range(2*star_points):
    r = star_outer_radius if i % 2 == 0 else star_inner_radius
    angle = i * angle_step
    pts.append((r*math.cos(angle), r*math.sin(angle)))
star_cut = cq.Workplane("XY").polyline(pts).close().extrude(-plate_thickness)
result = result.cut(star_cut)
result = result.faces(">Z").workplane().hole(blind_hole_diameter, blind_hole_depth)
mount_pts = []
for i in range(4):
    angle = math.radians(i*90)
    mount_pts.append((mount_hole_radius*math.cos(angle), mount_hole_radius*math.sin(angle)))
result = result.faces(">Z").workplane().pushPoints(mount_pts).hole(mount_hole_diameter)
num_pockets = int(360 / rib_spacing_angle)
for i in range(num_pockets):
    angle = math.radians(i * rib_spacing_angle)
    offset = outer_diameter/2 - rib_width/2 - 5
    x = offset * math.cos(angle)
    y = offset * math.sin(angle)
    result = result.faces(">Z").workplane().center(x, y).rect(rib_width, rib_width).cutBlind(rib_depth)
result = result.edges().chamfer(chamfer_size)
"""
star_plate_subcad = build_deterministic_subcad_code(star_plate_code, [])
check(star_plate_subcad is not None, "planner builds deterministic star-plate SubCAD code")
check(
    "Stock.cylindrical(100, 6)" in star_plate_subcad
    and ".profile_pocket({'type': 'polygon'" not in star_plate_subcad
    and star_plate_subcad.count(".profile_pocket(") == 12,
    "deterministic star-plate code omits no-op star cut and preserves radial pockets",
)
check(".drill(6, through=True, cx=38, cy=0)" in star_plate_subcad,
      "deterministic star-plate code preserves mount holes")
star_plate_exec = run_subcad(star_plate_subcad)
check(star_plate_exec["success"], "deterministic cylindrical star-plate SubCAD code executes")


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
    .machine_around_profiles([
        {"type": "rib", "width": 2, "length": 8, "cx": -8, "cy": 0},
        {"type": "rib", "width": 2, "length": 8, "cx": 8, "cy": 0},
    ], 2.0)
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
    "machine_around_profiles",
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
    .slot(10, 3, 1, face_selector="<Z")
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
through_pocket = base.profile_pocket(profile, 20.0, through=True)
check(through_pocket.volume < profile_part.volume,
      "profile_pocket supports internal through cuts")
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
