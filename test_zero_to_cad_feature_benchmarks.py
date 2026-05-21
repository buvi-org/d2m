"""Tests for Zero-to-CAD feature-family benchmark scans."""

import json

import pytest

from src.data import run_zero_to_cad_feature_benchmarks as bench
from src.data.zero_to_cad_dataset_manifest import load_manifest_jsonl, make_attempt_record, write_manifest_jsonl


def _rows(*items):
    for index, (uuid, ops, code) in enumerate(items):
        yield {
            "global_index": index,
            "uuid": uuid,
            "cadquery_code": code,
            "ops_trace": [{"op_name": op} for op in ops],
            "step_bytes": b"ISO-10303-21;",
            "parquet_file": "fake.parquet",
            "row_index": index,
        }


def _primitive_rows(count):
    return _rows(
        *[
            (f"primitive-{index}", ["box"], f".box({index + 1}, 2, 3)")
            for index in range(count)
        ]
    )


def test_dry_run_buckets_rows_by_planner_family_and_writes_summary(tmp_path, monkeypatch):
    monkeypatch.setattr(
        bench,
        "iter_zero_to_cad_rows",
        lambda *args, **kwargs: _rows(
            ("primitive-1", ["box"], ".box(1, 2, 3)"),
            ("hole-1", ["box", "hole"], ".box(1, 2, 3).hole(0.5)"),
            ("unsupported-1", [], ""),
        ),
    )

    summary = bench.run_feature_family_benchmark(
        source_dir="fake",
        output_dir=str(tmp_path),
        dry_run=True,
    )

    assert summary["schema"] == "zero_to_cad_feature_family_benchmark.v1"
    assert summary["scanned"] == 3
    assert summary["plannable"] == 2
    assert summary["selected"] == 2
    assert summary["filtered_out"] == 0
    assert summary["attempted"] == 0
    assert summary["executed"] == 0
    assert summary["matched"] == 0
    assert summary["failed"] == 0
    assert summary["consecutive_failures"] == 0
    assert summary["unsupported"] == 1
    assert summary["stopped_reason"] is None
    assert summary["remaining_to_goal"] == 100000
    assert summary["families"]["primitive"]["plannable"] == 2
    assert summary["families"]["hole"]["plannable"] == 1
    assert summary["families"][bench.UNSUPPORTED_FAMILY]["unsupported"] == 1
    assert summary["families"]["hole"]["examples"][0]["uuid"] == "hole-1"

    artifact = tmp_path / "feature_family_summary.json"
    assert artifact.exists()
    saved = json.loads(artifact.read_text(encoding="utf-8"))
    assert saved["families"]["primitive"]["plannable"] == 2


def test_executor_metrics_and_per_family_limits_are_distinct(tmp_path, monkeypatch):
    monkeypatch.setattr(
        bench,
        "iter_zero_to_cad_rows",
        lambda *args, **kwargs: _rows(
            ("hole-pass", ["hole"], ".hole(2)"),
            ("primitive-fail", ["box"], ".box(1, 2, 3)"),
            ("primitive-skipped", ["box"], ".box(4, 5, 6)"),
        ),
    )
    calls = []

    def fake_executor(row, context):
        calls.append((row["uuid"], context["families"]))
        return {
            "executed": True,
            "matched": row["uuid"] == "hole-pass",
        }

    summary = bench.run_feature_family_benchmark(
        source_dir="fake",
        output_dir=str(tmp_path),
        dry_run=False,
        per_family_limit=1,
        executor=fake_executor,
        write_summary=False,
    )

    assert calls == [
        ("hole-pass", ["hole"]),
        ("primitive-fail", ["primitive"]),
    ]
    assert summary["scanned"] == 3
    assert summary["plannable"] == 3
    assert summary["selected"] == 3
    assert summary["attempted"] == 2
    assert summary["executed"] == 2
    assert summary["matched"] == 1
    assert summary["failed"] == 1
    assert summary["consecutive_failures"] == 1
    assert summary["match_rate"] == 0.5
    assert summary["stopped_reason"] is None
    assert summary["families"]["hole"]["attempted"] == 1
    assert summary["families"]["hole"]["matched"] == 1
    assert summary["families"]["primitive"]["plannable"] == 2
    assert summary["families"]["primitive"]["attempted"] == 1
    assert summary["families"]["primitive"]["failed"] == 1


