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
    for evidence in _base_cut_pocket_evidence(code_text):
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

    for evidence in _retained_material_parameter_evidence(code_text):
        operation = "machine_around_profiles" if len(evidence.get("profiles") or []) > 1 else "machine_around_profile"
        if evidence.get("profile_type") == "circle":
            operation = "machine_around_cylinder"
        feature_source = evidence.get("source", "cadquery.retained_material.evidence")
        feature_evidence = {key: value for key, value in evidence.items() if key != "source"}
        add(feature_source,
            "retained_material", PLANNED_EXACT, operation,
            "source-derived retained-material dimensions and positions are available",
            **feature_evidence)

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
            "depth": depth,
            "base_height": 0.0,
            "suggested_subcad": (
                f".pocket(width={profile['width']:.6g}, length={profile['length']:.6g}, "
                f"depth={depth:.6g}, cx={profile['cx']:.6g}, cy={profile['cy']:.6g}, "
                "base_height=0.0)"
            ),
        })
    return evidence


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
