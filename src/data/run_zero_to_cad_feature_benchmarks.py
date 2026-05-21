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
    scanned: int = 0
    plannable: int = 0
    attempted: int = 0
    executed: int = 0
    matched: int = 0
    failed: int = 0
    unsupported: int = 0
    elapsed_seconds: float = 0.0

    @property
    def match_rate(self) -> float:
        return round(self.matched / self.executed, 4) if self.executed else 0.0


def run_feature_family_benchmark(
    *,
    source_dir: str = DEFAULT_SOURCE_DIR,
    split: str = "train",
    output_dir: str = DEFAULT_OUTPUT_DIR,
    scan_limit: int | None = None,
    start_offset: int = 0,
    per_family_limit: int | None = None,
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
    )
    family_stats: dict[str, FamilyStats] = {}
    attempts_by_family: Counter[str] = Counter()
    started = time.perf_counter()

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
        for family in families:
            bucket = family_stats.setdefault(family, FamilyStats(family=family))
            bucket.plannable += 1
            for status, count in statuses.items():
                bucket.statuses[status] = bucket.statuses.get(status, 0) + count
            _append_example(bucket, row_summary)

        if dry_run:
            continue
        if per_family_limit is not None and any(
            attempts_by_family[family] >= per_family_limit for family in families
        ):
            continue

        stats.attempted += 1
        for family in families:
            attempts_by_family[family] += 1
            family_stats[family].attempted += 1

        context = {
            "families": families,
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
            for family in families:
                family_stats[family].executed += 1
        if matched:
            stats.matched += 1
            for family in families:
                family_stats[family].matched += 1
        if failed:
            stats.failed += 1
            for family in families:
                family_stats[family].failed += 1

    stats.elapsed_seconds = time.perf_counter() - started
    summary = {
        "schema": "zero_to_cad_feature_family_benchmark.v1",
        **asdict(stats),
        "match_rate": stats.match_rate,
        "families": {
            family: asdict(bucket)
            for family, bucket in sorted(family_stats.items())
        },
    }
    if write_summary:
        _write_json(root / "feature_family_summary.json", summary)
    return summary


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


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Scan Zero-to-CAD rows by pure planner feature family.",
    )
    parser.add_argument("--source-dir", default=DEFAULT_SOURCE_DIR)
    parser.add_argument("--split", default="train", choices=["train", "val", "test"])
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--scan-limit", type=int, default=None)
    parser.add_argument("--start-offset", type=int, default=0)
    parser.add_argument("--per-family-limit", type=int, default=None)
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Attempt selected rows. The current default executor is a disabled placeholder.",
    )
    parser.add_argument("--no-summary-file", action="store_true")
    args = parser.parse_args(argv)

    summary = run_feature_family_benchmark(
        source_dir=args.source_dir,
        split=args.split,
        output_dir=args.output_dir,
        scan_limit=args.scan_limit,
        start_offset=args.start_offset,
        per_family_limit=args.per_family_limit,
        dry_run=not args.execute,
        write_summary=not args.no_summary_file,
    )
    print(json.dumps(summary, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
