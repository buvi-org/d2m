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
    assert summary["attempted"] == 0
    assert summary["executed"] == 0
    assert summary["matched"] == 0
    assert summary["failed"] == 0
    assert summary["unsupported"] == 1
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
