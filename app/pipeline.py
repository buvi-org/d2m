"""Full inference pipeline orchestrator for d2m Phase 0.

Wires together cad_parser -> feature extraction -> knowledge_graph rules
-> planner LLM call, with progress tracking and error handling at every step.
"""

from __future__ import annotations

import time
import logging
import traceback
from dataclasses import dataclass, field
from typing import Optional, Generator

import numpy as np

from src.cad_parser import (
    parse_step,
    build_aag,
    _to_json_serializable,
)
from src.knowledge_graph import run_all_rules
from src.planner import ProcessPlanner

logger = logging.getLogger(__name__)


# =========================================================================
#  PipelineResult dataclass
# =========================================================================

@dataclass
class PipelineResult:
    """Aggregate result from a full pipeline run."""

    geometry: dict = field(default_factory=dict)
    aag: dict = field(default_factory=dict)
    features: list[dict] = field(default_factory=list)
    rule_result: dict = field(default_factory=dict)
    plan: Optional[dict] = None
    plan_validated: bool = False
    validation_warnings: list[str] = field(default_factory=list)
    elapsed_time: float = 0.0
    step_times: dict[str, float] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)


# =========================================================================
#  Feature extraction heuristics (Phase 0 -- no trained GNN)
# =========================================================================

def _classify_face_to_feature_type(
    face_type: str,
    normal: tuple[float, float, float],
    centroid: tuple[float, float, float],
    area: float,
) -> Optional[str]:
    """Heuristic per-face classification into a machining feature type.

    In Phase 0 without a GNN, we use simple geometric rules:
    - Cylindrical face          -> candidate hole or fillet
    - Conical face              -> chamfer or countersink
    - Planar face, normal ~Z    -> top/bottom face (pocket floor candidate)
    - Planar face, normal !~Z   -> side face

    Returns a feature type string or None if indeterminate.
    """
    nz = abs(normal[2]) if len(normal) >= 3 else 0.0

    if face_type == "cylindrical":
        # Could be a hole (internal) or a fillet/round (blend surface)
        # Without curvature direction info, mark as "hole_candidate"
        return "hole_candidate"
    elif face_type == "conical":
        return "chamfer_candidate"
    elif face_type == "planar":
        if nz > 0.9:
            return "planar_z"
        elif nz < 0.1:
            return "planar_side"
        else:
            return "planar_angled"
    elif face_type == "toroidal":
        return "fillet_candidate"
    elif face_type == "spherical":
        return "spherical_feature"
    elif face_type == "spline":
        return "freeform_surface"
    else:
        return "other"


def _build_concave_components(
    nodes: list, adjacency: list
) -> list[list[int]]:
    """Group face indices connected by concave edges into feature components.

    Concave edges in the AAG indicate material-removal features (pockets,
    slots, steps). We build connected components over the subgraph formed
    by concave edges only.

    Returns list of components, each a list of node indices.
    """
    n = len(nodes)
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    # Union faces connected by concave edges
    for adj in adjacency:
        # Handle both dataclass and dict forms
        convexity = getattr(adj, "convexity", None) or adj.get("convexity", "")
        node_a = getattr(adj, "node_a", None)
        if node_a is None:
            node_a = adj.get("node_a", 0)
        node_b = getattr(adj, "node_b", None)
        if node_b is None:
            node_b = adj.get("node_b", 0)

        if convexity == "concave":
            union(node_a, node_b)

    # Collect components
    components: dict[int, list[int]] = {}
    for i in range(n):
        root = find(i)
        components.setdefault(root, []).append(i)

    # Only return components with >1 face (single-face components are
    # isolated faces that may be features like holes or chamfers)
    return [comp for comp in components.values() if len(comp) >= 1]


