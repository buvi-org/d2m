"""Feature-family benchmark runner for Zero-to-CAD SubCAD coverage.

This runner is deliberately lightweight.  It scans Zero-to-CAD rows, buckets
them by the pure SubCAD planner's feature families, and can optionally invoke an
injected per-row executor.  The executor seam is where the live translator and
original STEP comparison can be attached later without making scan tests costly.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from .pure_subcad_planner import plan_pure_subcad_features
from .zero_to_cad_dataset_manifest import (
    build_accepted_index,
    load_manifest_jsonl,
    make_attempt_record,
    write_manifest_jsonl,
)


DEFAULT_SOURCE_DIR = "data/zero_to_cad_100k"
DEFAULT_OUTPUT_DIR = "runs/zero_to_cad_feature_benchmarks"
UNSUPPORTED_FAMILY = "__unsupported__"
ALL_SPLITS = ("train", "val", "test")

RowExecutor = Callable[[dict[str, Any], dict[str, Any]], dict[str, Any]]
MatchRateGuardrail = tuple[int, float]


def iter_zero_to_cad_rows(*args: Any, **kwargs: Any):
    """Lazy bridge to the existing parquet reader without importing live runner deps."""
    from .run_zero_to_cad_translations import iter_zero_to_cad_rows as _iter_rows

    return _iter_rows(*args, **kwargs)


@dataclass
class FamilyStats:
    family: str
    plannable: int = 0
    attempted: int = 0
    executed: int = 0
    matched: int = 0
    failed: int = 0
    unsupported: int = 0
    examples: list[dict[str, Any]] = field(default_factory=list)
    statuses: dict[str, int] = field(default_factory=dict)

    def record_status(self, status: str) -> None:
        self.statuses[status] = self.statuses.get(status, 0) + 1


@dataclass
class BenchmarkStats:
    source_dir: str
    split: str
    output_dir: str
    dry_run: bool
    scan_limit: int | None
    per_family_limit: int | None
    family_filter: list[str] = field(default_factory=list)
    family_exclude: list[str] = field(default_factory=list)
    target_successes: int = 100000
    max_attempts: int | None = None
    max_failures: int | None = None
    max_consecutive_failures: int | None = None
    target_matches: int | None = None
    min_match_rate_after_attempts: list[dict[str, float | int]] = field(default_factory=list)
    stopped_reason: str | None = None
    scanned: int = 0
    plannable: int = 0
    selected: int = 0
    filtered_out: int = 0
    attempted: int = 0
    executed: int = 0
    matched: int = 0
    failed: int = 0
    skipped_accepted: int = 0
    consecutive_failures: int = 0
    unsupported: int = 0
    elapsed_seconds: float = 0.0

    @property
    def match_rate(self) -> float:
        return round(self.matched / self.executed, 4) if self.executed else 0.0

    @property
    def remaining_to_goal(self) -> int:
        return max(int(self.target_successes) - int(self.matched), 0)


def run_feature_family_benchmark(
    *,
    source_dir: str = DEFAULT_SOURCE_DIR,
    split: str = "train",
    output_dir: str = DEFAULT_OUTPUT_DIR,
    scan_limit: int | None = None,
    start_offset: int = 0,
    per_family_limit: int | None = None,
    family_filter: list[str] | None = None,
    family_exclude: list[str] | None = None,
    target_successes: int = 100000,
    max_attempts: int | None = None,
    max_failures: int | None = None,
    max_consecutive_failures: int | None = None,
    target_matches: int | None = None,
    min_match_rate_after_attempts: list[MatchRateGuardrail] | None = None,
    dry_run: bool = True,
    executor: RowExecutor | None = None,
    write_summary: bool = True,
    manifest_jsonl: str | None = None,
    accepted_index_jsonl: list[str] | None = None,
    _initial_attempted: int = 0,
    _initial_executed: int = 0,
    _initial_matched: int = 0,
    _initial_failed: int = 0,
) -> dict[str, Any]:
    """Scan or execute Zero-to-CAD rows grouped by planner feature family.

    ``dry_run=True`` never calls ``executor``.  With ``dry_run=False``, plannable
    rows selected by the optional per-family limit are counted as attempted; an
    executor result with ``executed`` and ``matched`` fields controls the later
    lifecycle counters.
    """
    root = Path(output_dir)
    if write_summary:
        root.mkdir(parents=True, exist_ok=True)
    manifest_path = Path(manifest_jsonl) if manifest_jsonl else None
    accepted_index = _load_accepted_index(accepted_index_jsonl)

    stats = BenchmarkStats(
        source_dir=source_dir,
        split=split,
        output_dir=str(root),
        dry_run=dry_run,
        scan_limit=scan_limit,
        per_family_limit=per_family_limit,
        family_filter=sorted(_normalize_family_filter(family_filter)),
        family_exclude=sorted(_normalize_family_filter(family_exclude)),
        target_successes=target_successes,
        max_attempts=max_attempts,
        max_failures=max_failures,
        max_consecutive_failures=max_consecutive_failures,
        target_matches=target_matches,
        min_match_rate_after_attempts=_serialize_match_rate_guardrails(
            _normalize_match_rate_guardrails(min_match_rate_after_attempts)
        ),
    )
    family_stats: dict[str, FamilyStats] = {}
    attempts_by_family: Counter[str] = Counter()
    started = time.perf_counter()
    requested_families = set(stats.family_filter)
    excluded_families = set(stats.family_exclude)
    match_rate_guardrails = _normalize_match_rate_guardrails(min_match_rate_after_attempts)
    stats.stopped_reason = _stop_reason(
        stats,
        max_attempts=max_attempts,
        max_failures=max_failures,
        max_consecutive_failures=max_consecutive_failures,
        target_matches=target_matches,
        min_match_rate_after_attempts=match_rate_guardrails,
        initial_attempted=_initial_attempted,
        initial_executed=_initial_executed,
        initial_matched=_initial_matched,
        initial_failed=_initial_failed,
    )

    for row in iter_zero_to_cad_rows(source_dir, split, start_offset=start_offset, limit=scan_limit):
        if stats.stopped_reason:
            break
        stats.scanned += 1
        accepted_record = accepted_index.get((split, str(row.get("uuid", ""))))
        if accepted_record is not None:
            accepted_families = [
                str(family) for family in accepted_record.get("families") or []
                if str(family)
            ]
            if excluded_families and any(family in excluded_families for family in accepted_families):
                stats.filtered_out += 1
                continue
            if requested_families:
                accepted_families = [
                    family for family in accepted_families if family in requested_families
                ]
            if not requested_families or accepted_families:
                _record_skipped_accepted(
                    stats,
                    family_stats,
                    row,
                    accepted_record,
                    accepted_families,
                )
                stats.stopped_reason = _stop_reason(
                    stats,
                    max_attempts=max_attempts,
                    max_failures=max_failures,
                    max_consecutive_failures=max_consecutive_failures,
                    target_matches=target_matches,
                    min_match_rate_after_attempts=match_rate_guardrails,
                    initial_attempted=_initial_attempted,
                    initial_executed=_initial_executed,
                    initial_matched=_initial_matched,
                    initial_failed=_initial_failed,
                )
                continue
        plan = plan_pure_subcad_features(row.get("ops_trace") or [], row.get("cadquery_code") or "")
        row_summary = summarize_row(row, plan.to_dict())

        if not plan.compatible:
            stats.unsupported += 1
            bucket = family_stats.setdefault(
                UNSUPPORTED_FAMILY,
                FamilyStats(family=UNSUPPORTED_FAMILY),
            )
            bucket.unsupported += 1
            _append_example(bucket, row_summary)
            continue

        families = sorted({feature.family for feature in plan.features})
        statuses = Counter(feature.planner_status for feature in plan.features)
        stats.plannable += 1
        if excluded_families and any(family in excluded_families for family in families):
            stats.filtered_out += 1
            continue
        selected_families = families
        if requested_families:
            selected_families = [family for family in families if family in requested_families]
        if not selected_families:
            stats.filtered_out += 1
            continue

        stats.selected += 1
        for family in selected_families:
            bucket = family_stats.setdefault(family, FamilyStats(family=family))
            bucket.plannable += 1
            for status, count in statuses.items():
                bucket.statuses[status] = bucket.statuses.get(status, 0) + count
            _append_example(bucket, row_summary)

        if dry_run:
            continue
        if per_family_limit is not None and any(
            attempts_by_family[family] >= per_family_limit for family in selected_families
        ):
            continue

        stats.attempted += 1
        for family in selected_families:
            attempts_by_family[family] += 1
            family_stats[family].attempted += 1

        context = {
            "families": families,
            "selected_families": selected_families,
            "planner": plan.to_dict(),
            "output_dir": str(root),
        }
        try:
            result = executor(row, context) if executor else {"executed": False, "matched": False}
        except Exception as exc:
            result = {"executed": False, "matched": False, "failed": True, "error": str(exc)}
        executed = bool(result.get("executed"))
        matched = bool(result.get("matched"))
        failed = bool(result.get("failed", executed and not matched))

        if executed:
            stats.executed += 1
            for family in selected_families:
                family_stats[family].executed += 1
        if matched:
            stats.matched += 1
            for family in selected_families:
                family_stats[family].matched += 1
        if failed:
            stats.failed += 1
            stats.consecutive_failures += 1
            for family in selected_families:
                family_stats[family].failed += 1
        else:
            stats.consecutive_failures = 0

        if manifest_path is not None:
            write_manifest_jsonl(
                manifest_path,
                [_manifest_record(row, split, selected_families, plan.to_dict(), result)],
                append=True,
            )

        stats.stopped_reason = _stop_reason(
            stats,
            max_attempts=max_attempts,
            max_failures=max_failures,
            max_consecutive_failures=max_consecutive_failures,
            target_matches=target_matches,
            min_match_rate_after_attempts=match_rate_guardrails,
            initial_attempted=_initial_attempted,
            initial_executed=_initial_executed,
            initial_matched=_initial_matched,
            initial_failed=_initial_failed,
        )

    stats.elapsed_seconds = time.perf_counter() - started
    summary = {
        "schema": "zero_to_cad_feature_family_benchmark.v1",
        **asdict(stats),
        "match_rate": stats.match_rate,
        "remaining_to_goal": stats.remaining_to_goal,
        "families": {
            family: asdict(bucket)
            for family, bucket in sorted(family_stats.items())
        },
    }
    if write_summary:
        _write_json(root / "feature_family_summary.json", summary)
    return summary


def run_feature_family_benchmark_splits(
    *,
    source_dir: str = DEFAULT_SOURCE_DIR,
    splits: list[str] | tuple[str, ...] = ALL_SPLITS,
    output_dir: str = DEFAULT_OUTPUT_DIR,
    scan_limit: int | None = None,
    start_offset: int = 0,
    per_family_limit: int | None = None,
    family_filter: list[str] | None = None,
    family_exclude: list[str] | None = None,
    target_successes: int = 100000,
    max_attempts: int | None = None,
    max_failures: int | None = None,
    max_consecutive_failures: int | None = None,
    target_matches: int | None = None,
    min_match_rate_after_attempts: list[MatchRateGuardrail] | None = None,
    dry_run: bool = True,
    executor: RowExecutor | None = None,
    write_summary: bool = True,
    manifest_jsonl: str | None = None,
    accepted_index_jsonl: list[str] | None = None,
) -> dict[str, Any]:
    """Run split-level scans and return one aggregate summary."""
    root = Path(output_dir)
    if write_summary:
        root.mkdir(parents=True, exist_ok=True)

    split_summaries = []
    for split in splits:
        attempted_so_far = sum(int(summary.get("attempted", 0)) for summary in split_summaries)
        failed_so_far = sum(int(summary.get("failed", 0)) for summary in split_summaries)
        matched_so_far = sum(int(summary.get("matched", 0)) for summary in split_summaries)
        executed_so_far = sum(int(summary.get("executed", 0)) for summary in split_summaries)
        split_summary = run_feature_family_benchmark(
            source_dir=source_dir,
            split=split,
            output_dir=str(root / split),
            scan_limit=scan_limit,
            start_offset=start_offset,
            per_family_limit=per_family_limit,
            family_filter=family_filter,
            family_exclude=family_exclude,
            target_successes=target_successes,
            max_attempts=max_attempts,
            max_failures=max_failures,
            max_consecutive_failures=max_consecutive_failures,
            target_matches=target_matches,
            min_match_rate_after_attempts=min_match_rate_after_attempts,
            dry_run=dry_run,
            executor=executor,
            write_summary=write_summary,
            manifest_jsonl=manifest_jsonl,
            accepted_index_jsonl=accepted_index_jsonl,
            _initial_attempted=attempted_so_far,
            _initial_executed=executed_so_far,
            _initial_matched=matched_so_far,
            _initial_failed=failed_so_far,
        )
        split_summaries.append(split_summary)
        if split_summary.get("stopped_reason"):
            break

    aggregate = _aggregate_split_summaries(
        split_summaries,
        source_dir=source_dir,
        output_dir=str(root),
        family_filter=family_filter,
        family_exclude=family_exclude,
        target_successes=target_successes,
        max_attempts=max_attempts,
        max_failures=max_failures,
        max_consecutive_failures=max_consecutive_failures,
        target_matches=target_matches,
        min_match_rate_after_attempts=min_match_rate_after_attempts,
        dry_run=dry_run,
        scan_limit=scan_limit,
        per_family_limit=per_family_limit,
    )
    if write_summary:
        _write_json(root / "feature_family_summary_all.json", aggregate)
    return aggregate


def make_translation_executor(
    *,
    provider: str = "deepseek",
    model: str | None = None,
    tolerance: float = 0.05,
    safety_cap: int = 5,
    stagnation_limit: int = 2,
    divergence_limit: int = 2,
    comparison_methods: list[str] | None = None,
    feature_aware: bool = False,
    trusted_tolerance_mm: float = 0.25,
    min_mesh_score: float = 95.0,
    volume_only_success: bool = False,
    deterministic_only: bool = False,
    translation_mode: str = "planner_guided",
) -> RowExecutor:
    """Create a guarded executor backed by the live translator runner.

    This is intentionally opt-in from the CLI. Dry scans and tests do not load
    provider keys or spend AI requests.
    """
    from .agentic_translator import AgenticTranslator, _load_local_env_if_present
    from .run_zero_to_cad_translations import (
        _apply_match_policy,
        _require_provider_key,
        _sample_output_dir,
        _save_result,
        _translate_row,
        _write_source_artifacts,
    )

    _load_local_env_if_present()
    _require_provider_key(provider)
    translator = AgenticTranslator(
        provider=provider,
        model=model,
        tolerance=tolerance,
        stagnation_limit=stagnation_limit,
        divergence_limit=divergence_limit,
        safety_cap=safety_cap,
        verbose=True,
        comparison_methods=comparison_methods,
        feature_aware=feature_aware,
        strict_mesh_convergence=not volume_only_success,
        min_mesh_score=min_mesh_score,
        mesh_tolerance_mm=trusted_tolerance_mm,
        deterministic_only=deterministic_only,
        translation_mode=translation_mode,
    )

    def _execute(row: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        output_root = Path(context["output_dir"])
        sample_dir = _sample_output_dir(output_root, row["global_index"], row["uuid"])
        sample_dir.mkdir(parents=True, exist_ok=True)
        row_for_run = dict(row)
        row_for_run["compatibility"] = {
            "compatible": True,
            "planner": context.get("planner"),
            "selected_families": context.get("selected_families", context.get("families", [])),
        }
        _write_source_artifacts(sample_dir, row_for_run)
        result = _translate_row(translator, row_for_run, sample_dir)
        result = _apply_match_policy(
            result,
            comparison_methods=comparison_methods,
            trusted_tolerance_mm=trusted_tolerance_mm,
            min_mesh_score=min_mesh_score,
            volume_only_success=volume_only_success,
        )
        _save_result(sample_dir, row_for_run, result, provider, model)
        exec_result = result.get("exec_result") or {}
        executed = bool(exec_result.get("success"))
        matched = bool(result.get("success"))
        return {
            "executed": executed,
            "matched": matched,
            "failed": not matched,
            "sample_dir": str(sample_dir),
            "stop_reason": result.get("stop_reason"),
            "trusted_match": result.get("trusted_match"),
            "comparison_methods": comparison_methods or [],
            "trusted_tolerance_mm": trusted_tolerance_mm,
            "min_mesh_score": min_mesh_score,
            "volume_only_success": volume_only_success,
            "error": result.get("error"),
        }

    return _execute


def summarize_row(row: dict[str, Any], planner: dict[str, Any]) -> dict[str, Any]:
    features = planner.get("features") or []
    return {
        "global_index": row.get("global_index"),
        "uuid": row.get("uuid"),
        "cadquery_chars": len(row.get("cadquery_code") or ""),
        "ops_trace_count": len(row.get("ops_trace") or []),
        "families": sorted({feature.get("family") for feature in features if feature.get("family")}),
        "operations": sorted({feature.get("operation") for feature in features if feature.get("operation")}),
    }


def _manifest_record(
    row: dict[str, Any],
    split: str,
    selected_families: list[str],
    planner: dict[str, Any],
    result: dict[str, Any],
) -> dict[str, Any]:
    sample_dir = Path(str(result.get("sample_dir", ""))) if result.get("sample_dir") else None
    status = "matched" if result.get("matched") else "failed"
    if result.get("executed") and not result.get("matched"):
        status = "executed"
    if result.get("failed"):
        status = "failed"
    artifact_base = sample_dir.as_posix() if sample_dir else ""
    artifacts = {}
    if sample_dir:
        artifacts = {
            "original_step": f"{artifact_base}/original_model.step",
            "generated_subcad": f"{artifact_base}/generated_subcad.py",
            "generated_step": f"{artifact_base}/generated.step",
            "process_plan": f"{artifact_base}/process_plan.json",
            "validation": f"{artifact_base}/validation.json",
            "comparison": f"{artifact_base}/result.json",
            "economics": f"{artifact_base}/economics.json",
        }
    return make_attempt_record(
        split=split,
        uuid=str(row.get("uuid", "")),
        global_index=int(row.get("global_index", 0)),
        parquet_file=str(row.get("parquet_file", "")),
        row_index=row.get("row_index"),
        artifacts=artifacts,
        planner="pure_subcad",
        families=selected_families,
        planner_tags=[
            str(feature.get("operation"))
            for feature in planner.get("features", [])
            if feature.get("operation")
        ],
        status=status,
        accepted=bool(result.get("matched")),
        tolerance_policy={
            "comparison_methods": result.get("comparison_methods", []),
            "tolerance_mm": result.get("trusted_tolerance_mm"),
            "min_mesh_score": result.get("min_mesh_score"),
            "volume_only_success": result.get("volume_only_success"),
            "extra": {
                "trusted_match": result.get("trusted_match"),
                "stop_reason": result.get("stop_reason"),
            },
        },
        errors=[result.get("error")] if result.get("error") else [],
        notes=str(result.get("stop_reason") or ""),
    )


def _append_example(bucket: FamilyStats, row_summary: dict[str, Any], limit: int = 5) -> None:
    if len(bucket.examples) < limit:
        bucket.examples.append(row_summary)


def _load_accepted_index(paths: list[str] | None) -> dict[tuple[str, str], dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path_text in paths or []:
        path = Path(path_text)
        if path.exists():
            records.extend(load_manifest_jsonl(path))
    return build_accepted_index(records)


def _record_skipped_accepted(
    stats: BenchmarkStats,
    family_stats: dict[str, FamilyStats],
    row: dict[str, Any],
    accepted_record: dict[str, Any],
    accepted_families: list[str],
) -> None:
    stats.selected += 1
    stats.matched += 1
    stats.skipped_accepted += 1
    row_summary = {
        "global_index": row.get("global_index"),
        "uuid": row.get("uuid"),
        "cadquery_chars": len(row.get("cadquery_code") or ""),
        "ops_trace_count": len(row.get("ops_trace") or []),
        "families": accepted_families,
        "operations": sorted({
            str(tag) for tag in accepted_record.get("planner_tags") or []
            if str(tag)
        }),
        "skipped_accepted": True,
    }
    for family in accepted_families or ["__accepted__"]:
        bucket = family_stats.setdefault(family, FamilyStats(family=family))
        bucket.matched += 1
        _append_example(bucket, row_summary)


def _normalize_family_filter(family_filter: list[str] | None) -> set[str]:
    return {
        str(family).strip().lower()
        for family in (family_filter or [])
        if str(family).strip()
    }


def _aggregate_split_summaries(
    split_summaries: list[dict[str, Any]],
    *,
    source_dir: str,
    output_dir: str,
    family_filter: list[str] | None,
    family_exclude: list[str] | None,
    target_successes: int,
    max_attempts: int | None,
    max_failures: int | None,
    max_consecutive_failures: int | None,
    target_matches: int | None,
    min_match_rate_after_attempts: list[MatchRateGuardrail] | None,
    dry_run: bool,
    scan_limit: int | None,
    per_family_limit: int | None,
) -> dict[str, Any]:
    numeric_fields = [
        "scanned",
        "plannable",
        "selected",
        "filtered_out",
        "attempted",
        "executed",
        "matched",
        "failed",
        "skipped_accepted",
        "unsupported",
        "elapsed_seconds",
    ]
    totals = {field_name: 0 for field_name in numeric_fields}
    families: dict[str, dict[str, Any]] = {}

    for summary in split_summaries:
        for field_name in numeric_fields:
            totals[field_name] += summary.get(field_name, 0)
        for family, payload in (summary.get("families") or {}).items():
            bucket = families.setdefault(
                family,
                {
                    "family": family,
                    "plannable": 0,
                    "attempted": 0,
                    "executed": 0,
                    "matched": 0,
                    "failed": 0,
                    "unsupported": 0,
                    "examples": [],
                    "statuses": {},
                },
            )
            for field_name in ("plannable", "attempted", "executed", "matched", "failed", "unsupported"):
                bucket[field_name] += payload.get(field_name, 0)
            for status, count in (payload.get("statuses") or {}).items():
                bucket["statuses"][status] = bucket["statuses"].get(status, 0) + count
            for example in payload.get("examples") or []:
                if len(bucket["examples"]) < 5:
                    bucket["examples"].append(example)

    matched = int(totals["matched"])
    executed = int(totals["executed"])
    stopped_reason = next(
        (summary.get("stopped_reason") for summary in split_summaries if summary.get("stopped_reason")),
        None,
    )
    return {
        "schema": "zero_to_cad_feature_family_benchmark.aggregate.v1",
        "source_dir": source_dir,
        "split": "all",
        "splits": [summary.get("split") for summary in split_summaries],
        "output_dir": output_dir,
        "dry_run": dry_run,
        "scan_limit": scan_limit,
        "per_family_limit": per_family_limit,
        "family_filter": sorted(_normalize_family_filter(family_filter)),
        "family_exclude": sorted(_normalize_family_filter(family_exclude)),
        "target_successes": target_successes,
        "max_attempts": max_attempts,
        "max_failures": max_failures,
        "max_consecutive_failures": max_consecutive_failures,
        "target_matches": target_matches,
        "min_match_rate_after_attempts": _serialize_match_rate_guardrails(
            _normalize_match_rate_guardrails(min_match_rate_after_attempts)
        ),
        "stopped_reason": stopped_reason,
        **totals,
        "consecutive_failures": (
            int(split_summaries[-1].get("consecutive_failures", 0))
            if split_summaries
            else 0
        ),
        "match_rate": round(matched / executed, 4) if executed else 0.0,
        "remaining_to_goal": max(int(target_successes) - matched, 0),
        "per_split": {
            summary.get("split", f"split_{index}"): summary
            for index, summary in enumerate(split_summaries)
        },
        "families": dict(sorted(families.items())),
    }


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")


def _stop_reason(
    stats: BenchmarkStats,
    *,
    max_attempts: int | None,
    max_failures: int | None,
    max_consecutive_failures: int | None,
    target_matches: int | None,
    min_match_rate_after_attempts: list[MatchRateGuardrail],
    initial_attempted: int = 0,
    initial_executed: int = 0,
    initial_matched: int = 0,
    initial_failed: int = 0,
) -> str | None:
    total_attempted = initial_attempted + stats.attempted
    total_executed = initial_executed + stats.executed
    total_matched = initial_matched + stats.matched
    total_failed = initial_failed + stats.failed
    match_rate = round(total_matched / total_executed, 4) if total_executed else 0.0

    if max_attempts is not None and total_attempted >= max_attempts:
        return "max_attempts"
    if max_failures is not None and total_failed >= max_failures:
        return "max_failures"
    if (
        max_consecutive_failures is not None
        and stats.consecutive_failures >= max_consecutive_failures
    ):
        return "max_consecutive_failures"
    if target_matches is not None and total_matched >= target_matches:
        return "target_matches"
    for attempts, min_rate in min_match_rate_after_attempts:
        if total_attempted >= attempts and match_rate < min_rate:
            return f"min_match_rate_after_attempts:{attempts}:{min_rate:g}"
    return None


def _normalize_match_rate_guardrails(
    guardrails: list[MatchRateGuardrail] | None,
) -> list[MatchRateGuardrail]:
    normalized: list[MatchRateGuardrail] = []
    for attempts, min_rate in guardrails or []:
        attempts = int(attempts)
        min_rate = float(min_rate)
        if attempts <= 0:
            raise ValueError("min_match_rate_after_attempts attempts must be positive")
        if min_rate < 0 or min_rate > 1:
            raise ValueError("min_match_rate_after_attempts rate must be between 0 and 1")
        normalized.append((attempts, min_rate))
    return sorted(normalized)


def _serialize_match_rate_guardrails(
    guardrails: list[MatchRateGuardrail],
) -> list[dict[str, float | int]]:
    return [
        {"attempts": attempts, "min_match_rate": min_rate}
        for attempts, min_rate in guardrails
    ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Scan Zero-to-CAD rows by pure planner feature family.",
    )
    parser.add_argument("--source-dir", default=DEFAULT_SOURCE_DIR)
    parser.add_argument("--split", default="train", choices=[*ALL_SPLITS, "all"])
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--scan-limit", type=int, default=None)
    parser.add_argument("--start-offset", type=int, default=0)
    parser.add_argument("--per-family-limit", type=int, default=None)
    parser.add_argument(
        "--family",
        action="append",
        default=[],
        help="Restrict selected rows to a planner family. May be repeated.",
    )
    parser.add_argument(
        "--exclude-family",
        action="append",
        default=[],
        help="Skip rows containing this planner family. May be repeated.",
    )
    parser.add_argument("--target-successes", type=int, default=100000)
    parser.add_argument(
        "--max-attempts",
        type=int,
        default=None,
        help="Stop after this many selected rows have been attempted.",
    )
    parser.add_argument(
        "--max-failures",
        type=int,
        default=None,
        help="Stop after this many attempted rows fail.",
    )
    parser.add_argument(
        "--max-consecutive-failures",
        type=int,
        default=None,
        help="Stop after this many attempted rows fail in a row.",
    )
    parser.add_argument(
        "--target-matches",
        type=int,
        default=None,
        help="Stop after this many attempted rows match.",
    )
    parser.add_argument(
        "--min-match-rate-after-attempts",
        action="append",
        default=[],
        metavar="ATTEMPTS:RATE",
        help="Stop when match rate is below RATE after ATTEMPTS attempts. May be repeated.",
    )
    parser.add_argument(
        "--executor",
        default="disabled",
        choices=["disabled", "translator"],
        help="Executor to use with --execute. Default is disabled to avoid accidental AI spend.",
    )
    parser.add_argument("--provider", default="deepseek")
    parser.add_argument("--model", default=None)
    parser.add_argument("--tolerance", type=float, default=0.05)
    parser.add_argument("--safety-cap", type=int, default=5)
    parser.add_argument("--stagnation-limit", type=int, default=2)
    parser.add_argument("--divergence-limit", type=int, default=2)
    parser.add_argument("--comparison-methods", default="slice")
    parser.add_argument("--feature-aware", action="store_true")
    parser.add_argument("--trusted-tolerance-mm", type=float, default=0.25)
    parser.add_argument("--min-mesh-score", type=float, default=95.0)
    parser.add_argument(
        "--volume-only-success",
        action="store_true",
        help="Debug mode only: count volume-ratio matches as successes.",
    )
    parser.add_argument(
        "--deterministic-only",
        action="store_true",
        help="Execute deterministic planner output only; do not spend LLM repair calls after a deterministic miss.",
    )
    parser.add_argument(
        "--translation-mode",
        default="planner_guided",
        choices=["planner_guided", "ai_heavy"],
        help="planner_guided uses deterministic/planner-first behavior; ai_heavy skips deterministic builders and lets the LLM infer pure SubCAD operations from evidence.",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Attempt selected rows. Requires --executor translator for live AI runs.",
    )
    parser.add_argument("--no-summary-file", action="store_true")
    parser.add_argument(
        "--manifest-jsonl",
        default=None,
        help="Optional JSONL path for per-attempt dataset manifest records.",
    )
    parser.add_argument(
        "--accepted-index",
        action="append",
        default=[],
        help="Manifest JSONL path(s) to read for already accepted matched rows. May be repeated or comma-separated.",
    )
    args = parser.parse_args(argv)
    comparison_methods = _parse_methods(args.comparison_methods)
    accepted_index_paths = _parse_path_list(args.accepted_index)
    try:
        match_rate_guardrails = _parse_match_rate_guardrails(args.min_match_rate_after_attempts)
    except ValueError as exc:
        parser.error(str(exc))
    executor = None
    if args.execute and args.executor == "disabled":
        parser.error("--execute requires --executor translator so live AI spend is explicit.")
    if args.execute and args.executor == "translator":
        executor = make_translation_executor(
            provider=args.provider,
            model=args.model,
            tolerance=args.tolerance,
            safety_cap=args.safety_cap,
            stagnation_limit=args.stagnation_limit,
            divergence_limit=args.divergence_limit,
            comparison_methods=comparison_methods,
            feature_aware=args.feature_aware,
            trusted_tolerance_mm=args.trusted_tolerance_mm,
            min_mesh_score=args.min_mesh_score,
            volume_only_success=args.volume_only_success,
            deterministic_only=args.deterministic_only,
            translation_mode=args.translation_mode,
        )

    if args.split == "all":
        summary = run_feature_family_benchmark_splits(
            source_dir=args.source_dir,
            output_dir=args.output_dir,
            scan_limit=args.scan_limit,
            start_offset=args.start_offset,
            per_family_limit=args.per_family_limit,
            family_filter=args.family,
            family_exclude=args.exclude_family,
            target_successes=args.target_successes,
            max_attempts=args.max_attempts,
            max_failures=args.max_failures,
            max_consecutive_failures=args.max_consecutive_failures,
            target_matches=args.target_matches,
            min_match_rate_after_attempts=match_rate_guardrails,
            dry_run=not args.execute,
            executor=executor,
            write_summary=not args.no_summary_file,
            manifest_jsonl=args.manifest_jsonl,
            accepted_index_jsonl=accepted_index_paths,
        )
    else:
        summary = run_feature_family_benchmark(
            source_dir=args.source_dir,
            split=args.split,
            output_dir=args.output_dir,
            scan_limit=args.scan_limit,
            start_offset=args.start_offset,
            per_family_limit=args.per_family_limit,
            family_filter=args.family,
            family_exclude=args.exclude_family,
            target_successes=args.target_successes,
            max_attempts=args.max_attempts,
            max_failures=args.max_failures,
            max_consecutive_failures=args.max_consecutive_failures,
            target_matches=args.target_matches,
            min_match_rate_after_attempts=match_rate_guardrails,
            dry_run=not args.execute,
            executor=executor,
            write_summary=not args.no_summary_file,
            manifest_jsonl=args.manifest_jsonl,
            accepted_index_jsonl=accepted_index_paths,
        )
    print(json.dumps(summary, indent=2, default=str))
    return 0


def _parse_methods(value: str | None) -> list[str]:
    if not value or value.lower() in {"none", "off", "false"}:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def _parse_path_list(values: list[str] | None) -> list[str]:
    paths: list[str] = []
    for value in values or []:
        paths.extend(item.strip() for item in value.split(",") if item.strip())
    return paths


def _parse_match_rate_guardrails(values: list[str] | None) -> list[MatchRateGuardrail]:
    guardrails: list[MatchRateGuardrail] = []
    for value in values or []:
        try:
            attempts_text, rate_text = value.split(":", 1)
            guardrails.append((int(attempts_text), float(rate_text)))
        except ValueError as exc:
            raise ValueError(
                "--min-match-rate-after-attempts must use ATTEMPTS:RATE, e.g. 10:0.6"
            ) from exc
    return _normalize_match_rate_guardrails(guardrails)


if __name__ == "__main__":
    raise SystemExit(main())
