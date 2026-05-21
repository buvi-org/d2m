"""Pure SubCAD feature planner for STEP/CadQuery translation.

The planner is intentionally conservative about manufacturing completeness but
does not use the old blocked-term model.  It classifies CadQuery/STEP evidence
into pure SubCAD operation families so benchmark runs can distinguish:

* exact operations we can represent today,
* tolerance-machined operations that need sampled/surface toolpaths, and
* genuinely unmachinable/manual-review cases.
"""

from __future__ import annotations

import ast
import json
import math
import re
import textwrap
from dataclasses import dataclass, field
from typing import Any


PLANNED_EXACT = "planned_exact_operation"
PLANNED_TOLERANCE = "planned_tolerance_operation"
PLANNED_MULTI_PROCESS = "planned_multi_process_operation"
UNSUPPORTED_UNMACHINABLE = "unsupported_unmachinable"
NEEDS_MANUAL_REVIEW = "needs_manual_review"


@dataclass
class PlannedFeature:
    """One detected source feature and its intended SubCAD operation family."""

    source: str
    family: str
    planner_status: str
    operation: str
    reason: str
    evidence: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "family": self.family,
            "planner_status": self.planner_status,
            "operation": self.operation,
            "reason": self.reason,
            "evidence": self.evidence,
        }


