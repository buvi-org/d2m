"""Surface extraction from tri-dexel models via modified marching cubes.

Extracts a triangle mesh from a TriDexelModel by:
1. Extracting surface points from each of the three dexel grids
2. Fusing points from all grids (keeping the highest-quality normal)
3. Running marching cubes on the fused point field
4. Optional Laplacian smoothing for staircase reduction

Also provides deviation mapping (comparison to target CAD mesh).
"""

from typing import Optional, Tuple
import numpy as np
import trimesh

from .tri_dexel import TriDexelModel, DexelGrid, DexelColumn


def extract_surface_points_z(grid: DexelGrid) -> Tuple[np.ndarray, np.ndarray]:
    """Extract surface points from a Z-axis DexelGrid.

    For each column, material entry/exit points define surface vertices.
    Entry points have normals pointing toward -Z (top surface).
    Exit points have normals pointing toward +Z (bottom surface).

    Args:
        grid: DexelGrid with axis='z'.

    Returns:
        (vertices, normals) where vertices is (N, 3) and normals is (N, 3).
    """
    # Placeholder -- implement in Phase 5
    return np.empty((0, 3)), np.empty((0, 3))


def extract_surface_points_x(grid: DexelGrid) -> Tuple[np.ndarray, np.ndarray]:
    """Extract surface points from an X-axis DexelGrid.

    Args:
        grid: DexelGrid with axis='x'.

    Returns:
        (vertices, normals) where vertices is (N, 3) and normals is (N, 3).
    """
    # Placeholder -- implement in Phase 5
    return np.empty((0, 3)), np.empty((0, 3))


def extract_surface_points_y(grid: DexelGrid) -> Tuple[np.ndarray, np.ndarray]:
    """Extract surface points from a Y-axis DexelGrid.

    Args:
        grid: DexelGrid with axis='y'.

    Returns:
        (vertices, normals) where vertices is (N, 3) and normals is (N, 3).
    """
    # Placeholder -- implement in Phase 5
    return np.empty((0, 3)), np.empty((0, 3))


def fuse_surface_points(vertices_z: np.ndarray, normals_z: np.ndarray,
                        vertices_x: np.ndarray, normals_x: np.ndarray,
                        vertices_y: np.ndarray, normals_y: np.ndarray,
                        resolution: float) -> Tuple[np.ndarray, np.ndarray]:
    """Fuse surface points from all three grids.

    For nearby points (within resolution/2), keeps the one whose
    dexel direction is closest to the surface normal (highest quality).

    The quality metric for each point is:
        quality = |normal . dexel_direction|
    where dexel_direction is the axis the grid's rays were cast along.

    Args:
        vertices_z: (N_z, 3) points from Z-grid.
        normals_z: (N_z, 3) normals from Z-grid.
        vertices_x: (N_x, 3) points from X-grid.
        normals_x: (N_x, 3) normals from X-grid.
        vertices_y: (N_y, 3) points from Y-grid.
        normals_y: (N_y, 3) normals from Y-grid.
        resolution: Grid resolution for distance threshold.

    Returns:
        (vertices, normals) merged and filtered arrays.
    """
    # Placeholder -- implement in Phase 5
    all_verts = np.vstack([vertices_z, vertices_x, vertices_y]) if len(vertices_z) > 0 else np.empty((0, 3))
    all_norms = np.vstack([normals_z, normals_x, normals_y]) if len(normals_z) > 0 else np.empty((0, 3))
    return all_verts, all_norms


def tri_dexel_to_mesh(tri_dexel: TriDexelModel) -> trimesh.Trimesh:
    """Convert a TriDexelModel to a triangle mesh.

    Uses a modified marching cubes approach:
    1. Extract surface points from all three dexel grids
    2. Fuse points (keep highest-quality per region)
    3. Run marching cubes on the fused point field
    4. Apply Laplacian smoothing to reduce staircase artifacts

    Args:
        tri_dexel: The tri-dexel model to mesh.

    Returns:
        A trimesh.Trimesh of the current material state.
    """
    # Placeholder -- implement in Phase 5
    return trimesh.Trimesh()


def compare_to_target(simulated: TriDexelModel,
                      target_mesh: trimesh.Trimesh,
                      resolution: Optional[float] = None) -> np.ndarray:
    """Compute signed distance deviation between simulated and target.

    For each vertex of the target mesh:
    - Checks material presence in the tri-dexel at that point
    - Computes signed distance: positive = uncut (material remains above target),
      negative = gouge (material removed below target)

    Args:
        simulated: The current tri-dexel state.
        target_mesh: The target (desired) CAD mesh.
        resolution: Sampling resolution (default: tri_dexel resolution).

    Returns:
        (N_vertices,) float array of signed deviations in mm.
        Positive = too much material (uncut), negative = gouge.
    """
    # Placeholder -- implement in Phase 5
    return np.zeros(len(target_mesh.vertices))


def detect_gouges(tri_dexel: TriDexelModel,
                  target_mesh: trimesh.Trimesh,
                  tolerance: float = 0.01) -> list:
    """Detect gouges where material was removed below the target surface.

    Args:
        tri_dexel: The current tri-dexel state.
        target_mesh: The target CAD mesh.
        tolerance: Maximum allowed gouge depth in mm.

    Returns:
        List of Gouge namedtuples with position, depth, severity.
    """
    # Placeholder -- implement in Phase 5
    return []


def estimate_volume(tri_dexel: TriDexelModel) -> float:
    """Estimate the total material volume from all three grids.

    Averages the volume computed from each grid independently.

    Args:
        tri_dexel: The tri-dexel model.

    Returns:
        Volume in mm^3.
    """
    vol_z = sum(
        col.material_volume() * tri_dexel.resolution**2
        for row in tri_dexel.dexel_z._columns
        for col in row
    )
    vol_x = sum(
        col.material_volume() * tri_dexel.resolution**2
        for row in tri_dexel.dexel_x._columns
        for col in row
    )
    vol_y = sum(
        col.material_volume() * tri_dexel.resolution**2
        for row in tri_dexel.dexel_y._columns
        for col in row
    )
    count = 0
    total = 0.0
    if vol_z > 0:
        total += vol_z
        count += 1
    if vol_x > 0:
        total += vol_x
        count += 1
    if vol_y > 0:
        total += vol_y
        count += 1
    return total / count if count > 0 else 0.0
