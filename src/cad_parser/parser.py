"""STEP file parser for B-Rep geometry feature extraction.

Provides the primary function parse_step() that reads a STEP AP203/AP214
file and extracts B-Rep geometry features: faces, edges, vertices,
bounding dimensions, volume, and closed-shell status.

Uses pythonOCC for full B-Rep analysis if available; falls back to
text-based entity extraction otherwise.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional
import os
import re
import math

import numpy as np


# =========================================================================
#  Data types
# =========================================================================

@dataclass
class FaceData:
    """Extracted face information."""
    type: str                    # planar, cylindrical, conical, spherical, toroidal, spline, other
    surface_area: float          # mm^2
    centroid: tuple[float, float, float]  # (x, y, z) in model space
    radius: float = 0.0          # cylinder/hole radius (valid for cylindrical faces)
    depth: float = 0.0           # face depth along its axis


@dataclass
class EdgeData:
    """Extracted edge information."""
    type: str    # line, arc, spline, other
    length: float  # mm


# =========================================================================
#  Check for pythonOCC availability
# =========================================================================

_HAS_PYTHONOCC = False
try:
    from OCP.STEPControl import STEPControl_Reader
    from OCP.TopExp import TopExp_Explorer
    from OCP.TopAbs import (
        TopAbs_FACE, TopAbs_EDGE, TopAbs_VERTEX,
        TopAbs_SOLID, TopAbs_SHELL, TopAbs_COMPOUND,
        TopAbs_REVERSED,
    )
    from OCP.BRepGProp import BRepGProp
    from OCP.GProp import GProp_GProps
    from OCP.Bnd import Bnd_Box
    from OCP.BRepBndLib import BRepBndLib
    from OCP.BRepAdaptor import BRepAdaptor_Surface, BRepAdaptor_Curve
    from OCP.GeomAbs import (
        GeomAbs_Plane, GeomAbs_Cylinder, GeomAbs_Cone,
        GeomAbs_Sphere, GeomAbs_Torus,
        GeomAbs_BSplineSurface, GeomAbs_BezierSurface,
        GeomAbs_SurfaceOfRevolution, GeomAbs_SurfaceOfExtrusion,
        GeomAbs_Line, GeomAbs_Circle, GeomAbs_Ellipse,
        GeomAbs_Hyperbola, GeomAbs_Parabola,
        GeomAbs_BSplineCurve, GeomAbs_BezierCurve,
        GeomAbs_OffsetCurve, GeomAbs_OtherCurve,
    )
    from OCP.BRepCheck import BRepCheck
    from OCP.BRepTools import BRepTools
    from OCP.BRep import BRep_Tool
    from OCP.TopoDS import TopoDS
    from OCP.TopLoc import TopLoc_Location
    from OCP.ShapeAnalysis import ShapeAnalysis_Shell
    from OCP.gp import gp_Pnt
    from OCP.BRepClass3d import BRepClass3d

    # OCP API compat wrappers (OCP uses PascalCase static methods with _s suffix)
    def _brepgprop_SurfaceProperties(shape, props):
        BRepGProp.SurfaceProperties_s(shape, props)

    def _brepgprop_VolumeProperties(shape, props, *args, **kwargs):
        BRepGProp.VolumeProperties_s(shape, props)

    def _brepgprop_LinearProperties(shape, props):
        BRepGProp.LinearProperties_s(shape, props)

    def _brepbndlib_Add(shape, bbox):
        BRepBndLib.Add_s(shape, bbox)

    def _TopoDS_Face(shape):
        return TopoDS.Face_s(shape)

    def _TopoDS_Edge(shape):
        return TopoDS.Edge_s(shape)

    _HAS_PYTHONOCC = True
except ImportError:
    pass


# =========================================================================
#  Face-type classification helpers
# =========================================================================

_FACE_TYPE_MAP = {
    GeomAbs_Plane: "planar",
    GeomAbs_Cylinder: "cylindrical",
    GeomAbs_Cone: "conical",
    GeomAbs_Sphere: "spherical",
    GeomAbs_Torus: "toroidal",
    GeomAbs_BSplineSurface: "spline",
    GeomAbs_BezierSurface: "spline",
    GeomAbs_SurfaceOfRevolution: "spline",
    GeomAbs_SurfaceOfExtrusion: "spline",
} if _HAS_PYTHONOCC else {}

_EDGE_TYPE_MAP = {
    GeomAbs_Line: "line",
    GeomAbs_Circle: "arc",
    GeomAbs_Ellipse: "spline",
    GeomAbs_Hyperbola: "spline",
    GeomAbs_Parabola: "spline",
    GeomAbs_BSplineCurve: "spline",
    GeomAbs_BezierCurve: "spline",
    GeomAbs_OffsetCurve: "spline",
    GeomAbs_OtherCurve: "other",
} if _HAS_PYTHONOCC else {}


def _classify_face_type(face) -> str:
    """Classify a TopoDS_Face by its underlying surface type."""
    try:
        # Downcast TopoDS_Shape to TopoDS_Face if needed (OCP returns base type)
        face = _TopoDS_Face(face)
        adaptor = BRepAdaptor_Surface(face)
        surf_type = adaptor.GetType()
        return _FACE_TYPE_MAP.get(surf_type, "other")
    except Exception:
        return "other"


def _classify_edge_type(edge) -> str:
    """Classify a TopoDS_Edge by its underlying curve type."""
    try:
        edge = _TopoDS_Edge(edge)
        adaptor = BRepAdaptor_Curve(edge)
        curve_type = adaptor.GetType()
        return _EDGE_TYPE_MAP.get(curve_type, "other")
    except Exception:
        return "other"


# =========================================================================
#  Face property extraction
# =========================================================================

def _face_properties(face):
    """Compute area and centroid for a TopoDS_Face.

    Returns:
        (area_mm2, (cx, cy, cz))
    """
    props = GProp_GProps()
    _brepgprop_SurfaceProperties(face, props)
    area = props.Mass()
    center = props.CentreOfMass()
    centroid = (center.X(), center.Y(), center.Z())
    return area, centroid


def _get_cylinder_radius(face) -> float:
    """Extract the radius of a cylindrical face.

    Returns 0.0 if the face is not cylindrical or radius cannot be determined.
    """
    try:
        adaptor = BRepAdaptor_Surface(face)
        if adaptor.GetType() == GeomAbs_Cylinder:
            cylinder = adaptor.Cylinder()
            return cylinder.Radius()
    except Exception:
        pass
    return 0.0


def _get_face_depth(face, normal: tuple) -> float:
    """Estimate the depth of a face along its normal/extrusion direction.

    Uses the face triangulation to find extent along the axis.
    Falls back to a reasonable default.
    """
    try:
        adaptor = BRepAdaptor_Surface(face)
        surf_type = adaptor.GetType()
        if surf_type == GeomAbs_Cylinder:
            cylinder = adaptor.Cylinder()
            ax3 = cylinder.Position()
            axis_dir = np.array([ax3.Direction().X(), ax3.Direction().Y(), ax3.Direction().Z()])
        else:
            # Use the face normal as the axis
            axis_dir = np.array(normal, dtype=np.float64)

        # Get triangulation extent along the axis
        location = TopLoc_Location()
        triangulation = BRep_Tool.Triangulation_s(face, location)
        if triangulation is not None:
            nodes = triangulation.Nodes()
            n_nodes = triangulation.NbNodes()
            if n_nodes > 0:
                min_proj = float('inf')
                max_proj = float('-inf')
                for ii in range(1, n_nodes + 1):
                    p = nodes.Value(ii)
                    proj = np.dot(np.array([p.X(), p.Y(), p.Z()]), axis_dir)
                    min_proj = min(min_proj, proj)
                    max_proj = max(max_proj, proj)
                depth = max_proj - min_proj
                if depth > 0.01:
                    return round(depth, 3)
    except Exception:
        pass
    return 0.0


def _get_face_normal(face):
    """Get an approximate outward-facing normal for a TopoDS_Face.

    For planar faces, uses the plane's axis direction.
    For non-planar faces, averages normals from the face's triangulation.
    Falls back to (0, 0, 1) if nothing is available.

    Returns:
        (nx, ny, nz) unit vector tuple.
    """
    try:
        adaptor = BRepAdaptor_Surface(face)
        surf_type = adaptor.GetType()

        normal = np.array([0.0, 0.0, 1.0])

        if surf_type == GeomAbs_Plane:
            plane = adaptor.Plane()
            ax3 = plane.Position()
            direction = ax3.Direction()
            normal = np.array([direction.X(), direction.Y(), direction.Z()],
                              dtype=np.float64)
        else:
            # For non-planar faces, get triangulation and average normals
            location = TopLoc_Location()
            triangulation = BRep_Tool.Triangulation_s(face, location)

            if triangulation is not None:
                triangles = triangulation.Triangles()
                nodes = triangulation.Nodes()
                n_tri = triangulation.NbTriangles()
                accumulated = np.zeros(3, dtype=np.float64)
                for i in range(1, n_tri + 1):
                    tri = triangles.Value(i)
                    p1 = nodes.Value(tri.Value(1))
                    p2 = nodes.Value(tri.Value(2))
                    p3 = nodes.Value(tri.Value(3))
                    v1 = np.array([p2.X() - p1.X(), p2.Y() - p1.Y(), p2.Z() - p1.Z()],
                                  dtype=np.float64)
                    v2 = np.array([p3.X() - p1.X(), p3.Y() - p1.Y(), p3.Z() - p1.Z()],
                                  dtype=np.float64)
                    tri_n = np.cross(v1, v2)
                    nrm = np.linalg.norm(tri_n)
                    if nrm > 1e-12:
                        accumulated += tri_n / nrm

                nrm = np.linalg.norm(accumulated)
                if nrm > 1e-12:
                    normal = accumulated / nrm

        # Apply face orientation: if REVERSED (1), flip the normal
        if hasattr(face, 'Orientation') and face.Orientation() == TopAbs_REVERSED:
            normal = -normal

        return (float(normal[0]), float(normal[1]), float(normal[2]))
    except Exception:
        return (0.0, 0.0, 1.0)


# =========================================================================
#  Edge property extraction
# =========================================================================

def _edge_length(edge) -> float:
    """Compute the length of a TopoDS_Edge in mm."""
    props = GProp_GProps()
    _brepgprop_LinearProperties(edge, props)
    return props.Mass()


# =========================================================================
#  Bounding box extraction
# =========================================================================

def _compute_bounding_box(shape):
    """Compute the axis-aligned bounding box of a TopoDS_Shape.

    Returns:
        (xmin, ymin, zmin, xmax, ymax, zmax) all in mm.
    """
    bbox = Bnd_Box()
    _brepbndlib_Add(shape, bbox)
    xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
    return (xmin, ymin, zmin, xmax, ymax, zmax)


# =========================================================================
#  Volume estimation
# =========================================================================

def _compute_volume(shape) -> float:
    """Compute the volume of a TopoDS_Shape in mm^3.

    Iterates through solids in the shape tree. For a compound containing
    multiple solids, sums their volumes. For a shell, computes volume
    from an enclosed solid classifier.

    Returns:
        Volume in mm^3, or 0.0 if not a solid.
    """
    # Try direct volume properties first (works for single solids)
    try:
        props = GProp_GProps()
        _brepgprop_VolumeProperties(shape, props)
        vol = props.Mass()
        if vol > 0.0:
            return vol
    except Exception:
        pass

    # If direct computation yields 0, iterate sub-shapes
    try:
        explorer = TopExp_Explorer(shape, TopAbs_SOLID)
        total_vol = 0.0
        while explorer.More():
            solid = explorer.Current()
            try:
                props = GProp_GProps()
                _brepgprop_VolumeProperties(solid, props)
                total_vol += props.Mass()
            except Exception:
                pass
            explorer.Next()
        if total_vol > 0.0:
            return total_vol
    except Exception:
        pass

    return 0.0


# =========================================================================
#  Closed shell / watertight check
# =========================================================================

def _check_closed_shell(shape) -> bool:
    """Determine if the shape is a closed (watertight) shell.

    Uses BRepCheck_Analyzer for validity and ShapeAnalysis_Shell
    for edge connectivity checking.

    Returns:
        True if the shape forms a watertight solid.
    """
    warnings: list[str] = []

    try:
        # 1. Run the general B-Rep validity checker
        analyzer = BRepCheck.Analyzer_s(shape)
        if not analyzer.IsValid():
            return False
    except Exception:
        warnings.append("BRepCheck_Analyzer failed; assuming not watertight")
        return False

    # 2. For shells specifically, check edge connectivity
    #    A closed shell has every edge shared by exactly two faces with
    #    consistent orientation.
    try:
        shell_explorer = TopExp_Explorer(shape, TopAbs_SHELL)
        while shell_explorer.More():
            shell = shell_explorer.Current()
            shell_checker = ShapeAnalysis_Shell()
            shell_checker.LoadShells(shell)
            shell_checker.CheckOrientedShells(shell)
            if shell_checker.HasBadEdges():
                return False
            shell_explorer.Next()
    except Exception:
        # If we can't run the shell check, fall back to the analyzer result
        pass

    return True


# =========================================================================
#  Edge-to-faces mapping helper
# =========================================================================

def _edge_face_adjacency(shape):
    """Build mapping from edges to the faces they belong to.

    This is used by the AAG builder but computed here so we can
    include it in the parse result if needed.

    Returns:
        dict: edge_hash -> (face_index_a, face_index_b)
        where face indices are indices into the faces list.
        Only includes edges shared by exactly two faces.
    """
    edge_to_faces: dict[int, list[int]] = {}

    face_explorer = TopExp_Explorer(shape, TopAbs_FACE)
    face_idx = 0
    while face_explorer.More():
        face = face_explorer.Current()
        edge_explorer = TopExp_Explorer(face, TopAbs_EDGE)
        while edge_explorer.More():
            edge = edge_explorer.Current()
            edge_hash = hash(edge)
            if edge_hash not in edge_to_faces:
                edge_to_faces[edge_hash] = []
            edge_to_faces[edge_hash].append(face_idx)
            edge_explorer.Next()
        face_idx += 1
        face_explorer.Next()

    # Keep only edges shared by exactly two faces
    return {h: (indices[0], indices[1])
            for h, indices in edge_to_faces.items()
            if len(indices) == 2}


# =========================================================================
#  Main parse function (pythonOCC path)
# =========================================================================

def _parse_with_pythonocc(filepath: str) -> dict:
    """Parse a STEP file using pythonOCC for full B-Rep extraction.

    Args:
        filepath: Path to .step or .stp file.

    Returns:
        Structured dict with all geometry features.

    Raises:
        RuntimeError: If the file cannot be read or contains no valid geometry.
    """
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"STEP file not found: {filepath}")

    reader = STEPControl_Reader()
    status = reader.ReadFile(filepath)

    if status != 1:
        raise RuntimeError(
            f"STEPControl_Reader.ReadFile returned status {status}. "
            f"The file may be malformed or not a valid STEP file."
        )

    reader.TransferRoots()
    shape = reader.OneShape()

    if shape.IsNull():
        raise RuntimeError("STEP file parsed but produced a null shape (no geometry).")

    warnings: list[str] = []

    # -----------------------------------------------------------------
    #  Extract faces
    # -----------------------------------------------------------------
    faces: list[FaceData] = []
    try:
        explorer = TopExp_Explorer(shape, TopAbs_FACE)
        while explorer.More():
            face = _TopoDS_Face(explorer.Current())
            try:
                area, centroid = _face_properties(face)
                face_type = _classify_face_type(face)
                normal = _get_face_normal(face)
                radius = _get_cylinder_radius(face) if face_type == "cylindrical" else 0.0
                depth = _get_face_depth(face, normal) if face_type == "cylindrical" else 0.0
                # Discard faces with negligible area (parsing artifacts)
                if area > 1e-12:
                    faces.append(FaceData(
                        type=face_type,
                        surface_area=area,
                        centroid=centroid,
                        radius=radius,
                        depth=depth,
                    ))
            except Exception as exc:
                warnings.append(f"Could not extract face properties: {exc}")
            explorer.Next()
    except Exception as exc:
        warnings.append(f"Face extraction failed: {exc}")

    # -----------------------------------------------------------------
    #  Extract edges
    # -----------------------------------------------------------------
    edges: list[EdgeData] = []
    try:
        explorer = TopExp_Explorer(shape, TopAbs_EDGE)
        while explorer.More():
            edge = _TopoDS_Edge(explorer.Current())
            try:
                length = _edge_length(edge)
                edge_type = _classify_edge_type(edge)
                if length > 1e-12:
                    edges.append(EdgeData(
                        type=edge_type,
                        length=length,
                    ))
            except Exception as exc:
                warnings.append(f"Could not extract edge properties: {exc}")
            explorer.Next()
    except Exception as exc:
        warnings.append(f"Edge extraction failed: {exc}")

    # -----------------------------------------------------------------
    #  Count vertices
    # -----------------------------------------------------------------
    vertices_count = 0
    try:
        explorer = TopExp_Explorer(shape, TopAbs_VERTEX)
        while explorer.More():
            vertices_count += 1
            explorer.Next()
    except Exception as exc:
        warnings.append(f"Vertex counting failed: {exc}")

    # -----------------------------------------------------------------
    #  Bounding box and overall dimensions
    # -----------------------------------------------------------------
    try:
        xmin, ymin, zmin, xmax, ymax, zmax = _compute_bounding_box(shape)
        dim_x = xmax - xmin
        dim_y = ymax - ymin
        dim_z = zmax - zmin
        bounding_box = (xmin, ymin, zmin, xmax, ymax, zmax)
        overall_dimensions = (dim_x, dim_y, dim_z)
    except Exception as exc:
        warnings.append(f"Bounding box computation failed: {exc}")
        bounding_box = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        overall_dimensions = (0.0, 0.0, 0.0)

    # -----------------------------------------------------------------
    #  Volume
    # -----------------------------------------------------------------
    try:
        volume = _compute_volume(shape)
    except Exception as exc:
        warnings.append(f"Volume computation failed: {exc}")
        volume = 0.0

    # -----------------------------------------------------------------
    #  Watertight check
    # -----------------------------------------------------------------
    try:
        is_closed = _check_closed_shell(shape)
    except Exception as exc:
        warnings.append(f"Closed-shell check failed: {exc}")
        is_closed = False

    return {
        "faces": faces,
        "edges": edges,
        "vertices_count": vertices_count,
        "bounding_box": bounding_box,
        "overall_dimensions": overall_dimensions,
        "volume": volume,
        "is_closed_shell": is_closed,
        "parse_warnings": warnings,
        "parser": "pythonOCC",
        "_occ_shape": shape,
    }


# =========================================================================
#  Text-based fallback parser
# =========================================================================

# STEP entity patterns (ISO 10303-21)
_RE_CARTESIAN_POINT = re.compile(
    r"#\d+\s*=\s*CARTESIAN_POINT\s*\(.*?\)",
    re.IGNORECASE | re.DOTALL,
)
_RE_COORDINATES = re.compile(r"\(\s*'[^']*'?\s*,\s*\(([^)]+)\)\s*\)")

_RE_CLOSED_SHELL = re.compile(
    r"CLOSED_SHELL\s*\(|MANIFOLD_SOLID_BREP\s*\(|MANIFOLD_SURFACE_SHAPE_REPRESENTATION",
    re.IGNORECASE,
)

_RE_ADVANCED_FACE = re.compile(
    r"ADVANCED_FACE\s*\(|FACE_OUTER_BOUND\s*\(|FACE_BOUND\s*\(",
    re.IGNORECASE,
)

_RE_PLANE = re.compile(r"PLANE\s*\(", re.IGNORECASE)
_RE_CYLINDRICAL = re.compile(r"CYLINDRICAL_SURFACE\s*\(", re.IGNORECASE)
_RE_CONICAL = re.compile(r"CONICAL_SURFACE\s*\(", re.IGNORECASE)
_RE_SPHERICAL = re.compile(r"SPHERICAL_SURFACE\s*\(", re.IGNORECASE)
_RE_TOROIDAL = re.compile(r"TOROIDAL_SURFACE\s*\(", re.IGNORECASE)
_RE_BSPLINE_SURF = re.compile(
    r"B_SPLINE_SURFACE\s*\(|BEZIER_SURFACE\s*\(",
    re.IGNORECASE,
)

# Edge/curve patterns
_RE_LINE_CURVE = re.compile(r"LINE\s*\(", re.IGNORECASE)
_RE_CIRCLE_CURVE = re.compile(r"CIRCLE\s*\(", re.IGNORECASE)
_RE_BSPLINE_CURVE = re.compile(
    r"B_SPLINE_CURVE\s*\(|BEZIER_CURVE\s*\(|ELLIPSE\s*\(",
    re.IGNORECASE,
)

# Volume entities
_RE_VOLUME = re.compile(
    r"VOLUME\s*\(\s*'[^']*'\s*,\s*\S+\s*,\s*([0-9eE.+\-]+)",
    re.IGNORECASE,
)


def _parse_with_text(filepath: str) -> dict:
    """Fallback parser: extract basic information from STEP as plain text.

    Parses the STEP file's entity structure without a geometric kernel.
    Extracts vertex coordinates, counts faces/edges, estimates bounding box,
    and detects closed-shell status.

    Args:
        filepath: Path to .step or .stp file.

    Returns:
        Structured dict with approximate geometry information.
    """
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"STEP file not found: {filepath}")

    with open(filepath, "r", encoding="utf-8", errors="replace") as fh:
        content = fh.read()

    warnings: list[str] = []

    # -----------------------------------------------------------------
    #  Extract Cartesian point coordinates
    # -----------------------------------------------------------------
    vertices: list[tuple[float, float, float]] = []
    # STEP Cartesian points look like:
    #   #123 = CARTESIAN_POINT('label', (1.0, 2.0, 3.0));
    cartesian_pattern = re.compile(
        r"#\d+\s*=\s*CARTESIAN_POINT\s*\(\s*'[^']*'\s*,\s*\(\s*"
        r"([+\-]?[0-9]*\.?[0-9]+(?:[eE][+\-]?[0-9]+)?)\s*,\s*"
        r"([+\-]?[0-9]*\.?[0-9]+(?:[eE][+\-]?[0-9]+)?)\s*,\s*"
        r"([+\-]?[0-9]*\.?[0-9]+(?:[eE][+\-]?[0-9]+)?)\s*"
        r"\)\s*\)",
        re.IGNORECASE,
    )
    for match in cartesian_pattern.finditer(content):
        try:
            x = float(match.group(1))
            y = float(match.group(2))
            z = float(match.group(3))
            vertices.append((x, y, z))
        except ValueError:
            continue

    # -----------------------------------------------------------------
    #  Count entities
    # -----------------------------------------------------------------
    # Count faces via ADVANCED_FACE or FACE_OUTER_BOUND
    face_indicator = "ADVANCED_FACE" if "ADVANCED_FACE" in content.upper() else "FACE_OUTER_BOUND"
    face_count = content.upper().count(face_indicator)

    # Count edges via EDGE_CURVE or ORIENTED_EDGE
    edge_count = content.upper().count("ORIENTED_EDGE")
    if edge_count == 0:
        edge_count = content.upper().count("EDGE_CURVE")

    # Classify faces by surface type
    face_type_counts: dict[str, int] = {}
    if "ADVANCED_FACE" in content.upper():
        for name, pattern in [
            ("planar", _RE_PLANE),
            ("cylindrical", _RE_CYLINDRICAL),
            ("conical", _RE_CONICAL),
            ("spherical", _RE_SPHERICAL),
            ("toroidal", _RE_TOROIDAL),
            ("spline", _RE_BSPLINE_SURF),
        ]:
            cnt = len(pattern.findall(content))
            if cnt > 0:
                face_type_counts[name] = cnt

    # Classify edges
    edge_type_counts: dict[str, int] = {}
    for name, pattern in [
        ("line", _RE_LINE_CURVE),
        ("arc", _RE_CIRCLE_CURVE),
        ("spline", _RE_BSPLINE_CURVE),
    ]:
        cnt = len(pattern.findall(content))
        if cnt > 0:
            edge_type_counts[name] = cnt

    # -----------------------------------------------------------------
    #  Bounding box
    # -----------------------------------------------------------------
    if vertices:
        xs = [v[0] for v in vertices]
        ys = [v[1] for v in vertices]
        zs = [v[2] for v in vertices]
        xmin, xmax = min(xs), max(xs)
        ymin, ymax = min(ys), max(ys)
        zmin, zmax = min(zs), max(zs)
        bounding_box = (xmin, ymin, zmin, xmax, ymax, zmax)
        overall_dimensions = (xmax - xmin, ymax - ymin, zmax - zmin)
    else:
        bounding_box = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        overall_dimensions = (0.0, 0.0, 0.0)
        warnings.append("No Cartesian points found; bounding box is zero.")

    # -----------------------------------------------------------------
    #  Closed shell detection
    # -----------------------------------------------------------------
    is_closed = bool(_RE_CLOSED_SHELL.search(content))

    # -----------------------------------------------------------------
    #  Volume from text (if present)
    # -----------------------------------------------------------------
    volume = 0.0
    vol_match = _RE_VOLUME.search(content)
    if vol_match:
        try:
            volume = float(vol_match.group(1))
        except ValueError:
            pass

    # Build approximate face data list
    faces: list[FaceData] = []
    for ftype, count in face_type_counts.items():
        for _ in range(count):
            # We don't have per-face area/centroid from text parsing,
            # so fill with estimates
            faces.append(FaceData(
                type=ftype,
                surface_area=0.0,
                centroid=(0.0, 0.0, 0.0),
            ))

    edges_out: list[EdgeData] = []
    for etype, count in edge_type_counts.items():
        for _ in range(count):
            edges_out.append(EdgeData(type=etype, length=0.0))

    return {
        "faces": faces,
        "edges": edges_out,
        "vertices_count": len(vertices),
        "bounding_box": bounding_box,
        "overall_dimensions": overall_dimensions,
        "volume": volume,
        "is_closed_shell": is_closed,
        "parse_warnings": warnings,
        "parser": "text (fallback)",
        "_text_debug": {
            "face_count": face_count,
            "edge_count": edge_count,
            "face_types": face_type_counts,
            "edge_types": edge_type_counts,
        },
    }


# =========================================================================
#  Public API
# =========================================================================

def parse_step(filepath: str) -> dict:
    """Parse a STEP file and extract B-Rep geometry features.

    Uses pythonOCC for full geometric analysis if available. Falls back
    to text-based entity counting if pythonOCC is not installed.

    Args:
        filepath: Absolute or relative path to a .step or .stp file.

    Returns:
        A dict with the following keys:

        faces : list[FaceData]
            Each FaceData has ``type`` (planar/cylindrical/conical/
            spherical/toroidal/spline/other), ``surface_area`` in mm^2,
            and ``centroid`` as (x, y, z) in model space.

        edges : list[EdgeData]
            Each EdgeData has ``type`` (line/arc/spline/other) and
            ``length`` in mm.

        vertices_count : int
            Total number of unique vertices in the B-Rep.

        bounding_box : tuple[float, float, float, float, float, float]
            (xmin, ymin, zmin, xmax, ymax, zmax) in model space.

        overall_dimensions : tuple[float, float, float]
            (length_x, length_y, length_z) extents in mm.

        volume : float
            Approximate volume in mm^3.  Zero if the shape is not a
            solid or volume cannot be computed.

        is_closed_shell : bool
            True if the model is a watertight solid.

        parse_warnings : list[str]
            Non-fatal warnings encountered during parsing.

        parser : str
            Which parser was used ("pythonOCC" or "text (fallback)").

    Raises:
        FileNotFoundError: If the file does not exist.
        RuntimeError: If the file cannot be read as a valid STEP file.
    """
    filepath = os.path.abspath(filepath)

    # Validate extension
    ext = os.path.splitext(filepath)[1].lower()
    if ext not in (".step", ".stp", ".stpnc"):
        # Allow it but warn through the result
        pass

    if _HAS_PYTHONOCC:
        try:
            return _parse_with_pythonocc(filepath)
        except Exception as exc:
            # If pythonOCC fails at runtime (e.g., bad file, OCC version
            # mismatch), fall back to text parser
            try:
                result = _parse_with_text(filepath)
                result.setdefault("parse_warnings", []).append(
                    f"pythonOCC parsing failed ({exc}); fell back to text parser"
                )
                return result
            except Exception:
                raise RuntimeError(
                    f"Failed to parse STEP file '{filepath}' with both "
                    f"pythonOCC ({exc}) and text fallback."
                ) from exc
    else:
        return _parse_with_text(filepath)


# =========================================================================
#  Self-test
# =========================================================================

if __name__ == "__main__":
    print("=== STEP Parser Self-Test ===\n")

    # -----------------------------------------------------------------
    # Test 1: Import check
    # -----------------------------------------------------------------
    print("1. Import check ...")
    print(f"   pythonOCC available: {_HAS_PYTHONOCC}")
    assert callable(parse_step), "parse_step is not callable"
    print("   PASSED\n")

    # -----------------------------------------------------------------
    # Test 2: File-not-found error
    # -----------------------------------------------------------------
    print("2. File-not-found error handling ...")
    try:
        parse_step("nonexistent_file.step")
        assert False, "Should have raised FileNotFoundError"
    except FileNotFoundError:
        print("   Correctly raised FileNotFoundError")
        print("   PASSED\n")

    # -----------------------------------------------------------------
    # Test 3: Data type instantiation
    # -----------------------------------------------------------------
    print("3. Data type instantiation ...")
    face = FaceData(type="planar", surface_area=100.0, centroid=(1.0, 2.0, 3.0))
    assert face.type == "planar"
    assert face.surface_area == 100.0
    assert face.centroid == (1.0, 2.0, 3.0)

    edge = EdgeData(type="line", length=50.0)
    assert edge.type == "line"
    assert edge.length == 50.0
    print("   PASSED\n")

    # -----------------------------------------------------------------
    # Test 4: Text fallback parser
    # -----------------------------------------------------------------
    print("4. Text fallback parser ...")
    # Create a minimal STEP file in memory
    minimal_step = """ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('Minimal test'),'2;1');
