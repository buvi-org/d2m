"""Parallel launcher for guarded Zero-to-CAD feature benchmark batches.

The launcher scans candidate rows in-process with the existing Zero-to-CAD row
iterator and pure SubCAD planner, then delegates each selected row to the
existing feature benchmark runner.  Every executed row gets an isolated output
directory with its own ``attempts.jsonl`` manifest so parallel runs do not share
append targets.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Literal


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from . import run_zero_to_cad_feature_benchmarks as feature_bench
from .pure_subcad_planner import plan_pure_subcad_features
from .zero_to_cad_dataset_manifest import build_accepted_index, load_manifest_jsonl


DEFAULT_SOURCE_DIR = feature_bench.DEFAULT_SOURCE_DIR
DEFAULT_OUTPUT_DIR = "runs/zero_to_cad_parallel_feature_batches"
ALL_SPLITS = feature_bench.ALL_SPLITS
UNSUPPORTED_FAMILY = feature_bench.UNSUPPORTED_FAMILY
WorkerMode = Literal["cli", "api"]


@dataclass(frozen=True)
class CandidateRow:
    ordinal: int
    split: str
    global_index: int
    uuid: str
    families: list[str]
    selected_families: list[str]
    planner: dict[str, Any]
    parquet_file: str = ""
    row_index: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class BatchConfig:
    source_dir: str = DEFAULT_SOURCE_DIR
    split: str = "train"
    output_dir: str = DEFAULT_OUTPUT_DIR
    run_id: str = ""
    scan_limit: int | None = None
    start_offset: int = 0
    candidate_limit: int | None = None
    concurrency: int = 1
    family_filter: list[str] = field(default_factory=list)
    family_exclude: list[str] = field(default_factory=list)
    accepted_index_jsonl: list[str] = field(default_factory=list)
    attempt_unsupported: bool = False
    dry_run: bool = True
    worker_mode: WorkerMode = "cli"
    provider: str = "deepseek"
    model: str | None = None
    base_url: str | None = None
    api_timeout_s: float = 120.0
    row_timeout_s: float | None = None
    worker_timeout_s: float | None = None
    tolerance: float = 0.05
    safety_cap: int = 5
    stagnation_limit: int = 2
    divergence_limit: int = 2
    comparison_methods: list[str] = field(default_factory=lambda: ["slice"])
    feature_aware: bool = False
    trusted_tolerance_mm: float = 0.25
    min_mesh_score: float = 95.0
    volume_only_success: bool = False
    deterministic_only: bool = False
    translation_mode: str = "planner_guided"
    write_summary: bool = True

    def __post_init__(self) -> None:
        if not self.run_id:
            object.__setattr__(self, "run_id", _timestamp_run_id())

    @property
    def resolved_run_id(self) -> str:
        return self.run_id

    def root_dir(self) -> Path:
        return Path(self.output_dir) / self.resolved_run_id


@dataclass
class RowWorkerResult:
    candidate: dict[str, Any]
    output_dir: str
    manifest_jsonl: str
    worker_mode: str
    ok: bool
    elapsed_seconds: float
    returncode: int | None = None
    summary: dict[str, Any] | None = None
    error: str = ""
    stdout_path: str = ""
    stderr_path: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate": self.candidate,
            "output_dir": self.output_dir,
            "manifest_jsonl": self.manifest_jsonl,
            "worker_mode": self.worker_mode,
            "ok": self.ok,
            "elapsed_seconds": self.elapsed_seconds,
            "returncode": self.returncode,
            "summary": self.summary,
            "error": self.error,
            "stdout_path": self.stdout_path,
            "stderr_path": self.stderr_path,
        }


RowWorker = Callable[[CandidateRow, BatchConfig], RowWorkerResult]


def select_candidate_rows(config: BatchConfig) -> list[CandidateRow]:
    """Return rows eligible for per-row feature benchmark execution."""
    accepted_index = _load_accepted_index(config.accepted_index_jsonl)
    requested_families = _normalize_families(config.family_filter)
    excluded_families = _normalize_families(config.family_exclude)
    selected: list[CandidateRow] = []

    for split in _iter_splits(config.split):
        for row in feature_bench.iter_zero_to_cad_rows(
            config.source_dir,
            split,
            start_offset=config.start_offset,
            limit=config.scan_limit,
        ):
            if accepted_index.get((split, str(row.get("uuid", "")))) is not None:
                continue

            plan = plan_pure_subcad_features(
                row.get("ops_trace") or [],
                row.get("cadquery_code") or "",
            )
            if not plan.compatible and not config.attempt_unsupported:
                continue

            families = sorted({feature.family for feature in plan.features})
            if not plan.compatible and config.attempt_unsupported:
                families = families or [UNSUPPORTED_FAMILY]
            if excluded_families and any(family in excluded_families for family in families):
                continue

            selected_families = families
            if requested_families:
                selected_families = [
                    family for family in families
                    if family in requested_families
                ]
            if not selected_families:
                continue

            selected.append(
                CandidateRow(
                    ordinal=len(selected),
                    split=split,
                    global_index=int(row.get("global_index", 0)),
                    uuid=str(row.get("uuid", "")),
                    families=families,
                    selected_families=selected_families,
                    planner=plan.to_dict(),
                    parquet_file=str(row.get("parquet_file", "")),
                    row_index=(
                        int(row["row_index"])
                        if row.get("row_index") is not None
                        else None
                    ),
                )
            )
            if config.candidate_limit is not None and len(selected) >= config.candidate_limit:
                return selected

    return selected


def launch_parallel_feature_batch(
    config: BatchConfig,
    *,
    worker: RowWorker | None = None,
) -> dict[str, Any]:
    """Select candidates, launch row workers, and write a batch summary."""
    if config.concurrency < 1:
        raise ValueError("concurrency must be at least 1")

    root = config.root_dir()
    started = time.perf_counter()
    candidates = select_candidate_rows(config)
    row_results: list[RowWorkerResult] = []
    stopped_reason = None

    if config.dry_run:
        stopped_reason = "dry_run"
    elif candidates:
        row_worker = worker or (_run_candidate_cli if config.worker_mode == "cli" else _run_candidate_api)
        with ThreadPoolExecutor(max_workers=config.concurrency) as pool:
            futures = {
                pool.submit(row_worker, candidate, config): candidate
                for candidate in candidates
            }
            for future in as_completed(futures):
                candidate = futures[future]
                try:
                    row_results.append(future.result())
                except Exception as exc:
                    row_results.append(_exception_result(candidate, config, exc))

    row_results.sort(key=lambda result: int(result.candidate.get("ordinal", 0)))
    summary = _batch_summary(
        config=config,
        root=root,
        candidates=candidates,
        row_results=row_results,
        stopped_reason=stopped_reason,
        elapsed_seconds=time.perf_counter() - started,
    )
    if config.write_summary:
        root.mkdir(parents=True, exist_ok=True)
        _write_json(root / "parallel_feature_batch_summary.json", summary)
    return summary


def _run_candidate_api(candidate: CandidateRow, config: BatchConfig) -> RowWorkerResult:
    started = time.perf_counter()
    row_dir = _candidate_output_dir(config, candidate)
    manifest_path = row_dir / "attempts.jsonl"
    row_dir.mkdir(parents=True, exist_ok=True)
    executor = feature_bench.make_translation_executor(
        provider=config.provider,
        model=config.model,
        base_url=config.base_url,
        api_timeout_s=config.api_timeout_s,
        row_timeout_s=config.row_timeout_s,
        tolerance=config.tolerance,
        safety_cap=config.safety_cap,
        stagnation_limit=config.stagnation_limit,
        divergence_limit=config.divergence_limit,
        comparison_methods=config.comparison_methods,
        feature_aware=config.feature_aware,
        trusted_tolerance_mm=config.trusted_tolerance_mm,
        min_mesh_score=config.min_mesh_score,
        volume_only_success=config.volume_only_success,
        deterministic_only=config.deterministic_only,
        translation_mode=config.translation_mode,
    )
    summary = feature_bench.run_feature_family_benchmark(
        source_dir=config.source_dir,
        split=candidate.split,
        output_dir=str(row_dir),
        scan_limit=1,
        start_offset=candidate.global_index,
        family_filter=candidate.selected_families,
        family_exclude=config.family_exclude,
        max_attempts=1,
        dry_run=False,
        executor=executor,
        write_summary=True,
        manifest_jsonl=str(manifest_path),
        accepted_index_jsonl=config.accepted_index_jsonl,
        attempt_unsupported=config.attempt_unsupported,
    )
    ok = _has_manifest_rows(manifest_path) and int(summary.get("attempted", 0)) == 1
    error = "" if ok else "worker completed without a per-row attempts.jsonl manifest"
    return RowWorkerResult(
        candidate=candidate.to_dict(),
        output_dir=str(row_dir),
        manifest_jsonl=str(manifest_path),
        worker_mode="api",
        ok=ok,
        elapsed_seconds=time.perf_counter() - started,
        summary=summary,
        error=error,
    )


def _run_candidate_cli(candidate: CandidateRow, config: BatchConfig) -> RowWorkerResult:
    started = time.perf_counter()
    row_dir = _candidate_output_dir(config, candidate)
    manifest_path = row_dir / "attempts.jsonl"
    stdout_path = row_dir / "worker_stdout.txt"
    stderr_path = row_dir / "worker_stderr.txt"
    summary_path = row_dir / "feature_family_summary.json"
    row_dir.mkdir(parents=True, exist_ok=True)
    command = _build_worker_command(candidate, config, row_dir, manifest_path)
    timeout_s = config.worker_timeout_s
    if timeout_s is None and config.row_timeout_s and config.row_timeout_s > 0:
        timeout_s = config.row_timeout_s + 30.0

    try:
        completed = subprocess.run(
            command,
            cwd=str(PROJECT_ROOT),
            text=True,
            capture_output=True,
            timeout=timeout_s,
            check=False,
        )
        stdout_path.write_text(completed.stdout, encoding="utf-8")
        stderr_path.write_text(completed.stderr, encoding="utf-8")
        summary = _load_json_if_exists(summary_path)
        ok = completed.returncode == 0 and _has_manifest_rows(manifest_path)
        error = ""
        if completed.returncode != 0:
            error = f"worker exited with code {completed.returncode}"
        elif not manifest_path.exists():
            error = "worker completed without a per-row attempts.jsonl manifest"
        return RowWorkerResult(
            candidate=candidate.to_dict(),
            output_dir=str(row_dir),
            manifest_jsonl=str(manifest_path),
            worker_mode="cli",
            ok=ok,
            elapsed_seconds=time.perf_counter() - started,
            returncode=completed.returncode,
            summary=summary,
            error=error,
            stdout_path=str(stdout_path),
            stderr_path=str(stderr_path),
        )
    except subprocess.TimeoutExpired as exc:
        stdout_path.write_text(_process_output_text(exc.stdout), encoding="utf-8")
        stderr_path.write_text(_process_output_text(exc.stderr), encoding="utf-8")
        return RowWorkerResult(
            candidate=candidate.to_dict(),
            output_dir=str(row_dir),
            manifest_jsonl=str(manifest_path),
            worker_mode="cli",
            ok=False,
            elapsed_seconds=time.perf_counter() - started,
            error=f"worker exceeded launcher timeout of {timeout_s:g} seconds",
            stdout_path=str(stdout_path),
            stderr_path=str(stderr_path),
        )


def _build_worker_command(
    candidate: CandidateRow,
    config: BatchConfig,
    row_dir: Path,
    manifest_path: Path,
) -> list[str]:
    command = [
        sys.executable,
        "-m",
        "src.data.run_zero_to_cad_feature_benchmarks",
        "--source-dir",
        config.source_dir,
        "--split",
        candidate.split,
        "--output-dir",
        str(row_dir),
        "--scan-limit",
        "1",
        "--start-offset",
        str(candidate.global_index),
        "--max-attempts",
        "1",
        "--executor",
        "translator",
        "--execute",
        "--provider",
        config.provider,
        "--api-timeout-s",
        f"{config.api_timeout_s:g}",
        "--tolerance",
        f"{config.tolerance:g}",
        "--safety-cap",
        str(config.safety_cap),
        "--stagnation-limit",
        str(config.stagnation_limit),
        "--divergence-limit",
        str(config.divergence_limit),
        "--comparison-methods",
        ",".join(config.comparison_methods),
        "--trusted-tolerance-mm",
        f"{config.trusted_tolerance_mm:g}",
        "--min-mesh-score",
        f"{config.min_mesh_score:g}",
        "--translation-mode",
        config.translation_mode,
        "--manifest-jsonl",
        str(manifest_path),
    ]
    if config.model:
        command.extend(["--model", config.model])
    if config.base_url:
        command.extend(["--base-url", config.base_url])
    if config.row_timeout_s is not None:
        command.extend(["--row-timeout-s", f"{config.row_timeout_s:g}"])
    for family in candidate.selected_families:
        command.extend(["--family", family])
    for family in config.family_exclude:
        command.extend(["--exclude-family", family])
    for index_path in config.accepted_index_jsonl:
        command.extend(["--accepted-index", index_path])
    if config.feature_aware:
        command.append("--feature-aware")
    if config.volume_only_success:
        command.append("--volume-only-success")
    if config.deterministic_only:
        command.append("--deterministic-only")
    if config.attempt_unsupported:
        command.append("--attempt-unsupported")
    return command


def _batch_summary(
    *,
    config: BatchConfig,
    root: Path,
    candidates: list[CandidateRow],
    row_results: list[RowWorkerResult],
    stopped_reason: str | None,
    elapsed_seconds: float,
) -> dict[str, Any]:
    aggregate = _aggregate_row_summaries(
        result.summary for result in row_results
        if result.summary is not None
    )
    return {
        "schema": "zero_to_cad_parallel_feature_batch.v1",
        "source_dir": config.source_dir,
        "split": config.split,
        "output_dir": str(root),
        "dry_run": config.dry_run,
        "worker_mode": config.worker_mode,
        "start_offset": config.start_offset,
        "scan_limit": config.scan_limit,
        "candidate_limit": config.candidate_limit,
        "concurrency": config.concurrency,
        "row_timeout_s": config.row_timeout_s,
        "worker_timeout_s": config.worker_timeout_s,
        "provider": config.provider,
        "model": config.model,
        "base_url": config.base_url,
        "safety_cap": config.safety_cap,
        "translation_mode": config.translation_mode,
        "family_filter": sorted(_normalize_families(config.family_filter)),
        "family_exclude": sorted(_normalize_families(config.family_exclude)),
        "accepted_index_jsonl": config.accepted_index_jsonl,
        "attempt_unsupported": config.attempt_unsupported,
        "comparison_methods": config.comparison_methods,
        "elapsed_seconds": elapsed_seconds,
        "stopped_reason": stopped_reason,
        "candidates_selected": len(candidates),
        "workers_launched": 0 if config.dry_run else len(row_results),
        "workers_ok": sum(1 for result in row_results if result.ok),
        "workers_failed": sum(1 for result in row_results if not result.ok),
        "aggregate": aggregate,
        "candidates": [candidate.to_dict() for candidate in candidates],
        "rows": [result.to_dict() for result in row_results],
    }


def _aggregate_row_summaries(summaries: Iterable[dict[str, Any]]) -> dict[str, Any]:
    fields = ("attempted", "executed", "matched", "failed", "skipped_accepted")
    totals = {field: 0 for field in fields}
    for summary in summaries:
        for field_name in fields:
            totals[field_name] += int(summary.get(field_name, 0) or 0)
    executed = totals["executed"]
    matched = totals["matched"]
    totals["match_rate"] = round(matched / executed, 4) if executed else 0.0
    return totals


def _exception_result(candidate: CandidateRow, config: BatchConfig, exc: Exception) -> RowWorkerResult:
    row_dir = _candidate_output_dir(config, candidate)
    manifest_path = row_dir / "attempts.jsonl"
    return RowWorkerResult(
        candidate=candidate.to_dict(),
        output_dir=str(row_dir),
        manifest_jsonl=str(manifest_path),
        worker_mode=config.worker_mode,
        ok=False,
        elapsed_seconds=0.0,
        error=str(exc),
    )


def _candidate_output_dir(config: BatchConfig, candidate: CandidateRow) -> Path:
    safe_uuid = _safe_path_fragment(candidate.uuid) or "missing_uuid"
    return (
        config.root_dir()
        / "rows"
        / f"{candidate.ordinal:05d}_{candidate.split}_{candidate.global_index:08d}_{safe_uuid}"
    )


def _load_accepted_index(paths: list[str]) -> dict[tuple[str, str], dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path_text in paths:
        path = Path(path_text)
        if path.exists():
            records.extend(load_manifest_jsonl(path))
    return build_accepted_index(records)


def _iter_splits(split: str) -> tuple[str, ...]:
    if split == "all":
        return ALL_SPLITS
    if split not in ALL_SPLITS:
        raise ValueError(f"Unknown split {split!r}; expected one of {[*ALL_SPLITS, 'all']}")
    return (split,)


def _normalize_families(families: Iterable[str] | None) -> set[str]:
    return {
        str(family).strip().lower()
        for family in families or []
        if str(family).strip()
    }


def _safe_path_fragment(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("._")[:80]


def _timestamp_run_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _load_json_if_exists(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _has_manifest_rows(path: Path) -> bool:
    return path.exists() and path.stat().st_size > 0


def _process_output_text(value: str | bytes | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")


def _parse_csv_repeated(values: list[str] | None) -> list[str]:
    parsed: list[str] = []
    for value in values or []:
        parsed.extend(item.strip() for item in value.split(",") if item.strip())
    return parsed


def _parse_methods(value: str | None) -> list[str]:
    if not value or value.lower() in {"none", "off", "false"}:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Launch isolated parallel Zero-to-CAD feature benchmark rows.",
    )
    parser.add_argument("--source-dir", default=DEFAULT_SOURCE_DIR)
    parser.add_argument("--split", default="train", choices=[*ALL_SPLITS, "all"])
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--run-id", default="")
    parser.add_argument("--scan-limit", type=int, default=None)
    parser.add_argument("--start-offset", type=int, default=0)
    parser.add_argument("--candidate-limit", type=int, default=None)
    parser.add_argument("--concurrency", type=int, default=1)
    parser.add_argument("--family", action="append", default=[])
    parser.add_argument("--exclude-family", action="append", default=[])
    parser.add_argument("--accepted-index", action="append", default=[])
    parser.add_argument("--attempt-unsupported", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--worker-mode", choices=["cli", "api"], default="cli")
    parser.add_argument("--provider", default="deepseek")
    parser.add_argument("--model", default=None)
    parser.add_argument("--base-url", default=None)
    parser.add_argument("--api-timeout-s", type=float, default=120.0)
    parser.add_argument("--row-timeout-s", type=float, default=None)
    parser.add_argument("--worker-timeout-s", type=float, default=None)
    parser.add_argument("--tolerance", type=float, default=0.05)
    parser.add_argument("--safety-cap", type=int, default=5)
    parser.add_argument("--stagnation-limit", type=int, default=2)
    parser.add_argument("--divergence-limit", type=int, default=2)
    parser.add_argument("--comparison-methods", default="slice")
    parser.add_argument("--feature-aware", action="store_true")
    parser.add_argument("--trusted-tolerance-mm", type=float, default=0.25)
    parser.add_argument("--min-mesh-score", type=float, default=95.0)
    parser.add_argument("--volume-only-success", action="store_true")
    parser.add_argument("--deterministic-only", action="store_true")
    parser.add_argument(
        "--translation-mode",
        default="planner_guided",
        choices=["planner_guided", "ai_heavy"],
    )
    parser.add_argument("--no-summary-file", action="store_true")
    args = parser.parse_args(argv)

    config = BatchConfig(
        source_dir=args.source_dir,
        split=args.split,
        output_dir=args.output_dir,
        run_id=args.run_id,
        scan_limit=args.scan_limit,
        start_offset=args.start_offset,
        candidate_limit=args.candidate_limit,
        concurrency=args.concurrency,
        family_filter=_parse_csv_repeated(args.family),
        family_exclude=_parse_csv_repeated(args.exclude_family),
        accepted_index_jsonl=_parse_csv_repeated(args.accepted_index),
        attempt_unsupported=args.attempt_unsupported,
        dry_run=not args.execute,
        worker_mode=args.worker_mode,
        provider=args.provider,
        model=args.model,
        base_url=args.base_url,
        api_timeout_s=args.api_timeout_s,
        row_timeout_s=args.row_timeout_s,
        worker_timeout_s=args.worker_timeout_s,
        tolerance=args.tolerance,
        safety_cap=args.safety_cap,
        stagnation_limit=args.stagnation_limit,
        divergence_limit=args.divergence_limit,
        comparison_methods=_parse_methods(args.comparison_methods),
        feature_aware=args.feature_aware,
        trusted_tolerance_mm=args.trusted_tolerance_mm,
        min_mesh_score=args.min_mesh_score,
        volume_only_success=args.volume_only_success,
        deterministic_only=args.deterministic_only,
        translation_mode=args.translation_mode,
        write_summary=not args.no_summary_file,
    )
    summary = launch_parallel_feature_batch(config)
    print(json.dumps(summary, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
