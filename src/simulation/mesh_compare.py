"""Localized mesh comparison for shape-quality feedback.

Provides per-vertex signed distance fields and Z-slice cross-sectional
comparison between a reference mesh and a candidate mesh. Designed to be
consumed by the agentic translator's convergence controller so the LLM
receives *where* deviation occurs, not just a global volume ratio.

Dependencies are deliberately limited to trimesh, numpy, and scipy.spatial
(cKDTree).  No rtree or trimesh.proximity required -- those pull in the
optional ``rtree`` package which may not be available.

Primary functions for external use:
    compare_meshes              -- convenience: run one or both comparison methods
    compute_signed_deviation    -- per-vertex SDF via cKDTree + vertex normals
    compute_z_slice_comparison  -- cross-sectional area comparison at Z heights
    generate_error_feedback     -- format deviation clusters as LLM-friendly text
    generate_slice_feedback     -- format Z-slice differences as LLM-friendly text
    cluster_error_regions       -- spatially group vertices with large deviation
"""

from __future__ import annotations

from typing import Optional

import numpy as np
import trimesh
from scipy.spatial import cKDTree

# From trimesh we only use mesh_plane (which does not require rtree).
from trimesh.intersections import mesh_plane


# =========================================================================
#  Approach 2: Per-Vertex Signed Distance Field
# =========================================================================

def compute_signed_deviation(
    reference_mesh: trimesh.Trimesh,
    candidate_mesh: trimesh.Trimesh,
    sample_distance: float = 0.5,
) -> dict:
    """Compute signed distance from reference-mesh vertices to candidate surface.

    Uses a cKDTree over candidate vertices for O(N log M) distance queries.
    The sign is determined by projecting (ref_vert - nearest_cand_vert) onto
    the vertex normal of the closest candidate vertex:

        dot > 0  -> reference vertex is OUTSIDE the candidate (overcut)
        dot < 0  -> reference vertex is INSIDE the candidate  (undercut)

    This avoids trimesh.proximity / rtree entirely.

    For large meshes (> 2000 reference vertices) a random subset is sampled
    and unsampled vertices are approximated by their nearest sampled neighbour.

    Args:
        reference_mesh: The reference (target / ground-truth) trimesh mesh.
        candidate_mesh: The candidate (generated / translated) trimesh mesh.
        sample_distance: Approximate spacing for surface sampling (mm).
            Lower values give finer feedback at higher computational cost.
            Ignored when fewer than 2000 reference vertices exist.

    Returns:
        dict with keys:
            mean_deviation:      float   -- mean signed distance (mm)
            max_overcut:         float   -- max positive deviation (overcut)
            max_undercut:        float   -- max negative deviation (undercut)
            rms_error:           float   -- root mean square error (mm)
            overcut_vertices:    int     -- count of overcut reference vertices
            undercut_vertices:   int     -- count of undercut reference vertices
            per_vertex_deviation: ndarray -- (N,) signed distance per vertex
    """
    ref_verts = np.asarray(reference_mesh.vertices, dtype=np.float64)
    cand_verts = np.asarray(candidate_mesh.vertices, dtype=np.float64)

    if len(cand_verts) == 0:
        big = float(1e9)
        return {
            "mean_deviation": big,
            "max_overcut": big,
            "max_undercut": big,
            "rms_error": big,
            "overcut_vertices": len(ref_verts),
            "undercut_vertices": 0,
            "per_vertex_deviation": np.full(len(ref_verts), big, dtype=np.float64),
        }

    # ---- Determine which reference vertices to query ------------------------
    n_ref = len(ref_verts)
    if n_ref > 2000:
        n_samples = max(2000, int(n_ref * sample_distance / 0.5))
        rng = np.random.default_rng(42)
        sampled_idx = rng.choice(n_ref, size=min(n_samples, n_ref), replace=False)
        sampled_idx.sort()
        query_verts = ref_verts[sampled_idx]
    else:
        sampled_idx = np.arange(n_ref, dtype=np.int64)
        query_verts = ref_verts

    # ---- cKDTree for nearest candidate vertex -------------------------------
    tree = cKDTree(cand_verts)
    distances, tree_idx = tree.query(query_verts, k=1)
    distances = np.asarray(distances, dtype=np.float64)
    tree_idx = np.asarray(tree_idx, dtype=np.int64)

    # ---- Sign via candidate vertex normals ----------------------------------
    # Get the vertex normals for each closest candidate vertex
    cand_normals = np.asarray(candidate_mesh.vertex_normals, dtype=np.float64)
    nn_normals = cand_normals[tree_idx]  # (Q, 3)

    # Vector from nearest candidate vertex to reference vertex
    nearest_cand = cand_verts[tree_idx]   # (Q, 3)
    vec = query_verts - nearest_cand      # (Q, 3)

    # Dot product: positive => ref is outside candidate (overcut)
    dot = np.sum(vec * nn_normals, axis=1)  # (Q,)

    signs = np.where(dot >= 0, 1.0, -1.0)
    per_vertex_sampled = distances * signs

    # ---- Map back to full reference vertex array -----------------------------
    per_vertex = np.zeros(n_ref, dtype=np.float64)

    if n_ref > 2000 and len(sampled_idx) < n_ref:
        per_vertex[sampled_idx] = per_vertex_sampled

        # Interpolate unsampled vertices from nearest sampled neighbour
        unsampled_mask = np.ones(n_ref, dtype=bool)
        unsampled_mask[sampled_idx] = False
        unsampled = np.where(unsampled_mask)[0]

        if len(unsampled) > 0:
            sampled_tree = cKDTree(ref_verts[sampled_idx])
            _, nn = sampled_tree.query(ref_verts[unsampled], k=1)
            per_vertex[unsampled] = per_vertex_sampled[nn]
    else:
        per_vertex = per_vertex_sampled

    # ---- Aggregate statistics ------------------------------------------------
    overcut_mask = per_vertex > 0
    undercut_mask = per_vertex < 0

    return {
        "mean_deviation": float(np.mean(per_vertex)),
        "max_overcut": float(np.max(per_vertex[overcut_mask]))
        if overcut_mask.any() else 0.0,
        "max_undercut": float(np.min(per_vertex[undercut_mask]))
        if undercut_mask.any() else 0.0,
        "rms_error": float(np.sqrt(np.mean(per_vertex ** 2))),
        "overcut_vertices": int(np.sum(overcut_mask)),
        "undercut_vertices": int(np.sum(undercut_mask)),
        "per_vertex_deviation": per_vertex,
    }


