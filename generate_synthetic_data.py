#!/usr/bin/env python3
"""Batch synthetic part generator for d2m Phase 1.

Generates 10,000+ parametric CAD parts with randomized features,
exports STEP files + 4-view PNG renders + JSON labels, and produces
data suitable for GNN training (Phase 2) and LLM fine-tuning (Phase 3).

Usage:
    python generate_synthetic_data.py --count 10000 --output-dir ./data/synthetic

    # Fast generation without renders:
    python generate_synthetic_data.py --count 10000 --no-render

    # Resume interrupted batch:
    python generate_synthetic_data.py --count 10000 --resume

    # Low resource mode:
    python generate_synthetic_data.py --count 100 --workers 1
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import traceback
import logging
from datetime import timedelta
from pathlib import Path
from typing import Optional

import numpy as np
from tqdm import tqdm

# Ensure project root on path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data.part_generator import generate_part, PartConfig
from src.data.label_generator import generate_labels, PartLabels
from src.data.export_pipeline import export_part

logger = logging.getLogger(__name__)


# =========================================================================
#  Check for completed parts (resume support)
# =========================================================================

def _get_existing_parts(output_dir: Path) -> set[int]:
    """Scan output_dir for completed part_NNNNN directories.

    A part is considered complete if its directory contains at minimum
    part.step, features.json, and plan.json.
    """
    existing: set[int] = set()
    if not output_dir.exists():
        return existing

    for entry in output_dir.iterdir():
        if not entry.is_dir() or not entry.name.startswith("part_"):
            continue
        try:
            idx = int(entry.name.split("_")[1])
        except (ValueError, IndexError):
            continue

        # Check for minimum required files
        step = entry / "part.step"
        features = entry / "features.json"
        plan = entry / "plan.json"
        if step.exists() and features.exists() and plan.exists():
            existing.add(idx)

    return existing


# =========================================================================
#  Multiprocessing worker
# =========================================================================

def _worker_generate_one(args: tuple) -> dict:
    """Worker process: generate a single part.

    Each worker creates its own CadQuery/OCC context in a spawned process
    to avoid cross-process OCC contamination.

    Args:
        args: (part_index, base_seed, output_dir_str, metal_ratio,
               do_render, render_method, config_dict)

    Returns:
        {"index": int, "ok": bool, "error": str or None}.
    """
    (part_index, base_seed, output_dir_str, metal_ratio,
     do_render, render_method, config_dict) = args

    output_dir = Path(output_dir_str)
    config = PartConfig(**config_dict) if config_dict else PartConfig()

    try:
        rng = np.random.default_rng(base_seed + part_index)
        shape, features_internal, meta = generate_part(rng, part_index, config)
        labels = generate_labels(features_internal, meta, rng,
                                 metal_ratio=metal_ratio, part_id=part_index)
        export_part(shape, labels, str(output_dir),
                    render=do_render, render_method=render_method)
        del shape
        return {"index": part_index, "ok": True, "error": None}
    except Exception as exc:
        err_msg = f"Part {part_index}: {exc}\n{traceback.format_exc()}"
        err_path = output_dir / "_errors.jsonl"
        with open(err_path, "a", encoding="utf-8") as f:
            json.dump({
                "part_index": part_index,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "error": str(exc),
            }, f)
            f.write("\n")
        return {"index": part_index, "ok": False, "error": str(exc)}


# =========================================================================
#  Main batch function
# =========================================================================

def generate_batch(
    count: int,
    output_dir: Path,
    seed: int = 42,
    metal_ratio: float = 0.5,
    workers: int = 1,
    resume: bool = True,
    render: bool = True,
    config: Optional[dict] = None,
) -> dict:
    """Generate a batch of synthetic parts.

    Args:
        count:     Total number of parts to generate.
        output_dir: Root output directory.
        seed:      Base random seed (each part uses seed + index).
        metal_ratio: Fraction of metal parts (0.0 - 1.0).
        workers:  Number of parallel processes.
        resume:   Skip already-completed parts.
        render:   Generate 4-view PNG renders per part.
        config:   Optional PartConfig overrides as dict.

    Returns:
        Dict with: total_generated, total_errors, elapsed_seconds,
        metal_count, plastic_count, output_dir_size_bytes.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    existing = _get_existing_parts(output_dir) if resume else set()
    to_generate = count - min(len(existing), count)

    if len(existing) > 0:
        print(f"Resuming: {len(existing)} parts already complete, {to_generate} remaining")

    if to_generate <= 0:
        print("All parts already generated.")
        return {
            "total_generated": 0,
            "total_errors": 0,
            "elapsed_seconds": 0.0,
            "metal_count": 0,
            "plastic_count": 0,
            "output_dir_size_bytes": _dir_size(output_dir),
        }

    # Build task list: only parts that need generation
    if workers > 1 and to_generate >= workers:
        import multiprocessing as mp
        mp.set_start_method("spawn", force=True)

        tasks = [
            (i, seed, str(output_dir), metal_ratio, render, "auto", config or {})
            for i in range(count)
            if i not in existing
        ]

        print(f"Starting {workers} workers for {len(tasks)} parts "
              f"({count} total, seed={seed}) ...")
        t0 = time.perf_counter()

        with mp.Pool(processes=workers) as pool:
            results = list(tqdm(
                pool.imap_unordered(_worker_generate_one, tasks),
                total=len(tasks),
                desc="Parts",
                unit="part",
            ))

        elapsed = time.perf_counter() - t0
        total_completed = sum(1 for r in results if r["ok"])
        total_errors = sum(1 for r in results if not r["ok"])

    else:
        # Single-process mode
        print(f"Generating {to_generate} parts (single-process, seed={seed}) ...")
        t0 = time.perf_counter()
        cfg = PartConfig(**(config or {}))

        total_completed = 0
        all_errors: list[str] = []

        for i in tqdm(range(count), desc="Parts", unit="part"):
            if i in existing:
                continue

            try:
                rng = np.random.default_rng(seed + i)
                shape, features_internal, meta = generate_part(rng, i, cfg)
                labels = generate_labels(features_internal, meta, rng, metal_ratio=metal_ratio, part_id=i)
                export_part(shape, labels, str(output_dir), render=render)
                del shape
                total_completed += 1
            except Exception as exc:
                err_msg = f"Part {i}: {exc}"
                all_errors.append(err_msg)
                err_path = output_dir / "_errors.jsonl"
                with open(err_path, "a", encoding="utf-8") as f:
                    json.dump({
                        "part_index": i,
                        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
                        "error": str(exc),
                    }, f)
                    f.write("\n")

        elapsed = time.perf_counter() - t0
        total_errors = len(all_errors)

    # Compute material split
    metal_count = 0
    plastic_count = 0
    for entry in output_dir.iterdir():
        if not entry.is_dir() or not entry.name.startswith("part_"):
            continue
        meta_path = entry / "metadata.json"
        if meta_path.exists():
            try:
                with open(meta_path) as f:
                    md = json.load(f)
                if md.get("is_metal"):
                    metal_count += 1
                else:
                    plastic_count += 1
            except Exception:
                pass

    return {
        "total_generated": total_completed,
        "total_errors": total_errors,
        "elapsed_seconds": elapsed,
        "metal_count": metal_count,
        "plastic_count": plastic_count,
        "output_dir_size_bytes": _dir_size(output_dir),
    }


