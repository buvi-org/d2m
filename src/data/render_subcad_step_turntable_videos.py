"""Render high-resolution multi-orientation turntable videos for STEP outputs.

The runner uses each STEP file as the corpus source and renders the sibling STL
mesh generated from the same SubCAD program. Rendering STL is more robust for
VTK offscreen video while preserving the exported geometry under review.
"""

from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SOURCE_ROOT = ROOT / "runs" / "subcad_limit_test_execution_full_patched"
DEFAULT_OUTPUT_ROOT = ROOT / "runs" / "subcad_limit_test_turntable_videos"


ORIENTATIONS = [
    {
        "name": "isometric",
        "elevation_deg": 28.0,
        "start_azimuth_deg": 35.0,
        "view_up": (0.0, 0.0, 1.0),
    },
    {
        "name": "high_oblique",
        "elevation_deg": 62.0,
        "start_azimuth_deg": 15.0,
        "view_up": (0.0, 0.0, 1.0),
    },
    {
        "name": "low_oblique",
        "elevation_deg": 8.0,
        "start_azimuth_deg": 0.0,
        "view_up": (0.0, 0.0, 1.0),
    },
    {
        "name": "underside_oblique",
        "elevation_deg": -28.0,
        "start_azimuth_deg": 45.0,
        "view_up": (0.0, 0.0, 1.0),
    },
]


def require_vtk():
    try:
        import vtk  # type: ignore
        from vtk.util.numpy_support import vtk_to_numpy  # type: ignore
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError("VTK is required for turntable rendering") from exc
    return vtk, vtk_to_numpy


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def find_step_records(source_root: Path) -> list[dict[str, Path]]:
    records = []
    for step_path in sorted(source_root.glob("agent_*/*/*.step")):
        stl_path = step_path.with_suffix(".stl")
        if not stl_path.exists():
            siblings = list(step_path.parent.glob("*.stl"))
            stl_path = siblings[0] if siblings else stl_path
        records.append({
            "step": step_path,
            "stl": stl_path,
            "part_dir": step_path.parent,
            "agent": step_path.parent.parent.name,
            "stem": step_path.stem,
        })
    return records


def load_requirement_id(part_dir: Path) -> str:
    result_path = part_dir / "result.json"
    if result_path.exists():
        try:
            data = json.loads(result_path.read_text(encoding="utf-8"))
            return str(data.get("requirement_id") or part_dir.name)
        except Exception:
            pass
    return part_dir.name.split("_", 1)[0].upper()


def _polydata_from_step(step_path: Path):
    vtk, _ = require_vtk()
    try:
        import cadquery as cq
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError("CadQuery is required for STEP tessellation rendering") from exc

    shape = cq.importers.importStep(str(step_path))
    solids = list(shape.vals()) if hasattr(shape, "vals") else [shape.val()]
    points = vtk.vtkPoints()
    polys = vtk.vtkCellArray()
    point_offset = 0
    total_faces = 0
    for solid in solids:
        if not hasattr(solid, "tessellate"):
            continue
        vertices, faces = solid.tessellate(0.05, 0.03)
        for vertex in vertices:
            points.InsertNextPoint(float(vertex.x), float(vertex.y), float(vertex.z))
        for face in faces:
            tri = vtk.vtkTriangle()
            tri.GetPointIds().SetId(0, int(face[0]) + point_offset)
            tri.GetPointIds().SetId(1, int(face[1]) + point_offset)
            tri.GetPointIds().SetId(2, int(face[2]) + point_offset)
            polys.InsertNextCell(tri)
            total_faces += 1
        point_offset += len(vertices)
    if point_offset == 0 or total_faces == 0:
        raise RuntimeError(f"STEP tessellation produced no mesh: {step_path}")
    poly = vtk.vtkPolyData()
    poly.SetPoints(points)
    poly.SetPolys(polys)
    return poly


def _polydata_from_stl(stl_path: Path):
    vtk, _ = require_vtk()
    reader = vtk.vtkSTLReader()
    reader.SetFileName(str(stl_path))
    reader.Update()
    poly = reader.GetOutput()
    if poly is None or poly.GetNumberOfPoints() == 0:
        raise RuntimeError(f"STL mesh is empty or unreadable: {stl_path}")
    return poly