# =========================================================================
#  Cluster error regions  (flood-fill over mesh edge graph)
# =========================================================================

def cluster_error_regions(
    reference_mesh: trimesh.Trimesh,
    per_vertex_deviation: np.ndarray,
    deviation_threshold: float = 0.1,
    min_cluster_size: int = 10,
) -> list[dict]:
    """Spatially cluster vertices whose deviation exceeds a threshold.

    Uses mesh adjacency: two vertices belong to the same cluster if they
    share an edge (are referenced by the same face) AND both exceed the
    threshold in the same direction (both overcut or both undercut).

    Does **not** depend on scipy.ndimage (vertex grids are unstructured);
    instead walks the edge graph via BFS flood-fill.

    Args:
        reference_mesh: The reference mesh whose vertices were evaluated.
        per_vertex_deviation: (N,) signed distance per vertex.
        deviation_threshold: Absolute deviation (mm) above which a vertex
            is considered "deviant".
        min_cluster_size: Minimum number of vertices to report as a cluster.

    Returns:
        list of dicts, each describing one error cluster:
            center:         [x, y, z]   -- cluster centroid
            max_deviation:  float       -- worst absolute deviation in cluster
            mean_deviation: float       -- mean signed deviation in cluster
            vertex_count:   int         -- number of vertices in cluster
            type:           "overcut" | "undercut"
            bbox:           [[xmin,ymin,zmin], [xmax,ymax,zmax]]
    """
    verts = np.asarray(reference_mesh.vertices, dtype=np.float64)
    edges = reference_mesh.edges_unique
    n_verts = len(verts)

    # Identify deviant vertices
    overcut = per_vertex_deviation > deviation_threshold
    undercut = per_vertex_deviation < -deviation_threshold
    deviant_mask = overcut | undercut

    if not deviant_mask.any():
        return []

    # Build adjacency list restricted to deviant vertices
    adj: dict[int, list[int]] = {int(i): [] for i in np.where(deviant_mask)[0]}
    for e in edges:
        a, b = int(e[0]), int(e[1])
        if a in adj and b in adj:
            # Only connect same-type vertices
            if overcut[a] == overcut[b] and undercut[a] == undercut[b]:
                adj[a].append(b)
                adj[b].append(a)

    # BFS flood-fill
    visited: set[int] = set()
    clusters: list[dict] = []

    for seed in adj:
        if seed in visited:
            continue
        stack = [seed]
        component: list[int] = []
        while stack:
            v = stack.pop()
            if v in visited:
                continue
            visited.add(v)
            component.append(v)
            for nb in adj[v]:
                if nb not in visited:
                    stack.append(nb)

        if len(component) >= min_cluster_size:
            comp_arr = np.array(component, dtype=np.int64)
            comp_verts = verts[comp_arr]
            comp_dev = per_vertex_deviation[comp_arr]
            ctype = "overcut" if overcut[component[0]] else "undercut"

            clusters.append({
                "center": comp_verts.mean(axis=0).tolist(),
                "max_deviation": float(np.max(np.abs(comp_dev))),
                "mean_deviation": float(np.mean(comp_dev)),
                "vertex_count": len(component),
                "type": ctype,
                "bbox": [
                    comp_verts.min(axis=0).tolist(),
                    comp_verts.max(axis=0).tolist(),
                ],
            })

    clusters.sort(key=lambda c: c["max_deviation"], reverse=True)
    return clusters


