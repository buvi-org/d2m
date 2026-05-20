"""Preview-only G-code-like text for neutral SubCAD toolpaths.

This module is intentionally not a postprocessor.  It formats serialized
neutral toolpath intent into readable controller-like text for review,
debugging, and demos.
"""

from __future__ import annotations

from typing import Any, Iterable, Optional


PREVIEW_NOTICE = "PREVIEW ONLY - NOT FOR PRODUCTION / NOT POSTED G-CODE"
DEFAULT_UNITS = {"linear": "mm", "time": "min", "angle": "deg"}


def gcode_preview(source: Any, *, units: Optional[dict] = None) -> str:
    """Return preview-only G-code-like text from a plan or toolpath.

    ``source`` may be a ``ProcessPlan``-like object, a full serialized process
    plan dict, a serialized ``Toolpath`` dict, or a list of serialized
    toolpaths/moves.
    """
    if hasattr(source, "to_dict"):
        source = source.to_dict()

    source_units = _units_from(source, units)
    lines = _header(source, source_units)

    if isinstance(source, dict) and isinstance(source.get("operations"), list):
        _append_plan_operations(lines, source)
    else:
        _append_standalone_toolpath(lines, source)

    lines.extend([
        "",
        "(End SubCAD preview)",
        f"(Reminder: {PREVIEW_NOTICE})",
    ])
    return "\n".join(lines)


def to_gcode_preview(source: Any, *, units: Optional[dict] = None) -> str:
    """Compatibility alias for :func:`gcode_preview`."""
    return gcode_preview(source, units=units)


def _header(source: Any, units: dict) -> list[str]:
    linear = units.get("linear", "mm")
    time = units.get("time", "min")
    angle = units.get("angle", "deg")

    lines = [
        f"({PREVIEW_NOTICE})",
        "(Neutral SubCAD motion preview for review only.)",
        "(Verify in CAM and use a real machine/controller post before cutting.)",
        f"(Units: linear={linear}, time={time}, angle={angle})",
    ]
    if linear == "mm":
        lines.append("G21 (units intent: millimeters)")
    elif linear in {"inch", "in"}:
        lines.append("G20 (units intent: inches)")
    else:
        lines.append(f"(Units intent: {linear})")
    lines.append("G90 (absolute-position preview intent)")

    if isinstance(source, dict):
        if source.get("material"):
            lines.append(f"(Material: {source.get('material')})")
        if source.get("stock_dimensions"):
            lines.append(f"(Stock: {source.get('stock_dimensions')})")
        setups = source.get("setups") or {}
        if setups:
            lines.append("(Setups/work offsets)")
            for name, setup in setups.items():
                if not isinstance(setup, dict):
                    continue
                face = setup.get("face_selector", "?")
                offset = setup.get("work_offset", "?")
                desc = setup.get("description", "")
                suffix = f" - {desc}" if desc else ""
                lines.append(f"({name}: face={face}, work_offset={offset}{suffix})")
    return lines


def _append_plan_operations(lines: list[str], plan: dict) -> None:
    setups = plan.get("setups") or {}
    for index, op in enumerate(plan.get("operations", []), start=1):
        if not isinstance(op, dict):
            continue
        toolpath = op.get("toolpath")
        _append_operation_header(lines, op, index, setups)
        if toolpath:
            _append_toolpath_moves(lines, toolpath, op)
        else:
            lines.append("(No serialized neutral toolpath available for this operation.)")
        _append_operation_footer(lines, op)


def _append_standalone_toolpath(lines: list[str], source: Any) -> None:
    if isinstance(source, list):
        for index, item in enumerate(source, start=1):
            label = _operation_label(item, index)
            lines.extend(["", f"(OP {index}: {label})"])
            _append_toolpath_moves(lines, item, {})
            lines.append("(END OP)")
        return

    lines.extend(["", f"(OP 1: {_operation_label(source, 1)})"])
    _append_toolpath_moves(lines, source, {})
    lines.append("(END OP)")


def _append_operation_header(
    lines: list[str],
    op: dict,
    index: int,
    setups: dict,
) -> None:
    lines.extend(["", f"(OP {op.get('sequence_number', index)}: {_operation_label(op, index)})"])

    setup_name = op.get("setup")
    setup = setups.get(setup_name, {}) if setup_name else {}
    work_offset = None
    if isinstance(setup, dict):
        work_offset = setup.get("work_offset")
    work_offset = work_offset or op.get("work_offset")
    if setup_name or work_offset:
        lines.append(f"(Setup: {setup_name or 'unspecified'}, work_offset={work_offset or 'unspecified'})")
        if work_offset:
            lines.append(f"{work_offset} (work offset intent)")

    face = op.get("face_selector")
    if face:
        lines.append(f"(Face selector: {face})")

    tool = _tool_label(op)
    if tool:
        lines.append(f"(TOOL: {tool})")

    feed = _feed_from(op)
    spindle = _spindle_from(op)
    coolant = _coolant_from(op)
    if feed is not None:
        lines.append(f"(Feed intent: F{_fmt(feed)})")
    if spindle is not None:
        lines.append(f"S{_fmt(spindle)} (spindle speed intent)")
        lines.append("M3 (spindle on intent)")
    if coolant is not None:
        lines.append(("M8" if coolant else "M9") + " (coolant intent)")