def setup_scene(step_path: Path, stl_path: Path, width: int, height: int, geometry_source: str, show_edges: bool):
    vtk, _ = require_vtk()

    if geometry_source == "step":
        try:
            poly = _polydata_from_step(step_path)
        except Exception:
            if not stl_path.exists():
                raise
            poly = _polydata_from_stl(stl_path)
            geometry_source = "stl_fallback"
    elif geometry_source == "stl":
        poly = _polydata_from_stl(stl_path)
    else:
        raise ValueError(f"Unknown geometry source: {geometry_source}")

    normals = vtk.vtkPolyDataNormals()
    normals.SetInputData(poly)
    normals.ConsistencyOn()
    normals.AutoOrientNormalsOn()
    normals.SplittingOn()
    normals.SetFeatureAngle(40.0)
    normals.ComputePointNormalsOn()
    normals.ComputeCellNormalsOff()
    normals.Update()

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(normals.GetOutputPort())
    mapper.ScalarVisibilityOff()

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(0.70, 0.76, 0.80)
    actor.GetProperty().SetSpecular(0.35)
    actor.GetProperty().SetSpecularPower(28.0)
    actor.GetProperty().SetDiffuse(0.78)
    actor.GetProperty().SetAmbient(0.20)
    actor.GetProperty().SetInterpolationToPhong()

    renderer = vtk.vtkRenderer()
    renderer.SetBackground(0.96, 0.97, 0.98)
    renderer.AddActor(actor)

    if show_edges:
        edge_filter = vtk.vtkFeatureEdges()
        edge_filter.SetInputData(poly)
        edge_filter.BoundaryEdgesOn()
        edge_filter.FeatureEdgesOn()
        edge_filter.NonManifoldEdgesOn()
        edge_filter.ManifoldEdgesOff()
        edge_filter.SetFeatureAngle(45.0)
        edge_filter.Update()

        edge_mapper = vtk.vtkPolyDataMapper()
        edge_mapper.SetInputConnection(edge_filter.GetOutputPort())
        edge_actor = vtk.vtkActor()
        edge_actor.SetMapper(edge_mapper)
        edge_actor.GetProperty().SetColor(0.04, 0.045, 0.05)
        edge_actor.GetProperty().SetLineWidth(0.8)
        edge_actor.GetProperty().SetOpacity(0.35)
        renderer.AddActor(edge_actor)

    light = vtk.vtkLight()
    light.SetLightTypeToSceneLight()
    light.SetPosition(1.0, -1.0, 1.8)
    light.SetFocalPoint(0.0, 0.0, 0.0)
    light.SetIntensity(0.95)
    renderer.AddLight(light)

    fill = vtk.vtkLight()
    fill.SetLightTypeToSceneLight()
    fill.SetPosition(-1.5, 1.2, 0.8)
    fill.SetFocalPoint(0.0, 0.0, 0.0)
    fill.SetIntensity(0.40)
    renderer.AddLight(fill)

    window = vtk.vtkRenderWindow()
    window.SetOffScreenRendering(1)
    window.SetSize(width, height)
    window.AddRenderer(renderer)
    window.SetMultiSamples(8)

    bounds = poly.GetBounds()
    center = (
        (bounds[0] + bounds[1]) / 2.0,
        (bounds[2] + bounds[3]) / 2.0,
        (bounds[4] + bounds[5]) / 2.0,
    )
    span = max(bounds[1] - bounds[0], bounds[3] - bounds[2], bounds[5] - bounds[4])
    if span <= 0:
        span = 1.0
    radius = math.sqrt(
        (bounds[1] - bounds[0]) ** 2
        + (bounds[3] - bounds[2]) ** 2
        + (bounds[5] - bounds[4]) ** 2
    ) / 2.0
    if radius <= 0:
        radius = span
    camera = renderer.GetActiveCamera()
    camera.SetFocalPoint(*center)
    camera.SetViewAngle(28.0)
    renderer.ResetCamera()

    return {
        "vtk": vtk,
        "window": window,
        "renderer": renderer,
        "camera": camera,
        "center": center,
        "distance": max(radius * 3.0, span * 2.5, 1.0),
        "bounds": bounds,
        "poly_points": int(poly.GetNumberOfPoints()),
        "poly_cells": int(poly.GetNumberOfCells()),
        "geometry_source": geometry_source,
    }


