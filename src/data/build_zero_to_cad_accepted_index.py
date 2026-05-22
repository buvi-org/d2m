"""Build a deduplicated accepted-pair index from Zero-to-CAD run manifests."""

from __future__ import annotations

import argparse
import json
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return rows
    for line_no, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            rows.append({
                "accepted": False,
                "status": "invalid_manifest_line",
                "manifest": str(path),
                "line": line_no,
            })
            continue
        row["_manifest"] = str(path)
        row["_manifest_line"] = line_no
        rows.append(row)
    return rows


def _accepted_key(row: dict[str, Any]) -> tuple[str, str] | None:
    source = row.get("source") or {}
    split = source.get("split")
    uuid = source.get("uuid")
    pair_id = row.get("accepted_pair_id")
    if split and uuid:
        return str(split), str(uuid)
    if split and pair_id:
        return str(split), str(pair_id)
    return None


def _is_accepted(row: dict[str, Any]) -> bool:
    return (
        row.get("accepted") is True
        and row.get("status") == "matched"
        and _comparison_volume_is_trusted(row)
    )


def _comparison_volume_is_trusted(row: dict[str, Any]) -> bool:
    """Re-check trusted manifests against the current strict volume policy."""
    artifacts = row.get("artifacts") or {}
    comparison_path = artifacts.get("comparison")
    if not comparison_path:
        return True
    try:
        result = json.loads(Path(str(comparison_path)).read_text(encoding="utf-8"))
    except OSError:
        return True
    except json.JSONDecodeError:
        return False

    policy = result.get("match_policy") or {}
    comparison = result.get("comparison") or {}
    ratio = comparison.get("volume_ratio")
    if ratio is None:
        ratio = policy.get("volume_ratio")
    try:
        volume_ratio = float(ratio)
    except (TypeError, ValueError):
        return False
    tolerance = policy.get("volume_tolerance", 0.05)
    try:
        volume_tolerance = float(tolerance)
    except (TypeError, ValueError):
        volume_tolerance = 0.05
    return volume_ratio > 0.0 and abs(1.0 - volume_ratio) <= volume_tolerance


def _record_completeness(row: dict[str, Any]) -> int:
    artifacts = row.get("artifacts") or {}
    required = ("comparison", "generated_step", "generated_subcad", "original_step", "process_plan")
    return sum(1 for name in required if artifacts.get(name))


def _sort_record(row: dict[str, Any]) -> tuple[str, int, str]:
    source = row.get("source") or {}
    split = str(source.get("split") or "")
    index = source.get("global_index", source.get("row_index", -1))
    try:
        numeric_index = int(index)
    except (TypeError, ValueError):
        numeric_index = -1
    uuid = str(source.get("uuid") or row.get("accepted_pair_id") or "")
    return split, numeric_index, uuid


def _git_value(args: list[str]) -> str:
    try:
        return subprocess.check_output(["git", *args], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return ""


def build_index(runs_dir: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    accepted_records: list[dict[str, Any]] = []
    total_records = 0
    invalid_records = 0

    for manifest in sorted(runs_dir.rglob("attempts.jsonl")):
        for row in _read_jsonl(manifest):
            total_records += 1
            if row.get("status") == "invalid_manifest_line":
                invalid_records += 1
                continue
            if _is_accepted(row):
                accepted_records.append(row)

    deduped: dict[tuple[str, str], dict[str, Any]] = {}
    duplicate_keys: Counter[tuple[str, str]] = Counter()
    for row in accepted_records:
        key = _accepted_key(row)
        if key is None:
            continue
        duplicate_keys[key] += 1
        current = deduped.get(key)
        if current is None or _record_completeness(row) >= _record_completeness(current):
            deduped[key] = row

    index = sorted(deduped.values(), key=_sort_record)
    by_split = Counter(str((row.get("source") or {}).get("split") or "") for row in index)
    latest_by_split: dict[str, int] = {}
    for row in index:
        source = row.get("source") or {}
        split = str(source.get("split") or "")
        try:
            global_index = int(source.get("global_index", source.get("row_index", -1)))
        except (TypeError, ValueError):
            continue
        latest_by_split[split] = max(latest_by_split.get(split, -1), global_index)

    duplicate_count = sum(count - 1 for count in duplicate_keys.values() if count > 1)
    summary = {
        "schema": "zero_to_cad_accepted_summary.v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "runs_dir": str(runs_dir),
        "accepted_unique": len(index),
        "accepted_records": len(accepted_records),
        "duplicate_accepted_records": duplicate_count,
        "total_manifest_records": total_records,
        "invalid_manifest_records": invalid_records,
        "by_split": dict(sorted(by_split.items())),
        "latest_by_split": dict(sorted(latest_by_split.items())),
        "comparison_policy": {
            "accepted": "accepted == true and status == matched and strict volume policy passes",
            "dedupe_key": "source.split + source.uuid",
            "max_volume_error": 0.05,
            "volume_only_success": False,
            "target": "original Zero-to-CAD model.step",
        },
        "git": {
            "commit": _git_value(["rev-parse", "HEAD"]),
            "branch": _git_value(["branch", "--show-current"]),
            "dirty": bool(_git_value(["status", "--porcelain"])),
        },
    }
    return index, summary


def write_outputs(index: list[dict[str, Any]], summary: dict[str, Any], index_path: Path, summary_path: Path) -> None:
    index_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    with index_path.open("w", encoding="utf-8", newline="\n") as f:
        for row in index:
            row = {k: v for k, v in row.items() if not k.startswith("_")}
            f.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs-dir", default="runs/zero_to_cad_live_pilots")
    parser.add_argument("--index-out", default="runs/zero_to_cad_live_pilots/accepted_index.jsonl")
    parser.add_argument("--summary-out", default="runs/zero_to_cad_live_pilots/accepted_summary.json")
    args = parser.parse_args()

    index, summary = build_index(Path(args.runs_dir))
    write_outputs(index, summary, Path(args.index_out), Path(args.summary_out))
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
