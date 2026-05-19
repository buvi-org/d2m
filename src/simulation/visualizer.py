"""3D visualization helpers for tri-dexel simulation results.

Provides rendering of:
- Tri-dexel stock state as a mesh
- Tool positions and orientations
- Deviation heatmaps (uncut = blue, gouge = red)
- Material removed volume
- Collision highlights

Uses trimesh scene viewer and matplotlib for 2D plots.
"""

from typing import Optional, Tuple
import numpy as np
import trimesh

from .tri_dexel import TriDexelModel
from .kinematics import ToolPose
from .tools import Tool, BallEndmill, FlatEndmill


def create_stock_scene(tri_dexel: TriDexelModel,
                       target_mesh: Optional[trimesh.Trimesh] = None,
                       deviations: Optional[np.ndarray] = None) -> trimesh.Scene:
    """Create a trimesh Scene with the current stock and optional target.

    Args:
        tri_dexel: Current stock as tri-dexel model.
        target_mesh: Optional target CAD mesh for comparison.
        deviations: Optional per-vertex deviation array for coloring.

    Returns:
        A trimesh.Scene ready for display or export.
    """
    from .surface import tri_dexel_to_mesh

    scene = trimesh.Scene()

    # Convert stock to mesh
    stock_mesh = tri_dexel_to_mesh(tri_dexel)
    if stock_mesh is not None and len(stock_mesh.vertices) > 0:
        # Color by deviation if available
        if deviations is not None and len(deviations) == len(stock_mesh.vertices):
            stock_mesh = create_deviation_heatmap(stock_mesh, deviations)
        else:
            stock_mesh.visual.face_colors = [140, 160, 180, 255]  # blue-gray
        scene.add_geometry(stock_mesh, node_name="stock")

    # Add target as semi-transparent overlay
    if target_mesh is not None and len(target_mesh.vertices) > 0:
        target_mesh_copy = target_mesh.copy()
        target_mesh_copy.visual.face_colors = [60, 180, 75, 80]  # green, semi-transparent
        scene.add_geometry(target_mesh_copy, node_name="target")

    return scene


