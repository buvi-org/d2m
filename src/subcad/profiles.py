"""Lightweight 2D profile normalization for SubCAD geometry operations."""

from __future__ import annotations

import math
from typing import Any


Point2D = tuple[float, float]


def _center(profile: dict[str, Any]) -> Point2D:
    center = profile.get("center")
    if center is not None:
        return float(center[0]), float(center[1])
    return float(profile.get("cx", profile.get("x", 0.0))), float(profile.get("cy", profile.get("y", 0.0)))


def _point(value: Any) -> Point2D:
    return float(value[0]), float(value[1])


def _circle_points(radius: float, cx: float = 0.0, cy: float = 0.0, segments: int = 48) -> list[Point2D]:
    count = max(int(segments), 12)
    return [
        (cx + radius * math.cos(2.0 * math.pi * i / count),
         cy + radius * math.sin(2.0 * math.pi * i / count))
        for i in range(count)
    ]


def _arc_points_from_angles(
    center: Point2D,
    radius: float,
    start_angle: float,
    end_angle: float,
    *,
    clockwise: bool = False,
    segments: int = 16,
) -> list[Point2D]:
    start = math.radians(start_angle)
    end = math.radians(end_angle)
    if clockwise:
        while end >= start:
            end -= 2.0 * math.pi
    else:
        while end <= start:
            end += 2.0 * math.pi
    count = max(int(segments), 2)
    return [
        (
            center[0] + radius * math.cos(start + (end - start) * i / count),
            center[1] + radius * math.sin(start + (end - start) * i / count),
        )
        for i in range(count + 1)
    ]


def _arc_points_from_endpoints(
    start: Point2D,
    end: Point2D,
    center: Point2D,
    *,
    clockwise: bool = False,
    segments: int = 16,
) -> list[Point2D]:
    radius = math.hypot(start[0] - center[0], start[1] - center[1])
    if radius <= 0.0:
        return [start, end]
    start_angle = math.degrees(math.atan2(start[1] - center[1], start[0] - center[0]))
    end_angle = math.degrees(math.atan2(end[1] - center[1], end[0] - center[0]))
    return _arc_points_from_angles(
        center,
        radius,
        start_angle,
        end_angle,
        clockwise=clockwise,
        segments=segments,
    )


def _arc_segment_points(segment: dict[str, Any], current: Point2D | None, segments: int) -> list[Point2D]:
    center = segment.get("center")
    if center is not None:
        center_pt = _point(center)
        clockwise = bool(segment.get("clockwise", segment.get("cw", False)))
        if "start_angle" in segment and "end_angle" in segment:
            radius = float(segment.get("radius", segment.get("r", 0.0)))
            return _arc_points_from_angles(
                center_pt,
                radius,
                float(segment["start_angle"]),
                float(segment["end_angle"]),
                clockwise=clockwise,
                segments=segment.get("segments", segments),
            )
        if "end" in segment:
            start = _point(segment.get("start", current))
            end = _point(segment["end"])
            return _arc_points_from_endpoints(
                start,
                end,
                center_pt,
                clockwise=clockwise,
                segments=segment.get("segments", segments),
            )

    if "points" in segment:
        return normalize_profile_points(segment["points"], arc_segments=segments)
    if "end" in segment:
        pts = []
        if current is None and "start" in segment:
            pts.append(_point(segment["start"]))
        pts.append(_point(segment["end"]))
        return pts
    if "point" in segment:
        return [_point(segment["point"])]
    return []


def _chain_points(segments_spec: list[Any], arc_segments: int) -> list[Point2D]:
    points: list[Point2D] = []
    current: Point2D | None = None
    for segment in segments_spec:
        if isinstance(segment, dict):
            kind = str(segment.get("type", segment.get("kind", "line"))).lower()
            if kind in {"arc", "circle_arc"}:
                new_points = _arc_segment_points(segment, current, arc_segments)
            else:
                new_points = _arc_segment_points(segment, current, arc_segments)
        else:
            new_points = [_point(segment)]
        for point in new_points:
            if not points or point != points[-1]:
                points.append(point)
            current = point
    return points


