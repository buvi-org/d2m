"""End-to-end test of the SubCAD-to-simulation bridge.

Exercises: Stock -> operations -> simulate() -> result
Tests single-setup and multi-setup scenarios.
"""

import sys
import os

# Ensure src/ is on the path so imports under src.subcad and src.simulation work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import traceback
import warnings

# Suppress trimesh deprecation warnings for cleaner output
warnings.filterwarnings("ignore", category=DeprecationWarning)


def main():
    passed = 0
    failed = 0
    errors = []

    def check(label: str, condition: bool, detail: str = ""):
        nonlocal passed, failed
        if condition:
            passed += 1
            print(f"  PASS  {label}")
        else:
            failed += 1
            msg = f"  FAIL  {label}  -- {detail}"
            print(msg)
            errors.append(msg)

    # ----------------------------------------------------------------
    # Import checks
    # ----------------------------------------------------------------
    print("=" * 60)
    print("0. Import checks")
    print("=" * 60)

    try:
        from src.subcad.stock import Stock, _op_to_simple_toolpath
        from src.subcad.fixturing import FixtureSpec, Setup
        from src.simulation.kinematics import ToolPose
        from src.simulation.tools import create_tool
        from src.simulation.tri_dexel import TriDexelModel
        from src.simulation.material_removal import MaterialRemovalEngine
        import numpy as np
        check("All imports succeeded", True)
    except ImportError as e:
        check("All imports succeeded", False, str(e))
        print(f"\nImport failed: {e}")
        traceback.print_exc()
        print("\n  Cannot continue without imports. Exiting.")
        return 1

    # Check cadquery availability
    try:
        import cadquery
        _HAS_CQ = True
        print("  CadQuery: available")
    except ImportError:
        _HAS_CQ = False
        print("  CadQuery: NOT available -- tests will use simulation-only path")

    from src.subcad.stock import Stock, _op_to_simple_toolpath
    from src.subcad.fixturing import FixtureSpec, Setup
    import numpy as np

    # ----------------------------------------------------------------
    # 1. _op_to_simple_toolpath output format
    # ----------------------------------------------------------------
    print("\n" + "=" * 60)
    print("1. _op_to_simple_toolpath output format")
    print("=" * 60)

    bbox = {"x_min": -50, "x_max": 50, "y_min": -25, "y_max": 25,
            "z_min": -20, "z_max": 0.0,
            "length": 100, "width": 50, "height": 20}

    # Test a drill operation
    drill_op = {
        "operation": "drill",
        "depth_mm": 10.0,
        "position": [25.0, 10.0],
        "tool_type": "drill",
        "tool_diameter_mm": 6.0,
    }
    tp = _op_to_simple_toolpath(drill_op, bbox)
    check("drill returns non-empty list", len(tp) > 0)
    check("drill returns ToolPose objects",
          all(isinstance(p, ToolPose) for p in tp),
          f"types: {set(type(p).__name__ for p in tp)}")
    if len(tp) > 0:
        pose0 = tp[0]
        check("ToolPose has position (numpy array)",
              isinstance(pose0.position, np.ndarray) and pose0.position.shape == (3,))
        check("ToolPose has orientation (quaternion)",
              isinstance(pose0.orientation, np.ndarray) and pose0.orientation.shape == (4,))
        # For a drill at cx=25, cy=10, the XY should be near those values
        check("drill position XY is correct",
              abs(pose0.position[0] - 25.0) < 0.1 and abs(pose0.position[1] - 10.0) < 0.1,
              f"got ({pose0.position[0]:.1f}, {pose0.position[1]:.1f})")

    # Test face_mill (should generate raster)
    fm_op = {
        "operation": "face_mill",
        "depth_mm": 1.0,
        "tool_type": "flat_endmill",
        "tool_diameter_mm": 50.0,
    }
    tp_fm = _op_to_simple_toolpath(fm_op, bbox)
    check("face_mill generates multiple poses", len(tp_fm) >= 2,
          f"got {len(tp_fm)} poses")

    # Test unknown operation type
    unknown_op = {
        "operation": "some_future_op",
        "depth_mm": 5.0,
        "position": [0.0, 0.0],
        "tool_type": "flat_endmill",
        "tool_diameter_mm": 10.0,
    }
    tp_unk = _op_to_simple_toolpath(unknown_op, bbox)
    check("unknown op still generates poses", len(tp_unk) > 0)

    # Test zero/negative depth edge case
    zero_depth_op = {
        "operation": "drill",
        "depth_mm": 0.0,
        "position": [0.0, 0.0],
        "tool_type": "drill",
        "tool_diameter_mm": 6.0,
    }
    tp_zero = _op_to_simple_toolpath(zero_depth_op, bbox)
    check("zero depth defaults to 1.0mm and produces poses", len(tp_zero) > 0)

    # ----------------------------------------------------------------
    # 2. Simulation engine standalone (no CadQuery needed)
    # ----------------------------------------------------------------
    print("\n" + "=" * 60)
    print("2. Simulation engine standalone (trimesh -> tri-dexel)")
    print("=" * 60)

    import trimesh

    # Create a simple box mesh
    stock_mesh = trimesh.creation.box(extents=[100.0, 50.0, 20.0])
    check("stock mesh created", stock_mesh is not None)
    check("stock mesh has vertices", len(stock_mesh.vertices) > 0)

    tri_model = TriDexelModel.from_mesh(stock_mesh, resolution=0.5)
    check("TriDexelModel created", tri_model is not None)
    vol_tri = tri_model.volume()
    check("tri-dexel volume > 0", vol_tri > 0, f"got {vol_tri:.1f} mm^3")
    check("tri-dexel volume ~100*50*20",
          abs(vol_tri - 100000) < 20000,
          f"got {vol_tri:.1f}, expected ~100000")

    engine = MaterialRemovalEngine(tri_dexel=tri_model, linear_resolution=0.5)
    check("MaterialRemovalEngine created", engine is not None)

    # Create a tool and do a single-pose removal
    tool = create_tool("flat_endmill", diameter=10.0)
    check("flat_endmill tool created", tool is not None)

    pose = ToolPose(
        position=np.array([0.0, 0.0, 0.0], dtype=np.float64),
        orientation=np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float64),
    )
    vol_before = tri_model.volume()
    result = engine.remove_tool_at_pose(tool, pose)
    vol_after = tri_model.volume()
    check("removal executed without error", True)
    check("removal result has columns_modified", result.columns_modified > 0,
          f"columns_modified={result.columns_modified}")
    check("volume decreased", vol_after < vol_before,
          f"before={vol_before:.1f}, after={vol_after:.1f}")
    print(f"        Volume removed: {vol_before - vol_after:.1f} mm^3, "
          f"time: {result.time_ms:.1f} ms")

    # ----------------------------------------------------------------
    # 3. Tool creation: all supported types
    # ----------------------------------------------------------------
    print("\n" + "=" * 60)
    print("3. Tool creation: all types")
    print("=" * 60)

    tool_types_tests = [
        ("flat_endmill", {"diameter": 10.0}),
        ("ball_endmill", {"diameter": 6.0}),
        ("drill", {"diameter": 8.5}),
        ("chamfer", {"diameter": 10.0, "tip_diameter": 2.0}),
    ]
    for ttype, kwargs in tool_types_tests:
        try:
            t = create_tool(ttype, **kwargs)
            check(f"create_tool({ttype})", t is not None,
                  f"tool: {t}")
        except Exception as e:
            check(f"create_tool({ttype})", False, str(e))

    # ----------------------------------------------------------------
    # 4. End-to-end: Stock -> simulate() -> result (single setup)
    # ----------------------------------------------------------------
    print("\n" + "=" * 60)
    print("4. End-to-end: Stock chain -> simulate()")
    print("=" * 60)

    if not _HAS_CQ:
        print("  SKIP: CadQuery not available")
    else:
        try:
            part = (Stock.rectangular(100, 50, 20, material="aluminum_6061")
                .face_mill(depth=1.0)
                .pocket(width=30, length=20, depth=5, corner_radius=0)
                .drill(diameter=6, cx=25, cy=10, depth=15, spot_drill=False)
                .chamfer(width=0.5)
            )
            check("part chain created", isinstance(part, Stock))
            check("part has ops", part._plan.total_operations >= 4,
                  f"got {part._plan.total_operations}")

            # Actual simulation call
            result = part.simulate(toolpath_precision=0.5)
            check("simulate returned a dict", isinstance(result, dict))

            # Check no hard error
            if "error" in result and result["error"]:
                check("simulate produced error result", False, result["error"])
            else:
                check("no error in result", True)

                check("has final_volume_mm3", "final_volume_mm3" in result)
                check("has volume_removed_mm3", "volume_removed_mm3" in result)
                check("has gouges list", "gouges" in result)
                check("has cycle_time_minutes", "cycle_time_minutes" in result)
                check("has ops_simulated", "ops_simulated" in result,
                      f"keys: {list(result.keys())}")

                # Volume assertions
                final_vol = result.get("final_volume_mm3", 0)
                removed_vol = result.get("volume_removed_mm3", 0)
                check("final_volume > 0", final_vol > 0, f"got {final_vol}")
                check("volume_removed > 0", removed_vol > 0, f"got {removed_vol}")

                ops_sim = result.get("ops_simulated", 0)
                check("ops_simulated > 0", ops_sim > 0, f"got {ops_sim}")

                print(f"        Final volume: {final_vol:.1f} mm^3")
                print(f"        Volume removed: {removed_vol:.1f} mm^3")
                print(f"        Ops simulated: {ops_sim}")
                print(f"        Gouges: {len(result.get('gouges', []))}")
                print(f"        Cycle time: {result.get('cycle_time_minutes', 'N/A')} min")

                # Print any gouge messages
                for g in result.get("gouges", []):
                    print(f"        Gouge note: {g}")

        except Exception as e:
            check("End-to-end simulate", False, str(e))
            traceback.print_exc()

    # ----------------------------------------------------------------
    # 5. Tool type alias mapping
    # ----------------------------------------------------------------
    print("\n" + "=" * 60)
    print("5. Tool type alias handling in simulate()")
    print("=" * 60)

    if _HAS_CQ:
        try:
            # Create a part with known tool types and simulate
            part2 = (Stock.rectangular(60, 40, 15, material="aluminum_6061")
                .face_mill(depth=0.5)   # uses flat_endmill tool
                .drill(diameter=5, cx=10, cy=5, depth=8, spot_drill=False)
            )
            result2 = part2.simulate(toolpath_precision=0.5)
            if "error" in result2 and result2["error"]:
                check("simulate with aliases", False, result2["error"])
            else:
                check("simulate with aliases succeeded", True)
                # Check for any skipped operations due to unknown tool type
                skipped = [g for g in result2.get("gouges", [])
                          if "skipped" in g.get("message", "").lower() or "unknown" in g.get("message", "").lower()]
                if skipped:
                    check("no operations skipped for unknown tool types",
                          len(skipped) == 0,
                          f"skipped: {skipped}")
        except Exception as e:
            check("Tool alias test", False, str(e))
            traceback.print_exc()

    # ----------------------------------------------------------------
    # 6. Multi-setup scenario (fixture + two setups)
    # ----------------------------------------------------------------
    print("\n" + "=" * 60)
    print("6. Multi-setup with fixture")
    print("=" * 60)

    if _HAS_CQ:
        try:
            from src.subcad.fixturing import ClampingZone

            # Create a fixture spec with proper ClampingZone objects
            fixture = FixtureSpec(
                name="test_vise",
                clamping_zones=[
                    ClampingZone(
                        label="vise_jaws",
                        x_min=-25, x_max=25,
                        y_min=-30, y_max=30,
                        z_min=-20, z_max=-10,
                    )
                ],
            )
            check("fixture created", fixture is not None)

            # Setup 1: machine top face
            part3 = (Stock.rectangular(80, 60, 25, material="steel_4140")
                .with_fixture(fixture)
                .new_setup("setup_top", face_selector=">Z",
                          work_offset="G54",
                          description="Top face operations")
            )
            check("setup_top created", "setup_top" in part3._setups)
            check("active setup is setup_top",
                  part3._active_setup == "setup_top")

            part3 = (part3
                .face_mill(depth=2.0)
                .pocket(width=40, length=30, depth=10, corner_radius=2)
                .drill(diameter=8, cx=20, cy=15, depth=12, spot_drill=False)
            )
            check("setup_top ops applied", part3._plan.total_operations >= 3)

            # Setup 2: flip part, machine bottom face
            part3 = part3.new_setup("setup_bottom", face_selector="<Z",
                                    work_offset="G55",
                                    description="Bottom face operations")
            check("setup_bottom created", "setup_bottom" in part3._setups)

            part3 = part3.face_mill(depth=1.0)
            check("bottom face op applied",
                  part3._plan.total_operations >= 4)

            # Now simulate
            result3 = part3.simulate(toolpath_precision=0.5)
            if "error" in result3 and result3["error"]:
                check("multi-setup simulate", False, result3["error"])
            else:
                check("multi-setup simulate succeeded", True)
                check("multi-setup final_volume > 0",
                      result3.get("final_volume_mm3", 0) > 0)
                check("multi-setup volume_removed > 0",
                      result3.get("volume_removed_mm3", 0) > 0)
                print(f"        Multi-setup final volume: {result3.get('final_volume_mm3', 0):.1f} mm^3")
                print(f"        Multi-setup volume removed: {result3.get('volume_removed_mm3', 0):.1f} mm^3")

        except Exception as e:
            check("Multi-setup scenario", False, str(e))
            traceback.print_exc()

    # ----------------------------------------------------------------
    # 7. Fixture clearance validation
    # ----------------------------------------------------------------
    print("\n" + "=" * 60)
    print("7. Fixture clearance validation")
    print("=" * 60)

    if _HAS_CQ:
        try:
            from src.subcad.fixturing import ClampingZone

            fixture2 = FixtureSpec(
                name="soft_jaws",
                clamping_zones=[
                    ClampingZone(
                        label="left_jaw",
                        x_min=-30, x_max=-20,
                        y_min=-30, y_max=30,
                        z_min=-20, z_max=0,
                    ),
                    ClampingZone(
                        label="right_jaw",
                        x_min=20, x_max=30,
                        y_min=-30, y_max=30,
                        z_min=-20, z_max=0,
                    ),
                ],
            )
            part4 = (Stock.rectangular(80, 60, 20, material="aluminum_6061")
                .with_fixture(fixture2)
                .new_setup("op1", face_selector=">Z")
            )
            # Drill near the jaw -- should generate a warning
            part4 = part4.drill(diameter=6, cx=0, cy=0, depth=10, spot_drill=False)

            warnings = part4.validate_fixture_clearance()
            check("validate_fixture_clearance returns list",
                  isinstance(warnings, list))
            # The drill at (0,0) is between the jaws so may or may not warn
            print(f"        Clearance warnings: {len(warnings)}")
            for w in warnings:
                print(f"          {w}")

        except Exception as e:
            check("Fixture clearance validation", False, str(e))
            traceback.print_exc()

    # ----------------------------------------------------------------
    # 8. Immutability preserved across simulation
    # ----------------------------------------------------------------
    print("\n" + "=" * 60)
    print("8. Immutability across simulation")
    print("=" * 60)

    if _HAS_CQ:
        try:
            s_a = Stock.rectangular(50, 50, 10)
            ops_before = s_a._plan.total_operations
            _ = s_a.simulate()
            ops_after = s_a._plan.total_operations
            check("simulate doesn't mutate operation count",
                  ops_before == ops_after,
                  f"before={ops_before}, after={ops_after}")

            s_b = s_a.face_mill(1.0)
            _ = s_b.simulate()
            check("simulate on face_milled part doesn't mutate it",
                  s_b._plan.total_operations == 1)
        except Exception as e:
            check("Immutability test", False, str(e))
            traceback.print_exc()

    # ----------------------------------------------------------------
    # 9. Error handling: simulate without operations
    # ----------------------------------------------------------------
    print("\n" + "=" * 60)
    print("9. simulate on part with no operations")
    print("=" * 60)

    if _HAS_CQ:
        try:
            s_empty = Stock.rectangular(30, 30, 10)
            result_empty = s_empty.simulate()
            check("empty plan simulate returns dict",
                  isinstance(result_empty, dict))
            check("empty plan ops_simulated is 0",
                  result_empty.get("ops_simulated", -1) == 0,
                  f"got {result_empty.get('ops_simulated')}")
            check("empty plan: initial volume == final volume",
                  abs(result_empty.get("volume_removed_mm3", 1)) < 0.01,
                  f"got {result_empty.get('volume_removed_mm3')}")
        except Exception as e:
            check("Empty plan simulate", False, str(e))
            traceback.print_exc()

    # ----------------------------------------------------------------
    # Summary
    # ----------------------------------------------------------------
    total = passed + failed
    print("\n" + "=" * 60)
    print(f"RESULTS: {passed}/{total} passed, {failed}/{total} failed")
    print("=" * 60)

    if errors:
        print("\nFailures:")
        for e in errors:
            print(f"  {e}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    exit(main())
