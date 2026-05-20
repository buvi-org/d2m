"""Benchmark bookkeeping for CadQuery -> SubCAD translation trials.

The helpers here intentionally do not require live LLM calls.  They normalize
translation results into durable records so live and mocked runs can share the
same reporting format.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable, Optional


@dataclass
class TranslationBenchmarkRecord:
    sample_id: str
    source_cadquery: str
    generated_subcad: str = ""
    execution_result: dict[str, Any] = field(default_factory=dict)
    comparison_metrics: dict[str, Any] = field(default_factory=dict)
    feedback: str = ""
    status: str = "error"
    attempts: int = 0
    error: str = ""

    @property
    def success(self) -> bool:
        return self.status == "pass"

    def to_dict(self) -> dict:
        data = asdict(self)
        data["success"] = self.success
        return data


def normalize_translation_result(
    sample_id: str,
    source_cadquery: str,
    result: dict[str, Any],
) -> TranslationBenchmarkRecord:
    """Convert an existing translator result dict into a benchmark record."""
    comparison = result.get("comparison") or result.get("comparison_metrics") or {}
    success = bool(result.get("success"))
    error = str(result.get("error") or "")
    status = "pass" if success else ("error" if error else "fail")
    feedback = result.get("feedback") or _feedback_from_history(result.get("history")) or ""
    return TranslationBenchmarkRecord(
        sample_id=sample_id,
        source_cadquery=source_cadquery,
        generated_subcad=result.get("subcad_code") or result.get("generated_subcad") or "",
        execution_result=result.get("exec_result") or result.get("execution_result") or {},
        comparison_metrics=comparison,
        feedback=feedback,
        status=status,
        attempts=int(result.get("attempts") or 0),
        error=error,
    )


def run_translation_benchmark(
    samples: Iterable[dict[str, Any]],
    translator_fn: Callable[[dict[str, Any]], dict[str, Any]],
    output_dir: Optional[str] = None,
) -> dict:
    """Run a translation benchmark using an injected translator function.

    ``samples`` are dicts with ``sample_id`` and ``cadquery_code`` keys.  The
    translator function receives each sample and returns the same result shape
    used by ``AgenticTranslator.translate``.
    """
    records: list[TranslationBenchmarkRecord] = []
    for index, sample in enumerate(samples):
        sample_id = str(sample.get("sample_id") or sample.get("uuid") or f"sample_{index:04d}")
        source = str(sample.get("cadquery_code") or sample.get("cadquery_file") or "")
        try:
            result = translator_fn(sample)
            record = normalize_translation_result(sample_id, source, result)
        except Exception as exc:
            record = TranslationBenchmarkRecord(
                sample_id=sample_id,
                source_cadquery=source,
                status="error",
                error=str(exc),
            )
        records.append(record)

    summary = summarize_benchmark(records)
    payload = {
        "summary": summary,
        "records": [record.to_dict() for record in records],
    }
    if output_dir:
        save_benchmark(payload, output_dir)
    return payload


def summarize_benchmark(records: Iterable[TranslationBenchmarkRecord]) -> dict:
    records = list(records)
    total = len(records)
    passed = sum(1 for record in records if record.status == "pass")
    failed = sum(1 for record in records if record.status == "fail")
    errors = sum(1 for record in records if record.status == "error")
    attempts = sum(record.attempts for record in records)
    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "errors": errors,
        "pass_rate": round(passed / total, 4) if total else 0.0,
        "average_attempts": round(attempts / total, 2) if total else 0.0,
        "common_failure_modes": _common_failure_modes(records),
    }


def save_benchmark(payload: dict, output_dir: str) -> None:
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    with open(path / "summary.json", "w", encoding="utf-8") as fh:
        json.dump(payload["summary"], fh, indent=2)
    with open(path / "records.json", "w", encoding="utf-8") as fh:
        json.dump(payload["records"], fh, indent=2)


def _feedback_from_history(history) -> str:
    if not isinstance(history, list) or not history:
        return ""
    last = history[-1]
    if isinstance(last, dict):
        return str(
            last.get("feedback")
            or last.get("mesh_feedback")
            or last.get("feature_feedback")
            or ""
        )
    return ""


def _common_failure_modes(records: list[TranslationBenchmarkRecord]) -> list[str]:
    modes: dict[str, int] = {}
    for record in records:
        if record.status == "pass":
            continue
        text = record.error or record.feedback or "unknown"
        key = text.strip().splitlines()[0][:80] if text.strip() else "unknown"
        modes[key] = modes.get(key, 0) + 1
    return [
        f"{name} ({count})"
        for name, count in sorted(modes.items(), key=lambda item: item[1], reverse=True)
    ][:5]


if __name__ == "__main__":
    payload = run_translation_benchmark(
        [{"sample_id": "demo", "cadquery_code": "import cadquery as cq"}],
        lambda sample: {"success": True, "subcad_code": "part = Stock.rectangular(1,1,1)", "attempts": 1},
    )
    assert payload["summary"]["pass_rate"] == 1.0
    print("translator_benchmark self-test passed")