def _component_to_feature(
    face_indices: list[int],
    nodes: list,
    component_id: int,
) -> dict:
    """Classify a connected component of faces as a specific feature type.

    Determines the feature type from the dominant face type in the component,
    then builds a feature dict suitable for the rule engine and LLM prompt.
    """
    if not face_indices:
        return {}

    # Normalize node access (dataclass or dict)
    def _get(node, attr, default=None):
        return getattr(node, attr, None) or node.get(attr, default)

    face_types = [_get(nodes[i], "face_type", "other") for i in face_indices]
    areas = [_get(nodes[i], "surface_area", 0.0) for i in face_indices]
    centroids = [_get(nodes[i], "centroid", (0.0, 0.0, 0.0)) for i in face_indices]
    normals = [_get(nodes[i], "normal", (0.0, 0.0, 1.0)) for i in face_indices]

    total_area = sum(areas)

    # Count face type frequencies
    from collections import Counter
    type_counts = Counter(face_types)

    # Determine dominant feature type
    dominant_type = type_counts.most_common(1)[0][0] if type_counts else "other"

    # Build dimensions
    zs = [c[2] for c in centroids]
    xs = [c[0] for c in centroids]
    ys = [c[1] for c in centroids]
    depth_range = max(zs) - min(zs) if zs else 0.0
    width_range = max(xs) - min(xs) if xs else 0.0
    height_range = max(ys) - min(ys) if ys else 0.0

    feature = {
        "feature_id": f"F{component_id:03d}",
        "face_indices": face_indices,
        "face_count": len(face_indices),
        "total_area_mm2": round(total_area, 2),
        "dominant_face_type": dominant_type,
        "face_type_counts": dict(type_counts),
    }

    if dominant_type == "cylindrical" and len(face_indices) >= 1:
        # Hole feature — use OCC cylinder radius from face data if available
        node_radius = max(
            _get(nodes[i], "radius", 0.0) for i in face_indices
        )
        node_depth = max(
            _get(nodes[i], "depth", 0.0) for i in face_indices
        )
        if node_radius > 0:
            hole_dia = round(node_radius * 2, 2)
        else:
            hole_dia = round(max(width_range, height_range), 2)
        if node_depth > 0:
            hole_depth = round(node_depth, 2)
        else:
            hole_depth = round(depth_range, 2)
        feature["type"] = "hole"
        feature["dimensions"] = {
            "diameter_mm": hole_dia,
            "depth_mm": hole_depth,
            "tolerance_mm": 0.05,
            "has_thread": False,
        }
    elif dominant_type == "conical":
        feature["type"] = "chamfer"
        feature["dimensions"] = {
            "chamfer_width_mm": round(max(width_range, height_range, depth_range), 2),
            "depth_mm": round(depth_range, 2),
        }
    elif dominant_type == "planar":
        # Could be pocket, slot, step, or face
        avg_normal_z = sum(abs(n[2]) for n in normals) / len(normals) if normals else 0.0

        if depth_range > 1.0 and len(face_indices) >= 3:
            # Multiple faces with depth variation -> pocket or slot
            aspect = width_range / max(height_range, 0.001)
            if aspect > 3.0 or aspect < 0.33:
                feature["type"] = "slot"
            else:
                feature["type"] = "pocket"
            feature["dimensions"] = {
                "width_mm": round(width_range, 2),
                "depth_mm": round(depth_range, 2),
                "corner_radius_mm": round(min(width_range, height_range) * 0.1, 2),
                "length_mm": round(max(width_range, height_range), 2),
            }
        elif avg_normal_z > 0.8:
            feature["type"] = "face"
            feature["dimensions"] = {
                "width_mm": round(max(width_range, height_range), 2),
                "depth_mm": round(depth_range, 2),
            }
        else:
            feature["type"] = "contour"
            feature["dimensions"] = {
                "depth_mm": round(depth_range, 2),
                "tool_diameter_mm": 10.0,
            }
    elif dominant_type == "toroidal":
        feature["type"] = "face"
        feature["dimensions"] = {
            "width_mm": round(max(width_range, height_range), 2),
            "depth_mm": round(depth_range, 2),
        }
    else:
        feature["type"] = "face"
        feature["dimensions"] = {
            "width_mm": round(max(width_range, height_range), 2),
            "depth_mm": round(depth_range, 2),
        }

    # Add location and tolerance info for the LLM prompt
    avg_centroid = (
        sum(c[0] for c in centroids) / len(centroids),
        sum(c[1] for c in centroids) / len(centroids),
        sum(c[2] for c in centroids) / len(centroids),
    )
    feature["location"] = (
        f"centered near ({avg_centroid[0]:.1f}, "
        f"{avg_centroid[1]:.1f}, {avg_centroid[2]:.1f})"
    )
    feature["tolerance"] = "±0.1mm"

    return feature


