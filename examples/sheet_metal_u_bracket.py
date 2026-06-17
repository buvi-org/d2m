"""Executable SubCAD example for a laser-cut and press-brake formed bracket."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.subcad import Stock


OUTPUT_DIR = Path("renders/sheet_metal_u_bracket")
PREVIEW_SIZE = (1400, 900)


def build_part():
    """Return a small controller/sensor mounting bracket made from one sheet."""
    blank_outline = {
        "type": "polygon",
        "points": [
            (-70, -45), (70, -45), (70, -30), (65, -30),
            (65, 30), (70, 30), (70, 45), (-70, 45),
            (-70, 30), (-65, 30), (-65, -30), (-70, -30),
        ],
    }

    return (
        Stock.sheet(140, 90, 1.6, material="steel_a36")
        .laser_cut_profile(blank_outline, kerf_width=0.18, assist_gas="nitrogen")
        .laser_cut_slot(length=18, width=6, cx=-42, cy=0)
        .laser_cut_slot(length=18, width=6, cx=42, cy=0)
        .laser_cut_hole(diameter=4.5, cx=-25, cy=35)
        .laser_cut_hole(diameter=4.5, cx=25, cy=35)
        .laser_cut_hole(diameter=4.5, cx=-25, cy=-35)
        .laser_cut_hole(diameter=4.5, cx=25, cy=-35)
        .press_brake_bend(axis="X", position=25, angle=90, side="positive", radius=2.0)
        .press_brake_bend(axis="X", position=-25, angle=-90, side="negative", radius=2.0)
    )


def export_example(output_dir: Path = OUTPUT_DIR):
    output_dir.mkdir(parents=True, exist_ok=True)
    part = build_part()
    step_path = output_dir / "sheet_metal_u_bracket.step"
    stl_path = output_dir / "sheet_metal_u_bracket.stl"
    part.to_step(str(step_path))
    part.to_stl(str(stl_path))
    part.save_process_plan(str(output_dir / "process_plan.json"))
    part.visualization_package(output_dir / "viz")
    export_previews(part, stl_path, output_dir)
    return part


def export_previews(part, stl_path: Path, output_dir: Path) -> None:
    """Export smooth PNG previews without triangulation edge overlays."""
    clean = output_dir / "preview_clean.png"
    iso = output_dir / "preview_iso.png"
    if not _render_preview_vtk(stl_path, clean, camera=(1.05, -1.35, 0.55)):
        _render_preview_matplotlib(part, clean, azim=-58, elev=23)
    if not _render_preview_vtk(stl_path, iso, camera=(1.15, -1.10, 0.75)):
        _render_preview_matplotlib(part, iso, azim=-45, elev=30)


def _render_preview_vtk(stl_path: Path, output_path: Path, *, camera: tuple[float, float, float]) -> bool:
    try:
        import vtk
    except Exception:
        return False

    reader = vtk.vtkSTLReader()
    reader.SetFileName(str(stl_path.resolve()))
    reader.Update()
    poly = reader.GetOutput()
    if poly is None or poly.GetNumberOfPoints() == 0:
        return False

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
    actor.GetProperty().SetAmbient(0.22)
    actor.GetProperty().SetInterpolationToPhong()

    renderer = vtk.vtkRenderer()
    renderer.SetBackground(1.0, 1.0, 1.0)
    renderer.AddActor(actor)
    for position, intensity in (((1.0, -1.0, 1.8), 0.95), ((-1.5, 1.2, 0.8), 0.45)):
        light = vtk.vtkLight()
        light.SetLightTypeToSceneLight()
        light.SetPosition(*position)
        light.SetFocalPoint(0.0, 0.0, 0.0)
        light.SetIntensity(intensity)
        renderer.AddLight(light)

    window = vtk.vtkRenderWindow()
    window.SetOffScreenRendering(1)
    window.SetSize(*PREVIEW_SIZE)
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
    active_camera = renderer.GetActiveCamera()
    active_camera.SetFocalPoint(*center)
    active_camera.SetPosition(
        center[0] + span * camera[0],
        center[1] + span * camera[1],
        center[2] + span * camera[2],
    )
    active_camera.SetViewUp(0.0, 0.0, 1.0)
    active_camera.SetViewAngle(24.0)
    renderer.ResetCameraClippingRange()
    window.Render()

    capture = vtk.vtkWindowToImageFilter()
    capture.SetInput(window)
    capture.SetScale(1)
    capture.SetInputBufferTypeToRGB()
    capture.ReadFrontBufferOff()
    capture.Update()

    writer = vtk.vtkPNGWriter()
    writer.SetFileName(str(output_path.resolve()))
    writer.SetInputConnection(capture.GetOutputPort())
    writer.Write()
    return output_path.exists() and output_path.stat().st_size > 0


def _render_preview_matplotlib(part, output_path: Path, *, azim: float, elev: float) -> None:
    import matplotlib.pyplot as plt
    import numpy as np
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    mesh = part.to_mesh()
    vertices = np.asarray(mesh.vertices)
    faces = np.asarray(mesh.faces)
    triangles = [[vertices[index] for index in face] for face in faces]

    fig = plt.figure(figsize=(9, 5.6), dpi=180)
    ax = fig.add_subplot(111, projection="3d")
    ax.add_collection3d(
        Poly3DCollection(
            triangles,
            facecolor="#c9d5df",
            edgecolor="none",
            linewidth=0.0,
            alpha=0.96,
        )
    )
    bbox = part.bounding_box
    cx = (bbox["x_min"] + bbox["x_max"]) / 2.0
    cy = (bbox["y_min"] + bbox["y_max"]) / 2.0
    cz = (bbox["z_min"] + bbox["z_max"]) / 2.0
    span = max(bbox["length"], bbox["width"], bbox["height"])
    ax.set_xlim(cx - span * 0.55, cx + span * 0.55)
    ax.set_ylim(cy - span * 0.42, cy + span * 0.42)
    ax.set_zlim(cz - span * 0.18, cz + span * 0.38)
    ax.view_init(elev=elev, azim=azim)
    try:
        ax.set_box_aspect((1.8, 0.8, 0.45))
    except Exception:
        pass
    ax.set_axis_off()
    fig.patch.set_facecolor("white")
    plt.tight_layout(pad=0)
    plt.savefig(output_path, dpi=180, bbox_inches="tight", pad_inches=0.02, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    result = export_example()
    print(result)
    print(result.bounding_box)