def generate_error_feedback(
    deviation_result: dict,
    clusters: list[dict],
    max_clusters: int = 5,
) -> str:
    """Format deviation analysis into an LLM-friendly feedback string.

    Args:
        deviation_result: The dict returned by ``compute_signed_deviation``.
        clusters: Result of ``cluster_error_regions``.
        max_clusters: Limit the number of reported clusters.

    Returns:
        Human-readable text summarising the most significant deviation
        regions, suitable for inclusion in an LLM prompt.

    Example:
        Overcut of 1.2mm near (10, 20, -5) affecting 45 surface points.
        Undercut of 0.8mm near (30, 15, -8) affecting 32 surface points.
    """
    lines: list[str] = []
    lines.append(
        f"RMS deviation: {deviation_result['rms_error']:.3f} mm. "
        f"Overcut vertices: {deviation_result['overcut_vertices']}, "
        f"Undercut vertices: {deviation_result['undercut_vertices']}."
    )

    if not clusters:
        lines.append("No significant localised deviation clusters found.")
        return "\n".join(lines)

    for c in clusters[:max_clusters]:
        ctype = c["type"]
        cx, cy, cz = c["center"]
        direction = (
            "candidate has EXTRA material (undercut / not enough removal)"
            if ctype == "undercut"
            else "candidate is OUTSIDE reference (overcut / too much removed)"
        )
        lines.append(
            f"{ctype.upper()} cluster near ({cx:.1f}, {cy:.1f}, {cz:.1f}): "
            f"max={c['max_deviation']:.3f} mm, "
            f"mean={c['mean_deviation']:.3f} mm, "
            f"affects {c['vertex_count']} surface points. "
            f"({direction})"
        )

    if len(clusters) > max_clusters:
        lines.append(
            f"... and {len(clusters) - max_clusters} more deviation clusters."
        )

    return "\n".join(lines)


# =========================================================================
#  Approach 1: Cross-Sectional Z-Slicing
# =========================================================================

def _plane_mesh_intersection_area(
    mesh: trimesh.Trimesh,
    z: float,
) -> float:
    """Compute cross-sectional area of *mesh* at Z = *z*.

    Uses trimesh.intersections.mesh_plane (no rtree dependency) to get
    line segments, then chains them into closed polygons.
    """
    try:
        segments = mesh_plane(
            mesh,
            plane_normal=[0, 0, 1],
            plane_origin=[0, 0, z],
        )
    except Exception:
        return 0.0

    if segments is None or len(segments) == 0:
        return 0.0

    # segments is (N, 2, 3) -- N line segments, each with 2 endpoints in 3D.
    return _polygon_area_from_segments(segments)