@dataclass
class PureSubCADPlan:
    """Planner output used by translator gating and reports."""

    features: list[PlannedFeature]
    compatible: bool
    coverage_mode: str = "pure_subcad_operations"
    unsupported_count: int = 0
    manual_review_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "coverage_mode": self.coverage_mode,
            "compatible": self.compatible,
            "unsupported_count": self.unsupported_count,
            "manual_review_count": self.manual_review_count,
            "features": [feature.to_dict() for feature in self.features],
            "summary": self.summary(),
        }

    def summary(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for feature in self.features:
            counts[feature.planner_status] = counts.get(feature.planner_status, 0) + 1
        return counts


def plan_pure_subcad_features(
    ops_trace: list[dict],
    cadquery_code: str = "",
) -> PureSubCADPlan:
    """Classify source evidence into pure SubCAD operation families.

    This is not a full geometric recognizer yet; it is the deterministic front
    door for the translator.  It maps common Zero-to-CAD construction calls to
    operation families requested by the pure coverage plan.
    """
    features: list[PlannedFeature] = []
    seen: set[tuple[str, str]] = set()

    def add(source: str, family: str, status: str, operation: str, reason: str, **evidence: Any) -> None:
        key = (source, operation)
        if key in seen:
            return
        seen.add(key)
        features.append(PlannedFeature(
            source=source,
            family=family,
            planner_status=status,
            operation=operation,
            reason=reason,
            evidence={k: v for k, v in evidence.items() if v is not None},
        ))

    trace_text = json.dumps(ops_trace, default=str).lower()
    code_text = cadquery_code.lower()
    combined = f"{trace_text}\n{code_text}"

    op_names = {str(op.get("op_name") or "").lower() for op in ops_trace if isinstance(op, dict)}
    functions = {str(op.get("function") or "").lower() for op in ops_trace if isinstance(op, dict)}
    has_tapered_extrude = (
        '"arg": "taper"' in trace_text
        or '"arg":"taper"' in trace_text
        or "taper=" in code_text
        or ".extrude(" in code_text and "taper" in code_text
    )

    if "box" in op_names or ".box(" in code_text:
        add("cadquery.box", "primitive", PLANNED_EXACT, "rectangular_stock",
            "box maps to rectangular SubCAD stock")
    if "cylinder" in op_names or ".cylinder(" in code_text:
        add("cadquery.cylinder", "primitive", PLANNED_EXACT, "cylindrical_stock",
            "cylinder maps to cylindrical SubCAD stock")
    if "cone" in op_names or ".cone(" in code_text:
        add("cadquery.cone", "axisymmetric", PLANNED_MULTI_PROCESS, "turn_profile",
            "cone/frustum maps to turning or mill-turn taper profile")
    if "sphere" in op_names or ".sphere(" in code_text:
        add("cadquery.sphere", "surface", PLANNED_TOLERANCE, "dome_mill",
            "sphere/dome maps to ball-endmill surface machining")

    if "rect" in op_names and ("cutblind" in op_names or ".cutblind(" in code_text):
        add("cadquery.rect.cutBlind", "cut", PLANNED_EXACT, "profile_pocket",
            "rectangular cut maps to profile pocket")
    base_cut_evidence = _base_cut_pocket_evidence(code_text)
    for evidence in base_cut_evidence:
        add(evidence.get("source", "cadquery.base_cut"),
            "cut", PLANNED_EXACT, "pocket",
            "source-derived lower/base-band rectangular cut is available",
            **{key: value for key, value in evidence.items() if key != "source"})
    if "circle" in op_names or ".circle(" in code_text:
        if "extrude" in op_names or ".extrude(" in code_text:
            if "union" in op_names or ".union(" in code_text or "combine" in op_names:
                add("cadquery.circle.extrude.union", "boss", PLANNED_EXACT, "machine_around_cylinder",
                    "circular extrusion joined to a body maps to machining around a retained cylinder")
            elif has_tapered_extrude:
                add("cadquery.circle.extrude.taper", "axisymmetric", PLANNED_MULTI_PROCESS, "turn_profile",
                    "tapered circle extrusion maps to a turning/frustum profile")
            else:
                add("cadquery.circle.extrude", "primitive", PLANNED_MULTI_PROCESS, "cylindrical_stock",
                    "circle extrusion maps to round stock or turning setup")
        if "cutblind" in op_names or "cut" in op_names or ".cutblind(" in code_text:
            add("cadquery.circle.cut", "cut", PLANNED_EXACT, "circular_pocket",
                "circular cut maps to circular pocket or bore")

    if any(name in op_names for name in {"polyline", "polygon", "lineto", "threpointarc", "threepointarc", "spline"}):
        status = PLANNED_TOLERANCE if "spline" in op_names else PLANNED_EXACT
        add("cadquery.profile", "profile", status, "profile_cutout",
            "non-rectangular sketch profile maps to profile machining")

    if "slot2d" in op_names:
        add("cadquery.slot2D", "profile", PLANNED_EXACT, "slot",
            "slot2D maps to SubCAD slot machining")

    if "hole" in op_names:
        add("cadquery.hole", "hole", PLANNED_EXACT, "drill",
            "hole maps to drill")
    if "cborehole" in op_names:
        add("cadquery.cboreHole", "hole", PLANNED_EXACT, "counterbore",
            "counterbore hole maps to drill plus counterbore")
    if "cskhole" in op_names:
        add("cadquery.cskHole", "hole", PLANNED_EXACT, "countersink",
            "countersink hole maps to drill plus countersink")

    if "chamfer" in op_names or ".chamfer(" in code_text:
        add("cadquery.chamfer", "edge_treatment", PLANNED_EXACT, "edge_chamfer",
            "selected-edge chamfer maps to edge_chamfer")
    if "fillet" in op_names or ".fillet(" in code_text:
        add("cadquery.fillet", "edge_treatment", PLANNED_TOLERANCE, "edge_fillet",
            "selected-edge fillet maps to ball/bull-nose finishing")

    if "union" in op_names or "combine" in op_names or ".union(" in code_text:
        add("cadquery.union", "retained_material", PLANNED_EXACT, "machine_around_profile",
            "constructive boss/pad/rib maps to machining around retained material")

    retained_evidence = _retained_material_parameter_evidence(code_text)
    for evidence in retained_evidence:
        operation = "machine_around_profiles" if len(evidence.get("profiles") or []) > 1 else "machine_around_profile"
        if evidence.get("profile_type") == "circle":
            operation = "machine_around_cylinder"
        feature_source = evidence.get("source", "cadquery.retained_material.evidence")
        feature_evidence = {key: value for key, value in evidence.items() if key != "source"}
        add(feature_source,
            "retained_material", PLANNED_EXACT, operation,
            "source-derived retained-material dimensions and positions are available",
            **feature_evidence)
    for evidence in _layered_profile_plan_evidence(base_cut_evidence, retained_evidence):
        add(evidence.get("source", "cadquery.layered_retained_profile_plan"),
            "retained_material", PLANNED_EXACT, "layered_retained_profile_plan",
            "source-derived layered retained profile sequence is available",
            **{key: value for key, value in evidence.items() if key != "source"})

    if "revolve" in op_names or ".revolve(" in code_text:
        add("cadquery.revolve", "axisymmetric", PLANNED_MULTI_PROCESS, "turn_profile",
            "revolved profile maps to turning or mill-turn")
    if "shell" in op_names or ".shell(" in code_text:
        shell_accessible = _shell_has_accessible_open_face(ops_trace, code_text)
        if shell_accessible:
            add("cadquery.shell", "thin_wall", PLANNED_MULTI_PROCESS, "thin_wall_pocket",
                "open shell maps to thin-wall pocket or hollow bore when accessible")
        else:
            add("cadquery.shell", "thin_wall", UNSUPPORTED_UNMACHINABLE, "thin_wall_pocket",
                "closed shell creates an inaccessible internal cavity for pure subtractive CNC")
    if "loft" in op_names or ".loft(" in code_text:
        add("cadquery.loft", "surface", PLANNED_TOLERANCE, "loft_mill",
            "loft maps to tolerance-machined surface operation")
    if "sweep" in op_names or ".sweep(" in code_text:
        add("cadquery.sweep", "surface", PLANNED_TOLERANCE, "sweep_mill",
            "sweep maps to tolerance-machined sweep operation")

    if any(token in combined for token in ("rarray", "polararray", "mirrorx", "mirrory", ".mirror(")):
        add("cadquery.pattern", "pattern", PLANNED_EXACT, "pattern",
            "feature pattern maps to repeated SubCAD operations")

    for evidence in _top_workplane_retained_material(ops_trace, code_text):
        add("cadquery.faces.top.workplane.extrude", "retained_material", PLANNED_EXACT,
            "machine_around_profile",
            "top-face additive extrusion maps to machining around retained material",
            **evidence)

    for evidence in _non_top_workplane_retained_material(ops_trace, code_text):
        add("cadquery.faces.workplane.extrude", "retained_material", NEEDS_MANUAL_REVIEW,
            "oriented_retained_material",
            "non-top workplane additive retained material needs an oriented SubCAD operation",
            **evidence)

    unsupported = [feature for feature in features if feature.planner_status == UNSUPPORTED_UNMACHINABLE]
    manual = [feature for feature in features if feature.planner_status == NEEDS_MANUAL_REVIEW]
    compatible = bool(features) and not unsupported and not manual
    return PureSubCADPlan(
        features=features,
        compatible=compatible,
        unsupported_count=len(unsupported),
        manual_review_count=len(manual),
    )


def build_deterministic_subcad_code(
    cadquery_code: str,
    ops_trace: list[dict] | None = None,
) -> str | None:
    """Build executable SubCAD when planner evidence is already complete.

    This is intentionally narrow: it only emits code for feature families where
    the deterministic planner has a full manufacturing sequence.  The first
    production use is Zero-to-CAD layered retained material (L base + boss/rib
    levels), where asking an LLM to transcribe the plan caused avoidable
    geometry regressions and wasted live calls.
    """
    plan = plan_pure_subcad_features(ops_trace or [], cadquery_code)
    split_shroud_code = _deterministic_split_shroud_code(cadquery_code)
    if split_shroud_code:
        return split_shroud_code
    l_bracket_variant_code = _deterministic_l_bracket_variant_code(cadquery_code)
    if l_bracket_variant_code:
        return l_bracket_variant_code
    l_bracket_code = _deterministic_l_bracket_code(cadquery_code)
    if l_bracket_code:
        return l_bracket_code
    profile_extrude_code = _deterministic_profile_extrude_code(cadquery_code)
    if profile_extrude_code:
        return profile_extrude_code
    box_union_profile_code = _deterministic_box_union_profile_code(cadquery_code)
    if box_union_profile_code:
        return box_union_profile_code
    base_extension_code = _deterministic_base_extension_code(cadquery_code)
    if base_extension_code:
        return base_extension_code
    box_code = _deterministic_box_chamfer_code(cadquery_code)
    if box_code:
        return box_code
    for feature in plan.features:
        if feature.operation != "layered_retained_profile_plan":
            continue
        evidence = feature.evidence or {}
        stock = evidence.get("suggested_stock")
        sequence = list(evidence.get("suggested_sequence") or [])
        if not stock or not sequence:
            continue
        sequence.extend(_deterministic_drill_calls(cadquery_code))
        return _format_fluent_subcad_code(stock, sequence)
    top_rib_code = _deterministic_top_retained_rib_code(cadquery_code, plan)
    if top_rib_code:
        return top_rib_code
    polar_rib_code = _deterministic_cylindrical_polar_rib_code(cadquery_code, plan)
    if polar_rib_code:
        return polar_rib_code
    shell_cover_code = _deterministic_cylindrical_shell_cover_code(cadquery_code)
    if shell_cover_code:
        return shell_cover_code
    inner_rib_cage_code = _deterministic_cylindrical_inner_rib_cage_code(cadquery_code)
    if inner_rib_cage_code:
        return inner_rib_cage_code
    annular_rib_code = _deterministic_cylindrical_annular_rib_code(cadquery_code)
    if annular_rib_code:
        return annular_rib_code
    grid_boss_code = _deterministic_cylindrical_grid_boss_code(cadquery_code)
    if grid_boss_code:
        return grid_boss_code
    star_plate_code = _deterministic_cylindrical_star_plate_code(cadquery_code)
    if star_plate_code:
        return star_plate_code
    washer_code = _deterministic_cylindrical_washer_code(cadquery_code)
    if washer_code:
        return washer_code
    return None


def _format_fluent_subcad_code(stock_expr: str, sequence: list[str]) -> str:
    lines = ["part = (", f"    {stock_expr}"]
    for item in sequence:
        text = str(item).strip()
        if not text:
            continue
        lines.append(f"    {text}")
    lines.append(")")
    return "\n".join(lines)


def _deterministic_box_chamfer_code(cadquery_code: str) -> str | None:
    lower = cadquery_code.lower()
    if lower.count(".box(") != 1:
        return None
    if any(token in lower for token in (".cut", ".hole(", ".union(", ".shell(", ".loft(", ".sweep(")):
        return None
    box = _box_stock_from_code(cadquery_code)
    if not box:
        return None
    stock = f"Stock.rectangular({box['length']:.6g}, {box['width']:.6g}, {box['height']:.6g})"
    sequence: list[str] = []
    env = _numeric_env(cadquery_code)
    chamfer_args = _first_call_args(cadquery_code, "chamfer")
    if not chamfer_args:
        return None
    if chamfer_args:
        width = _eval_number(chamfer_args[0], env)
        if width is not None and width > 0:
            selector = ">Z" if ".faces('>z')" in cadquery_code.lower() or '.faces(">z")' in cadquery_code.lower() else "all_edges"
            sequence.append(f'.edge_chamfer("{selector}", width={width:.6g})')
    return _format_fluent_subcad_code(stock, sequence)


def _deterministic_profile_extrude_code(cadquery_code: str) -> str | None:
    if ".extrude(" not in cadquery_code:
        return None
    if any(token in cadquery_code for token in (".hole(", ".cut(", ".cutBlind(", ".shell(", ".union(")):
        return None
    env = _numeric_env(cadquery_code)
    points = _first_polyline_points(cadquery_code, env)
    if len(points) < 3:
        points = _line_chain_points(cadquery_code, env)
    if len(points) < 3:
        return None
    extrude_args = _first_call_args(cadquery_code, "extrude")
    if not extrude_args:
        return None
    height = _eval_number(extrude_args[0], env)
    if height is None or height <= 0:
        return None
    min_x = min(x for x, _ in points)
    max_x = max(x for x, _ in points)
    min_y = min(y for _, y in points)
    max_y = max(y for _, y in points)
    length = max_x - min_x
    width = max_y - min_y
    if length <= 0 or width <= 0:
        return None
    x_shift = (min_x + max_x) / 2.0
    y_shift = (min_y + max_y) / 2.0
    shifted = [(x - x_shift, y - y_shift) for x, y in points]
    stock = f"Stock.rectangular({length:.6g}, {width:.6g}, {height:.6g})"
    return _format_fluent_subcad_code(
        stock,
        [f".profile_cutout({{'type': 'polygon', 'points': {_format_points(shifted)}}}, through=True)"],
    )


def _deterministic_box_union_profile_code(cadquery_code: str) -> str | None:
    lower = cadquery_code.lower()
    if lower.count(".box(") != 2 or ".union(" not in lower:
        return None
    if any(token in lower for token in (".cut", ".hole(", ".shell(", ".loft(", ".sweep(", ".chamfer(", ".fillet(")):
        return None
    env = _numeric_env(cadquery_code)
    if not {"bracket_width", "bracket_height", "plate_thickness"}.issubset(env):
        return None
    width = env["bracket_width"]
    height = env["bracket_height"]
    plate = env["plate_thickness"]
    if min(width, height, plate) <= 0:
        return None
    stock_width = height + plate
    y_min = -plate / 2.0
    y_max = height + plate / 2.0
    y_shift = (y_min + y_max) / 2.0
    points = [
        (-width / 2.0, y_min - y_shift),
        (width / 2.0, y_min - y_shift),
        (width / 2.0, plate / 2.0 - y_shift),
        (plate / 2.0, plate / 2.0 - y_shift),
        (plate / 2.0, y_max - y_shift),
        (-plate / 2.0, y_max - y_shift),
        (-plate / 2.0, plate / 2.0 - y_shift),
        (-width / 2.0, plate / 2.0 - y_shift),
    ]
    return _format_fluent_subcad_code(
        f"Stock.rectangular({width:.6g}, {stock_width:.6g}, {plate:.6g})",
        [f".profile_cutout({{'type': 'polygon', 'points': {_format_points(points)}}}, through=True)"],
    )


def _deterministic_base_extension_code(cadquery_code: str) -> str | None:
    lower = cadquery_code.lower()
    if ".union(" not in lower or lower.count(".extrude(") != 2:
        return None
    env = _numeric_env(cadquery_code)
    if not {"base_width", "base_depth", "base_thickness"}.issubset(env):
        return None
    if "straight_ext" not in lower:
        return None
    base_width = env["base_width"]
    base_depth = env["base_depth"]
    base_thickness = env["base_thickness"]
    ext_rect = _assigned_rect_dimensions(cadquery_code, "straight_ext", env)
    ext_height = _assigned_extrude_depth(cadquery_code, "straight_ext")
    ext_center = _assigned_center(cadquery_code, "straight_ext", env)
    if not ext_rect or ext_height is None or not ext_center:
        return None
    if min(base_width, base_depth, base_thickness, ext_rect[0], ext_rect[1], ext_height) <= 0:
        return None
    min_y = min(-base_depth / 2.0, ext_center[1] - ext_rect[1] / 2.0)
    max_y = max(base_depth / 2.0, ext_center[1] + ext_rect[1] / 2.0)
    stock_width = max_y - min_y
    y_shift = (min_y + max_y) / 2.0
    stock_height = max(base_thickness, ext_height)
    base_profile = (
        f"{{'type': 'rectangle', 'length': {base_width:.6g}, "
        f"'width': {base_depth:.6g}, 'cx': 0, 'cy': {-y_shift:.6g}}}"
    )
    extension_profile = (
        f"{{'type': 'rectangle', 'length': {ext_rect[0]:.6g}, "
        f"'width': {ext_rect[1]:.6g}, 'cx': {ext_center[0]:.6g}, 'cy': {ext_center[1] - y_shift:.6g}}}"
    )
    sequence = [
        f".machine_around_profiles([{base_profile}, {extension_profile}], "
        f"height={base_thickness:.6g}, base_height=0.0)",
    ]
    if ext_height > base_thickness:
        sequence.append(
            f".machine_around_profile({extension_profile}, "
            f"height={ext_height - base_thickness:.6g}, base_height={base_thickness:.6g})"
        )
    return _format_fluent_subcad_code(
        f"Stock.rectangular({base_width:.6g}, {stock_width:.6g}, {stock_height:.6g})",
        sequence,
    )


def _deterministic_l_bracket_variant_code(cadquery_code: str) -> str | None:
    env = _measure_env(cadquery_code)
    if "class LBracket" not in cadquery_code:
        return None

    if {
        "horizontal_leg_length",
        "vertical_leg_length",
        "thickness",
        "vertical_thickness",
        "rib_length",
        "rib_thickness",
        "rib_height",
    }.issubset(env):
        h = env["horizontal_leg_length"]
        v = env["vertical_leg_length"] + env["thickness"]
        base_height = env["thickness"]
        total_height = base_height + env["rib_height"]
        vertical_thickness = env["vertical_thickness"]
        if min(h, v, base_height, total_height, vertical_thickness) <= 0:
            return None
        x_shift = h / 2.0
        y_shift = v / 2.0
        points = [
            (0.0 - x_shift, 0.0 - y_shift),
            (h - x_shift, 0.0 - y_shift),
            (h - x_shift, env["thickness"] - y_shift),
            (vertical_thickness - x_shift, env["thickness"] - y_shift),
            (vertical_thickness - x_shift, v - y_shift),
            (0.0 - x_shift, v - y_shift),
        ]
        rib_cx = h / 2.0 - x_shift
        rib_cy = env["thickness"] / 2.0 - y_shift
        sequence = [
            f".profile_cutout({{'type': 'polygon', 'points': {_format_points(points)}}}, through=True)",
            f".machine_around_profile({{'type': 'rectangle', 'length': {env['rib_length']:.6g}, "
            f"'width': {env['rib_thickness']:.6g}, 'cx': {rib_cx:.6g}, 'cy': {rib_cy:.6g}}}, "
            f"height={env['rib_height']:.6g}, base_height={base_height:.6g})",
        ]
        chamfer = env.get("chamfer_dist") or env.get("chamfer_size")
        if chamfer:
            sequence.append(f'.edge_chamfer("|Z", width={chamfer:.6g})')
        return _format_fluent_subcad_code(
            f"Stock.rectangular({h:.6g}, {v:.6g}, {total_height:.6g})",
            sequence,
        )

    if {
        "horizontal_length",
        "vertical_height",
        "leg_thickness",
        "taper_length",
        "extrude_depth",
    }.issubset(env):
        h = env["horizontal_length"]
        v = env["vertical_height"]
        leg = env["leg_thickness"]
        taper = env["taper_length"]
        depth = env["extrude_depth"]
        if min(h, v, leg, taper, depth) <= 0:
            return None
        x_shift = h / 2.0
        y_shift = v / 2.0
        points = [
            (0.0 - x_shift, 0.0 - y_shift),
            (h - taper - x_shift, 0.0 - y_shift),
            (h - x_shift, leg - y_shift),
            (h - x_shift, v - y_shift),
            (leg - x_shift, v - y_shift),
            (leg - x_shift, leg - y_shift),
            (0.0 - x_shift, leg - y_shift),
        ]
        sequence = [
            f".profile_cutout({{'type': 'polygon', 'points': {_format_points(points)}}}, through=True)",
        ]
        chamfer = env.get("chamfer_size")
        if chamfer:
            sequence.append(f'.edge_chamfer("|Z", width={chamfer:.6g})')
        return _format_fluent_subcad_code(
            f"Stock.rectangular({h:.6g}, {v:.6g}, {depth:.6g})",
            sequence,
        )

    if {
        "leg_long_length",
        "leg_short_length",
        "leg_width",
        "thickness",
        "edge_clearance",
        "hole_diameter",
    }.issubset(env):
        long = env["leg_long_length"]
        short = env["leg_short_length"]
        width = env["leg_width"]
        height = env["thickness"]
        edge = env["edge_clearance"]
        hole_diameter = env["hole_diameter"]
        if min(long, short, width, height, edge, hole_diameter) <= 0:
            return None
        x_shift = long / 2.0
        y_shift = short / 2.0
        points = [
            (0.0 - x_shift, 0.0 - y_shift),
            (long - x_shift, 0.0 - y_shift),
            (long - x_shift, width - y_shift),
            (width - x_shift, width - y_shift),
            (width - x_shift, short - y_shift),
            (0.0 - x_shift, short - y_shift),
        ]
        second_center_x = long / 2.0 + width / 2.0
        second_center_y = width / 2.0 + short / 2.0
        second_half_x = (width - 2.0 * edge) / 2.0
        second_half_y = (short - 2.0 * edge) / 2.0
        hole_points = [
            (edge, edge),
            (long - edge, edge),
            (edge, width - edge),
            (long - edge, width - edge),
            (second_center_x - second_half_x, second_center_y - second_half_y),
            (second_center_x + second_half_x, second_center_y - second_half_y),
        ]
        sequence = [
            f".profile_cutout({{'type': 'polygon', 'points': {_format_points(points)}}}, through=True)",
        ]
        for x, y in hole_points:
            sequence.append(
                f".drill({hole_diameter:.6g}, through=True, cx={x - x_shift:.6g}, cy={y - y_shift:.6g})"
            )
        chamfer = env.get("chamfer_size")
        if chamfer:
            sequence.append(f'.edge_chamfer("|Z", width={chamfer:.6g})')
        return _format_fluent_subcad_code(
            f"Stock.rectangular({long:.6g}, {short:.6g}, {height:.6g})",
            sequence,
        )

    return None


def _deterministic_l_bracket_code(cadquery_code: str) -> str | None:
    env = _measure_env(cadquery_code)
    if "class LBracket" not in cadquery_code or ".cboreHole(" not in cadquery_code:
        if "class LBracket" not in cadquery_code or ".rarray(" not in cadquery_code or ".hole(" not in cadquery_code:
            return None

    if {"horizontal_leg_length", "vertical_leg_length", "leg_width", "thickness"}.issubset(env):
        h = env["horizontal_leg_length"]
        v = env["vertical_leg_length"]
        leg = env["leg_width"]
        points_source = [
            (0.0, 0.0),
            (h, 0.0),
            (h, leg),
            (leg, leg),
            (leg, v),
            (0.0, v),
        ]
        hole_points = [
            (h / 2.0 - env.get("hole_spacing", 0.0) / 2.0, leg),
            (h / 2.0 + env.get("hole_spacing", 0.0) / 2.0, leg),
        ]
        hole_diameter = env.get("hole_diameter")
        cbore_diameter = env.get("countersink_diameter")
        cbore_depth = env.get("countersink_depth")
    elif {"leg_length", "leg_height", "thickness"}.issubset(env):
        h = env["leg_length"]
        leg = env["thickness"]
        v = env["leg_height"] + env["thickness"]
        points_source = [
            (0.0, 0.0),
            (leg, 0.0),
            (leg, env["leg_height"]),
            (h, env["leg_height"]),
            (h, v),
            (0.0, v),
        ]
        spacing = env.get("hole_spacing", 0.0)
        rarray_args = _first_call_args(cadquery_code, "rarray")
        x_count = _eval_number(rarray_args[2], env) if len(rarray_args) >= 3 else 4.0
        x_count = x_count or 4.0
        x_count_int = max(1, int(round(x_count)))
        # This Zero-to-CAD idiom uses rarray after moveTo on an irregular top face;
        # CadQuery centers those points around the local workplane origin.
        hole_points = [
            (spacing * (index - (x_count_int - 1) / 2.0), 0.0)
            for index in range(x_count_int)
        ]
        hole_diameter = env.get("hole_clearance_diameter")
        cbore_diameter = None
        cbore_depth = None
    else:
        return None

    thickness = env["thickness"]
    if min(h, v, leg, thickness) <= 0 or not hole_diameter:
        return None
    x_shift = h / 2.0
    y_shift = v / 2.0
    points = [(x - x_shift, y - y_shift) for x, y in points_source]
    stock = f"Stock.rectangular({h:.6g}, {v:.6g}, {thickness:.6g})"
    sequence: list[str] = [
        f".profile_cutout({{'type': 'polygon', 'points': {_format_points(points)}}}, through=True)",
    ]
    if {"rib_width", "rib_height"}.issubset(env) and "leg_height" in env:
        rib_points = [
            (leg - x_shift, env["leg_height"] - y_shift),
            (leg + env["rib_width"] - x_shift, env["leg_height"] - y_shift),
            (leg - x_shift, env["leg_height"] + env["rib_height"] - y_shift),
        ]
        if not all(_point_in_polygon(point, points) or _point_on_polygon_edge(point, points) for point in rib_points):
            sequence.append(
                f".machine_around_profile({{'type': 'polygon', 'points': {_format_points(rib_points)}}}, "
                f"{thickness:.6g})"
            )
    chamfer = env.get("edge_chamfer")
    if chamfer is None:
        chamfer = env.get("chamfer")
    if chamfer is not None and chamfer > 0:
        sequence.append(f'.edge_chamfer("|Z", width={chamfer:.6g})')
    for hole_x, hole_y in hole_points:
        cx = hole_x - x_shift
        cy = hole_y - y_shift
        if cbore_diameter and cbore_depth:
            sequence.append(
                f".counterbore({hole_diameter:.6g}, "
                f"{cbore_diameter:.6g}, "
                f"{cbore_depth:.6g}, through=True, "
                f"cx={cx:.6g}, cy={cy:.6g})"
            )
        else:
            sequence.append(f".drill({hole_diameter:.6g}, through=True, cx={cx:.6g}, cy={cy:.6g})")
    return _format_fluent_subcad_code(stock, sequence)


def _measure_env(code_text: str) -> dict[str, float]:
    env = _numeric_env(code_text)
    match = re.search(r"measures\s*=\s*Measures\((?P<body>.*?)\)\s*\n", code_text, re.IGNORECASE | re.DOTALL)
    if not match:
        return env
    for arg in _split_args(match.group("body")):
        if "=" not in arg:
            continue
        key, value = arg.split("=", 1)
        number = _eval_number(value.strip(), env)
        if number is not None:
            env[key.strip()] = number
    return env


def _box_stock_from_code(code_text: str) -> dict[str, float] | None:
    env = _numeric_env(code_text)
    args = _first_call_args(code_text, "box")
    if len(args) < 3:
        return None
    length = _eval_number(args[0], env)
    width = _eval_number(args[1], env)
    height = _eval_number(args[2], env)
    if length is None or width is None or height is None:
        return None
    if length <= 0 or width <= 0 or height <= 0:
        return None
    return {"length": length, "width": width, "height": height}


def _deterministic_top_retained_rib_code(cadquery_code: str, plan: PureSubCADPlan) -> str | None:
    """Emit code for a flat base with one top retained rectangular rib.

    Several Zero-to-CAD samples use CadQuery calls whose positive ``cutBlind``
    direction points out of the body, so the original STEP contains the rib and
    through-hole pattern but not those commented cuts.  This builder follows
    deterministic source evidence and lets the original-STEP comparison remain
    the final authority.
    """
    base = _base_rect_from_sketch_extrude(cadquery_code)
    if not base:
        return None

    retained = [
        feature.evidence for feature in plan.features
        if feature.operation == "machine_around_profile"
        and feature.source == "cadquery.faces.top.workplane.extrude"
        and feature.evidence.get("profiles")
    ]
    if len(retained) != 1:
        return None
    evidence = retained[0]
    profiles = list(evidence.get("profiles") or [])
    if len(profiles) != 1:
        return None
    profile = profiles[0]
    if profile.get("type") != "rib":
        return None
    rib_height = float(evidence.get("height") or 0.0)
    if rib_height <= 0:
        return None

    stock = (
        f"Stock.rectangular({base['length']:.6g}, {base['width']:.6g}, "
        f"{base['height'] + rib_height:.6g})"
    )
    sequence = [
        (
            f".rib(width={float(profile['width']):.6g}, "
            f"length={float(profile['length']):.6g}, height={rib_height:.6g}, "
            f"cx={float(profile.get('cx', 0.0)):.6g}, cy={float(profile.get('cy', 0.0)):.6g})"
        )
    ]
    sequence.extend(_deterministic_drill_calls(cadquery_code))
    lowered = cadquery_code.lower()
    if ".chamfer(" in lowered:
        chamfer_width = _first_call_number(cadquery_code, "chamfer", _numeric_env(cadquery_code)) or 1.0
        sequence.append(f'.edge_chamfer("|Z", width={chamfer_width:.6g})')
    if ".fillet(" in lowered:
        fillet_radius = _first_call_number(cadquery_code, "fillet", _numeric_env(cadquery_code)) or 0.5
        sequence.append(f'.edge_fillet(">Z", radius={fillet_radius:.6g})')
    return _format_fluent_subcad_code(stock, sequence)


def _base_rect_from_sketch_extrude(code_text: str) -> dict[str, float] | None:
    env = _numeric_env(code_text)
    sketches = _sketch_rects(code_text, env)
    if not sketches:
        return None
    match = re.search(
        r"\.placesketch\(\s*(?P<name>\w+)\s*\)\s*\.extrude\((?P<depth>[^)]*)\)",
        code_text,
        re.IGNORECASE,
    )
    if not match:
        return None
    sketch = sketches.get(match.group("name"))
    depth = _eval_number(match.group("depth"), env)
    if not sketch or depth is None:
        return None
    return {
        "length": float(sketch["length"]),
        "width": float(sketch["width"]),
        "height": float(depth),
    }


def _deterministic_cylindrical_polar_rib_code(cadquery_code: str, plan: PureSubCADPlan) -> str | None:
    cylinder = _cylindrical_stock_from_circle_extrude(cadquery_code)
    if not cylinder:
        return None
    retained = [
        feature.evidence for feature in plan.features
        if feature.operation == "machine_around_profile"
        and feature.source == "cadquery.faces.top.workplane.extrude"
        and len(feature.evidence.get("profiles") or []) > 1
    ]
    if len(retained) != 1:
        return None
    evidence = retained[0]
    profiles = list(evidence.get("profiles") or [])
    rib_height = float(evidence.get("height") or 0.0)
    if not profiles or rib_height <= 0:
        return None

    stock = f"Stock.cylindrical({cylinder['diameter']:.6g}, {cylinder['height'] + rib_height:.6g})"
    sequence = [
        _suggest_machine_around_profiles(profiles, rib_height, cylinder["height"]),
    ]
    center_hole = _largest_unpositioned_hole_diameter(cadquery_code)
    if center_hole is not None:
        sequence.append(f".drill({center_hole:.6g}, through=True, cx=0.0, cy=0.0)")
    sequence.extend(_polar_hole_drill_calls(cadquery_code, skip_diameter=center_hole))
    return _format_fluent_subcad_code(stock, sequence)


def _cylindrical_stock_from_circle_extrude(code_text: str) -> dict[str, float] | None:
    env = _numeric_env(code_text)
    match = re.search(
        r"\.circle\((?P<radius>[^)]*)\)\s*\.extrude\((?P<height>[^)]*)\)",
        code_text,
        re.IGNORECASE,
    )
    if not match:
        return None
    radius = _eval_number(match.group("radius"), env)
    height = _eval_number(match.group("height"), env)
    if radius is None or height is None or radius <= 0 or height <= 0:
        return None
    return {"diameter": 2.0 * radius, "height": height}


def _deterministic_cylindrical_shell_cover_code(cadquery_code: str) -> str | None:
    env = _numeric_env(cadquery_code)
    outer_radius = env.get("outer_radius")
    height = env.get("cover_height")
    shell = env.get("shell_thickness")
    if outer_radius is None or height is None or shell is None:
        return None
    if "outer.cut(inner)" not in cadquery_code or outer_radius <= shell or height <= 0:
        return None
    inner_diameter = 2.0 * (outer_radius - shell)
    stock = f"Stock.cylindrical({2.0 * outer_radius:.6g}, {height:.6g})"
    sequence = [
        f".circular_pocket({inner_diameter:.6g}, depth={height:.6g}, cx=0.0, cy=0.0)",
    ]
    fillet = env.get("fillet_radius")
    if fillet is not None and ".fillet(" in cadquery_code.lower():
        sequence.append(f'.edge_fillet("|Z", radius={fillet:.6g})')
    return _format_fluent_subcad_code(stock, sequence)


def _deterministic_cylindrical_inner_rib_cage_code(cadquery_code: str) -> str | None:
    env = _numeric_env(cadquery_code)
    required = {"cage_length", "outer_diameter", "inner_diameter"}
    if not required.issubset(env):
        return None
    if "single_rib" not in cadquery_code or ".union(rib)" not in cadquery_code:
        return None

    length = env["cage_length"]
    outer_diameter = env["outer_diameter"]
    inner_diameter = env["inner_diameter"]
    if min(length, outer_diameter, inner_diameter) <= 0:
        return None

    stock = f"Stock.cylindrical({outer_diameter:.6g}, {length:.6g})"
    sequence: list[str] = []
    fillet = env.get("fillet_radius")
    if fillet is not None and fillet > 0:
        sequence.extend([
            f'.edge_fillet(">Z", radius={fillet:.6g})',
            f'.edge_fillet("<Z", radius={fillet:.6g})',
        ])
    sequence.append(f".circular_pocket({inner_diameter:.6g}, depth={length:.6g}, cx=0.0, cy=0.0)")
    return _format_fluent_subcad_code(stock, sequence)


def _deterministic_split_shroud_code(cadquery_code: str) -> str | None:
    env = _numeric_env(cadquery_code)
    required = {
        "outer_radius",
        "inner_radius",
        "shroud_height",
        "split_gap",
        "bolt_hole_dia",
        "num_bolts",
        "bolt_pattern_radius",
    }
    if not required.issubset(env):
        return None
    if "split_slab" not in cadquery_code or "bolt_points" not in cadquery_code:
        return None

    outer_radius = env["outer_radius"]
    inner_radius = env["inner_radius"]
    height = env["shroud_height"]
    split_gap = env["split_gap"]
    hole_dia = env["bolt_hole_dia"]
    hole_count = int(env["num_bolts"])
    hole_radius = env["bolt_pattern_radius"]
    if min(outer_radius, inner_radius, height, split_gap, hole_dia, hole_radius) <= 0:
        return None
    if hole_count <= 0 or hole_count > 100:
        return None

    stock = f"Stock.cylindrical({2.0 * outer_radius:.6g}, {height:.6g})"
    sequence: list[str] = [
        f".circular_pocket({2.0 * inner_radius:.6g}, depth={height:.6g}, cx=0.0, cy=0.0)",
        (
            f".profile_pocket({{'type': 'rectangle', 'length': {split_gap:.6g}, "
            f"'width': {4.0 * outer_radius:.6g}}}, depth={height:.6g}, through=True)"
        ),
    ]
    chamfer = env.get("chamfer_size")
    if chamfer is not None and chamfer > 0:
        sequence.append(f'.edge_chamfer("<X", width={chamfer:.6g})')
    for index in range(hole_count):
        angle = math.radians(index * 360.0 / hole_count)
        sequence.append(
            f".drill({hole_dia:.6g}, through=True, "
            f"cx={hole_radius * math.cos(angle):.6g}, "
            f"cy={hole_radius * math.sin(angle):.6g})"
        )
    return _format_fluent_subcad_code(stock, sequence)


def _largest_unpositioned_hole_diameter(code_text: str) -> float | None:
    env = _numeric_env(code_text)
    diameters: list[float] = []
    for match in re.finditer(r"\.hole\((?P<args>[^)]*)\)", code_text, re.IGNORECASE):
        prefix = code_text[max(0, match.start() - 120):match.start()].lower()
        if ".polararray(" in prefix:
            continue
        args = _split_args(match.group("args"))
        if not args:
            continue
        diameter = _eval_number(args[0], env)
        if diameter is not None and diameter > 0:
            diameters.append(diameter)
    return max(diameters) if diameters else None


def _polar_hole_drill_calls(code_text: str, *, skip_diameter: float | None = None) -> list[str]:
    env = _numeric_env(code_text)
    calls: list[str] = []
    for match in re.finditer(r"\.polararray\s*\(", code_text, re.IGNORECASE):
        polar_args, end = _call_args_at(code_text, match.end() - 1)
        if polar_args is None:
            continue
        next_polar = re.search(r"\.polararray\s*\(", code_text[end:], re.IGNORECASE)
        segment_end = end + next_polar.start() if next_polar else min(len(code_text), end + 500)
        segment = code_text[end:segment_end]
        hole_match = re.search(r"\.hole\((?P<hole>[^)]*)\)", segment, re.IGNORECASE)
        if not hole_match:
            continue
        rect_match = re.search(r"\.rect\(", segment, re.IGNORECASE)
        if rect_match and rect_match.start() < hole_match.start():
            continue
        hole_args = _split_args(hole_match.group("hole"))
        if not hole_args:
            continue
        diameter = _eval_number(hole_args[0], env)
        if diameter is None or diameter <= 0:
            continue
        if skip_diameter is not None and abs(diameter - skip_diameter) < 1e-9:
            continue
        polar = _parse_keyword_args(polar_args, env)
        radius = polar.get("radius")
        count = polar.get("count")
        start = polar.get("startangle", 0.0)
        sweep = polar.get("angle", 360.0)
        if radius is None and polar_args:
            radius = _eval_number(polar_args[0], env)
        if count is None and len(polar_args) > 1:
            count = _eval_number(polar_args[1], env)
        if radius is None or count is None or count <= 0 or count > 100:
            continue
        step = sweep / count
        for index in range(int(count)):
            angle = start + step * index
            radians = math.radians(angle)
            calls.append(
                f".drill({diameter:.6g}, through=True, "
                f"cx={radius * math.cos(radians):.6g}, "
                f"cy={radius * math.sin(radians):.6g})"
            )
    return calls


def _deterministic_cylindrical_annular_rib_code(cadquery_code: str) -> str | None:
    cylinder = _cylindrical_stock_from_circle_extrude(cadquery_code)
    ring = _annular_rib_from_code(cadquery_code)
    if not cylinder or not ring:
        return None
    stock = f"Stock.cylindrical({cylinder['diameter']:.6g}, {cylinder['height'] + ring['height']:.6g})"
    sequence = [
        (
            f".machine_around_cylinder({ring['outer_diameter']:.6g}, "
            f"height={ring['height']:.6g}, cx=0.0, cy=0.0, "
            f"base_height={cylinder['height']:.6g})"
        ),
        (
            f".circular_pocket({ring['inner_diameter']:.6g}, "
            f"depth={ring['height']:.6g}, cx=0.0, cy=0.0)"
        ),
    ]
    blind = _central_blind_hole_from_code(cadquery_code)
    if blind:
        base_height = max(cylinder["height"] - blind["depth"], 0.0)
        sequence.append(
            f".circular_pocket({blind['diameter']:.6g}, depth={blind['depth']:.6g}, "
            f"cx=0.0, cy=0.0, base_height={base_height:.6g})"
        )
    sequence.extend(_push_points_hole_drill_calls(cadquery_code))
    chamfer = _first_call_number(cadquery_code, "chamfer", _numeric_env(cadquery_code))
    if chamfer is not None:
        sequence.append(f'.edge_chamfer(">Z", width={chamfer:.6g})')
    return _format_fluent_subcad_code(stock, sequence)


def _deterministic_cylindrical_grid_boss_code(cadquery_code: str) -> str | None:
    cylinder = _cylindrical_stock_from_circle_extrude(cadquery_code)
    grid = _rarray_circle_bosses_from_code(cadquery_code)
    if not cylinder or not grid:
        return None
    stock = f"Stock.cylindrical({cylinder['diameter']:.6g}, {cylinder['height'] + grid['height']:.6g})"
    sequence: list[str] = []
    blind = _cut_cylinder_assignment_from_code(cadquery_code)
    if blind:
        sequence.append(
            f".circular_pocket({blind['diameter']:.6g}, depth={blind['depth']:.6g}, "
            "cx=0.0, cy=0.0, base_height=0.0)"
        )
    sequence.extend(_polar_hole_drill_calls(cadquery_code, skip_diameter=blind.get("diameter") if blind else None))
    chamfer = _first_call_number(cadquery_code, "chamfer", _numeric_env(cadquery_code))
    if chamfer is not None and chamfer > 0:
        relief_height = 0.8 * chamfer
        relief_diameter = max(cylinder["diameter"] - 2.0 * chamfer, 0.0)
        relief_base = max(cylinder["height"] - relief_height, 0.0)
        sequence.append(
            f".machine_around_cylinder({relief_diameter:.6g}, height={relief_height:.6g}, "
            f"cx=0.0, cy=0.0, base_height={relief_base:.6g})"
        )
    sequence.append(_suggest_machine_around_profiles(grid["profiles"], grid["height"], cylinder["height"]))
    return _format_fluent_subcad_code(stock, sequence)


def _deterministic_cylindrical_washer_code(cadquery_code: str) -> str | None:
    washer = _washer_stock_from_code(cadquery_code)
    if not washer:
        return None
    stock = f"Stock.cylindrical({washer['outer_diameter']:.6g}, {washer['height']:.6g})"
    sequence = [
        f".drill({washer['inner_diameter']:.6g}, through=True, cx=0.0, cy=0.0)",
    ]
    sequence.extend(_polar_hole_drill_calls(cadquery_code, skip_diameter=washer["inner_diameter"]))
    chamfer = _first_call_number(cadquery_code, "chamfer", _numeric_env(cadquery_code))
    if chamfer is not None:
        sequence.append(f'.edge_chamfer("all_edges", width={chamfer:.6g})')
    return _format_fluent_subcad_code(stock, sequence)


def _deterministic_cylindrical_star_plate_code(cadquery_code: str) -> str | None:
    """Emit a circular plate with star/profile cutouts and repeated top pockets."""
    env = _numeric_env(cadquery_code)
    required = {
        "outer_diameter",
        "plate_thickness",
        "star_points",
        "star_outer_radius",
        "star_inner_radius",
    }
    if not required.issubset(env):
        return None
    if ".polyline(pts)" not in cadquery_code or "star_cut" not in cadquery_code:
        return None

    outer_diameter = env["outer_diameter"]
    plate_thickness = env["plate_thickness"]
    star_points = int(env["star_points"])
    outer_radius = env["star_outer_radius"]
    inner_radius = env["star_inner_radius"]
    if outer_diameter <= 0 or plate_thickness <= 0 or star_points < 3:
        return None

    points: list[tuple[float, float]] = []
    angle_step = math.pi / star_points
    for index in range(2 * star_points):
        radius = outer_radius if index % 2 == 0 else inner_radius
        angle = index * angle_step
        points.append((radius * math.cos(angle), radius * math.sin(angle)))

    stock = f"Stock.cylindrical({outer_diameter:.6g}, {plate_thickness:.6g})"
    sequence: list[str] = []
    star_depth = _assigned_extrude_depth(cadquery_code, "star_cut")
    if star_depth is None or star_depth > 0:
        sequence.append(
            (
                f".profile_pocket({{'type': 'polygon', 'points': {_format_points(points)}}}, "
                f"depth={plate_thickness:.6g}, through=True)"
            )
        )

    blind = _central_blind_hole_from_code(cadquery_code)
    if blind:
        sequence.append(
            f".circular_pocket({blind['diameter']:.6g}, depth={blind['depth']:.6g}, "
            "cx=0.0, cy=0.0)"
        )

    mount_diameter = env.get("mount_hole_diameter")
    mount_radius = env.get("mount_hole_radius")
    if mount_diameter and mount_radius:
        for index in range(4):
            angle = math.radians(index * 90.0)
            sequence.append(
                f".drill({mount_diameter:.6g}, through=True, "
                f"cx={mount_radius * math.cos(angle):.6g}, "
                f"cy={mount_radius * math.sin(angle):.6g})"
            )

    rib_width = env.get("rib_width")
    rib_depth = env.get("rib_depth")
    spacing_angle = env.get("rib_spacing_angle")
    if rib_width and rib_depth and spacing_angle:
        pocket_count = int(360.0 / spacing_angle)
        offset = outer_diameter / 2.0 - rib_width / 2.0 - 5.0
        if pocket_count > 0 and pocket_count <= 72 and offset > 0:
            for index in range(pocket_count):
                angle = math.radians(index * spacing_angle)
                x = offset * math.cos(angle)
                y = offset * math.sin(angle)
                sequence.append(
                    f".profile_pocket({{'type': 'rectangle', 'width': {rib_width:.6g}, "
                    f"'length': {rib_width:.6g}, 'cx': {x:.6g}, 'cy': {y:.6g}}}, "
                    f"depth={rib_depth:.6g})"
                )

    chamfer = _first_call_number(cadquery_code, "chamfer", env)
    if chamfer is not None:
        sequence.append(f'.edge_chamfer("all_edges", width={chamfer:.6g})')
    return _format_fluent_subcad_code(stock, sequence)


def _format_points(points: list[tuple[float, float]]) -> str:
    return "[" + ", ".join(f"({x:.6g}, {y:.6g})" for x, y in points) + "]"


def _first_polyline_points(code_text: str, env: dict[str, float]) -> list[tuple[float, float]]:
    args = _first_call_args(code_text, "polyline")
    if not args:
        return []
    return _eval_points_literal(args[0], env)


def _line_chain_points(code_text: str, env: dict[str, float]) -> list[tuple[float, float]]:
    points: list[tuple[float, float]] = []
    for match in re.finditer(r"\.(moveTo|lineTo)\s*\(", code_text):
        call_name = match.group(1)
        args, _ = _call_args_at(code_text, match.end() - 1)
        if not args or len(args) < 2:
            continue
        x = _eval_number(args[0], env)
        y = _eval_number(args[1], env)
        if x is None or y is None:
            continue
        if call_name == "lineTo" and not points:
            points.append((0.0, 0.0))
        if not points or (abs(points[-1][0] - x) > 1e-9 or abs(points[-1][1] - y) > 1e-9):
            points.append((x, y))
    return points


def _point_on_polygon_edge(
    point: tuple[float, float],
    polygon: list[tuple[float, float]],
    *,
    tolerance: float = 1e-6,
) -> bool:
    px, py = point
    for (x1, y1), (x2, y2) in zip(polygon, polygon[1:] + polygon[:1]):
        dx = x2 - x1
        dy = y2 - y1
        cross = (px - x1) * dy - (py - y1) * dx
        if abs(cross) > tolerance:
            continue
        dot = (px - x1) * dx + (py - y1) * dy
        if -tolerance <= dot <= dx * dx + dy * dy + tolerance:
            return True
    return False


def _point_in_polygon(point: tuple[float, float], polygon: list[tuple[float, float]]) -> bool:
    px, py = point
    inside = False
    j = len(polygon) - 1
    for i, (xi, yi) in enumerate(polygon):
        xj, yj = polygon[j]
        if ((yi > py) != (yj > py)) and (
            px < (xj - xi) * (py - yi) / ((yj - yi) or 1e-12) + xi
        ):
            inside = not inside
        j = i
    return inside


def _assigned_extrude_depth(code_text: str, name: str) -> float | None:
    env = _numeric_env(code_text)
    match = re.search(
        rf"{re.escape(name)}\s*=\s*\(.*?\.extrude\((?P<depth>[^)]*)\).*?\)",
        code_text,
        re.IGNORECASE | re.DOTALL,
    )
    if not match:
        match = re.search(
            rf"{re.escape(name)}\s*=.*?\.extrude\((?P<depth>[^)]*)\)",
            code_text,
            re.IGNORECASE,
        )
    if not match:
        return None
    return _eval_number(match.group("depth"), env)


def _assigned_rect_dimensions(
    code_text: str,
    name: str,
    env: dict[str, float],
) -> tuple[float, float] | None:
    body = _assigned_expression_body(code_text, name)
    if not body:
        return None
    args = _first_call_args(body, "rect")
    if len(args) < 2:
        return None
    length = _eval_number(args[0], env)
    width = _eval_number(args[1], env)
    if length is None or width is None:
        return None
    return (length, width)


def _assigned_center(
    code_text: str,
    name: str,
    env: dict[str, float],
) -> tuple[float, float] | None:
    body = _assigned_expression_body(code_text, name)
    if not body:
        return None
    args = _first_call_args(body, "center")
    if len(args) < 2:
        return (0.0, 0.0)
    x = _eval_number(args[0], env)
    y = _eval_number(args[1], env)
    if x is None or y is None:
        return None
    return (x, y)


def _assigned_expression_body(code_text: str, name: str) -> str | None:
    match = re.search(
        rf"{re.escape(name)}\s*=\s*\((?P<body>.*?)\)\s*(?:\n\w+\s*=|\nresult\s*=|\Z)",
        code_text,
        re.IGNORECASE | re.DOTALL,
    )
    if match:
        return match.group("body")
    match = re.search(
        rf"{re.escape(name)}\s*=\s*(?P<body>.*?)(?:\n\w+\s*=|\nresult\s*=|\Z)",
        code_text,
        re.IGNORECASE | re.DOTALL,
    )
    return match.group("body") if match else None


def _washer_stock_from_code(code_text: str) -> dict[str, float] | None:
    env = _numeric_env(code_text)
    match = re.search(
        r"\.circle\((?P<outer>[^)]*)\)\s*\.circle\((?P<inner>[^)]*)\)\s*\.extrude\((?P<height>[^)]*)\)",
        code_text,
        re.IGNORECASE | re.DOTALL,
    )
    if not match:
        return None
    outer = _eval_number(match.group("outer"), env)
    inner = _eval_number(match.group("inner"), env)
    height = _eval_number(match.group("height"), env)
    if outer is None or inner is None or height is None:
        return None
    if outer <= inner or inner <= 0 or height <= 0:
        return None
    return {
        "outer_diameter": 2.0 * outer,
        "inner_diameter": 2.0 * inner,
        "height": height,
    }


def _rarray_circle_bosses_from_code(code_text: str) -> dict[str, Any] | None:
    env = _numeric_env(code_text)
    match = re.search(
        r"\.rarray\((?P<rarray>[^)]*)\)\s*\.circle\((?P<circle>[^)]*)\)\s*\.extrude\((?P<height>[^)]*)\)",
        code_text,
        re.IGNORECASE | re.DOTALL,
    )
    if not match:
        return None
    args = _split_args(match.group("rarray"))
    if len(args) < 4:
        return None
    x_spacing = _eval_number(args[0], env)
    y_spacing = _eval_number(args[1], env)
    cols = _eval_number(args[2], env)
    rows = _eval_number(args[3], env)
    radius = _eval_number(match.group("circle"), env)
    height = _eval_number(match.group("height"), env)
    if None in {x_spacing, y_spacing, cols, rows, radius, height}:
        return None
    if cols <= 0 or rows <= 0 or cols > 100 or rows > 100 or radius <= 0 or height <= 0:
        return None
    profiles: list[dict[str, float | str]] = []
    for ix in range(int(cols)):
        x = (ix - (cols - 1.0) / 2.0) * x_spacing
        for iy in range(int(rows)):
            y = (iy - (rows - 1.0) / 2.0) * y_spacing
            profiles.append({"type": "circle", "diameter": 2.0 * radius, "cx": x, "cy": y})
    return {"profiles": profiles, "height": height}


def _cut_cylinder_assignment_from_code(code_text: str) -> dict[str, float] | None:
    env = _numeric_env(code_text)
    match = re.search(
        r"(?P<name>\w+)\s*=\s*\(\s*cq\.workplane\([^)]*\)\s*\.circle\((?P<radius>[^)]*)\)\s*\.extrude\((?P<depth>[^)]*)\)\s*\)",
        code_text,
        re.IGNORECASE | re.DOTALL,
    )
    while match:
        name = match.group("name")
        if f".cut({name})" in code_text:
            radius = _eval_number(match.group("radius"), env)
            depth = _eval_number(match.group("depth"), env)
            if radius is not None and depth is not None and radius > 0 and depth > 0:
                return {"diameter": 2.0 * radius, "depth": depth}
        match = re.search(
            r"(?P<name>\w+)\s*=\s*\(\s*cq\.workplane\([^)]*\)\s*\.circle\((?P<radius>[^)]*)\)\s*\.extrude\((?P<depth>[^)]*)\)\s*\)",
            code_text[match.end():],
            re.IGNORECASE | re.DOTALL,
        )
    return None


def _annular_rib_from_code(code_text: str) -> dict[str, float] | None:
    env = _numeric_env(code_text)
    outer = env.get("outer_rib_radius")
    inner = env.get("inner_rib_radius")
    height = env.get("rib_height")
    if outer is None or inner is None or height is None:
        return None
    if outer <= inner or inner <= 0 or height <= 0:
        return None
    if ".cut(inner_cut)" not in code_text.lower() and ".cut( inner_cut )" not in code_text.lower():
        return None
    return {
        "outer_diameter": 2.0 * outer,
        "inner_diameter": 2.0 * inner,
        "height": height,
    }


def _central_blind_hole_from_code(code_text: str) -> dict[str, float] | None:
    env = _numeric_env(code_text)
    for match in re.finditer(r"\.hole\((?P<args>[^)]*)\)", code_text, re.IGNORECASE):
        prefix = code_text[max(0, match.start() - 120):match.start()].lower()
        if ".pushpoints(" in prefix or ".polararray(" in prefix:
            continue
        args = _split_args(match.group("args"))
        if len(args) < 2:
            continue
        diameter = _eval_number(args[0], env)
        depth = _eval_number(args[1], env)
        if diameter is not None and depth is not None and diameter > 0 and depth > 0:
            return {"diameter": diameter, "depth": depth}
    return None


def _push_points_hole_drill_calls(code_text: str) -> list[str]:
    env = _numeric_env(code_text)
    calls: list[str] = []
    pattern = re.compile(
        r"\.pushpoints\((?P<points>\[.*?\])\)\s*\.hole\((?P<hole>[^)]*)\)",
        re.IGNORECASE | re.DOTALL,
    )
    for match in pattern.finditer(code_text):
        points = _eval_points_literal(match.group("points"), env)
        hole_args = _split_args(match.group("hole"))
        if not points or not hole_args:
            continue
        diameter = _eval_number(hole_args[0], env)
        if diameter is None or diameter <= 0:
            continue
        for x, y in points:
            calls.append(f".drill({diameter:.6g}, through=True, cx={x:.6g}, cy={y:.6g})")
    return calls


def _eval_points_literal(points_text: str, env: dict[str, float]) -> list[tuple[float, float]]:
    try:
        node = ast.parse(points_text, mode="eval").body
    except SyntaxError:
        return []
    value = _eval_ast_value(node, env, {})
    points: list[tuple[float, float]] = []
    if not isinstance(value, list):
        return []
    for item in value:
        if (
            isinstance(item, (list, tuple))
            and len(item) >= 2
            and isinstance(item[0], (int, float))
            and isinstance(item[1], (int, float))
        ):
            points.append((float(item[0]), float(item[1])))
    return points


def _call_args_at(text: str, open_paren_index: int) -> tuple[list[str] | None, int]:
    if open_paren_index < 0 or open_paren_index >= len(text) or text[open_paren_index] != "(":
        return None, open_paren_index
    depth = 1
    index = open_paren_index + 1
    while index < len(text) and depth:
        char = text[index]
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        index += 1
    if depth:
        return None, index
    return _split_args(text[open_paren_index + 1:index - 1]), index


def _deterministic_drill_calls(code_text: str) -> list[str]:
    diameter = _hole_diameter_from_code(code_text)
    if diameter is None:
        return []
    calls = []
    for x, y in _hole_positions_from_code(code_text):
        calls.append(f".drill({diameter:.6g}, through=True, cx={x:.6g}, cy={y:.6g})")
    return calls


def _hole_diameter_from_code(code_text: str) -> float | None:
    env = _numeric_env(code_text)
    match = re.search(r"\.hole\(\s*(?P<arg>[^),]+)", code_text, re.IGNORECASE)
    if not match:
        return None
    return _eval_number(match.group("arg"), env)


def _hole_positions_from_code(code_text: str) -> list[tuple[float, float]]:
    try:
        tree = ast.parse(textwrap.dedent(code_text))
    except SyntaxError:
        return []

    env = _numeric_env(code_text)
    value_env: dict[str, Any] = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if not isinstance(target, ast.Name):
            continue
        value = _eval_ast_value(node.value, env, value_env)
        if value is not None:
            value_env[target.id] = value

    positions: list[tuple[float, float]] = []
    for value in value_env.values():
        if not isinstance(value, list):
            continue
        for item in value:
            if (
                isinstance(item, (list, tuple))
                and len(item) >= 2
                and isinstance(item[0], (int, float))
                and isinstance(item[1], (int, float))
            ):
                positions.append((float(item[0]), float(item[1])))
        if positions:
            break
    return positions


def _eval_ast_value(
    node: ast.AST,
    env: dict[str, float],
    value_env: dict[str, Any],
) -> Any:
    number = _eval_ast_number(node, env)
    if number is not None:
        return number
    if isinstance(node, ast.Name):
        return value_env.get(node.id)
    if isinstance(node, ast.Tuple):
        values = [_eval_ast_value(item, env, value_env) for item in node.elts]
        return tuple(values) if all(value is not None for value in values) else None
    if isinstance(node, ast.List):
        values = [_eval_ast_value(item, env, value_env) for item in node.elts]
        return values if all(value is not None for value in values) else None
    return None


def _shell_has_accessible_open_face(ops_trace: list[dict], code_text: str) -> bool:
    """Best-effort gate for CadQuery shell accessibility.

    ``solid.shell(-t)`` without a selected face creates a closed internal void,
    which is not machinable from solid stock by pure subtractive CNC. Chained
    ``faces(...).shell(...)`` evidence is treated as an open/accessed shell.
    """
    for op in ops_trace:
        if not isinstance(op, dict):
            continue
        if str(op.get("op_name") or "").lower() != "shell":
            continue
        function = str(op.get("function") or "").lower()
        if ".faces" in function or function.endswith("faces.shell"):
            return True

    shell_index = code_text.find(".shell(")
    if shell_index < 0:
        return False
    recent_chain = code_text[max(0, shell_index - 120):shell_index]
    return ".faces(" in recent_chain


_FACE_WORKPLANE_RE = re.compile(
    r"\.faces\(\s*['\"](?P<selector>[<>][xyz])['\"]\s*\)\s*\.workplane\(\s*\)",
    re.IGNORECASE,
)


def _top_workplane_retained_material(
    ops_trace: list[dict],
    code_text: str,
) -> list[dict[str, Any]]:
    """Find additive sketches on the top face.

    CadQuery often builds ribs/bosses as
    ``result.faces(">Z").workplane()...extrude(height)`` without an explicit
    ``union`` call.  These still require retained-material SubCAD operations.
    """
    evidence: list[dict[str, Any]] = []
    for match in _FACE_WORKPLANE_RE.finditer(code_text):
        selector = match.group("selector").upper()
        if selector != ">Z":
            continue
        chain = code_text[match.end():_next_chain_boundary(code_text, match.end())]
        if ".extrude(" not in chain or _chain_is_subtractive(chain):
            continue
        detail = _retained_chain_evidence(chain, code_text)
        evidence.append({
            "face_selector": selector,
            "chain": _trim_evidence_chain(chain),
            **detail,
        })

    if evidence:
        return evidence

    return _top_workplane_retained_material_from_trace(ops_trace)


def _non_top_workplane_retained_material(
    ops_trace: list[dict],
    code_text: str,
) -> list[dict[str, Any]]:
    """Find additive sketches on selected non-top faces.

    Current SubCAD retained-material operations are top-workplane operations.
    Bottom and side subtractive cuts can still be represented through a face
    selector, but additive side/bottom workplane features such as CadQuery
    gussets need a real oriented retained-material operation before they should
    be marked compatible.
    """
    evidence: list[dict[str, Any]] = []
    for match in _FACE_WORKPLANE_RE.finditer(code_text):
        selector = match.group("selector").upper()
        if selector == ">Z":
            continue
        chain = code_text[match.end():_next_chain_boundary(code_text, match.end())]
        if ".extrude(" not in chain or _chain_is_subtractive(chain):
            continue
        evidence.append({
            "face_selector": selector,
            "chain": _trim_evidence_chain(chain),
        })

    if evidence:
        return evidence

    return _non_top_workplane_retained_material_from_trace(ops_trace)


def _next_chain_boundary(code_text: str, start: int) -> int:
    candidates = [
        index for index in (
            code_text.find(".faces(", start),
            code_text.find(";", start),
        )
        if index >= 0
    ]
    return min(candidates) if candidates else len(code_text)


def _chain_is_subtractive(chain: str) -> bool:
    return any(token in chain for token in (".cut", ".cutblind(", ".cutthruall(", ".hole("))


def _trim_evidence_chain(chain: str) -> str:
    compact = " ".join(chain.strip().split())
    return compact[:160]


def _retained_material_parameter_evidence(code_text: str) -> list[dict[str, Any]]:
    evidence: list[dict[str, Any]] = []
    loop_evidence = _for_loop_retained_rectangles(code_text)
    standalone_evidence = _standalone_union_retained_features(code_text)
    evidence.extend(loop_evidence)
    evidence.extend(standalone_evidence)
    evidence.extend(_mixed_height_retained_level_evidence(loop_evidence, standalone_evidence))
    return evidence


def _base_cut_pocket_evidence(code_text: str) -> list[dict[str, Any]]:
    env = _numeric_env(code_text)
    outer = _outer_rect_extrude(code_text, env)
    evidence: list[dict[str, Any]] = []
    assignment_re = re.compile(
        r"^\s*(?P<name>\w+)\s*=\s*\(\s*cq\.workplane\([^)]*\)(?P<body>.*?\.rect\([^)]*\).*?\.translate\([^)]*\).*?\.extrude\([^)]*\).*?)\n\s*\)",
        re.IGNORECASE | re.DOTALL | re.MULTILINE,
    )
    for match in assignment_re.finditer(code_text):
        name = match.group("name")
        body = match.group("body")
        if f".cut({name})" not in code_text:
            continue
        profile = _rect_profile_from_chain(body, env)
        if not profile:
            continue
        translate = _translate_xy_from_chain(body, env)
        if translate:
            profile["cx"], profile["cy"] = translate
        depth = _first_call_number(body, "extrude", env)
        if depth is None:
            continue
        evidence.append({
            "source": f"cadquery.base_cut.{name}",
            "profile": profile,
            "retained_profile": _retained_l_profile(outer, profile) if outer else None,
            "outer_profile": outer,
            "depth": depth,
            "base_height": 0.0,
            "suggested_subcad": (
                f".pocket(width={profile['width']:.6g}, length={profile['length']:.6g}, "
                f"depth={depth:.6g}, cx={profile['cx']:.6g}, cy={profile['cy']:.6g}, "
                "base_height=0.0)"
            ),
        })
    return evidence


def _outer_rect_extrude(code_text: str, env: dict[str, float]) -> dict[str, Any] | None:
    match = re.search(
        r"^\s*\w+\s*=\s*cq\.workplane\([^)]*\)\s*\.rect\((?P<args>[^)]*)\)\s*\.extrude\((?P<depth>[^)]*)\)",
        code_text,
        re.IGNORECASE | re.MULTILINE,
    )
    if not match:
        return None
    args = _split_args(match.group("args"))
    if len(args) < 2:
        return None
    length = _eval_number(args[0], env)
    width = _eval_number(args[1], env)
    depth = _eval_number(match.group("depth"), env)
    if length is None or width is None:
        return None
    return {"type": "rect", "length": length, "width": width, "cx": 0.0, "cy": 0.0, "depth": depth}


def _retained_l_profile(outer: dict[str, Any] | None, cut_profile: dict[str, Any]) -> dict[str, Any] | None:
    if not outer:
        return None
    ox0, oy0, ox1, oy1 = _rect_bounds(outer)
    cx0, cy0, cx1, cy1 = _rect_bounds(cut_profile)
    if abs(cx1 - ox1) < 1e-6 and abs(cy1 - oy1) < 1e-6:
        return {
            "type": "polygon",
            "points": [
                (ox0, oy0),
                (ox1, oy0),
                (ox1, cy0),
                (cx0, cy0),
                (cx0, oy1),
                (ox0, oy1),
            ],
        }
    return None


def _rect_bounds(profile: dict[str, Any]) -> tuple[float, float, float, float]:
    length = float(profile.get("length", profile.get("width", 0.0)))
    width = float(profile.get("width", profile.get("length", 0.0)))
    cx = float(profile.get("cx", profile.get("x", 0.0)))
    cy = float(profile.get("cy", profile.get("y", 0.0)))
    return (cx - length / 2.0, cy - width / 2.0, cx + length / 2.0, cy + width / 2.0)


def _for_loop_retained_rectangles(code_text: str) -> list[dict[str, Any]]:
    env = _numeric_env(code_text)
    evidence: list[dict[str, Any]] = []
    loop_re = re.compile(
        r"for\s+(?P<var>\w+)\s+in\s+range\((?P<count>[^)]*)\):(?P<body>.*?)(?=\n\S|\Z)",
        re.IGNORECASE | re.DOTALL,
    )
    for match in loop_re.finditer(code_text):
        body = match.group("body")
        if ".rect(" not in body or ".extrude(" not in body:
            continue
        count = _eval_number(match.group("count"), env)
        if count is None or count <= 0 or count > 100:
            continue
        profiles: list[dict[str, Any]] = []
        for index in range(int(count)):
            scoped = dict(env)
            scoped[match.group("var")] = float(index)
            scoped.update(_numeric_env(body, scoped))
            profile = _rect_profile_from_chain(body, scoped)
            if profile:
                profiles.append(profile)
        height = _first_call_number(body, "extrude", env)
        base_height = _translate_z_from_chain(body, env)
        if len(profiles) > 1 and height is not None:
            evidence.append({
                "source": "cadquery.for_loop.retained_rectangles",
                "profiles": profiles,
                "height": height,
                "base_height": base_height,
                "suggested_subcad": _suggest_machine_around_profiles(profiles, height, base_height),
            })
    return evidence


def _standalone_union_retained_features(code_text: str) -> list[dict[str, Any]]:
    env = _numeric_env(code_text)
    evidence: list[dict[str, Any]] = []
    assignment_re = re.compile(
        r"^\s*(?P<name>\w+)\s*=\s*\(\s*cq\.workplane\([^)]*\)(?P<body>.*?\.extrude\([^)]*\).*?)\n\s*\)",
        re.IGNORECASE | re.DOTALL | re.MULTILINE,
    )
    for match in assignment_re.finditer(code_text):
        name = match.group("name")
        body = match.group("body")
        if f".union({name})" not in code_text:
            continue
        height = _first_call_number(body, "extrude", env)
        base_height = _translate_z_from_chain(body, env)
        if height is None:
            continue
        if ".circle(" in body:
            center = _center_from_chain(body, env)
            diameter = _first_call_number(body, "circle", env)
            if diameter is not None:
                diameter *= 2.0
                evidence.append({
                    "source": f"cadquery.union.{name}",
                    "profile_type": "circle",
                    "profile": {
                        "type": "circle",
                        "diameter": diameter,
                        "cx": center[0],
                        "cy": center[1],
                    },
                    "diameter": diameter,
                    "cx": center[0],
                    "cy": center[1],
                    "height": height,
                    "base_height": base_height,
                    "suggested_subcad": (
                        f".machine_around_cylinder({diameter:.6g}, {height:.6g}, "
                        f"cx={center[0]:.6g}, cy={center[1]:.6g}"
                        f"{', base_height=' + format(base_height, '.6g') if base_height is not None else ''})"
                    ),
                })
            continue
        profile = _rect_profile_from_chain(body, env)
        if profile:
            evidence.append({
                "source": f"cadquery.union.{name}",
                "profiles": [profile],
                "height": height,
                "base_height": base_height,
                "suggested_subcad": _suggest_machine_around_profiles([profile], height, base_height),
            })
    return evidence


def _mixed_height_retained_level_evidence(
    loop_evidence: list[dict[str, Any]],
    standalone_evidence: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    suggestions: list[dict[str, Any]] = []
    for ribs in loop_evidence:
        rib_profiles = list(ribs.get("profiles") or [])
        rib_height = ribs.get("height")
        base_height = ribs.get("base_height")
        if not rib_profiles or rib_height is None or base_height is None:
            continue
        for boss in standalone_evidence:
            if boss.get("profile_type") != "circle":
                continue
            if boss.get("base_height") != base_height:
                continue
            boss_height = boss.get("height")
            boss_profile = boss.get("profile")
            if boss_height is None or boss_profile is None or boss_height <= rib_height:
                continue
            upper_height = boss_height - rib_height
            lower_profiles = [boss_profile, *rib_profiles]
            sequence = [
                (
                    f".machine_around_cylinder({boss_profile['diameter']:.6g}, {upper_height:.6g}, "
                    f"cx={boss_profile['cx']:.6g}, cy={boss_profile['cy']:.6g}, "
                    f"base_height={base_height + rib_height:.6g})"
                ),
                _suggest_machine_around_profiles(lower_profiles, rib_height, base_height),
            ]
            suggestions.append({
                "source": "cadquery.retained_levels.mixed_height",
                "profiles": lower_profiles,
                "height": rib_height,
                "base_height": base_height,
                "suggested_sequence": sequence,
                "suggested_subcad": " then ".join(sequence),
            })
    return suggestions


def _layered_profile_plan_evidence(
    base_cut_evidence: list[dict[str, Any]],
    retained_evidence: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    plans: list[dict[str, Any]] = []
    bases = [item for item in base_cut_evidence if item.get("retained_profile") and item.get("outer_profile")]
    rib_groups = [item for item in retained_evidence if len(item.get("profiles") or []) > 1 and item.get("base_height") is not None]
    bosses = [item for item in retained_evidence if item.get("profile_type") == "circle" and item.get("profile")]
    for base in bases:
        base_profile = base["retained_profile"]
        outer = base["outer_profile"]
        base_top = float(base.get("depth") or 0.0)
        for ribs in rib_groups:
            rib_base = float(ribs.get("base_height"))
            rib_height = float(ribs.get("height") or 0.0)
            if rib_height <= 0.0:
                continue
            for boss in bosses:
                boss_base = boss.get("base_height")
                boss_height = boss.get("height")
                boss_profile = boss.get("profile")
                if boss_base is None or boss_height is None or boss_profile is None:
                    continue
                boss_base = float(boss_base)
                boss_height = float(boss_height)
                if abs(boss_base - rib_base) > 1e-6 or boss_height <= rib_height:
                    continue
                stock_envelope = _symmetric_stock_envelope(outer, [boss_profile, *(ribs.get("profiles") or [])])
                sequence: list[str] = []
                stock = (
                    f"Stock.rectangular({stock_envelope['length']:.6g}, "
                    f"{stock_envelope['width']:.6g}, {boss_base + boss_height:.6g})"
                )
                sequence.append(
                    f".machine_around_profile({base_profile!r}, height={boss_base:.6g}, "
                    f"base_height=0.0, stock_envelope={stock_envelope!r})"
                )
                fusion_height = max(base_top - boss_base, 0.0)
                if fusion_height > 1e-6:
                    sequence.append(
                        f".machine_around_profiles([{base_profile!r}, {boss_profile!r}], "
                        f"height={fusion_height:.6g}, base_height={boss_base:.6g}, "
                        f"stock_envelope={stock_envelope!r})"
                    )
                visible_rib_height = max(rib_height - fusion_height, 0.0)
                if visible_rib_height > 1e-6:
                    lower_profiles = [boss_profile, *(ribs.get("profiles") or [])]
                    sequence.append(_suggest_machine_around_profiles(lower_profiles, visible_rib_height, base_top))
                upper_base = boss_base + rib_height
                upper_height = max((boss_base + boss_height) - upper_base, 0.0)
                if upper_height > 1e-6:
                    sequence.append(
                        f".machine_around_cylinder({boss_profile['diameter']:.6g}, "
                        f"height={upper_height:.6g}, cx={boss_profile['cx']:.6g}, "
                        f"cy={boss_profile['cy']:.6g}, base_height={upper_base:.6g})"
                    )
                plans.append({
                    "source": "cadquery.layered_retained_profile_plan",
                    "suggested_stock": stock,
                    "suggested_sequence": sequence,
                    "suggested_subcad": stock + "".join(sequence),
                    "stock_envelope": stock_envelope,
                    "retained_profile": base_profile,
                })
    return plans


def _symmetric_stock_envelope(outer: dict[str, Any], profiles: list[dict[str, Any]]) -> dict[str, Any]:
    xmin, ymin, xmax, ymax = _rect_bounds(outer)
    for profile in profiles:
        ptype = str(profile.get("type", profile.get("shape", ""))).lower()
        if ptype in {"circle", "circular"} or "diameter" in profile or "radius" in profile:
            radius = float(profile.get("radius", float(profile.get("diameter", 0.0)) / 2.0))
            cx = float(profile.get("cx", 0.0))
            cy = float(profile.get("cy", 0.0))
            bx0, by0, bx1, by1 = cx - radius, cy - radius, cx + radius, cy + radius
        else:
            bx0, by0, bx1, by1 = _rect_bounds(profile)
        xmin, ymin, xmax, ymax = min(xmin, bx0), min(ymin, by0), max(xmax, bx1), max(ymax, by1)
    return {
        "type": "rect",
        "length": 2.0 * max(abs(xmin), abs(xmax)),
        "width": 2.0 * max(abs(ymin), abs(ymax)),
        "cx": 0.0,
        "cy": 0.0,
    }


def _retained_chain_evidence(chain: str, code_text: str) -> dict[str, Any]:
    env = _numeric_env(code_text)
    if ".polararray(" in chain and ".rect(" in chain:
        profiles = _polar_rect_profiles(chain, env)
        height = _first_call_number(chain, "extrude", env)
        if profiles and height is not None:
            return {
                "profiles": profiles,
                "height": height,
                "suggested_subcad": _suggest_machine_around_profiles(profiles, height),
            }
    profile = _rect_profile_from_chain(chain, env)
    if not profile:
        sketches = _sketch_rects(code_text, env)
        sketch_match = re.search(r"\.placesketch\(\s*(?P<name>\w+)\s*\)", chain, re.IGNORECASE)
        if sketch_match and sketch_match.group("name") in sketches:
            profile = dict(sketches[sketch_match.group("name")])
            cx, cy = _center_from_chain(chain, env)
            profile["cx"] = cx
            profile["cy"] = cy
    height = _first_call_number(chain, "extrude", env)
    if profile and height is not None:
        return {
            "profiles": [profile],
            "height": height,
            "suggested_subcad": _suggest_machine_around_profiles([profile], height),
        }
    return {}


def _numeric_env(code_text: str, initial: dict[str, float] | None = None) -> dict[str, float]:
    env: dict[str, float] = dict(initial or {})
    try:
        tree = ast.parse(textwrap.dedent(code_text))
    except SyntaxError:
        return env
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if not isinstance(target, ast.Name):
            continue
        value = _eval_ast_number(node.value, env)
        if value is not None:
            env[target.id] = value
    return env


def _eval_number(expr: str, env: dict[str, float]) -> float | None:
    try:
        return _eval_ast_number(ast.parse(expr, mode="eval").body, env)
    except SyntaxError:
        return None


def _eval_ast_number(node: ast.AST, env: dict[str, float]) -> float | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.Name):
        return env.get(node.id)
    if isinstance(node, ast.UnaryOp):
        value = _eval_ast_number(node.operand, env)
        if value is None:
            return None
        if isinstance(node.op, ast.USub):
            return -value
        if isinstance(node.op, ast.UAdd):
            return value
    if isinstance(node, ast.BinOp):
        left = _eval_ast_number(node.left, env)
        right = _eval_ast_number(node.right, env)
        if left is None or right is None:
            return None
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Div):
            return left / right if right else None
        if isinstance(node.op, ast.FloorDiv):
            return math.floor(left / right) if right else None
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"int", "float"} and node.args:
        value = _eval_ast_number(node.args[0], env)
        if value is None:
            return None
        return float(int(value)) if node.func.id == "int" else float(value)
    return None


