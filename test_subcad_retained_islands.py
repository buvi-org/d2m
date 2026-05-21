"""Regression tests for retained rib/boss islands machined from taller stock."""

import math

import pytest

from src.subcad import Stock

try:
    import cadquery as cq
except ImportError:  # pragma: no cover - environment dependent
    cq = None


pytestmark = pytest.mark.skipif(cq is None, reason="CadQuery is required")


def _slice_area(part: Stock, z: float, thickness: float = 0.05) -> float:
    slab = (
        cq.Workplane("XY")
        .box(200.0, 200.0, thickness, centered=True)
        .translate((0.0, 0.0, z))
    )
    return part._shape.intersect(slab).val().Volume() / thickness


def test_top_rib_retains_island_without_erasing_plate_volume() -> None:
    part = Stock.rectangular(80.0, 50.0, 12.0).rib(10.0, 40.0, 4.0)

    expected_volume = 80.0 * 50.0 * 8.0 + 10.0 * 40.0 * 4.0
    assert part.volume == pytest.approx(expected_volume, abs=1e-6)
    assert _slice_area(part, 5.5) == pytest.approx(10.0 * 40.0, abs=1e-6)
    assert _slice_area(part, 0.0) == pytest.approx(80.0 * 50.0, abs=1e-6)


def test_bottom_rib_keeps_retained_island_on_bottom_face() -> None:
    part = Stock.rectangular(80.0, 50.0, 12.0).rib(
        10.0,
        40.0,
        4.0,
        face_selector="<Z",
    )

    assert _slice_area(part, -5.5) == pytest.approx(10.0 * 40.0, abs=1e-6)
    assert _slice_area(part, 5.5) == pytest.approx(80.0 * 50.0, abs=1e-6)


def test_circular_machine_around_profile_models_plate_plus_top_boss() -> None:
    part = Stock.rectangular(80.0, 50.0, 12.0).machine_around_profile(
        {"type": "circle", "diameter": 12.0},
        4.0,
    )

    boss_area = math.pi * 6.0**2
    expected_volume = 80.0 * 50.0 * 8.0 + boss_area * 4.0
    assert part.volume == pytest.approx(expected_volume, abs=1e-6)
    assert _slice_area(part, 5.5) == pytest.approx(boss_area, abs=1e-6)
    assert _slice_area(part, 0.0) == pytest.approx(80.0 * 50.0, abs=1e-6)
    assert part.process_plan()["operations"][-1]["operation"] == "machine_around_profile"


def test_multi_island_retained_ribs_preserve_all_top_features() -> None:
    rib_profiles = [
        {"type": "rib", "width": 4.0, "length": 20.0, "cx": -20.0, "cy": 0.0},
        {"type": "rib", "width": 4.0, "length": 20.0, "cx": 0.0, "cy": 0.0},
        {"type": "rib", "width": 4.0, "length": 20.0, "cx": 20.0, "cy": 0.0},
    ]

    part = Stock.rectangular(80.0, 50.0, 10.0).machine_around_profiles(
        rib_profiles,
        2.0,
    )

    expected_top_area = 3 * 4.0 * 20.0
    expected_volume = 80.0 * 50.0 * 8.0 + expected_top_area * 2.0
    assert part.volume == pytest.approx(expected_volume, abs=1e-6)
    assert _slice_area(part, 4.5) == pytest.approx(expected_top_area, abs=1e-6)
    assert _slice_area(part, 0.0) == pytest.approx(80.0 * 50.0, abs=1e-6)
    assert part.process_plan()["operations"][-1]["operation"] == "machine_around_profiles"


def test_rotated_retained_rib_uses_angle_in_profile_geometry() -> None:
    part = Stock.rectangular(80.0, 50.0, 10.0).rib(
        4.0,
        20.0,
        2.0,
        angle=45.0,
    )

    expected_top_area = 4.0 * 20.0
    assert _slice_area(part, 4.5) == pytest.approx(expected_top_area, abs=1e-6)
    operation = part.process_plan()["operations"][-1]
    assert operation["operation"] == "rib"
    assert operation["angle_deg"] == pytest.approx(45.0)


