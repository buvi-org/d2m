"""Contract tests for SubCAD operation-video simulation exports.

Run with:

    python test_subcad_operation_video_simulation.py
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path
from typing import Any

from src.subcad import Stock
from src.subcad.geometry import _HAS_CADQUERY
from src.subcad.video_export import build_video_export_plan


TIMELINE_SCHEMA = "subcad.simulation_timeline.v1"
SIMULATION_KWARGS = {
    "resolution_mm": 50.0,
    "keyframe_interval_sec": 0.1,
    "include_machine": False,
    "include_fixtures": False,
    "include_process_effects": False,
    "max_keyframes": 12,
}


def _json_blob(value: Any) -> str:
    try:
        return json.dumps(value, sort_keys=True)
    except TypeError:
        return str(value)


def _normalized_blob(value: Any) -> str:
    return _json_blob(value).replace("\\\\", "/").replace("\\", "/")


def _first_number(mapping: Any, names: tuple[str, ...]) -> float | None:
    if not isinstance(mapping, dict):
        return None
    for name in names:
        value = mapping.get(name)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return float(value)
    return None


def _time_seconds(record: Any) -> float | None:
    return _first_number(
        record,
        (
            "time_seconds",
            "timestamp_seconds",
            "seconds",
            "time_sec",
            "timestamp_sec",
            "t",
        ),
    )


def _segments_from_timeline(timeline: Any) -> list[Any]:
    if isinstance(timeline, list):
        return timeline
    if isinstance(timeline, dict):
        for name in ("segments", "events", "items"):
            value = timeline.get(name)
            if isinstance(value, list):
                return value
    return []


def _segment_start_seconds(segment: Any) -> float | None:
    return _first_number(
        segment,
        ("start_seconds", "start_time_seconds", "start_time_sec", "start_sec", "start", "t0"),
    )


def _segment_end_seconds(segment: Any) -> float | None:
    return _first_number(
        segment,
        ("end_seconds", "end_time_seconds", "end_time_sec", "end_sec", "end", "t1"),
    )


def _timeline_duration_seconds(payload: dict[str, Any]) -> float | None:
    timeline = payload.get("timeline")
    for container in (payload, timeline):
        duration = _first_number(
            container,
            (
                "duration_seconds",
                "total_duration_seconds",
                "total_seconds",
                "total_time_sec",
                "duration_sec",
            ),
        )
        if duration is not None:
            return duration

    segment_ends = [
        end
        for end in (_segment_end_seconds(segment) for segment in _segments_from_timeline(timeline))
        if end is not None
    ]
    if segment_ends:
        return max(segment_ends)

    keyframe_times = [
        time
        for time in (_time_seconds(keyframe) for keyframe in payload.get("stock_keyframes", []))
        if time is not None
    ]
    return max(keyframe_times) if keyframe_times else None


def _state_path_strings(value: Any) -> list[str]:
    paths: list[str] = []
    if isinstance(value, dict):
        for nested in value.values():
            paths.extend(_state_path_strings(nested))
    elif isinstance(value, list):
        for nested in value:
            paths.extend(_state_path_strings(nested))
    elif isinstance(value, str):
        normalized = value.replace("\\", "/")
        if normalized.endswith(".stl") and "simulation_states/" in normalized:
            paths.append(normalized)
    return paths


def _make_reference_part() -> Stock:
    return Stock.rectangular(36, 24, 10, material="aluminum_6061").pocket(
        width=10,
        length=14,
        depth=2,
        corner_radius=0,
        cx=0,
        cy=0,
    )


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def main() -> int:
    if not _HAS_CADQUERY:
        print("SKIP: CadQuery not available")
        return 0

    passed = 0
    failed = 0
    failures: list[str] = []

    def check(label: str, condition: bool, detail: str = "") -> None:
        nonlocal passed, failed
        if condition:
            passed += 1
            print(f"  PASS  {label}")
        else:
            failed += 1
            suffix = f" -- {detail}" if detail else ""
            message = f"  FAIL  {label}{suffix}"
            print(message)
            failures.append(message)

    print("=" * 60)
    print("SubCAD Operation Video Simulation Contract")
    print("=" * 60)

    part = _make_reference_part()
    plan = part.process_plan()
    total_ops = int(plan.get("total_operations", 0))
    check("reference part has one operation", total_ops == 1, f"got {total_ops}")

    timeline_method = getattr(part, "simulation_timeline", None)
    check(
        "Stock exposes simulation_timeline(...)",
        callable(timeline_method),
        "expected public operation-video timeline API",
    )

    timeline_payload: dict[str, Any] | None = None
    if callable(timeline_method):
        try:
            timeline_payload = timeline_method(**SIMULATION_KWARGS)
        except Exception as exc:
            check("simulation_timeline(...) does not raise", False, repr(exc))
        else:
            check("simulation_timeline(...) returns dict", isinstance(timeline_payload, dict))

    if isinstance(timeline_payload, dict):
        check(
            "timeline schema version",
            timeline_payload.get("schema_version") == TIMELINE_SCHEMA,
            f"got {timeline_payload.get('schema_version')!r}",
        )
        check("timeline field present", isinstance(timeline_payload.get("timeline"), (dict, list)))
        check("operations field present", isinstance(timeline_payload.get("operations"), list))
        if isinstance(timeline_payload.get("operations"), list):
            check(
                "timeline operation count matches plan",
                len(timeline_payload["operations"]) == total_ops,
                f"got {len(timeline_payload['operations'])}, expected {total_ops}",
            )

        duration = _timeline_duration_seconds(timeline_payload)
        check("timeline duration uses real seconds", duration is not None and duration > 0.0, f"got {duration}")

        segments = _segments_from_timeline(timeline_payload.get("timeline"))
        timed_segments = [
            segment
            for segment in segments
            if _segment_start_seconds(segment) is not None and _segment_end_seconds(segment) is not None
        ]
        check(
            "timeline has timestamped segments",
            len(timed_segments) > 0,
            "expected segment start/end seconds",
        )
        check(
            "segment timestamps are ordered",
            all(
                _segment_start_seconds(segment) <= _segment_end_seconds(segment)
                for segment in timed_segments
            ),
        )

        keyframes = timeline_payload.get("stock_keyframes")
        check("stock_keyframes list present", isinstance(keyframes, list))
        if isinstance(keyframes, list):
            keyframe_times = [_time_seconds(keyframe) for keyframe in keyframes]
            numeric_times = [time for time in keyframe_times if time is not None]
            check(
                "stock keyframes have seconds",
                len(numeric_times) == len(keyframes) and len(numeric_times) >= 2,
                f"times={keyframe_times}",
            )
            check(
                "stock keyframe seconds are monotonic",
                numeric_times == sorted(numeric_times),
                f"times={numeric_times}",
            )
            if duration is not None and numeric_times:
                check("first keyframe starts at zero seconds", abs(numeric_times[0]) < 1e-9)
                check(
                    "final keyframe reaches the timeline end",
                    abs(numeric_times[-1] - duration) < max(1e-6, duration * 0.01),
                    f"last={numeric_times[-1]}, duration={duration}",
                )
            check(
                "small interval creates mid-operation stock keyframes",
                len(keyframes) > total_ops + 1,
                f"got {len(keyframes)} keyframes for {total_ops} op(s)",
            )
            check(
                "at least one stock keyframe is inside the operation",
                any(time is not None and 0.0 < time < (duration or 0.0) for time in keyframe_times),
            )

    package_method = getattr(part, "export_simulation_package", None)
    check(
        "Stock exposes export_simulation_package(...)",
        callable(package_method),
        "expected public operation-video package export API",
    )

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        if callable(package_method):
            package_dir = tmp_path / "sim_package"
            package: dict[str, Any] | None = None
            try:
                package = package_method(package_dir, **SIMULATION_KWARGS)
            except Exception as exc:
                check("export_simulation_package(...) does not raise", False, repr(exc))
            else:
                check("export_simulation_package(...) returns dict", isinstance(package, dict))

            timeline_path = package_dir / "simulation_timeline.json"
            states_dir = package_dir / "simulation_states"
            check("simulation_timeline.json written", timeline_path.exists())
            check("simulation_states directory written", states_dir.is_dir())

            if timeline_path.exists():
                saved_timeline = _read_json(timeline_path)
                check(
                    "saved timeline schema version",
                    saved_timeline.get("schema_version") == TIMELINE_SCHEMA,
                    f"got {saved_timeline.get('schema_version')!r}",
                )
                state_paths = _state_path_strings(saved_timeline)
                check(
                    "timeline references simulation state STL assets",
                    len(state_paths) > 0,
                    "expected simulation_states/*.stl references",
                )
                check(
                    "referenced simulation state STL assets exist",
                    all((package_dir / path).exists() for path in state_paths),
                    f"paths={state_paths}",
                )

            stl_paths = sorted(states_dir.glob("*.stl")) if states_dir.is_dir() else []
            check("simulation_states/*.stl written", len(stl_paths) >= 2, f"got {len(stl_paths)}")
            check(
                "simulation state STL files are non-empty",
                bool(stl_paths) and all(path.stat().st_size > 0 for path in stl_paths),
            )

            metadata_payloads: list[Any] = []
            if isinstance(package, dict):
                metadata_payloads.append(package)
            for metadata_name in ("scene.json", "package.json", "video_manifest.json"):
                metadata_path = package_dir / metadata_name
                if metadata_path.exists():
                    metadata_payloads.append(_read_json(metadata_path))
            check("scene/package metadata available", len(metadata_payloads) > 0)
            check(
                "scene/package metadata references simulation_timeline.json",
                any("simulation_timeline.json" in _normalized_blob(payload) for payload in metadata_payloads),
            )
            check(
                "scene/package metadata references simulation state STL assets",
                any("simulation_states/" in _normalized_blob(payload) and "stl" in _normalized_blob(payload).lower()
                    for payload in metadata_payloads),
            )
            if isinstance(package, dict):
                video_manifest_asset = package.get("assets", {}).get("video_manifest", {})
                check(
                    "scene assets reference video_manifest.json",
                    video_manifest_asset.get("path") == "video_manifest.json"
                    and video_manifest_asset.get("preferred_format") == "webm",
                    f"asset={video_manifest_asset}",
                )

            headless_plan: dict[str, Any] | None = None
            try:
                headless_plan = build_video_export_plan(
                    package_dir / "scene.json",
                    tmp_path / "headless_export.webm",
                    max_frames=5,
                )
            except Exception as exc:
                check("headless video export dry-run does not raise", False, repr(exc))
            else:
                check("headless video export dry-run returns dict", isinstance(headless_plan, dict))
            if isinstance(headless_plan, dict):
                check("headless video export dry-run status", headless_plan.get("status") == "dry_run")
                check("headless video export resolves WebM output", headless_plan.get("output_format") == "webm")
                check(
                    "headless video export reads timeline seconds",
                    float(headless_plan.get("timeline_total_time_sec") or 0) > 0,
                    f"plan={headless_plan}",
                )
                check(
                    "headless video export honors frame cap",
                    1 <= int(headless_plan.get("frame_count") or 0) <= 5,
                    f"frames={headless_plan.get('frame_count')}",
                )

        viz_dir = tmp_path / "viz_package"
        try:
            scene = part.visualization_package(viz_dir)
        except Exception as exc:
            check("visualization_package(...) remains callable", False, repr(exc))
        else:
            scene_path = viz_dir / "scene.json"
            toolpath_path = viz_dir / "toolpath.json"
            stock_path = viz_dir / "stock.stl"
            check("visualization_package(...) returns dict", isinstance(scene, dict))
            check("visualization scene.json still written", scene_path.exists())
            check("visualization toolpath.json still written", toolpath_path.exists())
            check("visualization stock.stl still written", stock_path.exists() and stock_path.stat().st_size > 0)

            if scene_path.exists():
                scene_json = _read_json(scene_path)
                check(
                    "visualization schema remains v1",
                    scene_json.get("schema_version") == "subcad.visualization_package.v1",
                    f"got {scene_json.get('schema_version')!r}",
                )
                stock_states = scene_json.get("assets", {}).get("stock_states", [])
                check(
                    "visualization stock-state timeline remains op-count based",
                    len(stock_states) == total_ops + 1,
                    f"got {len(stock_states)}, expected {total_ops + 1}",
                )
                check(
                    "visualization stock states still use states/*.stl",
                    all(str(state.get("path", "")).startswith("states/") for state in stock_states),
                )

        turning_part = (
            Stock.cylindrical(60, 100, material="steel_1045")
            .with_machine("machines/generic_lathe.json")
            .mill_turn_setup(axis="Z")
            .turn_od(diameter=42, length=80)
        )
        try:
            turning_timeline = turning_part.simulation_timeline(
                **{**SIMULATION_KWARGS, "include_machine": True, "max_keyframes": 4}
            )
        except Exception as exc:
            check("turning machine-schema timeline does not raise", False, repr(exc))
            turning_timeline = {}
        machines = turning_timeline.get("machines", []) if isinstance(turning_timeline, dict) else []
        check("turning timeline emits machine list", isinstance(machines, list) and len(machines) == 1)
        turning_machine = machines[0] if machines else {}
        check(
            "turning machine keeps component schema",
            isinstance(turning_machine.get("components"), list)
            and any(component.get("id") == "chuck" for component in turning_machine["components"]),
        )
        check(
            "turning machine validates turn capability",
            "turn" in ((turning_machine.get("capabilities") or {}).get("processes") or []),
        )

        turning_package_dir = tmp_path / "turning_machine_package"
        try:
            turning_scene = turning_part.export_simulation_package(
                turning_package_dir,
                **{**SIMULATION_KWARGS, "include_machine": True, "max_keyframes": 4}
            )
        except Exception as exc:
            check("turning package with machine schema does not raise", False, repr(exc))
            turning_scene = {}
        scene_machine = turning_scene.get("machine") if isinstance(turning_scene, dict) else None
        check(
            "turning scene carries viewer machine schema",
            isinstance(scene_machine, dict)
            and isinstance(scene_machine.get("components"), list)
            and any(component.get("type") == "workholding" for component in scene_machine["components"]),
        )

    total = passed + failed
    print("=" * 60)
    if failed == 0:
        print(f"Operation video simulation contract: ALL {passed}/{total} PASSED")
    else:
        print(f"Operation video simulation contract: {passed}/{total} passed, {failed} FAILED")
        print("\nFailures:")
        for failure in failures:
            print(failure)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