ENDSEC;
DATA;
#1 = CARTESIAN_POINT('',(0.0,0.0,0.0));
#2 = CARTESIAN_POINT('',(10.0,0.0,0.0));
#3 = CARTESIAN_POINT('',(10.0,10.0,0.0));
#4 = CARTESIAN_POINT('',(0.0,10.0,0.0));
#5 = CARTESIAN_POINT('',(0.0,0.0,10.0));
#6 = CARTESIAN_POINT('',(10.0,0.0,10.0));
#7 = CARTESIAN_POINT('',(10.0,10.0,10.0));
#8 = CARTESIAN_POINT('',(0.0,10.0,10.0));
#10 = PLANE('',#20);
#11 = CLOSED_SHELL('',(#12));
#12 = ADVANCED_FACE('',(#13),#14,.T.);
#13 = FACE_OUTER_BOUND('',#15,.T.);
ENDSEC;
END-ISO-10303-21;
"""
    import tempfile
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".step", delete=False, encoding="utf-8",
    ) as tmp:
        tmp.write(minimal_step)
        tmp_path = tmp.name

    try:
        # Force text parser
        result = _parse_with_text(tmp_path)
        print(f"   Parser used:        {result['parser']}")
        print(f"   Vertices found:     {result['vertices_count']}")
        print(f"   Bounding box:       {result['bounding_box']}")
        print(f"   Overall dimensions: {result['overall_dimensions']}")
        print(f"   Is closed shell:    {result['is_closed_shell']}")
        print(f"   Warnings:           {result['parse_warnings']}")
        assert result["vertices_count"] == 8, f"Expected 8 vertices, got {result['vertices_count']}"
        assert result["is_closed_shell"] is True, "Should detect CLOSED_SHELL"
        # Bounding box should be roughly 10x10x10
        dims = result["overall_dimensions"]
        assert abs(dims[0] - 10.0) < 0.01, f"X dimension wrong: {dims[0]}"
        assert abs(dims[1] - 10.0) < 0.01, f"Y dimension wrong: {dims[1]}"
        assert abs(dims[2] - 10.0) < 0.01, f"Z dimension wrong: {dims[2]}"
        print("   PASSED\n")
    finally:
        os.unlink(tmp_path)

    # -----------------------------------------------------------------
    # Test 5: Full parse_step with text fallback
    # -----------------------------------------------------------------
    print("5. Full parse_step() with text fallback ...")
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".step", delete=False, encoding="utf-8",
    ) as tmp:
        tmp.write(minimal_step)
        tmp_path = tmp.name

    try:
        result = parse_step(tmp_path)
        print(f"   Parser used:     {result['parser']}")
        print(f"   Vertices count:  {result['vertices_count']}")
        print(f"   Dimensions:      {result['overall_dimensions']}")
        # If pythonOCC is available, the result should use it
        if _HAS_PYTHONOCC:
            print("   (pythonOCC used, geometry may differ from text fallback)")
            assert result["parser"] == "pythonOCC"
        else:
            assert result["parser"] == "text (fallback)"
        print("   PASSED\n")
    finally:
        os.unlink(tmp_path)

    # -----------------------------------------------------------------
    # Test 6: Round-trip with faces and edges lists
    # -----------------------------------------------------------------
    print("6. Face and edge list structure ...")
    assert isinstance(result.get("faces", []), list)
    assert isinstance(result.get("edges", []), list)
    assert isinstance(result["vertices_count"], int)
    assert isinstance(result["volume"], (int, float))
    assert isinstance(result["parse_warnings"], list)

    for key in ("faces", "edges", "vertices_count", "bounding_box",
                "overall_dimensions", "volume", "is_closed_shell"):
        assert key in result, f"Missing key '{key}' in parse result"
    print("   PASSED\n")

    print("=== ALL PARSER TESTS PASSED ===")