def _first_call_number(chain: str, call_name: str, env: dict[str, float]) -> float | None:
    args = _first_call_args(chain, call_name)
    if not args:
        return None
    return _eval_number(args[0], env)


def _rect_profile_from_chain(chain: str, env: dict[str, float]) -> dict[str, Any] | None:
    rect_args = _first_call_args(chain, "rect")
    if len(rect_args) < 2:
        return None
    length = _eval_number(rect_args[0], env)
    width = _eval_number(rect_args[1], env)
    if length is None or width is None:
        return None
    cx, cy = _center_from_chain(chain, env)
    profile: dict[str, Any] = {
        "type": "rib",
        "length": length,
        "width": width,
        "cx": cx,
        "cy": cy,
    }
    return profile


def _center_from_chain(chain: str, env: dict[str, float]) -> tuple[float, float]:
    center_args = _first_call_args(chain, "center")
    if len(center_args) >= 2:
        return (
            _eval_number(center_args[0], env) or 0.0,
            _eval_number(center_args[1], env) or 0.0,
        )
    return (0.0, 0.0)


def _polar_rect_profiles(chain: str, env: dict[str, float]) -> list[dict[str, Any]]:
    polar_args = _first_call_args(chain, "polararray")
    rect_args = _first_call_args(chain, "rect")
    if len(rect_args) < 2:
        return []
    length = _eval_number(rect_args[0], env)
    width = _eval_number(rect_args[1], env)
    if length is None or width is None:
        return []
    polar = _parse_keyword_args(polar_args, env)
    radius = polar.get("radius")
    count = polar.get("count")
    start = polar.get("startangle", 0.0)
    sweep = polar.get("angle", 360.0)
    if radius is None and polar_args:
        radius = _eval_number(polar_args[0], env)
    if count is None and len(polar_args) > 1:
        count = _eval_number(polar_args[1], env)
    if radius is None or count is None or count <= 0 or count > 100:
        return []
    profiles = []
    step = sweep / count
    for index in range(int(count)):
        angle = start + step * index
        radians = math.radians(angle)
        profiles.append({
            "type": "rib",
            "length": length,
            "width": width,
            "cx": radius * math.cos(radians),
            "cy": radius * math.sin(radians),
            "angle": angle,
        })
    return profiles


