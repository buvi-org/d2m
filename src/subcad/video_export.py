"""Headless video export for SubCAD operation simulations.

The browser viewer is still the richest interactive surface.  This module is a
non-interactive export path: it reads an exported ``scene.json`` plus its
``simulation_timeline.json`` and ``simulation_states/*.stl`` keyframes, renders
frames with VTK offscreen, and streams raw RGB frames into ffmpeg.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse


DEFAULT_WIDTH = 1280
DEFAULT_HEIGHT = 720
DEFAULT_FPS = 30
DEFAULT_PLAYBACK_RATE = 10.0
RENDERER_VERSION = "subcad.headless_video.v1"


@dataclass(frozen=True)
class TimelineContext:
    scene_path: Path
    scene_dir: Path
    scene: dict[str, Any]
    timeline_path: Path | None
    timeline: dict[str, Any]
    video_manifest_path: Path | None
    video_manifest: dict[str, Any]


@dataclass(frozen=True)
class VideoExportPlan:
    scene_path: Path
    output_path: Path
    manifest_path: Path
    timeline_path: Path | None
    video_manifest_path: Path | None
    width: int
    height: int
    fps: int
    playback_rate: float
    timeline_total_time_sec: float
    rendered_duration_sec: float
    frame_count: int
    output_format: str
    turning_scene: bool
    max_frames: int | None


def build_video_export_plan(
    scene: str | os.PathLike[str],
    out: str | os.PathLike[str],
    *,
    fps: int | None = None,
    width: int = DEFAULT_WIDTH,
    height: int = DEFAULT_HEIGHT,
    playback_rate: float | None = None,
    max_frames: int | None = None,
    manifest: str | os.PathLike[str] | None = None,
) -> dict[str, Any]:
    """Return the resolved headless export plan without rendering frames."""

    context = _load_timeline_context(scene)
    plan = _make_plan(
        context,
        Path(out),
        fps=fps,
        width=width,
        height=height,
        playback_rate=playback_rate,
        max_frames=max_frames,
        manifest=Path(manifest) if manifest else None,
    )
    return _plan_payload(context, plan, status="dry_run")


def export_video(
    scene: str | os.PathLike[str],
    out: str | os.PathLike[str],
    *,
    fps: int | None = None,
    width: int = DEFAULT_WIDTH,
    height: int = DEFAULT_HEIGHT,
    playback_rate: float | None = None,
    max_frames: int | None = None,
    manifest: str | os.PathLike[str] | None = None,
    crf: int = 34,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Export a playable operation-simulation video.

    ``dry_run`` resolves the scene, timeline, keyframes, timings, and output
    paths but does not invoke VTK or ffmpeg.
    """

    context = _load_timeline_context(scene)
    plan = _make_plan(
        context,
        Path(out),
        fps=fps,
        width=width,
        height=height,
        playback_rate=playback_rate,
        max_frames=max_frames,
        manifest=Path(manifest) if manifest else None,
    )
    if dry_run:
        return _plan_payload(context, plan, status="dry_run")

    started = time.perf_counter()
    plan.output_path.parent.mkdir(parents=True, exist_ok=True)
    plan.manifest_path.parent.mkdir(parents=True, exist_ok=True)

    ffmpeg_path = shutil.which("ffmpeg")
    if not ffmpeg_path:
        raise RuntimeError("ffmpeg was not found on PATH")

    vtk, vtk_to_numpy = _require_vtk()
    renderer = _VtkOperationRenderer(vtk, vtk_to_numpy, context, plan)
    result = _plan_payload(context, plan, status="running")
    result.update({
        "ffmpeg": ffmpeg_path,
        "renderer": RENDERER_VERSION,
        "crf": int(crf),
    })

    frame_records: list[dict[str, Any]] = []
    proc: subprocess.Popen[bytes] | None = None
    try:
        command = _ffmpeg_command(ffmpeg_path, plan.output_path, plan.width, plan.height, plan.fps, crf)
        proc = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )
        assert proc.stdin is not None
        for frame_index in range(plan.frame_count):
            sim_time = _frame_sim_time(frame_index, plan.frame_count, plan.timeline_total_time_sec)
            frame, frame_record = renderer.render_frame(frame_index, sim_time)
            proc.stdin.write(frame.tobytes())
            if (
                frame_index == 0
                or frame_index == plan.frame_count - 1
                or frame_index % max(1, plan.fps) == 0
            ):
                frame_records.append(frame_record)
        proc.stdin.close()
        stderr = proc.stderr.read().decode("utf-8", errors="replace") if proc.stderr else ""
        return_code = proc.wait()
        if return_code != 0:
            raise RuntimeError(f"ffmpeg failed with code {return_code}: {stderr[-2000:]}")
        if not plan.output_path.exists() or plan.output_path.stat().st_size == 0:
            raise RuntimeError("ffmpeg did not produce a non-empty video")

        result.update({
            "status": "ok",
            "video": str(plan.output_path),
            "file_size_bytes": plan.output_path.stat().st_size,
            "elapsed_sec": round(time.perf_counter() - started, 3),
            "sampled_frames": frame_records,
        })
        _write_json(plan.manifest_path, result)
        return result
    except Exception as exc:
        if proc is not None and proc.poll() is None:
            proc.kill()
        result.update({
            "status": "error",
            "error_type": type(exc).__name__,
            "error": str(exc),
            "elapsed_sec": round(time.perf_counter() - started, 3),
        })
        _write_json(plan.manifest_path, result)
        raise


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Export a SubCAD operation simulation video headlessly.")
    parser.add_argument("scene", help="Path or visualization URL containing scene.json")
    parser.add_argument("--out", required=True, help="Output video path (.webm or .mp4)")
    parser.add_argument("--manifest", help="Optional JSON manifest output path")
    parser.add_argument("--fps", type=int, default=None, help="Output frames per second")
    parser.add_argument("--width", type=int, default=DEFAULT_WIDTH, help="Output width in pixels")
    parser.add_argument("--height", type=int, default=DEFAULT_HEIGHT, help="Output height in pixels")
    parser.add_argument(
        "--speed",
        "--playback-rate",
        dest="playback_rate",
        type=float,
        default=None,
        help="Simulation seconds per exported video second",
    )
    parser.add_argument("--max-frames", type=int, default=None, help="Render at most this many frames")
    parser.add_argument("--crf", type=int, default=34, help="Encoder CRF/quality value")
    parser.add_argument("--dry-run", action="store_true", help="Print the resolved export plan without rendering")
    args = parser.parse_args(argv)

    try:
        result = export_video(
            args.scene,
            args.out,
            fps=args.fps,
            width=args.width,
            height=args.height,
            playback_rate=args.playback_rate,
            max_frames=args.max_frames,
            manifest=args.manifest,
            crf=args.crf,
            dry_run=args.dry_run,
        )
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({
            "status": "error",
            "error_type": type(exc).__name__,
            "error": str(exc),
        }, indent=2), file=sys.stderr)
        return 1

    print(json.dumps(result, indent=2))
    return 0


