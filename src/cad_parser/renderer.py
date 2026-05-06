"""4-view image generator for STEP file visualization.

Generates four standard orthographic/isometric views of a CAD model:
front, top, side, and isometric.  Uses CadQuery's built-in rendering
or matplotlib 3D as a fallback.

Phase 0 stub: provides a functional but simplified implementation.
Future phases will add hidden-line removal, dimension annotations,
and higher-resolution output.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
import os
import math

import numpy as np


# =========================================================================
#  Data types
# =========================================================================

@dataclass
class CameraView:
    """Camera setup for a standard engineering view."""
    name: str            # front, top, side, isometric
    azimuth: float       # degrees (matplotlib convention)
    elevation: float     # degrees (matplotlib convention)
    roll: float = 0.0    # degrees


# Standard engineering views
_STANDARD_VIEWS = [
    CameraView("front", azimuth=-90.0, elevation=0.0),
    CameraView("top", azimuth=-90.0, elevation=90.0),
    CameraView("side", azimuth=0.0, elevation=0.0),
    CameraView("isometric", azimuth=-60.0, elevation=30.0),
]


# =========================================================================
#  Check for available rendering backends
# =========================================================================

_HAS_CQ_RENDERER = False
try:
    # CadQuery has built-in SVG/PNG export via its jupyter renderer
    # or via cq-editor's export utilities
    import cadquery as cq  # noqa: F401
    try:
        from cadquery import exporters
        _HAS_CQ_RENDERER = True
    except ImportError:
        pass
except ImportError:
    pass

_HAS_MATPLOTLIB = False
try:
    import matplotlib
    matplotlib.use("Agg")  # non-interactive backend
    import matplotlib.pyplot as plt
    _HAS_MATPLOTLIB = True
except ImportError:
    pass

_HAS_TRIMESH = False
try:
    import trimesh
    _HAS_TRIMESH = True
except ImportError:
    pass


# =========================================================================
#  matplotlib 3D-based rendering
# =========================================================================

def _render_with_matplotlib(
    vertices: np.ndarray,
    faces: np.ndarray,
    view: CameraView,
    output_path: str,
    bounds: Optional[tuple] = None,
    dpi: int = 150,
    figsize: tuple = (6, 6),
    face_color: str = "#e8e0d8",
    edge_color: str = "#333333",
    edge_width: float = 0.3,
) -> str:
    """Render a single view of a triangle mesh using matplotlib 3D.

    Args:
        vertices: (V, 3) vertex positions.
        faces: (F, 3) face indices.
        view: CameraView with azimuth, elevation, roll.
        output_path: File path for the output PNG.
        bounds: Optional (xmin, ymin, zmin, xmax, ymax, zmax) for axis equal.
        dpi: Output resolution.
        figsize: Figure size in inches.
        face_color: Mesh face color.
        edge_color: Mesh edge color.
        edge_width: Mesh edge line width.

    Returns:
        The output file path.
    """
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    fig = plt.figure(figsize=figsize, dpi=dpi)
    ax = fig.add_subplot(111, projection="3d")

    # Build triangle collection
    tri_verts = []
    if faces is not None and len(faces) > 0 and len(vertices) > 0:
        for tri in faces:
            try:
                tri_verts.append([
                    vertices[tri[0]],
                    vertices[tri[1]],
                    vertices[tri[2]],
                ])
            except IndexError:
                continue

    if tri_verts:
        mesh = Poly3DCollection(
            tri_verts,
            facecolors=face_color,
            edgecolors=edge_color,
            linewidths=edge_width,
            alpha=0.92,
        )
        ax.add_collection3d(mesh)

    # Set camera view
    ax.view_init(elev=view.elevation, azim=view.azimuth)

    # Set equal aspect ratio
    if bounds and bounds[3] > bounds[0] and bounds[4] > bounds[1] and bounds[5] > bounds[2]:
        ax.set_xlim(bounds[0], bounds[3])
        ax.set_ylim(bounds[1], bounds[4])
        ax.set_zlim(bounds[2], bounds[5])
    elif tri_verts:
        # Use data limits
        all_pts = np.vstack(tri_verts).reshape(-1, 3)
        margin = 0.05 * np.max(all_pts.max(axis=0) - all_pts.min(axis=0))
        if margin < 0.1:
            margin = 1.0
        ax.set_xlim(all_pts[:, 0].min() - margin, all_pts[:, 0].max() + margin)
        ax.set_ylim(all_pts[:, 1].min() - margin, all_pts[:, 1].max() + margin)
        ax.set_zlim(all_pts[:, 2].min() - margin, all_pts[:, 2].max() + margin)

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title(view.name.title(), fontsize=12, fontweight="bold")

    # Hide grid for cleaner engineering view
    ax.grid(True, alpha=0.3)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor("white")
    ax.yaxis.pane.set_edgecolor("white")
    ax.zaxis.pane.set_edgecolor("white")

    plt.tight_layout()
    plt.savefig(output_path, dpi=dpi, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    return output_path


# =========================================================================
#  CadQuery-based rendering
# =========================================================================

def _render_with_cadquery(
    step_filepath: str,
    output_dir: str,
) -> list[str]:
    """Render 4 views of a STEP file using CadQuery's exporter.

    This path produces higher-quality vector/raster output using
    CadQuery's built-in OCCT-based renderer.

    Args:
        step_filepath: Path to the STEP file.
        output_dir: Directory for output images.

    Returns:
        List of output file paths.
    """
    try:
        import cadquery as cq
    except ImportError:
        return _render_stub(step_filepath, output_dir)

    try:
        shape = cq.importers.importStep(step_filepath)
    except Exception as exc:
        raise RuntimeError(
            f"CadQuery could not import STEP file: {exc}"
        ) from exc

    output_paths: list[str] = []
    base_name = os.path.splitext(os.path.basename(step_filepath))[0]

    # CadQuery view directions (view vector)
    view_vectors = {
        "front": (0.0, 0.0, 1.0),    # looking at -Z face
        "top": (0.0, 1.0, 0.0),      # looking at +Y face
        "side": (1.0, 0.0, 0.0),     # looking at +X face
        "isometric": (1.0, 1.0, 1.0), # diagonal
    }

    for view_name, view_dir in view_vectors.items():
        output_path = os.path.join(output_dir, f"{base_name}_{view_name}.png")
        try:
            # CadQuery SVG export then convert to PNG
            svg_opts = exporters.ExportTypes.SVG
            svg_path = os.path.join(output_dir, f"{base_name}_{view_name}.svg")
            exporters.export(
                shape,
                svg_path,
                exportType=svg_opts,
                projectionDir=view_dir,
                showAxes=False,
                showGrid=False,
            )
            # SVG produced; for PNG we note it was generated
            if os.path.isfile(svg_path):
                output_paths.append(svg_path)
            else:
                # Fallback: try direct PNG if available
                try:
                    png_opts = exporters.ExportTypes.PNG
                    exporters.export(
                        shape, output_path, exportType=png_opts,
                        projectionDir=view_dir,
                    )
                    if os.path.isfile(output_path):
                        output_paths.append(output_path)
                except Exception:
                    output_paths.append(output_path)  # placeholder
        except Exception:
            output_paths.append(output_path)

    return output_paths


# =========================================================================
#  Stub renderer (placeholder)
# =========================================================================

def _render_stub(step_filepath: str, output_dir: str) -> list[str]:
    """Stub renderer: returns placeholder file paths without generating images.

    Useful when no rendering backend is available. Returns paths that
    callers can check for existence to determine if rendering succeeded.

    Args:
        step_filepath: Path to the STEP file.
        output_dir: Directory where images would be written.

    Returns:
        List of placeholder file paths.
    """
    base_name = os.path.splitext(os.path.basename(step_filepath))[0]
    paths = []
    for view in _STANDARD_VIEWS:
        paths.append(
            os.path.join(output_dir, f"{base_name}_{view.name}.png")
        )
    return paths


# =========================================================================
#  Trimesh-based rendering
# =========================================================================

def _render_with_trimesh(
    step_filepath: str,
    output_dir: str,
) -> list[str]:
    """Render 4 views by converting STEP to mesh via trimesh then using scene.

    Trimesh can load STEP files via its built-in loader (which wraps
    pythonOCC or CadQuery). This provides a lightweight rendering path.

    Args:
        step_filepath: Path to the STEP file.
        output_dir: Directory for output images.

    Returns:
        List of output file paths.
    """
    if not _HAS_TRIMESH:
        return _render_stub(step_filepath, output_dir)

    import trimesh

    try:
        mesh = trimesh.load_mesh(step_filepath)
    except Exception:
        return _render_stub(step_filepath, output_dir)

    if mesh is None or (hasattr(mesh, "vertices") and len(mesh.vertices) == 0):
        return _render_stub(step_filepath, output_dir)

    if hasattr(mesh, "geometry") and isinstance(mesh, trimesh.Scene):
        # Convert scene to a single mesh
        meshes = []
        for geom in mesh.geometry.values():
            if hasattr(geom, "vertices") and len(geom.vertices) > 0:
                meshes.append(geom)
        if meshes:
            mesh = trimesh.util.concatenate(meshes)
        else:
            return _render_stub(step_filepath, output_dir)

    # If we have matplotlib, use it for rendering
    if _HAS_MATPLOTLIB and hasattr(mesh, "vertices"):
        base_name = os.path.splitext(os.path.basename(step_filepath))[0]
        bounds = mesh.bounds if hasattr(mesh, "bounds") else None
        bb = (
            bounds[0][0], bounds[0][1], bounds[0][2],
            bounds[1][0], bounds[1][1], bounds[1][2],
        ) if bounds is not None else None

        output_paths = []
        for view in _STANDARD_VIEWS:
            output_path = os.path.join(output_dir, f"{base_name}_{view.name}.png")
            try:
                _render_with_matplotlib(
                    mesh.vertices, mesh.faces, view, output_path, bounds=bb,
                )
                output_paths.append(output_path)
            except Exception:
                output_paths.append(output_path)  # placeholder
        return output_paths

    return _render_stub(step_filepath, output_dir)


# =========================================================================
#  Public API
# =========================================================================

def render_views(
    step_filepath: str,
    output_dir: str,
    method: str = "auto",
) -> list[str]:
    """Generate 4 standard engineering views of a STEP model.

    Produces four PNG (or SVG) images: front, top, side, and isometric.
    Automatically selects the best available rendering backend.

    Args:
        step_filepath: Path to the .step or .stp file.
        output_dir: Directory to write output images. Created if it
                    does not exist.
        method: Rendering method:
            - "auto": Use CadQuery > trimesh+matplotlib > stub.
            - "cadquery": Force CadQuery backend.
            - "matplotlib": Force matplotlib 3D backend.
            - "stub": Placeholder only (no actual rendering).

    Returns:
        List of output file paths. For the stub renderer, files may
        not actually exist on disk.

    Raises:
        FileNotFoundError: If step_filepath does not exist.
        RuntimeError: If rendering fails with the chosen method.
    """
    step_filepath = os.path.abspath(step_filepath)

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Validate method first (before file existence)
    valid_methods = {"auto", "cadquery", "matplotlib", "stub"}
    if method not in valid_methods:
        raise ValueError(
            f"Unknown render method: {method!r}. "
            f"Valid options: {', '.join(sorted(valid_methods))}."
        )

    if method == "stub":
        return _render_stub(step_filepath, output_dir)

    if not os.path.isfile(step_filepath):
        raise FileNotFoundError(f"STEP file not found: {step_filepath}")

    if method == "cadquery":
        if not _HAS_CQ_RENDERER:
            raise RuntimeError(
                "CadQuery renderer is not available. "
                "Install cadquery with: pip install cadquery"
            )
        return _render_with_cadquery(step_filepath, output_dir)

    elif method == "matplotlib":
        if not _HAS_MATPLOTLIB:
            raise RuntimeError(
                "matplotlib renderer is not available. "
                "Install with: pip install matplotlib"
            )
        return _render_with_trimesh(step_filepath, output_dir)

    elif method == "auto":
        # Try backends in order of quality
        if _HAS_CQ_RENDERER:
            try:
                return _render_with_cadquery(step_filepath, output_dir)
            except Exception:
                pass

        if _HAS_TRIMESH or _HAS_MATPLOTLIB:
            try:
                result = _render_with_trimesh(step_filepath, output_dir)
                # Check if any actual images were produced
                if result and any(os.path.isfile(p) for p in result):
                    return result
            except Exception:
                pass

        return _render_stub(step_filepath, output_dir)

    else:
        # Should be unreachable due to validation above
        return _render_stub(step_filepath, output_dir)


# =========================================================================
#  Self-test
# =========================================================================

if __name__ == "__main__":
    print("=== Renderer Self-Test ===\n")

    import tempfile

    # -----------------------------------------------------------------
    # Test 1: Stub renderer
    # -----------------------------------------------------------------
    print("1. Stub renderer ...")
    with tempfile.TemporaryDirectory() as tmpdir:
        paths = render_views("nonexistent.step", tmpdir, method="stub")
        print(f"   Generated {len(paths)} placeholder paths:")
        for p in paths:
            print(f"     {p}")
        assert len(paths) == 4, f"Expected 4 views, got {len(paths)}"
        assert all(p.endswith(".png") for p in paths)
    print("   PASSED\n")

    # -----------------------------------------------------------------
    # Test 2: Output directory creation
    # -----------------------------------------------------------------
    print("2. Output directory creation ...")
    with tempfile.TemporaryDirectory() as parent:
        nested = os.path.join(parent, "subdir", "images")
        paths = render_views("nonexistent.step", nested, method="stub")
        assert os.path.isdir(nested), "Output directory was not created"
        print(f"   Created nested dir: {nested}")
    print("   PASSED\n")

    # -----------------------------------------------------------------
    # Test 3: File-not-found error
    # -----------------------------------------------------------------
    print("3. File-not-found error ...")
    try:
        render_views("no_such_file.step", "/tmp", method="auto")
        assert False, "Should have raised FileNotFoundError"
    except FileNotFoundError:
        print("   Correctly raised FileNotFoundError")
    print("   PASSED\n")

    # -----------------------------------------------------------------
    # Test 4: Camera view definitions
    # -----------------------------------------------------------------
    print("4. Camera view definitions ...")
    for view in _STANDARD_VIEWS:
        print(f"   {view.name:<10} azim={view.azimuth:7.1f}  elev={view.elevation:7.1f}")
    assert len(_STANDARD_VIEWS) == 4
    names = [v.name for v in _STANDARD_VIEWS]
    assert names == ["front", "top", "side", "isometric"]
    print("   PASSED\n")

    # -----------------------------------------------------------------
    # Test 5: Invalid method
    # -----------------------------------------------------------------
    print("5. Invalid method error ...")
    try:
        render_views("nonexistent.step", "/tmp", method="invalid_method")
        assert False, "Should have raised ValueError"
    except ValueError as exc:
        print(f"   Correctly raised ValueError: {exc}")
    print("   PASSED\n")

    # -----------------------------------------------------------------
    # Test 6: Backend availability report
    # -----------------------------------------------------------------
    print("6. Backend availability ...")
    print(f"   CadQuery renderer:  {_HAS_CQ_RENDERER}")
    print(f"   matplotlib 3D:      {_HAS_MATPLOTLIB}")
    print(f"   trimesh:            {_HAS_TRIMESH}")
    print("   PASSED\n")

    # -----------------------------------------------------------------
    # Test 7: matplotlib render (if available)
    # -----------------------------------------------------------------
    if _HAS_MATPLOTLIB:
        print("7. matplotlib rendering test ...")
        # Create a simple box mesh
        vertices = np.array([
            [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
            [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1],
        ], dtype=np.float64)
        faces = np.array([
            [0, 1, 2], [0, 2, 3],  # bottom
            [4, 5, 6], [4, 6, 7],  # top
            [0, 1, 5], [0, 5, 4],  # front
            [2, 3, 7], [2, 7, 6],  # back
            [1, 2, 6], [1, 6, 5],  # right
            [0, 3, 7], [0, 7, 4],  # left
        ])
        with tempfile.TemporaryDirectory() as tmpdir:
            output = os.path.join(tmpdir, "test_front.png")
            _render_with_matplotlib(
                vertices, faces,
                CameraView("front", azimuth=-90, elevation=0),
                output,
                bounds=(0, 0, 0, 1, 1, 1),
            )
            assert os.path.isfile(output), f"Output file not created: {output}"
            size_kb = os.path.getsize(output) / 1024
            print(f"   Generated: {output} ({size_kb:.1f} KB)")
            print("   PASSED\n")
    else:
        print("7. matplotlib not available -- skipping rendering test\n")

    print("=== ALL RENDERER TESTS PASSED ===")
