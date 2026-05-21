"""Tests for Zero-to-CAD feature-family benchmark scans."""

import json

from src.data import run_zero_to_cad_feature_benchmarks as bench


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
    assert summary["unsupported"] == 1
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
    assert summary["match_rate"] == 0.5
    assert summary["families"]["hole"]["attempted"] == 1
    assert summary["families"]["hole"]["matched"] == 1
    assert summary["families"]["primitive"]["plannable"] == 2
    assert summary["families"]["primitive"]["attempted"] == 1
    assert summary["families"]["primitive"]["failed"] == 1


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
