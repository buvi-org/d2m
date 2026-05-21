"""Tests for Zero-to-CAD feature-family Markdown summaries."""

import json

from src.data import summarize_zero_to_cad_feature_benchmarks as report


def _write_summary(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_single_split_summary_renders_totals_top_families_and_statuses(tmp_path):
    summary_path = tmp_path / "feature_family_summary.json"
    _write_summary(
        summary_path,
        {
            "schema": "zero_to_cad_feature_family_benchmark.v1",
            "split": "train",
            "scanned": 20,
            "plannable": 17,
            "unsupported": 3,
            "attempted": 4,
            "executed": 3,
            "matched": 2,
            "failed": 1,
            "remaining_to_goal": 98,
            "match_rate": 0.6667,
            "families": {
                "primitive": {
                    "plannable": 12,
                    "attempted": 3,
                    "executed": 2,
                    "matched": 1,
                    "failed": 1,
                    "statuses": {"planned": 12},
                },
                "hole": {
                    "plannable": 5,
                    "attempted": 1,
                    "executed": 1,
                    "matched": 1,
                    "failed": 0,
                    "statuses": {"planned": 4, "manual_review": 1},
                },
                "__unsupported__": {
                    "unsupported": 3,
                    "statuses": {},
                },
            },
        },
    )

    markdown = report.write_markdown_report(summary_path, top_n=2)

    assert "# Zero-to-CAD Feature Benchmark Report" in markdown
    assert "**Scope:** Split: train" in markdown
    assert "| scanned | 20 |" in markdown
    assert "| remaining_to_goal | 98 |" in markdown
    assert "| match_rate | 66.67% |" in markdown
    assert "| primitive | 12 | 3 | 2 | 1 | 1 | 0 | 50.00% |" in markdown
    assert "| hole | 5 | 1 | 1 | 1 | 0 | 0 | 100.00% |" in markdown
    assert "| hole | planned: 4, manual_review: 1 |" in markdown
    assert "| __unsupported__ | unsupported: 3 |" in markdown
    assert "## Splits" not in markdown


def test_aggregate_summary_renders_per_split_table_and_prefers_all_file(tmp_path):
    _write_summary(
        tmp_path / "feature_family_summary.json",
        {
            "schema": "zero_to_cad_feature_family_benchmark.v1",
            "split": "train",
            "scanned": 1,
        },
    )
    _write_summary(
        tmp_path / "feature_family_summary_all.json",
        {
            "schema": "zero_to_cad_feature_family_benchmark.aggregate.v1",
            "split": "all",
            "scanned": 30,
            "plannable": 24,
            "unsupported": 6,
            "attempted": 9,
            "executed": 8,
            "matched": 6,
            "failed": 2,
            "remaining_to_goal": 94,
            "match_rate": 0.75,
            "per_split": {
                "train": {
                    "scanned": 20,
                    "plannable": 16,
                    "unsupported": 4,
                    "attempted": 6,
                    "executed": 5,
                    "matched": 4,
                    "failed": 1,
                    "match_rate": 0.8,
                },
                "val": {
                    "scanned": 10,
                    "plannable": 8,
                    "unsupported": 2,
                    "attempted": 3,
                    "executed": 3,
                    "matched": 2,
                    "failed": 1,
                    "match_rate": 0.6667,
                },
            },
            "families": {
                "primitive": {"plannable": 18, "executed": 5, "matched": 4},
                "profile": {"plannable": 6, "executed": 3, "matched": 2},
            },
        },
    )

    markdown = report.write_markdown_report(tmp_path)

    assert "**Scope:** Aggregate" in markdown
    assert "| matched | 6 |" in markdown
    assert "## Splits" in markdown
    assert "| train | 20 | 16 | 4 | 6 | 5 | 4 | 1 | 80.00% |" in markdown
    assert "| val | 10 | 8 | 2 | 3 | 3 | 2 | 1 | 66.67% |" in markdown
    assert "| primitive | 18 | 0 | 5 | 4 | 0 | 0 | 80.00% |" in markdown


def test_cli_writes_markdown_file(tmp_path):
    summary_path = tmp_path / "feature_family_summary.json"
    output_path = tmp_path / "report.md"
    _write_summary(
        summary_path,
        {
            "schema": "zero_to_cad_feature_family_benchmark.v1",
            "split": "test",
            "scanned": 3,
            "plannable": 2,
            "unsupported": 1,
            "families": {"primitive": {"plannable": 2, "statuses": {"planned": 2}}},
        },
    )

    exit_code = report.main([str(summary_path), "--output", str(output_path), "--top-n", "1"])

    assert exit_code == 0
    assert output_path.exists()
    assert "**Scope:** Split: test" in output_path.read_text(encoding="utf-8")
