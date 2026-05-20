"""Verify generated SubCAD pair datasets.

The verifier re-executes every saved ``subcad_program.py`` and compares the
fresh output STEP against the saved ``model.step``.  This checks that dataset
pairs are reproducible, not just that files exist.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def verify_dataset(
    input_dir: str,
    *,
    limit: int | None = None,
    exact_volume_tolerance: float = 1e-6,
    output: str | None = None,
) -> dict[str, Any]:
    from src.data.subcad_repl import compare_to_reference, run_subcad

    root = Path(input_dir)
    samples = [
        path for path in sorted(root.glob("shard_*/sample_*"))
        if path.is_dir() and not path.name.endswith(".tmp")
    ]
    if limit is not None:
        samples = samples[:limit]

    t0 = time.perf_counter()
    passed = 0
    failed: list[dict[str, Any]] = []
    ratios: list[float] = []

    for sample in samples:
        code_path = sample / "subcad_program.py"
        step_path = sample / "model.step"
        if not code_path.exists() or not step_path.exists():
            failed.append({"sample": str(sample), "error": "missing required files"})
            continue

        result = run_subcad(code_path.read_text(encoding="utf-8"))
        if not result.get("success"):
            failed.append({
                "sample": str(sample),
                "error": str(result.get("error", "execution failed"))[:1000],
            })
            continue

        comparison = compare_to_reference(result.get("step_path"), str(step_path))
        ratio = float(comparison.get("volume_ratio", 0.0))
        ratios.append(ratio)
        if comparison.get("match") and abs(ratio - 1.0) <= exact_volume_tolerance:
            passed += 1
        else:
            failed.append({
                "sample": str(sample),
                "error": "volume mismatch",
                "comparison": comparison,
            })
        _cleanup_temp(result)

    elapsed = time.perf_counter() - t0
    report = {
        "input_dir": str(root),
        "samples_checked": len(samples),
        "passed_exact_volume": passed,
        "failed": len(failed),
        "ratio_min": min(ratios) if ratios else None,
        "ratio_max": max(ratios) if ratios else None,
        "elapsed_seconds": elapsed,
        "samples_per_minute": round(len(samples) / max(elapsed, 0.1) * 60.0, 2),
        "failures": failed[:50],
    }
    if output:
        Path(output).write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify SubCAD generated pair datasets.")
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--output", default=None)
    parser.add_argument("--exact-volume-tolerance", type=float, default=1e-6)
    args = parser.parse_args(argv)

    report = verify_dataset(
        args.input_dir,
        limit=args.limit,
        exact_volume_tolerance=args.exact_volume_tolerance,
        output=args.output,
    )
    print(json.dumps(report, indent=2, default=str))
    return 0 if report["failed"] == 0 else 1


def _cleanup_temp(result: dict[str, Any]) -> None:
    for key in ("step_path", "stl_path"):
        path = result.get(key)
        if path and os.path.exists(path):
            try:
                os.unlink(path)
            except OSError:
                pass


if __name__ == "__main__":
    raise SystemExit(main())