def test_accepted_index_skips_translator_and_counts_match(tmp_path, monkeypatch):
    monkeypatch.setattr(
        bench,
        "iter_zero_to_cad_rows",
        lambda *args, **kwargs: _rows(
            ("already-accepted", ["box", "hole"], ".box(1, 2, 3).hole(0.5)"),
            ("new-row", ["hole"], ".hole(2)"),
        ),
    )
    accepted_manifest = tmp_path / "accepted.jsonl"
    write_manifest_jsonl(
        accepted_manifest,
        [
            make_attempt_record(
                split="train",
                uuid="already-accepted",
                global_index=0,
                families=["hole", "primitive"],
                planner_tags=["drill", "rectangular_stock"],
                status="matched",
                accepted=True,
            )
        ],
        append=False,
    )
    calls = []

    def fake_executor(row, context):
        calls.append(row["uuid"])
        return {"executed": True, "matched": True}

    summary = bench.run_feature_family_benchmark(
        source_dir="fake",
        split="train",
        output_dir=str(tmp_path),
        dry_run=False,
        family_filter=["hole"],
        accepted_index_jsonl=[str(accepted_manifest)],
        executor=fake_executor,
        write_summary=False,
    )

    assert calls == ["new-row"]
    assert summary["scanned"] == 2
    assert summary["attempted"] == 1
    assert summary["executed"] == 1
    assert summary["matched"] == 2
    assert summary["skipped_accepted"] == 1
    assert summary["families"]["hole"]["matched"] == 2
    assert summary["families"]["hole"]["examples"][0]["skipped_accepted"] is True


def test_executor_stops_at_max_attempts(tmp_path, monkeypatch):
    monkeypatch.setattr(
        bench,
        "iter_zero_to_cad_rows",
        lambda *args, **kwargs: _primitive_rows(5),
    )
    calls = []

    def fake_executor(row, context):
        calls.append(row["uuid"])
        return {"executed": True, "matched": True}

    summary = bench.run_feature_family_benchmark(
        source_dir="fake",
        output_dir=str(tmp_path),
        dry_run=False,
        max_attempts=2,
        executor=fake_executor,
        write_summary=False,
    )

    assert calls == ["primitive-0", "primitive-1"]
    assert summary["stopped_reason"] == "max_attempts"
    assert summary["scanned"] == 2
    assert summary["attempted"] == 2
    assert summary["executed"] == 2
    assert summary["matched"] == 2
    assert summary["failed"] == 0
    assert summary["families"]["primitive"]["attempted"] == 2


def test_executor_stops_at_max_failures_without_resetting_total(tmp_path, monkeypatch):
    monkeypatch.setattr(
        bench,
        "iter_zero_to_cad_rows",
        lambda *args, **kwargs: _primitive_rows(5),
    )
    outcomes = [False, True, False, True]

    def fake_executor(row, context):
        return {"executed": True, "matched": outcomes.pop(0)}

    summary = bench.run_feature_family_benchmark(
        source_dir="fake",
        output_dir=str(tmp_path),
        dry_run=False,
        max_failures=2,
        executor=fake_executor,
        write_summary=False,
    )

    assert summary["stopped_reason"] == "max_failures"
    assert summary["attempted"] == 3
    assert summary["executed"] == 3
    assert summary["matched"] == 1
    assert summary["failed"] == 2
    assert summary["consecutive_failures"] == 1
    assert summary["families"]["primitive"]["failed"] == 2