def _load_timeline_context(scene: str | os.PathLike[str]) -> TimelineContext:
    scene_path = _resolve_scene_path(scene)
    scene_data = _read_json(scene_path)
    scene_dir = scene_path.parent

    video_manifest_path = _resolve_optional_asset_path(
        scene_dir,
        _asset_path(scene_data, "video_manifest") or "video_manifest.json",
    )
    video_manifest = _read_json(video_manifest_path) if video_manifest_path and video_manifest_path.exists() else {}

    timeline_ref = (
        _asset_path(scene_data, "simulation_timeline")
        or _nested_string(scene_data, ("simulation", "timeline_path"))
        or video_manifest.get("timeline")
        or "simulation_timeline.json"
    )
    timeline_path = _resolve_optional_asset_path(scene_dir, timeline_ref)
    timeline = _read_json(timeline_path) if timeline_path and timeline_path.exists() else {}

    return TimelineContext(
        scene_path=scene_path,
        scene_dir=scene_dir,
        scene=scene_data,
        timeline_path=timeline_path,
        timeline=timeline,
        video_manifest_path=video_manifest_path,
        video_manifest=video_manifest,
    )


def _make_plan(
    context: TimelineContext,
    output_path: Path,
    *,
    fps: int | None,
    width: int,
    height: int,
    playback_rate: float | None,
    max_frames: int | None,
    manifest: Path | None,
) -> VideoExportPlan:
    total_time_sec = _timeline_total_time_sec(context)
    selected_fps = int(fps or context.video_manifest.get("fps") or _nested_number(context.timeline, ("timeline", "fps")) or DEFAULT_FPS)
    selected_fps = max(1, selected_fps)
    selected_rate = float(
        playback_rate
        or context.video_manifest.get("playback_rate")
        or _nested_number(context.timeline, ("timeline", "playback_rate"))
        or DEFAULT_PLAYBACK_RATE
    )
    selected_rate = max(0.001, selected_rate)
    output_path = output_path.expanduser().resolve()
    output_format = _output_format(output_path)
    rendered_duration_sec = total_time_sec / selected_rate if total_time_sec > 0 else 0.0
    frame_count = max(1, int(math.ceil(rendered_duration_sec * selected_fps)))
    if max_frames is not None:
        frame_count = min(frame_count, max(1, int(max_frames)))
        rendered_duration_sec = frame_count / float(selected_fps)
    manifest_path = (manifest.expanduser().resolve() if manifest else output_path.with_suffix(".json"))
    return VideoExportPlan(
        scene_path=context.scene_path,
        output_path=output_path,
        manifest_path=manifest_path,
        timeline_path=context.timeline_path,
        video_manifest_path=context.video_manifest_path,
        width=max(64, int(width)),
        height=max(64, int(height)),
        fps=selected_fps,
        playback_rate=selected_rate,
        timeline_total_time_sec=total_time_sec,
        rendered_duration_sec=round(rendered_duration_sec, 6),
        frame_count=frame_count,
        output_format=output_format,
        turning_scene=_is_turning_scene(context),
        max_frames=max_frames,
    )


def _plan_payload(context: TimelineContext, plan: VideoExportPlan, *, status: str) -> dict[str, Any]:
    keyframes = _keyframe_records(context)
    segments = _timeline_segments(context.timeline)
    return {
        "status": status,
        "renderer": RENDERER_VERSION,
        "scene": str(plan.scene_path),
        "timeline": str(plan.timeline_path) if plan.timeline_path else None,
        "video_manifest": str(plan.video_manifest_path) if plan.video_manifest_path else None,
        "output": str(plan.output_path),
        "manifest": str(plan.manifest_path),
        "output_format": plan.output_format,
        "width": plan.width,
        "height": plan.height,
        "fps": plan.fps,
        "playback_rate": plan.playback_rate,
        "timeline_total_time_sec": plan.timeline_total_time_sec,
        "rendered_duration_sec": plan.rendered_duration_sec,
        "frame_count": plan.frame_count,
        "max_frames": plan.max_frames,
        "turning_scene": plan.turning_scene,
        "segment_count": len(segments),
        "keyframe_count": len(keyframes),
        "machine_component_count": sum(len(machine.get("components") or []) for machine in _machines(context)),
        "notes": [
            "Headless export samples simulation stock keyframes; it does not modify the CadQuery STEP chain.",
            "Current renderer uses VTK primitives for machine schema components and ffmpeg for encoding.",
        ],
    }


