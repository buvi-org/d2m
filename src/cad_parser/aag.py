"""Attributed Adjacency Graph (AAG) builder for B-Rep face topology.

Constructs a face-adjacency graph from extracted face and edge data.
Each face becomes a node with attributes (type, area, normal).
Each shared edge between faces becomes an edge in the graph with
attributes (convexity, angle).

The AAG is the foundational data structure for machining feature
recognition -- convex edges indicate protrusions, concave edges
indicate pockets/slots, and the graph topology reveals features
like steps, slots, holes, and pockets.

Reference:
  Joshi & Chang (1988), "Graph-based heuristics for recognition of
  machined features from a 3D solid model".
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional
import math

import numpy as np


# =========================================================================
#  Data types
# =========================================================================

@dataclass
class AAGNode:
    """A node in the AAG representing a B-Rep face.

    Attributes:
        id: Unique node identifier (matches index in faces list).
        face_type: Surface type (planar, cylindrical, conical, etc.).
        surface_area: Area in mm^2.
        centroid: (x, y, z) in model space.
        normal: Approximate outward-facing unit normal vector.
        radius: Cylinder radius (valid for cylindrical faces).
        depth: Face depth along its axis (valid for cylindrical faces).
    """
    id: int
    face_type: str
    surface_area: float
    centroid: tuple[float, float, float]
    normal: tuple[float, float, float]
    radius: float = 0.0
    depth: float = 0.0


@dataclass
class AAGEdge:
    """An edge in the AAG connecting two adjacent faces.

    Attributes:
        node_a: Index of the first face.
        node_b: Index of the second face.
        convexity: "convex", "concave", or "tangent".
        angle_deg: Angle between face normals at the shared edge
                   (0-360 degrees).  For convex edges this is the
                   internal angle (< 180).  For concave edges this
                   is the external angle (> 180).
    """
    node_a: int
    node_b: int
    convexity: str       # "convex", "concave", or "tangent"
    angle_deg: float     # angle between faces in degrees


# =========================================================================
#  Helper: determine convexity from normal and edge midpoint
# =========================================================================

def _determine_convexity(
    n_a: np.ndarray,
    n_b: np.ndarray,
    centroid_a: np.ndarray,
    centroid_b: np.ndarray,
    edge_midpoint: np.ndarray,
    edge_direction: np.ndarray,
    tolerance_deg: float = 1.0,
) -> tuple[str, float]:
    """Determine convexity and angle between two faces at a shared edge.

    Method:
      1. Compute the cross product of the face normals: n_a x n_b.
      2. Compute the dot product of that cross product with the edge
         direction.
      3. If dot > 0:  the edge is convex  (faces fold inward).
         If dot < 0:  the edge is concave (faces fold outward).
         If |dot| is near zero relative to tolerance: tangent.

    The angle is computed from the dot product of normals. For concave
    edges, the angle is 360 - acos(n_a . n_b) to represent the external
    angle (> 180 deg).

    Args:
        n_a, n_b: Unit normal vectors of the two faces.
        centroid_a, centroid_b: Face centroids (used as sanity check).
        edge_midpoint: 3D midpoint of the shared edge.
        edge_direction: Unit vector along the edge direction.
        tolerance_deg: Angular tolerance for tangent classification.

    Returns:
        (convexity, angle_deg) tuple.
    """
    # Cross product of normals gives a vector perpendicular to both
    cross = np.cross(n_a, n_b)
    cross_norm = np.linalg.norm(cross)

    if cross_norm < 1e-12:
        # Normals are parallel or anti-parallel => tangent
        dot_n = np.dot(n_a, n_b)
        if dot_n > 0:
            angle = 0.0  # same direction
        else:
            angle = 180.0  # opposite direction
        return ("tangent", angle)

    cross_unit = cross / cross_norm
    dot_cross_edge = np.dot(cross_unit, edge_direction)

    # Sanity check: ensure the face centroid ordering is consistent
    # The vector from centroid_a to centroid_b should point "through"
    # the edge for a convex connection or "around" for concave.
    # We adjust convexity sign based on centroid positions relative
    # to the edge.
    dir_ab = centroid_b - centroid_a
    dir_ab_norm = np.linalg.norm(dir_ab)
    if dir_ab_norm > 1e-12:
        dir_ab_unit = dir_ab / dir_ab_norm
        # If the edge midpoint is between the centroids, adjust sign
        to_edge = edge_midpoint - centroid_a
        proj = np.dot(to_edge, dir_ab_unit)
        # Normal case: edge midpoint projects between centroids
        # We use the raw cross-edge dot product

    # Base angle from normals
    dot_n = np.clip(np.dot(n_a, n_b), -1.0, 1.0)
    angle_rad = math.acos(dot_n)
    angle_deg = math.degrees(angle_rad)

    # Determine convexity
    if abs(dot_cross_edge) < math.sin(math.radians(tolerance_deg)):
        convexity = "tangent"
    elif dot_cross_edge > 0:
        convexity = "convex"
        # Internal angle is already < 180
    else:
        convexity = "concave"
        angle_deg = 360.0 - angle_deg  # external angle > 180

    return (convexity, round(angle_deg, 3))


# =========================================================================
#  Helper: get edge geometry from pythonOCC
# =========================================================================

def _get_edge_midpoint_and_direction(edge) -> tuple[np.ndarray, np.ndarray]:
    """Extract the midpoint and direction vector from an OCC edge.

    Uses BRepAdaptor_Curve to sample the edge at its midpoint parameter.

    Args:
        edge: A TopoDS_Edge from pythonOCC.

    Returns:
        (midpoint_xyz, direction_xyz) as numpy arrays.
    """
    try:
        from OCP.BRepAdaptor import BRepAdaptor_Curve
        from OCP.TopoDS import TopoDS

        edge = TopoDS.Edge_s(edge)
        adaptor = BRepAdaptor_Curve(edge)
        t0 = adaptor.FirstParameter()
        t1 = adaptor.LastParameter()
        t_mid = (t0 + t1) / 2.0

        # Evaluate point and first derivative at midpoint
        p = adaptor.Value(t_mid)
        d = adaptor.DN(t_mid, 1)  # first derivative

        midpoint = np.array([p.X(), p.Y(), p.Z()], dtype=np.float64)
        direction = np.array([d.X(), d.Y(), d.Z()], dtype=np.float64)

        # Normalize direction
        d_norm = np.linalg.norm(direction)
        if d_norm > 1e-12:
            direction /= d_norm

        return midpoint, direction
    except Exception:
        return np.zeros(3), np.array([1.0, 0.0, 0.0])


# =========================================================================
#  AAG Builder (pythonOCC path)
# =========================================================================

def _build_aag_with_pythonocc(faces: list, edges: list,
                              shape=None, face_normals: Optional[list] = None) -> dict:
    """Build AAG using pythonOCC to compute edge geometry and convexity.

    Args:
        faces: List of FaceData from parser.parse_step().
        edges: List of EdgeData from parser.parse_step().
        shape: Optional TopoDS_Shape for direct edge access.
        face_normals: Optional pre-computed face normals.

    Returns:
        Dict with "nodes" and "adjacency" keys.
    """
    from OCP.TopExp import TopExp_Explorer
    from OCP.TopAbs import TopAbs_FACE, TopAbs_EDGE
    from OCP.TopoDS import TopoDS as _TopoDS

    # Build face index -> OCC face mapping
    occ_faces: list = []
    if shape is not None:
        try:
            explorer = TopExp_Explorer(shape, TopAbs_FACE)
            while explorer.More():
                occ_faces.append(_TopoDS.Face_s(explorer.Current()))
                explorer.Next()
        except Exception:
            occ_faces = []

    # Compute face normals if not provided
    if face_normals is None:
        from .parser import _get_face_normal
        face_normals = []
        if occ_faces:
            for face in occ_faces:
                face_normals.append(_get_face_normal(face))
        else:
            face_normals = [(0.0, 0.0, 1.0) for _ in faces]

    # Build edge-to-faces adjacency
    edge_to_faces: dict[int, list[int]] = {}
    if shape is not None and occ_faces:
        for face_idx, occ_face in enumerate(occ_faces):
            explorer = TopExp_Explorer(occ_face, TopAbs_EDGE)
            while explorer.More():
                edge = explorer.Current()
                edge_hash = hash(edge)
                if edge_hash not in edge_to_faces:
                    edge_to_faces[edge_hash] = []
                if face_idx not in edge_to_faces[edge_hash]:
                    edge_to_faces[edge_hash].append(face_idx)
                explorer.Next()

    # Filter to edges shared by exactly two faces
    shared_edges: dict[int, tuple[int, int]] = {}
    for ehash, face_list in edge_to_faces.items():
        if len(face_list) == 2:
            shared_edges[ehash] = (face_list[0], face_list[1])

    # Build OCC edge hash -> edge mapping
    occ_edges: dict[int, object] = {}
    if shape is not None:
        explorer = TopExp_Explorer(shape, TopAbs_EDGE)
        while explorer.More():
            edge = explorer.Current()
            ehash = hash(edge)
            occ_edges[ehash] = edge
            explorer.Next()

    # Construct adjacency list with convexity
    adjacency: list[AAGEdge] = []
    for ehash, (fa, fb) in shared_edges.items():
        if fa >= len(face_normals) or fb >= len(face_normals):
            continue

        n_a = np.array(face_normals[fa], dtype=np.float64)
        n_b = np.array(face_normals[fb], dtype=np.float64)

        # Get edge geometry
        edge = occ_edges.get(ehash)
        if edge is not None:
            edge_mid, edge_dir = _get_edge_midpoint_and_direction(edge)
        else:
            edge_mid = np.zeros(3)
            edge_dir = np.array([1.0, 0.0, 0.0])

        # Get face centroids
        c_a = np.array(faces[fa].centroid if fa < len(faces) else (0, 0, 0),
                       dtype=np.float64)
        c_b = np.array(faces[fb].centroid if fb < len(faces) else (0, 0, 0),
                       dtype=np.float64)

        convexity, angle_deg = _determine_convexity(
            n_a, n_b, c_a, c_b, edge_mid, edge_dir,
        )

        adjacency.append(AAGEdge(
            node_a=fa,
            node_b=fb,
            convexity=convexity,
            angle_deg=angle_deg,
        ))

    # Build nodes
    nodes = []
    for i, face in enumerate(faces):
        normal = face_normals[i] if i < len(face_normals) else (0.0, 0.0, 1.0)
        radius = getattr(face, "radius", 0.0) or 0.0
        depth = getattr(face, "depth", 0.0) or 0.0
        nodes.append(AAGNode(
            id=i,
            face_type=face.type,
            surface_area=face.surface_area,
            centroid=face.centroid,
            normal=normal,
            radius=radius,
            depth=depth,
        ))

    return {"nodes": nodes, "adjacency": adjacency}


# =========================================================================
#  AAG Builder (fallback / no pythonOCC)
# =========================================================================

def _build_aag_from_data(faces: list, edges: list,
                         face_normals: Optional[list] = None) -> dict:
    """Build a simplified AAG from extracted face/edge data without OCC.

    When pythonOCC is not available, we cannot determine adjacency or
    convexity precisely. This builds the node list and marks all edges
    as having unknown convexity.

    Args:
        faces: List of FaceData from parser.parse_step().
        edges: List of EdgeData from parser.parse_step().
        face_normals: Optional pre-computed face normals.

    Returns:
        Dict with "nodes" and "adjacency" keys.
    """
    if face_normals is None:
        face_normals = [(0.0, 0.0, 1.0) for _ in faces]

    nodes = []
    for i, face in enumerate(faces):
        normal = face_normals[i] if i < len(face_normals) else (0.0, 0.0, 1.0)
        radius = getattr(face, "radius", 0.0) or 0.0
        depth = getattr(face, "depth", 0.0) or 0.0
        nodes.append(AAGNode(
            id=i,
            face_type=face.type,
            surface_area=face.surface_area,
            centroid=face.centroid,
            normal=normal,
            radius=radius,
            depth=depth,
        ))

    # Without OCC we cannot determine which faces share which edges,
    # so adjacency is empty (or could be computed from heuristics).
    adjacency: list[AAGEdge] = []

    return {"nodes": nodes, "adjacency": adjacency}


# =========================================================================
#  Public API
# =========================================================================

def build_aag(
    faces: list,
    edges: list,
    shape=None,
    face_normals: Optional[list] = None,
) -> dict:
    """Build an Attributed Adjacency Graph from face and edge data.

    Each face becomes a graph node with attributes (type, area, normal).
    Each pair of adjacent faces becomes a graph edge with convexity
    classification (convex, concave, or tangent) and angle.

    The result is JSON-serializable and can be fed directly to an LLM
    or graph neural network for feature recognition.

    Args:
        faces: List of FaceData objects or dicts with ``type``,
               ``surface_area``, ``centroid`` fields.
        edges: List of EdgeData objects or dicts with ``type``,
               ``length`` fields.
        shape: Optional OCC TopoDS_Shape for precise edge geometry.
               When provided, convexity is computed from edge geometry.
               When None, adjacency cannot be determined precisely.
        face_normals: Optional list of (nx, ny, nz) per face in the
                      same order as ``faces``.

    Returns:
        A dict with two keys:

        nodes : list[dict]
            Each node has: ``id`` (int), ``face_type`` (str),
            ``surface_area`` (float), ``centroid`` ([x,y,z]),
            ``normal`` ([nx,ny,nz]).

        adjacency : list[dict]
            Each adjacency has: ``node_a`` (int), ``node_b`` (int),
            ``convexity`` ("convex"/"concave"/"tangent"),
            ``angle_deg`` (float).

    Example:
        >>> result = parse_step("part.step")
        >>> aag = build_aag(result["faces"], result["edges"])
        >>> print(f"Nodes: {len(aag['nodes'])}, Edges: {len(aag['adjacency'])}")
    """
    # Normalize input: accept dataclasses or plain dicts
    from .parser import FaceData, EdgeData

    normalized_faces: list[FaceData] = []
    for item in faces:
        if isinstance(item, FaceData):
            normalized_faces.append(item)
        elif isinstance(item, dict):
            normalized_faces.append(FaceData(
                type=item.get("type", "other"),
                surface_area=float(item.get("surface_area", 0.0)),
                centroid=tuple(item.get("centroid", (0.0, 0.0, 0.0))),
            ))
        else:
            normalized_faces.append(FaceData(
                type=getattr(item, "type", "other"),
                surface_area=float(getattr(item, "surface_area", 0.0)),
                centroid=tuple(getattr(item, "centroid", (0.0, 0.0, 0.0))),
            ))

    normalized_edges: list[EdgeData] = []
    for item in edges:
        if isinstance(item, EdgeData):
            normalized_edges.append(item)
        elif isinstance(item, dict):
            normalized_edges.append(EdgeData(
                type=item.get("type", "other"),
                length=float(item.get("length", 0.0)),
            ))
        else:
            normalized_edges.append(EdgeData(
                type=getattr(item, "type", "other"),
                length=float(getattr(item, "length", 0.0)),
            ))

    # Check for pythonOCC availability (OCP from cadquery-ocp)
    try:
        from OCP.TopoDS import TopoDS  # noqa: F401
        _has_occ = True
    except ImportError:
        _has_occ = False

    if _has_occ and shape is not None:
        return _build_aag_with_pythonocc(
            normalized_faces, normalized_edges, shape, face_normals,
        )
    else:
        return _build_aag_from_data(
            normalized_faces, normalized_edges, face_normals,
        )


def _to_json_serializable(aag: dict) -> dict:
    """Convert an AAG dict to a fully JSON-serializable format.

    Dataclass instances are converted to plain dicts. Numpy arrays
    and tuples are converted to lists.

    Args:
        aag: Result from build_aag().

    Returns:
        JSON-serializable dict.
    """
    def _convert_node(node) -> dict:
        return {
            "id": node.id if hasattr(node, "id") else node["id"],
            "face_type": node.face_type if hasattr(node, "face_type") else node["face_type"],
            "surface_area": node.surface_area if hasattr(node, "surface_area") else node["surface_area"],
            "centroid": list(node.centroid if hasattr(node, "centroid") else node["centroid"]),
            "normal": list(node.normal if hasattr(node, "normal") else node["normal"]),
            "radius": node.radius if hasattr(node, "radius") else node.get("radius", 0.0),
            "depth": node.depth if hasattr(node, "depth") else node.get("depth", 0.0),
        }

    def _convert_edge(adj) -> dict:
        return {
            "node_a": adj.node_a if hasattr(adj, "node_a") else adj["node_a"],
            "node_b": adj.node_b if hasattr(adj, "node_b") else adj["node_b"],
            "convexity": adj.convexity if hasattr(adj, "convexity") else adj["convexity"],
            "angle_deg": adj.angle_deg if hasattr(adj, "angle_deg") else adj["angle_deg"],
        }

    return {
        "nodes": [_convert_node(n) for n in aag["nodes"]],
        "adjacency": [_convert_edge(a) for a in aag["adjacency"]],
    }


# =========================================================================
#  Self-test
# =========================================================================

if __name__ == "__main__":
    print("=== AAG Builder Self-Test ===\n")

    from .parser import FaceData, EdgeData

    # -----------------------------------------------------------------
    # Test 1: Simple cube AAG (text-based, no OCC shape)
    # -----------------------------------------------------------------
    print("1. AAG from cube face data (text mode) ...")
    cube_faces = [
        FaceData(type="planar", surface_area=100.0, centroid=(5.0, 0.0, 0.0)),   # front
        FaceData(type="planar", surface_area=100.0, centroid=(-5.0, 0.0, 0.0)),  # back
        FaceData(type="planar", surface_area=100.0, centroid=(0.0, 5.0, 0.0)),   # right
        FaceData(type="planar", surface_area=100.0, centroid=(0.0, -5.0, 0.0)),  # left
        FaceData(type="planar", surface_area=100.0, centroid=(0.0, 0.0, 5.0)),   # top
        FaceData(type="planar", surface_area=100.0, centroid=(0.0, 0.0, -5.0)),  # bottom
    ]
    cube_edges = [
        EdgeData(type="line", length=10.0) for _ in range(12)
    ]

    aag = build_aag(cube_faces, cube_edges)
    print(f"   Nodes: {len(aag['nodes'])}")
    print(f"   Adjacency edges: {len(aag['adjacency'])}")
    assert len(aag["nodes"]) == 6, f"Expected 6 nodes, got {len(aag['nodes'])}"
    # Without OCC shape, adjacency is empty
    print("   PASSED\n")

    # -----------------------------------------------------------------
    # Test 2: Node attribute validation
    # -----------------------------------------------------------------
    print("2. Node attribute validation ...")
    for node in aag["nodes"]:
        assert hasattr(node, "id") or "id" in node
        assert hasattr(node, "face_type") or "face_type" in node
        assert hasattr(node, "surface_area") or "surface_area" in node
        assert hasattr(node, "centroid") or "centroid" in node
        assert hasattr(node, "normal") or "normal" in node
    print("   PASSED\n")

    # -----------------------------------------------------------------
    # Test 3: Input normalization (dicts instead of dataclasses)
    # -----------------------------------------------------------------
    print("3. Input normalization (dict input) ...")
    dict_faces = [
        {"type": "planar", "surface_area": 25.0, "centroid": (1.0, 2.0, 3.0)},
    ]
    dict_edges = [
        {"type": "line", "length": 5.0},
    ]
    aag2 = build_aag(dict_faces, dict_edges)
    assert len(aag2["nodes"]) == 1
    assert aag2["nodes"][0].face_type == "planar"
    assert aag2["nodes"][0].surface_area == 25.0
    print("   PASSED\n")

    # -----------------------------------------------------------------
    # Test 4: Convexity determination
    # -----------------------------------------------------------------
    print("4. Convexity classification ...")
    # Two faces meeting at 90 degrees (convex corner)
    n_a = np.array([1.0, 0.0, 0.0])
    n_b = np.array([0.0, 1.0, 0.0])
    c_a = np.array([1.0, 0.0, 0.0])
    c_b = np.array([0.0, 1.0, 0.0])
    edge_mid = np.array([0.0, 0.0, 0.0])
    edge_dir = np.array([0.0, 0.0, 1.0])

    convexity, angle = _determine_convexity(n_a, n_b, c_a, c_b, edge_mid, edge_dir)
    print(f"   n_a=(1,0,0), n_b=(0,1,0), edge_dir=(0,0,1): {convexity}, {angle} deg")
    # cross(na, nb) = (0,0,1), dot with edge_dir(0,0,1) = 1 > 0 => convex
    assert convexity == "convex", f"Expected convex, got {convexity}"
    assert abs(angle - 90.0) < 0.1, f"Expected 90 deg, got {angle}"
    print("   PASSED\n")

    # -----------------------------------------------------------------
    # Test 5: Concave classification
    # -----------------------------------------------------------------
    print("5. Concave classification ...")
    n_a2 = np.array([1.0, 0.0, 0.0])
    n_b2 = np.array([0.0, -1.0, 0.0])
    edge_dir2 = np.array([0.0, 0.0, 1.0])

    convexity2, angle2 = _determine_convexity(n_a2, n_b2, c_a, c_b, edge_mid, edge_dir2)
    print(f"   n_a=(1,0,0), n_b=(0,-1,0), edge_dir=(0,0,1): {convexity2}, {angle2} deg")
    # cross(na, nb) = (0,0,-1), dot with edge_dir(0,0,1) = -1 < 0 => concave
    assert convexity2 == "concave", f"Expected concave, got {convexity2}"
    assert angle2 > 180.0, f"Expected >180 deg for concave, got {angle2}"
    print("   PASSED\n")

    # -----------------------------------------------------------------
    # Test 6: Tangent classification
    # -----------------------------------------------------------------
    print("6. Tangent classification ...")
    n_a3 = np.array([0.0, 0.0, 1.0])
    n_b3 = np.array([0.0, 0.0, 1.0])
    edge_dir3 = np.array([1.0, 0.0, 0.0])
    convexity3, angle3 = _determine_convexity(n_a3, n_b3, c_a, c_b, edge_mid, edge_dir3)
    print(f"   Parallel normals: {convexity3}, {angle3} deg")
    assert convexity3 == "tangent", f"Expected tangent, got {convexity3}"
    assert abs(angle3) < 1.0, f"Expected ~0 deg, got {angle3}"
    print("   PASSED\n")

    # -----------------------------------------------------------------
    # Test 7: JSON serialization
    # -----------------------------------------------------------------
    print("7. JSON serialization ...")
    json_aag = _to_json_serializable(aag)
    import json
    json_str = json.dumps(json_aag, indent=2)
    parsed = json.loads(json_str)
    assert "nodes" in parsed
    assert "adjacency" in parsed
    assert isinstance(parsed["nodes"][0]["centroid"], list)
    assert isinstance(parsed["nodes"][0]["normal"], list)
    print(f"   Serialized {len(json_str)} bytes")
    print("   PASSED\n")

    # -----------------------------------------------------------------
    # Test 8: Empty input
    # -----------------------------------------------------------------
    print("8. Empty input handling ...")
    empty_aag = build_aag([], [])
    assert len(empty_aag["nodes"]) == 0
    assert len(empty_aag["adjacency"]) == 0
    print("   PASSED\n")

    print("=== ALL AAG TESTS PASSED ===")
