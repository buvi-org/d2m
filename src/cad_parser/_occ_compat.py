"""OCP (Python.NET) compatibility layer for OCC.Core (SWIG) API.

cadquery-ocp provides OpenCascade via Python.NET (OCP.* namespace).
The original parser code was written for the SWIG wrapper (OCC.Core.*).

This module re-exports OCP classes/functions under the OCC.Core.* names
so the parser code works without modification.
"""

# STEP file reading
from OCP.STEPControl import STEPControl_Reader

# Topology explorers
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import (
    TopAbs_FACE, TopAbs_EDGE, TopAbs_VERTEX,
    TopAbs_SOLID, TopAbs_SHELL, TopAbs_COMPOUND,
    TopAbs_REVERSED,
)

# Property computation (mass, area, volume, centroid)
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp

# Bounding box
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib

# Surface/curve adaptors for geometric analysis
from OCP.BRepAdaptor import BRepAdaptor_Surface, BRepAdaptor_Curve

# Geometric types
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

# Shape analysis / checking
from OCP.BRepCheck import BRepCheck
from OCP.BRepTools import BRepTools
from OCP.BRep import BRep
from OCP.TopoDS import TopoDS
from OCP.gp import gp_Pnt
from OCP.TopLoc import TopLoc_Location
from OCP.ShapeAnalysis import ShapeAnalysis_Shell

# Adapted API: SWIG wrapper functions -> OCP static methods

def brepgprop_SurfaceProperties(shape, props):
    """Compat for brepgprop_SurfaceProperties."""
    BRepGProp.SurfaceProperties_s(shape, props)

def brepgprop_VolumeProperties(shape, props, *args, **kwargs):
    """Compat for brepgprop_VolumeProperties."""
    BRepGProp.VolumeProperties_s(shape, props)

def brepgprop_LinearProperties(shape, props):
    """Compat for brepgprop_LinearProperties."""
    BRepGProp.LinearProperties_s(shape, props)

def brepbndlib_Add(shape, bbox):
    """Compat for brepbndlib_Add."""
    BRepBndLib.Add_s(shape, bbox)

def _extract_TopoDS_Face(shape):
    """Downcast TopoDS_Shape to TopoDS_Face."""
    return TopoDS.Face_s(shape)

def _extract_TopoDS_Edge(shape):
    """Downcast TopoDS_Shape to TopoDS_Edge."""
    return TopoDS.Edge_s(shape)


class BRep_Tool:
    """Compat for OCC.Core.BRep.BRep_Tool."""
    @staticmethod
    def Triangulation(face, location):
        return BRep.Tool.Triangulation_s(face, location)


class BRepCheck_Analyzer:
    """Compat for OCC.Core.BRepCheck.BRepCheck_Analyzer."""
    def __init__(self, shape):
        self._analyzer = BRepCheck.Analyzer_s(shape)

    def IsValid(self):
        return self._analyzer.IsValid()


class BRepClass3d_SolidClassifier:
    """Compat for OCC.Core.BRepClass3d.BRepClass3d_SolidClassifier."""
    def __init__(self, shape):
        self._classifier = BRepClass3d.SolidClassifier_s(shape)

    def Perform(self, pnt, tolerance=1e-6):
        self._classifier.Perform(pnt, tolerance)

    def State(self):
        return self._classifier.State()

    @staticmethod
    def PerformInfinitePoint(shape, tolerance=1e-6):
        from OCP.BRepClass3d import BRepClass3d as Bc3d
        classifier = Bc3d.SolidClassifier_s(shape)
        # Use a point far outside the bounding box
        classifier.Perform(gp_Pnt(1e9, 1e9, 1e9), tolerance)
        return classifier


# Import BRepClass3d for the SolidClassifier
try:
    from OCP.BRepClass3d import BRepClass3d
except ImportError:
    BRepClass3d = None

if BRepClass3d is not None:
    # Override BRepClass3d_SolidClassifier with proper import
    class BRepClass3d_SolidClassifier:
        """Compat for OCC.Core.BRepClass3d.BRepClass3d_SolidClassifier."""
        def __init__(self, shape):
            self._classifier = BRepClass3d.SolidClassifier_s(shape)

        def Perform(self, pnt, tolerance=1e-6):
            self._classifier.Perform(pnt, tolerance)

        def State(self):
            return self._classifier.State()


def _get_face_normal_occ(face) -> tuple:
    """Get face normal using OCP API directly."""
    import numpy as np

    try:
        adaptor = BRepAdaptor_Surface(face)
        surf_type = adaptor.GetType()
        normal = np.array([0.0, 0.0, 1.0], dtype=np.float64)

        if surf_type == GeomAbs_Plane:
            plane = adaptor.Plane()
            ax3 = plane.Position()
            direction = ax3.Direction()
            normal = np.array([direction.X(), direction.Y(), direction.Z()],
                              dtype=np.float64)
        else:
            location = TopLoc_Location()
            triangulation = BRep.Tool.Triangulation_s(face, location)
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

        # Apply face orientation
        from OCP.TopAbs import TopAbs_REVERSED as _TopAbs_REVERSED
        if hasattr(face, 'Orientation') and face.Orientation() == _TopAbs_REVERSED:
            normal = -normal

        return (float(normal[0]), float(normal[1]), float(normal[2]))
    except Exception:
        return (0.0, 0.0, 1.0)


def TopoDS_Compound():
    """Create an empty TopoDS_Compound."""
    from OCP.TopoDS import TopoDS
    return TopoDS.Compound_s()


class TopoDS_Shape:
    """Just a type placeholder — OCP uses TopoDS_Shape directly."""
    pass
