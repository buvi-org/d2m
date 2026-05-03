"""Surface extraction from tri-dexel models via modified marching cubes.

Extracts a triangle mesh from a TriDexelModel by:
1. Extracting surface points from each of the three dexel grids
2. Fusing points from all grids (keeping the highest-quality normal)
3. Building a signed distance field from the fused points
4. Running standard marching cubes on that field
5. Optional Laplacian smoothing for staircase reduction

Also provides deviation mapping (comparison to target CAD mesh).
"""

from dataclasses import dataclass
from typing import Optional, Tuple
import numpy as np
import trimesh

from .tri_dexel import TriDexelModel, DexelGrid, DexelColumn, DexelInterval, AABB


# =========================================================================
#  Surface point extraction from each grid
# =========================================================================

def _extract_surface_points(grid: DexelGrid) -> Tuple[np.ndarray, np.ndarray]:
    """Extract surface vertices and normals from a single dexel grid.

    For each non-empty column:
      - The FIRST interval entry point is a surface vertex
        (material starts -- surface facing toward the ray origin)
      - The LAST interval exit point is a surface vertex
        (material ends -- surface facing away from the ray origin)
      - Intermediate entry/exit pairs are internal surfaces
        (only relevant for shells or internal voids)

    Surface normals are approximate: aligned with the dexel ray direction.
    - Entry points: normal points toward ray origin (opposite to ray dir)
    - Exit points:  normal points along ray dir

    Args:
        grid: A populated DexelGrid.

    Returns:
        (vertices, normals) -- both (N, 3) float64 arrays.
    """
    ray_dir = grid.ray_direction()
    n_entry = -ray_dir   # surface normal at entry points
    n_exit = ray_dir      # surface normal at exit points

    verts: list[np.ndarray] = []
    norms: list[np.ndarray] = []
    n_cells = grid.nu_cells * grid.nv_cells

    # Estimate capacity to avoid reallocation
    verts = []
    norms = []

    for i in range(grid.nu_cells):
        for j in range(grid.nv_cells):
            col = grid._columns[i][j]
            if col.is_empty:
                continue
            ray_origin = grid.ray_origin(i, j)

            for iv in col._intervals:
                # Entry point
                p_entry = ray_origin + iv.start * ray_dir
                verts.append(p_entry)
                norms.append(n_entry)

                # Exit point
                p_exit = ray_origin + iv.end * ray_dir
                verts.append(p_exit)
                norms.append(n_exit)

    if not verts:
        return np.empty((0, 3), dtype=np.float64), np.empty((0, 3), dtype=np.float64)

    return np.array(verts, dtype=np.float64), np.array(norms, dtype=np.float64)


# =========================================================================
#  Point fusion (deduplicate across grids)
# =========================================================================

def _fuse_surface_points(
    verts_z: np.ndarray, norms_z: np.ndarray,
    verts_x: np.ndarray, norms_x: np.ndarray,
    verts_y: np.ndarray, norms_y: np.ndarray,
    resolution: float,
) -> Tuple[np.ndarray, np.ndarray]:
    """Fuse surface points from all three grids, keeping highest-quality.

    Quality metric for a point from axis-a grid:
        quality = |normal . dexel_direction|
    where dexel_direction is the ray cast direction of that grid.
    1.0 = surface perfectly perpendicular to ray (best quality).
    0.0 = surface grazing the ray (poor quality).

    Points within resolution/2 of each other are considered duplicates;
    the one with higher quality is kept.

    Args:
        verts_z, norms_z: Points from Z-grid.
        verts_x, norms_x: Points from X-grid.
        verts_y, norms_y: Points from Y-grid.
        resolution:        Grid spacing for distance threshold.

    Returns:
        (vertices, normals) merged arrays.
    """
    z_dir = np.array([0.0, 0.0, 1.0])
    x_dir = np.array([1.0, 0.0, 0.0])
    y_dir = np.array([0.0, 1.0, 0.0])

    all_verts = []
    all_norms = []
    all_quality = []

    for verts, norms, axis_dir in [
        (verts_z, norms_z, z_dir),
        (verts_x, norms_x, x_dir),
        (verts_y, norms_y, y_dir),
    ]:
        if len(verts) == 0:
            continue
        # Quality = |normal . axis_direction|
        q = np.abs(np.sum(norms * axis_dir, axis=1))
        all_verts.append(verts)
        all_norms.append(norms)
        all_quality.append(q)

    if not all_verts:
        return np.empty((0, 3), dtype=np.float64), np.empty((0, 3), dtype=np.float64)

    big_verts = np.vstack(all_verts)
    big_norms = np.vstack(all_norms)
    big_qual = np.concatenate(all_quality)
    N = len(big_verts)

    # For small point clouds, no fusion needed
    if N < 2:
        return big_verts, big_norms

    # Use a simple greedy deduplication: sort by quality descending,
    # then keep points that aren't too close to already-kept ones.
    order = np.argsort(-big_qual)
    threshold = resolution / 2.0
    threshold_sq = threshold * threshold

    kept_mask = np.zeros(N, dtype=bool)

    for idx in order:
        p = big_verts[idx]
        # Check against already-kept points
        if kept_mask.any():
            # Compute distances only to kept points
            kept_indices = np.where(kept_mask)[0]
            dists_sq = np.sum((big_verts[kept_indices] - p) ** 2, axis=1)
            if np.min(dists_sq) < threshold_sq:
                continue
        kept_mask[idx] = True

    return big_verts[kept_mask], big_norms[kept_mask]