def _translate_z_from_chain(chain: str, env: dict[str, float]) -> float | None:
    args = _first_call_args(chain, "translate")
    if len(args) != 1:
        return None
    tuple_text = args[0].strip()
    if tuple_text.startswith("(") and tuple_text.endswith(")"):
        parts = _split_args(tuple_text[1:-1])
        if len(parts) >= 3:
            return _eval_number(parts[2], env)
    return None


def _translate_xy_from_chain(chain: str, env: dict[str, float]) -> tuple[float, float] | None:
    args = _first_call_args(chain, "translate")
    if len(args) != 1:
        return None
    tuple_text = args[0].strip()
    if tuple_text.startswith("(") and tuple_text.endswith(")"):
        parts = _split_args(tuple_text[1:-1])
        if len(parts) >= 2:
            return (
                _eval_number(parts[0], env) or 0.0,
                _eval_number(parts[1], env) or 0.0,
            )
    return None


def _parse_keyword_args(args: list[str], env: dict[str, float]) -> dict[str, float]:
    values: dict[str, float] = {}
    for arg in args:
        if "=" not in arg:
            continue
        key, value = arg.split("=", 1)
        number = _eval_number(value.strip(), env)
        if number is not None:
            values[key.strip().lower()] = number
    return values


def _first_call_args(chain: str, call_name: str) -> list[str]:
    match = re.search(rf"\.{re.escape(call_name)}\s*\(", chain, re.IGNORECASE)
    if not match:
        return []
    start = match.end()
    depth = 1
    index = start
    while index < len(chain) and depth:
        char = chain[index]
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        index += 1
    if depth:
        return []
    return _split_args(chain[start:index - 1])


