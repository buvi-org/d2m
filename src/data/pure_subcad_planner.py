"""Pure SubCAD feature planner for STEP/CadQuery translation.

The planner is intentionally conservative about manufacturing completeness but
does not use the old blocked-term model.  It classifies CadQuery/STEP evidence
into pure SubCAD operation families so benchmark runs can distinguish:

* exact operations we can represent today,
* tolerance-machined operations that need sampled/surface toolpaths, and
* genuinely unmachinable/manual-review cases.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any


PLANNED_EXACT = "planned_exact_operation"
PLANNED_TOLERANCE = "planned_tolerance_operation"
PLANNED_MULTI_PROCESS = "planned_multi_process_operation"
UNSUPPORTED_UNMACHINABLE = "unsupported_unmachinable"
NEEDS_MANUAL_REVIEW = "needs_manual_review"


@dataclass
class PlannedFeature:
    """One detected source feature and its intended SubCAD operation family."""

    source: str
    family: str
    planner_status: str
    operation: str
    reason: str
    evidence: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "family": self.family,
            "planner_status": self.planner_status,
            "operation": self.operation,
            "reason": self.reason,
            "evidence": self.evidence,
        }


@dataclass
class PureSubCADPlan:
    """Planner output used by translator gating and reports."""

    features: list[PlannedFeature]
    compatible: bool
    coverage_mode: str = "pure_subcad_operations"
    unsupported_count: int = 0
    manual_review_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "coverage_mode": self.coverage_mode,
            "compatible": self.compatible,
            "unsupported_count": self.unsupported_count,
            "manual_review_count": self.manual_review_count,
            "features": [feature.to_dict() for feature in self.features],
            "summary": self.summary(),
        }

    def summary(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for feature in self.features:
            counts[feature.planner_status] = counts.get(feature.planner_status, 0) + 1
        return counts


def plan_pure_subcad_features(
    ops_trace: list[dict],
    cadquery_code: str = "",
) -> PureSubCADPlan:
    """Classify source evidence into pure SubCAD operation families.

    This is not a full geometric recognizer yet; it is the deterministic front
    door for the translator.  It maps common Zero-to-CAD construction calls to
    operation families requested by the pure coverage plan.
    """
    features: list[PlannedFeature] = []
    seen: set[tuple[str, str]] = set()

    def add(source: str, family: str, status: str, operation: str, reason: str, **evidence: Any) -> None:
        key = (source, operation)
        if key in seen:
            return
        seen.add(key)
        features.append(PlannedFeature(
            source=source,
            family=family,
            planner_status=status,
            operation=operation,
            reason=reason,
            evidence={k: v for k, v in evidence.items() if v is not None},
        ))

    trace_text = json.dumps(ops_trace, default=str).lower()
    code_text = cadquery_code.lower()
    combined = f"{trace_text}\n{code_text}"

    op_names = {str(op.get("op_name") or "").lower() for op in ops_trace if isinstance(op, dict)}
    functions = {str(op.get("function") or "").lower() for op in ops_trace if isinstance(op, dict)}
    has_tapered_extrude = (
        '"arg": "taper"' in trace_text
        or '"arg":"taper"' in trace_text
        or "taper=" in code_text
        or ".extrude(" in code_text and "taper" in code_text
    )

    if "box" in op_names or ".box(" in code_text:
        add("cadquery.box", "primitive", PLANNED_EXACT, "rectangular_stock",
            "box maps to rectangular SubCAD stock")
    if "cylinder" in op_names or ".cylinder(" in code_text:
        add("cadquery.cylinder", "primitive", PLANNED_EXACT, "cylindrical_stock",
            "cylinder maps to cylindrical SubCAD stock")
    if "cone" in op_names or ".cone(" in code_text:
        add("cadquery.cone", "axisymmetric", PLANNED_MULTI_PROCESS, "turn_profile",
            "cone/frustum maps to turning or mill-turn taper profile")
    if "sphere" in op_names or ".sphere(" in code_text:
        add("cadquery.sphere", "surface", PLANNED_TOLERANCE, "dome_mill",
            "sphere/dome maps to ball-endmill surface machining")

    if "rect" in op_names and ("cutblind" in op_names or ".cutblind(" in code_text):
        add("cadquery.rect.cutBlind", "cut", PLANNED_EXACT, "profile_pocket",
            "rectangular cut maps to profile pocket")
    if "circle" in op_names or ".circle(" in code_text:
        if "extrude" in op_names or ".extrude(" in code_text:
            if "union" in op_names or ".union(" in code_text or "combine" in op_names:
                add("cadquery.circle.extrude.union", "boss", PLANNED_EXACT, "machine_around_cylinder",
                    "circular extrusion joined to a body maps to machining around a retained cylinder")
            elif has_tapered_extrude:
                add("cadquery.circle.extrude.taper", "axisymmetric", PLANNED_MULTI_PROCESS, "turn_profile",
                    "tapered circle extrusion maps to a turning/frustum profile")
            else:
                add("cadquery.circle.extrude", "primitive", PLANNED_MULTI_PROCESS, "cylindrical_stock",
                    "circle extrusion maps to round stock or turning setup")
        if "cutblind" in op_names or "cut" in op_names or ".cutblind(" in code_text:
            add("cadquery.circle.cut", "cut", PLANNED_EXACT, "circular_pocket",
                "circular cut maps to circular pocket or bore")

    if any(name in op_names for name in {"polyline", "polygon", "lineto", "threpointarc", "threepointarc", "spline"}):
        status = PLANNED_TOLERANCE if "spline" in op_names else PLANNED_EXACT
        add("cadquery.profile", "profile", status, "profile_cutout",
            "non-rectangular sketch profile maps to profile machining")

    if "slot2d" in op_names:
        add("cadquery.slot2D", "profile", PLANNED_EXACT, "slot",
            "slot2D maps to SubCAD slot machining")

    if "hole" in op_names:
        add("cadquery.hole", "hole", PLANNED_EXACT, "drill",
            "hole maps to drill")
    if "cborehole" in op_names:
        add("cadquery.cboreHole", "hole", PLANNED_EXACT, "counterbore",
            "counterbore hole maps to drill plus counterbore")
    if "cskhole" in op_names:
        add("cadquery.cskHole", "hole", PLANNED_EXACT, "countersink",
            "countersink hole maps to drill plus countersink")

    if "chamfer" in op_names or ".chamfer(" in code_text:
        add("cadquery.chamfer", "edge_treatment", PLANNED_EXACT, "edge_chamfer",
            "selected-edge chamfer maps to edge_chamfer")
    if "fillet" in op_names or ".fillet(" in code_text:
        add("cadquery.fillet", "edge_treatment", PLANNED_TOLERANCE, "edge_fillet",
            "selected-edge fillet maps to ball/bull-nose finishing")

    if "union" in op_names or "combine" in op_names or ".union(" in code_text:
        add("cadquery.union", "retained_material", PLANNED_EXACT, "machine_around_profile",
            "constructive boss/pad/rib maps to machining around retained material")

    if "revolve" in op_names or ".revolve(" in code_text:
        add("cadquery.revolve", "axisymmetric", PLANNED_MULTI_PROCESS, "turn_profile",
            "revolved profile maps to turning or mill-turn")
    if "shell" in op_names or ".shell(" in code_text:
        shell_accessible = _shell_has_accessible_open_face(ops_trace, code_text)
        if shell_accessible:
            add("cadquery.shell", "thin_wall", PLANNED_MULTI_PROCESS, "thin_wall_pocket",
                "open shell maps to thin-wall pocket or hollow bore when accessible")
        else:
            add("cadquery.shell", "thin_wall", UNSUPPORTED_UNMACHINABLE, "thin_wall_pocket",
                "closed shell creates an inaccessible internal cavity for pure subtractive CNC")
    if "loft" in op_names or ".loft(" in code_text:
        add("cadquery.loft", "surface", PLANNED_TOLERANCE, "loft_mill",
            "loft maps to tolerance-machined surface operation")
    if "sweep" in op_names or ".sweep(" in code_text:
        add("cadquery.sweep", "surface", PLANNED_TOLERANCE, "sweep_mill",
            "sweep maps to tolerance-machined sweep operation")

    if any(token in combined for token in ("rarray", "polararray", "mirrorx", "mirrory", ".mirror(")):
        add("cadquery.pattern", "pattern", PLANNED_EXACT, "pattern",
            "feature pattern maps to repeated SubCAD operations")

    unsupported = [feature for feature in features if feature.planner_status == UNSUPPORTED_UNMACHINABLE]
    manual = [feature for feature in features if feature.planner_status == NEEDS_MANUAL_REVIEW]
    compatible = bool(features) and not unsupported and not manual
    return PureSubCADPlan(
        features=features,
        compatible=compatible,
        unsupported_count=len(unsupported),
        manual_review_count=len(manual),
    )


def _shell_has_accessible_open_face(ops_trace: list[dict], code_text: str) -> bool:
    """Best-effort gate for CadQuery shell accessibility.

    ``solid.shell(-t)`` without a selected face creates a closed internal void,
    which is not machinable from solid stock by pure subtractive CNC. Chained
    ``faces(...).shell(...)`` evidence is treated as an open/accessed shell.
    """
    for op in ops_trace:
        if not isinstance(op, dict):
            continue
        if str(op.get("op_name") or "").lower() != "shell":
            continue
        function = str(op.get("function") or "").lower()
        if ".faces" in function or function.endswith("faces.shell"):
            return True

    shell_index = code_text.find(".shell(")
    if shell_index < 0:
        return False
    recent_chain = code_text[max(0, shell_index - 120):shell_index]
    return ".faces(" in recent_chain


def compatibility_report(ops_trace: list[dict], cadquery_code: str = "") -> dict[str, Any]:
    """Back-compatible dict shape consumed by existing benchmark runner."""
    plan = plan_pure_subcad_features(ops_trace, cadquery_code)
    reasons = [
        feature.reason
        for feature in plan.features
        if feature.planner_status in {UNSUPPORTED_UNMACHINABLE, NEEDS_MANUAL_REVIEW}
    ]
    return {
        "compatible": plan.compatible,
        "reasons": reasons,
        "planner": plan.to_dict(),
    }