def set_camera(scene: dict[str, Any], orientation: dict[str, Any], frame_index: int, frames_per_orientation: int) -> None:
    camera = scene["camera"]
    cx, cy, cz = scene["center"]
    distance = scene["distance"]
    fraction = frame_index / float(frames_per_orientation)
    az = math.radians(float(orientation["start_azimuth_deg"]) + 360.0 * fraction)
    elev = math.radians(float(orientation["elevation_deg"]))
    x = cx + distance * math.cos(elev) * math.cos(az)
    y = cy + distance * math.cos(elev) * math.sin(az)
    z = cz + distance * math.sin(elev)
    camera.SetPosition(x, y, z)
    camera.SetFocalPoint(cx, cy, cz)
    camera.SetViewUp(*orientation["view_up"])
    camera.OrthogonalizeViewUp()
    camera.SetParallelProjection(True)
    span = max(
        scene["bounds"][1] - scene["bounds"][0],
        scene["bounds"][3] - scene["bounds"][2],
        scene["bounds"][5] - scene["bounds"][4],
        1.0,
    )
    camera.SetParallelScale(span * 0.72)
    scene["renderer"].ResetCameraClippingRange()


def capture_rgb(scene: dict[str, Any], vtk_to_numpy) -> np.ndarray:
    vtk = scene["vtk"]
    window = scene["window"]
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
    arr = np.flipud(arr)
    return np.ascontiguousarray(arr, dtype=np.uint8)


def ffmpeg_command(output_path: Path, width: int, height: int, fps: int, crf: int) -> list[str]:
    return [
        "ffmpeg",
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
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        str(crf),
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        str(output_path),
    ]


def render_video(
    record: dict[str, Path],
    output_root: Path,
    width: int,
    height: int,
    fps: int,
    frames_per_orientation: int,
    crf: int,
    geometry_source: str,
    show_edges: bool,
) -> dict[str, Any]:
    vtk, vtk_to_numpy = require_vtk()
    del vtk
    requirement_id = load_requirement_id(record["part_dir"])
    out_dir = output_root / record["agent"] / record["part_dir"].name
    out_dir.mkdir(parents=True, exist_ok=True)
    video_path = out_dir / "turntable_review.mp4"
    manifest_path = out_dir / "turntable_manifest.json"
    started = time.perf_counter()
    result: dict[str, Any] = {
        "requirement_id": requirement_id,
        "source_step": relative(record["step"]),
        "render_mesh_stl": relative(record["stl"]),
        "video": relative(video_path),
        "manifest": relative(manifest_path),
        "status": "unknown",
        "width": width,
        "height": height,
        "fps": fps,
        "frames_per_orientation": frames_per_orientation,
        "orientations": [item["name"] for item in ORIENTATIONS],
        "geometry_source_requested": geometry_source,
        "show_edges": show_edges,
    }

    if geometry_source == "stl" and not record["stl"].exists():
        result.update({"status": "error", "error": f"Missing STL fallback mesh: {record['stl']}"})
        manifest_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        return result

    try:
        scene = setup_scene(record["step"], record["stl"], width, height, geometry_source, show_edges)
        proc = subprocess.Popen(
            ffmpeg_command(video_path, width, height, fps, crf),
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )
        assert proc.stdin is not None
        frame_manifest = []
        frame_no = 0
        for orientation in ORIENTATIONS:
            start_frame = frame_no
            for i in range(frames_per_orientation):
                set_camera(scene, orientation, i, frames_per_orientation)
                frame = capture_rgb(scene, vtk_to_numpy)
                proc.stdin.write(frame.tobytes())
                frame_no += 1
            frame_manifest.append({
                "orientation": orientation["name"],
                "start_frame": start_frame,
                "end_frame": frame_no - 1,
                "elevation_deg": orientation["elevation_deg"],
                "rotation_deg": 360,
            })
        proc.stdin.close()
        stderr = proc.stderr.read().decode("utf-8", errors="replace") if proc.stderr else ""
        return_code = proc.wait()
        if return_code != 0:
            raise RuntimeError(f"ffmpeg failed with code {return_code}: {stderr[-2000:]}")
        if not video_path.exists() or video_path.stat().st_size == 0:
            raise RuntimeError("ffmpeg did not produce a non-empty video")
        result.update({
            "status": "ok",
            "frames": frame_no,
            "duration_sec": round(frame_no / float(fps), 3),
            "file_size_bytes": video_path.stat().st_size,
            "mesh_points": scene["poly_points"],
            "mesh_cells": scene["poly_cells"],
            "geometry_source_used": scene["geometry_source"],
            "frame_manifest": frame_manifest,
        })
    except Exception as exc:  # noqa: BLE001
        result.update({
            "status": "error",
            "error_type": type(exc).__name__,
            "error": str(exc),
        })
    finally:
        result["elapsed_sec"] = round(time.perf_counter() - started, 3)
        manifest_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