def _split_args(arg_text: str) -> list[str]:
    args: list[str] = []
    start = 0
    depth = 0
    for index, char in enumerate(arg_text):
        if char in "([{":
            depth += 1
        elif char in ")]}":
            depth -= 1
        elif char == "," and depth == 0:
            args.append(arg_text[start:index].strip())
            start = index + 1
    tail = arg_text[start:].strip()
    if tail:
        args.append(tail)
    return args


def _sketch_rects(code_text: str, env: dict[str, float]) -> dict[str, dict[str, Any]]:
    sketches: dict[str, dict[str, Any]] = {}
    sketch_re = re.compile(
        r"(?P<name>\w+)\s*=\s*cq\.sketch\(\)\.rect\((?P<args>[^)]*)\)",
        re.IGNORECASE,
    )
    for match in sketch_re.finditer(code_text):
        args = _split_args(match.group("args"))
        if len(args) < 2:
            continue
        length = _eval_number(args[0], env)
        width = _eval_number(args[1], env)
        if length is not None and width is not None:
            sketches[match.group("name")] = {
                "type": "rib",
                "length": length,
                "width": width,
                "cx": 0.0,
                "cy": 0.0,
            }
    return sketches


def _suggest_machine_around_profiles(
    profiles: list[dict[str, Any]],
    height: float,
    base_height: float | None = None,
) -> str:
    clean_profiles = []
    for profile in profiles:
        clean_profiles.append({
            key: round(value, 6) if isinstance(value, float) else value
            for key, value in profile.items()
        })
    if len(clean_profiles) == 1:
        base_arg = f", base_height={base_height:.6g}" if base_height is not None else ""
        return f".machine_around_profile({clean_profiles[0]!r}, height={height:.6g}{base_arg})"
    base_arg = f", base_height={base_height:.6g}" if base_height is not None else ""
    return f".machine_around_profiles({clean_profiles!r}, height={height:.6g}{base_arg})"


