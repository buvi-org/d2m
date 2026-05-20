"""Engineering economics estimates for SubCAD process plans.

This module intentionally produces review estimates, not shop quotes.  It uses
local versioned catalogs so tests and offline workflows have deterministic
machine, material, and tool cost data.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Iterable


ECONOMICS_SCHEMA_VERSION = "subcad.economics.v1"
DEFAULT_MACHINE = "generic_3axis_mill"
DEFAULT_WEIGHTS = {"time": 0.5, "cost": 0.5}


def estimate_cost(
    stock_or_plan: Any,
    machine: str = DEFAULT_MACHINE,
    quantity: int = 1,
    currency: str | None = None,
) -> dict:
    """Return a structured engineering time/cost estimate."""
    plan = _plan_dict(stock_or_plan)
    quantity = max(int(quantity or 1), 1)
    warnings: list[str] = []

    machine_entry = _catalog_entry("machines.json", "machines", machine)
    if machine_entry is None:
        warnings.append(f"Machine {machine!r} not found; using zero-rate defaults.")
        machine_entry = {
            "id": machine,
            "currency": currency or "USD",
            "machine_hourly_rate": 0.0,
            "setup_hourly_rate": 0.0,
            "default_tool_change_seconds": 0.0,
            "setup_minutes_per_setup": 0.0,
            "load_unload_minutes_per_part": 0.0,
        }
    resolved_currency = currency or machine_entry.get("currency") or "USD"

    material_result = _material_cost(plan, resolved_currency, warnings)
    operation_results, tooling_total = _operation_tooling_costs(plan, resolved_currency, warnings)

    cutting_time = round(sum(op["cutting_time_min"] for op in operation_results), 6)
    if cutting_time <= 0.0:
        cutting_time = float(plan.get("estimated_time_minutes") or 0.0)
    tool_change_count = _tool_change_count(plan)
    tool_change_seconds = _as_float(machine_entry.get("default_tool_change_seconds"), 0.0)
    tool_change_time = tool_change_count * tool_change_seconds / 60.0
    setup_count = _setup_count(plan)
    setup_total_time = setup_count * _as_float(machine_entry.get("setup_minutes_per_setup"), 0.0)
    setup_time_per_part = setup_total_time / quantity
    load_unload_time = _as_float(machine_entry.get("load_unload_minutes_per_part"), 0.0)
    machine_run_time_per_part = cutting_time + tool_change_time + load_unload_time
    total_time_per_part = machine_run_time_per_part + setup_time_per_part
    total_batch_time = setup_total_time + machine_run_time_per_part * quantity

    machine_cost = machine_run_time_per_part / 60.0 * _as_float(machine_entry.get("machine_hourly_rate"), 0.0)
    setup_cost = setup_time_per_part / 60.0 * _as_float(machine_entry.get("setup_hourly_rate"), 0.0)
    total_cost = material_result["material_cost"] + machine_cost + setup_cost + tooling_total

    return {
        "schema_version": ECONOMICS_SCHEMA_VERSION,
        "estimate_type": "engineering_estimate",
        "quote_status": "not_a_quote",
        "machine_id": machine_entry.get("id", machine),
        "machine": machine_entry,
        "quantity": quantity,
        "currency": resolved_currency,
        "time_breakdown": {
            "cutting_time_min": round(cutting_time, 6),
            "tool_change_count": tool_change_count,
            "tool_change_seconds_each": round(tool_change_seconds, 6),
            "tool_change_time_min": round(tool_change_time, 6),
            "setup_count": setup_count,
            "setup_time_total_min": round(setup_total_time, 6),
            "setup_time_per_part_min": round(setup_time_per_part, 6),
            "load_unload_time_per_part_min": round(load_unload_time, 6),
            "machine_run_time_per_part_min": round(machine_run_time_per_part, 6),
            "total_time_per_part_min": round(total_time_per_part, 6),
            "total_batch_time_min": round(total_batch_time, 6),
        },
        "cost_breakdown": {
            "material_cost": round(material_result["material_cost"], 6),
            "machine_cost": round(machine_cost, 6),
            "setup_cost": round(setup_cost, 6),
            "tooling_cost": round(tooling_total, 6),
            "total_cost": round(total_cost, 6),
            "total_batch_cost": round(total_cost * quantity, 6),
        },
        "material": material_result,
        "operations": operation_results,
        "tools": _tool_cost_summary(operation_results),
        "economics_warnings": warnings,
        "assumptions": [
            "Engineering estimate only; not a production quote.",
            "First tool load is treated as setup; only in-program tool transitions count as tool changes.",
            "Setup time and setup cost are amortized by quantity.",
        ],
    }


def compare_programs(
    programs: Iterable[Any],
    target: Any = None,
    weights: dict | None = None,
    quantity: int = 1,
    machine: str = DEFAULT_MACHINE,
) -> dict:
    """Compare multiple valid programs by time/cost Pareto and weighted score."""
    weights = _normalize_weights(weights or DEFAULT_WEIGHTS)
    candidates = []
    for index, program in enumerate(programs):
        estimate = estimate_cost(program, machine=machine, quantity=quantity)
        validation_errors = _validation_errors(program)
        comparison = _target_comparison(program, target)
        status = "valid"
        if validation_errors:
            status = "invalid"
        elif comparison and comparison.get("status") == "fail":
            status = "target_mismatch"

        candidates.append({
            "index": index,
            "status": status,
            "valid": status == "valid",
            "estimate": estimate,
            "validation_errors": validation_errors,
            "target_comparison": comparison,
            "time_min": estimate["time_breakdown"]["total_time_per_part_min"],
            "cost": estimate["cost_breakdown"]["total_cost"],
        })

    valid = [candidate for candidate in candidates if candidate["valid"]]
    if valid:
        min_time = min(candidate["time_min"] for candidate in valid)
        max_time = max(candidate["time_min"] for candidate in valid)
        min_cost = min(candidate["cost"] for candidate in valid)
        max_cost = max(candidate["cost"] for candidate in valid)
        for candidate in valid:
            time_norm = _normalize_metric(candidate["time_min"], min_time, max_time)
            cost_norm = _normalize_metric(candidate["cost"], min_cost, max_cost)
            candidate["score"] = round(100.0 * (1.0 - (weights["time"] * time_norm + weights["cost"] * cost_norm)), 6)
            candidate["pareto_optimal"] = _is_pareto(candidate, valid)

        fastest = min(valid, key=lambda candidate: candidate["time_min"])
        cheapest = min(valid, key=lambda candidate: candidate["cost"])
        weighted_best = max(valid, key=lambda candidate: candidate["score"])
        pareto = [candidate["index"] for candidate in valid if candidate.get("pareto_optimal")]
    else:
        fastest = cheapest = weighted_best = None
        pareto = []

    return {
        "schema_version": "subcad.program_comparison.v1",
        "quantity": max(int(quantity or 1), 1),
        "machine_id": machine,
        "weights": weights,
        "candidates": candidates,
        "fastest_index": fastest["index"] if fastest else None,
        "cheapest_index": cheapest["index"] if cheapest else None,
        "weighted_best_index": weighted_best["index"] if weighted_best else None,
        "pareto_optimal_indices": pareto,
    }


def _catalog_dir() -> Path:
    return Path(__file__).resolve().parent / "catalogs"


def _catalog_payload(filename: str) -> dict:
    path = _catalog_dir() / filename
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _catalog_entry(filename: str, key: str, entry_id: str) -> dict | None:
    for entry in _catalog_payload(filename).get(key, []):
        if str(entry.get("id")) == str(entry_id):
            return dict(entry)
    return None


def _plan_dict(source: Any) -> dict:
    if isinstance(source, dict):
        return dict(source)
    if hasattr(source, "process_plan"):
        return source.process_plan()
    if hasattr(source, "to_dict"):
        return source.to_dict()
    raise TypeError("Expected a Stock, ProcessPlan, or process-plan dict.")


def _material_cost(plan: dict, currency: str, warnings: list[str]) -> dict:
    material_id = str(plan.get("material") or "")
    entry = _catalog_entry("materials_cost.json", "materials", material_id)
    if entry is None:
        warnings.append(f"Material cost for {material_id or 'unspecified'} missing; material cost defaults to zero.")
        entry = {"id": material_id, "currency": currency, "price_per_kg": 0.0, "waste_factor": 1.0}

    density = _as_float(entry.get("density_gcm3"), None)
    if density is None:
        try:
            from .material import get_material_props

            density = _as_float(get_material_props(material_id).get("density_gcm3"), 0.0)
        except Exception:
            density = 0.0
    if density <= 0:
        warnings.append(f"Density for {material_id or 'unspecified'} missing; material mass defaults to zero.")

    volume_mm3 = _stock_volume_mm3(plan.get("stock_dimensions") or {})
    mass_kg = volume_mm3 * density / 1_000_000.0
    price_per_kg = _as_float(entry.get("price_per_kg"), 0.0)
    waste_factor = _as_float(entry.get("waste_factor"), 1.0)
    material_cost = mass_kg * price_per_kg * waste_factor
    if price_per_kg <= 0:
        warnings.append(f"Price per kg for {material_id or 'unspecified'} missing; material price defaults to zero.")

    return {
        "material_id": material_id,
        "currency": entry.get("currency", currency),
        "stock_volume_mm3": round(volume_mm3, 6),
        "density_gcm3": round(density, 6),
        "mass_kg": round(mass_kg, 6),
        "price_per_kg": round(price_per_kg, 6),
        "waste_factor": round(waste_factor, 6),
        "material_cost": material_cost,
    }


def _operation_tooling_costs(plan: dict, currency: str, warnings: list[str]) -> tuple[list[dict], float]:
    results = []
    total = 0.0
    for op in plan.get("operations", []):
        minutes = _operation_minutes(op)
        tool = op.get("tool") if isinstance(op.get("tool"), dict) else {}
        tool_id = _tool_identity(op)
        tool_cost_min = _tool_cost_per_min(tool_id, tool, warnings)
        cost = minutes * tool_cost_min
        total += cost
        results.append({
            "sequence_number": op.get("sequence_number"),
            "operation": op.get("operation"),
            "tool_id": tool_id,
            "cutting_time_min": round(minutes, 6),
            "tool_cost_per_cutting_min": round(tool_cost_min, 6),
            "tooling_cost": round(cost, 6),
            "currency": currency,
        })
    return results, total


def _tool_cost_per_min(tool_id: str, tool: dict, warnings: list[str]) -> float:
    for source in (tool, _tool_catalog_lookup(tool_id) or {}):
        explicit = _as_float(source.get("cost_per_cutting_min"), 0.0)
        if explicit > 0:
            return explicit
        replacement = _as_float(source.get("replacement_cost"), 0.0)
        life = _as_float(source.get("expected_life_minutes"), 0.0)
        if replacement > 0 and life > 0:
            return replacement / life
    if tool_id:
        warnings.append(f"Tool cost for {tool_id} missing; tooling cost defaults to zero.")
    return 0.0


def _tool_catalog_lookup(tool_id: str) -> dict | None:
    if not tool_id:
        return None
    try:
        from .tool_library import ToolCatalog

        return ToolCatalog.get(tool_id).to_dict()
    except Exception:
        return None


def _tool_cost_summary(operations: list[dict]) -> list[dict]:
    grouped: dict[str, dict] = {}
    for op in operations:
        tool_id = op.get("tool_id") or "unknown"
        item = grouped.setdefault(tool_id, {
            "tool_id": tool_id,
            "cutting_time_min": 0.0,
            "tooling_cost": 0.0,
            "tool_cost_per_cutting_min": op.get("tool_cost_per_cutting_min", 0.0),
        })
        item["cutting_time_min"] += op.get("cutting_time_min", 0.0)
        item["tooling_cost"] += op.get("tooling_cost", 0.0)
    return [
        {
            **item,
            "cutting_time_min": round(item["cutting_time_min"], 6),
            "tooling_cost": round(item["tooling_cost"], 6),
        }
        for item in grouped.values()
    ]


def _operation_minutes(op: dict) -> float:
    pass_plan = op.get("pass_plan") if isinstance(op.get("pass_plan"), dict) else {}
    for key in ("estimated_time_min", "estimated_time_minutes"):
        value = _as_float(pass_plan.get(key), None)
        if value is not None:
            return value
    summary = op.get("toolpath_summary") if isinstance(op.get("toolpath_summary"), dict) else {}
    for key in ("estimated_time_min", "estimated_time_minutes"):
        value = _as_float(summary.get(key), None)
        if value is not None:
            return value
    toolpath = op.get("toolpath") if isinstance(op.get("toolpath"), dict) else {}
    for key in ("estimated_time_min", "estimated_time_minutes"):
        value = _as_float(toolpath.get(key), None)
        if value is not None:
            return value
    return 0.0


def _tool_identity(op: dict) -> str:
    tool = op.get("tool") if isinstance(op.get("tool"), dict) else {}
    selection = op.get("tool_selection") if isinstance(op.get("tool_selection"), dict) else {}
    assembly = tool.get("assembly") if isinstance(tool.get("assembly"), dict) else {}
    for source in (selection, assembly, tool, op):
        for key in ("selected_tool_id", "catalog_id", "tool_id", "tool_number"):
            value = source.get(key) if isinstance(source, dict) else None
            if value not in (None, ""):
                return str(value)
    tool_type = tool.get("tool_type", op.get("tool_type", "tool"))
    diameter = tool.get("diameter_mm", op.get("tool_diameter_mm", ""))
    return f"{tool_type}:{diameter}"


def _tool_change_count(plan: dict) -> int:
    changes = 0
    previous = None
    for op in plan.get("operations", []):
        current = _tool_identity(op)
        if previous is not None and current != previous:
            changes += 1
        previous = current
    return changes


def _setup_count(plan: dict) -> int:
    setups = plan.get("setups") if isinstance(plan.get("setups"), dict) else {}
    if setups:
        return len(setups)
    names = {op.get("setup") for op in plan.get("operations", []) if op.get("setup")}
    if names:
        return len(names)
    return 1 if plan.get("operations") else 0


def _stock_volume_mm3(stock_dimensions: dict) -> float:
    length = _as_float(stock_dimensions.get("length"), 0.0)
    width = _as_float(stock_dimensions.get("width"), 0.0)
    height = _as_float(stock_dimensions.get("height"), 0.0)
    if length > 0 and width > 0 and height > 0:
        return length * width * height
    diameter = _as_float(stock_dimensions.get("diameter"), 0.0)
    if diameter > 0 and height > 0:
        return math.pi * (diameter / 2.0) ** 2 * height
    return 0.0


def _validation_errors(program: Any) -> list:
    try:
        if hasattr(program, "validate_shop_floor"):
            report = program.validate_shop_floor(structured=True)
            return list(getattr(report, "errors", []) or [])
    except Exception as exc:
        return [f"Validation failed: {exc}"]
    plan = _plan_dict(program)
    buckets = plan.get("validation_buckets") or plan.get("validation") or {}
    if isinstance(buckets, dict):
        return list(buckets.get("errors", []) or [])
    return []


def _target_comparison(program: Any, target: Any) -> dict | None:
    if target is None:
        return None
    if not hasattr(program, "compare_to_target"):
        return {"status": "unknown", "feedback": "Target comparison requires a Stock candidate."}
    try:
        return program.compare_to_target(target)
    except Exception as exc:
        return {"status": "fail", "feedback": f"Target comparison failed: {exc}"}


def _normalize_weights(weights: dict) -> dict:
    time = max(_as_float(weights.get("time"), 0.5), 0.0)
    cost = max(_as_float(weights.get("cost"), 0.5), 0.0)
    total = time + cost
    if total <= 0:
        return dict(DEFAULT_WEIGHTS)
    return {"time": time / total, "cost": cost / total}


def _normalize_metric(value: float, minimum: float, maximum: float) -> float:
    if maximum <= minimum:
        return 0.0
    return (value - minimum) / (maximum - minimum)


def _is_pareto(candidate: dict, valid: list[dict]) -> bool:
    for other in valid:
        if other is candidate:
            continue
        no_worse = other["time_min"] <= candidate["time_min"] and other["cost"] <= candidate["cost"]
        better = other["time_min"] < candidate["time_min"] or other["cost"] < candidate["cost"]
        if no_worse and better:
            return False
    return True


def _as_float(value: Any, default: float | None = 0.0) -> float:
    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default
