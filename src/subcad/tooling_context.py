"""Tool assembly and magazine context helpers for SubCAD process plans.

This module is intentionally independent from process-plan and validation
integration. It provides JSON-friendly tooling metadata and small query helpers
that downstream validation can call without depending on simulation classes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any, Optional


SCHEMA_VERSION = "subcad.tooling_context.v1"
MAGAZINE_SCHEMA_VERSION = "subcad.tool_magazine.v1"


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _tooling_path(tooling: str | Path) -> Path:
    raw = Path(tooling)
    if raw.exists():
        return raw

    candidates = [
        _repo_root() / str(tooling),
        _repo_root() / "tooling" / str(tooling),
    ]
    if raw.suffix.lower() != ".json":
        candidates.append(_repo_root() / "tooling" / f"{tooling}.json")

    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"tooling definition not found: {tooling}")


def _first_value(data: dict[str, Any], *keys: str, default=None):
    for key in keys:
        if key in data and data[key] is not None:
            return data[key]
    return default


def _as_float(value, default: Optional[float] = None) -> Optional[float]:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _as_int(value, default: Optional[int] = None) -> Optional[int]:
    try:
        if value is None or value == "":
            return default
        return int(value)
    except (TypeError, ValueError):
        return default


def _as_bool(value, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    if isinstance(value, (int, float)):
        return bool(value)
    return str(value).strip().lower() in {"1", "true", "yes", "y", "on"}


def _normalize_interface(value) -> str:
    return str(value or "").strip().upper()


def _operation_tool_type(op: dict) -> str:
    tool = op.get("tool") if isinstance(op.get("tool"), dict) else {}
    assembly = tool.get("assembly") if isinstance(tool.get("assembly"), dict) else {}
    for source in (op, tool, assembly):
        for key in ("tool_type", "type"):
            if source.get(key):
                return str(source[key]).strip()
    return ""


def _operation_tool_id(op: dict) -> str:
    tool = op.get("tool") if isinstance(op.get("tool"), dict) else {}
    assembly = tool.get("assembly") if isinstance(tool.get("assembly"), dict) else {}
    for source in (op, tool, assembly):
        for key in ("tool_id", "id", "catalog_id", "selected_tool_id"):
            if source.get(key):
                return str(source[key]).strip()
    return ""


def _operation_tool_diameter(op: dict) -> Optional[float]:
    tool = op.get("tool") if isinstance(op.get("tool"), dict) else {}
    assembly = tool.get("assembly") if isinstance(tool.get("assembly"), dict) else {}
    for source in (op, tool, assembly):
        value = _first_value(
            source,
            "diameter",
            "diameter_mm",
            "tool_diameter_mm",
            "cutter_diameter_mm",
        )
        diameter = _as_float(value)
        if diameter is not None:
            return diameter
    return None


def required_tool_types(process_plan_or_operations) -> list[str]:
    """Return required tool types from a plan dict or operation list."""
    if isinstance(process_plan_or_operations, dict):
        operations = list(process_plan_or_operations.get("operations") or [])
        operations.extend(process_plan_or_operations.get("tools_used") or [])
    else:
        operations = process_plan_or_operations or []

    result: list[str] = []
    for op in operations:
        if not isinstance(op, dict):
            continue
        tool_type = _operation_tool_type(op)
        if tool_type and tool_type not in result:
            result.append(tool_type)
    return result


@dataclass
class ToolAssembly:
    """A cutter, holder, and machine interface as loaded for a shop context."""

    tool_id: str
    tool_type: str
    diameter_mm: float
    flutes: int = 0
    material: str = ""
    coating: str = ""
    stickout_mm: float = 0.0
    holder: str = ""
    interface: str = ""
    coolant_through: bool = False
    max_rpm: Optional[float] = None
    max_feed_mm_per_min: Optional[float] = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ToolAssembly":
        """Build a tool assembly from exact or legacy SubCAD field names."""
        assembly = data.get("assembly") if isinstance(data.get("assembly"), dict) else {}
        safe_limits = data.get("safe_limits") if isinstance(data.get("safe_limits"), dict) else {}

        merged = dict(assembly)
        merged.update(data)

        tool_id = str(_first_value(
            merged,
            "id",
            "tool_id",
            "catalog_id",
            "selected_tool_id",
            default="",
        )).strip()
        tool_type = str(_first_value(
            merged,
            "type",
            "tool_type",
            default="",
        )).strip()
        diameter = _as_float(_first_value(
            merged,
            "diameter",
            "diameter_mm",
            "tool_diameter_mm",
            "cutter_diameter_mm",
            default=0.0,
        ), 0.0) or 0.0

        flutes = _as_int(_first_value(merged, "flutes", "num_flutes"), 0) or 0
        stickout = _as_float(
            _first_value(merged, "stickout", "stickout_mm", default=0.0),
            0.0,
        ) or 0.0
        max_rpm = _as_float(_first_value(merged, "max_rpm", default=safe_limits.get("max_rpm")))
        max_feed = _as_float(_first_value(
            merged,
            "max_feed_mm_per_min",
            "max_feed",
            "feed_rate_mm_per_min",
            default=safe_limits.get(
                "max_feed_mm_per_min",
                safe_limits.get("feed_rate_mm_per_min"),
            ),
        ))

        known = {
            "assembly",
            "safe_limits",
            "id",
            "tool_id",
            "catalog_id",
            "selected_tool_id",
            "type",
            "tool_type",
            "diameter",
            "diameter_mm",
            "tool_diameter_mm",
            "cutter_diameter_mm",
            "flutes",
            "num_flutes",
            "material",
            "coating",
            "stickout",
            "stickout_mm",
            "holder",
            "holder_id",
            "interface",
            "tool_interface",
            "holder_interface",
            "spindle_interface",
            "coolant_through",
            "through_coolant",
            "through_spindle_coolant",
            "max_rpm",
            "max_feed_mm_per_min",
            "max_feed",
            "feed_rate_mm_per_min",
        }
        metadata = {
            key: value
            for key, value in data.items()
            if key not in known and value is not None
        }

        return cls(
            tool_id=tool_id,
            tool_type=tool_type,
            diameter_mm=diameter,
            flutes=flutes,
            material=str(_first_value(merged, "material", default="") or ""),
            coating=str(_first_value(merged, "coating", default="") or ""),
            stickout_mm=stickout,
            holder=str(_first_value(merged, "holder", "holder_id", default="") or ""),
            interface=str(_first_value(
                merged,
                "interface",
                "tool_interface",
                "holder_interface",
                "spindle_interface",
                default="",
            ) or ""),
            coolant_through=_as_bool(_first_value(
                merged,
                "coolant_through",
                "through_coolant",
                "through_spindle_coolant",
            )),
            max_rpm=max_rpm,
            max_feed_mm_per_min=max_feed,
            metadata=metadata,
        )

    @property
    def id(self) -> str:
        return self.tool_id

    @property
    def type(self) -> str:
        return self.tool_type

    @property
    def diameter(self) -> float:
        return self.diameter_mm

    @property
    def stickout(self) -> float:
        return self.stickout_mm

    def matches_type(self, tool_type: str) -> bool:
        return self.tool_type.lower() == str(tool_type or "").lower()

    def interface_matches(self, required_interface: str) -> bool:
        if not required_interface or not self.interface:
            return True
        return _normalize_interface(self.interface) == _normalize_interface(required_interface)

    def supports_rpm(self, rpm) -> bool:
        requested = _as_float(rpm)
        return requested is None or self.max_rpm is None or requested <= self.max_rpm + 1e-6

    def supports_feed(self, feed_mm_per_min) -> bool:
        requested = _as_float(feed_mm_per_min)
        limit = self.max_feed_mm_per_min
        return requested is None or limit is None or requested <= limit + 1e-6

    def supports_coolant(self, coolant: str) -> bool:
        coolant_mode = str(coolant or "").lower()
        if coolant_mode in {"", "none", "off", "false", "flood", "mist", "air_blast"}:
            return True
        if coolant_mode in {"through_spindle", "through_tool", "coolant_through"}:
            return self.coolant_through
        return True

    def to_dict(self) -> dict[str, Any]:
        result = {
            "id": self.tool_id,
            "type": self.tool_type,
            "diameter": self.diameter_mm,
            "diameter_mm": self.diameter_mm,
            "flutes": self.flutes,
            "material": self.material,
            "coating": self.coating,
            "stickout": self.stickout_mm,
            "stickout_mm": self.stickout_mm,
            "holder": self.holder,
            "interface": self.interface,
            "coolant_through": self.coolant_through,
            "tool_id": self.tool_id,
            "tool_type": self.tool_type,
            "tool_diameter_mm": self.diameter_mm,
            "holder_id": self.holder,
        }
        if self.max_rpm is not None:
            result["max_rpm"] = self.max_rpm
        if self.max_feed_mm_per_min is not None:
            result["max_feed_mm_per_min"] = self.max_feed_mm_per_min
        if self.metadata:
            result["metadata"] = dict(self.metadata)
        return result


@dataclass
class MagazineSlot:
    """One magazine pocket and the tool loaded into it."""

    slot: int
    tool_id: str = ""
    label: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MagazineSlot":
        return cls(
            slot=_as_int(_first_value(data, "slot", "pocket", "station", default=0), 0) or 0,
            tool_id=str(_first_value(data, "tool_id", "id", "catalog_id", default="") or ""),
            label=str(_first_value(data, "label", "name", default="") or ""),
        )

    def to_dict(self) -> dict[str, Any]:
        result = {"slot": self.slot, "tool_id": self.tool_id}
        if self.label:
            result["label"] = self.label
        return result


@dataclass
class ToolMagazine:
    """Tool magazine capacity, machine interface, and loaded slots."""

    magazine_id: str = ""
    capacity: Optional[int] = None
    interface: str = ""
    slots: list[MagazineSlot] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ToolMagazine":
        raw_slots = data.get("slots") or data.get("pockets") or []
        slots: list[MagazineSlot] = []

        if isinstance(raw_slots, dict):
            for slot, tool_id in raw_slots.items():
                if isinstance(tool_id, dict):
                    slot_data = {"slot": slot, **tool_id}
                else:
                    slot_data = {"slot": slot, "tool_id": tool_id}
                slots.append(MagazineSlot.from_dict(slot_data))
        else:
            for entry in raw_slots:
                if isinstance(entry, dict):
                    slots.append(MagazineSlot.from_dict(entry))

        capacity = _as_int(data.get("capacity"))
        if capacity is None and slots:
            capacity = max(slot.slot for slot in slots)

        return cls(
            magazine_id=str(_first_value(data, "id", "magazine_id", "name", default="") or ""),
            capacity=capacity,
            interface=str(_first_value(
                data,
                "interface",
                "tool_interface",
                "holder_interface",
                default="",
            ) or ""),
            slots=sorted(slots, key=lambda slot: slot.slot),
        )

    @property
    def id(self) -> str:
        return self.magazine_id

    @property
    def loaded_tool_ids(self) -> list[str]:
        return [slot.tool_id for slot in self.slots if slot.tool_id]

    @property
    def loaded_count(self) -> int:
        return len(self.loaded_tool_ids)

    def slot_for(self, tool_id: str) -> Optional[MagazineSlot]:
        wanted = str(tool_id or "")
        for slot in self.slots:
            if slot.tool_id == wanted:
                return slot
        return None

    def has_tool(self, tool_id: str) -> bool:
        return self.slot_for(tool_id) is not None

    def has_capacity(self, required_count: Optional[int] = None) -> bool:
        if self.capacity is None:
            return True
        count = required_count if required_count is not None else self.loaded_count
        return count <= self.capacity

    def interface_matches(self, required_interface: str) -> bool:
        if not required_interface or not self.interface:
            return True
        return _normalize_interface(self.interface) == _normalize_interface(required_interface)

    def slot_issues(self) -> list[dict[str, Any]]:
        issues: list[dict[str, Any]] = []
        seen: set[int] = set()
        for slot in self.slots:
            if slot.slot <= 0:
                issues.append({"code": "magazine_slot_invalid", "slot": slot.slot})
            if self.capacity is not None and slot.slot > self.capacity:
                issues.append({
                    "code": "magazine_slot_over_capacity",
                    "slot": slot.slot,
                    "capacity": self.capacity,
                    "tool_id": slot.tool_id,
                })
            if slot.slot in seen:
                issues.append({"code": "magazine_slot_duplicate", "slot": slot.slot})
            seen.add(slot.slot)
        return issues

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": MAGAZINE_SCHEMA_VERSION,
            "id": self.magazine_id,
            "capacity": self.capacity,
            "interface": self.interface,
            "slots": [slot.to_dict() for slot in self.slots],
        }


@dataclass
class ToolingContext:
    """Loaded tool assemblies plus an optional magazine assignment."""

    tools: list[ToolAssembly] = field(default_factory=list)
    magazine: Optional[ToolMagazine] = None
    name: str = ""
    source: str = ""
    schema_version: str = SCHEMA_VERSION

    @classmethod
    def from_json(
        cls,
        tooling: str | Path,
        magazine: Optional[str | Path | dict[str, Any] | ToolMagazine] = None,
    ) -> "ToolingContext":
        path = _tooling_path(tooling)
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        return cls.from_dict(data, source=str(path), magazine=magazine)

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
        source: str = "",
        magazine: Optional[str | Path | dict[str, Any] | ToolMagazine] = None,
    ) -> "ToolingContext":
        raw_tools = (
            data.get("tools")
            or data.get("tool_assemblies")
            or data.get("assemblies")
            or []
        )
        if not raw_tools and ("id" in data or "tool_id" in data) and ("type" in data or "tool_type" in data):
            raw_tools = [data]

        tools = [
            ToolAssembly.from_dict(entry)
            for entry in raw_tools
            if isinstance(entry, dict)
        ]

        resolved_magazine = _load_magazine(magazine)
        if resolved_magazine is None and isinstance(data.get("magazine"), dict):
            resolved_magazine = ToolMagazine.from_dict(data["magazine"])

        return cls(
            tools=tools,
            magazine=resolved_magazine,
            name=str(data.get("name") or ""),
            source=str(data.get("source") or source or ""),
            schema_version=str(data.get("schema_version") or SCHEMA_VERSION),
        )

    @property
    def tool_ids(self) -> list[str]:
        return [tool.tool_id for tool in self.tools if tool.tool_id]

    @property
    def tool_types(self) -> list[str]:
        result: list[str] = []
        for tool in self.tools:
            if tool.tool_type and tool.tool_type not in result:
                result.append(tool.tool_type)
        return result

    def get_tool(self, tool_id: str) -> Optional[ToolAssembly]:
        wanted = str(tool_id or "")
        for tool in self.tools:
            if tool.tool_id == wanted:
                return tool
        wanted_lower = wanted.lower()
        for tool in self.tools:
            if tool.tool_id.lower() == wanted_lower:
                return tool
        return None

    def find_by_id(self, tool_id: str) -> Optional[ToolAssembly]:
        return self.get_tool(tool_id)

    def tools_by_type(self, tool_type: str) -> list[ToolAssembly]:
        return [tool for tool in self.tools if tool.matches_type(tool_type)]

    def find_by_type(self, tool_type: str) -> list[ToolAssembly]:
        return self.tools_by_type(tool_type)

    def tool_for_operation(self, operation: dict) -> Optional[ToolAssembly]:
        tool_id = _operation_tool_id(operation)
        if tool_id:
            tool = self.get_tool(tool_id)
            if tool is not None:
                return tool

        tool_type = _operation_tool_type(operation)
        diameter = _operation_tool_diameter(operation)
        candidates = self.tools_by_type(tool_type)
        if not candidates:
            return None
        if diameter is None:
            return candidates[0]
        for tool in candidates:
            if abs(tool.diameter_mm - diameter) < 0.001:
                return tool
        return candidates[0]

    def required_tool_types(self, process_plan_or_operations) -> list[str]:
        return required_tool_types(process_plan_or_operations)

    def missing_tool_types(self, process_plan_or_operations) -> list[str]:
        available = {tool_type.lower() for tool_type in self.tool_types}
        return [
            tool_type
            for tool_type in required_tool_types(process_plan_or_operations)
            if tool_type.lower() not in available
        ]

    def has_required_tool_types(self, process_plan_or_operations) -> bool:
        return not self.missing_tool_types(process_plan_or_operations)

    def has_capacity(self, required_count: Optional[int] = None) -> bool:
        if self.magazine is None:
            return True
        if required_count is None:
            required_count = len(self.magazine.loaded_tool_ids or self.tool_ids)
        return self.magazine.has_capacity(required_count)

    def capacity_issues(self, required_count: Optional[int] = None) -> list[dict[str, Any]]:
        if self.magazine is None:
            return []
        issues = self.magazine.slot_issues()
        if required_count is not None and not self.magazine.has_capacity(required_count):
            issues.append({
                "code": "magazine_capacity_exceeded",
                "required_tool_count": required_count,
                "capacity": self.magazine.capacity,
            })
        elif required_count is None and not self.magazine.has_capacity():
            issues.append({
                "code": "magazine_capacity_exceeded",
                "required_tool_count": self.magazine.loaded_count,
                "capacity": self.magazine.capacity,
            })
        return issues

    def interface_mismatches(self, required_interface: str = "") -> list[dict[str, Any]]:
        issues: list[dict[str, Any]] = []
        expected = required_interface
        if self.magazine is not None:
            if required_interface and not self.magazine.interface_matches(required_interface):
                issues.append({
                    "code": "magazine_interface_mismatch",
                    "magazine_id": self.magazine.magazine_id,
                    "magazine_interface": self.magazine.interface,
                    "required_interface": required_interface,
                })
            expected = expected or self.magazine.interface

        if not expected:
            return issues

        tool_ids = self.magazine.loaded_tool_ids if self.magazine else self.tool_ids
        tools = [self.get_tool(tool_id) for tool_id in tool_ids] if tool_ids else self.tools
        for tool in [tool for tool in tools if tool is not None]:
            if not tool.interface:
                issues.append({
                    "code": "tool_interface_missing",
                    "tool_id": tool.tool_id,
                    "required_interface": expected,
                })
            elif not tool.interface_matches(expected):
                issues.append({
                    "code": "tool_interface_mismatch",
                    "tool_id": tool.tool_id,
                    "tool_interface": tool.interface,
                    "required_interface": expected,
                })
        return issues

    def interfaces_ok(self, required_interface: str = "") -> bool:
        return not self.interface_mismatches(required_interface)

    def max_rpm_for(self, tool_id: str) -> Optional[float]:
        tool = self.get_tool(tool_id)
        return tool.max_rpm if tool else None

    def max_feed_for(self, tool_id: str) -> Optional[float]:
        tool = self.get_tool(tool_id)
        return tool.max_feed_mm_per_min if tool else None

    def supports_rpm(self, tool_id: str, rpm) -> bool:
        tool = self.get_tool(tool_id)
        return tool is not None and tool.supports_rpm(rpm)

    def supports_feed(self, tool_id: str, feed_mm_per_min) -> bool:
        tool = self.get_tool(tool_id)
        return tool is not None and tool.supports_feed(feed_mm_per_min)

    def coolant_through_supported(self, tool_id: str) -> bool:
        tool = self.get_tool(tool_id)
        return bool(tool and tool.coolant_through)

    def supports_coolant(self, tool_id: str, coolant: str) -> bool:
        tool = self.get_tool(tool_id)
        return tool is not None and tool.supports_coolant(coolant)

    def to_dict(self) -> dict[str, Any]:
        result = {
            "schema_version": self.schema_version,
            "name": self.name,
            "source": self.source,
            "tools": [tool.to_dict() for tool in self.tools],
        }
        if self.magazine is not None:
            result["magazine"] = self.magazine.to_dict()
        return result


def _load_magazine(magazine) -> Optional[ToolMagazine]:
    if magazine is None:
        return None
    if isinstance(magazine, ToolMagazine):
        return magazine
    if isinstance(magazine, dict):
        return ToolMagazine.from_dict(magazine)
    path = _tooling_path(magazine)
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    if "magazine" in data and isinstance(data["magazine"], dict):
        data = data["magazine"]
    return ToolMagazine.from_dict(data)


def load_tooling_context(
    tooling,
    magazine: Optional[str | Path | dict[str, Any] | ToolMagazine] = None,
) -> ToolingContext:
    """Return a ``ToolingContext`` from a path, dict, or context object."""
    if isinstance(tooling, ToolingContext):
        if magazine is None:
            return tooling
        data = tooling.to_dict()
        return ToolingContext.from_dict(data, source=tooling.source, magazine=magazine)
    if isinstance(tooling, dict):
        return ToolingContext.from_dict(tooling, magazine=magazine)
    return ToolingContext.from_json(tooling, magazine=magazine)