def _polygon_area_from_segments(segments: np.ndarray) -> float:
    """Compute the area of (possibly multiple) polygons from line segments.

    Args:
        segments: (N, 2, 3) array where each row is a 3D line segment.

    Returns:
        Total unsigned 2D projected area (XY plane) in mm^2.
    """
    if len(segments) < 3:
        return 0.0

    # Drop Z and flatten to 2D -- all endpoints share the same Z so projection
    # is exact.
    seg2d = segments[:, :, :2]  # (N, 2, 2)

    # Build an undirected adjacency map from endpoint to connected endpoints.
    # We use a tolerance-aware approach: snap points that are very close.
    # Two endpoints are "the same vertex" if they are within epsilon.
    eps = 1e-6

    # Collect unique vertices by rounding
    flat = seg2d.reshape(-1, 2)
    # Round to epsilon grid to merge nearby points
    rounded = np.round(flat / eps) * eps
    _, inv, counts = np.unique(
        rounded, axis=0, return_inverse=True, return_counts=True
    )

    n_verts = len(np.unique(inv))
    # Build adjacency: for each segment, connect its two endpoint indices
    adj: dict[int, list[int]] = {i: [] for i in range(n_verts)}
    for s in seg2d:
        a, b = s
        # Find indices via the inverse mapping
        ra = np.round(a / eps) * eps
        rb = np.round(b / eps) * eps
        # Find which unique vertex this maps to
        dist_a = np.sum((np.unique(rounded, axis=0) - ra) ** 2, axis=1)
        dist_b = np.sum((np.unique(rounded, axis=0) - rb) ** 2, axis=1)
        ia = int(np.argmin(dist_a))
        ib = int(np.argmin(dist_b))
        if ia != ib:
            adj.setdefault(ia, []).append(ib)
            adj.setdefault(ib, []).append(ia)

    unique_verts = np.unique(rounded, axis=0)

    # Walk connected components
    visited = set()
    total_area = 0.0

    for seed in adj:
        if seed in visited:
            continue
        # Walk to build ordered polygon
        poly_idx = _trace_polygon(adj, seed, visited)
        if poly_idx is not None and len(poly_idx) >= 3:
            poly_pts = unique_verts[poly_idx]
            total_area += abs(_shoelace_area(poly_pts))

    return total_area


def _trace_polygon(
    adj: dict[int, list[int]],
    seed: int,
    visited: set,
) -> Optional[list[int]]:
    """Trace a closed polygon from an adjacency map starting at *seed*.

    Follows edges greedily: at each step the next vertex is an unvisited
    neighbour.  If the polygon is closed (returns to start) the trace is
    returned; otherwise returns None.

    Marks all traversed vertices as visited.

    Returns:
        Ordered list of vertex indices forming the polygon, or None.
    """
    if seed not in adj or len(adj[seed]) == 0:
        return None

    path = [seed]
    visited.add(seed)
    current = seed

    # We need at least degree 2 for a closed polygon
    while True:
        # Pick the first unvisited neighbour
        nbrs = adj.get(current, [])
        next_v = None
        for nb in nbrs:
            if nb not in visited:
                next_v = nb
                break
        # If no unvisited neighbour, check if we can close to start
        if next_v is None:
            if seed in nbrs and len(path) >= 3:
                return path  # Closed polygon
            else:
                # Dead end -- still mark visited and return what we have
                return path if len(path) >= 3 else None

        # Check if closing now would form a valid polygon
        if len(path) >= 3 and seed in adj.get(next_v, []):
            # We could close, but let's be greedy and continue unless degree is 2
            pass

        path.append(next_v)
        visited.add(next_v)
        current = next_v

        # Safety: avoid infinite loops
        if len(path) > len(adj) * 2:
            return None


def _shoelace_area(pts_2d: np.ndarray) -> float:
    """Shoelace formula for signed 2D polygon area.

    Args:
        pts_2d: (N, 2) array of ordered polygon vertices.

    Returns:
        Signed area (positive = CCW, negative = CW).
    """
    x = pts_2d[:, 0]
    y = pts_2d[:, 1]
    return 0.5 * float(np.dot(x, np.roll(y, 1)) - np.dot(np.roll(x, 1), y))