def extract_features(geometry: dict, aag: dict) -> list[dict]:
    """Extract machining features from parsed geometry and AAG.

    Phase 0 heuristic approach:
    1. Build concave connected components from the AAG (concave edges
       indicate material-removal features).
    2. Classify each component by its dominant face type.
    3. Also classify faces NOT in any concave component individually
       (isolated holes, chamfers, etc.).

    Args:
        geometry: Parsed geometry dict from parse_step().
        aag: AAG dict from build_aag() / _to_json_serializable().

    Returns:
        List of feature dicts with keys: feature_id, type, dimensions,
        location, tolerance, face_indices, etc.

    Features returned are compatible with both the knowledge_graph
    rule engine and the planner's LLM prompt formatting.
    """
    nodes = aag.get("nodes", [])
    adjacency = aag.get("adjacency", [])

    if not nodes:
        return []

    # Build concave-connected components
    components = _build_concave_components(nodes, adjacency)

    # Track which faces have been assigned to a feature component
    assigned = set()

    features: list[dict] = []
    for comp_id, face_indices in enumerate(components):
        feature = _component_to_feature(face_indices, nodes, comp_id)
        if feature:
            features.append(feature)
            assigned.update(face_indices)

    # Add any unassigned faces as individual features (e.g., isolated holes)
    for i, node in enumerate(nodes):
        if i in assigned:
            continue

        face_type = getattr(node, "face_type", None) or node.get("face_type", "other")
        centroid = getattr(node, "centroid", None) or node.get("centroid", (0.0, 0.0, 0.0))
        normal = getattr(node, "normal", None) or node.get("normal", (0.0, 0.0, 1.0))
        area = getattr(node, "surface_area", None) or node.get("surface_area", 0.0)

        candidate_type = _classify_face_to_feature_type(
            face_type, normal, centroid, area
        )

        # Get radius and depth from node if available (pythonOCC extraction)
        node_radius = getattr(node, "radius", None) or node.get("radius", 0.0)
        node_depth = getattr(node, "depth", None) or node.get("depth", 0.0)

        # Build a minimal feature dict
        fid = f"F{len(features):03d}"
        if candidate_type == "hole_candidate":
            # Use OCC cylinder radius if available, otherwise estimate from area
            if node_radius > 0:
                hole_dia = round(node_radius * 2, 2)
            elif area > 0:
                # Cylinder lateral surface: area = pi * d * h, use aspect heuristic
                hole_dia = round(np.sqrt(area / np.pi) * 2, 2)
            else:
                hole_dia = 10.0
            features.append({
                "feature_id": fid,
                "type": "hole",
                "dimensions": {
                    "diameter_mm": hole_dia,
                    "depth_mm": round(node_depth, 2) if node_depth > 0 else 20.0,
                    "tolerance_mm": 0.05,
                    "has_thread": False,
                },
                "location": f"centered near ({centroid[0]:.1f}, {centroid[1]:.1f}, {centroid[2]:.1f})",
                "tolerance": "±0.1mm",
                "face_indices": [i],
                "face_count": 1,
                "dominant_face_type": face_type,
            })
        elif candidate_type == "chamfer_candidate":
            features.append({
                "feature_id": fid,
                "type": "chamfer",
                "dimensions": {
                    "chamfer_width_mm": 1.5,
                    "depth_mm": 1.5,
                },
                "location": f"near ({centroid[0]:.1f}, {centroid[1]:.1f}, {centroid[2]:.1f})",
                "tolerance": "±0.1mm",
                "face_indices": [i],
                "face_count": 1,
                "dominant_face_type": face_type,
            })
        elif candidate_type == "fillet_candidate":
            features.append({
                "feature_id": fid,
                "type": "face",
                "dimensions": {
                    "width_mm": round(np.sqrt(area), 2) if area > 0 else 10.0,
                    "depth_mm": 1.0,
                },
                "location": f"near ({centroid[0]:.1f}, {centroid[1]:.1f}, {centroid[2]:.1f})",
                "tolerance": "±0.1mm",
                "notes": "Fillet/round surface",
                "face_indices": [i],
                "face_count": 1,
                "dominant_face_type": face_type,
            })
        elif candidate_type in ("planar_z", "planar_side", "planar_angled"):
            features.append({
                "feature_id": fid,
                "type": "face",
                "dimensions": {
                    "width_mm": round(np.sqrt(area) * 2, 2) if area > 0 else 50.0,
                    "depth_mm": 2.0,
                },
                "location": f"near ({centroid[0]:.1f}, {centroid[1]:.1f}, {centroid[2]:.1f})",
                "tolerance": "±0.1mm",
                "face_indices": [i],
                "face_count": 1,
                "dominant_face_type": face_type,
            })

    return features