def _slot_points(profile: dict[str, Any], arc_segments: int) -> list[Point2D]:
    fallback_width = float(profile.get("radius", 5.0)) * 2.0
    width = float(profile.get("width", profile.get("diameter", profile.get("slot_width", fallback_width))))
    length = float(profile.get("length", profile.get("slot_length", width * 2.0)))
    radius = width / 2.0
    cx, cy = _center(profile)
    straight = max(length - width, 0.0)
    left_cx = cx - straight / 2.0
    right_cx = cx + straight / 2.0
    right = _arc_points_from_angles((right_cx, cy), radius, -90.0, 90.0, segments=arc_segments)
    left = _arc_points_from_angles((left_cx, cy), radius, 90.0, 270.0, segments=arc_segments)
    return right + left


def _polygon_points(profile: dict[str, Any]) -> list[Point2D]:
    n_sides = int(profile.get("n_sides", profile.get("sides", profile.get("count", 0))))
    if n_sides < 3:
        return []
    radius = float(
        profile.get(
            "circumradius",
            profile.get("radius", float(profile.get("diameter", 10.0)) / 2.0),
        )
    )
    if radius <= 0.0:
        return []
    cx, cy = _center(profile)
    start_angle = math.radians(float(profile.get("rotation_deg", profile.get("angle", 0.0))))
    return [
        (
            cx + radius * math.cos(start_angle + 2.0 * math.pi * i / n_sides),
            cy + radius * math.sin(start_angle + 2.0 * math.pi * i / n_sides),
        )
        for i in range(n_sides)
    ]


def normalize_profile_points(profile: Any, *, arc_segments: int = 16, circle_segments: int = 64) -> list[Point2D]:
    """Return a closed-profile point approximation when one is practical.

    The function intentionally accepts several lightweight shapes emitted by
    CadQuery/Zero-to-CAD translators while preserving legacy raw point lists.
    """
    if isinstance(profile, dict):
        profile_type = str(profile.get("type", profile.get("shape", ""))).lower()

        points = (
            profile.get("points")
            or profile.get("vertices")
            or profile.get("polyline")
            or profile.get("control_points")
        )
        if points:
            return [_point(point) for point in points]

        if "segments" in profile:
            return _chain_points(list(profile["segments"]), arc_segments)

        if profile_type in {"slot", "obround", "obround_slot", "slot2d"}:
            return _slot_points(profile, arc_segments)

        if profile_type in {"polygon", "regular_polygon"} or "n_sides" in profile or "sides" in profile:
            polygon = _polygon_points(profile)
            if polygon:
                return polygon

        if profile_type in {"circle", "circular"} or "diameter" in profile or "radius" in profile:
            cx, cy = _center(profile)
            radius = float(profile.get("radius", float(profile.get("diameter", 10.0)) / 2.0))
            return _circle_points(radius, cx, cy, circle_segments)

        if profile_type in {"rectangle", "rect", "rib", "pad"} or "width" in profile or "length" in profile:
            width = float(profile.get("width", profile.get("length", 10.0)))
            length = float(profile.get("length", profile.get("width", 10.0)))
            cx, cy = _center(profile)
            return [
                (cx - length / 2.0, cy - width / 2.0),
                (cx + length / 2.0, cy - width / 2.0),
                (cx + length / 2.0, cy + width / 2.0),
                (cx - length / 2.0, cy + width / 2.0),
            ]

    if isinstance(profile, (list, tuple)):
        return [_point(point) for point in profile]

    return []


def profile_bounds_xy(profile: Any) -> tuple[float, float, float, float]:
    """Return ``(xmin, ymin, xmax, ymax)`` for a lightweight profile."""
    points = normalize_profile_points(profile)
    if points:
        xs = [point[0] for point in points]
        ys = [point[1] for point in points]
        return min(xs), min(ys), max(xs), max(ys)
    return -5.0, -5.0, 5.0, 5.0


def profile_span_yx(profile: Any) -> tuple[float, float]:
    """Return ``(width_y, length_x)`` for toolpath and operation metadata."""
    xmin, ymin, xmax, ymax = profile_bounds_xy(profile)
    return ymax - ymin, xmax - xmin
