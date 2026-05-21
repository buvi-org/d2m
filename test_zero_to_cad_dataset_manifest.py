"""Tests for Zero-to-CAD dataset attempt manifest utilities."""

import json
from datetime import datetime
from pathlib import Path

import pytest

from src.data.zero_to_cad_dataset_manifest import (
    MANIFEST_SCHEMA,
    DatasetAttemptRecord,
    SourceIdentity,
    accepted_pair_id,
    build_accepted_index,
    load_manifest_jsonl,
    make_attempt_record,
    source_key,
    summarize_manifest,
    write_manifest_jsonl,
)


def test_make_attempt_record_normalizes_json_safe_fields():
    record = make_attempt_record(
        split="train",
        uuid="part-001",
        global_index=7,
        parquet_file=Path("shard-000.parquet"),
        row_index=3,
        artifacts={
            "original_step": Path("source.step"),
            "generated_subcad": Path("generated.py"),
            "generated_step": Path("generated.step"),
            "process_plan": Path("plan.json"),
            "validation": Path("validation.json"),
            "comparison": Path("comparison.json"),
            "economics": Path("economics.json"),
        },
        planner="pure_subcad",
        families=["hole", "primitive", "hole"],
        planner_tags=["drill", "drill", "mill"],
        status="MATCHED",
        accepted=True,
        tolerance_policy={
            "comparison_methods": ["mesh", "features"],
            "tolerance_mm": 0.25,
            "min_mesh_score": 95.0,
            "feature_aware": True,
            "extra": {"captured_at": datetime(2026, 5, 21, 12, 30)},
        },
        metadata={
            "git_commit": "abc123",
            "model_provider": "deepseek",
            "model": "translator-v1",
            "prompt_id": "zero-to-cad-attempt",
            "extra": {"seed_path": Path("prompts/seed.txt")},
        },
    )

    assert record["schema"] == MANIFEST_SCHEMA
    assert record["accepted_pair_id"] == "zero_to_cad:train:part-001"
    assert record["source"] == {
        "split": "train",
        "uuid": "part-001",
        "global_index": 7,
        "parquet_file": "shard-000.parquet",
        "row_index": 3,
    }
    assert record["artifacts"]["original_step"] == "source.step"
    assert record["artifacts"]["economics"] == "economics.json"
    assert record["families"] == ["hole", "primitive"]
    assert record["planner_tags"] == ["drill", "mill"]
    assert record["status"] == "matched"
    assert record["accepted"] is True
    assert record["tolerance_policy"]["extra"]["captured_at"] == "2026-05-21T12:30:00"
    assert record["metadata"]["extra"]["seed_path"] == "prompts/seed.txt"
    json.dumps(record)


def test_build_accepted_index_keeps_only_matched_accepted_rows():
    matched = make_attempt_record(
        split="train",
        uuid="accepted-row",
        global_index=1,
        families=["hole"],
        status="matched",
        accepted=True,
    )
    failed = make_attempt_record(
        split="train",
        uuid="failed-row",
        global_index=2,
        families=["hole"],
        status="failed",
        accepted=False,
    )
    executed_not_accepted = make_attempt_record(
        split="train",
        uuid="executed-row",
        global_index=3,
        families=["hole"],
        status="executed",
        accepted=True,
    )

    index = build_accepted_index([failed, executed_not_accepted, matched])

    assert accepted_pair_id("train", "accepted-row") == "zero_to_cad:train:accepted-row"
    assert source_key(matched) == ("train", "accepted-row")
    assert sorted(index) == [("train", "accepted-row")]
    assert index[("train", "accepted-row")]["accepted"] is True


def test_write_manifest_jsonl_appends_and_loads_records(tmp_path):
    manifest_path = tmp_path / "attempts.jsonl"
    planned = make_attempt_record(
        split="val",
        uuid="part-002",
        global_index=8,
        families=["profile"],
        status="planned",
    )
    failed = DatasetAttemptRecord(
        source=SourceIdentity(split="val", uuid="part-003", global_index=9),
        families=["hole"],
        status="failed",
        errors=["comparison below threshold"],
    )

    assert write_manifest_jsonl(manifest_path, [planned], append=False) == 1
    assert write_manifest_jsonl(manifest_path, [failed], append=True) == 1

    lines = manifest_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    loaded = load_manifest_jsonl(manifest_path)
    assert loaded[0]["source"]["uuid"] == "part-002"
    assert loaded[1]["source"]["uuid"] == "part-003"
    assert loaded[1]["errors"] == ["comparison below threshold"]


def test_summarize_manifest_counts_status_and_family_acceptance():
    records = [
        make_attempt_record(
            split="train",
            uuid="matched-hole",
            global_index=1,
            families=["hole", "primitive"],
            status="matched",
            accepted=True,
        ),
        make_attempt_record(
            split="train",
            uuid="failed-hole",
            global_index=2,
            families=["hole"],
            status="failed",
        ),
        make_attempt_record(
            split="train",
            uuid="unsupported",
            global_index=3,
            status="unsupported",
        ),
    ]

    summary = summarize_manifest(records)

    assert summary["schema"] == f"{MANIFEST_SCHEMA}.summary"
    assert summary["total"] == 3
    assert summary["accepted"] == 1
    assert summary["by_status"] == {"failed": 1, "matched": 1, "unsupported": 1}
    assert summary["by_family"]["hole"] == {
        "accepted": 1,
        "failed": 1,
        "matched": 1,
        "total": 2,
    }
    assert summary["by_family"]["primitive"] == {
        "accepted": 1,
        "matched": 1,
        "total": 1,
    }
    assert summary["by_family"]["__unclassified__"] == {
        "total": 1,
        "unsupported": 1,
    }


def test_unknown_status_is_rejected():
    with pytest.raises(ValueError, match="Unsupported manifest status"):
        make_attempt_record(
            split="test",
            uuid="bad-status",
            global_index=4,
            status="queued",
        )