# =========================================================================
#  Plan validation against rule engine results
# =========================================================================

def _validate_plan_against_rules(plan: dict, rule_result: dict) -> list[str]:
    """Check that the LLM-generated plan satisfies the rule engine constraints.

    Args:
        plan: Parsed process plan dict from the LLM.
        rule_result: Dict from run_all_rules() with 'errors' and 'warnings' keys.

    Returns:
        List of validation warning strings.
    """
    warnings: list[str] = []

    # 1. Check for hard errors from the rule engine
    errors = rule_result.get("errors", [])
    if errors:
        error_msgs = [e.get("message", str(e)) for e in errors]
        warnings.append(
            f"Rule engine found {len(errors)} hard error(s): {'; '.join(error_msgs[:3])}"
        )

    # 2. Check that plan addresses all required operations from rule engine
    required_ops = {
        op.get("operation", "")
        for op in rule_result.get("suggested_operations", [])
    }
    plan_ops = {
        op.get("operation_name", op.get("operation", "")) or op.get("strategy", "")
        for op in plan.get("operations", [])
    }

    # Normalize names for comparison
    def _normalize(name: str) -> str:
        return name.lower().replace(" ", "_").replace("-", "_")

    req_norm = {_normalize(op) for op in required_ops}
    plan_norm = {_normalize(op) for op in plan_ops}

    missing = req_norm - plan_norm
    # Only flag as missing if the plan has at least some operations
    # (avoids false positives from naming mismatches)
    if missing and plan_ops:
        # Check for partial coverage
        uncovered = req_norm - plan_norm
        if len(uncovered) >= len(req_norm) * 0.5:
            warnings.append(
                f"Plan may be missing {len(uncovered)} required operation types "
                f"({', '.join(sorted(uncovered)[:5])})"
            )

    # 3. Check DFM notes presence
    dfm = plan.get("dfm_notes")
    if dfm is None:
        warnings.append("Plan is missing 'dfm_notes' section")
    elif isinstance(dfm, list) and len(dfm) == 0:
        warnings.append("Plan has empty dfm_notes (no DFM feedback)")

    # 4. Check alternative approaches
    alternatives = plan.get("alternative_approaches")
    if alternatives is None:
        warnings.append("Plan is missing 'alternative_approaches' section")
    elif isinstance(alternatives, list) and len(alternatives) == 0:
        warnings.append("Plan has no alternative approaches")

    return warnings


