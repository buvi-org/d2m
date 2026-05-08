#!/usr/bin/env python3
"""Convert synthetic part labels to LLM instruction fine-tuning format (JSONL).

Reads part_NNNNN/features.json + plan.json from each subdirectory and
writes a single JSONL file with {"messages": [...]} format suitable for
DeepSeek fine-tuning API, Llama chat templates, and similar instruction-
tuned models.

Uses the existing src/planner/dataset.py batch_convert() for the core
conversion logic.

Usage:
    python convert_dataset.py --input-dir data/synthetic --output data/train.jsonl
    python convert_dataset.py --input-dir data/synthetic --output data/train.jsonl --val-split 0.1
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import random
from pathlib import Path
from typing import Optional

# Ensure project root on path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.planner.dataset import batch_convert


# =========================================================================
#  Helpers
# =========================================================================

def _discover_parts(input_dir: Path) -> list[Path]:
    """Discover all valid part directories under input_dir.

    A valid part dir has both features.json and plan.json.
    """
    parts: list[Path] = []
    if not input_dir.exists():
        return parts

    for entry in sorted(input_dir.iterdir()):
        if not entry.is_dir() or not entry.name.startswith("part_"):
            continue
        features = entry / "features.json"
        plan = entry / "plan.json"
        if features.exists() and plan.exists():
            parts.append(entry)

    return parts


def _split_train_val(
    parts: list[Path],
    val_split: float,
    seed: int = 42,
) -> tuple[list[Path], list[Path]]:
    """Shuffle and split parts into train and validation sets."""
    rng = random.Random(seed)
    shuffled = list(parts)
    rng.shuffle(shuffled)

    val_count = max(1, int(len(shuffled) * val_split))
    val = shuffled[:val_count]
    train = shuffled[val_count:]
    return train, val


def _write_jsonl(parts: list[Path], output_path: str) -> int:
    """Convert part dirs to JSONL and write to output_path.

    Creates a temp directory with just the selected parts and runs
    batch_convert against it.

    Returns number of samples written.
    """
    import tempfile
    import shutil

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)

        # Symlink/copy part dirs into temp dir
        for i, part_dir in enumerate(parts):
            dst = tmp / f"part_{i:05d}"
            # Copy features.json and plan.json
            os.makedirs(dst, exist_ok=True)
            shutil.copy2(part_dir / "features.json", dst / "features.json")
            shutil.copy2(part_dir / "plan.json", dst / "plan.json")

        # Run batch_convert
        output_file = batch_convert(str(tmp), output_path)
        if output_file is None:
            raise RuntimeError("batch_convert returned None")

    # Count lines
    count = 0
    with open(output_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                count += 1
    return count


# =========================================================================
#  Main
# =========================================================================

def main():
    parser = argparse.ArgumentParser(
        description="d2m Phase 1: Convert synthetic data to LLM fine-tuning format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python convert_dataset.py --input-dir data/synthetic --output data/train.jsonl
  python convert_dataset.py --input-dir data/synthetic --output data/train.jsonl --val-split 0.1
  python convert_dataset.py --input-dir data/synthetic --output data/train.jsonl --val-split 0.1 --val-output data/val.jsonl
        """,
    )

    parser.add_argument("--input-dir", type=str, required=True,
                        help="Directory containing part_NNNNN/ subdirectories")
    parser.add_argument("--output", type=str, required=True,
                        help="Output JSONL file path for training data")
    parser.add_argument("--val-split", type=float, default=0.0,
                        help="Fraction of data for validation (default: 0.0 = no split)")
    parser.add_argument("--val-output", type=str, default=None,
                        help="Output JSONL file path for validation data (default: derived from --output)")
    parser.add_argument("--seed", type=int, default=42,
                        help="Shuffle seed for train/val split (default: 42)")

    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_path = args.output

    print("d2m Dataset Converter")
    print(f"  Input dir:   {input_dir.absolute()}")
    print(f"  Output:      {output_path}")

    # Discover parts
    parts = _discover_parts(input_dir)
    print(f"  Parts found: {len(parts)}")

    if len(parts) == 0:
        print("ERROR: No valid part directories found.")
        sys.exit(1)

    # Handle train/val split
    if args.val_split > 0:
        train_parts, val_parts = _split_train_val(parts, args.val_split, args.seed)

        val_output = args.val_output
        if val_output is None:
            base, ext = os.path.splitext(output_path)
            val_output = f"{base}_val{ext}"

        print(f"  Train:       {len(train_parts)} samples")
        print(f"  Val:         {len(val_parts)} samples")
        print(f"  Val output:  {val_output}")
        print()

        train_count = _write_jsonl(train_parts, output_path)
        val_count = _write_jsonl(val_parts, val_output)

        print(f"  Train written: {train_count} samples -> {output_path}")
        print(f"  Val written:   {val_count} samples -> {val_output}")

        # Verify format
        _verify_jsonl(output_path, train_count)
        _verify_jsonl(val_output, val_count)

    else:
        print()
        sample_count = _write_jsonl(parts, output_path)
        print(f"  Written: {sample_count} samples -> {output_path}")

        # Verify format
        _verify_jsonl(output_path, sample_count)

    print()
    print("Conversion complete.")


def _verify_jsonl(path: str, expected: int):
    """Verify JSONL file has the right structure."""
    if not os.path.exists(path):
        print(f"  WARNING: Output file missing: {path}")
        return

    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
                msgs = record.get("messages", [])
                if len(msgs) < 2:
                    print(f"  WARNING: Line {i} has only {len(msgs)} messages")
                roles = [m.get("role") for m in msgs]
                if "user" not in roles:
                    print(f"  WARNING: Line {i} missing user message")
                if "assistant" not in roles:
                    print(f"  WARNING: Line {i} missing assistant message")
            except json.JSONDecodeError as e:
                print(f"  WARNING: Line {i} invalid JSON: {e}")
                break

    # Check total records
    with open(path, "r", encoding="utf-8") as f:
        actual = sum(1 for line in f if line.strip())
    if actual != expected:
        print(f"  WARNING: Expected {expected} records, got {actual}")

    print(f"  Verified: {actual} valid JSONL records")


if __name__ == "__main__":
    main()