def test_executor_stops_at_max_consecutive_failures(tmp_path, monkeypatch):
    monkeypatch.setattr(
        bench,
        "iter_zero_to_cad_rows",
        lambda *args, **kwargs: _primitive_rows(5),
    )

    def fake_executor(row, context):
        return {"executed": True, "matched": False}

    summary = bench.run_feature_family_benchmark(
        source_dir="fake",
        output_dir=str(tmp_path),
        dry_run=False,
        max_consecutive_failures=2,
        executor=fake_executor,
        write_summary=False,
    )

    assert summary["stopped_reason"] == "max_consecutive_failures"
    assert summary["attempted"] == 2
    assert summary["failed"] == 2
    assert summary["consecutive_failures"] == 2


def test_executor_stops_at_target_matches(tmp_path, monkeypatch):
    monkeypatch.setattr(
        bench,
        "iter_zero_to_cad_rows",
        lambda *args, **kwargs: _primitive_rows(5),
    )
    calls = []

    def fake_executor(row, context):
        calls.append(row["uuid"])
        return {"executed": True, "matched": True}

    summary = bench.run_feature_family_benchmark(
        source_dir="fake",
        output_dir=str(tmp_path),
        dry_run=False,
        target_matches=2,
        executor=fake_executor,
        write_summary=False,
    )

    assert calls == ["primitive-0", "primitive-1"]
    assert summary["stopped_reason"] == "target_matches"
    assert summary["attempted"] == 2
    assert summary["matched"] == 2
    assert summary["remaining_to_goal"] == 99998


def test_executor_writes_manifest_jsonl_when_requested(tmp_path, monkeypatch):
    monkeypatch.setattr(
        bench,
        "iter_zero_to_cad_rows",
        lambda *args, **kwargs: _primitive_rows(2),
    )
    manifest_path = tmp_path / "attempts.jsonl"

    def fake_executor(row, context):
        return {
            "executed": True,
            "matched": row["uuid"] == "primitive-0",
            "sample_dir": str(tmp_path / row["uuid"]),
            "comparison_methods": ["slice"],
            "trusted_tolerance_mm": 0.1,
            "min_mesh_score": 95.0,
            "trusted_match": row["uuid"] == "primitive-0",
        }

    summary = bench.run_feature_family_benchmark(
        source_dir="fake",
        split="train",
        output_dir=str(tmp_path),
        dry_run=False,
        executor=fake_executor,
        manifest_jsonl=str(manifest_path),
        write_summary=False,
    )

    records = load_manifest_jsonl(manifest_path)
    assert summary["attempted"] == 2
    assert len(records) == 2
    assert records[0]["status"] == "matched"
    assert records[0]["accepted"] is True
    assert records[0]["source"]["split"] == "train"
    assert records[0]["families"] == ["primitive"]
    assert records[0]["tolerance_policy"]["comparison_methods"] == ["slice"]
    assert records[1]["status"] == "executed"
    assert records[1]["accepted"] is False


def test_executor_stops_at_min_match_rate_after_attempts(tmp_path, monkeypatch):
    monkeypatch.setattr(
        bench,
        "iter_zero_to_cad_rows",
        lambda *args, **kwargs: _primitive_rows(5),
    )
    outcomes = [False, True, False, True]

    def fake_executor(row, context):
        return {"executed": True, "matched": outcomes.pop(0)}

    summary = bench.run_feature_family_benchmark(
        source_dir="fake",
        output_dir=str(tmp_path),
        dry_run=False,
        min_match_rate_after_attempts=[(3, 0.5)],
        executor=fake_executor,
        write_summary=False,
    )

    assert summary["stopped_reason"] == "min_match_rate_after_attempts:3:0.5"
    assert summary["min_match_rate_after_attempts"] == [
        {"attempts": 3, "min_match_rate": 0.5}
    ]
    assert summary["attempted"] == 3
    assert summary["matched"] == 1
    assert summary["failed"] == 2
    assert summary["match_rate"] == 0.3333