def _append_operation_footer(lines: list[str], op: dict) -> None:
    if _coolant_from(op):
        lines.append("M9 (coolant off preview)")
    if _spindle_from(op) is not None:
        lines.append("M5 (spindle stop preview)")
    lines.append("(END OP)")


def _append_toolpath_moves(lines: list[str], toolpath: Any, op: dict) -> None:
    if hasattr(toolpath, "to_dict"):
        toolpath = toolpath.to_dict()

    default_feed = _feed_from(toolpath) or _feed_from(op)
    default_spindle = _spindle_from(toolpath) or _spindle_from(op)
    default_coolant = _coolant_from(toolpath)
    if default_coolant is None:
        default_coolant = _coolant_from(op)

    moves = _moves_from(toolpath)
    if not moves:
        lines.append("(No moves in serialized neutral toolpath.)")
        return

    for number, move in enumerate(moves, start=1):
        if not isinstance(move, dict):
            move = {"position": move}
        move_type = str(move.get("type") or move.get("move_type") or "feed").lower()
        position = _position_from(move)
        feed = _first_number(move, ("feed_mm_min", "feed", "feed_rate_mm_min")) or default_feed
        spindle = _first_number(move, ("spindle_rpm",)) or default_spindle
        coolant = move.get("coolant", default_coolant)

        comment_parts = [f"{number}: {move_type}"]
        if spindle is not None:
            comment_parts.append(f"S{_fmt(spindle)}")
        if coolant is not None:
            comment_parts.append("coolant " + ("on" if coolant else "off"))

        if move_type == "dwell":
            dwell = _first_number(move, ("dwell_seconds", "seconds", "p")) or 0.0
            lines.append(f"G4 P{_fmt(dwell)} ({'; '.join(comment_parts)})")
        elif move_type in {"rapid", "retract"}:
            lines.append(f"G0{_xyz(position)} ({'; '.join(comment_parts)})")
        elif move_type in {"feed", "plunge"}:
            suffix = f" F{_fmt(feed)}" if feed is not None else ""
            lines.append(f"G1{_xyz(position)}{suffix} ({'; '.join(comment_parts)})")
        elif move_type == "arc":
            lines.append(_arc_line(move, position, feed, comment_parts))
        else:
            suffix = f" F{_fmt(feed)}" if feed is not None else ""
            lines.append(f"G1{_xyz(position)}{suffix} ({'; '.join(comment_parts)}; unrecognized preview move)")


def _arc_line(move: dict, position: Optional[Iterable], feed: Optional[float], comments: list[str]) -> str:
    direction = str(move.get("arc_direction") or move.get("direction") or "").lower()
    code = "G2" if direction == "cw" else "G3" if direction == "ccw" else "G2/G3"
    center = move.get("arc_center") or move.get("center")
    if isinstance(center, (list, tuple)) and len(center) >= 2:
        comments.append(f"center X{_fmt(center[0])} Y{_fmt(center[1])}")
    feed_text = f" F{_fmt(feed)}" if feed is not None else ""
    comments.append(f"ARC PREVIEW {direction or 'direction unspecified'}")
    return f"{code}{_xyz(position)}{feed_text} ({'; '.join(comments)})"


def _moves_from(toolpath: Any) -> list:
    if isinstance(toolpath, dict):
        moves = toolpath.get("moves")
        if isinstance(moves, list):
            return moves
        positions = toolpath.get("positions")
        if isinstance(positions, list):
            return [{"type": "feed", "position": p} for p in positions]
        if "position" in toolpath:
            return [toolpath]
        return []
    if isinstance(toolpath, list):
        if _looks_like_position(toolpath):
            return [{"type": "feed", "position": toolpath}]
        return list(toolpath)
    return []


def _position_from(move: dict) -> Optional[Iterable]:
    if "position" in move:
        return move.get("position")
    if all(axis in move for axis in ("x", "y", "z")):
        return [move.get("x"), move.get("y"), move.get("z")]
    return None