# =========================================================================
#  InferencePipeline
# =========================================================================

class InferencePipeline:
    """Full CAPP inference pipeline: STEP -> Features -> Rules -> Plan.

    Wires together:
    1. CAD parser (STEP -> geometry + AAG)
    2. Feature extraction (heuristic, no GNN in Phase 0)
    3. Rule engine (DFM checks, suggested operations)
    4. LLM planner (DeepSeek-generated process plan)
    5. Post-plan validation

    Usage::

        pipeline = InferencePipeline()
        result = pipeline.run("part.step", "aluminum_6061", volume=500)
        print(result.plan["operations"])

    Or with progress updates::

        for step in pipeline.step_by_step("part.step", "aluminum_6061"):
            print(f"{step['step']}: {step['status']}")
    """

    def __init__(self, deepseek_api_key: Optional[str] = None):
        """Initialize the pipeline with all components.

        Args:
            deepseek_api_key: DeepSeek API key. If None, reads from
                              DEEPSEEK_API_KEY env var (via ProcessPlanner).
                              Can also be set later.
        """
        self._api_key = deepseek_api_key
        self._planner: Optional[ProcessPlanner] = None

    # -----------------------------------------------------------------
    #  Lazy planner init
    # -----------------------------------------------------------------

    def _get_planner(self) -> ProcessPlanner:
        """Get or lazily initialize the ProcessPlanner."""
        if self._planner is None:
            self._planner = ProcessPlanner(api_key=self._api_key)
        return self._planner

    # -----------------------------------------------------------------
    #  Batch runner
    # -----------------------------------------------------------------

    def run(
        self,
        step_filepath: str,
        material: str = "aluminum_6061",
        volume: int = 100,
        tolerances: str = "±0.1mm",
    ) -> PipelineResult:
        """Run the full pipeline end-to-end.

        Args:
            step_filepath: Path to the STEP file (.step/.stp).
            material: Material key (e.g., "aluminum_6061", "steel_4140").
            volume: Production volume in units.
            tolerances: Tolerance specification string.

        Returns:
            PipelineResult with all outputs and timing information.
        """
        result = PipelineResult()
        t0 = time.perf_counter()

        # --- Step 1: Parse STEP file ---
        t1 = time.perf_counter()
        try:
            geometry = parse_step(step_filepath)
            result.geometry = geometry
            result.step_times["parse_step"] = round(time.perf_counter() - t1, 3)
            logger.info(
                "STEP parsing complete: %d faces, %d edges, volume=%.1f mm^3",
                len(geometry.get("faces", [])),
                len(geometry.get("edges", [])),
                geometry.get("volume", 0.0),
            )
        except Exception as e:
            result.errors.append(f"STEP parsing failed: {e}")
            logger.error("STEP parsing error: %s", traceback.format_exc())
            result.elapsed_time = round(time.perf_counter() - t0, 3)
            return result

        # --- Step 2: Build AAG ---
        t2 = time.perf_counter()
        try:
            faces = geometry.get("faces", [])
            edges = geometry.get("edges", [])
            shape = geometry.get("_occ_shape")
            raw_aag = build_aag(faces, edges, shape=shape)
            result.aag = _to_json_serializable(raw_aag)
            result.step_times["build_aag"] = round(time.perf_counter() - t2, 3)
            logger.info(
                "AAG built: %d nodes, %d adjacency edges",
                len(result.aag.get("nodes", [])),
                len(result.aag.get("adjacency", [])),
            )
        except Exception as e:
            result.errors.append(f"AAG construction failed: {e}")
            logger.error("AAG error: %s", traceback.format_exc())
            result.elapsed_time = round(time.perf_counter() - t0, 3)
            return result

        # --- Step 3: Extract features ---
        t3 = time.perf_counter()
        try:
            result.features = extract_features(result.geometry, result.aag)
            result.step_times["extract_features"] = round(time.perf_counter() - t3, 3)
            logger.info(
                "Feature extraction: %d features from %d faces",
                len(result.features),
                len(result.aag.get("nodes", [])),
            )
        except Exception as e:
            result.errors.append(f"Feature extraction failed: {e}")
            logger.error("Feature extraction error: %s", traceback.format_exc())
            result.elapsed_time = round(time.perf_counter() - t0, 3)
            return result

        # --- Step 4: Run rule engine ---
        t4 = time.perf_counter()
        try:
            result.rule_result = run_all_rules(result.features, material)
            result.step_times["rule_engine"] = round(time.perf_counter() - t4, 3)
            rw = len(result.rule_result.get("warnings", []))
            re = len(result.rule_result.get("errors", []))
            ro = len(result.rule_result.get("suggested_operations", []))
            logger.info(
                "Rule engine: %d warnings, %d errors, %d suggested ops",
                rw, re, ro,
            )
        except Exception as e:
            result.errors.append(f"Rule engine failed: {e}")
            logger.error("Rule engine error: %s", traceback.format_exc())
            result.elapsed_time = round(time.perf_counter() - t0, 3)
            return result

        # --- Step 5: Format features for LLM prompt ---
        t5 = time.perf_counter()
        try:
            # Build dimensions dict from geometry for the LLM
            dims = geometry.get("overall_dimensions", (0.0, 0.0, 0.0))
            dimensions = {"x": dims[0], "y": dims[1], "z": dims[2]}

            planner = self._get_planner()
            result.plan = planner.generate_plan(
                features=result.features,
                material=material,
                volume=volume,
                dimensions=dimensions,
                tolerances=tolerances,
            )
            result.step_times["llm_plan"] = round(time.perf_counter() - t5, 3)
            logger.info(
                "LLM plan generated: %d operations, %.1f min estimated",
                len(result.plan.get("operations", [])),
                result.plan.get("total_estimated_time_minutes", 0.0),
            )
        except Exception as e:
            result.errors.append(f"LLM plan generation failed: {e}")
            logger.error("LLM plan error: %s", traceback.format_exc())
            # Don't return here -- we still have rule results to show
            result.elapsed_time = round(time.perf_counter() - t0, 3)
            return result

        # --- Step 6: Validate plan against rules ---
        t6 = time.perf_counter()
        try:
            result.validation_warnings = _validate_plan_against_rules(
                result.plan, result.rule_result
            )
            result.plan_validated = (
                len(result.rule_result.get("errors", [])) == 0
                and len(result.validation_warnings) <= 2
            )
            result.step_times["validate"] = round(time.perf_counter() - t6, 3)
        except Exception as e:
            result.validation_warnings.append(f"Plan validation error: {e}")
            logger.error("Validation error: %s", traceback.format_exc())
            result.plan_validated = False

        result.elapsed_time = round(time.perf_counter() - t0, 3)
        logger.info("Pipeline complete: %.2fs elapsed", result.elapsed_time)
        return result

    # -----------------------------------------------------------------
    #  Generator-based step-by-step runner
    # -----------------------------------------------------------------

    def step_by_step(
        self,
        step_filepath: str,
        material: str = "aluminum_6061",
        volume: int = 100,
        tolerances: str = "±0.1mm",
    ) -> Generator[dict, None, PipelineResult]:
        """Run the pipeline, yielding progress updates at each step.

        Each yielded dict has:
            step:   str   Human-readable step name.
            status: str   "running", "done", or "error".
            data:   dict  Step-specific output (partial results).
            time:   float Elapsed seconds for this step.

        The final yield is followed by the return of the PipelineResult.

        Usage with Streamlit::

            result = None
            progress_bar = st.progress(0)
            for update in pipeline.step_by_step("part.step", "aluminum_6061"):
                progress_bar.progress(update["progress"])
                # Show update["data"] as it arrives
            # result is the PipelineResult
        """
        result = PipelineResult()
        t0 = time.perf_counter()
        total_steps = 6

        # --- Step 1: Parse STEP ---
        t_start = time.perf_counter()
        yield {
            "step": "Parsing STEP file",
            "status": "running",
            "progress": 0.0,
            "data": {},
            "time": 0.0,
        }
        try:
            result.geometry = parse_step(step_filepath)
            elapsed = round(time.perf_counter() - t_start, 3)
            result.step_times["parse_step"] = elapsed
            yield {
                "step": "Parsing STEP file",
                "status": "done",
                "progress": 1 / total_steps,
                "data": {
                    "faces": len(result.geometry.get("faces", [])),
                    "edges": len(result.geometry.get("edges", [])),
                    "volume": round(result.geometry.get("volume", 0.0), 2),
                    "watertight": result.geometry.get("is_closed_shell", False),
                    "dimensions": result.geometry.get("overall_dimensions", (0, 0, 0)),
                },
                "time": elapsed,
            }
        except Exception as e:
            result.errors.append(f"STEP parsing failed: {e}")
            yield {
                "step": "Parsing STEP file",
                "status": "error",
                "progress": 0.0,
                "data": {"error": str(e)},
                "time": round(time.perf_counter() - t_start, 3),
            }
            result.elapsed_time = round(time.perf_counter() - t0, 3)
            return result

        # --- Step 2: Build AAG ---
        t_start = time.perf_counter()
        yield {
            "step": "Building adjacency graph",
            "status": "running",
            "progress": 1 / total_steps,
            "data": {},
            "time": 0.0,
        }
        try:
            faces = result.geometry.get("faces", [])
            edges = result.geometry.get("edges", [])
            shape = result.geometry.get("_occ_shape")
            raw_aag = build_aag(faces, edges, shape=shape)
            result.aag = _to_json_serializable(raw_aag)
            elapsed = round(time.perf_counter() - t_start, 3)
            result.step_times["build_aag"] = elapsed
            yield {
                "step": "Building adjacency graph",
                "status": "done",
                "progress": 2 / total_steps,
                "data": {
                    "nodes": len(result.aag.get("nodes", [])),
                    "adjacency_edges": len(result.aag.get("adjacency", [])),
                },
                "time": elapsed,
            }
        except Exception as e:
            result.errors.append(f"AAG construction failed: {e}")
            yield {
                "step": "Building adjacency graph",
                "status": "error",
                "progress": 1 / total_steps,
                "data": {"error": str(e)},
                "time": round(time.perf_counter() - t_start, 3),
            }
            result.elapsed_time = round(time.perf_counter() - t0, 3)
            return result

        # --- Step 3: Extract features ---
        t_start = time.perf_counter()
        yield {
            "step": "Extracting manufacturing features",
            "status": "running",
            "progress": 2 / total_steps,
            "data": {},
            "time": 0.0,
        }
        try:
            result.features = extract_features(result.geometry, result.aag)
            elapsed = round(time.perf_counter() - t_start, 3)
            result.step_times["extract_features"] = elapsed
            type_summary = {}
            for f in result.features:
                ft = f.get("type", "unknown")
                type_summary[ft] = type_summary.get(ft, 0) + 1
            yield {
                "step": "Extracting manufacturing features",
                "status": "done",
                "progress": 3 / total_steps,
                "data": {
                    "feature_count": len(result.features),
                    "feature_types": type_summary,
                },
                "time": elapsed,
            }
        except Exception as e:
            result.errors.append(f"Feature extraction failed: {e}")
            yield {
                "step": "Extracting manufacturing features",
                "status": "error",
                "progress": 2 / total_steps,
                "data": {"error": str(e)},
                "time": round(time.perf_counter() - t_start, 3),
            }
            result.elapsed_time = round(time.perf_counter() - t0, 3)
            return result

        # --- Step 4: Run rule engine ---
        t_start = time.perf_counter()
        yield {
            "step": "Running DFM rule checks",
            "status": "running",
            "progress": 3 / total_steps,
            "data": {},
            "time": 0.0,
        }
        try:
            result.rule_result = run_all_rules(result.features, material)
            elapsed = round(time.perf_counter() - t_start, 3)
            result.step_times["rule_engine"] = elapsed
            yield {
                "step": "Running DFM rule checks",
                "status": "done",
                "progress": 4 / total_steps,
                "data": {
                    "warnings": len(result.rule_result.get("warnings", [])),
                    "errors": len(result.rule_result.get("errors", [])),
                    "suggested_ops": len(result.rule_result.get("suggested_operations", [])),
                },
                "time": elapsed,
            }
        except Exception as e:
            result.errors.append(f"Rule engine failed: {e}")
            yield {
                "step": "Running DFM rule checks",
                "status": "error",
                "progress": 3 / total_steps,
                "data": {"error": str(e)},
                "time": round(time.perf_counter() - t_start, 3),
            }
            result.elapsed_time = round(time.perf_counter() - t0, 3)
            return result

        # --- Step 5: Generate LLM plan ---
        t_start = time.perf_counter()
        yield {
            "step": "Generating process plan (DeepSeek LLM)",
            "status": "running",
            "progress": 4 / total_steps,
            "data": {},
            "time": 0.0,
        }
        try:
            dims = result.geometry.get("overall_dimensions", (0.0, 0.0, 0.0))
            dimensions = {"x": dims[0], "y": dims[1], "z": dims[2]}

            planner = self._get_planner()
            result.plan = planner.generate_plan(
                features=result.features,
                material=material,
                volume=volume,
                dimensions=dimensions,
                tolerances=tolerances,
            )
            elapsed = round(time.perf_counter() - t_start, 3)
            result.step_times["llm_plan"] = elapsed
            yield {
                "step": "Generating process plan (DeepSeek LLM)",
                "status": "done",
                "progress": 5 / total_steps,
                "data": {
                    "operations": len(result.plan.get("operations", [])),
                    "estimated_time": result.plan.get("total_estimated_time_minutes", 0),
                    "token_usage": result.plan.get("_metadata", {}).get("token_usage"),
                },
                "time": elapsed,
            }
        except Exception as e:
            result.errors.append(f"LLM plan generation failed: {e}")
            yield {
                "step": "Generating process plan (DeepSeek LLM)",
                "status": "error",
                "progress": 4 / total_steps,
                "data": {"error": str(e)},
                "time": round(time.perf_counter() - t_start, 3),
            }
            result.elapsed_time = round(time.perf_counter() - t0, 3)
            return result

        # --- Step 6: Validate plan ---
        t_start = time.perf_counter()
        yield {
            "step": "Validating plan against rules",
            "status": "running",
            "progress": 5 / total_steps,
            "data": {},
            "time": 0.0,
        }
        try:
            result.validation_warnings = _validate_plan_against_rules(
                result.plan, result.rule_result
            )
            result.plan_validated = (
                len(result.rule_result.get("errors", [])) == 0
                and len(result.validation_warnings) <= 2
            )
            elapsed = round(time.perf_counter() - t_start, 3)
            result.step_times["validate"] = elapsed
            yield {
                "step": "Validating plan against rules",
                "status": "done",
                "progress": 1.0,
                "data": {
                    "validated": result.plan_validated,
                    "validation_warnings": len(result.validation_warnings),
                },
                "time": elapsed,
            }
        except Exception as e:
            result.validation_warnings.append(f"Plan validation error: {e}")
            yield {
                "step": "Validating plan against rules",
                "status": "error",
                "progress": 5 / total_steps,
                "data": {"error": str(e)},
                "time": round(time.perf_counter() - t_start, 3),
            }

        result.elapsed_time = round(time.perf_counter() - t0, 3)
        return result
