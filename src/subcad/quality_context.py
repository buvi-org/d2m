"""Quality, inspection, tolerance, and collision policy context."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any, Optional


PROBE_METHODS = {"probe", "on_machine_probe", "touch_probe", "cmm"}


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _quality_path(quality: str | Path) -> Path:
    raw = Path(quality)
    if raw.exists():
        return raw

    candidates = [
        _repo_root() / str(quality),
        _repo_root() / "quality" / str(quality),
    ]
    if raw.suffix.lower() != ".json":
        candidates.append(_repo_root() / "quality" / f"{quality}.json")

    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"quality definition not found: {quality}")


def _as_list(value) -> list:
    if value in (None, ""):
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return [value]


def _normalized_methods(value) -> list[str]:
    return [str(method).lower() for method in _as_list(value)]


def _feature_name(feature_or_op) -> str:
    if isinstance(feature_or_op, dict):
        for key in ("feature_id", "feature", "name", "operation"):
            if feature_or_op.get(key):
                return str(feature_or_op[key])
        return ""
    if feature_or_op is None:
        return ""
    return str(feature_or_op)


def _normalize_tolerance_band(band: dict[str, Any]) -> dict[str, Any]:
    result = dict(band)
    nominal = result.get("nominal_mm")
    tolerance = result.get("tolerance_mm")
    if nominal is not None and tolerance is not None:
        nominal = float(nominal)
        tolerance = float(tolerance)
        result.setdefault("lower_mm", nominal - tolerance)
        result.setdefault("upper_mm", nominal + tolerance)
    elif nominal is not None and ("plus_mm" in result or "minus_mm" in result):
        nominal = float(nominal)
        plus = float(result.get("plus_mm") or 0.0)
        minus = float(result.get("minus_mm") or 0.0)
        result.setdefault("lower_mm", nominal - minus)
        result.setdefault("upper_mm", nominal + plus)
    return result


def _normalize_feature_map(value) -> dict[str, dict[str, Any]]:
    if not value:
        return {}
    if isinstance(value, dict):
        return {
            str(name): dict(spec) if isinstance(spec, dict) else {"value": spec}
            for name, spec in value.items()
        }
    result = {}
    for item in _as_list(value):
        if not isinstance(item, dict):
            continue
        name = item.get("name") or item.get("feature") or item.get("feature_id")
        if name:
            result[str(name)] = dict(item)
    return result


def _normalize_collision_policy(policy: Optional[dict[str, Any]]) -> dict[str, Any]:
    policy = dict(policy or {})
    enabled = bool(policy.get("enabled", policy.get("required", False)))
    required = bool(policy.get("required", False))
    default_clearance = float(policy.get("clearance_mm", policy.get("min_clearance_mm", 2.0)))
    policy["enabled"] = enabled
    policy["required"] = required
    policy["min_clearance_mm"] = float(policy.get("min_clearance_mm", default_clearance))
    policy["clearance_mm"] = default_clearance
    policy.setdefault("holder_check", True)
    policy.setdefault("fixture_check", True)
    policy.setdefault("toolpath_required", required)
    policy.setdefault("severity", "error" if required else "warning")
    policy.setdefault("holder_clearance_mm", default_clearance)
    policy.setdefault("fixture_clearance_mm", default_clearance)
    policy.setdefault("rapid_clearance_mm", default_clearance)
    return policy


@dataclass
class QualityContext:
    """Serializable quality requirements for a process plan."""

    schema_version: str = "subcad.quality_context.v1"
    quality_id: str = "quality"
    tolerances: dict[str, Any] = field(default_factory=dict)
    inspection: dict[str, Any] = field(default_factory=dict)
    surface_finish: dict[str, Any] = field(default_factory=dict)
    critical_dimensions: list[dict[str, Any]] = field(default_factory=list)
    critical_features: dict[str, dict[str, Any]] = field(default_factory=dict)
    process_capability: dict[str, Any] = field(default_factory=dict)
    collision_policy: dict[str, Any] = field(default_factory=dict)
    source: str = ""

    @classmethod
    def from_json(cls, quality: str | Path) -> "QualityContext":
        path = _quality_path(quality)
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        return cls.from_dict(data, source=str(path))

    @classmethod
    def from_dict(cls, data: dict[str, Any], source: str = "") -> "QualityContext":
        if "quality" in data and isinstance(data["quality"], dict):
            data = data["quality"]

        tolerances = dict(data.get("tolerances") or {})
        if isinstance(tolerances.get("default"), dict):
            tolerances["default"] = _normalize_tolerance_band(tolerances["default"])
        tolerance_features = _normalize_feature_map(tolerances.get("features"))
        if tolerance_features:
            tolerances["features"] = {
                name: _normalize_tolerance_band(spec)
                for name, spec in tolerance_features.items()
            }

        return cls(
            schema_version=str(data.get("schema_version") or "subcad.quality_context.v1"),
            quality_id=str(data.get("quality_id") or data.get("id") or "quality"),
            tolerances=tolerances,
            inspection=dict(data.get("inspection") or {}),
            surface_finish=dict(data.get("surface_finish") or data.get("finish") or {}),
            critical_dimensions=[
                dict(item) for item in _as_list(data.get("critical_dimensions"))
                if isinstance(item, dict)
            ],
            critical_features=_normalize_feature_map(data.get("critical_features")),
            process_capability=dict(data.get("process_capability") or {}),
            collision_policy=_normalize_collision_policy(data.get("collision_policy")),
            source=str(data.get("source") or source or ""),
        )

    def tolerance_bands(self, feature=None) -> dict[str, Any]:
        """Return normalized tolerance bands, optionally emphasizing one feature."""
        bands: dict[str, Any] = {}
        default = self.tolerances.get("default")
        if isinstance(default, dict):
            bands["default"] = _normalize_tolerance_band(default)

        features = _normalize_feature_map(self.tolerances.get("features"))
        for name, spec in features.items():
            bands[name] = _normalize_tolerance_band(spec)

        requested = _feature_name(feature)
        if requested:
            for item in self.critical_dimensions:
                item_name = str(item.get("name") or item.get("feature") or item.get("feature_id") or "")
                if requested in {item_name, str(item.get("feature") or "")}:
                    bands.setdefault(item_name or requested, _normalize_tolerance_band(item))
            if requested in self.critical_features:
                bands.setdefault(requested, dict(self.critical_features[requested]))
        return bands

    def required_inspection_methods(self, feature=None) -> list[str]:
        """Return required inspection methods for a feature or operation."""
        requested = _feature_name(feature)
        methods: list[str] = []

        methods.extend(_normalized_methods(
            self.inspection.get("methods", self.inspection.get("required_methods"))
        ))

        for requirement in _as_list(self.inspection.get("requirements")):
            if not isinstance(requirement, dict):
                continue
            target = str(requirement.get("target") or requirement.get("feature") or "")
            if not requested or requested == target:
                methods.extend(_normalized_methods(requirement.get("methods")))

        bands = self.tolerance_bands(requested)
        for name, band in bands.items():
            if name in {"default", requested} or not requested:
                methods.extend(_normalized_methods(band.get("methods")))

        finish_features = _normalize_feature_map(self.surface_finish.get("features"))
        if requested in finish_features:
            methods.extend(_normalized_methods(finish_features[requested].get("methods")))

        for item in self.critical_dimensions:
            if not isinstance(item, dict):
                continue
            targets = {
                str(item.get("name") or ""),
                str(item.get("feature") or ""),
                str(item.get("feature_id") or ""),
            }
            if requested and requested not in targets:
                continue
            methods.extend(_normalized_methods(item.get("methods")))

        if requested in self.critical_features:
            methods.extend(_normalized_methods(self.critical_features[requested].get("methods")))

        unique = []
        for method in methods:
            if method and method not in unique:
                unique.append(method)
        return unique

    def needs_probe(self, feature=None) -> bool:
        """Return True when inspection intent needs probing/CMM-style measurement."""
        requested = _feature_name(feature)
        if bool(self.inspection.get("requires_probe")):
            return True

        for method in self.required_inspection_methods(requested):
            if method in PROBE_METHODS or "probe" in method:
                return True

        bands = self.tolerance_bands(requested)
        for name, band in bands.items():
            if name in {"default", requested} or not requested:
                if band.get("requires_probe"):
                    return True

        for requirement in _as_list(self.inspection.get("requirements")):
            if not isinstance(requirement, dict):
                continue
            target = str(requirement.get("target") or requirement.get("feature") or "")
            if (not requested or requested == target) and requirement.get("requires_probe"):
                return True
        return False

    def collision_required(self, operation: Optional[dict[str, Any]] = None) -> bool:
        """Return True when collision validation is mandatory."""
        if operation and (
            operation.get("requires_collision_check")
            or operation.get("collision_check_required")
        ):
            return True
        return bool(self.collision_policy.get("required"))

    def clearance_limits(self) -> dict[str, float]:
        """Return normalized clearance requirements by category."""
        policy = self.collision_policy
        return {
            "min_clearance_mm": float(policy.get("min_clearance_mm", 2.0)),
            "holder_clearance_mm": float(policy.get("holder_clearance_mm", 2.0)),
            "fixture_clearance_mm": float(policy.get("fixture_clearance_mm", 2.0)),
            "rapid_clearance_mm": float(policy.get("rapid_clearance_mm", 2.0)),
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "quality_id": self.quality_id,
            "tolerances": dict(self.tolerances),
            "inspection": dict(self.inspection),
            "surface_finish": dict(self.surface_finish),
            "critical_dimensions": list(self.critical_dimensions),
            "critical_features": dict(self.critical_features),
            "process_capability": dict(self.process_capability),
            "collision_policy": dict(self.collision_policy),
            "source": self.source,
        }


def load_quality_context(quality) -> QualityContext:
    """Return a ``QualityContext`` from a path, id, dict, or context object."""
    if isinstance(quality, QualityContext):
        return quality
    if isinstance(quality, dict):
        return QualityContext.from_dict(quality)
    return QualityContext.from_json(quality)


def load_collision_policy(policy) -> dict[str, Any]:
    """Return a normalized collision policy dictionary."""
    if policy is None:
        return {}
    if hasattr(policy, "to_dict"):
        policy = policy.to_dict()
    if not isinstance(policy, dict):
        raise TypeError("collision policy must be a dictionary or provide to_dict()")
    return _normalize_collision_policy(policy)


def tolerance_bands(quality, feature=None) -> dict[str, Any]:
    return load_quality_context(quality).tolerance_bands(feature)


def required_inspection_methods(quality, feature=None) -> list[str]:
    return load_quality_context(quality).required_inspection_methods(feature)


def needs_probe(quality, feature=None) -> bool:
    return load_quality_context(quality).needs_probe(feature)


def collision_required(quality, operation: Optional[dict[str, Any]] = None) -> bool:
    return load_quality_context(quality).collision_required(operation)


def clearance_limits(quality) -> dict[str, float]:
    return load_quality_context(quality).clearance_limits()
