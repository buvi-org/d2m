"""SubCAD validation -- pre-operation feasibility and DFM checks."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class ValidationIssue:
    """Structured validation issue while preserving a string message."""

    severity: str
    code: str
    message: str
    operation_index: Optional[int] = None
    operation: str = ""
    context: dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        return self.message


@dataclass
class ValidationReport:
    """Structured validation result returned by validate_all(structured=True)."""

    issues: list[ValidationIssue] = field(default_factory=list)

    @property
    def warnings(self) -> list[str]:
        return [issue.message for issue in self.issues if issue.severity == "warning"]

    @property
    def errors(self) -> list[str]:
        return [issue.message for issue in self.issues if issue.severity == "error"]

    @property
    def messages(self) -> list[str]:
        return [issue.message for issue in self.issues]

    @property
    def ok(self) -> bool:
        return not self.errors

    def append(self, issue: ValidationIssue) -> None:
        self.issues.append(issue)

    def extend(self, issues: list[ValidationIssue]) -> None:
        self.issues.extend(issues)

    def __iter__(self):
        return iter(self.messages)

    def __len__(self) -> int:
        return len(self.issues)

    def __getitem__(self, index):
        return self.messages[index]


def _issue(severity: str, code: str, message: str,
           op_index: Optional[int] = None, op: Optional[dict] = None,
           **context) -> ValidationIssue:
    return ValidationIssue(
        severity=severity,
        code=code,
        message=message,
        operation_index=op_index,
        operation=(op or {}).get("operation", ""),
        context={k: v for k, v in context.items() if v is not None},
    )


def _as_float(value, default: Optional[float] = None) -> Optional[float]:
    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _op_name(op: dict) -> str:
    return str(op.get("operation", "")).lower()


def _position_key(op: dict):
    pos = op.get("position")
    if not isinstance(pos, (list, tuple)) or len(pos) < 2:
        return None
    x = _as_float(pos[0])
    y = _as_float(pos[1])
    if x is None or y is None:
        return None
    face = op.get("face_selector", ">Z")
    setup = op.get("setup", "")
    return (round(x, 3), round(y, 3), face, setup)


def _depth_mm(op: dict) -> float:
    dims = op.get("dimensions") if isinstance(op.get("dimensions"), dict) else {}
    for key in ("depth_mm", "depth", "counterbore_depth_mm"):
        depth = _as_float(op.get(key, dims.get(key)))
        if depth is not None:
            return abs(depth)
    return 0.0


def _tool_diameter_mm(op: dict) -> Optional[float]:
    for key in ("tool_diameter_mm", "tool_diameter", "diameter_mm"):
        value = _as_float(op.get(key))
        if value is not None:
            return value
    return None


def _toolpath_records(toolpath) -> Optional[list]:
    if isinstance(toolpath, dict):
        if isinstance(toolpath.get("moves"), list):
            return toolpath["moves"]
        if isinstance(toolpath.get("positions"), list):
            return toolpath["positions"]
        return [toolpath]
    if isinstance(toolpath, list):
        return toolpath
    return None


def _toolpath_xyz(record) -> Optional[tuple[float, float, float]]:
    if isinstance(record, dict):
        if all(k in record for k in ("x", "y", "z")):
            values = (record.get("x"), record.get("y"), record.get("z"))
        else:
            values = record.get("position")
            if values is None:
                return None
    elif isinstance(record, (list, tuple)) and len(record) >= 3:
        values = record[:3]
    else:
        return None

    try:
        return (float(values[0]), float(values[1]), float(values[2]))
    except (TypeError, ValueError, IndexError):
        return None


def _toolpath_move_type(record) -> str:
    if not isinstance(record, dict):
        return ""
    return str(record.get("type", record.get("move_type", ""))).lower()


def _is_cutting_operation(op: dict) -> bool:
    op_type = _op_name(op)
    non_cutting = {"", "inspect", "inspection", "setup", "fixture", "probe"}
    return op_type not in non_cutting


def _stock_limits(stock_dims: dict) -> dict[str, Optional[float]]:
    return {
        "length": _as_float(stock_dims.get("length", stock_dims.get("x"))),
        "width": _as_float(stock_dims.get("width", stock_dims.get("y"))),
        "height": _as_float(stock_dims.get("height", stock_dims.get("z"))),
    }


def _xy_inside_stock(x: float, y: float, length: Optional[float], width: Optional[float],
                     margin: float) -> bool:
    x_ok = True
    y_ok = True
    if length is not None:
        x_ok = (-margin <= x <= length + margin) or (
            -length / 2.0 - margin <= x <= length / 2.0 + margin
        )
    if width is not None:
        y_ok = (-margin <= y <= width + margin) or (
            -width / 2.0 - margin <= y <= width / 2.0 + margin
        )
    return x_ok and y_ok


def _tool_flute_length_mm(op: dict, tool_specs: Optional[list] = None) -> Optional[float]:
    for key in (
        "flute_length_mm",
        "tool_flute_length_mm",
        "tool_flute_length",
        "flute_length",
    ):
        value = _as_float(op.get(key))
        if value is not None:
            return value

    if not tool_specs:
        return None

    op_type = op.get("tool_type")
    op_dia = _tool_diameter_mm(op)
    for tool in tool_specs:
        if isinstance(tool, dict):
            tool_type = tool.get("tool_type")
            tool_dia = _as_float(tool.get("tool_diameter_mm", tool.get("diameter")))
            flute = _as_float(tool.get("flute_length_mm", tool.get("flute_length")))
        else:
            tool_type = getattr(tool, "tool_type", None)
            tool_dia = _as_float(getattr(tool, "diameter", None))
            flute = _as_float(getattr(tool, "flute_length", None))
        if flute is None:
            continue
        type_matches = not op_type or not tool_type or op_type == tool_type
        dia_matches = op_dia is None or tool_dia is None or abs(op_dia - tool_dia) < 0.001
        if type_matches and dia_matches:
            return flute
    return None


def check_wall_thickness(shape, operation, min_wall_mm: float = 1.0) -> list[str]:
    """Check if an operation would leave walls thinner than min_wall_mm."""
    return []  # placeholder, returns empty for now


def check_tool_reach(operation, stock_dims: dict, tool) -> list[str]:
    """Check if the tool can physically reach the operation position."""
    warnings = []
    # Check if drill/pocket depth exceeds tool flute_length
    if isinstance(tool, dict):
        flute = _as_float(tool.get("flute_length_mm", tool.get("flute_length")), 50.0)
        reach = _as_float(tool.get("reach_mm", tool.get("tool_reach_mm")))
    else:
        flute = _as_float(getattr(tool, 'flute_length', 50.0), 50.0)
        reach = _as_float(getattr(tool, 'reach', None))
    if isinstance(operation, dict):
        depth = _depth_mm(operation)
        reach = _as_float(operation.get("tool_reach_mm", operation.get("reach_mm")), reach)
    else:
        depth = _as_float(getattr(operation, 'depth', 0.0), 0.0)
    if depth > flute:
        warnings.append(f"Depth ({depth}mm) exceeds tool flute length ({flute}mm).")
    if reach is not None and depth > reach:
        warnings.append(f"Depth ({depth}mm) exceeds tool reach ({reach}mm).")
    return warnings


def check_operation_order(operations: list[dict]) -> list[str]:
    """Validate operation ordering (face_mill first, chamfer last, etc.)."""
    return [issue.message for issue in _check_operation_order(operations)]


def _check_tool_reach_and_geometry(
    operations: list[dict],
    stock_dims: dict,
    tool_specs: Optional[list] = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    stock_height = _as_float(stock_dims.get("height") or stock_dims.get("z"))

    for i, op in enumerate(operations):
        op_type = _op_name(op)
        depth = _depth_mm(op)
        tool_dia = _tool_diameter_mm(op)
        flute = _tool_flute_length_mm(op, tool_specs)

        if flute is not None and depth > flute:
            issues.append(_issue(
                "warning", "tool_flute_length",
                f"{op_type or 'operation'} at position {i} depth ({depth:g}mm) "
                f"exceeds tool flute length ({flute:g}mm).",
                i, op, depth_mm=depth, flute_length_mm=flute,
            ))

        reach = _as_float(op.get("tool_reach_mm", op.get("reach_mm")))
        if reach is not None and depth > reach:
            issues.append(_issue(
                "warning", "tool_reach",
                f"{op_type or 'operation'} at position {i} depth ({depth:g}mm) "
                f"exceeds tool reach ({reach:g}mm).",
                i, op, depth_mm=depth, tool_reach_mm=reach,
            ))

        if op.get("through") and stock_height is not None and depth > stock_height:
            issues.append(_issue(
                "warning", "through_depth",
                f"{op_type or 'operation'} at position {i} depth ({depth:g}mm) "
                f"exceeds stock height ({stock_height:g}mm); verify through-cut clearance.",
                i, op, depth_mm=depth, stock_height_mm=stock_height,
            ))

        if tool_dia is None:
            continue

        slot_width = _as_float(op.get("slot_width_mm"))
        if slot_width is not None and tool_dia > slot_width:
            issues.append(_issue(
                "warning", "tool_vs_slot_width",
                f"{op_type or 'operation'} at position {i} uses a {tool_dia:g}mm tool "
                f"for a {slot_width:g}mm slot.",
                i, op, tool_diameter_mm=tool_dia, slot_width_mm=slot_width,
            ))

        dims = op.get("dimensions") if isinstance(op.get("dimensions"), dict) else {}
        pocket_width = _as_float(dims.get("width", op.get("pocket_width_mm")))
        pocket_length = _as_float(dims.get("length", op.get("pocket_length_mm")))
        if op_type in ("pocket", "rough_pocket", "finish_pocket") and pocket_width is not None:
            limiting_width = min(v for v in (pocket_width, pocket_length) if v is not None)
            if tool_dia > limiting_width:
                issues.append(_issue(
                    "warning", "tool_vs_pocket_width",
                    f"{op_type} at position {i} uses a {tool_dia:g}mm tool "
                    f"for a {limiting_width:g}mm pocket opening.",
                    i, op, tool_diameter_mm=tool_dia, pocket_width_mm=limiting_width,
                ))

        corner_radius = _as_float(op.get("corner_radius_mm"))
        if corner_radius is not None and corner_radius > 0 and tool_dia / 2.0 > corner_radius:
            if not op.get("has_finish_pass"):
                issues.append(_issue(
                    "warning", "tool_vs_internal_corner_radius",
                    f"{op_type or 'operation'} at position {i} has internal corner "
                    f"radius {corner_radius:g}mm smaller than tool radius {tool_dia / 2.0:g}mm.",
                    i, op, tool_radius_mm=tool_dia / 2.0, corner_radius_mm=corner_radius,
                ))

        pocket_dia = _as_float(
            op.get("pocket_diameter_mm",
                   op.get("counterbore_diameter_mm", op.get("spot_face_diameter_mm")))
        )
        if pocket_dia is not None and op_type in (
            "circular_pocket", "counterbore", "spot_face", "bore"
        ) and tool_dia >= pocket_dia:
            issues.append(_issue(
                "warning", "tool_vs_pocket_diameter",
                f"{op_type} at position {i} uses a {tool_dia:g}mm tool "
                f"for a {pocket_dia:g}mm circular pocket.",
                i, op, tool_diameter_mm=tool_dia, pocket_diameter_mm=pocket_dia,
            ))

        hole_dia = _as_float(op.get("hole_diameter_mm", op.get("thread_diameter_mm")))
        if hole_dia is not None and op_type in ("bore", "thread_mill") and tool_dia >= hole_dia:
            issues.append(_issue(
                "warning", "tool_vs_hole_diameter",
                f"{op_type} at position {i} uses a {tool_dia:g}mm tool "
                f"for a {hole_dia:g}mm hole.",
                i, op, tool_diameter_mm=tool_dia, hole_diameter_mm=hole_dia,
            ))

    return issues


def _check_toolpaths(operations: list[dict], stock_dims: dict) -> list[ValidationIssue]:
    """Validate authored toolpath completeness and approximate stock fit."""
    issues: list[ValidationIssue] = []
    limits = _stock_limits(stock_dims)
    margin = _as_float(stock_dims.get("toolpath_margin_mm"), 0.01) or 0.01

    for i, op in enumerate(operations):
        if "toolpath" not in op:
            continue

        op_type = _op_name(op) or "operation"
        records = _toolpath_records(op.get("toolpath"))
        records = records if records is not None else []
        points = [p for p in (_toolpath_xyz(record) for record in records) if p is not None]

        if _is_cutting_operation(op) and not records:
            issues.append(_issue(
                "warning", "empty_toolpath",
                f"{op_type} at position {i} has an empty authored toolpath.",
                i, op,
            ))
            continue

        if not points:
            continue

        toolpath = op.get("toolpath")
        safe_z = None
        if isinstance(toolpath, dict):
            safe_z = _as_float(toolpath.get("safe_z"))
        safe_z = _as_float(op.get("safe_z_mm", op.get("safe_z")), safe_z)
        if safe_z is None:
            positive_z = [z for _, _, z in points if z > 0]
            safe_z = max(positive_z) if positive_z else 0.0

        final_z = points[-1][2]
        has_retract = any(_toolpath_move_type(record) == "retract" for record in records)
        if _is_cutting_operation(op) and final_z < safe_z - 0.01 and not has_retract:
            issues.append(_issue(
                "warning", "missing_retract_safe_z",
                f"{op_type} at position {i} toolpath does not retract to safe Z "
                f"({safe_z:g}mm).",
                i, op, final_z_mm=final_z, safe_z_mm=safe_z,
            ))

        depth = _depth_mm(op)
        cutting_z = [z for _, _, z in points if z <= 0.0]
        if depth > 0 and cutting_z:
            min_z = min(cutting_z)
            required_z = -depth
            if min_z > required_z + 0.01:
                issues.append(_issue(
                    "warning", "toolpath_above_requested_depth",
                    f"{op_type} at position {i} toolpath reaches z={min_z:g}mm, "
                    f"above requested depth z={required_z:g}mm.",
                    i, op, reached_z_mm=min_z, requested_depth_mm=depth,
                ))

        x_bad = []
        y_bad = []
        z_bad = []
        for x, y, z in points:
            if not _xy_inside_stock(x, y, limits["length"], limits["width"], margin):
                x_bad.append(x)
                y_bad.append(y)
            if limits["height"] is not None and z < -limits["height"] - margin:
                z_bad.append(z)
        if x_bad or z_bad:
            context = {
                "bounds": {
                    "min": [min(x for x, _, _ in points),
                            min(y for _, y, _ in points),
                            min(z for _, _, z in points)],
                    "max": [max(x for x, _, _ in points),
                            max(y for _, y, _ in points),
                            max(z for _, _, z in points)],
                },
                "stock_dimensions": limits,
            }
            issues.append(_issue(
                "warning", "toolpath_stock_bounds",
                f"{op_type} at position {i} has toolpath points outside approximate "
                "stock bounds.",
                i, op, **context,
            ))

    return issues


def _check_operation_order(operations: list[dict]) -> list[ValidationIssue]:
    """Validate operation ordering with structured issue output."""
    issues: list[ValidationIssue] = []
    op_names = [op.get("operation", "") for op in operations]

    # Face mill should be first
    face_mill_order_issue_indices = set()
    if "face_mill" in op_names and op_names[0] != "face_mill":
        first_face = op_names.index("face_mill")
        face_mill_order_issue_indices.add(first_face)
        issues.append(_issue(
            "warning", "face_mill_not_first",
            "Face mill should be the first operation for proper datum.",
            first_face, operations[first_face],
        ))

    first_cut_by_face: dict[tuple[str, str], int] = {}
    first_face_mill_by_face: dict[tuple[str, str], int] = {}
    for i, op in enumerate(operations):
        key = (str(op.get("setup", "")), str(op.get("face_selector", ">Z")))
        if _op_name(op) == "face_mill":
            first_face_mill_by_face.setdefault(key, i)
        elif _op_name(op) not in ("spot_drill",):
            first_cut_by_face.setdefault(key, i)
    for key, cut_i in first_cut_by_face.items():
        face_i = first_face_mill_by_face.get(key)
        if face_i is not None and face_i > cut_i and face_i not in face_mill_order_issue_indices:
            issues.append(_issue(
                "warning", "face_mill_after_cut",
                f"Face mill for setup/face {key} occurs after another cutting operation; "
                "establish the datum before feature machining.",
                face_i, operations[face_i], setup=key[0], face_selector=key[1],
            ))

    # Tap after drill
    drilled_keys: set = set()
    any_drill_seen = False
    for i, name in enumerate(op_names):
        op = operations[i]
        op_type = _op_name(op)
        if op_type in ("drill", "peck_drill"):
            any_drill_seen = True
            key = _position_key(op)
            if key is not None:
                drilled_keys.add(key)
            continue

        if op_type in ("tap", "ream", "bore", "thread_mill"):
            key = _position_key(op)
            has_preceding_drill = key in drilled_keys if key is not None else any_drill_seen
            if not has_preceding_drill:
                issues.append(_issue(
                    "warning", f"{op_type}_before_drill",
                    f"{op_type} at position {i} has no preceding drill operation.",
                    i, op,
                ))

    return issues


def _check_setup_accessibility(process_plan_dict: dict) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    operations = process_plan_dict.get("operations", [])
    fixture = process_plan_dict.get("fixture")
    setups = process_plan_dict.get("setups") or {}

    if fixture and not setups:
        issues.append(_issue(
            "warning", "fixture_without_setups",
            "Fixture metadata exists but no setups are defined.",
        ))

    setup_faces: dict[str, str] = {}
    for name, setup in setups.items():
        face = setup.get("face_selector") if isinstance(setup, dict) else None
        setup_faces[name] = face or ""
        if not face:
            issues.append(_issue(
                "warning", "setup_missing_face",
                f"Setup '{name}' is missing a face selector.",
                setup=name,
            ))
        if isinstance(setup, dict) and not setup.get("work_offset"):
            issues.append(_issue(
                "warning", "setup_missing_work_offset",
                f"Setup '{name}' is missing a work offset.",
                setup=name,
            ))
        if face and face not in {">Z", "<Z", ">X", "<X", ">Y", "<Y"}:
            issues.append(_issue(
                "warning", "setup_unsupported_face",
                f"Setup '{name}' uses unsupported face selector '{face}'.",
                setup=name, face_selector=face,
            ))

    referenced_faces = set()
    for i, op in enumerate(operations):
        setup_name = op.get("setup")
        face = op.get("face_selector")
        if fixture and setups and not setup_name:
            issues.append(_issue(
                "warning", "operation_missing_setup",
                f"{_op_name(op) or 'operation'} at position {i} has fixture/setup "
                "metadata available but no setup assignment.",
                i, op,
            ))
        if setup_name and setup_name not in setups:
            issues.append(_issue(
                "warning", "operation_unknown_setup",
                f"{_op_name(op) or 'operation'} at position {i} references unknown setup "
                f"'{setup_name}'.",
                i, op, setup=setup_name,
            ))
        if setup_name in setup_faces and face and setup_faces[setup_name] and face != setup_faces[setup_name]:
            issues.append(_issue(
                "warning", "setup_face_mismatch",
                f"{_op_name(op) or 'operation'} at position {i} uses face '{face}' "
                f"but setup '{setup_name}' is defined for '{setup_faces[setup_name]}'.",
                i, op, setup=setup_name, op_face=face, setup_face=setup_faces[setup_name],
            ))
        if face and face != ">Z":
            referenced_faces.add(face)
        if face and face not in {">Z", "<Z", ">X", "<X", ">Y", "<Y"}:
            issues.append(_issue(
                "warning", "operation_unsupported_face",
                f"{_op_name(op) or 'operation'} at position {i} uses unsupported "
                f"face selector '{face}'.",
                i, op, face_selector=face,
            ))

    if referenced_faces and not setups:
        issues.append(_issue(
            "warning", "multi_face_without_setups",
            "Operations reference non-top faces but no setup metadata is defined.",
            faces=sorted(referenced_faces),
        ))
    elif referenced_faces:
        for i, op in enumerate(operations):
            face = op.get("face_selector")
            if face and face != ">Z" and not op.get("setup"):
                issues.append(_issue(
                    "warning", "non_top_face_missing_setup",
                    f"{_op_name(op) or 'operation'} at position {i} machines face "
                    f"'{face}' but has no setup assignment.",
                    i, op, face_selector=face,
                ))

    return issues


def _zone_contains(zone: dict, x: float, y: float) -> bool:
    margin = _as_float(zone.get("margin_mm"), 2.0) or 0.0
    return (
        (_as_float(zone.get("x_min"), 0.0) or 0.0) - margin <= x <=
        (_as_float(zone.get("x_max"), 0.0) or 0.0) + margin
        and (_as_float(zone.get("y_min"), 0.0) or 0.0) - margin <= y <=
        (_as_float(zone.get("y_max"), 0.0) or 0.0) + margin
    )


def _check_fixture_clearance(process_plan_dict: dict) -> list[ValidationIssue]:
    fixture = process_plan_dict.get("fixture")
    setups = process_plan_dict.get("setups") or {}
    if not fixture and not setups:
        return []

    issues: list[ValidationIssue] = []
    fixture_zones = fixture.get("clamping_zones", []) if isinstance(fixture, dict) else []
    for i, op in enumerate(process_plan_dict.get("operations", [])):
        setup_name = op.get("setup")
        setup = setups.get(setup_name, {}) if setup_name else {}
        zones = fixture_zones
        if isinstance(setup, dict) and setup.get("clamping_zones"):
            zones = setup.get("clamping_zones", zones)
        if not zones:
            continue

        op_type = _op_name(op)
        pos = op.get("position")
        if isinstance(pos, (list, tuple)) and len(pos) >= 2:
            x = _as_float(pos[0])
            y = _as_float(pos[1])
            if x is not None and y is not None:
                for zone in zones:
                    if isinstance(zone, dict) and _zone_contains(zone, x, y):
                        label = zone.get("label", "clamping zone")
                        issues.append(_issue(
                            "warning", "fixture_clearance",
                            f"{op_type or 'operation'} at position {i} intersects "
                            f"fixture clamping zone '{label}'.",
                            i, op, zone=label, x=x, y=y,
                        ))

        records = _toolpath_records(op.get("toolpath"))
        points = [p for p in (_toolpath_xyz(record) for record in records or []) if p is not None]
        for x, y, _z in points:
            for zone in zones:
                if isinstance(zone, dict) and _zone_contains(zone, x, y):
                    label = zone.get("label", "clamping zone")
                    issues.append(_issue(
                        "warning", "fixture_toolpath_clearance",
                        f"{op_type or 'operation'} at position {i} has authored "
                        f"toolpath through fixture clamping zone '{label}'.",
                        i, op, zone=label, x=x, y=y,
                    ))
                    break
            else:
                continue
            break

        if op_type in ("face_mill", "contour"):
            issues.append(_issue(
                "warning", "fixture_full_face_clearance",
                f"{op_type} at position {i} covers the full face; verify fixture "
                "clamps are clear of the toolpath.",
                i, op,
            ))

    return issues


def _check_requested_wall_thickness(process_plan_dict: dict) -> list[ValidationIssue]:
    request = process_plan_dict.get("check_wall_thickness")
    min_wall = _as_float(process_plan_dict.get("min_wall_mm"), 1.0) or 1.0
    if not request:
        return []
    return [_issue(
        "warning", "wall_thickness_placeholder",
        f"Wall thickness validation was requested (min {min_wall:g}mm), "
        "but geometric wall analysis is not implemented yet.",
        min_wall_mm=min_wall,
    )]


def _check_plan_metadata(process_plan_dict: dict) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if not process_plan_dict.get("material"):
        issues.append(_issue(
            "warning", "missing_material",
            "Process plan is missing material metadata.",
        ))
    schema = process_plan_dict.get("schema_version")
    if schema and schema != "subcad.shop_floor.v1":
        issues.append(_issue(
            "warning", "unexpected_schema_version",
            f"Process plan schema_version is '{schema}', expected 'subcad.shop_floor.v1'.",
            schema_version=schema,
        ))
    elif "schema_version" not in process_plan_dict:
        issues.append(_issue(
            "warning", "missing_schema_version",
            "Process plan is missing schema_version metadata.",
        ))
    return issues


def validate_all(process_plan_dict: dict, stock_dims: dict,
                 tool_specs: Optional[list] = None,
                 structured: bool = False):
    """Run all validation checks against a complete process plan.

    By default this returns the legacy ``list[str]`` warning output. Pass
    ``structured=True`` to receive a ``ValidationReport`` with issue metadata.
    """
    report = ValidationReport()
    ops = process_plan_dict.get("operations", [])
    merged_stock = dict(stock_dims or {})
    merged_stock.update(process_plan_dict.get("stock_dimensions") or {})

    report.extend(_check_plan_metadata(process_plan_dict))
    report.extend(_check_operation_order(ops))
    report.extend(_check_tool_reach_and_geometry(ops, merged_stock, tool_specs))
    report.extend(_check_toolpaths(ops, merged_stock))
    report.extend(_check_setup_accessibility(process_plan_dict))
    report.extend(_check_fixture_clearance(process_plan_dict))
    report.extend(_check_requested_wall_thickness(process_plan_dict))

    if structured:
        return report
    return report.messages


# =============================================================================
#  Self-test
# =============================================================================

if __name__ == "__main__":
    print("=== SubCAD Validation Self-Test ===\n")
    passed = 0
    failed = 0

    def _check(label: str, condition: bool, detail: str = ""):
        global passed, failed
        if condition:
            passed += 1
            print(f"  PASS  {label}")
        else:
            failed += 1
            print(f"  FAIL  {label}  -- {detail}")

    # ------------------------------------------------------------------
    # 1. check_wall_thickness (placeholder)
    # ------------------------------------------------------------------
    print("1. check_wall_thickness ...")
    result = check_wall_thickness(None, None)
    _check("returns list", isinstance(result, list))
    _check("empty for now", len(result) == 0)
    print()

    # ------------------------------------------------------------------
    # 2. check_tool_reach
    # ------------------------------------------------------------------
    print("2. check_tool_reach ...")
    from dataclasses import dataclass

    @dataclass
    class FakeTool:
        flute_length: float = 50.0

    @dataclass
    class FakeOp:
        depth: float = 0.0

    tool = FakeTool(flute_length=30.0)
    shallow_op = FakeOp(depth=10.0)
    w = check_tool_reach(shallow_op, {}, tool)
    _check("shallow op OK", len(w) == 0, f"got {w}")

    deep_op = FakeOp(depth=40.0)
    w = check_tool_reach(deep_op, {}, tool)
    _check("deep op warns", len(w) == 1, f"got {len(w)}")
    if w:
        _check("mentions flute length", "flute" in w[0].lower())
    print()

    # ------------------------------------------------------------------
    # 3. check_operation_order
    # ------------------------------------------------------------------
    print("3. check_operation_order ...")

    # Correct order
    ops_ok = [
        {"operation": "face_mill"},
        {"operation": "drill"},
        {"operation": "tap"},
        {"operation": "chamfer"},
    ]
    w = check_operation_order(ops_ok)
    _check("correct order OK", len(w) == 0, f"got {w}")

    # Face mill not first
    ops_bad1 = [
        {"operation": "drill"},
        {"operation": "face_mill"},
    ]
    w = check_operation_order(ops_bad1)
    _check("face_mill not first warns", len(w) == 1, f"got {len(w)}")

    # Tap without drill
    ops_bad2 = [
        {"operation": "tap"},
    ]
    w = check_operation_order(ops_bad2)
    _check("tap without drill warns", len(w) == 1, f"got {len(w)}")
    print()

    # ------------------------------------------------------------------
    # 4. validate_all
    # ------------------------------------------------------------------
    print("4. validate_all ...")
    plan = {
        "schema_version": "subcad.shop_floor.v1",
        "material": "aluminum_6061",
        "operations": [
            {"operation": "face_mill"},
            {"operation": "drill"},
        ],
    }
    w = validate_all(plan, {})
    _check("returns list", isinstance(w, list))
    _check("no warnings for valid plan", len(w) == 0, f"got {w}")

    plan_bad = {
        "schema_version": "subcad.shop_floor.v1",
        "material": "aluminum_6061",
        "operations": [
            {"operation": "drill"},
            {"operation": "face_mill"},
        ],
    }
    w = validate_all(plan_bad, {})
    _check("warns for bad order", len(w) == 1, f"got {len(w)}")
    print()

    # ------------------------------------------------------------------
    # 5. SubCAD Shop-Floor v1 structured readiness checks
    # ------------------------------------------------------------------
    print("5. shop-floor readiness checks ...")
    plan_shop = {
        "operations": [
            {
                "operation": "slot",
                "tool_type": "flat_endmill",
                "tool_diameter_mm": 8.0,
                "slot_width_mm": 6.0,
                "depth_mm": 20.0,
                "position": [0, 0],
            },
            {
                "operation": "tap",
                "tool_type": "thread_mill",
                "tool_diameter_mm": 6.0,
                "thread_diameter_mm": 6.0,
                "depth_mm": 12.0,
                "position": [10, 10],
            },
            {
                "operation": "rough_pocket",
                "tool_type": "flat_endmill",
                "tool_diameter_mm": 10.0,
                "depth_mm": 3.0,
                "dimensions": {"width": 20.0, "length": 30.0, "depth": 3.0},
                "corner_radius_mm": 2.0,
                "position": [15, 15],
            },
            {
                "operation": "circular_pocket",
                "tool_type": "flat_endmill",
                "tool_diameter_mm": 12.0,
                "pocket_diameter_mm": 10.0,
                "depth_mm": 2.0,
                "position": [20, 20],
            },
        ],
    }
    report = validate_all(
        plan_shop,
        {},
        tool_specs=[{"tool_type": "flat_endmill", "diameter": 8.0, "flute_length_mm": 10.0}],
        structured=True,
    )
    codes = {issue.code for issue in report.issues}
    _check("structured report returned", isinstance(report, ValidationReport))
    _check("list-compatible iteration", list(report) == report.messages)
    _check("tool flute warning", "tool_flute_length" in codes, f"got {codes}")
    _check("slot width warning", "tool_vs_slot_width" in codes, f"got {codes}")
    _check("tap order warning", "tap_before_drill" in codes, f"got {codes}")
    _check("corner radius warning", "tool_vs_internal_corner_radius" in codes, f"got {codes}")
    _check("circular pocket warning", "tool_vs_pocket_diameter" in codes, f"got {codes}")

    plan_fixture = {
        "fixture": {
            "name": "test_fixture",
            "clamping_zones": [
                {"label": "left_clamp", "x_min": -5, "x_max": 5,
                 "y_min": -5, "y_max": 5, "z_min": 0, "z_max": 10,
                 "margin_mm": 0},
            ],
        },
        "setups": {
            "op1": {"name": "op1", "face_selector": ">Z", "work_offset": "G54"},
        },
        "operations": [
            {"operation": "drill", "position": [0, 0], "setup": "op1", "face_selector": ">Z"},
            {"operation": "drill", "position": [12, 0], "face_selector": ">Z"},
            {"operation": "drill", "position": [20, 0], "setup": "missing", "face_selector": ">Z"},
        ],
        "check_wall_thickness": True,
        "min_wall_mm": 1.5,
    }
    report = validate_all(plan_fixture, {}, structured=True)
    codes = {issue.code for issue in report.issues}
    _check("fixture clearance warning", "fixture_clearance" in codes, f"got {codes}")
    _check("missing setup assignment warning", "operation_missing_setup" in codes, f"got {codes}")
    _check("unknown setup warning", "operation_unknown_setup" in codes, f"got {codes}")
    _check("wall thickness placeholder warning", "wall_thickness_placeholder" in codes, f"got {codes}")

    plan_toolpaths = {
        "schema_version": "subcad.shop_floor.v1",
        "material": "aluminum_6061",
        "stock_dimensions": {"length": 50.0, "width": 40.0, "height": 10.0},
        "operations": [
            {
                "operation": "rough_pocket",
                "depth_mm": 5.0,
                "toolpath": [],
            },
            {
                "operation": "drill",
                "depth_mm": 5.0,
                "toolpath": {
                    "safe_z": 5.0,
                    "moves": [
                        {"type": "rapid", "position": [0, 0, 5.0]},
                        {"type": "plunge", "position": [60, 0, -2.0]},
                    ],
                },
            },
        ],
    }
    report = validate_all(plan_toolpaths, {}, structured=True)
    codes = {issue.code for issue in report.issues}
    legacy_messages = validate_all(plan_toolpaths, {})
    _check("empty toolpath warning", "empty_toolpath" in codes, f"got {codes}")
    _check("missing retract/safe-Z warning", "missing_retract_safe_z" in codes, f"got {codes}")
    _check("toolpath depth warning", "toolpath_above_requested_depth" in codes, f"got {codes}")
    _check("stock bounds warning", "toolpath_stock_bounds" in codes, f"got {codes}")
    _check("legacy validate_all remains list output", isinstance(legacy_messages, list))
    print()

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    total = passed + failed
    print(f"=== {'ALL TESTS PASSED' if failed == 0 else 'SOME TESTS FAILED'} "
          f"({passed}/{total} passed) ===")
    if failed > 0:
        import sys
        sys.exit(1)