def _dir_size(path: Path) -> int:
    """Compute total size of all files under path in bytes."""
    total = 0
    if not path.exists():
        return 0
    for f in path.rglob("*"):
        if f.is_file():
            total += f.stat().st_size
    return total


# =========================================================================
#  CLI
# =========================================================================

def main():
    parser = argparse.ArgumentParser(
        description="d2m Phase 1: Synthetic Data Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_synthetic_data.py --count 100 --no-render
  python generate_synthetic_data.py --count 10000 --workers 4
  python generate_synthetic_data.py --count 5000 --seed 123 --metal-ratio 0.6 --resume
        """,
    )

    parser.add_argument("--count", type=int, default=10000,
                        help="Total number of parts to generate (default: 10000)")
    parser.add_argument("--output-dir", type=str, default="./data/synthetic",
                        help="Output directory (default: ./data/synthetic)")
    parser.add_argument("--seed", type=int, default=42,
                        help="Base random seed (default: 42)")
    parser.add_argument("--metal-ratio", type=float, default=0.5,
                        help="Fraction of metal parts (default: 0.5)")
    parser.add_argument("--workers", type=int, default=1,
                        help="Number of parallel processes (default: 1)")
    parser.add_argument("--resume", action="store_true", default=True,
                        help="Skip already-completed parts (default)")
    parser.add_argument("--no-resume", action="store_false", dest="resume",
                        help="Overwrite existing parts")
    parser.add_argument("--no-render", action="store_false", dest="render",
                        help="Skip 4-view render generation (faster)")
    parser.set_defaults(render=True, resume=True)

    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    print(f"d2m Phase 1: Synthetic Data Generator")
    print(f"  Target count:  {args.count}")
    print(f"  Output dir:    {output_dir.absolute()}")
    print(f"  Seed:          {args.seed}")
    print(f"  Metal ratio:   {args.metal_ratio:.0%}")
    print(f"  Workers:       {args.workers}")
    print(f"  Render:        {args.render}")
    print(f"  Resume:        {args.resume}")
    print()

    t_start = time.perf_counter()

    result = generate_batch(
        count=args.count,
        output_dir=output_dir,
        seed=args.seed,
        metal_ratio=args.metal_ratio,
        workers=args.workers,
        resume=args.resume,
        render=args.render,
    )

    t_total = time.perf_counter() - t_start

    # Summary
    print()
    print("=" * 60)
    print("Generation Complete")
    print("=" * 60)
    print(f"  Generated:     {result['total_generated']}")
    print(f"  Errors:        {result['total_errors']}")
    print(f"  Metals:        {result['metal_count']}")
    print(f"  Plastics:      {result['plastic_count']}")
    print(f"  Elapsed:       {timedelta(seconds=int(t_total))}")
    if result["total_generated"] > 0:
        rate = result["total_generated"] / max(t_total, 0.1)
        print(f"  Rate:          {rate:.1f} parts/min")
    size_mb = result["output_dir_size_bytes"] / (1024 * 1024)
    print(f"  Output size:   {size_mb:.1f} MB")
    print()

    if result["total_errors"] > 0:
        print(f"  Errors logged to: {output_dir / '_errors.jsonl'}")
        sys.exit(1)
    else:
        print("  All parts generated successfully.")


if __name__ == "__main__":
    main()
