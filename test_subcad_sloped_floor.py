"""Focused tests for SubCAD sloped-floor wedge cuts."""

from src.subcad import Stock
from src.subcad.operations import create_operation


passed = 0
failed = 0


def check(condition, label):
    global passed, failed
    if condition:
        passed += 1
        print(f"  PASS  {label}")
    else:
        failed += 1
        print(f"  FAIL  {label}")


def run_checks():
    global passed, failed
    passed = 0
    failed = 0

    print("SubCAD sloped-floor tests")

    stock = Stock.rectangular(40, 20, 10)
    part = stock.slope_cut(
        width=8,
        length=20,
        start_depth=2,
        end_depth=6,
        slope_axis="X",
    )

    expected_removed = 20 * 8 * ((2 + 6) / 2)
    actual_removed = stock.volume - part.volume
    check(part.volume < stock.volume, "sloped floor reduces stock volume")
    check(
        abs(actual_removed - expected_removed) < 1.0,
        f"sloped floor removes wedge volume ({actual_removed:.1f} mm3)",
    )

    plan = part.process_plan()
    op = plan["operations"][-1]
    check(op["operation"] == "sloped_floor", "process plan records sloped_floor")
    check(op["start_depth_mm"] == 2, "process plan records start depth")
    check(op["end_depth_mm"] == 6, "process plan records end depth")
    check(op["slope_axis"] == "X", "process plan records slope axis")
    check("toolpath" in op and op["toolpath"].get("moves"), "operation emits neutral toolpath")
    check(op.get("pass_plan", {}).get("strategy") == "sloped_floor_raster",
          "operation emits pass-plan metadata")

    stock_y = Stock.rectangular(40, 20, 10)
    part_y = stock_y.sloped_floor(
        width=10,
        length=12,
        start_depth=1,
        end_depth=5,
        slope_axis="Y",
    )
    expected_removed_y = 12 * 10 * ((1 + 5) / 2)
    actual_removed_y = stock_y.volume - part_y.volume
    check(
        abs(actual_removed_y - expected_removed_y) < 1.0,
        f"Y-axis sloped floor removes wedge volume ({actual_removed_y:.1f} mm3)",
    )

    factory_op = create_operation(
        "slope_cut",
        width=6,
        length=10,
        start_depth=1,
        end_depth=3,
    )
    check(factory_op.to_dict()["operation"] == "sloped_floor",
          "operation factory accepts slope_cut alias")

    print("\n" + "=" * 60)
    if failed:
        print(f"FAILED: {failed} failed, {passed} passed")
        raise AssertionError(f"{failed} sloped-floor checks failed")
    print(f"ALL PASSED: {passed}/{passed} tests passed")


def test_subcad_sloped_floor_wedge_cut_and_plan():
    run_checks()


if __name__ == "__main__":
    try:
        run_checks()
    except AssertionError as exc:
        raise SystemExit(1) from exc
