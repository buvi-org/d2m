"""Run agentic translation on N exploration samples and report results."""
import json, os, sys, time
from pathlib import Path

os.chdir(Path(__file__).resolve().parent)

from dotenv import load_dotenv
load_dotenv()

from src.data.agentic_translator import AgenticTranslator


def run_batch(n: int = 10, tolerance: float = 0.05):
    translator = AgenticTranslator(
        provider="deepseek",
        tolerance=tolerance,
        stagnation_limit=5,
        safety_cap=15,
        verbose=True,
    )

    results = []
    for i in range(1, n + 1):
        sample_dir = f"data/zero_to_cad_exploration/sample_{i}"
        cq_path = os.path.join(sample_dir, "cadquery_code.py")
        ops_path = os.path.join(sample_dir, "ops_trace.json")
        step_path = os.path.join(sample_dir, "model.step")

        if not os.path.exists(cq_path):
            print(f"\n[{i}/{n}] SKIP — {sample_dir} not found")
            continue

        with open(cq_path) as f:
            cq_code = f.read()
        with open(ops_path) as f:
            ops_trace = json.load(f)

        uid = os.path.basename(sample_dir)
        print(f"\n{'='*60}")
        print(f"[{i}/{n}] Translating {uid}...")
        print(f"{'='*60}")

        t0 = time.time()
        result = translator.translate(
            {"cadquery_file": cq_code, "cadquery_ops_json": json.dumps(ops_trace), "uuid": uid},
            step_path=step_path,
        )
        elapsed = time.time() - t0

        # Save subCAD code
        code_path = os.path.join(sample_dir, "subcad_code.py")
        with open(code_path, "w") as f:
            f.write(result["subcad_code"] or "# FAILED")

        res_path = os.path.join(sample_dir, "translation_result.json")
        with open(res_path, "w") as f:
            json.dump({
                "uuid": uid,
                "success": result["success"],
                "attempts": result["attempts"],
                "stop_reason": result["stop_reason"],
                "volume_ratio": result.get("comparison", {}).get("volume_ratio"),
                "target_volume": result.get("comparison", {}).get("target_volume"),
                "candidate_volume": result.get("comparison", {}).get("candidate_volume"),
                "elapsed_s": round(elapsed, 1),
            }, f, indent=2)

        ratio = result.get("comparison", {}).get("volume_ratio", 0)
        error_pct = abs(1.0 - ratio) * 100 if ratio > 0 else 100
        status = "MATCH" if result["success"] else "FAIL"
        print(f"  {status} | ratio={ratio:.4f} (error={error_pct:.1f}%) | "
              f"{result['attempts']} attempts | {elapsed:.0f}s | {result['stop_reason']}")

        results.append({
            "sample": uid,
            "success": result["success"],
            "ratio": ratio,
            "error_pct": error_pct,
            "attempts": result["attempts"],
            "elapsed_s": elapsed,
            "stop_reason": result["stop_reason"],
        })

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    succeeded = sum(1 for r in results if r["success"])
    print(f"Matched: {succeeded}/{len(results)} ({succeeded/len(results)*100:.0f}%)")
    for r in results:
        status = "MATCH" if r["success"] else "FAIL"
        print(f"  {r['sample']}: {status} | ratio={r['ratio']:.4f} "
              f"error={r['error_pct']:.1f}% | {r['attempts']}att | {r['elapsed_s']:.0f}s")
    print(f"Total time: {sum(r['elapsed_s'] for r in results):.0f}s")

    # Save batch summary
    with open("data/zero_to_cad_exploration/batch_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"Saved: data/zero_to_cad_exploration/batch_results.json")


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    run_batch(n)
