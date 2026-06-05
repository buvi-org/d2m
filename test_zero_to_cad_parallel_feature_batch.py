"""Tests for the parallel Zero-to-CAD feature benchmark launcher."""

from __future__ import annotations

import json

from src.data import run_zero_to_cad_parallel_feature_batch as batch
from src.data.zero_to_cad_dataset_manifest import make_attempt_record, write_manifest_jsonl


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


def test_select_candidate_rows_filters_families_and_accepted_index(tmp_path, monkeypatch):
    monkeypatch.setattr(
        batch.feature_bench,
        "iter_zero_to_cad_rows",
        lambda *args, **kwargs: _rows(
            ("accepted-hole", ["box", "hole"], ".box(1, 2, 3).hole(0.5)"),
            ("new-hole", ["box", "hole"], ".box(1, 2, 3).hole(0.5)"),
            ("axis-hole", ["box", "hole", "revolve"], ".box(1, 2, 3).revolve().hole(1)"),
            ("box-only", ["box"], ".box(1, 2, 3)"),
        ),
    )
    accepted_manifest = tmp_path / "accepted.jsonl"
    write_manifest_jsonl(
        accepted_manifest,
        [
            make_attempt_record(
                split="train",
                uuid="accepted-hole",
                global_index=0,
                families=["hole", "primitive"],
                status="matched",
                accepted=True,
            )
        ],
        append=False,
    )

    config = batch.BatchConfig(
        source_dir="fake",
        run_id="test",
        family_filter=["hole"],
        family_exclude=["axisymmetric"],
        accepted_index_jsonl=[str(accepted_manifest)],
        dry_run=True,
    )

    candidates = batch.select_candidate_rows(config)

    assert [candidate.uuid for candidate in candidates] == ["new-hole"]
    assert candidates[0].families == ["hole", "primitive"]
    assert candidates[0].selected_families == ["hole"]


def test_launch_parallel_feature_batch_writes_distinct_per_row_manifests(tmp_path, monkeypatch):
    monkeypatch.setattr(
        batch.feature_bench,
        "iter_zero_to_cad_rows",
        lambda *args, **kwargs: _rows(
            ("first-box", ["box"], ".box(1, 2, 3)"),
            ("second-box", ["box"], ".box(4, 5, 6)"),
        ),
    )
    seen_manifests = []

    def fake_worker(candidate, config):
        row_dir = batch._candidate_output_dir(config, candidate)
        manifest_path = row_dir / "attempts.jsonl"
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps({"uuid": candidate.uuid}) + "\n", encoding="utf-8")
        seen_manifests.append(manifest_path)
        return batch.RowWorkerResult(
            candidate=candidate.to_dict(),
            output_dir=str(row_dir),
            manifest_jsonl=str(manifest_path),
            worker_mode="fake",
            ok=True,
            elapsed_seconds=0.01,
            summary={"attempted": 1, "executed": 1, "matched": 1, "failed": 0},
        )

    config = batch.BatchConfig(
        source_dir="fake",
        output_dir=str(tmp_path),
        run_id="parallel",
        candidate_limit=2,
        concurrency=2,
        dry_run=False,
        worker_mode="api",
    )

    summary = batch.launch_parallel_feature_batch(config, worker=fake_worker)

    assert summary["workers_launched"] == 2
    assert summary["workers_ok"] == 2
    assert summary["aggregate"]["attempted"] == 2
    assert len({path.parent for path in seen_manifests}) == 2
    assert all(path.name == "attempts.jsonl" and path.exists() for path in seen_manifests)
    assert (tmp_path / "parallel" / "parallel_feature_batch_summary.json").exists()


def test_build_worker_command_delegates_to_feature_benchmark_cli(tmp_path):
    config = batch.BatchConfig(
        source_dir="fake_source",
        output_dir=str(tmp_path),
        run_id="delegation",
        family_exclude=["axisymmetric"],
        accepted_index_jsonl=["accepted.jsonl"],
        dry_run=False,
        provider="deepseek",
        model="deepseek-chat",
        base_url="http://127.0.0.1:1234/v1",
        row_timeout_s=12.0,
        safety_cap=3,
        translation_mode="ai_heavy",
        comparison_methods=["volume", "mesh", "slices"],
        attempt_unsupported=True,
    )
    candidate = batch.CandidateRow(
        ordinal=0,
        split="train",
        global_index=42,
        uuid="part/42",
        families=["hole", "primitive"],
        selected_families=["hole"],
        planner={"compatible": True},
    )
    row_dir = tmp_path / "row"
    manifest_path = row_dir / "attempts.jsonl"

    command = batch._build_worker_command(candidate, config, row_dir, manifest_path)

    assert command[:3] == [
        batch.sys.executable,
        "-m",
        "src.data.run_zero_to_cad_feature_benchmarks",
    ]
    assert "--execute" in command
    assert command[command.index("--start-offset") + 1] == "42"
    assert command[command.index("--scan-limit") + 1] == "1"
    assert command[command.index("--manifest-jsonl") + 1] == str(manifest_path)
    assert command[command.index("--row-timeout-s") + 1] == "12"
    assert command[command.index("--safety-cap") + 1] == "3"
    assert command[command.index("--base-url") + 1] == "http://127.0.0.1:1234/v1"
    assert command[command.index("--translation-mode") + 1] == "ai_heavy"
    assert command[command.index("--comparison-methods") + 1] == "volume,mesh,slices"
    assert "--attempt-unsupported" in command
    assert "--accepted-index" in command