def _xyz(position: Optional[Iterable]) -> str:
    if not isinstance(position, (list, tuple)) or len(position) < 3:
        return ""
    return f" X{_fmt(position[0])} Y{_fmt(position[1])} Z{_fmt(position[2])}"


def _operation_label(data: Any, index: int) -> str:
    if isinstance(data, dict):
        return str(data.get("operation") or data.get("label") or data.get("name") or f"toolpath_{index}")
    return f"toolpath_{index}"


def _tool_label(op: dict) -> str:
    tool = op.get("tool") if isinstance(op, dict) else None
    if isinstance(tool, dict) and tool.get("label"):
        return str(tool["label"])
    tool_type = op.get("tool_type")
    if tool_type is None and isinstance(tool, dict):
        tool_type = tool.get("tool_type")
    diameter = op.get("tool_diameter_mm")
    if diameter is None and isinstance(tool, dict):
        diameter = tool.get("diameter_mm") or tool.get("tool_diameter_mm")
    if tool_type and diameter not in (None, ""):
        return f"{tool_type} D{diameter}mm"
    if tool_type:
        return str(tool_type)
    return ""


def _feed_from(data: Any) -> Optional[float]:
    if not isinstance(data, dict):
        return None
    feed = _first_number(data, ("feed_mm_min", "feed", "feed_rate_mm_min", "feed_rate_mm_per_min"))
    if feed is not None:
        return feed
    feeds = data.get("feeds_speeds")
    if isinstance(feeds, dict):
        return _first_number(feeds, ("feed_rate_mm_per_min", "feed_rate_mm_min", "feed_mm_min", "feed"))
    return None


def _spindle_from(data: Any) -> Optional[float]:
    if not isinstance(data, dict):
        return None
    spindle = _first_number(data, ("spindle_rpm", "rpm"))
    if spindle is not None:
        return spindle
    feeds = data.get("feeds_speeds")
    if isinstance(feeds, dict):
        return _first_number(feeds, ("spindle_rpm", "rpm"))
    return None


def _coolant_from(data: Any) -> Optional[bool]:
    if not isinstance(data, dict):
        return None
    if "coolant" in data:
        return bool(data["coolant"])
    feeds = data.get("feeds_speeds")
    if isinstance(feeds, dict) and "coolant" in feeds:
        return bool(feeds["coolant"])
    return None


def _first_number(data: dict, keys: tuple[str, ...]) -> Optional[float]:
    for key in keys:
        value = data.get(key)
        if value in (None, ""):
            continue
        try:
            return float(value)
        except (TypeError, ValueError):
            continue
    return None


def _units_from(source: Any, override: Optional[dict]) -> dict:
    merged = dict(DEFAULT_UNITS)
    if isinstance(source, dict) and isinstance(source.get("units"), dict):
        merged.update(source["units"])
    if override:
        merged.update(override)
    return merged


def _looks_like_position(value: Any) -> bool:
    if not isinstance(value, (list, tuple)) or len(value) < 3:
        return False
    return all(isinstance(v, (int, float)) for v in value[:3])


def _fmt(value: Any) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)
    text = f"{number:.4f}".rstrip("0").rstrip(".")
    return text if text else "0"


def _self_test() -> None:
    sample = {
        "units": {"linear": "mm", "time": "min", "angle": "deg"},
        "material": "aluminum_6061",
        "setups": {"op1": {"work_offset": "G54", "face_selector": ">Z"}},
        "operations": [
            {
                "sequence_number": 1,
                "operation": "pocket",
                "setup": "op1",
                "tool": {"label": "end_mill D6mm"},
                "feeds_speeds": {"feed_rate_mm_min": 240, "spindle_rpm": 9000, "coolant": True},
                "toolpath": {
                    "operation": "pocket",
                    "moves": [
                        {"type": "rapid", "position": [0, 0, 5]},
                        {"type": "plunge", "position": [0, 0, -1], "feed_mm_min": 120},
                        {"type": "arc", "position": [5, 0, -1], "arc_center": [2.5, 0, -1], "arc_direction": "ccw"},
                        {"type": "dwell", "position": [5, 0, -1], "dwell_seconds": 0.5},
                        {"type": "retract", "position": [5, 0, 5]},
                    ],
                    "coolant": True,
                },
            }
        ],
    }
    preview = gcode_preview(sample)
    assert PREVIEW_NOTICE in preview
    assert "G21" in preview
    assert "G54" in preview
    assert "TOOL: end_mill D6mm" in preview
    assert "ARC PREVIEW" in preview
    assert "G4 P0.5" in preview


if __name__ == "__main__":
    _self_test()
    print("gcode_preview self-test passed")
