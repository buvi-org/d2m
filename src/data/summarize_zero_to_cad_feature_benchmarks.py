"""Markdown reporting for Zero-to-CAD feature-family benchmark summaries."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable


SUMMARY_GLOB = "feature_family_summary*.json"
PREFERRED_SUMMARY_NAMES = (
    "feature_family_summary_all.json",
    "feature_family_summary.json",
)
TOTAL_FIELDS = (
    "scanned",
    "plannable",
    "unsupported",
    "attempted",
    "executed",
    "matched",
    "failed",
)
FAMILY_COUNT_FIELDS = (
    "plannable",
    "unsupported",
    "attempted",
    "executed",
    "matched",
    "failed",
)


def load_summary(path: str | Path) -> dict[str, Any]:
    """Load one feature-family summary JSON from a file or output directory."""
    summary_path = resolve_summary_path(path)
    return json.loads(summary_path.read_text(encoding="utf-8"))


def resolve_summary_path(path: str | Path) -> Path:
    """Resolve a summary file path, preferring aggregate output in directories."""
    root = Path(path)
    if root.is_file():
        return root
    if not root.exists():
        raise FileNotFoundError(f"Summary path does not exist: {root}")
    if not root.is_dir():
        raise ValueError(f"Summary path is not a file or directory: {root}")

    for name in PREFERRED_SUMMARY_NAMES:
        candidate = root / name
        if candidate.exists():
            return candidate

    matches = sorted(root.glob(SUMMARY_GLOB))
    if not matches:
        raise FileNotFoundError(f"No {SUMMARY_GLOB} files found in {root}")
    if len(matches) > 1:
        names = ", ".join(match.name for match in matches)
        raise ValueError(f"Multiple summary files found; choose one explicitly: {names}")
    return matches[0]


def render_markdown_report(summary: dict[str, Any], *, top_n: int = 10) -> str:
    """Render a compact Markdown report for one single-split or aggregate summary."""
    split = str(summary.get("split") or "unknown")
    schema = str(summary.get("schema") or "")
    is_aggregate = split == "all" or "per_split" in summary or "aggregate" in schema
    title = "Zero-to-CAD Feature Benchmark Report"
    scope = "Aggregate" if is_aggregate else f"Split: {split}"

    lines = [
        f"# {title}",
        "",
        f"**Scope:** {scope}",
        "",
        "## Totals",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
    ]
    for field_name in TOTAL_FIELDS:
        lines.append(f"| {field_name} | {_format_int(summary.get(field_name, 0))} |")
    lines.append(f"| remaining_to_goal | {_format_int(summary.get('remaining_to_goal', 0))} |")
    lines.append(f"| match_rate | {_format_rate(summary.get('match_rate', 0))} |")

    if is_aggregate and summary.get("per_split"):
        lines.extend(_render_split_table(summary["per_split"]))

    families = _families(summary)
    lines.extend(_render_top_families(families, top_n=top_n))
    lines.extend(_render_family_statuses(families))
    return "\n".join(lines).rstrip() + "\n"


def write_markdown_report(
    input_path: str | Path,
    output_path: str | Path | None = None,
    *,
    top_n: int = 10,
) -> str:
    """Load a summary, render Markdown, optionally write it, and return the text."""
    summary = load_summary(input_path)
    markdown = render_markdown_report(summary, top_n=top_n)
    if output_path is not None:
        Path(output_path).write_text(markdown, encoding="utf-8")
    return markdown


def _render_split_table(per_split: dict[str, Any]) -> list[str]:
    lines = [
        "",
        "## Splits",
        "",
        "| Split | Scanned | Plannable | Unsupported | Attempted | Executed | Matched | Failed | Match Rate |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for split, payload in sorted(per_split.items()):
        lines.append(
            "| {split} | {scanned} | {plannable} | {unsupported} | {attempted} | "
            "{executed} | {matched} | {failed} | {match_rate} |".format(
                split=split,
                scanned=_format_int(payload.get("scanned", 0)),
                plannable=_format_int(payload.get("plannable", 0)),
                unsupported=_format_int(payload.get("unsupported", 0)),
                attempted=_format_int(payload.get("attempted", 0)),
                executed=_format_int(payload.get("executed", 0)),
                matched=_format_int(payload.get("matched", 0)),
                failed=_format_int(payload.get("failed", 0)),
                match_rate=_format_rate(payload.get("match_rate", 0)),
            )
        )
    return lines


def _render_top_families(families: dict[str, dict[str, Any]], *, top_n: int) -> list[str]:
    lines = [
        "",
        "## Top Families",
        "",
        "| Family | Plannable | Attempted | Executed | Matched | Failed | Unsupported | Match Rate |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for family, payload in _top_families(families, top_n=top_n):
        lines.append(
            "| {family} | {plannable} | {attempted} | {executed} | {matched} | "
            "{failed} | {unsupported} | {match_rate} |".format(
                family=family,
                plannable=_format_int(payload.get("plannable", 0)),
                attempted=_format_int(payload.get("attempted", 0)),
                executed=_format_int(payload.get("executed", 0)),
                matched=_format_int(payload.get("matched", 0)),
                failed=_format_int(payload.get("failed", 0)),
                unsupported=_format_int(payload.get("unsupported", 0)),
                match_rate=_family_match_rate(payload),
            )
        )
    if not families:
        lines.append("| _none_ | 0 | 0 | 0 | 0 | 0 | 0 | 0.00% |")
    return lines


def _render_family_statuses(families: dict[str, dict[str, Any]]) -> list[str]:
    lines = [
        "",
        "## Family Statuses",
        "",
        "| Family | Status Counts |",
        "| --- | --- |",
    ]
    if not families:
        lines.append("| _none_ | - |")
        return lines

    for family, payload in sorted(families.items()):
        statuses = _status_text(payload)
        lines.append(f"| {family} | {statuses} |")
    return lines


def _families(summary: dict[str, Any]) -> dict[str, dict[str, Any]]:
    families = summary.get("families") or {}
    return {
        str(family): dict(payload or {})
        for family, payload in families.items()
    }


def _top_families(
    families: dict[str, dict[str, Any]],
    *,
    top_n: int,
) -> list[tuple[str, dict[str, Any]]]:
    ranked = sorted(
        families.items(),
        key=lambda item: (-int(item[1].get("plannable", 0) or 0), item[0]),
    )
    return ranked[: max(int(top_n), 0)]


def _status_text(payload: dict[str, Any]) -> str:
    statuses = dict(payload.get("statuses") or {})
    if not statuses:
        derived = {
            field_name: int(payload.get(field_name, 0) or 0)
            for field_name in FAMILY_COUNT_FIELDS
            if int(payload.get(field_name, 0) or 0)
        }
        statuses = derived
    if not statuses:
        return "-"
    ordered = sorted(statuses.items(), key=lambda item: (-int(item[1] or 0), str(item[0])))
    return ", ".join(f"{status}: {_format_int(count)}" for status, count in ordered)


def _family_match_rate(payload: dict[str, Any]) -> str:
    executed = int(payload.get("executed", 0) or 0)
    matched = int(payload.get("matched", 0) or 0)
    return _format_rate(matched / executed if executed else 0)


def _format_rate(value: Any) -> str:
    try:
        rate = float(value)
    except (TypeError, ValueError):
        rate = 0.0
    return f"{rate * 100:.2f}%"


def _format_int(value: Any) -> str:
    try:
        number = int(value)
    except (TypeError, ValueError):
        number = 0
    return f"{number:,}"


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Render a compact Markdown report from feature_family_summary*.json.",
    )
    parser.add_argument("summary", help="Summary JSON file or output directory.")
    parser.add_argument("--output", "-o", default=None, help="Optional Markdown output path.")
    parser.add_argument("--top-n", type=int, default=10, help="Number of top families to include.")
    args = parser.parse_args(list(argv) if argv is not None else None)

    markdown = write_markdown_report(args.summary, args.output, top_n=args.top_n)
    if args.output is None:
        print(markdown, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
