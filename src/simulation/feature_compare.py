"""Feature-aware per-operation comparison for subtractive CAD.

Routes:
  Approach 3: Feature-Aware Per-Operation Comparison
  Uses the ops trace / process plan to know what features exist and where,
  then compares each feature individually between a reference STEP and a
  candidate mesh. Produces localized per-feature feedback suitable for an
  LLM-driven iterative refinement loop.

Key functions:
  - extract_features_from_mesh  -- geometry-guided feature extraction
  - compare_features             -- match + measure per-feature pairs
  - generate_feature_feedback    -- LLM-friendly human-readable summary
  - compare_with_features        -- end-to-end pipeline entry point

Dependencies:
  trimesh, numpy, scipy          -- geometry processing
  CadQuery (via subcad.geometry) -- STEP import (NOT cascadio)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import numpy as np

try:
    import scipy.spatial as scipy_spatial
    _HAS_SCIPY = True
except ImportError:
    _HAS_SCIPY = False  # reserved for future use (e.g. KD-tree matching)

try:
    import trimesh
    _HAS_TRIMESH = True
except ImportError:
    _HAS_TRIMESH = False


# =============================================================================
#  Constants
# =============================================================================

# Face-normal angle thresholds (radians)
PLANAR_TOLERANCE = np.radians(5.0)      # faces within 5 deg = same plane
CYLINDRICAL_TOLERANCE = np.radians(15.0)
AXIS_ALIGNED_TOLERANCE = np.radians(5.0)

# Primary axis direction vectors
DIR_UP = np.array([0.0, 0.0, 1.0], dtype=np.float64)
DIR_DOWN = np.array([0.0, 0.0, -1.0], dtype=np.float64)
PRIMARY_DIRS = np.array([
    [1, 0, 0], [-1, 0, 0],
    [0, 1, 0], [0, -1, 0],
    [0, 0, 1], [0, 0, -1],
], dtype=np.float64)

# =============================================================================
#  Data class for feature specs parsed from ops trace
# =============================================================================


@dataclass
class _FeatureSpec:
    """Internal: feature expectation parsed from an ops-trace entry."""
    ftype: str                     # "pocket", "hole", "chamfer", "slot", "contour", etc.
    approx_center: list[float]     # [x, y, z] estimated center
    diameter: Optional[float] = None
    depth: Optional[float] = None
    width: Optional[float] = None
    length: Optional[float] = None
    radius: Optional[float] = None  # for fillets
    trace_index: int = 0            # original ops-trace list index
    label: str = ""                 # human label, e.g. "Pocket at (50,20)"


# =============================================================================
#  STEP loading (via CadQuery, not cascadio)
# =============================================================================


def _load_step_as_mesh(step_path: str) -> "trimesh.Trimesh":
    """Load a STEP file and return a trimesh mesh via CadQuery tessellation.

    Cascadio is NOT available, so we use CadQuery's importStep + tessellate.
    """
    if not _HAS_TRIMESH:
        raise RuntimeError("trimesh is required for feature comparison")

    try:
        from src.subcad.geometry import import_step, to_mesh
    except ImportError:
        from subcad.geometry import import_step, to_mesh

    shape = import_step(step_path)
    mesh = to_mesh(shape)
    if mesh is None:
        raise RuntimeError(f"Failed to tessellate STEP file: {step_path}")
    return mesh


# =============================================================================
#  Ops-trace parsing
# =============================================================================

def _parse_ops_trace_to_specs(ops_trace: list[dict]) -> list[_FeatureSpec]:
    """Convert an ops-trace list into a list of expected _FeatureSpec objects.

    The ops trace comes from CadQuery's operation graph. Each entry is a
    flattened call record. We extract the operation type and key parameters
    so we know *what* features to look for and *where*.
    """
    specs: list[_FeatureSpec] = []

    # CadQuery operation name -> feature-type mapping
    CQ_OP_TO_FEATURE: dict[str, str] = {
        "cutBlind": "pocket",
        "cutThruAll": "pocket",
        "cboreHole": "hole",
        "cskHole": "hole",
        "hole": "hole",
        "fillet": "fillet",
        "chamfer": "chamfer",
        "extrude": "boss",
        "pocket": "pocket",
        "circular_pocket": "hole",   # subCAD circular pocket ~= large hole
        "drill": "hole",
        "slot": "slot",
        "face_mill": "face",
        "contour": "contour",
        "tap": "hole",
        "threaded_hole": "hole",
        "countersink": "hole",
        "counterbore": "hole",
    }

    # Recognized parameter names that carry position / dimension info
    POSITION_KEYS = {"cx", "cy", "cz", "x", "y", "z", "center", "position"}
    DIAMETER_KEYS = {"diameter", "dia", "hole_diameter"}
    DEPTH_KEYS = {"depth", "blind_depth", "cut_depth"}
    WIDTH_KEYS = {"width", "w"}
    LENGTH_KEYS = {"length", "l"}
    RADIUS_KEYS = {"radius", "r", "fillet_radius", "corner_radius"}

    for i, entry in enumerate(ops_trace):
        if not isinstance(entry, dict):
            continue

        # Determine operation name
        op_name = ""
        for key in ("function_name", "op", "operation", "name", "type"):
            val = entry.get(key)
            if isinstance(val, str) and val:
                op_name = val
                break

        if not op_name:
            # Try function_path (e.g. "box.cutBlind")
            fp = entry.get("function_path", "")
            if isinstance(fp, str):
                parts = fp.split(".")
                for p in reversed(parts):
                    if p in CQ_OP_TO_FEATURE:
                        op_name = p
                        break

        if not op_name:
            continue

        ftype = CQ_OP_TO_FEATURE.get(op_name)
        if ftype is None:
            # Unknown op type, try to infer
            if "hole" in op_name.lower():
                ftype = "hole"
            elif "pocket" in op_name.lower():
                ftype = "pocket"
            elif "cut" in op_name.lower():
                ftype = "pocket"
            elif "fillet" in op_name.lower():
                ftype = "fillet"
            elif "chamfer" in op_name.lower():
                ftype = "chamfer"
            elif "extrude" in op_name.lower():
                ftype = "boss"
            elif "face_mill" in op_name.lower():
                ftype = "face"
            elif "slot" in op_name.lower():
                ftype = "slot"
            elif "contour" in op_name.lower():
                ftype = "contour"
            else:
                ftype = "unknown"

        # Extract parameters
        params = entry.get("params", entry.get("parameters", entry.get("args", {})))
        if isinstance(params, list):
            # Some traces store args as a positional list
            params_dict: dict = {}
            for j, val in enumerate(params):
                params_dict[f"arg{j}"] = val
            params = params_dict
        if not isinstance(params, dict):
            params = {}

        # Merge top-level keys that look like parameters (some traces put them flat)
        for k, v in entry.items():
            if k in ("function_name", "op", "operation", "name", "type",
                     "function_path", "params", "parameters", "args",
                     "lineno", "line", "chain_id"):
                continue
            if k not in params:
                params[k] = v

        # Extract numeric values
        def _get_num(keyset, default=0.0):
            for k in keyset:
                v = params.get(k)
                if v is not None:
                    try:
                        return float(v)
                    except (TypeError, ValueError):
                        pass
            return default

        def _get_pos(default=(0.0, 0.0, 0.0)):
            cx = _get_num({"cx", "x", "center_x"}, 0.0)
            cy = _get_num({"cy", "y", "center_y"}, 0.0)
            cz = _get_num({"cz", "z", "center_z"}, 0.0)
            # Try tuple params
            for k in ("center", "position", "origin", "location"):
                v = params.get(k)
                if isinstance(v, (list, tuple)) and len(v) >= 2:
                    cx = float(v[0])
                    cy = float(v[1])
                    if len(v) >= 3:
                        cz = float(v[2])
                    break
            return (cx, cy, cz)

        cx, cy, cz = _get_pos()
        diameter = _get_num(DIAMETER_KEYS)
        depth = _get_num(DEPTH_KEYS)
        width = _get_num(WIDTH_KEYS)
        length = _get_num(LENGTH_KEYS)
        radius = _get_num(RADIUS_KEYS)

        # Generate a human-readable label
        label_parts = [ftype.capitalize()]
        if cx != 0 or cy != 0:
            label_parts.append(f"at ({cx:.0f}, {cy:.0f})")
        label = " ".join(label_parts)

        spec = _FeatureSpec(
            ftype=ftype,
            approx_center=[cx, cy, cz],
            diameter=diameter if diameter > 0 else None,
            depth=depth if depth > 0 else None,
            width=width if width > 0 else None,
            length=length if length > 0 else None,
            radius=radius if radius > 0 else None,
            trace_index=i,
            label=label,
        )
        specs.append(spec)

    return specs


# =============================================================================
#  Mesh-based feature detection (no ops trace)
# =============================================================================

def _is_planar(face_normals: np.ndarray) -> bool:
    """Check if a set of face normals are all parallel (planar region)."""
    if len(face_normals) <= 1:
        return True
    mean_normal = face_normals.mean(axis=0)
    mean_normal /= np.linalg.norm(mean_normal) + 1e-12
    dots = np.abs(np.dot(face_normals, mean_normal))
    return np.all(dots > np.cos(PLANAR_TOLERANCE))


def _is_cylindrical(face_normals: np.ndarray) -> tuple[bool, Optional[np.ndarray]]:
    """Check if face normals are consistent with a cylindrical surface.

    Cylindrical face normals all lie in a plane perpendicular to the cylinder
    axis. Returns (is_cylindrical, estimated_axis).
    """
    if len(face_normals) < 6:
        return False, None
    # PCA on normals: cylinders have normals spanning a plane (two large
    # eigenvalues); planes have normals all parallel (one large eigenvalue).
    # eigh returns eigenvalues in ascending order: [lambda0, lambda1, lambda2].
    centered = face_normals - face_normals.mean(axis=0)
    cov = np.dot(centered.T, centered) / len(face_normals)
    eigenvalues, eigenvectors = np.linalg.eigh(cov)
    if len(eigenvalues) < 3:
        return False, None
    # lambda0 must be very small relative to lambda2 (one dead direction)
    # lambda1 must be large relative to lambda0 (normals span a plane, not a line)
    ratio_02 = eigenvalues[0] / (eigenvalues[2] + 1e-12)
    ratio_12 = eigenvalues[1] / (eigenvalues[0] + 1e-12)
    if ratio_02 < 0.12 and ratio_12 > 5.0:
        axis = eigenvectors[:, 0]
        return True, axis
    return False, None



def _estimate_cylinder_diameter(
    vertices: np.ndarray, axis: np.ndarray
) -> tuple[float, np.ndarray]:
    """Fit a cylinder to vertices. Returns (diameter, center_point).

    Projects vertices onto plane perpendicular to axis, then fits a circle.
    """
    axis = axis / (np.linalg.norm(axis) + 1e-12)
    # Project onto plane perpendicular to axis
    # For each vertex v, projected = v - dot(v - centroid, axis) * axis
    centroid = vertices.mean(axis=0)
    projected = vertices - np.outer(np.dot(vertices - centroid, axis), axis)
    # Fit circle in projected plane using least squares
    # Center is the mean of projected points in the plane
    proj_centroid_2d = projected.mean(axis=0)
    # Radius = mean distance from centroid to projected points
    distances = np.linalg.norm(projected - proj_centroid_2d, axis=1)
    radius = float(np.mean(distances))
    diameter = 2.0 * radius
    return diameter, proj_centroid_2d


def _estimate_pocket_dimensions(
    vertices: np.ndarray, face_normals: np.ndarray
) -> dict:
    """Estimate pocket dimensions (width, length, depth) from a face group."""
    if len(vertices) == 0:
        return {"width": 0.0, "length": 0.0, "depth": 0.0}

    bbox_min = vertices.min(axis=0)
    bbox_max = vertices.max(axis=0)
    extents = bbox_max - bbox_min
    return {
        "width": float(extents[1]),   # Y extent
        "length": float(extents[0]),  # X extent
        "depth": float(extents[2]),   # Z extent
    }


def _classify_face_group(
    mesh: "trimesh.Trimesh",
    face_indices: np.ndarray,
) -> dict:
    """Classify a connected face group and measure its properties.

    Returns a feature dict compatible with extract_features_from_mesh output.
    """
    normals = mesh.face_normals[face_indices]
    vertices = mesh.vertices[mesh.faces[face_indices]].reshape(-1, 3)
    unique_verts = np.unique(vertices, axis=0)

    is_cyl, axis = _is_cylindrical(normals)
    is_flat = _is_planar(normals)
    mean_normal = normals.mean(axis=0)
    mean_normal /= np.linalg.norm(mean_normal) + 1e-12

    bbox_min = unique_verts.min(axis=0).tolist()
    bbox_max = unique_verts.max(axis=0).tolist()
    center = unique_verts.mean(axis=0).tolist()

    result: dict = {
        "type": "unknown",
        "center": center,
        "bbox": [bbox_min, bbox_max],
        "diameter": None,
        "depth": None,
        "width": None,
        "length": None,
        "face_indices": face_indices.tolist(),
        "submesh": None,
    }

    # Z extent
    z_extent = bbox_max[2] - bbox_min[2]

    if is_cyl and axis is not None:
        # Cylindrical feature -> hole
        diam, ctr = _estimate_cylinder_diameter(unique_verts, axis)
        result["type"] = "hole"
        result["diameter"] = round(float(diam), 2)
        result["depth"] = round(float(z_extent), 2)
        result["center"] = ctr.tolist()

    elif is_flat:
        # Planar face group -- check orientation
        up_dot = abs(np.dot(mean_normal, DIR_UP))
        # Is the face aligned with ANY primary axis direction?
        max_primary = max(abs(np.dot(mean_normal, d)) for d in PRIMARY_DIRS)
        is_axis_aligned = max_primary > np.cos(AXIS_ALIGNED_TOLERANCE)

        if up_dot > np.cos(AXIS_ALIGNED_TOLERANCE):
            # Upward-facing planar region
            z_min = bbox_min[2]
            mesh_z_max = float(mesh.vertices[:, 2].max())
            mesh_z_min = float(mesh.vertices[:, 2].min())
            # True pocket floor: below top AND above absolute bottom
            if z_min < mesh_z_max - 1.0 and z_min > mesh_z_min + 1.0:
                dims = _estimate_pocket_dimensions(unique_verts, normals)
                result["type"] = "pocket"
                result["width"] = round(dims["width"], 2)
                result["length"] = round(dims["length"], 2)
                result["depth"] = round(float(mesh_z_max - z_min), 2)
            else:
                result["type"] = "face"
        elif is_axis_aligned:
            # Side or bottom face -- not a feature
            result["type"] = "face"
        elif up_dot < 0.3 and len(face_indices) < mesh.faces.shape[0] * 0.05:
            # Small non-axis-aligned angled region -> chamfer
            result["type"] = "chamfer"
        else:
            result["type"] = "face"
    else:
        # Non-planar, non-cylindrical
        if len(face_indices) < 10:
            result["type"] = "fillet"
        else:
            result["type"] = "contour"

    # Try to extract submesh
    try:
        result["submesh"] = mesh.submesh([face_indices], only_watertight=False,
                                         append=True)
    except Exception:
        result["submesh"] = None

    return result


def _region_grow_by_normal(
    mesh: "trimesh.Trimesh",
    angle_threshold_rad: float = 0.3,
    min_faces: int = 6,
) -> list[np.ndarray]:
    """Segment mesh into regions by normal-continuity region growing.

    Uses face adjacency: adjacent faces are merged if their normals differ
    by less than *angle_threshold_rad*. This naturally groups cylindrical
    walls, planar floors, and sharp edges into separate regions.
    """
    n_faces = mesh.faces.shape[0]
    if n_faces == 0:
        return []

    normals = mesh.face_normals
    adj = mesh.face_adjacency

    # Per-face adjacency list
    neighbors: list[list[int]] = [[] for _ in range(n_faces)]
    for a, b in adj:
        neighbors[a].append(b)
        neighbors[b].append(a)

    cos_threshold = np.cos(angle_threshold_rad)
    assigned = np.full(n_faces, -1, dtype=np.int32)
    regions: list[list[int]] = []

    for seed in range(n_faces):
        if assigned[seed] >= 0:
            continue
        # Start new region
        region_id = len(regions)
        regions.append([])
        stack = [seed]
        assigned[seed] = region_id
        seed_normal = normals[seed]

        while stack:
            face = stack.pop()
            regions[region_id].append(face)

            for nb in neighbors[face]:
                if assigned[nb] >= 0:
                    continue
                # Check if normals are similar
                if np.dot(normals[nb], normals[face]) > cos_threshold:
                    assigned[nb] = region_id
                    stack.append(nb)

    # Filter out tiny regions
    result = []
    for region in regions:
        if len(region) >= min_faces:
            result.append(np.array(region, dtype=np.int64))

    return result


def _region_grow_within_mask(
    mesh: "trimesh.Trimesh",
    face_mask: np.ndarray,
    angle_threshold_rad: float = 0.35,
    min_faces: int = 2,
) -> list[np.ndarray]:
    """Like _region_grow_by_normal but restricted to faces where mask is True.

    Adjacent faces are merged only if BOTH are in the mask AND their normals
    differ by less than angle_threshold_rad.
    """
    n_faces = mesh.faces.shape[0]
    normals = mesh.face_normals
    adj = mesh.face_adjacency

    neighbors: list[list[int]] = [[] for _ in range(n_faces)]
    for a, b in adj:
        neighbors[a].append(b)
        neighbors[b].append(a)

    cos_threshold = np.cos(angle_threshold_rad)
    assigned = np.full(n_faces, -1, dtype=np.int32)
    regions: list[list[int]] = []

    # Only seed from masked faces
    valid = np.where(face_mask)[0]
    for seed in valid:
        if assigned[seed] >= 0:
            continue
        region_id = len(regions)
        regions.append([])
        stack = [seed]
        assigned[seed] = region_id

        while stack:
            face = stack.pop()
            regions[region_id].append(face)
            for nb in neighbors[face]:
                if assigned[nb] >= 0:
                    continue
                if not face_mask[nb]:
                    continue
                if np.dot(normals[nb], normals[face]) > cos_threshold:
                    assigned[nb] = region_id
                    stack.append(nb)

    result = []
    for region in regions:
        if len(region) >= min_faces:
            result.append(np.array(region, dtype=np.int64))
    return result


def _detect_features_pure_geometry(mesh: "trimesh.Trimesh") -> list[dict]:
    """Detect features from mesh geometry alone (no ops trace).

    Strategy:
      1. Segment the mesh into regions by normal continuity (region growing).
      2. Classify each region.
      3. Filter to keep only "interesting" features (holes, pockets, chamfers).
    """
    if mesh.faces.shape[0] == 0:
        return []

    # 1. Region growing by normal continuity
    # NOTE: low min_faces accommodates coarse tessellations. Finer meshes
    # (e.g. tolerance < 0.05) give better feature extraction.
    regions = _region_grow_by_normal(mesh, angle_threshold_rad=0.3, min_faces=2)

    # 2. Classify each region
    mesh_z_max = float(mesh.vertices[:, 2].max())

    features: list[dict] = []
    for region_faces in regions:
        feat = _classify_face_group(mesh, region_faces)

        # Flag likely pocket floors: planar upward-facing region below top
        if feat["type"] == "face":
            region_normals = mesh.face_normals[region_faces]
            mean_n = region_normals.mean(axis=0)
            mean_n /= np.linalg.norm(mean_n) + 1e-12
            up_dot = abs(np.dot(mean_n, DIR_UP))
            region_z = mesh.vertices[mesh.faces[region_faces]].reshape(-1, 3)[:, 2]
            z_min = float(region_z.min())
            mesh_z_min = float(mesh.vertices[:, 2].min())
            if (up_dot > 0.9 and z_min < mesh_z_max - 1.0
                    and z_min > mesh_z_min + 1.0):
                # Upward-facing region below top AND above absolute bottom
                dims = _estimate_pocket_dimensions(
                    np.unique(mesh.vertices[mesh.faces[region_faces]].reshape(-1, 3), axis=0),
                    region_normals,
                )
                feat["type"] = "pocket"
                feat["width"] = round(dims["width"], 2)
                feat["length"] = round(dims["length"], 2)
                feat["depth"] = round(float(mesh_z_max - z_min), 2)

        if feat["type"] not in ("unknown", "face"):
            features.append(feat)

    # 3. Deduplicate: merge co-located holes (fragmented cylindrical surfaces)
    features = _deduplicate_features(features)

    return features


def _deduplicate_features(features: list[dict]) -> list[dict]:
    """Merge co-located features of the same type, and hole floors into holes.

    Fragmented cylindrical hole surfaces (wall, conical bottom, fillet
    edge, flat floor) detected as separate features are merged back into
    a single hole feature by center proximity.
    """
    if len(features) <= 1:
        return features

    n = len(features)
    merged_mask = np.zeros(n, dtype=bool)
    result: list[dict] = []

    for i in range(n):
        if merged_mask[i]:
            continue

        fi = features[i]
        ftype_i = fi.get("type", "")
        ci = np.array(fi["center"])
        dia_i = fi.get("diameter") or 5.0
        depth_i = fi.get("depth") or 5.0

        group = [i]
        for j in range(i + 1, n):
            if merged_mask[j]:
                continue
            fj = features[j]
            ftype_j = fj.get("type", "")
            cj = np.array(fj["center"])
            dist = float(np.linalg.norm(ci - cj))

            # Determine threshold and type compatibility
            threshold = 15.0

            if ftype_i == "hole":
                # Merge holes with same-type holes and pocket-type hole floors
                if ftype_j == "hole":
                    threshold = max(10.0, depth_i * 2, dia_i * 2)
                elif ftype_j == "pocket":
                    # Hole floor: XY centers nearly identical, pocket is small
                    p_width = fj.get("width") or 999
                    p_length = fj.get("length") or 999
                    xy_dist = float(np.linalg.norm(ci[:2] - cj[:2]))
                    pocket_fits_hole = (xy_dist < dia_i * 1.2 and
                                        p_width < dia_i * 2 and
                                        p_length < dia_i * 2)
                    if pocket_fits_hole:
                        threshold = max(10.0, depth_i * 2, dia_i * 2)
                    else:
                        continue

            if dist < threshold:
                group.append(j)
                merged_mask[j] = True

        if len(group) == 1:
            result.append(fi)
        else:
            # Merge: keep the feature with the largest diameter (hole) or best info
            merged = fi.copy()
            max_dia = fi.get("diameter") or 0
            all_faces = list(fi["face_indices"])
            best_type = ftype_i

            for idx in group[1:]:
                fj = features[idx]
                dia_j = fj.get("diameter") or 0
                if dia_j > max_dia:
                    max_dia = dia_j
                if fj.get("type") == "hole":
                    best_type = "hole"
                    if dia_j >= max_dia:
                        merged.update({k: v for k, v in fj.items()
                                       if v is not None})
                all_faces.extend(fj["face_indices"])

            merged["type"] = best_type
            merged["face_indices"] = all_faces
            merged["diameter"] = round(max_dia, 2) if max_dia > 0 else None
            # Recompute bbox from merged faces
            bboxes = []
            for idx in group:
                b = features[idx].get("bbox")
                if b and len(b) == 2:
                    bboxes.append(b)
            if bboxes:
                merged["bbox"] = [
                    [min(b[0][d] for b in bboxes) for d in range(3)],
                    [max(b[1][d] for b in bboxes) for d in range(3)],
                ]
            result.append(merged)
        merged_mask[i] = True

    return result


# =============================================================================
#  Ops-trace-guided feature extraction
# =============================================================================

def _find_hole_in_mesh(
    mesh: "trimesh.Trimesh",
    spec: _FeatureSpec,
    search_radius: float = 15.0,
) -> Optional[dict]:
    """Find a hole feature near spec position using cylindrical face detection."""
    spec_center = np.array(spec.approx_center, dtype=np.float64)

    # Find faces near the expected center
    face_centers = mesh.triangles_center
    dists = np.linalg.norm(face_centers - spec_center, axis=1)
    near_mask = dists < search_radius

    if not near_mask.any():
        # Try a radius based on the diameter if known
        if spec.diameter:
            search_radius = max(search_radius, spec.diameter * 2)
            near_mask = dists < search_radius
            if not near_mask.any():
                return None
        else:
            return None

    near_indices = np.where(near_mask)[0]

    # Use region-growing by normal continuity for better grouping
    # (simple connected-components would merge flat top + cylinder wall)
    near_subset = np.zeros(mesh.faces.shape[0], dtype=bool)
    near_subset[near_indices] = True
    groups = _region_grow_within_mask(mesh, near_subset, angle_threshold_rad=0.35)
    best_hole = None
    best_score = float("inf")

    for group in groups:
        if len(group) < 8:
            continue
        group_normals = mesh.face_normals[group]
        is_cyl, axis = _is_cylindrical(group_normals)
        if is_cyl and axis is not None:
            group_verticies = mesh.vertices[mesh.faces[group]].reshape(-1, 3)
            unique_v = np.unique(group_verticies, axis=0)
            diam, ctr = _estimate_cylinder_diameter(unique_v, axis)

            # Score: how well it matches the spec (XY plane)
            score = float(np.linalg.norm(ctr[:2] - np.array(spec_center[:2])))
            if spec.diameter:
                score += abs(diam - spec.diameter) * 2.0

            if score < best_score:
                best_score = score
                z_min = float(unique_v[:, 2].min())
                z_max = float(unique_v[:, 2].max())
                bbox_min = unique_v.min(axis=0).tolist()
                bbox_max = unique_v.max(axis=0).tolist()

                submesh = None
                try:
                    submesh = mesh.submesh([group], only_watertight=False,
                                           append=True)
                except Exception:
                    pass

                best_hole = {
                    "type": "hole",
                    "center": ctr.tolist(),
                    "bbox": [bbox_min, bbox_max],
                    "diameter": round(float(diam), 2),
                    "depth": round(float(z_max - z_min), 2),
                    "width": None,
                    "length": None,
                    "face_indices": group.tolist(),
                    "submesh": submesh,
                }

    return best_hole


def _find_pocket_in_mesh(
    mesh: "trimesh.Trimesh",
    spec: _FeatureSpec,
    search_radius: float = 20.0,
) -> Optional[dict]:
    """Find a pocket feature near spec position."""
    spec_center = np.array(spec.approx_center, dtype=np.float64)

    face_centers = mesh.triangles_center
    dists = np.linalg.norm(face_centers - spec_center, axis=1)
    near_mask = dists < search_radius

    if not near_mask.any():
        if spec.width and spec.length:
            search_radius = max(search_radius, max(spec.width, spec.length) * 1.5)
            near_mask = dists < search_radius
        if not near_mask.any():
            return None

    near_indices = np.where(near_mask)[0]
    near_subset = np.zeros(mesh.faces.shape[0], dtype=bool)
    near_subset[near_indices] = True
    groups = _region_grow_within_mask(mesh, near_subset, angle_threshold_rad=0.35)

    best_pocket = None
    best_score = float("inf")
    mesh_z_max = float(mesh.vertices[:, 2].max())

    for group in groups:
        if len(group) < 8:
            continue
        group_normals = mesh.face_normals[group]
        group_verts = mesh.vertices[mesh.faces[group]].reshape(-1, 3)
        unique_v = np.unique(group_verts, axis=0)

        z_min = float(unique_v[:, 2].min())
        z_max = float(unique_v[:, 2].max())

        # Pocket candidates: faces below the top surface
        if z_min >= mesh_z_max - 1.0:
            continue  # at top surface

        mean_normal = group_normals.mean(axis=0)
        mean_normal /= np.linalg.norm(mean_normal) + 1e-12

        # Check if mostly upward-facing (pocket floor)
        up_dot = abs(np.dot(mean_normal, DIR_UP))
        is_planar = _is_planar(group_normals)

        bbox_min = unique_v.min(axis=0).tolist()
        bbox_max = unique_v.max(axis=0).tolist()
        x_ext = bbox_max[0] - bbox_min[0]
        y_ext = bbox_max[1] - bbox_min[1]

        # Score: proximity + size match
        ctr = unique_v.mean(axis=0)
        score = float(np.linalg.norm(ctr - spec_center))
        if spec.width:
            score += abs(y_ext - spec.width)
        if spec.length:
            score += abs(x_ext - spec.length)

        if score < best_score:
            best_score = score

            submesh = None
            try:
                submesh = mesh.submesh([group], only_watertight=False,
                                       append=True)
            except Exception:
                pass

            best_pocket = {
                "type": "pocket",
                "center": ctr.tolist(),
                "bbox": [bbox_min, bbox_max],
                "diameter": None,
                "depth": round(float(mesh_z_max - z_min), 2),
                "width": round(float(y_ext), 2),
                "length": round(float(x_ext), 2),
                "face_indices": group.tolist(),
                "submesh": submesh,
            }

    return best_pocket


# =============================================================================
#  Public API: extract_features_from_mesh
# =============================================================================

def extract_features_from_mesh(
    mesh: "trimesh.Trimesh",
    ops_trace: Optional[list[dict]] = None,
) -> list[dict]:
    """Extract geometric features from a mesh, optionally guided by an ops trace.

    Each returned feature dict has keys:
        type:         str   -- "pocket", "hole", "boss", "chamfer", "contour", etc.
        center:       [x,y,z] -- estimated feature center
        bbox:         [[xmin,ymin,zmin], [xmax,ymax,zmax]]
        diameter:     float | None -- for holes
        depth:        float | None -- for pockets/holes
        width:        float | None -- for pockets/slots
        length:       float | None -- for slots
        face_indices: list[int] -- mesh face indices belonging to this feature
        submesh:      trimesh.Trimesh | None -- extracted sub-mesh
        label:        str   -- human-readable label

    Args:
        mesh: Input mesh (typically from STEP tessellation).
        ops_trace: Optional ops trace list from CadQuery execution.
                   Used to guide feature extraction when available.

    Returns:
        List of feature dicts sorted by type then center position.
    """
    if not _HAS_TRIMESH:
        raise RuntimeError("trimesh is required")

    if mesh.faces.shape[0] == 0:
        return []

    # Merge close vertices to improve topology
    try:
        mesh.merge_vertices()
    except Exception:
        pass

    features: list[dict] = []

    if ops_trace:
        # Ops-trace-guided extraction: parse trace, then search mesh near
        # each expected feature location
        specs = _parse_ops_trace_to_specs(ops_trace)
        features = _extract_features_from_specs(mesh, specs)
    else:
        # Pure geometric extraction
        features = _detect_features_pure_geometry(mesh)

    # Sort for deterministic output: by type, then by center x, y, z
    features.sort(key=lambda f: (
        f.get("type", ""),
        round(f.get("center", [0, 0, 0])[0], 1),
        round(f.get("center", [0, 0, 0])[1], 1),
        round(f.get("center", [0, 0, 0])[2], 1),
    ))

    return features


def _extract_features_from_specs(
    mesh: "trimesh.Trimesh", specs: list[_FeatureSpec]
) -> list[dict]:
    """Extract features from mesh using ops-trace-derived specs as guides."""
    features: list[dict] = []

    for spec in specs:
        if spec.ftype == "hole":
            feat = _find_hole_in_mesh(mesh, spec)
        elif spec.ftype in ("pocket", "slot", "face"):
            feat = _find_pocket_in_mesh(mesh, spec)
        elif spec.ftype == "chamfer":
            feat = _find_pocket_in_mesh(mesh, spec, search_radius=10.0)
            if feat:
                feat["type"] = "chamfer"
        else:
            # For boss, fillet, contour, unknown - use geometric detection
            # Skip if we can't find a good match
            continue

        if feat is not None:
            feat["label"] = spec.label
            features.append(feat)

    # Also add any geometrically detected features in regions NOT covered by
    # specs, to catch extra operations
    geom_features = _detect_features_pure_geometry(mesh)
    spec_centers = np.array([s.approx_center for s in specs], dtype=np.float64)

    for gf in geom_features:
        if len(spec_centers) == 0:
            features.append(gf)
            continue
        center = np.array(gf["center"], dtype=np.float64)
        dists = np.linalg.norm(spec_centers - center, axis=1)
        if dists.min() > 15.0:
            # Feature not covered by any spec - add it
            gf["label"] = f"Extra {gf['type']} at ({center[0]:.0f},{center[1]:.0f})"
            features.append(gf)

    return features


# =============================================================================
#  Feature matching & comparison
# =============================================================================

def _compute_feature_volume(feature: dict) -> float:
    """Compute approximate volume for a feature.

    Uses the feature's submesh if available, otherwise estimates from
    bounding-box dimensions.
    """
    submesh = feature.get("submesh")
    if submesh is not None and hasattr(submesh, "is_empty") and not submesh.is_empty:
        try:
            vol = float(submesh.volume)
            if vol > 0:
                return vol
        except Exception:
            pass

    # Estimate from bounding box dimensions (crude but zero-cost fallback)
    bbox = feature.get("bbox")
    if bbox and len(bbox) == 2:
        mn = np.array(bbox[0])
        mx = np.array(bbox[1])
        extents = mx - mn
        ftype = feature.get("type", "")
        if ftype == "hole":
            dia = feature.get("diameter") or extents[0]
            depth = feature.get("depth") or extents[2]
            return float(np.pi * (dia / 2) ** 2 * depth)
        elif ftype in ("pocket", "slot"):
            w = feature.get("width") or extents[1]
            l = feature.get("length") or extents[0]
            d = feature.get("depth") or extents[2]
            return float(w * l * d)
        else:
            return float(np.prod(extents))

    return 0.0


def _feature_distance(f1: dict, f2: dict) -> float:
    """Compute a match distance between two features (lower = better match)."""
    c1 = np.array(f1["center"])
    c2 = np.array(f2["center"])
    spatial_dist = float(np.linalg.norm(c1 - c2))

    # Type penalty
    t1, t2 = f1.get("type", ""), f2.get("type", "")
    type_penalty = 0.0 if t1 == t2 else 50.0

    # Size penalty for holes
    d1 = f1.get("diameter") or 0
    d2 = f2.get("diameter") or 0
    size_penalty = 0.0
    if d1 > 0 and d2 > 0:
        size_penalty = abs(d1 - d2) * 2.0

    return spatial_dist + type_penalty + size_penalty


def _match_features(
    ref_features: list[dict],
    cand_features: list[dict],
    max_distance: float = 25.0,
) -> tuple[list[tuple[int, int, float]], set[int], set[int]]:
    """Match reference features to candidate features.

    Returns:
        matches: list of (ref_idx, cand_idx, distance) for matched pairs
        unmatched_ref: set of ref indices not matched
        unmatched_cand: set of cand indices not matched
    """
    if not ref_features or not cand_features:
        return [], set(range(len(ref_features))), set(range(len(cand_features)))

    # Compute all pairwise distances
    n_ref = len(ref_features)
    n_cand = len(cand_features)

    # Build distance matrix
    distances = np.full((n_ref, n_cand), np.inf)
    for i in range(n_ref):
        for j in range(n_cand):
            d = _feature_distance(ref_features[i], cand_features[j])
            distances[i, j] = d

    # Greedy matching: pick best pair, remove both, repeat
    matches: list[tuple[int, int, float]] = []
    used_ref: set[int] = set()
    used_cand: set[int] = set()

    flat_dists = []
    for i in range(n_ref):
        for j in range(n_cand):
            flat_dists.append((distances[i, j], i, j))
    flat_dists.sort()

    for dist, i, j in flat_dists:
        if i in used_ref or j in used_cand:
            continue
        if dist > max_distance:
            break
        matches.append((i, j, dist))
        used_ref.add(i)
        used_cand.add(j)

    unmatched_ref = set(range(n_ref)) - used_ref
    unmatched_cand = set(range(n_cand)) - used_cand

    return matches, unmatched_ref, unmatched_cand


# =============================================================================
#  Public API: compare_features
# =============================================================================

def compare_features(
    ref_features: list[dict],
    cand_features: list[dict],
    tolerance_mm: float = 0.1,
) -> list[dict]:
    """Match and compare features between reference and candidate.

    Returns a list of per-feature comparison dicts, each with keys:
        ref_feature: dict        -- the matched reference feature
        cand_feature: dict       -- the matched candidate feature (or None)
        match_type: str          -- "exact", "shifted", "wrong_size", "missing", "extra"
        dimension_errors: dict   -- {dim_name: (expected, actual)}
        position_error: float    -- mm, center offset
        volume_error_pct: float  -- per-feature volume difference %
        status: str              -- "ok", "warning", "error"

    Args:
        ref_features: Features extracted from the reference (ground-truth) mesh.
        cand_features: Features extracted from the candidate (subCAD output) mesh.
        tolerance_mm: Tolerance for dimension matching (default 0.1 mm).

    Returns:
        List of per-feature comparison dicts.
    """
    matches, unmatched_ref, unmatched_cand = _match_features(
        ref_features, cand_features, max_distance=50.0
    )

    results: list[dict] = []

    # Process matched pairs
    for ref_idx, cand_idx, dist in matches:
        ref = ref_features[ref_idx]
        cand = cand_features[cand_idx]

        c_ref = np.array(ref["center"])
        c_cand = np.array(cand["center"])
        pos_error = float(np.linalg.norm(c_ref - c_cand))

        # Compare dimensions
        dim_errors: dict[str, tuple[float, float]] = {}
        for dim_key in ("diameter", "depth", "width", "length"):
            rv = ref.get(dim_key)
            cv = cand.get(dim_key)
            if rv is not None and cv is not None and rv > 0 and cv > 0:
                if abs(rv - cv) > tolerance_mm:
                    dim_errors[dim_key] = (float(rv), float(cv))

        # Determine match quality
        if not dim_errors and pos_error < tolerance_mm:
            match_type = "exact"
            status = "ok"
        elif dim_errors and pos_error < tolerance_mm * 10:
            match_type = "wrong_size"
            status = "error"
        elif not dim_errors and pos_error >= tolerance_mm:
            match_type = "shifted"
            status = "warning" if pos_error < tolerance_mm * 5 else "error"
        else:
            match_type = "wrong_size"
            status = "error"

        # Volume comparison
        ref_vol = _compute_feature_volume(ref)
        cand_vol = _compute_feature_volume(cand)
        if ref_vol > 0 and cand_vol > 0:
            vol_error_pct = round(abs(ref_vol - cand_vol) / ref_vol * 100.0, 1)
        elif ref_vol > 0 and cand_vol <= 0:
            vol_error_pct = 100.0
        else:
            vol_error_pct = 0.0

        results.append({
            "ref_feature": ref,
            "cand_feature": cand,
            "match_type": match_type,
            "dimension_errors": dim_errors,
            "position_error": round(pos_error, 3),
            "volume_error_pct": vol_error_pct,
            "status": status,
        })

    # Process unmatched reference features (missing in candidate)
    for ref_idx in unmatched_ref:
        ref = ref_features[ref_idx]
        results.append({
            "ref_feature": ref,
            "cand_feature": None,
            "match_type": "missing",
            "dimension_errors": {},
            "position_error": 0.0,
            "volume_error_pct": 100.0,
            "status": "error",
        })

    # Process unmatched candidate features (extra in candidate)
    for cand_idx in unmatched_cand:
        cand = cand_features[cand_idx]
        results.append({
            "ref_feature": None,
            "cand_feature": cand,
            "match_type": "extra",
            "dimension_errors": {},
            "position_error": 0.0,
            "volume_error_pct": 0.0,
            "status": "warning",
        })

    return results


# =============================================================================
#  Public API: generate_feature_feedback
# =============================================================================

def generate_feature_feedback(
    feature_comparisons: list[dict],
) -> str:
    """Format per-feature comparison into LLM-friendly feedback.

    Produces a human-readable string summarizing each feature's status,
    suitable for inclusion in an LLM iteration prompt.

    Example output::

        Hole at (30, 10): diameter 5.8mm instead of 6.0mm --- WRONG SIZE
        Pocket at (50, 20): depth 8.2mm instead of 10.0mm --- UNDERCUT
        Hole at (15, 40): MISSING --- not found in candidate
        Extra pocket at (80, 60) --- not in reference
        Chamfer at (10, 10): EXACT

    Args:
        feature_comparisons: Output from compare_features().

    Returns:
        Formatted feedback string.
    """
    if not feature_comparisons:
        return "  No features to compare."

    lines: list[str] = []
    line_num = 0

    for comp in feature_comparisons:
        line_num += 1
        mtype = comp["match_type"]
        status = comp["status"]

        if mtype == "missing":
            ref = comp.get("ref_feature", {})
            ftype = ref.get("type", "feature").capitalize()
            label = ref.get("label", "")
            center = ref.get("center", [0, 0, 0])
            loc_str = label or f"{ftype} at ({center[0]:.0f}, {center[1]:.0f})"
            lines.append(f"  {loc_str}: MISSING --- not found in candidate")

        elif mtype == "extra":
            cand = comp.get("cand_feature", {})
            ftype = cand.get("type", "feature").capitalize()
            center = cand.get("center", [0, 0, 0])
            lines.append(
                f"  EXTRA {ftype} at ({center[0]:.0f}, {center[1]:.0f}) --- not in reference"
            )

        elif mtype == "exact":
            ref = comp.get("ref_feature", {})
            label = ref.get("label", "")
            ftype = ref.get("type", "feature").capitalize()
            center = ref.get("center", [0, 0, 0])
            loc_str = label or f"{ftype} at ({center[0]:.0f}, {center[1]:.0f})"
            lines.append(f"  {loc_str}: OK --- matched within tolerance")

        elif mtype == "shifted":
            ref = comp.get("ref_feature", {})
            label = ref.get("label", "")
            ftype = ref.get("type", "feature").capitalize()
            center = ref.get("center", [0, 0, 0])
            pos_err = comp.get("position_error", 0)
            loc_str = label or f"{ftype} at ({center[0]:.0f}, {center[1]:.0f})"
            lines.append(
                f"  {loc_str}: POSITION SHIFTED by {pos_err:.2f}mm --- MISALIGNED"
            )

        elif mtype == "wrong_size":
            ref = comp.get("ref_feature", {})
            label = ref.get("label", "")
            ftype = ref.get("type", "feature").capitalize()
            center = ref.get("center", [0, 0, 0])
            loc_str = label or f"{ftype} at ({center[0]:.0f}, {center[1]:.0f})"

            dim_parts = []
            for dim_key, (expected, actual) in comp.get("dimension_errors", {}).items():
                direction = "UNDERSIZED" if actual < expected else "OVERSIZED"
                dim_parts.append(
                    f"{dim_key} {actual}mm instead of {expected}mm"
                )

            if dim_parts:
                lines.append(f"  {loc_str}: {'; '.join(dim_parts)} --- WRONG SIZE")
            else:
                lines.append(f"  {loc_str}: WRONG SIZE (volume mismatch)")

    header = f"\n=== Per-Feature Comparison ({len(feature_comparisons)} features) ===\n"
    return header + "\n".join(lines)


# =============================================================================
#  Public API: compare_with_features
# =============================================================================

def compare_with_features(
    ref_step_path: str,
    candidate_mesh: "trimesh.Trimesh",
    ops_trace: Optional[list[dict]] = None,
    tolerance_mm: float = 0.1,
) -> dict:
    """Run full feature-aware comparison between reference STEP and candidate mesh.

    Pipeline:
        1. Load reference STEP -> mesh
        2. Extract features from reference mesh (guided by ops_trace if provided)
        3. Extract features from candidate mesh (purely geometric, no ops_trace)
        4. Match and compare features
        5. Generate feedback and summary scores

    Args:
        ref_step_path: Path to the reference STEP file (ground truth).
        candidate_mesh: Mesh from the subCAD candidate execution.
        ops_trace: Optional ops trace from CadQuery (used to guide reference
                   feature extraction).
        tolerance_mm: Dimension comparison tolerance (default 0.1 mm).

    Returns:
        dict with keys:
            feature_comparisons: list[dict] -- from compare_features()
            feedback: str -- human-readable summary
            missing_features: int -- count of features in ref but not cand
            wrong_size_features: int -- count of wrong-size features
            extra_features: int -- count of features in cand but not ref
            ok_features: int -- count of exact matches
            score: float -- 0-100 quality score
    """
    # 1. Load reference mesh
    ref_mesh = _load_step_as_mesh(ref_step_path)

    # 2. Extract reference features (ops-trace-guided if available)
    ref_features = extract_features_from_mesh(ref_mesh, ops_trace=ops_trace)

    # 3. Extract candidate features (purely geometric)
    cand_features = extract_features_from_mesh(candidate_mesh, ops_trace=None)

    # 4. Match and compare
    comparisons = compare_features(ref_features, cand_features, tolerance_mm)

    # 5. Compute summary statistics
    missing_count = sum(1 for c in comparisons if c["match_type"] == "missing")
    wrong_size_count = sum(1 for c in comparisons if c["match_type"] == "wrong_size")
    extra_count = sum(1 for c in comparisons if c["match_type"] == "extra")
    ok_count = sum(1 for c in comparisons if c["match_type"] == "exact")
    shifted_count = sum(1 for c in comparisons if c["match_type"] == "shifted")

    # 6. Score: 0-100
    # Start at 100, subtract penalties
    score = 100.0
    score -= missing_count * 25.0        # missing features are severe
    score -= wrong_size_count * 15.0     # wrong size is moderate
    score -= extra_count * 10.0           # extra features are moderate
    score -= shifted_count * 5.0          # shifted is minor
    score = max(0.0, min(100.0, score))

    # 7. Generate feedback
    feedback = generate_feature_feedback(comparisons)

    # Add summary line
    summary_lines = [
        f"\nSummary: {ok_count} OK, {wrong_size_count} wrong size, "
        f"{shifted_count} shifted, {missing_count} missing, "
        f"{extra_count} extra | Score: {score:.0f}/100",
    ]
    feedback += "\n".join(summary_lines)

    return {
        "feature_comparisons": comparisons,
        "feedback": feedback,
        "missing_features": missing_count,
        "wrong_size_features": wrong_size_count,
        "extra_features": extra_count,
        "shifted_features": shifted_count,
        "ok_features": ok_count,
        "score": round(score, 1),
    }
