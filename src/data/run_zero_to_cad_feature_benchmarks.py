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


DEFAULT_SOURCE_DIR = "data/zero_to_cad_100k"
DEFAULT_OUTPUT_DIR = "runs/zero_to_cad_feature_benchmarks"
UNSUPPORTED_FAMILY = "__unsupported__"
ALL_SPLITS = ("train", "val", "test")

RowExecutor = Callable[[dict[str, Any], dict[str, Any]], dict[str, Any]]


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
    target_successes: int = 100000
    scanned: int = 0
    plannable: int = 0
    selected: int = 0
    filtered_out: int = 0
    attempted: int = 0
    executed: int = 0
    matched: int = 0
    failed: int = 0
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
    target_successes: int = 100000,
    dry_run: bool = True,
    executor: RowExecutor | None = None,
    write_summary: bool = True,
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

    stats = BenchmarkStats(
        source_dir=source_dir,
        split=split,
        output_dir=str(root),
        dry_run=dry_run,
        scan_limit=scan_limit,
        per_family_limit=per_family_limit,
        family_filter=sorted(_normalize_family_filter(family_filter)),
        target_successes=target_successes,
    )
    family_stats: dict[str, FamilyStats] = {}
    attempts_by_family: Counter[str] = Counter()
    started = time.perf_counter()
    requested_families = set(stats.family_filter)

    for row in iter_zero_to_cad_rows(source_dir, split, start_offset=start_offset, limit=scan_limit):
        stats.scanned += 1
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
            for family in selected_families:
                family_stats[family].failed += 1

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
    target_successes: int = 100000,
    dry_run: bool = True,
    executor: RowExecutor | None = None,
    write_summary: bool = True,
) -> dict[str, Any]:
    """Run split-level scans and return one aggregate summary."""
    root = Path(output_dir)
    if write_summary:
        root.mkdir(parents=True, exist_ok=True)

    split_summaries = []
    for split in splits:
        split_summary = run_feature_family_benchmark(
            source_dir=source_dir,
            split=split,
            output_dir=str(root / split),
            scan_limit=scan_limit,
            start_offset=start_offset,
            per_family_limit=per_family_limit,
            family_filter=family_filter,
            target_successes=target_successes,
            dry_run=dry_run,
            executor=executor,
            write_summary=write_summary,
        )
        split_summaries.append(split_summary)

    aggregate = _aggregate_split_summaries(
        split_summaries,
        source_dir=source_dir,
        output_dir=str(root),
        family_filter=family_filter,
        target_successes=target_successes,
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


def _append_example(bucket: FamilyStats, row_summary: dict[str, Any], limit: int = 5) -> None:
    if len(bucket.examples) < limit:
        bucket.examples.append(row_summary)


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
    target_successes: int,
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
        "target_successes": target_successes,
        **totals,
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
    parser.add_argument("--target-successes", type=int, default=100000)
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
        "--execute",
        action="store_true",
        help="Attempt selected rows. Requires --executor translator for live AI runs.",
    )
    parser.add_argument("--no-summary-file", action="store_true")
    args = parser.parse_args(argv)
    comparison_methods = _parse_methods(args.comparison_methods)
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
        )

    if args.split == "all":
        summary = run_feature_family_benchmark_splits(
            source_dir=args.source_dir,
            output_dir=args.output_dir,
            scan_limit=args.scan_limit,
            start_offset=args.start_offset,
            per_family_limit=args.per_family_limit,
            family_filter=args.family,
            target_successes=args.target_successes,
            dry_run=not args.execute,
            executor=executor,
            write_summary=not args.no_summary_file,
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
            target_successes=args.target_successes,
            dry_run=not args.execute,
            executor=executor,
            write_summary=not args.no_summary_file,
        )
    print(json.dumps(summary, indent=2, default=str))
    return 0


def _parse_methods(value: str | None) -> list[str]:
    if not value or value.lower() in {"none", "off", "false"}:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


if __name__ == "__main__":
    raise SystemExit(main())