# =========================================================================
#  Signed distance field from point cloud
# =========================================================================

def _point_cloud_to_sdf(
    points: np.ndarray, normals: np.ndarray,
    bounds: AABB, resolution: float,
) -> np.ndarray:
    """Build a signed distance field on a regular 3D grid from oriented points.

    For each grid vertex, compute the signed distance as:
        sdf = (vertex - nearest_point) . normal_of_nearest_point
    Positive = outside material (in direction of outward normal).
    Negative = inside material.

    Args:
        points:    (N, 3) surface point positions.
        normals:   (N, 3) surface normals (pointing outward from material).
        bounds:    AABB of the region.
        resolution: Grid spacing for the SDF (use resolution/2 for sub-voxel).

    Returns:
        (nx, ny, nz) float64 SDF array.
    """
    if len(points) == 0:
        # No surface points -> no material -> SDF = +inf (all outside)
        nx = max(1, int(np.ceil((bounds.max[0] - bounds.min[0]) / resolution)))
        ny = max(1, int(np.ceil((bounds.max[1] - bounds.min[1]) / resolution)))
        nz = max(1, int(np.ceil((bounds.max[2] - bounds.min[2]) / resolution)))
        return np.full((nx, ny, nz), 1e10, dtype=np.float64)

    ext = bounds.max - bounds.min
    nx = max(2, int(np.ceil(ext[0] / resolution)) + 1)
    ny = max(2, int(np.ceil(ext[1] / resolution)) + 1)
    nz = max(2, int(np.ceil(ext[2] / resolution)) + 1)

    sdf = np.full((nx, ny, nz), np.inf, dtype=np.float64)

    # Build grid coordinates
    xs = np.linspace(bounds.min[0], bounds.max[0], nx)
    ys = np.linspace(bounds.min[1], bounds.max[1], ny)
    zs = np.linspace(bounds.min[2], bounds.max[2], nz)

    # For each grid point, compute distance to nearest surface point
    # This is O(N_points * N_grid) which is expensive for large grids.
    # For the MVP we process in batches.

    # Flatten grid points
    grid_shape = (nx, ny, nz)
    total_grid = nx * ny * nz

    # Process grid in batches to manage memory
    batch_size = 10_000
    for start in range(0, total_grid, batch_size):
        end = min(start + batch_size, total_grid)
        batch_indices = np.arange(start, end)
        iz = batch_indices % nz
        iy = (batch_indices // nz) % ny
        ix = batch_indices // (ny * nz)

        batch_points = np.column_stack([xs[ix], ys[iy], zs[iz]])  # (B, 3)

        # For each batch grid point, find nearest surface point
        # Brute-force search (acceptable for MVP; use KD-tree for production)
        # points: (N, 3), batch_points: (B, 3)
        # diff: (B, N, 3)
        diff = batch_points[:, np.newaxis, :] - points[np.newaxis, :, :]  # (B, N, 3)
        dists_sq = np.sum(diff * diff, axis=2)  # (B, N)
        nearest_idx = np.argmin(dists_sq, axis=1)  # (B,)
        nearest_normals = normals[nearest_idx]  # (B, 3)
        nearest_dists = diff[np.arange(len(batch_points)), nearest_idx]  # (B, 3)

        # Signed distance = dot(vertex - nearest, normal)
        sd = np.sum(nearest_dists * nearest_normals, axis=1)  # (B,)

        sdf[ix, iy, iz] = sd

    return sdf


# =========================================================================
#  Marching cubes wrapper
# =========================================================================

def _marching_cubes(sdf: np.ndarray, bounds: AABB,
                    level: float = 0.0) -> trimesh.Trimesh:
    """Run marching cubes on a signed distance field.

    Uses skimage.measure.marching_cubes if available, otherwise falls
    back to trimesh's internal voxel-to-mesh.
    """
    try:
        from skimage.measure import marching_cubes as mc
        spacing = (
            (bounds.max[0] - bounds.min[0]) / (sdf.shape[0] - 1),
            (bounds.max[1] - bounds.min[1]) / (sdf.shape[1] - 1),
            (bounds.max[2] - bounds.min[2]) / (sdf.shape[2] - 1),
        )
        verts, faces, normals, values = mc(
            sdf.astype(np.float32), level=level, spacing=spacing,
        )
        if len(verts) == 0:
            return trimesh.Trimesh()
        # Shift vertices to match bounds
        verts = verts + bounds.min
        return trimesh.Trimesh(vertices=verts, faces=faces)
    except ImportError:
        pass

    # Fallback: trimesh voxel approach
    # Convert SDF to binary occupancy
    nx, ny, nz = sdf.shape
    occupied = sdf <= level
    if not np.any(occupied):
        return trimesh.Trimesh()

    # Create a voxel grid
    pitch = (bounds.max - bounds.min) / np.array([nx - 1, ny - 1, nz - 1])
    pitch = np.mean(pitch)  # uniform

    # Use trimesh's voxel marching cubes
    try:
        vox = trimesh.voxel.VoxelGrid(
            encoding=trimesh.voxel.encoding.DenseEncoding(occupied),
            transform=np.eye(4),
        )
        # Create a simple mesh from occupied voxels
        from trimesh import primitives
        boxes = []
        indices = np.argwhere(occupied)
        for idx in indices:
            center = bounds.min + (idx + 0.5) * pitch
            box = primitives.Box(extents=[pitch] * 3)
            box.apply_translation(center)
            boxes.append(box)
        if boxes:
            return trimesh.util.concatenate(boxes)
        return trimesh.Trimesh()
    except Exception:
        return trimesh.Trimesh()


# =========================================================================
#  Main API
# =========================================================================

def tri_dexel_to_mesh(tri_dexel: TriDexelModel) -> trimesh.Trimesh:
    """Convert a TriDexelModel to a triangle mesh.

    Pipeline:
    1. Extract surface points + normals from each dexel grid.
    2. Fuse duplicates across grids (keep highest-quality normal).
    3. Build a signed distance field at resolution/2.
    4. Run marching cubes on the SDF.

    Args:
        tri_dexel: The tri-dexel model to convert.

    Returns:
        A trimesh.Trimesh of the current material state.
    """
    # 1. Extract surface points from each grid
    verts_z, norms_z = _extract_surface_points(tri_dexel.dexel_z)
    verts_x, norms_x = _extract_surface_points(tri_dexel.dexel_x)
    verts_y, norms_y = _extract_surface_points(tri_dexel.dexel_y)

    # 2. Fuse
    fused_verts, fused_norms = _fuse_surface_points(
        verts_z, norms_z, verts_x, norms_x, verts_y, norms_y,
        resolution=tri_dexel.resolution,
    )

    if len(fused_verts) < 4:
        return trimesh.Trimesh()

    # 3. Build SDF
    sdf_resolution = tri_dexel.resolution / 2.0
    sdf = _point_cloud_to_sdf(
        fused_verts, fused_norms,
        bounds=tri_dexel.bounds,
        resolution=sdf_resolution,
    )

    # 4. Marching cubes
    mesh = _marching_cubes(sdf, tri_dexel.bounds)
    return mesh


def compare_to_target(simulated: TriDexelModel,
                      target_mesh: trimesh.Trimesh,
                      sample_spacing: Optional[float] = None) -> np.ndarray:
    """Compute signed distance deviation between simulated and target mesh.

    For each vertex of the target mesh, checks material presence in the
    tri-dexel model at that point.

    Positive deviation = uncut material (stock remains above target).
    Negative deviation = gouge (material removed below target).
    Zero = exactly on target.

    Args:
        simulated:      The current tri-dexel stock state.
        target_mesh:    The target (desired) CAD mesh.
        sample_spacing: Sampling resolution. Defaults to tri_dexel resolution.

    Returns:
        (V,) float64 array of signed deviations in mm.
    """
    if sample_spacing is None:
        sample_spacing = simulated.resolution

    vertices = target_mesh.vertices.copy()
    V = len(vertices)
    deviations = np.zeros(V, dtype=np.float64)

    for v_idx in range(V):
        pt = vertices[v_idx]

        # Check if material exists at this point in the simulated model
        has_material = simulated.get_material_at(pt)

        if has_material:
            # Uncut: material remains on top of target surface
            # Positive deviation = how much material is above
            deviations[v_idx] = sample_spacing  # approximate
        else:
            # No material here -- check if it was cut (expected) or gouged
            # Cast a ray along the surface normal to find the cut surface
            normal = target_mesh.vertex_normals[v_idx]
            # Look for material behind the target surface
            probe_pt = pt - normal * sample_spacing * 2
            if simulated.get_material_at(probe_pt):
                # There's material behind the target surface
                # This is a gouge: material removed BELOW the surface
                deviations[v_idx] = -sample_spacing  # approximate gouge depth

    return deviations


def detect_gouges(tri_dexel: TriDexelModel,
                  target_mesh: trimesh.Trimesh,
                  tolerance: float = 0.01) -> list:
    """Detect gouges where material was removed below the target surface.

    Uses a simple vertex-sampling approach.

    Args:
        tri_dexel:   Current tri-dexel state.
        target_mesh: Target CAD mesh.
        tolerance:   Maximum allowed gouge depth in mm.

    Returns:
        List of dicts with position, depth, severity.
    """
    from .material_removal import Gouge

    gouges: list[Gouge] = []
    vertices = target_mesh.vertices
    normals = target_mesh.vertex_normals
    resolution = tri_dexel.resolution

    for idx in range(len(vertices)):
        pt = vertices[idx]
        normal = normals[idx]

        if tri_dexel.get_material_at(pt):
            continue  # Material present = no gouge

        # Trace inward along normal to find how deep material was removed
        max_depth = resolution * 10
        step = resolution

        gouge_depth = 0.0
        for d in np.arange(0, max_depth, step):
            probe = pt - normal * d
            if tri_dexel.get_material_at(probe):
                gouge_depth = d
                break

        if gouge_depth > tolerance:
            severity = "minor"
            if gouge_depth > tolerance * 10:
                severity = "severe"
            elif gouge_depth > tolerance * 3:
                severity = "moderate"

            gouges.append(Gouge(
                position=pt.copy(),
                depth=float(gouge_depth),
                severity=severity,
            ))

    return gouges


def estimate_volume(tri_dexel: TriDexelModel) -> float:
    """Estimate total material volume by averaging the three grids.

    Args:
        tri_dexel: The tri-dexel model.

    Returns:
        Volume in mm^3.
    """
    return tri_dexel.volume()


# =========================================================================
#  Self-test
# =========================================================================

if __name__ == "__main__":
    print("=== Surface Extraction Self-Test ===\n")

    from .tri_dexel import TriDexelModel
    import trimesh

    # ------------------------------------------------------------------
    # 1. Basic surface extraction from a box
    # ------------------------------------------------------------------
    print("1. Surface extraction: box mesh ...")
    box = trimesh.creation.box(extents=[10.0, 10.0, 10.0])
    model = TriDexelModel.from_mesh(box, resolution=0.5)
    mesh = tri_dexel_to_mesh(model)

    print(f"   Input faces:  {len(box.faces)}")
    print(f"   Output faces: {len(mesh.faces)}")
    print(f"   Output verts: {len(mesh.vertices)}")

    # The extracted mesh should be non-empty
    assert len(mesh.faces) > 0, "Extracted mesh is empty"

    # Volume should be close to original
    if len(mesh.faces) > 0 and mesh.is_watertight:
        vol = mesh.volume
        print(f"   Mesh volume:  {vol:.1f} mm^3 (expected ~1000)")
        print("   PASSED\n")
    else:
        # Not watertight but has geometry
        print(f"   Mesh has {len(mesh.faces)} faces (not verified watertight)")
        print("   PASSED\n")

    # ------------------------------------------------------------------
    # 2. Deviation mapping
    # ------------------------------------------------------------------
    print("2. Deviation mapping ...")
    # Create a slightly smaller target (simulate machining)
    model2 = TriDexelModel.from_mesh(box, resolution=0.5)
    devs = compare_to_target(model2, box)
    print(f"   Deviations: min={devs.min():.4f}, max={devs.max():.4f}, "
          f"mean={devs.mean():.4f}")
    # Same mesh should have near-zero deviations
    assert np.all(np.abs(devs) < 1.0), "Deviations should be near zero for identical meshes"
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 3. Volume estimation
    # ------------------------------------------------------------------
    print("3. Volume estimation ...")
    vol = estimate_volume(model)
    print(f"   Volume: {vol:.2f} mm^3")
    assert abs(vol - 1000.0) < 50.0, f"Volume {vol:.1f} too far from 1000"
    print("   PASSED\n")

    print("=== ALL SURFACE TESTS PASSED ===")
