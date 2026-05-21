"""Tests for Z-slice cross-section area handling."""

import numpy as np

from src.simulation.mesh_compare import _polygon_area_from_segments


def _loop_segments(points):
    segments = []
    for index, point in enumerate(points):
        nxt = points[(index + 1) % len(points)]
        segments.append([[point[0], point[1], 0.0], [nxt[0], nxt[1], 0.0]])
    return segments


def test_polygon_area_subtracts_inner_hole_loops():
    outer = [(-5.0, -5.0), (5.0, -5.0), (5.0, 5.0), (-5.0, 5.0)]
    inner = [(-2.0, -2.0), (-2.0, 2.0), (2.0, 2.0), (2.0, -2.0)]
    segments = np.array(_loop_segments(outer) + _loop_segments(inner), dtype=float)

    assert abs(_polygon_area_from_segments(segments) - 84.0) < 1e-6


def test_polygon_area_adds_island_inside_hole():
    outer = [(-5.0, -5.0), (5.0, -5.0), (5.0, 5.0), (-5.0, 5.0)]
    inner = [(-3.0, -3.0), (-3.0, 3.0), (3.0, 3.0), (3.0, -3.0)]
    island = [(-1.0, -1.0), (1.0, -1.0), (1.0, 1.0), (-1.0, 1.0)]
    segments = np.array(
        _loop_segments(outer) + _loop_segments(inner) + _loop_segments(island),
        dtype=float,
    )

    assert abs(_polygon_area_from_segments(segments) - 68.0) < 1e-6