def test_offset_rib_after_prior_slot_remains_continuous() -> None:
    part = (
        Stock.rectangular(80.0, 60.0, 11.0)
        .pocket(width=50.0, length=5.0, depth=5.0, cx=0.0, cy=0.0)
        .rib(width=40.0, length=20.0, height=6.0, cx=20.0, cy=0.0)
    )

    for z in [0.0, 1.0, 2.5, 4.5]:
        assert _slice_area(part, z) == pytest.approx(800.0, abs=1e-6)


def test_blind_counterbore_does_not_drill_through_retained_rib() -> None:
    base = (
        Stock.rectangular(80.0, 60.0, 11.0)
        .pocket(width=50.0, length=5.0, depth=5.0, cx=0.0, cy=0.0)
        .rib(width=40.0, length=20.0, height=6.0, cx=20.0, cy=0.0)
    )

    blind = base.counterbore(8.0, 12.0, 1.0, cx=20.0, cy=0.0, through=False)
    through = base.counterbore(8.0, 12.0, 1.0, cx=20.0, cy=0.0, through=True)

    assert _slice_area(blind, 0.0) == pytest.approx(800.0, abs=1e-6)
    assert _slice_area(through, 0.0) < 800.0


def test_z_band_retained_profiles_support_mixed_feature_heights() -> None:
    stock = Stock.rectangular(80.0, 40.0, 20.0)
    boss = {"type": "circle", "diameter": 12.0, "cx": 0.0, "cy": 0.0}
    ribs = [
        {"type": "rib", "length": 20.0, "width": 4.0, "cx": -20.0, "cy": 0.0},
        {"type": "rib", "length": 20.0, "width": 4.0, "cx": 20.0, "cy": 0.0},
    ]

    part = (
        stock
        .machine_around_profile(boss, height=8.0, base_height=12.0)
        .machine_around_profiles([boss, *ribs], height=4.0, base_height=8.0)
    )

    boss_area = math.pi * 6.0**2
    rib_area = 2 * 20.0 * 4.0
    assert _slice_area(part, -5.0) == pytest.approx(80.0 * 40.0, abs=1e-6)
    assert _slice_area(part, 0.0) == pytest.approx(boss_area + rib_area, abs=1e-6)
    assert _slice_area(part, 7.0) == pytest.approx(boss_area, abs=1e-6)


def test_z_band_pocket_cuts_base_without_erasing_tall_retained_stock() -> None:
    part = Stock.rectangular(80.0, 30.0, 20.0).pocket(
        width=10.0,
        length=60.0,
        depth=8.0,
        cx=10.0,
        cy=10.0,
        base_height=0.0,
    )

    assert _slice_area(part, -5.0) == pytest.approx(80.0 * 30.0 - 60.0 * 10.0, abs=1e-6)
    assert _slice_area(part, 5.0) == pytest.approx(80.0 * 30.0, abs=1e-6)


def test_z_band_circular_pocket_cuts_requested_band_only() -> None:
    part = Stock.rectangular(40.0, 30.0, 10.0).circular_pocket(
        diameter=10.0,
        depth=3.0,
        base_height=2.0,
    )

    expected_area = math.pi * 5.0**2
    assert _slice_area(part, -4.0) == pytest.approx(40.0 * 30.0, abs=1e-6)
    assert _slice_area(part, -2.0) == pytest.approx(40.0 * 30.0 - expected_area, abs=1e-6)
    assert _slice_area(part, 1.5) == pytest.approx(40.0 * 30.0, abs=1e-6)
    assert part.process_plan()["operations"][-1]["base_height_mm"] == pytest.approx(2.0)