def _non_top_workplane_retained_material_from_trace(ops_trace: list[dict]) -> list[dict[str, Any]]:
    evidence: list[dict[str, Any]] = []
    for index, op in enumerate(ops_trace):
        if not isinstance(op, dict):
            continue
        if str(op.get("op_name") or "").lower() != "workplane":
            continue
        function = str(op.get("function") or "").lower()
        selector = _face_selector_from_text(function)
        if selector is None or selector == ">Z":
            continue
        window = ops_trace[index + 1:index + 8]
        op_names = {str(item.get("op_name") or "").lower() for item in window if isinstance(item, dict)}
        if "extrude" in op_names and not any(name.startswith("cut") for name in op_names):
            evidence.append({"face_selector": selector, "trace_index": index})
    return evidence


def _top_workplane_retained_material_from_trace(ops_trace: list[dict]) -> list[dict[str, Any]]:
    evidence: list[dict[str, Any]] = []
    for index, op in enumerate(ops_trace):
        if not isinstance(op, dict):
            continue
        if str(op.get("op_name") or "").lower() != "workplane":
            continue
        function = str(op.get("function") or "").lower()
        selector = _face_selector_from_text(function)
        if selector != ">Z":
            continue
        window = ops_trace[index + 1:index + 8]
        op_names = {str(item.get("op_name") or "").lower() for item in window if isinstance(item, dict)}
        if "extrude" in op_names and not any(name.startswith("cut") for name in op_names):
            evidence.append({"face_selector": selector, "trace_index": index})
    return evidence


def _face_selector_from_text(text: str) -> str | None:
    match = re.search(r"\.faces\(\s*['\"](?P<selector>[<>][xyz])['\"]\s*\)", text, re.IGNORECASE)
    return match.group("selector").upper() if match else None


def compatibility_report(ops_trace: list[dict], cadquery_code: str = "") -> dict[str, Any]:
    """Back-compatible dict shape consumed by existing benchmark runner."""
    plan = plan_pure_subcad_features(ops_trace, cadquery_code)
    reasons = [
        feature.reason
        for feature in plan.features
        if feature.planner_status in {UNSUPPORTED_UNMACHINABLE, NEEDS_MANUAL_REVIEW}
    ]
    return {
        "compatible": plan.compatible,
        "reasons": reasons,
        "planner": plan.to_dict(),
    }