def write_summary(output_root: Path, results: list[dict[str, Any]]) -> None:
    ok = sum(1 for item in results if item.get("status") == "ok")
    errors = len(results) - ok
    summary = {
        "total": len(results),
        "ok": ok,
        "errors": errors,
        "results": results,
    }
    output_root.mkdir(parents=True, exist_ok=True)
    (output_root / "turntable_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    (output_root / "turntable_summary.jsonl").write_text(
        "".join(json.dumps(item, sort_keys=True) + "\n" for item in results),
        encoding="utf-8",
    )
    print(json.dumps({
        "total": len(results),
        "ok": ok,
        "errors": errors,
        "summary": relative(output_root / "turntable_summary.json"),
    }, indent=2))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, default=DEFAULT_SOURCE_ROOT)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--width", type=int, default=1920)
    parser.add_argument("--height", type=int, default=1080)
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--frames-per-orientation", type=int, default=60)
    parser.add_argument("--crf", type=int, default=18)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--name-contains", default="")
    parser.add_argument("--skip-existing", action="store_true")
    parser.add_argument("--geometry-source", choices=["step", "stl"], default="step")
    parser.add_argument("--show-edges", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.source_root.is_absolute():
        args.source_root = ROOT / args.source_root
    if not args.output_root.is_absolute():
        args.output_root = ROOT / args.output_root
    args.source_root = args.source_root.resolve()
    args.output_root = args.output_root.resolve()

    records = find_step_records(args.source_root)
    if args.name_contains:
        needle = args.name_contains.lower()
        records = [record for record in records if needle in record["part_dir"].name.lower()]
    if args.limit:
        records = records[: args.limit]
    results = []
    for index, record in enumerate(records, start=1):
        out_video = args.output_root / record["agent"] / record["part_dir"].name / "turntable_review.mp4"
        out_manifest = args.output_root / record["agent"] / record["part_dir"].name / "turntable_manifest.json"
        if args.skip_existing and out_video.exists() and out_manifest.exists() and out_video.stat().st_size > 0:
            try:
                result = json.loads(out_manifest.read_text(encoding="utf-8"))
                result["status"] = "ok"
                result["skipped_existing"] = True
                results.append(result)
                print(f"[{index}/{len(records)}] skip {record['part_dir'].name}", flush=True)
                continue
            except Exception:
                pass
        print(f"[{index}/{len(records)}] render {record['part_dir'].name}", flush=True)
        results.append(
            render_video(
                record,
                args.output_root,
                args.width,
                args.height,
                args.fps,
                args.frames_per_orientation,
                args.crf,
                args.geometry_source,
                args.show_edges,
            )
        )
    write_summary(args.output_root, results)
    if any(item.get("status") != "ok" for item in results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
