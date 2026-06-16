"""Setup intent context helpers for SubCAD process plans.

This module normalizes high-level setup intent into validation-friendly
metadata without coupling the authoring layer to Stock or ProcessPlan.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, is_dataclass
import json
from pathlib import Path
from typing import Any, Optional


SETUP_CONTEXT_SCHEMA_VERSION = "subcad.setup_context.v1"
SUPPORTED_FACE_SELECTORS = (">Z", "<Z", ">X", "<X", ">Y", "<Y")
SUPPORTED_FACES = set(SUPPORTED_FACE_SELECTORS)

_FACE_ALIASES = {
    "TOP": ">Z",
    "UP": ">Z",
    "UPPER": ">Z",
    "+Z": ">Z",
    "Z+": ">Z",
    ">Z": ">Z",
    "BOTTOM": "<Z",
    "DOWN": "<Z",
    "LOWER": "<Z",
    "-Z": "<Z",
    "Z-": "<Z",
    "<Z": "<Z",
    "RIGHT": ">X",
    "+X": ">X",
    "X+": ">X",
    ">X": ">X",
    "LEFT": "<X",
    "-X": "<X",
    "X-": "<X",
    "<X": "<X",
    "BACK": ">Y",
    "REAR": ">Y",
    "+Y": ">Y",
    "Y+": ">Y",
    ">Y": ">Y",
    "FRONT": "<Y",
    "-Y": "<Y",
    "Y-": "<Y",
    "<Y": "<Y",
}


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _setup_path(setup: str | Path) -> Path:
    raw = Path(setup)
    if raw.exists():
        return raw

    candidates = [
        _repo_root() / str(setup),
        _repo_root() / "setups" / str(setup),
    ]
    if raw.suffix.lower() != ".json":
        candidates.append(_repo_root() / "setups" / f"{setup}.json")

    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"setup definition not found: {setup}")


def _unique(values) -> list:
    result = []
    for value in values or []:
        if value not in result:
            result.append(value)
    return result


def normalize_face_selector(face: Any) -> str:
    """Return a canonical SubCAD face selector such as ``">Z"``."""
    if isinstance(face, dict):
        for key in ("face_selector", "face", "side", "primary_face", "operation_side"):
            if key in face:
                return normalize_face_selector(face[key])
    for attr in ("face_selector", "primary_face", "operation_side"):
        if hasattr(face, attr):
            return normalize_face_selector(getattr(face, attr))

    raw = str(face or "").strip()
    if not raw:
        raise ValueError("face selector is required")

    key = raw.upper().replace(" ", "_").strip("_")
    if key.endswith("_FACE"):
        key = key[:-5]
    elif key.endswith("FACE"):
        key = key[:-4].strip("_")
    key = key.replace("POSITIVE_", "+").replace("NEGATIVE_", "-")
    key = _FACE_ALIASES.get(key, key)

    if len(key) == 2 and key[0] in {">", "<"} and key[1] in {"X", "Y", "Z"}:
        return key
    if len(key) == 2 and key[0] in {"+", "-"} and key[1] in {"X", "Y", "Z"}:
        return (">" if key[0] == "+" else "<") + key[1]
    if len(key) == 2 and key[0] in {"X", "Y", "Z"} and key[1] in {"+", "-"}:
        return (">" if key[1] == "+" else "<") + key[0]

    raise ValueError(f"unsupported face selector: {raw!r}")


def _object_dict(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, dict):
        return dict(value)
    if hasattr(value, "to_dict"):
        return dict(value.to_dict())
    if is_dataclass(value):
        return asdict(value)

    result = {}
    for key in (
        "setup_id",
        "id",
        "name",
        "fixture_type",
        "description",
        "workholding",
        "fixture",
        "datum",
        "orientation",
        "part_orientation",
        "face_selector",
        "accessible_faces",
        "primary_face",
        "operation_side",
        "setup_count",
        "work_offset",
        "work_offset_values",
        "stock_allowance",
        "stock_allowance_mm",
        "notes",
        "source",
    ):
        if hasattr(value, key):
            result[key] = getattr(value, key)
    return result


def _coerce_fixture(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, str):
        return {"name": value}
    data = _object_dict(value)
    return data or {"description": str(value)}


def _coerce_orientation(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, str):
        return {"primary_face": normalize_face_selector(value)}

    data = _object_dict(value)
    for key in ("primary_face", "face_selector", "operation_side", "up_face"):
        if data.get(key):
            data[key] = normalize_face_selector(data[key])
    return data


def _coerce_stock_allowance(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, (int, float)):
        return {"uniform_mm": float(value)}
    if isinstance(value, str):
        return {"description": value}
    data = _object_dict(value)
    return data or {"description": str(value)}


def _coerce_offset_values(value: Any) -> tuple[float, float, float, float, float, float]:
    if value is None:
        return (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    if isinstance(value, dict):
        return tuple(float(value.get(axis, 0.0)) for axis in ("x", "y", "z", "a", "b", "c"))
    if isinstance(value, (list, tuple)):
        if len(value) > 6:
            raise ValueError("work_offset_values must contain at most six values")
        padded = list(value) + [0.0] * (6 - len(value))
        return tuple(float(item) for item in padded[:6])
    raise ValueError("work_offset_values must be a sequence or axis dictionary")


def _coerce_setup_count(value: Any) -> int:
    if isinstance(value, dict):
        return max(1, len(value))
    if isinstance(value, (list, tuple, set)):
        return max(1, len(value))
    if value is None or value == "":
        return 1
    return int(value)


def _split_faces(value: str) -> list[str]:
    for delimiter in (",", ";", "|"):
        value = value.replace(delimiter, " ")
    return [item for item in value.split() if item]


def _coerce_faces(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        raw_faces = _split_faces(value)
    else:
        raw_faces = list(value)

    faces: list[str] = []
    for face in raw_faces:
        selector = normalize_face_selector(face)
        if selector not in faces:
            faces.append(selector)
    return faces


def _fixture_name(fixture: Optional[dict[str, Any]]) -> str:
    if not fixture:
        return ""
    return str(fixture.get("name") or fixture.get("id") or fixture.get("fixture") or "")


def _fixture_type(fixture: Optional[dict[str, Any]]) -> str:
    if not fixture:
        return ""
    return str(fixture.get("fixture_type") or fixture.get("type") or "")


@dataclass
class SetupContext:
    """Serializable manufacturing setup intent."""

    setup_id: str = "setup"
    name: str = "Setup"
    workholding: dict[str, Any] = field(default_factory=dict)
    datum: dict[str, Any] = field(default_factory=dict)
    orientation: dict[str, Any] = field(default_factory=dict)
    primary_face: str = ">Z"
    accessible_faces: list[str] = field(default_factory=lambda: [">Z"])
    operation_side: str = ""
    work_offset: str = "G54"
    work_offset_values: tuple[float, float, float, float, float, float] = (
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
    )
    setup_count: int = 1
    allow_reorientation: bool = False
    stock_allowance_mm: dict[str, Any] = field(default_factory=dict)
    notes: str = ""
    source: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    schema_version: str = SETUP_CONTEXT_SCHEMA_VERSION

    def __post_init__(self) -> None:
        self.workholding = _coerce_fixture(self.workholding)
        self.datum = _object_dict(self.datum)
        self.orientation = _coerce_orientation(self.orientation)
        self.metadata = _object_dict(self.metadata)

        offset_name = self.datum.get("work_offset") or self.datum.get("register")
        self.work_offset = str(self.work_offset or offset_name or "G54").upper()

        offset_values = (
            self.datum.get("work_offset_values")
            or self.datum.get("offset_values")
            or self.datum.get("machine_coordinates")
            or self.work_offset_values
        )
        self.work_offset_values = _coerce_offset_values(offset_values)
        self.datum.setdefault("work_offset", self.work_offset)
        self.datum.setdefault("work_offset_values", list(self.work_offset_values))

        self.primary_face = normalize_face_selector(
            self.primary_face
            or self.orientation.get("primary_face")
            or self.orientation.get("face_selector")
            or self.operation_side
            or ">Z"
        )
        self.operation_side = normalize_face_selector(self.operation_side or self.primary_face)

        faces = _coerce_faces(self.accessible_faces)
        if not faces:
            orientation_faces = self.orientation.get("accessible_faces") or self.orientation.get("faces")
            faces = _coerce_faces(orientation_faces) if orientation_faces else [self.primary_face]
        faces = [self.operation_side] + [face for face in faces if face != self.operation_side]
        self.accessible_faces = _unique(faces)

        self.setup_count = _coerce_setup_count(self.setup_count)
        if self.setup_count < 1:
            raise ValueError("setup_count must be at least 1")

        self.stock_allowance_mm = _coerce_stock_allowance(self.stock_allowance_mm)
        if self.notes is None:
            self.notes = ""
        elif isinstance(self.notes, (list, tuple)):
            self.notes = "; ".join(str(item) for item in self.notes if item)
        else:
            self.notes = str(self.notes)

    @classmethod
    def from_json(cls, setup: str | Path) -> "SetupContext":
        path = _setup_path(setup)
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        return cls.from_dict(data, source=str(path))

    @classmethod
    def from_dict(cls, data: dict[str, Any], source: str = "") -> "SetupContext":
        if not isinstance(data, dict):
            raise TypeError("setup context data must be a dictionary")

        payload = dict(data.get("setup_context") or data.get("setup_intent") or data)
        datum = payload.get("datum") or {}
        fixture = payload.get("workholding", payload.get("fixture", {}))
        orientation = payload.get("orientation", payload.get("part_orientation", {}))
        operation_side = payload.get("operation_side", payload.get("side", ""))
        primary_face = payload.get(
            "primary_face",
            payload.get("face_selector", operation_side or ">Z"),
        )
        accessible = payload.get(
            "accessible_faces",
            payload.get("faces", payload.get("face_selectors", [])),
        )
        offset_values = payload.get("work_offset_values")
        if offset_values is None and isinstance(datum, dict):
            offset_values = datum.get("work_offset_values") or datum.get("offset_values")

        known = {
            "schema_version",
            "setup_context",
            "setup_intent",
            "setup_id",
            "id",
            "name",
            "workholding",
            "fixture",
            "datum",
            "orientation",
            "part_orientation",
            "primary_face",
            "face_selector",
            "accessible_faces",
            "faces",
            "face_selectors",
            "operation_side",
            "side",
            "work_offset",
            "work_offset_values",
            "setup_count",
            "setups",
            "setups_required",
            "allow_reorientation",
            "reorientation",
            "stock_allowance_mm",
            "stock_allowance",
            "allowance",
            "notes",
            "source",
            "metadata",
        }
        metadata = dict(payload.get("metadata") or {})
        metadata.update({key: value for key, value in payload.items() if key not in known})

        return cls(
            setup_id=str(payload.get("setup_id") or payload.get("id") or payload.get("name") or "setup"),
            name=str(payload.get("name") or payload.get("setup_id") or "Setup"),
            workholding=fixture,
            datum=datum,
            orientation=orientation,
            primary_face=primary_face,
            accessible_faces=accessible,
            operation_side=operation_side,
            work_offset=payload.get(
                "work_offset",
                datum.get("work_offset", "G54") if isinstance(datum, dict) else "G54",
            ),
            work_offset_values=offset_values,
            setup_count=payload.get(
                "setup_count",
                payload.get("setups_required", payload.get("setups", 1)),
            ),
            allow_reorientation=bool(payload.get("allow_reorientation", payload.get("reorientation", False))),
            stock_allowance_mm=payload.get(
                "stock_allowance_mm",
                payload.get("stock_allowance", payload.get("allowance", {})),
            ),
            notes=payload.get("notes", ""),
            source=str(payload.get("source") or source or ""),
            metadata=metadata,
            schema_version=str(payload.get("schema_version") or SETUP_CONTEXT_SCHEMA_VERSION),
        )

    @classmethod
    def from_object(cls, value: Any) -> "SetupContext":
        """Build a context from a dict-like object or attribute object."""
        if isinstance(value, SetupContext):
            return value
        if isinstance(value, dict):
            return cls.from_dict(value)
        return cls.from_dict(_object_dict(value))

    @property
    def fixture(self) -> dict[str, Any]:
        """Alias for fixture/workholding vocabulary."""
        return self.workholding

    @property
    def part_orientation(self) -> dict[str, Any]:
        """Alias for part-orientation vocabulary."""
        return self.orientation

    @property
    def stock_allowance(self) -> dict[str, Any]:
        """Alias for stock allowance metadata."""
        return self.stock_allowance_mm

    def can_access_face(self, face: Any) -> bool:
        """Return True when *face* is reachable in this setup intent."""
        return normalize_face_selector(face or self.primary_face) in set(self.accessible_faces)

    def requires_reorientation(self, face: Any) -> bool:
        """Return True when *face* needs another orientation or setup."""
        return not self.can_access_face(face)

    def unsupported_faces(self) -> list[str]:
        return [face for face in self.accessible_faces if face not in SUPPORTED_FACES]

    def setup_record(self, name: Optional[str] = None) -> dict[str, Any]:
        """Return a serialized setup record compatible with ProcessPlan."""
        setup_name = name or self.setup_id or "setup_1"
        record = {
            "name": setup_name,
            "fixture": _fixture_name(self.fixture),
            "fixture_type": _fixture_type(self.fixture),
            "face_selector": self.primary_face,
            "work_offset": self.work_offset,
            "work_offset_values": list(self.work_offset_values),
            "accessible_faces": list(self.accessible_faces),
            "operation_side": self.operation_side,
            "setup_count": self.setup_count,
            "part_orientation": dict(self.orientation),
            "datum": dict(self.datum),
        }
        if self.stock_allowance_mm:
            record["stock_allowance_mm"] = dict(self.stock_allowance_mm)
        if self.notes:
            record["notes"] = self.notes
        if self.metadata:
            record["metadata"] = dict(self.metadata)
        return record

    def to_plan_metadata(self, setup_name: Optional[str] = None) -> dict[str, Any]:
        """Return fixture, setup, and work-offset metadata for plan integration."""
        name = setup_name or self.setup_id or "setup_1"
        return {
            "fixture": dict(self.fixture) if self.fixture else None,
            "setups": {name: self.setup_record(name)},
            "work_offsets": {self.work_offset: list(self.work_offset_values)},
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "setup_id": self.setup_id,
            "name": self.name,
            "workholding": dict(self.workholding),
            "fixture": dict(self.fixture),
            "datum": dict(self.datum),
            "orientation": dict(self.orientation),
            "part_orientation": dict(self.orientation),
            "primary_face": self.primary_face,
            "operation_side": self.operation_side,
            "accessible_faces": list(self.accessible_faces),
            "work_offset": self.work_offset,
            "work_offset_values": list(self.work_offset_values),
            "setup_count": self.setup_count,
            "allow_reorientation": self.allow_reorientation,
            "stock_allowance_mm": dict(self.stock_allowance_mm),
            "stock_allowance": dict(self.stock_allowance_mm),
            "notes": self.notes,
            "source": self.source,
            "metadata": dict(self.metadata),
        }


def load_setup_context(value: Any = None, **overrides: Any) -> SetupContext:
    """Return a ``SetupContext`` from a path, id, dict, object, or context."""
    if value is None:
        data: dict[str, Any] = {}
    elif isinstance(value, SetupContext):
        if not overrides:
            return value
        data = value.to_dict()
    elif isinstance(value, dict):
        data = dict(value)
    elif isinstance(value, (str, Path)) and not overrides:
        return SetupContext.from_json(value)
    else:
        data = _object_dict(value)

    data.update(overrides)
    return SetupContext.from_dict(data)


def coerce_setup_context(value: Any = None, **overrides: Any) -> SetupContext:
    """Compatibility alias for :func:`load_setup_context`."""
    return load_setup_context(value, **overrides)
