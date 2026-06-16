"""Controller and post capability context for SubCAD process plans.

This module mirrors :mod:`subcad.machine_context` at the controller/post layer.
It keeps validation and posting code independent from a specific postprocessor
while still giving them a compact capability summary to query.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any, Optional


CONTROLLER_SCHEMA_VERSION = "subcad.controller_capabilities.v1"


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _controller_path(controller: str | Path) -> Path:
    raw = Path(controller)
    if raw.exists():
        return raw

    candidates = [
        _repo_root() / str(controller),
        _repo_root() / "controllers" / str(controller),
    ]
    if raw.suffix.lower() != ".json":
        candidates.append(_repo_root() / "controllers" / f"{controller}.json")

    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"controller definition not found: {controller}")


def _controller_id_from_path(path: Optional[Path], data: dict[str, Any]) -> str:
    if data.get("controller_id"):
        return str(data["controller_id"])
    if data.get("id"):
        return str(data["id"])
    if path is not None:
        return path.stem
    name = str(data.get("name") or data.get("model") or "controller").strip()
    return _normalize_name(name)


def _unique(values, *, normalize=lambda value: value) -> list:
    result = []
    seen = set()
    for value in values or []:
        normalized = normalize(value)
        if normalized in ("", None) or normalized in seen:
            continue
        seen.add(normalized)
        result.append(normalized)
    return result


def _as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, dict):
        return bool(value.get("supported", True))
    if isinstance(value, str):
        return value.strip().lower() in {"1", "yes", "true", "supported", "enabled"}
    return bool(value)


def _normalize_cycle(value: Any) -> str:
    return str(value).strip().upper()


def _normalize_name(value: Any) -> str:
    return str(value).strip().lower().replace("-", "_").replace(" ", "_")


def _normalize_code(value: Any) -> str:
    return str(value).strip().upper().replace(" ", "")


def _first_present(*values):
    for value in values:
        if value not in (None, ""):
            return value
    return None


def _coolant_codes_from(data: dict[str, Any], supports: dict[str, Any]) -> dict[str, str]:
    raw_codes = _first_present(
        data.get("coolant_codes"),
        supports.get("coolant_codes"),
        data.get("coolant"),
        supports.get("coolant"),
    )
    if isinstance(raw_codes, dict):
        return {
            _normalize_name(mode): _normalize_code(code)
            for mode, code in raw_codes.items()
            if _normalize_name(mode)
        }
    if isinstance(raw_codes, str):
        raw_codes = [raw_codes]
    return {
        _normalize_name(mode): ""
        for mode in (raw_codes or [])
        if _normalize_name(mode)
    }


@dataclass
class ControllerContext:
    """Lightweight controller/post capability summary stored in a SubCAD plan."""

    controller_id: str
    name: str = ""
    manufacturer: str = ""
    model: str = ""
    post_dialect: str = ""
    source: str = ""
    cycles: list[str] = field(default_factory=list)
    rotary_modes: list[str] = field(default_factory=list)
    coolant_codes: dict[str, str] = field(default_factory=dict)
    coordinate_systems: list[str] = field(default_factory=list)
    probing: bool = False
    rigid_tapping: bool = False
    macros: bool = False
    supports: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_json(cls, controller: str | Path) -> "ControllerContext":
        path = _controller_path(controller)
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        return cls.from_dict(data, source=str(path))

    @classmethod
    def from_dict(cls, data: dict[str, Any], source: str = "") -> "ControllerContext":
        supports = dict(data.get("supports") or data.get("capabilities") or {})
        cycles = _first_present(
            data.get("supported_cycles"),
            data.get("controller_cycles"),
            data.get("cycles"),
            supports.get("supported_cycles"),
            supports.get("controller_cycles"),
            supports.get("cycles"),
            [],
        )
        rotary_modes = _first_present(
            data.get("rotary_modes"),
            supports.get("rotary_modes"),
            [],
        )
        coolant_codes = _coolant_codes_from(data, supports)
        coordinate_systems = _first_present(
            data.get("coordinate_systems"),
            supports.get("coordinate_systems"),
            ["G54", "G55", "G56", "G57", "G58", "G59"],
        )
        post_dialect = _first_present(
            data.get("post_dialect"),
            data.get("dialect"),
            supports.get("post_dialect"),
            supports.get("dialect"),
            "",
        )
        path = Path(source) if source else None

        return cls(
            controller_id=_controller_id_from_path(path, data),
            name=str(data.get("name") or data.get("controller_id") or "Controller"),
            manufacturer=str(data.get("manufacturer") or ""),
            model=str(data.get("model") or ""),
            post_dialect=str(post_dialect),
            source=str(data.get("source") or source or ""),
            cycles=_unique(cycles, normalize=_normalize_cycle),
            rotary_modes=_unique(rotary_modes, normalize=_normalize_name),
            coolant_codes=coolant_codes,
            coordinate_systems=_unique(coordinate_systems, normalize=_normalize_code),
            probing=_as_bool(_first_present(data.get("probing"), supports.get("probing"), False)),
            rigid_tapping=_as_bool(_first_present(data.get("rigid_tapping"), supports.get("rigid_tapping"), False)),
            macros=_as_bool(_first_present(
                data.get("macro_support"),
                data.get("macros"),
                supports.get("macro_support"),
                supports.get("macros"),
                supports.get("macro_b"),
                False,
            )),
            supports=supports,
        )

    @property
    def supported_cycles(self) -> list[str]:
        return list(self.cycles)

    @property
    def coolant_modes(self) -> list[str]:
        return list(self.coolant_codes.keys())

    @property
    def macro_support(self) -> bool:
        return self.macros

    @property
    def capabilities(self) -> dict[str, Any]:
        capabilities = dict(self.supports)
        capabilities.update({
            "schema_version": capabilities.get("schema_version") or CONTROLLER_SCHEMA_VERSION,
            "supported_cycles": self.supported_cycles,
            "controller_cycles": self.supported_cycles,
            "rotary_modes": list(self.rotary_modes),
            "coolant_codes": dict(self.coolant_codes),
            "coolant": self.coolant_modes,
            "probing": self.probing,
            "rigid_tapping": self.rigid_tapping,
            "macro_support": self.macros,
            "coordinate_systems": list(self.coordinate_systems),
            "post_dialect": self.post_dialect,
        })
        return capabilities

    def supports_cycle(self, cycle: str) -> bool:
        if not cycle:
            return False
        return _normalize_cycle(cycle) in set(self.cycles)

    def supports_coolant(self, coolant: str) -> bool:
        if not coolant:
            return False
        mode = _normalize_name(coolant)
        code = _normalize_code(coolant)
        return mode in self.coolant_codes or code in set(self.coolant_codes.values())

    def coolant_code(self, coolant: str) -> str:
        if not coolant:
            return ""
        mode = _normalize_name(coolant)
        code = _normalize_code(coolant)
        if mode in self.coolant_codes:
            return self.coolant_codes[mode]
        if code in set(self.coolant_codes.values()):
            return code
        return ""

    def supports_rotary_mode(self, mode: str) -> bool:
        if not mode:
            return False
        return _normalize_name(mode) in set(self.rotary_modes)

    def supports_work_offset(self, offset: str) -> bool:
        return self.supports_coordinate_system(offset)

    def supports_coordinate_system(self, coordinate_system: str) -> bool:
        if not coordinate_system:
            return False
        return _normalize_code(coordinate_system) in set(self.coordinate_systems)

    def supports_probe(self) -> bool:
        return bool(self.probing)

    def supports_probing(self) -> bool:
        return bool(self.probing)

    def supports_rigid_tapping(self) -> bool:
        return bool(self.rigid_tapping)

    def supports_macro(self) -> bool:
        return bool(self.macros)

    def supports_macros(self) -> bool:
        return bool(self.macros)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": CONTROLLER_SCHEMA_VERSION,
            "controller_id": self.controller_id,
            "name": self.name,
            "manufacturer": self.manufacturer,
            "model": self.model,
            "post_dialect": self.post_dialect,
            "source": self.source,
            "cycles": list(self.cycles),
            "supported_cycles": self.supported_cycles,
            "controller_cycles": self.supported_cycles,
            "rotary_modes": list(self.rotary_modes),
            "coolant_codes": dict(self.coolant_codes),
            "coolant_modes": self.coolant_modes,
            "coordinate_systems": list(self.coordinate_systems),
            "probing": self.probing,
            "rigid_tapping": self.rigid_tapping,
            "macros": self.macros,
            "macro_support": self.macros,
            "supports": dict(self.supports),
            "capabilities": self.capabilities,
        }


def load_controller_context(controller) -> ControllerContext:
    """Return a ``ControllerContext`` from a path, id, dict, or context object."""
    if isinstance(controller, ControllerContext):
        return controller
    if isinstance(controller, dict):
        return ControllerContext.from_dict(controller)
    return ControllerContext.from_json(controller)
