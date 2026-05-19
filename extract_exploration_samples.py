"""Extract exploration samples from Zero-To-CAD-100k parquet files.

Creates data/zero_to_cad_exploration/sample_N directories each containing:
    cadquery_code.py   - Original CadQuery source code
    ops_trace.json     - Operations trace (JSON)
    model.step         - Reference STEP file

Usage:
    python extract_exploration_samples.py                    # 5 samples from train
    python extract_exploration_samples.py --split val        # from validation
    python extract_exploration_samples.py --n 20             # 20 samples
    python extract_exploration_samples.py --split train --n 3  # 3 from train
"""

import argparse
import json
import os
import sys
from pathlib import Path

# Ensure the working directory is project root
os.chdir(Path(__file__).resolve().parent)


def extract_samples(
    source_dir: str = "data/zero_to_cad_100k",
    output_dir: str = "data/zero_to_cad_exploration",
    split: str = "train",
    n: int = 5,
    start_idx: int = 0,
    seed: int = 42,
) -> list[dict]:
    """Extract N samples from the parquet dataset into exploration directories.

    Args:
        source_dir: Path to the downloaded Zero-To-CAD-100k dataset.
        output_dir: Where to create the sample directories.
        split: Which split to pull from ("train", "val", "test").
        n: Number of samples to extract.
        start_idx: Starting file index (0-based).
        seed: Random seed for reproducibility.

    Returns:
        List of dicts with uuid, source_dir, and file paths.
    """
    import pyarrow.parquet as pq

    parquet_dir = os.path.join(source_dir, "data", split)
    if not os.path.isdir(parquet_dir):
        print(f"ERROR: Directory not found: {parquet_dir}")
        print(f"Make sure you've downloaded the dataset to {source_dir}")
        sys.exit(1)

    # List all parquet files
    parquet_files = sorted(
        f for f in os.listdir(parquet_dir) if f.endswith(".parquet")
    )
    print(f"Found {len(parquet_files)} parquet files in {split} split")

    # Extract samples
    extracted = []
    sample_num = 0
    needed = n

    for pf in parquet_files[start_idx:]:
        if needed <= 0:
            break

        pf_path = os.path.join(parquet_dir, pf)
        print(f"\nReading {pf} ...")
        try:
            table = pq.read_table(pf_path)
        except Exception as e:
            print(f"  Skipping: {e}")
            continue

        rows = table.to_pydict()
        num_rows = len(rows["uuid"])

        for i in range(num_rows):
            if needed <= 0:
                break

            uid = str(rows["uuid"][i])
            cq_code = rows["cadquery_file"][i]
            ops_json = rows["cadquery_ops_json"][i]
            step_bytes = rows["step_file"][i]

            if isinstance(cq_code, bytes):
                cq_code = cq_code.decode("utf-8")
            if isinstance(ops_json, bytes):
                ops_json = ops_json.decode("utf-8")
            if step_bytes is None or len(step_bytes) == 0:
                continue

            # Validate ops_json is valid JSON
            try:
                ops_data = json.loads(ops_json)
                json.dumps(ops_data)  # round-trip to normalize
            except (json.JSONDecodeError, TypeError):
                continue

            # Create sample directory
            sample_dir = os.path.join(output_dir, f"sample_{sample_num + 1}")
            os.makedirs(sample_dir, exist_ok=True)

            # Write cadquery code
            cq_path = os.path.join(sample_dir, "cadquery_code.py")
            with open(cq_path, "w", encoding="utf-8") as f:
                f.write(cq_code)

            # Write ops trace
            ops_path = os.path.join(sample_dir, "ops_trace.json")
            with open(ops_path, "w", encoding="utf-8") as f:
                json.dump(ops_data, f, indent=2)

            # Write STEP file
            step_path = os.path.join(sample_dir, "model.step")
            with open(step_path, "wb") as f:
                f.write(step_bytes)

            # Write metadata
            meta = {
                "uuid": uid,
                "source_file": pf,
                "row_index": i,
                "num_faces": rows["num_faces"][i],
                "ops_count": rows["cadquery_ops_count"][i],
            }
            meta_path = os.path.join(sample_dir, "metadata.json")
            with open(meta_path, "w", encoding="utf-8") as f:
                json.dump(meta, f, indent=2)

            extracted.append({
                "uuid": uid,
                "sample_num": sample_num + 1,
                "dir": sample_dir,
                "num_faces": rows["num_faces"][i],
                "ops_count": rows["cadquery_ops_count"][i],
            })

            step_kb = len(step_bytes) / 1024
            print(
                f"  sample_{sample_num + 1}: {uid[:16]}... "
                f"faces={rows['num_faces'][i]} "
                f"ops={rows['cadquery_ops_count'][i]} "
                f"step={step_kb:.0f}KB"
            )

            sample_num += 1
            needed -= 1

    print(f"\nExtracted {len(extracted)} samples to {output_dir}/")
    return extracted


def main():
    parser = argparse.ArgumentParser(
        description="Extract exploration samples from Zero-To-CAD-100k"
    )
    parser.add_argument(
        "--source-dir",
        default="data/zero_to_cad_100k",
        help="Path to downloaded dataset",
    )
    parser.add_argument(
        "--output-dir",
        default="data/zero_to_cad_exploration",
        help="Output directory for samples",
    )
    parser.add_argument(
        "--split",
        default="train",
        choices=["train", "val", "test"],
        help="Dataset split to pull from",
    )
    parser.add_argument(
        "--n",
        type=int,
        default=5,
        help="Number of samples to extract",
    )
    parser.add_argument(
        "--start-idx",
        type=int,
        default=0,
        help="Starting parquet file index",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed",
    )
    args = parser.parse_args()

    extract_samples(
        source_dir=args.source_dir,
        output_dir=args.output_dir,
        split=args.split,
        n=args.n,
        start_idx=args.start_idx,
        seed=args.seed,
    )


if __name__ == "__main__":
    main()
