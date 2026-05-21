"""Manifest records for Zero-to-CAD dataset attempts and accepted pairs.

The utilities in this module are intentionally small and dependency-free so
pipeline workers can append durable per-row bookkeeping without importing the
live translator, geometry stack, or parquet reader.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


MANIFEST_SCHEMA = "zero_to_cad_dataset_attempt_manifest.v1"
STATUS_LIFECYCLE = (
    "planned",
    "attempted",
    "executed",
    "matched",
    "failed",
    "unsupported",
    "manual_review",
)


@dataclass
class SourceIdentity:
    split: str
    uuid: str
    global_index: int
    parquet_file: str = ""
    row_index: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return _json_safe(asdict(self))


@dataclass
class ArtifactPaths:
    original_step: str = ""
    generated_subcad: str = ""
    generated_step: str = ""
    process_plan: str = ""
    validation: str = ""
    comparison: str = ""
    economics: str = ""

    def to_dict(self) -> dict[str, Any]:
        return _json_safe(asdict(self))


@dataclass
class TolerancePolicy:
    comparison_methods: list[str] = field(default_factory=list)
    tolerance: float | None = None
    tolerance_mm: float | None = None
    min_mesh_score: float | None = None
    volume_only_success: bool | None = None
    feature_aware: bool | None = None
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return _json_safe(asdict(self))


@dataclass
class ManifestMetadata:
    git_commit: str = ""
    git_branch: str = ""
    model_provider: str = ""
    model: str = ""
    prompt_id: str = ""
    prompt_version: str = ""
    run_id: str = ""
    worker: str = ""
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return _json_safe(asdict(self))


@dataclass
class DatasetAttemptRecord:
    source: SourceIdentity
    artifacts: ArtifactPaths = field(default_factory=ArtifactPaths)
    status: str = "planned"
    accepted: bool = False
    planner: str = ""
    families: list[str] = field(default_factory=list)
    planner_tags: list[str] = field(default_factory=list)
    tolerance_policy: TolerancePolicy = field(default_factory=TolerancePolicy)
    metadata: ManifestMetadata = field(default_factory=ManifestMetadata)
    errors: list[str] = field(default_factory=list)
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        status = _normalize_status(self.status)
        data = asdict(self)
        data["schema"] = MANIFEST_SCHEMA
        data["status"] = status
        data["accepted"] = bool(self.accepted)
        data["families"] = sorted({str(family) for family in self.families if str(family)})
        data["planner_tags"] = sorted({str(tag) for tag in self.planner_tags if str(tag)})
        return _json_safe(data)


def make_attempt_record(
    *,
    split: str,
    uuid: str,
    global_index: int,
    parquet_file: str = "",
    row_index: int | None = None,
    artifacts: Mapping[str, Any] | ArtifactPaths | None = None,
    planner: str = "",
    families: Sequence[str] | None = None,
    planner_tags: Sequence[str] | None = None,
    status: str = "planned",
    accepted: bool = False,
    tolerance_policy: Mapping[str, Any] | TolerancePolicy | None = None,
    metadata: Mapping[str, Any] | ManifestMetadata | None = None,
    errors: Sequence[Any] | None = None,
    notes: str = "",
) -> dict[str, Any]:
    """Build a JSON-safe manifest dict for one attempted Zero-to-CAD row."""
    record = DatasetAttemptRecord(
        source=SourceIdentity(
            split=str(split),
            uuid=str(uuid),
            global_index=int(global_index),
            parquet_file=str(parquet_file),
            row_index=int(row_index) if row_index is not None else None,
        ),
        artifacts=_coerce_dataclass(artifacts, ArtifactPaths),
        status=status,
        accepted=accepted,
        planner=str(planner),
        families=[str(family) for family in families or []],
        planner_tags=[str(tag) for tag in planner_tags or []],
        tolerance_policy=_coerce_dataclass(tolerance_policy, TolerancePolicy),
        metadata=_coerce_dataclass(metadata, ManifestMetadata),
        errors=[str(error) for error in errors or []],
        notes=str(notes),
    )
    return record.to_dict()


def write_manifest_jsonl(
    path: str | Path,
    records: Iterable[Mapping[str, Any] | DatasetAttemptRecord],
    *,
    append: bool = True,
) -> int:
    """Write manifest records as newline-delimited JSON and return row count."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    mode = "a" if append else "w"
    count = 0
    with output_path.open(mode, encoding="utf-8") as fh:
        for record in records:
            payload = record.to_dict() if isinstance(record, DatasetAttemptRecord) else _json_safe(dict(record))
            fh.write(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n")
            count += 1
    return count


def summarize_manifest(records: Iterable[Mapping[str, Any] | DatasetAttemptRecord]) -> dict[str, Any]:
    """Summarize manifest counts by lifecycle status and planner family."""
    status_counts: Counter[str] = Counter()
    family_counts: dict[str, Counter[str]] = defaultdict(Counter)
    accepted = 0
    total = 0

    for record in records:
        payload = record.to_dict() if isinstance(record, DatasetAttemptRecord) else dict(record)
        status = _normalize_status(str(payload.get("status") or "planned"))
        families = [str(family) for family in payload.get("families") or []] or ["__unclassified__"]
        total += 1
        status_counts[status] += 1
        if bool(payload.get("accepted")):
            accepted += 1
        for family in families:
            family_counts[family]["total"] += 1
            family_counts[family][status] += 1
            if bool(payload.get("accepted")):
                family_counts[family]["accepted"] += 1

    return {
        "schema": f"{MANIFEST_SCHEMA}.summary",
        "total": total,
        "accepted": accepted,
        "by_status": dict(sorted(status_counts.items())),
        "by_family": {
            family: dict(sorted(counts.items()))
            for family, counts in sorted(family_counts.items())
        },
    }


def load_manifest_jsonl(path: str | Path) -> list[dict[str, Any]]:
    """Read manifest JSONL records from disk."""
    records: list[dict[str, Any]] = []
    with Path(path).open("r", encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                records.append(json.loads(line))
    return records


def _coerce_dataclass(value: Any, cls: type) -> Any:
    if isinstance(value, cls):
        return value
    if value is None:
        return cls()
    if not isinstance(value, Mapping):
        raise TypeError(f"{cls.__name__} value must be a mapping or {cls.__name__}")
    allowed = cls.__dataclass_fields__
    kwargs = {key: value[key] for key in value if key in allowed}
    return cls(**kwargs)


def _normalize_status(status: str) -> str:
    normalized = str(status or "planned").strip().lower()
    if normalized not in STATUS_LIFECYCLE:
        raise ValueError(f"Unsupported manifest status: {status!r}")
    return normalized


def _json_safe(value: Any) -> Any:
    if isinstance(value, Path):
        return value.as_posix()
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, Mapping):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_json_safe(item) for item in value]
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    if isinstance(value, set):
        return sorted(_json_safe(item) for item in value)
    try:
        json.dumps(value)
    except (TypeError, ValueError):
        return str(value)
    return value
