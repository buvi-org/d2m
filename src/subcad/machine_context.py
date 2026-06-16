"""Machine context helpers for SubCAD process plans.

This module keeps SubCAD's authoring layer independent from the heavier
simulation machine model while still using the same machine JSON files.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any, Optional


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _machine_path(machine: str | Path) -> Path:
    raw = Path(machine)
    if raw.exists():
        return raw

    candidates = [
        _repo_root() / str(machine),
        _repo_root() / "machines" / str(machine),
    ]
    if raw.suffix.lower() != ".json":
        candidates.append(_repo_root() / "machines" / f"{machine}.json")

    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"machine definition not found: {machine}")


def _machine_id_from_path(path: Optional[Path], data: dict[str, Any]) -> str:
    if data.get("machine_id"):
        return str(data["machine_id"])
    if path is not None:
        return path.stem
    name = str(data.get("name") or data.get("model") or "machine").strip()
    return name.lower().replace(" ", "_").replace("-", "_")


MILL_OPERATION_FAMILIES = [
    "face_mill",
    "pocket",
    "circular_pocket",
    "spot_drill",
    "drill",
    "peck_drill",
    "ream",
    "bore",
    "tap",
    "thread_mill",
    "threaded_hole",
    "chamfer",
    "contour",
    "slot",
    "t_slot",
    "dovetail",
    "groove",
    "surface_3d",
    "deburr",
    "spot_face",
    "edge_chamfer",
    "edge_fillet",
    "profile_pocket",
    "profile_cutout",
    "profile_contour",
    "machine_around_profile",
    "machine_around_profiles",
    "machine_around_cylinder",
    "rib",
    "pad",
    "thin_wall_pocket",
    "thin_wall_shell",
]

FIVE_AXIS_OPERATION_FAMILIES = [
    "surface_mill",
    "sweep_mill",
    "loft_mill",
    "dome_mill",
]

TURN_OPERATION_FAMILIES = [
    "turn_profile",
    "turn_face",
    "turn_od",
    "turn_id",
    "turn_groove",
    "turn_thread",
]

MILL_TURN_OPERATION_FAMILIES = [
    "mill_turn_setup",
    "hollow_bore",
    "tube_profile",
]

WIRE_OPERATION_FAMILIES = [
    "wire_cut_profile",
    "wire_cut_internal",
]


def _unique(values) -> list:
    result = []
    for value in values or []:
        if value not in result:
            result.append(value)
    return result


def _default_operation_families(processes: list[str]) -> list[str]:
    families = list(MILL_OPERATION_FAMILIES)
    lowered = {str(process).lower() for process in processes or []}
    if "5axis" in lowered or "mill_turn" in lowered:
        families.extend(FIVE_AXIS_OPERATION_FAMILIES)
    if "turn" in lowered or "mill_turn" in lowered:
        families.extend(TURN_OPERATION_FAMILIES)
    if "mill_turn" in lowered:
        families.extend(MILL_TURN_OPERATION_FAMILIES)
    if "wire" in lowered:
        families.extend(WIRE_OPERATION_FAMILIES)
    return _unique(families)


def _capabilities_with_defaults(data: dict[str, Any], inferred: dict[str, Any]) -> dict[str, Any]:
    explicit = dict(data.get("capabilities") or {})
    capabilities = dict(inferred)
    capabilities.update(explicit)

    processes = list(capabilities.get("processes") or inferred.get("processes") or [])
    capabilities["processes"] = _unique(processes)
    capabilities["operation_families"] = _unique(
        capabilities.get("operation_families") or _default_operation_families(processes)
    )
    capabilities["controller_cycles"] = _unique(capabilities.get("controller_cycles") or [])
    capabilities["coolant"] = _unique(capabilities.get("coolant") or [])
    if "probing" not in capabilities:
        capabilities["probing"] = False
    capabilities.setdefault("tool_interface", "")
    capabilities.setdefault("tool_capacity", None)
    capabilities.setdefault("schema_version", "subcad.machine_capabilities.v1")
    return capabilities


@dataclass
class MachineContext:
    """Lightweight machine capability summary stored in a SubCAD plan."""

    machine_id: str
    name: str
    manufacturer: str = ""
    model: str = ""
    source: str = ""
    axes: list[str] = field(default_factory=list)
    linear_limits: dict[str, tuple[float, float]] = field(default_factory=dict)
    rotary_limits: dict[str, tuple[float, float]] = field(default_factory=dict)
    axis_limits: dict[str, dict[str, Any]] = field(default_factory=dict)
    spindle: dict[str, Any] = field(default_factory=dict)
    capabilities: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_json(cls, machine: str | Path) -> "MachineContext":
        path = _machine_path(machine)
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        return cls.from_dict(data, source=str(path))

    @classmethod
    def from_dict(cls, data: dict[str, Any], source: str = "") -> "MachineContext":
        if "components" not in data and "machine_id" in data:
            capabilities = _capabilities_with_defaults(
                data,
                {"processes": data.get("capabilities", {}).get("processes", [])},
            )
            return cls(
                machine_id=str(data.get("machine_id") or data.get("id") or "machine"),
                name=str(data.get("name") or data.get("machine_id") or "Machine"),
                manufacturer=str(data.get("manufacturer") or ""),
                model=str(data.get("model") or data.get("model_name") or ""),
                source=str(data.get("source") or source or ""),
                axes=list(data.get("axes") or []),
                linear_limits={
                    str(axis).upper(): (float(limits[0]), float(limits[1]))
                    for axis, limits in (data.get("linear_limits") or {}).items()
                    if isinstance(limits, (list, tuple)) and len(limits) == 2
                },
                rotary_limits={
                    str(axis).upper(): (float(limits[0]), float(limits[1]))
                    for axis, limits in (data.get("rotary_limits") or {}).items()
                    if isinstance(limits, (list, tuple)) and len(limits) == 2
                },
                axis_limits=dict(data.get("axis_limits") or {}),
                spindle=dict(data.get("spindle") or {}),
                capabilities=capabilities,
            )

        axes: list[str] = []
        linear_limits: dict[str, tuple[float, float]] = {}
        rotary_limits: dict[str, tuple[float, float]] = {}
        axis_limits: dict[str, dict[str, Any]] = {}
        spindle: dict[str, Any] = {}

        for component in data.get("components") or []:
            axis = str(component.get("axis") or "").upper()
            ctype = component.get("type")
            limits = component.get("limits")
            if axis:
                axes.append(axis)
            if axis and isinstance(limits, list) and len(limits) == 2:
                limit_pair = (float(limits[0]), float(limits[1]))
                axis_limits[axis] = {
                    "limits": [limit_pair[0], limit_pair[1]],
                    "max_feed": component.get("max_feed"),
                    "rapid_feed": component.get("rapid_feed"),
                    "max_rpm": component.get("max_rpm"),
                    "type": ctype,
                }
                if ctype == "linear_axis":
                    linear_limits[axis] = limit_pair
                elif ctype == "rotary_axis":
                    rotary_limits[axis] = limit_pair
            if ctype == "spindle":
                spindle = {
                    "max_rpm": component.get("max_rpm"),
                    "max_power_kw": component.get("max_power_kw"),
                    "max_torque_nm": component.get("max_torque_nm"),
                    "label": component.get("label", ""),
                    "spindle_nose_to_gauge_mm": component.get("spindle_nose_to_gauge_mm"),
                }

        axes = sorted(set(axes), key="XYZABCUVW".find)
        rotary_axes = sorted(rotary_limits.keys(), key="ABC".find)
        processes = ["mill", "indexed_3axis"]
        if len(rotary_axes) >= 2:
            processes.append("5axis")

        path = Path(source) if source else None
        inferred_capabilities = {
            "processes": processes,
            "rotary_axes": rotary_axes,
        }
        capabilities = _capabilities_with_defaults(data, inferred_capabilities)

        return cls(
            machine_id=_machine_id_from_path(path, data),
            name=str(data.get("name") or data.get("model") or "Machine"),
            manufacturer=str(data.get("manufacturer") or ""),
            model=str(data.get("model") or ""),
            source=source,
            axes=axes,
            linear_limits=linear_limits,
            rotary_limits=rotary_limits,
            axis_limits=axis_limits,
            spindle=spindle,
            capabilities=capabilities,
        )

    @property
    def rotary_axes(self) -> list[str]:
        return list(self.rotary_limits.keys())

    def to_dict(self) -> dict[str, Any]:
        return {
            "machine_id": self.machine_id,
            "name": self.name,
            "manufacturer": self.manufacturer,
            "model": self.model,
            "source": self.source,
            "axes": list(self.axes),
            "linear_limits": {
                axis: [limits[0], limits[1]]
                for axis, limits in self.linear_limits.items()
            },
            "rotary_limits": {
                axis: [limits[0], limits[1]]
                for axis, limits in self.rotary_limits.items()
            },
            "axis_limits": dict(self.axis_limits),
            "rotary_axes": self.rotary_axes,
            "spindle": dict(self.spindle),
            "capabilities": dict(self.capabilities),
        }


def load_machine_context(machine) -> MachineContext:
    """Return a ``MachineContext`` from a path, id, dict, or context object."""
    if isinstance(machine, MachineContext):
        return machine
    if isinstance(machine, dict):
        return MachineContext.from_dict(machine)
    return MachineContext.from_json(machine)
