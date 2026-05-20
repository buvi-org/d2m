"""Generate executable SubCAD -> STEP training pairs.

This is the deterministic dataset path for the specialist STEP-to-SubCAD
model.  It creates pairs without using LLM calls:

    SubCAD source code -> executable Stock -> STEP/process plan/economics

The generator is resumable and intended to scale to 100k samples on local
hardware.  Data output is under ``data/`` by default, which is gitignored.
"""

from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import os
import random
import shutil
import sys
import time
import traceback
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


MATERIALS = [
    "aluminum_6061",
    "aluminum_7075",
    "steel_4140",
    "steel_304",
]


@dataclass
class PairSpec:
    sample_id: str
    seed: int
    material: str
    length: float
    width: float
    stock_height: float
    face_depth: float
    operations: list[dict[str, Any]]

    @property
    def final_height(self) -> float:
        return round(self.stock_height - self.face_depth, 3)


def generate_dataset(
    count: int = 100_000,
    output_dir: str = "data/subcad_pairs_100k",
    seed: int = 9409,
    workers: int = 1,
    resume: bool = True,
    start_index: int = 0,
    shard_size: int = 1000,
    keep_stl: bool = False,
) -> dict[str, Any]:
    """Generate a dataset of SubCAD pairs."""
    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    _write_dataset_info(root, count, seed, shard_size)

    indices = [
        i for i in range(start_index, start_index + count)
        if not (resume and _is_complete(_sample_dir(root, i, shard_size)))
    ]

    t0 = time.perf_counter()
    if workers > 1 and len(indices) > 1:
        mp.set_start_method("spawn", force=True)
        tasks = [
            (i, seed, str(root), shard_size, keep_stl)
            for i in indices
        ]
        with mp.Pool(processes=workers) as pool:
            results = list(pool.imap_unordered(_worker_generate_one, tasks))
    else:
        results = [
            _worker_generate_one((i, seed, str(root), shard_size, keep_stl))
            for i in indices
        ]

    elapsed = time.perf_counter() - t0
    generated = sum(1 for item in results if item.get("ok"))
    failed = sum(1 for item in results if not item.get("ok"))
    completed_total = count_completed(root)
    manifest = {
        "requested_count": count,
        "start_index": start_index,
        "generated_this_run": generated,
        "failed_this_run": failed,
        "completed_total": completed_total,
        "elapsed_seconds": elapsed,
        "samples_per_minute": round(generated / max(elapsed, 0.1) * 60.0, 2),
        "output_dir": str(root),
        "errors_path": str(root / "_errors.jsonl"),
    }
    (root / "manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )
    return manifest


def count_completed(output_dir: str | Path) -> int:
    root = Path(output_dir)
    if not root.exists():
        return 0
    return sum(1 for path in root.glob("shard_*/sample_*") if _is_complete(path))


def build_pair_spec(index: int, seed: int = 9409) -> PairSpec:
    """Build a deterministic, safe SubCAD program specification."""
    rng = random.Random(seed + index)
    length = _round(rng.uniform(50.0, 140.0))
    width = _round(rng.uniform(35.0, 100.0))
    stock_height = _round(rng.uniform(12.0, 45.0))
    face_depth = _round(rng.uniform(0.4, min(2.2, stock_height * 0.12)))
    final_height = stock_height - face_depth
    material = rng.choice(MATERIALS)
    operations: list[dict[str, Any]] = [
        {"type": "face_mill", "depth": face_depth},
    ]

    feature_count = rng.randint(2, 5)
    used_points: list[tuple[float, float, float]] = []
    used_boxes: list[tuple[float, float, float, float]] = []
    for _ in range(feature_count):
        choices = ["pocket", "drill", "slot", "circular_pocket"]
        op_type = rng.choice(choices)

        if op_type == "pocket":
            pocket_length = _round(rng.uniform(10.0, min(length * 0.38, 42.0)))
            pocket_width = _round(rng.uniform(8.0, min(width * 0.38, 30.0)))
            placed = _placed_center(
                rng, length, width, pocket_length, pocket_width, used_boxes
            )
            if placed is None:
                continue
            cx, cy = placed
            depth = _round(rng.uniform(1.0, max(1.5, final_height * 0.55)))
            operations.append({
                "type": "pocket",
                "length": pocket_length,
                "width": pocket_width,
                "depth": min(depth, _round(final_height - 1.0)),
                "corner_radius": 0.0,
                "cx": cx,
                "cy": cy,
            })
        elif op_type == "circular_pocket":
            diameter = _round(rng.uniform(8.0, min(length, width, 28.0)))
            placed = _placed_center(
                rng, length, width, diameter, diameter, used_boxes
            )
            if placed is None:
                continue
            cx, cy = placed
            depth = _round(rng.uniform(1.0, max(1.5, final_height * 0.45)))
            operations.append({
                "type": "circular_pocket",
                "diameter": diameter,
                "depth": min(depth, _round(final_height - 1.0)),
                "cx": cx,
                "cy": cy,
            })
        elif op_type == "slot":
            slot_width = _round(rng.uniform(5.0, min(width * 0.22, 14.0)))
            slot_length = _round(rng.uniform(max(slot_width + 8.0, 18.0), min(length * 0.48, 55.0)))
            angle = rng.choice([0.0, 0.0, 90.0])
            bound_length = slot_width if angle == 90.0 else slot_length
            bound_width = slot_length if angle == 90.0 else slot_width
            placed = _placed_center(
                rng, length, width, bound_length, bound_width, used_boxes
            )
            if placed is None:
                continue
            cx, cy = placed
            depth = _round(rng.uniform(1.0, max(1.5, final_height * 0.45)))
            operations.append({
                "type": "slot",
                "length": slot_length,
                "width": slot_width,
                "depth": min(depth, _round(final_height - 1.0)),
                "angle": angle,
                "cx": cx,
                "cy": cy,
            })
        else:
            diameter = _round(rng.choice([3.0, 4.0, 5.0, 6.0, 8.0, 10.0]))
            placed = _placed_center(
                rng, length, width, diameter, diameter, used_boxes
            )
            if placed is None:
                continue
            cx, cy = placed
            used_points.append((cx, cy, diameter))
            through = rng.random() < 0.45
            depth = _round(final_height + 1.0 if through else rng.uniform(4.0, max(4.5, final_height * 0.8)))
            operations.append({
                "type": "drill",
                "diameter": diameter,
                "depth": depth,
                "through": through,
                "cx": cx,
                "cy": cy,
            })

    # Keep the first 100k pair run focused on robust volumetric features.
    # CadQuery edge chamfers can fail on some randomized feature interactions,
    # so chamfer-heavy augmentation should be a later dataset shard.

    return PairSpec(
        sample_id=f"subcad_{index:06d}",
        seed=seed + index,
        material=material,
        length=length,
        width=width,
        stock_height=stock_height,
        face_depth=face_depth,
        operations=operations,
    )


def render_subcad_source(spec: PairSpec) -> str:
    """Render a REPL-executable SubCAD program from a spec."""
    lines = [
        "from types import SimpleNamespace as Measures",
        "",
        "m = Measures(",
        f"    length={spec.length!r},",
        f"    width={spec.width!r},",
        f"    stock_height={spec.stock_height!r},",
        f"    face_depth={spec.face_depth!r},",
        f"    material={spec.material!r},",
        ")",
        "",
        "part = Stock.rectangular(m.length, m.width, m.stock_height, material=m.material)",
    ]

    for op in spec.operations:
        if op["type"] == "face_mill":
            lines.append(f"part = part.face_mill(depth={op['depth']!r})")
        elif op["type"] == "pocket":
            lines.append(
                "part = part.pocket("
                f"width={op['width']!r}, length={op['length']!r}, depth={op['depth']!r}, "
                f"corner_radius={op['corner_radius']!r}, cx={op['cx']!r}, cy={op['cy']!r})"
            )
        elif op["type"] == "circular_pocket":
            lines.append(
                "part = part.circular_pocket("
                f"diameter={op['diameter']!r}, depth={op['depth']!r}, "
                f"cx={op['cx']!r}, cy={op['cy']!r})"
            )
        elif op["type"] == "slot":
            lines.append(
                "part = part.slot("
                f"length={op['length']!r}, width={op['width']!r}, depth={op['depth']!r}, "
                f"angle={op['angle']!r}, cx={op['cx']!r}, cy={op['cy']!r})"
            )
        elif op["type"] == "drill":
            lines.append(
                "part = part.drill("
                f"diameter={op['diameter']!r}, depth={op['depth']!r}, "
                f"cx={op['cx']!r}, cy={op['cy']!r}, through={op['through']!r})"
            )
        elif op["type"] == "chamfer":
            lines.append(f"part = part.chamfer(width={op['width']!r})")

    return "\n".join(lines) + "\n"


def generate_one(index: int, output_dir: str | Path, seed: int = 9409, shard_size: int = 1000, keep_stl: bool = False) -> dict[str, Any]:
    """Generate one pair and write it to disk."""
    from src.data.subcad_repl import run_subcad

    root = Path(output_dir)
    sample_dir = _sample_dir(root, index, shard_size)
    if sample_dir.exists():
        shutil.rmtree(sample_dir)
    tmp_dir = sample_dir
    tmp_dir.mkdir(parents=True, exist_ok=True)

    spec = build_pair_spec(index, seed)
    source = render_subcad_source(spec)
    exec_result = run_subcad(source)
    if not exec_result.get("success"):
        raise RuntimeError(exec_result.get("error", "SubCAD execution failed"))

    plan = exec_result.get("process_plan") or {}
    part = exec_result.get("part")
    validation = part.validate_shop_floor(structured=True) if part is not None else {}
    economics = part.estimate_cost(quantity=1) if part is not None else {}

    step_src = exec_result.get("step_path")
    if not step_src:
        raise RuntimeError("SubCAD execution did not export STEP")

    shutil.copy2(step_src, tmp_dir / "model.step")
    if keep_stl and exec_result.get("stl_path"):
        shutil.copy2(exec_result["stl_path"], tmp_dir / "model.stl")

    (tmp_dir / "subcad_program.py").write_text(source, encoding="utf-8")
    _write_json(tmp_dir / "spec.json", asdict(spec) | {"final_height": spec.final_height})
    _write_json(tmp_dir / "features.json", _features_from_spec(spec))
    _write_json(tmp_dir / "process_plan.json", plan)
    _write_json(tmp_dir / "validation.json", validation)
    _write_json(tmp_dir / "economics.json", economics)
    _write_json(tmp_dir / "metadata.json", {
        "sample_id": spec.sample_id,
        "index": index,
        "seed": spec.seed,
        "schema": "subcad.pair.v1",
        "source": "deterministic_subcad_generator",
        "files": [
            "subcad_program.py",
            "model.step",
            "spec.json",
            "features.json",
            "process_plan.json",
            "validation.json",
            "economics.json",
        ],
    })

    complete = tmp_dir / "_COMPLETE"
    complete.write_text(time.strftime("%Y-%m-%dT%H:%M:%S"), encoding="utf-8")

    _cleanup_temp(exec_result)
    return {
        "index": index,
        "sample_id": spec.sample_id,
        "ok": True,
        "operation_count": len(plan.get("operations", [])),
        "sample_dir": str(sample_dir),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate deterministic SubCAD -> STEP training pairs.",
    )
    parser.add_argument("--count", type=int, default=100_000)
    parser.add_argument("--output-dir", default="data/subcad_pairs_100k")
    parser.add_argument("--seed", type=int, default=9409)
    parser.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    parser.add_argument("--start-index", type=int, default=0)
    parser.add_argument("--shard-size", type=int, default=1000)
    parser.add_argument("--no-resume", action="store_true")
    parser.add_argument("--keep-stl", action="store_true")
    parser.add_argument("--count-complete", action="store_true")
    args = parser.parse_args(argv)

    if args.count_complete:
        print(count_completed(args.output_dir))
        return 0

    manifest = generate_dataset(
        count=args.count,
        output_dir=args.output_dir,
        seed=args.seed,
        workers=args.workers,
        resume=not args.no_resume,
        start_index=args.start_index,
        shard_size=args.shard_size,
        keep_stl=args.keep_stl,
    )
    print(json.dumps(manifest, indent=2))
    return 0 if manifest["failed_this_run"] == 0 else 1


def _worker_generate_one(args: tuple[int, int, str, int, bool]) -> dict[str, Any]:
    index, seed, output_dir, shard_size, keep_stl = args
    try:
        return generate_one(index, output_dir, seed, shard_size, keep_stl)
    except Exception as exc:
        root = Path(output_dir)
        root.mkdir(parents=True, exist_ok=True)
        with (root / "_errors.jsonl").open("a", encoding="utf-8") as fh:
            json.dump({
                "index": index,
                "error": str(exc),
                "traceback": traceback.format_exc(),
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            }, fh)
            fh.write("\n")
        return {"index": index, "ok": False, "error": str(exc)}


def _features_from_spec(spec: PairSpec) -> dict[str, Any]:
    return {
        "schema": "subcad.features.v1",
        "sample_id": spec.sample_id,
        "material": spec.material,
        "dimensions": {
            "length": spec.length,
            "width": spec.width,
            "stock_height": spec.stock_height,
            "final_height": spec.final_height,
        },
        "features": [
            {"feature_id": f"F{i:03d}", **op}
            for i, op in enumerate(spec.operations, start=1)
        ],
    }


def _sample_dir(root: Path, index: int, shard_size: int) -> Path:
    shard = index // shard_size
    return root / f"shard_{shard:04d}" / f"sample_{index:06d}"


def _is_complete(sample_dir: Path) -> bool:
    if sample_dir.name.endswith(".tmp"):
        return False
    required = [
        "subcad_program.py",
        "model.step",
        "spec.json",
        "features.json",
        "process_plan.json",
        "metadata.json",
        "_COMPLETE",
    ]
    return sample_dir.is_dir() and all((sample_dir / name).exists() for name in required)


def _round(value: float) -> float:
    return round(float(value), 3)


def _safe_center(rng: random.Random, length: float, width: float, feat_length: float, feat_width: float) -> tuple[float, float]:
    x_margin = max(feat_length / 2.0 + 4.0, 6.0)
    y_margin = max(feat_width / 2.0 + 4.0, 6.0)
    cx = rng.uniform(-length / 2.0 + x_margin, length / 2.0 - x_margin)
    cy = rng.uniform(-width / 2.0 + y_margin, width / 2.0 - y_margin)
    return _round(cx), _round(cy)


def _placed_center(
    rng: random.Random,
    length: float,
    width: float,
    feat_length: float,
    feat_width: float,
    used_boxes: list[tuple[float, float, float, float]],
    clearance: float = 3.0,
) -> tuple[float, float] | None:
    """Place a feature footprint without overlapping earlier features."""
    for _ in range(40):
        cx, cy = _safe_center(rng, length, width, feat_length, feat_width)
        box = _footprint(cx, cy, feat_length, feat_width, clearance)
        if not any(_boxes_overlap(box, existing) for existing in used_boxes):
            used_boxes.append(box)
            return cx, cy
    return None


def _footprint(
    cx: float,
    cy: float,
    feat_length: float,
    feat_width: float,
    clearance: float,
) -> tuple[float, float, float, float]:
    return (
        cx - feat_length / 2.0 - clearance,
        cx + feat_length / 2.0 + clearance,
        cy - feat_width / 2.0 - clearance,
        cy + feat_width / 2.0 + clearance,
    )


def _boxes_overlap(
    a: tuple[float, float, float, float],
    b: tuple[float, float, float, float],
) -> bool:
    return not (a[1] <= b[0] or b[1] <= a[0] or a[3] <= b[2] or b[3] <= a[2])


def _spaced_point(
    rng: random.Random,
    length: float,
    width: float,
    diameter: float,
    used: list[tuple[float, float, float]],
) -> tuple[float, float]:
    for _ in range(20):
        cx, cy = _safe_center(rng, length, width, diameter, diameter)
        if all(((cx - ux) ** 2 + (cy - uy) ** 2) ** 0.5 > (diameter + ud + 4.0) for ux, uy, ud in used):
            used.append((cx, cy, diameter))
            return cx, cy
    cx, cy = _safe_center(rng, length, width, diameter, diameter)
    used.append((cx, cy, diameter))
    return cx, cy


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")


def _write_dataset_info(root: Path, count: int, seed: int, shard_size: int) -> None:
    info_path = root / "dataset_info.json"
    if info_path.exists():
        return
    _write_json(info_path, {
        "schema": "subcad_pairs_dataset.v1",
        "target_count": count,
        "seed": seed,
        "shard_size": shard_size,
        "description": "Deterministic executable SubCAD-to-STEP training pairs.",
    })


def _cleanup_temp(exec_result: dict[str, Any]) -> None:
    for key in ("step_path", "stl_path"):
        path = exec_result.get(key)
        if path and os.path.exists(path):
            try:
                os.unlink(path)
            except OSError:
                pass


if __name__ == "__main__":
    raise SystemExit(main())