class _VtkOperationRenderer:
    def __init__(
        self,
        vtk: Any,
        vtk_to_numpy: Any,
        context: TimelineContext,
        plan: VideoExportPlan,
    ) -> None:
        self.vtk = vtk
        self.vtk_to_numpy = vtk_to_numpy
        self.context = context
        self.plan = plan
        self.keyframes = _keyframe_records(context)
        self.segments = _timeline_segments(context.timeline)
        self.mesh_cache: dict[Path, Any] = {}
        self.chuck_assembly: Any = None
        self.tool_tip_actor: Any = None
        self.tool_holder_source: Any = None
        self.tool_holder_actor: Any = None
        self.tool_insert_actor: Any = None
        self.stock_actor: Any = None
        self.stock_mapper: Any = None
        self.caption_actor: Any = None

        self.renderer = vtk.vtkRenderer()
        self.renderer.SetBackground(0.035, 0.041, 0.067)
        self.window = vtk.vtkRenderWindow()
        self.window.SetOffScreenRendering(1)
        self.window.SetSize(plan.width, plan.height)
        self.window.AddRenderer(self.renderer)
        self._build_scene()

    def render_frame(self, frame_index: int, sim_time_sec: float) -> tuple[Any, dict[str, Any]]:
        segment = _segment_at_time(self.segments, sim_time_sec)
        keyframe = _keyframe_at_time(self.keyframes, sim_time_sec)
        if keyframe is not None:
            polydata = self._polydata_for_keyframe(keyframe)
            if polydata is not None and self.stock_mapper is not None:
                self.stock_mapper.SetInputData(polydata)

        spin_deg = (sim_time_sec * 720.0) % 360.0
        if self.plan.turning_scene and self.stock_actor is not None:
            self.stock_actor.SetOrientation(spin_deg, 0.0, 0.0)
        if self.chuck_assembly is not None:
            self.chuck_assembly.SetOrientation(spin_deg, 0.0, 0.0)

        tool_point = _tool_point_at_time(self.context, segment, sim_time_sec)
        self._update_tool(tool_point, segment)
        self._update_caption(frame_index, sim_time_sec, segment, keyframe)
        frame = _capture_rgb(self.vtk, self.window, self.vtk_to_numpy)
        return frame, {
            "frame": frame_index,
            "simulation_time_sec": round(sim_time_sec, 4),
            "segment": segment.get("id") if segment else None,
            "operation": segment.get("operation") if segment else None,
            "keyframe": keyframe.get("path") if keyframe else None,
        }

    def _build_scene(self) -> None:
        vtk = self.vtk
        self._add_lights()

        first_polydata = self._initial_polydata()
        if first_polydata is not None:
            self.stock_mapper = vtk.vtkPolyDataMapper()
            self.stock_mapper.SetInputData(first_polydata)
            self.stock_actor = vtk.vtkActor()
            self.stock_actor.SetMapper(self.stock_mapper)
            prop = self.stock_actor.GetProperty()
            prop.SetColor(0.58, 0.70, 0.92)
            prop.SetMetallic(0.35)
            prop.SetRoughness(0.38)
            prop.SetInterpolationToPhong()
            self.renderer.AddActor(self.stock_actor)

        if self.plan.turning_scene:
            self._build_lathe_machine()
        else:
            self._build_mill_table()
        self._build_tool_actors()
        self._build_caption_actor()
        self._configure_camera()

    def _add_lights(self) -> None:
        vtk = self.vtk
        key = vtk.vtkLight()
        key.SetLightTypeToSceneLight()
        key.SetPosition(80, -180, 120)
        key.SetFocalPoint(0, 0, 0)
        key.SetIntensity(0.95)
        self.renderer.AddLight(key)

        fill = vtk.vtkLight()
        fill.SetLightTypeToSceneLight()
        fill.SetPosition(-120, 100, 80)
        fill.SetFocalPoint(0, 0, 0)
        fill.SetIntensity(0.35)
        self.renderer.AddLight(fill)

    def _initial_polydata(self) -> Any:
        keyframe = _keyframe_at_time(self.keyframes, 0.0)
        if keyframe is not None:
            polydata = self._polydata_for_keyframe(keyframe)
            if polydata is not None:
                return polydata

        stock_path = _resolve_optional_asset_path(
            self.context.scene_dir,
            _asset_path(self.context.scene, "stock_mesh") or "stock.stl",
        )
        if stock_path and stock_path.exists():
            return self._load_polydata(stock_path)
        return None

    def _polydata_for_keyframe(self, keyframe: dict[str, Any]) -> Any:
        path = _keyframe_path(self.context, keyframe)
        if path is None:
            return None
        if path not in self.mesh_cache:
            self.mesh_cache[path] = self._load_polydata(path)
        return self.mesh_cache[path]

    def _load_polydata(self, path: Path) -> Any:
        vtk = self.vtk
        reader = vtk.vtkSTLReader()
        reader.SetFileName(str(path))
        reader.Update()
        polydata = reader.GetOutput()
        if self.plan.turning_scene:
            matrix = vtk.vtkMatrix4x4()
            rows = (
                (0.0, 0.0, -1.0, 0.0),
                (0.0, 1.0, 0.0, 0.0),
                (1.0, 0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0, 1.0),
            )
            for row_index, row in enumerate(rows):
                for col_index, value in enumerate(row):
                    matrix.SetElement(row_index, col_index, value)
            transform = vtk.vtkTransform()
            transform.SetMatrix(matrix)
            filt = vtk.vtkTransformPolyDataFilter()
            filt.SetTransform(transform)
            filt.SetInputData(polydata)
            filt.Update()
            polydata = filt.GetOutput()

        normals = vtk.vtkPolyDataNormals()
        normals.SetInputData(polydata)
        normals.SetFeatureAngle(55.0)
        normals.ConsistencyOn()
        normals.Update()
        return normals.GetOutput()

    def _build_lathe_machine(self) -> None:
        stock = self.context.scene.get("stock_dimensions") or {}
        length = float(stock.get("height") or stock.get("length") or 100.0)
        diameter = float(stock.get("diameter") or max(stock.get("length") or 0, stock.get("width") or 0, 60.0))
        radius = max(diameter / 2.0, 18.0)
        machine = (_machines(self.context) or [{}])[0]
        z_travel = _axis_travel(machine, "Z")
        span = max(length, z_travel or 0.0, 100.0)
        bed_z = -radius - 18.0

        bed_component = _component(machine, "bed", "base")
        headstock_component = _component(machine, "headstock")
        chuck_component = _component(machine, "lathe_chuck", "chuck", "workholding")
        tailstock_component = _component(machine, "tailstock")

        bed_size = _visual_size(bed_component, (span + 70.0, 18.0, 8.0))
        self._add_box((0.0, 0.0, bed_z), bed_size, _color(bed_component, "#253241"))

        rail_y = max(bed_size[1] * 0.34, 12.0)
        for y in (-rail_y, rail_y):
            self._add_box((0.0, y, bed_z + bed_size[2] / 2.0 + 4.0), (max(bed_size[0] - 14.0, span + 56.0), 4.0, 4.0), "#334155")

        chuck_radius = max(_visual_number(chuck_component, ("diameter_mm", "outer_diameter_mm"), radius * 2.7) / 2.0, radius + 8.0)
        chuck_length = _visual_number(chuck_component, ("length_mm", "width_mm"), 16.0)
        headstock_size = _visual_size(headstock_component, (26.0, chuck_radius * 2.25, chuck_radius * 1.9))
        headstock_x = _component_x(headstock_component, -span / 2.0 - 24.0)
        self._add_box((headstock_x, 0.0, -4.0), headstock_size, _color(headstock_component, "#334155"))

        chuck_x = _component_x(chuck_component, -span / 2.0 - 8.0)
        self.chuck_assembly = self.vtk.vtkAssembly()
        self.chuck_assembly.SetPosition(chuck_x, 0.0, 0.0)
        chuck_actor = self._make_cylinder_x((0.0, 0.0, 0.0), chuck_length, chuck_radius, _color(chuck_component, "#475569"), opacity=1.0)
        self.chuck_assembly.AddPart(chuck_actor)

        jaw_count = max(3, int(round(_visual_number(chuck_component, ("jaw_count", "jaws"), 3.0))))
        jaw_length = max(_visual_number(chuck_component, ("jaw_length_mm",), radius * 0.44), 14.0)
        jaw_width = max(_visual_number(chuck_component, ("jaw_width_mm",), radius * 0.24), 8.0)
        jaw_center_radius = radius + jaw_length / 2.0 - 1.0
        for index in range(jaw_count):
            angle = index * math.tau / jaw_count
            center = (
                chuck_length * 0.45,
                math.cos(angle) * jaw_center_radius,
                math.sin(angle) * jaw_center_radius,
            )
            jaw = self._make_box(center, (chuck_length * 0.62, jaw_length, jaw_width), "#111827")
            jaw.RotateX(math.degrees(angle))
            self.chuck_assembly.AddPart(jaw)
        self.renderer.AddActor(self.chuck_assembly)

        tail_visual = _component_visual(tailstock_component)
        body_size = _number_list(tail_visual.get("body_size_mm"), 3) or (24.0, radius * 1.4, radius * 1.35)
        tailstock_x = _component_x(tailstock_component, span / 2.0 + 25.0)
        tailstock_z = bed_z + radius * 0.65
        self._add_box((tailstock_x, 0.0, tailstock_z), body_size, _color(tailstock_component, "#334155"))

        center_length = float(tail_visual.get("center_length_mm") or 22.0)
        center_radius = max(float(tail_visual.get("center_diameter_mm") or 16.0) / 2.0, 4.0)
        center_x = tailstock_x - center_length * 0.62
        self._add_cone_x((center_x, 0.0, 0.0), center_length, center_radius, "#64748b", direction=-1.0)
        self._add_axis_line((chuck_x - chuck_length, 0.0, 0.0), (tailstock_x + center_length * 0.5, 0.0, 0.0), "#22d3ee")

    def _build_mill_table(self) -> None:
        bounds = _scene_bounds(self.context.scene)
        x_span = max(bounds[1] - bounds[0], 80.0)
        y_span = max(bounds[3] - bounds[2], 80.0)
        z_min = bounds[4]
        self._add_box((0.0, 0.0, z_min - 8.0), (x_span + 50.0, y_span + 50.0, 8.0), "#263241")

    def _build_tool_actors(self) -> None:
        vtk = self.vtk
        sphere = vtk.vtkSphereSource()
        sphere.SetRadius(3.0)
        sphere.SetThetaResolution(24)
        sphere.SetPhiResolution(12)
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(sphere.GetOutputPort())
        self.tool_tip_actor = vtk.vtkActor()
        self.tool_tip_actor.SetMapper(mapper)
        tip_property = self.tool_tip_actor.GetProperty()
        tip_property.SetColor(1.0, 0.63, 0.05)
        tip_property.SetAmbient(0.2)
        tip_property.SetSpecular(0.35)
        self.renderer.AddActor(self.tool_tip_actor)

        self.tool_holder_source = vtk.vtkLineSource()
        tube = vtk.vtkTubeFilter()
        tube.SetInputConnection(self.tool_holder_source.GetOutputPort())
        tube.SetRadius(2.3)
        tube.SetNumberOfSides(16)
        holder_mapper = vtk.vtkPolyDataMapper()
        holder_mapper.SetInputConnection(tube.GetOutputPort())
        self.tool_holder_actor = vtk.vtkActor()
        self.tool_holder_actor.SetMapper(holder_mapper)
        self.tool_holder_actor.GetProperty().SetColor(0.62, 0.70, 0.78)
        self.renderer.AddActor(self.tool_holder_actor)

        self.tool_insert_actor = self._add_cone_x((0.0, 0.0, 0.0), 8.0, 4.0, "#f59e0b", direction=-1.0)

    def _build_caption_actor(self) -> None:
        vtk = self.vtk
        self.caption_actor = vtk.vtkTextActor()
        self.caption_actor.SetDisplayPosition(24, self.plan.height - 54)
        prop = self.caption_actor.GetTextProperty()
        prop.SetFontFamilyToArial()
        prop.SetFontSize(max(16, int(self.plan.height * 0.026)))
        prop.SetColor(0.88, 0.94, 1.0)
        prop.SetBackgroundColor(0.02, 0.03, 0.05)
        prop.SetBackgroundOpacity(0.55)
        self.renderer.AddActor2D(self.caption_actor)

    def _configure_camera(self) -> None:
        if self.plan.turning_scene:
            stock = self.context.scene.get("stock_dimensions") or {}
            length = float(stock.get("height") or stock.get("length") or 100.0)
            diameter = float(stock.get("diameter") or max(stock.get("length") or 0, stock.get("width") or 0, 60.0))
            radius = max(diameter / 2.0, 18.0)
            machine = (_machines(self.context) or [{}])[0]
            span = max(length, _axis_travel(machine, "Z") or 0.0, 100.0)
            camera = self.renderer.GetActiveCamera()
            camera.SetFocalPoint(0.0, 0.0, 0.0)
            camera.SetPosition(0.0, -max(span * 1.75, radius * 6.0), max(radius * 1.2, 45.0))
            camera.SetViewUp(0.0, 0.0, 1.0)
            camera.ParallelProjectionOn()
            camera.SetParallelScale(max(radius * 2.35, span * 0.34))
        else:
            self.renderer.ResetCamera()
            camera = self.renderer.GetActiveCamera()
            camera.ParallelProjectionOn()
            camera.Azimuth(-35)
            camera.Elevation(22)
            self.renderer.ResetCameraClippingRange()

    def _update_tool(self, point: tuple[float, float, float] | None, segment: dict[str, Any] | None) -> None:
        visible = point is not None and segment is not None and _is_cutting_segment(segment)
        for actor in (self.tool_tip_actor, self.tool_holder_actor, self.tool_insert_actor):
            if actor is not None:
                actor.SetVisibility(1 if visible else 0)
        if not visible or point is None:
            return

        px, py, pz = point
        if self.tool_tip_actor is not None:
            self.tool_tip_actor.SetPosition(px, py, pz)

        if self.plan.turning_scene:
            holder_end = (px, py + 38.0, pz + 16.0)
            insert_center = (px + 3.0, py + 2.0, pz)
            insert_direction = (-1.0, -0.25, 0.0)
        else:
            holder_end = (px, py, pz + 45.0)
            insert_center = (px, py, pz + 4.0)
            insert_direction = (0.0, 0.0, -1.0)

        if self.tool_holder_source is not None:
            self.tool_holder_source.SetPoint1(*holder_end)
            self.tool_holder_source.SetPoint2(px, py, pz)
            self.tool_holder_source.Update()

        if self.tool_insert_actor is not None:
            self.tool_insert_actor.SetPosition(*insert_center)
            source = self.tool_insert_actor.GetMapper().GetInputConnection(0, 0).GetProducer()
            if hasattr(source, "SetDirection"):
                source.SetDirection(*insert_direction)
                source.Update()

    def _update_caption(
        self,
        frame_index: int,
        sim_time_sec: float,
        segment: dict[str, Any] | None,
        keyframe: dict[str, Any] | None,
    ) -> None:
        if self.caption_actor is None:
            return
        label = segment.get("label") or segment.get("operation") if segment else "Simulation"
        keyframe_label = keyframe.get("label") if keyframe else "stock"
        self.caption_actor.SetInput(
            f"{label} | t={sim_time_sec:0.2f}s / {self.plan.timeline_total_time_sec:0.2f}s | {keyframe_label}"
        )

    def _add_box(self, center: tuple[float, float, float], size: tuple[float, float, float], color: str, opacity: float = 1.0) -> Any:
        actor = self._make_box(center, size, color, opacity)
        self.renderer.AddActor(actor)
        return actor

    def _make_box(self, center: tuple[float, float, float], size: tuple[float, float, float], color: str, opacity: float = 1.0) -> Any:
        vtk = self.vtk
        source = vtk.vtkCubeSource()
        source.SetXLength(float(size[0]))
        source.SetYLength(float(size[1]))
        source.SetZLength(float(size[2]))
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(source.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.SetPosition(*center)
        actor.GetProperty().SetColor(*_rgb(color))
        actor.GetProperty().SetOpacity(float(opacity))
        actor.GetProperty().SetMetallic(0.45)
        actor.GetProperty().SetRoughness(0.35)
        return actor

    def _add_cylinder_x(self, center: tuple[float, float, float], length: float, radius: float, color: str, opacity: float = 1.0) -> Any:
        actor = self._make_cylinder_x(center, length, radius, color, opacity)
        self.renderer.AddActor(actor)
        return actor

    def _make_cylinder_x(self, center: tuple[float, float, float], length: float, radius: float, color: str, opacity: float = 1.0) -> Any:
        vtk = self.vtk
        source = vtk.vtkCylinderSource()
        source.SetHeight(float(length))
        source.SetRadius(float(radius))
        source.SetResolution(64)
        transform = vtk.vtkTransform()
        transform.RotateZ(90.0)
        filt = vtk.vtkTransformPolyDataFilter()
        filt.SetTransform(transform)
        filt.SetInputConnection(source.GetOutputPort())
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(filt.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.SetPosition(*center)
        actor.GetProperty().SetColor(*_rgb(color))
        actor.GetProperty().SetOpacity(float(opacity))
        actor.GetProperty().SetMetallic(0.65)
        actor.GetProperty().SetRoughness(0.22)
        return actor

    def _add_cone_x(
        self,
        center: tuple[float, float, float],
        length: float,
        radius: float,
        color: str,
        *,
        direction: float | tuple[float, float, float] = 1.0,
    ) -> Any:
        vtk = self.vtk
        source = vtk.vtkConeSource()
        source.SetHeight(float(length))
        source.SetRadius(float(radius))
        source.SetResolution(32)
        if isinstance(direction, tuple):
            source.SetDirection(*direction)
        else:
            source.SetDirection(float(direction), 0.0, 0.0)
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(source.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.SetPosition(*center)
        actor.GetProperty().SetColor(*_rgb(color))
        actor.GetProperty().SetMetallic(0.6)
        actor.GetProperty().SetRoughness(0.24)
        self.renderer.AddActor(actor)
        return actor

    def _add_axis_line(self, start: tuple[float, float, float], end: tuple[float, float, float], color: str) -> None:
        vtk = self.vtk
        source = vtk.vtkLineSource()
        source.SetPoint1(*start)
        source.SetPoint2(*end)
        tube = vtk.vtkTubeFilter()
        tube.SetInputConnection(source.GetOutputPort())
        tube.SetRadius(0.6)
        tube.SetNumberOfSides(8)
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(tube.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(*_rgb(color))
        actor.GetProperty().SetOpacity(0.65)
        self.renderer.AddActor(actor)


def _require_vtk() -> tuple[Any, Any]:
    try:
        import vtk  # type: ignore
        from vtk.util.numpy_support import vtk_to_numpy  # type: ignore
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"VTK is required for headless video export: {exc}") from exc
    return vtk, vtk_to_numpy


def _capture_rgb(vtk: Any, window: Any, vtk_to_numpy: Any) -> Any:
    window.Render()
    filt = vtk.vtkWindowToImageFilter()
    filt.SetInput(window)
    filt.SetInputBufferTypeToRGB()
    filt.ReadFrontBufferOff()
    filt.Update()
    image = filt.GetOutput()
    width, height, _ = image.GetDimensions()
    arr = vtk_to_numpy(image.GetPointData().GetScalars())
    arr = arr.reshape(height, width, 3)
    arr = arr[::-1, :, :]
    return arr.copy()


def _ffmpeg_command(ffmpeg_path: str, output_path: Path, width: int, height: int, fps: int, crf: int) -> list[str]:
    base = [
        ffmpeg_path,
        "-y",
        "-f",
        "rawvideo",
        "-vcodec",
        "rawvideo",
        "-pix_fmt",
        "rgb24",
        "-s",
        f"{width}x{height}",
        "-r",
        str(fps),
        "-i",
        "-",
        "-an",
    ]
    if _output_format(output_path) == "webm":
        return base + [
            "-c:v",
            "libvpx-vp9",
            "-deadline",
            "realtime",
            "-cpu-used",
            "6",
            "-row-mt",
            "1",
            "-b:v",
            "0",
            "-crf",
            str(crf),
            "-pix_fmt",
            "yuv420p",
            str(output_path),
        ]
    return base + [
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        str(crf),
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        str(output_path),
    ]


def _resolve_scene_path(value: str | os.PathLike[str]) -> Path:
    raw = str(value)
    if raw.startswith("http://") or raw.startswith("https://"):
        parsed = urlparse(raw)
        query = parse_qs(parsed.query)
        if query.get("session"):
            raw = query["session"][0]
        else:
            raw = parsed.path
    path = Path(raw).expanduser()
    candidates = [path]
    if not path.is_absolute():
        candidates.append(Path("web") / path)
    for candidate in candidates:
        resolved = candidate.resolve()
        if resolved.exists():
            return resolved
    raise FileNotFoundError(f"scene.json not found: {value}")


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)
    return payload if isinstance(payload, dict) else {}


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def _asset_path(scene: dict[str, Any], name: str) -> str | None:
    asset = (scene.get("assets") or {}).get(name)
    if isinstance(asset, dict) and isinstance(asset.get("path"), str):
        return asset["path"]
    if isinstance(asset, str):
        return asset
    return None


def _resolve_optional_asset_path(base: Path, value: Any) -> Path | None:
    if not isinstance(value, str) or not value:
        return None
    path = Path(value)
    if not path.is_absolute():
        path = base / path
    return path.resolve()


def _nested_string(payload: dict[str, Any], keys: tuple[str, ...]) -> str | None:
    value: Any = payload
    for key in keys:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value if isinstance(value, str) else None


def _nested_number(payload: dict[str, Any], keys: tuple[str, ...]) -> float | None:
    value: Any = payload
    for key in keys:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return float(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else None


def _timeline_total_time_sec(context: TimelineContext) -> float:
    for value in (
        _nested_number(context.timeline, ("timeline", "total_time_sec")),
        context.video_manifest.get("duration_sec"),
        _nested_number(context.scene, ("simulation", "total_time_sec")),
    ):
        if isinstance(value, (int, float)) and value > 0:
            return round(float(value), 6)
    ends = [_segment_end(segment) for segment in _timeline_segments(context.timeline)]
    return round(max(ends), 6) if ends else 0.0


def _timeline_segments(timeline: dict[str, Any]) -> list[dict[str, Any]]:
    raw = (timeline.get("timeline") or {}).get("segments")
    if not isinstance(raw, list):
        raw = timeline.get("segments")
    segments: list[dict[str, Any]] = []
    for item in raw or []:
        if not isinstance(item, dict):
            continue
        segment = dict(item)
        segment.setdefault("startTimeSec", _segment_start(segment))
        segment.setdefault("endTimeSec", _segment_end(segment))
        segment.setdefault("moveType", segment.get("move_type") or segment.get("moveType"))
        segment.setdefault("start", segment.get("start_position") or segment.get("start"))
        segment.setdefault("end", segment.get("end_position") or segment.get("end"))
        segments.append(segment)
    return segments


def _segment_start(segment: dict[str, Any]) -> float:
    for key in ("start_time_sec", "startTimeSec", "start_sec", "start"):
        value = segment.get(key)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return float(value)
    return 0.0


def _segment_end(segment: dict[str, Any]) -> float:
    for key in ("end_time_sec", "endTimeSec", "end_sec"):
        value = segment.get(key)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return float(value)
    return _segment_start(segment)


def _keyframe_records(context: TimelineContext) -> list[dict[str, Any]]:
    keyframes = context.timeline.get("stock_keyframes")
    if not isinstance(keyframes, list):
        keyframes = []
    records = [dict(item) for item in keyframes if isinstance(item, dict)]
    if not records:
        stock_states = (context.scene.get("assets") or {}).get("stock_states")
        if isinstance(stock_states, list):
            records = [dict(item) for item in stock_states if isinstance(item, dict)]
    records.sort(key=lambda item: float(item.get("time_sec") or item.get("timeSec") or item.get("index") or 0.0))
    return records


def _keyframe_path(context: TimelineContext, keyframe: dict[str, Any]) -> Path | None:
    path = keyframe.get("path")
    if not isinstance(path, str):
        return None
    return _resolve_optional_asset_path(context.scene_dir, path)


def _keyframe_at_time(keyframes: list[dict[str, Any]], time_sec: float) -> dict[str, Any] | None:
    selected = None
    for keyframe in keyframes:
        keyframe_time = float(keyframe.get("time_sec") or keyframe.get("timeSec") or 0.0)
        if keyframe_time <= time_sec + 1e-9:
            selected = keyframe
        else:
            break
    return selected or (keyframes[0] if keyframes else None)


def _segment_at_time(segments: list[dict[str, Any]], time_sec: float) -> dict[str, Any] | None:
    for segment in segments:
        if _segment_start(segment) <= time_sec <= _segment_end(segment) + 1e-9:
            return segment
    return segments[-1] if segments else None


def _frame_sim_time(frame_index: int, frame_count: int, total_time_sec: float) -> float:
    if frame_count <= 1:
        return 0.0
    return min(total_time_sec, (frame_index / float(frame_count - 1)) * total_time_sec)


def _is_turning_scene(context: TimelineContext) -> bool:
    values: list[Any] = []
    for source in (context.scene.get("operations"), context.timeline.get("operations"), _timeline_segments(context.timeline)):
        if isinstance(source, list):
            for item in source:
                if isinstance(item, dict):
                    values.extend([
                        item.get("operation"),
                        item.get("process"),
                        item.get("tool_type"),
                        item.get("move_type"),
                        item.get("moveType"),
                        item.get("segment_type"),
                        item.get("fidelity"),
                    ])
    for machine in _machines(context):
        capabilities = machine.get("capabilities") or {}
        values.extend(capabilities.get("processes") or [])
        values.append(machine.get("machine_id"))
        values.append(machine.get("name"))
    text = " ".join(str(value) for value in values if value).lower()
    return "turn" in text or "lathe" in text or "boring" in text


def _machines(context: TimelineContext) -> list[dict[str, Any]]:
    machines = context.timeline.get("machines")
    if isinstance(machines, list) and machines:
        return [machine for machine in machines if isinstance(machine, dict)]
    machines = context.scene.get("machines")
    if isinstance(machines, list) and machines:
        return [machine for machine in machines if isinstance(machine, dict)]
    machine = context.scene.get("machine")
    return [machine] if isinstance(machine, dict) else []


def _tool_point_at_time(
    context: TimelineContext,
    segment: dict[str, Any] | None,
    sim_time_sec: float,
) -> tuple[float, float, float] | None:
    if not segment:
        return None
    start = _point(segment.get("start") or segment.get("start_position"))
    end = _point(segment.get("end") or segment.get("end_position"))
    if start is None or end is None:
        return None
    start_sec = _segment_start(segment)
    end_sec = _segment_end(segment)
    duration = max(end_sec - start_sec, 1e-9)
    progress = max(0.0, min(1.0, (sim_time_sec - start_sec) / duration))

    if _is_turning_scene(context):
        motion_start, motion_end = _turning_motion(segment, start, end)
    else:
        motion_start, motion_end = start, end
    native = tuple(motion_start[index] + (motion_end[index] - motion_start[index]) * progress for index in range(3))
    if _is_turning_scene(context):
        native = _safe_turning_point(context, segment, native, progress)
        return (-native[2], native[1], native[0])
    return native


def _turning_motion(
    segment: dict[str, Any],
    start: tuple[float, float, float],
    end: tuple[float, float, float],
) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
    if not _is_turning_segment(segment):
        return start, end
    move = str(segment.get("moveType") or segment.get("move_type") or "").lower()
    if ("turn" in move or "od" in move) and abs(start[2] - end[2]) > 1e-6:
        max_radius = max(abs(start[0]), abs(end[0]))
        min_radius = min(abs(start[0]), abs(end[0]))
        low_z = start if start[2] <= end[2] else end
        high_z = start if start[2] > end[2] else end
        sign = -1.0 if (start[0] or end[0]) < 0 else 1.0
        return (
            (sign * max_radius, low_z[1], low_z[2]),
            (sign * min_radius, high_z[1], high_z[2]),
        )
    if -start[2] < -end[2]:
        return end, start
    return start, end


def _safe_turning_point(
    context: TimelineContext,
    segment: dict[str, Any],
    point: tuple[float, float, float],
    progress: float,
) -> tuple[float, float, float]:
    if not _is_turning_segment(segment):
        return point
    stock = context.scene.get("stock_dimensions") or {}
    radius = float(stock.get("diameter") or max(stock.get("length") or 0, stock.get("width") or 0, 0)) / 2.0
    if radius <= 0:
        return point
    move = str(segment.get("moveType") or segment.get("move_type") or "").lower()
    if "turn" in move or "od" in move:
        target_radius = min(abs(point[0]), radius)
        current_cut_radius = radius - ((radius - target_radius) * progress)
        sign = -1.0 if point[0] < 0 else 1.0
        return (sign * max(target_radius, current_cut_radius), point[1], point[2])
    return point


def _is_turning_segment(segment: dict[str, Any]) -> bool:
    text = " ".join(str(segment.get(key) or "") for key in (
        "operation",
        "operation_label",
        "moveType",
        "move_type",
        "segment_type",
        "tool_type",
    )).lower()
    return "turn" in text or "boring" in text or "lathe" in text


def _is_cutting_segment(segment: dict[str, Any]) -> bool:
    if segment.get("cutting") is False:
        return False
    text = " ".join(str(segment.get(key) or "") for key in ("moveType", "move_type", "segment_type", "operation")).lower()
    return "cut" in text or "feed" in text or "turn" in text or "boring" in text or "mill" in text or segment.get("cutting") is True


def _point(value: Any) -> tuple[float, float, float] | None:
    if not isinstance(value, (list, tuple)) or len(value) < 3:
        return None
    try:
        return (float(value[0]), float(value[1]), float(value[2]))
    except (TypeError, ValueError):
        return None


def _component(machine: dict[str, Any], *needles: str) -> dict[str, Any]:
    needles_lower = [needle.lower() for needle in needles]
    for component in machine.get("components") or []:
        if not isinstance(component, dict):
            continue
        values = [
            component.get("id"),
            component.get("type"),
            component.get("label"),
            component.get("fixture_type"),
        ]
        text = " ".join(str(value) for value in values if value).lower()
        if any(needle in text for needle in needles_lower):
            return component
    return {}


def _component_visual(component: dict[str, Any]) -> dict[str, Any]:
    visual = component.get("visual")
    return visual if isinstance(visual, dict) else {}


def _component_x(component: dict[str, Any], fallback: float) -> float:
    transform = component.get("transform")
    if isinstance(transform, list) and transform and isinstance(transform[0], (int, float)):
        return float(transform[0])
    return fallback


def _visual_number(component: dict[str, Any], keys: tuple[str, ...], fallback: float) -> float:
    visual = _component_visual(component)
    for key in keys:
        value = visual.get(key)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return float(value)
    return float(fallback)


def _visual_size(component: dict[str, Any], fallback: tuple[float, float, float]) -> tuple[float, float, float]:
    visual = _component_visual(component)
    return _number_list(visual.get("size_mm"), 3) or fallback


def _number_list(value: Any, count: int) -> tuple[float, ...] | None:
    if not isinstance(value, list) or len(value) < count:
        return None
    try:
        return tuple(float(value[index]) for index in range(count))
    except (TypeError, ValueError):
        return None


def _color(component: dict[str, Any], fallback: str) -> str:
    value = _component_visual(component).get("color")
    return value if isinstance(value, str) else fallback


def _rgb(value: str) -> tuple[float, float, float]:
    text = value.strip()
    if text.startswith("#"):
        text = text[1:]
    if len(text) == 3:
        text = "".join(ch * 2 for ch in text)
    if len(text) != 6:
        return (0.5, 0.55, 0.62)
    try:
        return (
            int(text[0:2], 16) / 255.0,
            int(text[2:4], 16) / 255.0,
            int(text[4:6], 16) / 255.0,
        )
    except ValueError:
        return (0.5, 0.55, 0.62)


def _axis_travel(machine: dict[str, Any], axis: str) -> float | None:
    upper = axis.upper()
    for source in (
        (machine.get("linear_limits") or {}).get(upper),
        ((machine.get("axis_limits") or {}).get(upper) or {}).get("limits"),
    ):
        if isinstance(source, list) and len(source) >= 2:
            try:
                return abs(float(source[1]) - float(source[0]))
            except (TypeError, ValueError):
                pass
    for component in machine.get("components") or []:
        if isinstance(component, dict) and str(component.get("axis") or "").upper() == upper:
            limits = component.get("limits")
            if isinstance(limits, list) and len(limits) >= 2:
                try:
                    return abs(float(limits[1]) - float(limits[0]))
                except (TypeError, ValueError):
                    pass
    return None


def _scene_bounds(scene: dict[str, Any]) -> tuple[float, float, float, float, float, float]:
    bbox = scene.get("bounding_box") or {}
    if isinstance(bbox, dict):
        values = (
            bbox.get("x_min"),
            bbox.get("x_max"),
            bbox.get("y_min"),
            bbox.get("y_max"),
            bbox.get("z_min"),
            bbox.get("z_max"),
        )
        if all(isinstance(value, (int, float)) for value in values):
            return tuple(float(value) for value in values)  # type: ignore[return-value]
    return (-40.0, 40.0, -40.0, 40.0, -10.0, 40.0)


def _output_format(path: Path) -> str:
    suffix = path.suffix.lower().lstrip(".")
    if suffix in {"webm", "mp4", "m4v"}:
        return "webm" if suffix == "webm" else "mp4"
    raise ValueError(f"Unsupported output video extension: {path.suffix or '<none>'}; use .webm or .mp4")


if __name__ == "__main__":
    raise SystemExit(main())