def compute_z_slice_comparison(
    reference_mesh: trimesh.Trimesh,
    candidate_mesh: trimesh.Trimesh,
    num_slices: int = 20,
) -> dict:
    """Slice both meshes at regular Z intervals and compare cross-sectional areas.

    For each Z height the meshes are intersected with a horizontal plane
    (Z = constant) and the area of each resulting cross-section polygon is
    measured. Differences indicate where along the vertical axis the
    candidate over-cuts or under-cuts.

    Uses ``trimesh.intersections.mesh_plane`` (no rtree dependency) for
    per-slice intersection, then chains the resulting line segments into
    closed polygons via adjacency walking.

    Args:
        reference_mesh: The reference (target) trimesh mesh.
        candidate_mesh: The candidate (translated) trimesh mesh.
        num_slices: Number of equally-spaced Z planes.

    Returns:
        dict with keys:
            z_values:       list[float]  -- Z heights of each slice
            ref_areas:      list[float]  -- cross-sectional area (ref)
            cand_areas:     list[float]  -- cross-sectional area (candidate)
            area_diffs:     list[float]  -- signed diff (candidate - ref)
            max_diff_z:     float        -- Z where max abs difference occurs
            max_diff_pct:   float        -- max area diff as % of ref area
            problem_slices: list[dict]   -- slices with |diff| > 5%
    """
    # Determine shared Z range
    ref_bounds = reference_mesh.bounds
    cand_bounds = candidate_mesh.bounds
    z_min = float(min(ref_bounds[0, 2], cand_bounds[0, 2]))
    z_max = float(max(ref_bounds[1, 2], cand_bounds[1, 2]))
    if z_max <= z_min:
        z_max = z_min + 1.0

    z_values = np.linspace(z_min, z_max, num_slices).tolist()

    ref_areas: list[float] = []
    cand_areas: list[float] = []
    area_diffs: list[float] = []
    max_diff_z = 0.0
    max_diff_pct = 0.0
    problem_slices: list[dict] = []

    for z in z_values:
        ra = _plane_mesh_intersection_area(reference_mesh, z)
        ca = _plane_mesh_intersection_area(candidate_mesh, z)

        ref_areas.append(ra)
        cand_areas.append(ca)
        diff = ca - ra
        area_diffs.append(diff)

        pct = (diff / ra * 100.0) if ra > 1e-9 else 0.0

        if abs(pct) > abs(max_diff_pct):
            max_diff_pct = pct
            max_diff_z = z

        if abs(pct) > 5.0:
            problem_slices.append({
                "z": float(z),
                "ref_area": ra,
                "cand_area": ca,
                "area_diff": diff,
                "pct_diff": pct,
                "direction": "MORE" if diff > 0 else "LESS",
            })

    return {
        "z_values": [float(z) for z in z_values],
        "ref_areas": ref_areas,
        "cand_areas": cand_areas,
        "area_diffs": area_diffs,
        "max_diff_z": float(max_diff_z),
        "max_diff_pct": float(max_diff_pct),
        "problem_slices": problem_slices,
    }


def generate_slice_feedback(
    slice_result: dict,
    threshold_pct: float = 5.0,
) -> str:
    """Format Z-slice comparison into an LLM-friendly feedback string.

    Args:
        slice_result: Dict returned by ``compute_z_slice_comparison``.
        threshold_pct: Minimum area difference (%) to report a slice.

    Returns:
        Human-readable text describing cross-section differences.

    Example:
        At Z=-5.0mm: candidate has 15% MORE area -- material uncut.
        At Z=-12.0mm: candidate has 8% LESS area -- overcut detected.
    """
    lines: list[str] = []

    max_z = slice_result.get("max_diff_z", 0)
    max_pct = slice_result.get("max_diff_pct", 0)
    lines.append(
        f"Max cross-section difference: {max_pct:+.1f}% at Z={max_z:.1f} mm."
    )

    problems = slice_result.get("problem_slices", [])
    if not problems:
        lines.append(
            "All Z-slices are within 5% cross-sectional area of reference."
        )
        return "\n".join(lines)

    lines.append(
        f"{'Z (mm)':>8s}  {'Ref Area':>10s}  {'Cand Area':>10s}  "
        f"{'Diff %':>8s}  Note"
    )
    lines.append("  " + "-" * 58)

    for ps in problems[:12]:
        note = (
            "material UN-CUT (undercut)"
            if ps["direction"] == "MORE"
            else "OVER-CUT detected"
        )
        lines.append(
            f"{ps['z']:8.1f}  {ps['ref_area']:10.2f}  "
            f"{ps['cand_area']:10.2f}  "
            f"{ps['pct_diff']:+7.1f}%  {note}"
        )

    if len(problems) > 12:
        lines.append(f"  ... and {len(problems) - 12} more problem slices.")

    return "\n".join(lines)


