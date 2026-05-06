"""
d2m CAD Parser Module - STEP file geometry feature extraction.

Provides tools for reading ISO 10303 STEP files (AP203/AP214) and
extracting B-Rep geometry features for CAPP process planning:

- parse_step():    Full B-Rep extraction (faces, edges, vertices,
                   dimensions, volume, watertight check).
- build_aag():     Attributed Adjacency Graph construction from
                   face/edge data for feature recognition.
- render_views():  4-view image generation (front, top, side, iso).

Primary classes for external use:
    FaceData     - Extracted face (type, area, centroid).
    EdgeData     - Extracted edge (type, length).
    AAGNode      - Graph node for a face.
    AAGEdge      - Graph edge between adjacent faces.
    CameraView   - Camera setup for rendering.

Backend selection:
    Uses pythonOCC (preferred) for full B-Rep analysis with automatic
    fallback to text-based STEP parsing when pythonOCC is unavailable.
    Rendering tries CadQuery > trimesh+matplotlib > stub.
"""

__version__ = "0.1.0"

from .parser import FaceData, EdgeData, parse_step
from .aag import AAGNode, AAGEdge, build_aag, _to_json_serializable
from .renderer import CameraView, render_views

__all__ = [
    # Parser
    "FaceData",
    "EdgeData",
    "parse_step",
    # AAG
    "AAGNode",
    "AAGEdge",
    "build_aag",
    "_to_json_serializable",
    # Renderer
    "CameraView",
    "render_views",
]