def test_family_filter_selects_matching_rows_only(tmp_path, monkeypatch):
    monkeypatch.setattr(
        bench,
        "iter_zero_to_cad_rows",
        lambda *args, **kwargs: _rows(
            ("hole-1", ["box", "hole"], ".box(1, 2, 3).hole(0.5)"),
            ("primitive-1", ["box"], ".box(1, 2, 3)"),
            ("slot-1", ["slot2D"], ".slot2D(10, 2)"),
        ),
    )

    summary = bench.run_feature_family_benchmark(
        source_dir="fake",
        output_dir=str(tmp_path),
        dry_run=True,
        family_filter=["hole"],
    )

    assert summary["scanned"] == 3
    assert summary["plannable"] == 3
    assert summary["selected"] == 1
    assert summary["filtered_out"] == 2
    assert summary["family_filter"] == ["hole"]
    assert sorted(summary["families"]) == ["hole"]
    assert summary["families"]["hole"]["examples"][0]["uuid"] == "hole-1"


def test_family_exclude_skips_risky_mixed_family_rows(tmp_path, monkeypatch):
    monkeypatch.setattr(
        bench,
        "iter_zero_to_cad_rows",
        lambda *args, **kwargs: _rows(
            ("hole-axisymmetric", ["box", "hole", "revolve"], ".box(1, 2, 3).revolve().hole(1)"),
            ("hole-simple", ["box", "hole"], ".box(1, 2, 3).hole(1)"),
        ),
    )

    summary = bench.run_feature_family_benchmark(
        source_dir="fake",
        output_dir=str(tmp_path),
        dry_run=True,
        family_filter=["hole"],
        family_exclude=["axisymmetric"],
        write_summary=False,
    )

    assert summary["scanned"] == 2
    assert summary["plannable"] == 2
    assert summary["selected"] == 1
    assert summary["filtered_out"] == 1
    assert summary["family_exclude"] == ["axisymmetric"]
    assert summary["families"]["hole"]["examples"][0]["uuid"] == "hole-simple"


def test_all_split_aggregate_merges_family_metrics(tmp_path, monkeypatch):
    def fake_rows(source_dir, split, **kwargs):
        if split == "train":
            return _rows(("train-hole", ["hole"], ".hole(2)"))
        if split == "val":
            return _rows(("val-box", ["box"], ".box(1, 2, 3)"))
        return _rows(("test-slot", ["slot2D"], ".slot2D(10, 2)"))

    monkeypatch.setattr(bench, "iter_zero_to_cad_rows", fake_rows)

    summary = bench.run_feature_family_benchmark_splits(
        source_dir="fake",
        output_dir=str(tmp_path),
        dry_run=True,
        write_summary=True,
    )

    assert summary["schema"] == "zero_to_cad_feature_family_benchmark.aggregate.v1"
    assert summary["split"] == "all"
    assert summary["splits"] == ["train", "val", "test"]
    assert summary["scanned"] == 3
    assert summary["plannable"] == 3
    assert summary["selected"] == 3
    assert summary["remaining_to_goal"] == 100000
    assert "train" in summary["per_split"]
    assert "hole" in summary["families"]
    assert "primitive" in summary["families"]
    assert "profile" in summary["families"]
    assert (tmp_path / "feature_family_summary_all.json").exists()


def test_parse_methods_supports_disabled_and_comma_lists():
    assert bench._parse_methods("slice,sdf") == ["slice", "sdf"]
    assert bench._parse_methods("none") == []
    assert bench._parse_methods("") == []


def test_parse_match_rate_guardrails_supports_attempt_rate_pairs():
    assert bench._parse_match_rate_guardrails(["10:0.6", "3:0.5"]) == [
        (3, 0.5),
        (10, 0.6),
    ]


def test_execute_still_requires_translator_executor():
    with pytest.raises(SystemExit):
        bench.main(["--execute", "--no-summary-file"])
