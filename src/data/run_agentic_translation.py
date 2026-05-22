"""CLI helper for live CadQuery -> SubCAD agentic translation runs.

This module is intentionally thin: it wraps the existing translator loop,
adds preflight checks, and saves artifacts from a live run.  It also supports a
dry-run mode so prompts/sample wiring can be checked without an API key.
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

from .agentic_translator import (
    AgenticTranslator,
    build_system_prompt,
    build_user_prompt,
)
from .cadquery_to_subcad import step_to_stock_dims


DEFAULT_SAMPLE_DIR = "data/zero_to_cad_exploration/sample_1"


def build_dry_run_preview(sample_dir: str, translation_mode: str = "planner_guided") -> dict[str, Any]:
    """Load a sample and build prompt metadata without calling an LLM."""
    paths = _sample_paths(sample_dir)
    _require_sample_files(paths)

    cq_code = paths["cadquery"].read_text(encoding="utf-8")
    ops_trace = json.loads(paths["ops"].read_text(encoding="utf-8"))
    stock_dims = step_to_stock_dims(paths["step"].read_bytes())
    system_prompt = build_system_prompt(translation_mode)
    user_prompt = build_user_prompt(
        cq_code,
        ops_trace,
        str(paths["step"]),
        stock_dims,
        translation_mode=translation_mode,
    )

    return {
        "sample_dir": str(Path(sample_dir)),
        "cadquery_chars": len(cq_code),
        "ops_trace_count": len(ops_trace) if isinstance(ops_trace, list) else 0,
        "stock_dims": stock_dims,
        "translation_mode": translation_mode,
        "system_prompt_chars": len(system_prompt),
        "user_prompt_chars": len(user_prompt),
        "system_prompt_preview": system_prompt[:700],
        "user_prompt_preview": user_prompt[:1200],
    }


def run_live_translation(
    sample_dir: str,
    *,
    provider: str = "deepseek",
    model: str | None = None,
    api_timeout_s: float = 120.0,
    output_dir: str | None = None,
    tolerance: float = 0.05,
    stagnation_limit: int = 3,
    divergence_limit: int = 2,
    safety_cap: int = 8,
    comparison_methods: list[str] | None = None,
    feature_aware: bool = False,
    verbose: bool = True,
    translation_mode: str = "planner_guided",
) -> dict[str, Any]:
    """Run the live translator and save a durable result bundle."""
    paths = _sample_paths(sample_dir)
    _require_sample_files(paths)
    _require_provider_key(provider)

    cq_code = paths["cadquery"].read_text(encoding="utf-8")
    ops_trace = json.loads(paths["ops"].read_text(encoding="utf-8"))
    sample = {
        "cadquery_file": cq_code,
        "cadquery_ops_json": json.dumps(ops_trace),
        "uuid": Path(sample_dir).name,
    }

    translator = AgenticTranslator(
        provider=provider,
        model=model,
        api_timeout_s=api_timeout_s,
        tolerance=tolerance,
        stagnation_limit=stagnation_limit,
        divergence_limit=divergence_limit,
        safety_cap=safety_cap,
        verbose=verbose,
        comparison_methods=comparison_methods,
        feature_aware=feature_aware,
        translation_mode=translation_mode,
    )
    result = translator.translate(sample, step_path=str(paths["step"]))

    bundle_dir = Path(output_dir) if output_dir else _default_output_dir(sample_dir)
    bundle_dir.mkdir(parents=True, exist_ok=True)
    _save_result_bundle(bundle_dir, result, paths, provider, model)
    result["output_dir"] = str(bundle_dir)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run CadQuery -> SubCAD agentic translation on one sample.",
    )
    parser.add_argument("--sample-dir", default=DEFAULT_SAMPLE_DIR)
    parser.add_argument("--provider", default="deepseek")
    parser.add_argument("--model", default=None)
    parser.add_argument("--api-timeout-s", type=float, default=120.0)
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--tolerance", type=float, default=0.05)
    parser.add_argument("--stagnation-limit", type=int, default=3)
    parser.add_argument("--divergence-limit", type=int, default=2)
    parser.add_argument("--safety-cap", type=int, default=8)
    parser.add_argument(
        "--comparison-methods",
        default="sdf,slice",
        help="Comma-separated mesh comparison methods, or 'none'.",
    )
    parser.add_argument("--feature-aware", action="store_true")
    parser.add_argument(
        "--translation-mode",
        default="planner_guided",
        choices=["planner_guided", "ai_heavy"],
        help="planner_guided uses deterministic/planner-first behavior; ai_heavy skips deterministic builders and treats planner candidates as advisory.",
    )
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Build prompts and sample metadata without calling the LLM.",
    )
    args = parser.parse_args(argv)

    if args.dry_run:
        print(json.dumps(build_dry_run_preview(args.sample_dir, args.translation_mode), indent=2, default=str))
        return 0

    comparison_methods = _parse_methods(args.comparison_methods)
    try:
        result = run_live_translation(
            args.sample_dir,
            provider=args.provider,
            model=args.model,
            api_timeout_s=args.api_timeout_s,
            output_dir=args.output_dir,
            tolerance=args.tolerance,
            stagnation_limit=args.stagnation_limit,
            divergence_limit=args.divergence_limit,
            safety_cap=args.safety_cap,
            comparison_methods=comparison_methods,
            feature_aware=args.feature_aware,
            verbose=not args.quiet,
            translation_mode=args.translation_mode,
        )
    except Exception as exc:
        print(f"ERROR: {exc}")
        return 2

    status = "PASS" if result.get("success") else "FAIL"
    print(
        f"{status}: attempts={result.get('attempts')} "
        f"stop={result.get('stop_reason')} output={result.get('output_dir')}"
    )
    return 0 if result.get("success") else 1


def _sample_paths(sample_dir: str) -> dict[str, Path]:
    root = Path(sample_dir)
    return {
        "root": root,
        "cadquery": root / "cadquery_code.py",
        "ops": root / "ops_trace.json",
        "step": root / "model.step",
    }


def _require_sample_files(paths: dict[str, Path]) -> None:
    missing = [str(path) for key, path in paths.items() if key != "root" and not path.exists()]
    if missing:
        raise FileNotFoundError("Missing sample files: " + ", ".join(missing))


def _require_provider_key(provider: str) -> None:
    env_by_provider = {
        "deepseek": "DEEPSEEK_API_KEY",
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
    }
    env_name = env_by_provider.get(provider.lower())
    if env_name and not os.environ.get(env_name):
        raise RuntimeError(
            f"{env_name} is not set. Export it before running a live translation."
        )


def _default_output_dir(sample_dir: str) -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return Path("runs") / "agentic_translator" / f"{Path(sample_dir).name}_{stamp}"


def _parse_methods(raw: str) -> list[str] | None:
    if raw.strip().lower() in {"", "none", "off", "false"}:
        return None
    return [item.strip() for item in raw.split(",") if item.strip()]


def _save_result_bundle(
    output_dir: Path,
    result: dict[str, Any],
    paths: dict[str, Path],
    provider: str,
    model: str | None,
) -> None:
    if result.get("subcad_code"):
        (output_dir / "generated_subcad.py").write_text(
            result["subcad_code"],
            encoding="utf-8",
        )

    metadata = {
        "provider": provider,
        "model": model,
        "sample_dir": str(paths["root"]),
        "source_cadquery": str(paths["cadquery"]),
        "source_step": str(paths["step"]),
        "success": result.get("success", False),
        "attempts": result.get("attempts", 0),
        "stop_reason": result.get("stop_reason"),
    }
    (output_dir / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2, default=str),
        encoding="utf-8",
    )
    (output_dir / "result.json").write_text(
        json.dumps(_json_safe_result(result), indent=2, default=str),
        encoding="utf-8",
    )


def _json_safe_result(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: _json_safe_result(item)
            for key, item in value.items()
            if key != "part"
        }
    if isinstance(value, list):
        return [_json_safe_result(item) for item in value]
    if isinstance(value, tuple):
        return [_json_safe_result(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


if __name__ == "__main__":
    raise SystemExit(main())