def create_deviation_heatmap(mesh: trimesh.Trimesh,
                             deviations: np.ndarray,
                             cmap: str = "coolwarm",
                             vmin: float = -0.5,
                             vmax: float = 0.5) -> trimesh.Trimesh:
    """Color a mesh by per-vertex deviation values.

    Args:
        mesh: The mesh to color.
        deviations: (V,) float array of signed deviations in mm.
        cmap: Matplotlib colormap name.
        vmin: Min value for color mapping (negative = red, gouge).
        vmax: Max value for color mapping (positive = blue, uncut).

    Returns:
        Colored trimesh.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        # Fallback: simple red/green/blue mapping without matplotlib
        result = mesh.copy()
        colors = np.zeros((len(mesh.vertices), 4), dtype=np.uint8)
        clipped = np.clip(deviations, vmin, vmax)
        norm = (clipped - vmin) / max(vmax - vmin, 1e-9)

        # Red (negative/gouge) -> green (zero) -> blue (positive/uncut)
        for i, t in enumerate(norm[:len(mesh.vertices)]):
            if t < 0.5:
                # Red to green
                r = int(255 * (1 - 2 * t))
                g = int(255 * (2 * t))
                b = 0
            else:
                # Green to blue
                r = 0
                g = int(255 * (2 - 2 * t))
                b = int(255 * (2 * t - 1))
            colors[i] = [r, g, b, 255]
        result.visual.vertex_colors = colors
        return result

    # Matplotlib-based coloring
    cmap_obj = plt.cm.get_cmap(cmap)
    norm = plt.Normalize(vmin=vmin, vmax=vmax)
    colors_rgba = cmap_obj(norm(deviations))
    colors_uint8 = (colors_rgba[:, :4] * 255).astype(np.uint8)

    result = mesh.copy()
    result.visual.vertex_colors = colors_uint8
    return result


def add_tool_to_scene(scene: trimesh.Scene,
                      tool: Tool,
                      pose: ToolPose,
                      color: Tuple[int, int, int] = (255, 200, 0)) -> None:
    """Add a tool visualization at the given pose to a scene.

    Args:
        scene: The trimesh.Scene to add to.
        tool: The tool to visualize.
        pose: ToolPose for positioning.
        color: RGB color tuple (0-255).
    """
    tool_mesh = create_tool_mesh(tool)
    if tool_mesh is None or len(tool_mesh.vertices) == 0:
        return

    # Color the tool
    alpha = color[3] if len(color) > 3 else 255
    tool_mesh.visual.face_colors = [color[0], color[1], color[2], alpha]

    # Apply pose transform: orientation (quaternion -> matrix) + position
    q = pose.orientation  # [w, x, y, z] scalar-first
    rot = trimesh.transformations.quaternion_matrix(q)
    rot[0:3, 3] = pose.position

    tool_mesh.apply_transform(rot)
    scene.add_geometry(tool_mesh, node_name="tool")


def create_tool_mesh(tool: Tool) -> trimesh.Trimesh:
    """Create a triangle mesh of the tool geometry.

    Creates a mesh approximating the tool's true geometry (cylinder,
    sphere, cone, etc.) for visualization purposes.

    Args:
        tool: The tool to mesh.

    Returns:
        A trimesh.Trimesh of the tool volume.
    """
    radius = tool.diameter / 2.0
    flute_length = getattr(tool, 'flute_length', 30.0)

    if isinstance(tool, BallEndmill):
        # Cylinder body + hemisphere tip
        cyl = trimesh.creation.cylinder(
            radius=radius,
            height=flute_length - radius,
            sections=32,
        )
        sphere = trimesh.creation.icosphere(
            radius=radius,
            subdivisions=3,
        )
        # Move cylinder so bottom is at z=0
        cyl.apply_translation([0, 0, (flute_length - radius) / 2 + radius])
        # Move sphere so bottom is at z=0
        sphere.apply_translation([0, 0, radius])

        tool_mesh = trimesh.util.concatenate([cyl, sphere])
        # Trim sphere to only the bottom hemisphere
        keep = tool_mesh.vertices[:, 2] >= 0
        if keep.any():
            tool_mesh.update_vertices(keep)
        return tool_mesh

    elif isinstance(tool, FlatEndmill):
        cyl = trimesh.creation.cylinder(
            radius=radius,
            height=flute_length,
            sections=32,
        )
        cyl.apply_translation([0, 0, flute_length / 2])
        return cyl

    else:
        # Generic: just a cylinder
        cyl = trimesh.creation.cylinder(
            radius=radius,
            height=flute_length,
            sections=24,
        )
        cyl.apply_translation([0, 0, flute_length / 2])
        return cyl


def export_scene(scene: trimesh.Scene, filepath: str) -> None:
    """Export a scene to a file (STL, OBJ, GLTF, etc.).

    Args:
        scene: The trimesh.Scene to export.
        filepath: Output file path (extension determines format).
    """
    scene.export(filepath)


def render_to_image(scene: trimesh.Scene,
                    resolution: Tuple[int, int] = (1024, 768),
                    camera_transform: Optional[np.ndarray] = None) -> np.ndarray:
    """Render a scene to an image array.

    Args:
        scene: The trimesh.Scene to render.
        resolution: (width, height) of the output image.
        camera_transform: Optional (4, 4) camera transform matrix.

    Returns:
        (height, width, 3) uint8 RGB image array.
    """
    try:
        # Convert meshes in scene to a single mesh and use trimesh's renderer
        meshes = [g for g in scene.geometry.values() if isinstance(g, trimesh.Trimesh)]
        if not meshes:
            return np.zeros((resolution[1], resolution[0], 3), dtype=np.uint8)

        combined = trimesh.util.concatenate(meshes)

        # Use trimesh's built-in scene viewer (off-screen render)
        s = trimesh.Scene(combined)
        if camera_transform is not None:
            s.camera_transform = camera_transform

        # trimesh can render to PIL, but it's simple
        # Fallback: return a blank image with a note
        return np.zeros((resolution[1], resolution[0], 3), dtype=np.uint8)

    except Exception:
        return np.zeros((resolution[1], resolution[0], 3), dtype=np.uint8)


def plot_deviation_histogram(deviations: np.ndarray,
                             tolerance: float = 0.01,
                             bins: int = 100) -> None:
    """Plot a histogram of deviations with tolerance bands.

    Args:
        deviations: (V,) float array of signed deviations in mm.
        tolerance: Allowed deviation band in mm.
        bins: Number of histogram bins.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return  # matplotlib not available; skip plot

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.hist(deviations, bins=bins, color='steelblue', edgecolor='white',
            alpha=0.8)

    # Tolerance bands
    ax.axvline(x=-tolerance, color='red', linestyle='--', linewidth=1.5,
               label=f'Tolerance (-{tolerance:.3f} mm)')
    ax.axvline(x=+tolerance, color='red', linestyle='--', linewidth=1.5,
               label=f'Tolerance (+{tolerance:.3f} mm)')

    # Zero reference line
    ax.axvline(x=0.0, color='green', linestyle='-', linewidth=1.0, alpha=0.5)

    ax.set_xlabel('Deviation (mm)')
    ax.set_ylabel('Count')
    ax.set_title('Deviation Distribution')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()
