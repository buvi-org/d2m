"""Run live Zero-to-CAD -> SubCAD translation trials.

This is the corrected benchmark flow:

    original Zero-to-CAD cadquery_file + ops_trace + model.step
    -> agentic LLM translator generates SubCAD
    -> execute generated SubCAD
    -> compare generated STEP against the original model.step

Self-generated SubCAD pairs are not used here and do not count as translator
success.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import traceback
from collections import Counter
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from .agentic_translator import AgenticTranslator, _load_local_env_if_present
from .pure_subcad_planner import compatibility_report as pure_subcad_compatibility_report


DEFAULT_SOURCE_DIR = "data/zero_to_cad_100k"
DEFAULT_OUTPUT_DIR = "runs/zero_to_cad_translations"


@dataclass
class BatchStats:
    source_dir: str
    split: str
    output_dir: str
    target_successes: int
    attempted: int = 0
    succeeded: int = 0
    failed: int = 0
    api_errors: int = 0
    skipped_existing: int = 0
    skipped_incompatible: int = 0
    elapsed_seconds: float = 0.0
    stopped_reason: str = ""

    @property
    def pass_rate(self) -> float:
        return round(self.succeeded / self.attempted, 4) if self.attempted else 0.0


def run_batch(
    *,
    source_dir: str = DEFAULT_SOURCE_DIR,
    split: str = "train",
    output_dir: str = DEFAULT_OUTPUT_DIR,
    target_successes: int = 100_000,
    max_attempts: int | None = None,
    start_offset: int = 0,
    provider: str = "deepseek",
    model: str | None = None,
    api_timeout_s: float = 120.0,
    tolerance: float = 0.05,
    safety_cap: int = 5,
    stagnation_limit: int = 2,
    divergence_limit: int = 2,
    comparison_methods: list[str] | None = None,
    feature_aware: bool = False,
    compatible_only: bool = True,
    trusted_tolerance_mm: float = 0.25,
    min_mesh_score: float = 95.0,
    volume_only_success: bool = False,
    max_api_errors: int = 3,
    pilot_attempts: int = 10,
    min_pilot_pass_rate: float = 0.1,
    resume: bool = True,
    dry_run: bool = False,
    translation_mode: str = "planner_guided",
) -> dict[str, Any]:
    _load_local_env_if_present()
    _require_provider_key(provider)

    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    stats = BatchStats(
        source_dir=source_dir,
        split=split,
        output_dir=str(root),
        target_successes=target_successes,
    )

    if dry_run:
        samples = []
        for row in iter_zero_to_cad_rows(source_dir, split, start_offset=start_offset):
            compatible = compatibility_report(row["ops_trace"], row["cadquery_code"])
            if compatible_only and not compatible["compatible"]:
                continue
            row["compatibility"] = compatible
            samples.append(row)
            if len(samples) >= 3:
                break
        return {
            **asdict(stats),
            "dry_run": True,
            "preview_count": len(samples),
            "preview": [
                {
                    "global_index": row["global_index"],
                    "uuid": row["uuid"],
                    "cadquery_chars": len(row["cadquery_code"]),
                    "ops_trace_count": len(row["ops_trace"]) if isinstance(row["ops_trace"], list) else 0,
                    "step_bytes": len(row["step_bytes"]),
                    "compatibility": row["compatibility"],
                }
                for row in samples
            ],
        }

    translator = AgenticTranslator(
        provider=provider,
        model=model,
        api_timeout_s=api_timeout_s,
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
        translation_mode=translation_mode,
    )

    started = time.perf_counter()
    consecutive_api_errors = 0
    attempted_limit = max_attempts if max_attempts is not None else target_successes * 3

    for row in iter_zero_to_cad_rows(source_dir, split, start_offset=start_offset):
        compatible = compatibility_report(row["ops_trace"], row["cadquery_code"])
        row["compatibility"] = compatible
        if compatible_only and not compatible["compatible"]:
            stats.skipped_incompatible += 1
            if stats.skipped_incompatible % 1000 == 0:
                _write_summary(root, stats, started)
            continue

        if stats.succeeded >= target_successes:
            stats.stopped_reason = "target_successes_reached"
            break
        if stats.attempted >= attempted_limit:
            stats.stopped_reason = "max_attempts_reached"
            break

        sample_dir = _sample_output_dir(root, row["global_index"], row["uuid"])
        result_path = sample_dir / "result.json"
        if resume and _is_success_record(result_path):
            stats.skipped_existing += 1
            stats.succeeded += 1
            continue
        if resume and result_path.exists():
            stats.skipped_existing += 1
            continue

        sample_dir.mkdir(parents=True, exist_ok=True)
        _write_source_artifacts(sample_dir, row)
        stats.attempted += 1

        print(
            f"\n[{stats.attempted}] Zero-to-CAD {row['global_index']} "
            f"{row['uuid'][:12]}..."
        )

        try:
            result = _translate_row(translator, row, sample_dir)
            result = _apply_match_policy(
                result,
                comparison_methods=comparison_methods,
                trusted_tolerance_mm=trusted_tolerance_mm,
                min_mesh_score=min_mesh_score,
                volume_only_success=volume_only_success,
            )
            _save_result(sample_dir, row, result, provider, model)
        except Exception as exc:
            result = {
                "success": False,
                "error": str(exc),
                "stop_reason": "runner_exception",
                "traceback": traceback.format_exc(),
            }
            _save_result(sample_dir, row, result, provider, model)

        if _is_api_error(result):
            stats.api_errors += 1
            consecutive_api_errors += 1
        else:
            consecutive_api_errors = 0

        if result.get("success"):
            stats.succeeded += 1
        else:
            stats.failed += 1

        _write_summary(root, stats, started)

        if consecutive_api_errors >= max_api_errors:
            stats.stopped_reason = "max_consecutive_api_errors"
            break

        if (
            pilot_attempts > 0
            and stats.attempted >= pilot_attempts
            and stats.succeeded / max(stats.attempted, 1) < min_pilot_pass_rate
        ):
            stats.stopped_reason = "pilot_pass_rate_too_low"
            break

    else:
        stats.stopped_reason = "source_exhausted"

    return _write_summary(root, stats, started)


def iter_zero_to_cad_rows(
    source_dir: str,
    split: str,
    *,
    start_offset: int = 0,
    limit: int | None = None,
) -> Iterable[dict[str, Any]]:
    import pyarrow.parquet as pq

    parquet_dir = Path(source_dir) / "data" / split
    if not parquet_dir.exists():
        raise FileNotFoundError(f"Missing parquet directory: {parquet_dir}")

    yielded = 0
    global_index = 0
    columns = ["uuid", "cadquery_file", "cadquery_ops_json", "step_file"]
    for parquet_path in sorted(parquet_dir.glob("*.parquet")):
        table = pq.read_table(parquet_path, columns=columns)
        rows = table.to_pydict()
        for row_index in range(table.num_rows):
            if global_index < start_offset:
                global_index += 1
                continue
            if limit is not None and yielded >= limit:
                return

            cq_code = rows["cadquery_file"][row_index]
            if isinstance(cq_code, bytes):
                cq_code = cq_code.decode("utf-8", errors="replace")

            ops_json = rows["cadquery_ops_json"][row_index]
            if isinstance(ops_json, bytes):
                ops_json = ops_json.decode("utf-8", errors="replace")
            try:
                ops_trace = json.loads(ops_json)
            except Exception:
                ops_trace = []

            step_bytes = rows["step_file"][row_index]
            if step_bytes is None or len(step_bytes) == 0:
                global_index += 1
                continue

            yield {
                "global_index": global_index,
                "uuid": str(rows["uuid"][row_index]),
                "cadquery_code": cq_code,
                "ops_trace": ops_trace,
                "step_bytes": step_bytes,
                "parquet_file": str(parquet_path),
                "row_index": row_index,
            }
            yielded += 1
            global_index += 1


def scan_compatibility(
    source_dir: str = DEFAULT_SOURCE_DIR,
    splits: list[str] | None = None,
) -> dict[str, Any]:
    """Count rows currently eligible for exact SubCAD translation trials."""
    split_names = splits or ["train", "val", "test"]
    totals = Counter()
    by_split: dict[str, dict[str, Any]] = {}
    for split in split_names:
        counts = Counter()
        examples = []
        for row in iter_zero_to_cad_rows(source_dir, split):
            report = compatibility_report(row["ops_trace"], row["cadquery_code"])
            counts["total"] += 1
            if report["compatible"]:
                counts["compatible"] += 1
                if len(examples) < 5:
                    examples.append({
                        "global_index": row["global_index"],
                        "uuid": row["uuid"],
                        "cadquery_chars": len(row["cadquery_code"]),
                        "ops_trace_count": len(row["ops_trace"]) if isinstance(row["ops_trace"], list) else 0,
                    })
            else:
                for reason in report["reasons"]:
                    counts[reason] += 1
        totals.update(counts)
        by_split[split] = {
            "counts": dict(counts),
            "examples": examples,
        }
    return {
        "source_dir": source_dir,
        "splits": split_names,
        "total": dict(totals),
        "by_split": by_split,
    }


def compatibility_report(ops_trace: list[dict], cadquery_code: str = "") -> dict[str, Any]:
    """Pure-operation compatibility gate for current SubCAD translation."""
    return pure_subcad_compatibility_report(ops_trace, cadquery_code)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run live Zero-to-CAD -> SubCAD translation trials.",
    )
    parser.add_argument("--source-dir", default=DEFAULT_SOURCE_DIR)
    parser.add_argument("--split", default="train", choices=["train", "val", "test"])
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--target-successes", type=int, default=100_000)
    parser.add_argument("--max-attempts", type=int, default=None)
    parser.add_argument("--start-offset", type=int, default=0)
    parser.add_argument("--provider", default="deepseek")
    parser.add_argument("--model", default=None)
    parser.add_argument("--api-timeout-s", type=float, default=120.0)
    parser.add_argument("--tolerance", type=float, default=0.05)
    parser.add_argument("--safety-cap", type=int, default=5)
    parser.add_argument("--stagnation-limit", type=int, default=2)
    parser.add_argument("--divergence-limit", type=int, default=2)
    parser.add_argument("--comparison-methods", default="sdf,slice")
    parser.add_argument("--feature-aware", action="store_true")
    parser.add_argument("--allow-unsupported", action="store_true")
    parser.add_argument("--scan-compatible", action="store_true")
    parser.add_argument("--trusted-tolerance-mm", type=float, default=0.25)
    parser.add_argument("--min-mesh-score", type=float, default=95.0)
    parser.add_argument(
        "--volume-only-success",
        action="store_true",
        help="Debug mode only: count volume-ratio matches as successes even without mesh/slice trust checks.",
    )
    parser.add_argument(
        "--translation-mode",
        default="planner_guided",
        choices=["planner_guided", "ai_heavy"],
        help="planner_guided uses deterministic/planner-first behavior; ai_heavy skips deterministic builders and lets the LLM infer pure SubCAD operations from evidence.",
    )
    parser.add_argument("--max-api-errors", type=int, default=3)
    parser.add_argument("--pilot-attempts", type=int, default=10)
    parser.add_argument("--min-pilot-pass-rate", type=float, default=0.1)
    parser.add_argument("--no-resume", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    if args.scan_compatible:
        summary = scan_compatibility(args.source_dir, [args.split])
        print(json.dumps(summary, indent=2, default=str))
        return 0

    comparison_methods = _parse_methods(args.comparison_methods)
    summary = run_batch(
        source_dir=args.source_dir,
        split=args.split,
        output_dir=args.output_dir,
        target_successes=args.target_successes,
        max_attempts=args.max_attempts,
        start_offset=args.start_offset,
        provider=args.provider,
        model=args.model,
        api_timeout_s=args.api_timeout_s,
        tolerance=args.tolerance,
        safety_cap=args.safety_cap,
        stagnation_limit=args.stagnation_limit,
        divergence_limit=args.divergence_limit,
        comparison_methods=comparison_methods,
        feature_aware=args.feature_aware,
        compatible_only=not args.allow_unsupported,
        trusted_tolerance_mm=args.trusted_tolerance_mm,
        min_mesh_score=args.min_mesh_score,
        volume_only_success=args.volume_only_success,
        max_api_errors=args.max_api_errors,
        pilot_attempts=args.pilot_attempts,
        min_pilot_pass_rate=args.min_pilot_pass_rate,
        resume=not args.no_resume,
        dry_run=args.dry_run,
        translation_mode=args.translation_mode,
    )
    print(json.dumps(summary, indent=2, default=str))
    return 0 if summary.get("failed", 0) == 0 and summary.get("api_errors", 0) == 0 else 1


def _translate_row(
    translator: AgenticTranslator,
    row: dict[str, Any],
    sample_dir: Path,
) -> dict[str, Any]:
    step_path = sample_dir / "original_model.step"
    sample = {
        "cadquery_file": row["cadquery_code"],
        "cadquery_ops_json": json.dumps(row["ops_trace"]),
        "uuid": row["uuid"],
    }
    result = translator.translate(sample, step_path=str(step_path))

    generated = result.get("subcad_code")
    if generated:
        (sample_dir / "generated_subcad.py").write_text(generated, encoding="utf-8")

    exec_result = result.get("exec_result") or {}
    part = exec_result.get("part")
    if part is not None:
        try:
            _write_json(sample_dir / "process_plan.json", part.process_plan())
        except Exception:
            pass
        try:
            _write_json(sample_dir / "validation.json", part.validate_shop_floor(structured=True))
        except Exception:
            pass
        try:
            _write_json(sample_dir / "economics.json", part.estimate_cost(quantity=1))
        except Exception:
            pass

    return result


def _write_source_artifacts(sample_dir: Path, row: dict[str, Any]) -> None:
    (sample_dir / "cadquery_code.py").write_text(row["cadquery_code"], encoding="utf-8")
    _write_json(sample_dir / "ops_trace.json", row["ops_trace"])
    (sample_dir / "original_model.step").write_bytes(row["step_bytes"])
    _write_json(sample_dir / "source_metadata.json", {
        "uuid": row["uuid"],
        "global_index": row["global_index"],
        "parquet_file": row["parquet_file"],
        "row_index": row["row_index"],
        "benchmark_target": "original_model.step",
        "compatibility": row.get("compatibility"),
    })


def _save_result(
    sample_dir: Path,
    row: dict[str, Any],
    result: dict[str, Any],
    provider: str,
    model: str | None,
) -> None:
    payload = {
        "schema": "zero_to_cad_subcad_translation.v1",
        "uuid": row["uuid"],
        "global_index": row["global_index"],
        "provider": provider,
        "model": model,
        "success": bool(result.get("success")),
        "translator_success": bool(result.get("translator_success", result.get("success"))),
        "trusted_match": result.get("trusted_match"),
        "match_policy": result.get("match_policy"),
        "attempts": result.get("attempts", 0),
        "stop_reason": result.get("stop_reason"),
        "error": result.get("error"),
        "comparison": result.get("comparison"),
        "mesh_comparison": result.get("mesh_comparison"),
        "feature_comparison": result.get("feature_comparison"),
        "subcad_code": result.get("subcad_code"),
        "history": result.get("history", []),
        "benchmark_target": "original_model.step",
        "compatibility": row.get("compatibility"),
    }
    _write_json(sample_dir / "result.json", _json_safe(payload))


def _write_summary(root: Path, stats: BatchStats, started: float) -> dict[str, Any]:
    stats.elapsed_seconds = time.perf_counter() - started
    payload = asdict(stats)
    payload["pass_rate"] = stats.pass_rate
    payload["samples_per_minute"] = round(
        stats.attempted / max(stats.elapsed_seconds, 0.1) * 60.0,
        2,
    )
    _write_json(root / "summary.json", payload)
    return payload


def _sample_output_dir(root: Path, global_index: int, uuid: str) -> Path:
    shard = global_index // 1000
    safe_uuid = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in uuid)
    return root / f"shard_{shard:04d}" / f"{global_index:06d}_{safe_uuid[:16]}"


def _is_success_record(path: Path) -> bool:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return False
    return bool(data.get("success"))


def _require_provider_key(provider: str) -> None:
    env_by_provider = {
        "deepseek": "DEEPSEEK_API_KEY",
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
    }
    env_name = env_by_provider.get(provider.lower())
    if env_name and not os.environ.get(env_name):
        raise RuntimeError(f"{env_name} is not set; add it to env or .env before live runs.")


def _is_api_error(result: dict[str, Any]) -> bool:
    text = f"{result.get('stop_reason') or ''} {result.get('error') or ''}".lower()
    return "api" in text or "rate limit" in text or "unauthorized" in text or "authentication" in text


def _apply_match_policy(
    result: dict[str, Any],
    *,
    comparison_methods: list[str] | None,
    trusted_tolerance_mm: float,
    min_mesh_score: float,
    volume_only_success: bool,
) -> dict[str, Any]:
    """Count only original-STEP geometry matches as batch successes.

    The translator itself currently converges on relative volume. That is useful
    for prompt iteration but not enough for a Zero-to-CAD benchmark sample. This
    wrapper preserves the raw translator result while making the batch success
    flag mean "trusted enough to keep as a matched pair".
    """
    result = dict(result)
    translator_success = bool(result.get("success"))
    comparison = result.get("comparison") or {}
    mesh_comparison = result.get("mesh_comparison") or {}
    volume_match = bool(comparison.get("match"))
    policy = {
        "target": "original_model.step",
        "volume_match": volume_match,
        "requires_mesh_comparison": not volume_only_success,
        "trusted_tolerance_mm": float(trusted_tolerance_mm),
        "min_mesh_score": float(min_mesh_score),
        "comparison_methods": comparison_methods,
    }

    trusted = False
    status = "volume_mismatch"
    if volume_only_success:
        trusted = volume_match
        status = "volume_only_pass" if trusted else "volume_only_fail"
    elif not volume_match:
        trusted = False
    elif not comparison_methods:
        status = "mesh_comparison_not_run"
    elif mesh_comparison.get("error"):
        status = "mesh_comparison_error"
        policy["mesh_error"] = mesh_comparison.get("error")
    else:
        score = float(mesh_comparison.get("score", 0.0) or 0.0)
        sdf = mesh_comparison.get("sdf") or {}
        rms = float(sdf.get("rms_error", 0.0) or 0.0)
        max_overcut = abs(float(sdf.get("max_overcut", 0.0) or 0.0))
        max_undercut = abs(float(sdf.get("max_undercut", 0.0) or 0.0))
        max_deviation = max(rms, max_overcut, max_undercut)
        slice_result = mesh_comparison.get("slice") or {}
        problem_slices = slice_result.get("problem_slices") or []
        policy.update({
            "mesh_score": score,
            "rms_error_mm": rms,
            "max_overcut_mm": max_overcut,
            "max_undercut_mm": max_undercut,
            "problem_slice_count": len(problem_slices),
        })
        trusted = (
            score >= min_mesh_score
            and max_deviation <= trusted_tolerance_mm
            and not problem_slices
        )
        status = "trusted_pass" if trusted else "trusted_fail"

    policy["status"] = status
    result["translator_success"] = translator_success
    result["trusted_match"] = trusted
    result["success"] = trusted
    result["match_policy"] = policy
    if translator_success and not trusted:
        result["stop_reason"] = "trusted_match_failed"
    return result


def _parse_methods(raw: str) -> list[str] | None:
    if raw.strip().lower() in {"", "none", "off", "false"}:
        return []
    return [item.strip() for item in raw.split(",") if item.strip()]


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")


def _json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _json_safe(item) for key, item in value.items() if key != "part"}
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    if isinstance(value, tuple):
        return [_json_safe(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


if __name__ == "__main__":
    raise SystemExit(main())