# =========================================================================
#  Composite score
# =========================================================================

def _compute_composite_score(
    sdf_result: dict | None,
    slice_result: dict | None,
) -> float:
    """Combine SDF and slice results into a single 0-100 quality score.

    100 = perfect match. Score decays with RMS error and max slice deviation.

    Args:
        sdf_result: Dict from ``compute_signed_deviation``, or None.
        slice_result: Dict from ``compute_z_slice_comparison``, or None.

    Returns:
        Float in [0, 100].
    """
    score = 100.0

    if sdf_result is not None:
        rms = sdf_result.get("rms_error", 0.0)
        score -= min(60.0, rms * 50.0)

    if slice_result is not None:
        max_pct = abs(slice_result.get("max_diff_pct", 0.0))
        score -= min(40.0, max_pct * 1.0)

    return max(0.0, min(100.0, round(score, 1)))


# =========================================================================
#  Combined convenience function
# =========================================================================

def compare_meshes(
    reference_mesh: trimesh.Trimesh,
    candidate_mesh: trimesh.Trimesh,
    methods: list[str] | None = None,
    **kwargs,
) -> dict:
    """Run mesh comparison methods and return combined results.

    This is the main entry point. It can run the signed-distance-field (SDF)
    or Z-slice (``"slice"``) methods, or both. Results are assembled into a
    single dict suitable for passing to the agentic translator's feedback
    builder.

    Args:
        reference_mesh: The reference (target / ground-truth) mesh.
        candidate_mesh: The candidate (generated / translated) mesh.
        methods: Which comparison methods to run. Options: ``"sdf"``,
            ``"slice"``. Pass None or omit to run both.
        **kwargs: Passed through to ``compute_signed_deviation``
            (``sample_distance``) and ``compute_z_slice_comparison``
            (``num_slices``).

    Returns:
        dict with keys:
            sdf:      dict | None     -- result of ``compute_signed_deviation``
            slice:    dict | None     -- result of ``compute_z_slice_comparison``
            feedback: str             -- combined human-readable feedback
            clusters: list[dict] | None -- error clusters from SDF
            score:    float           -- 0-100 composite quality score
    """
    if methods is None:
        methods = ["sdf", "slice"]

    sdf_result: dict | None = None
    slice_result: dict | None = None
    clusters: list[dict] | None = None
    feedback_parts: list[str] = []

    if "sdf" in methods:
        sdf_kwargs = {k: kwargs[k] for k in ("sample_distance",) if k in kwargs}
        sdf_result = compute_signed_deviation(
            reference_mesh, candidate_mesh, **sdf_kwargs
        )
        clusters = cluster_error_regions(
            reference_mesh, sdf_result["per_vertex_deviation"]
        )
        feedback_parts.append(generate_error_feedback(sdf_result, clusters))

    if "slice" in methods:
        slice_kwargs = {k: kwargs[k] for k in ("num_slices",) if k in kwargs}
        slice_result = compute_z_slice_comparison(
            reference_mesh, candidate_mesh, **slice_kwargs
        )
        feedback_parts.append(generate_slice_feedback(slice_result))

    feedback = "\n\n".join(feedback_parts) if feedback_parts else ""
    score = _compute_composite_score(sdf_result, slice_result)

    return {
        "sdf": sdf_result,
        "slice": slice_result,
        "feedback": feedback,
        "clusters": clusters,
        "score": score,
    }
