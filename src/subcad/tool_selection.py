"""Inventory-aware tool selection for SubCAD operations."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .tool_library import ToolCatalog, ToolSpec


@dataclass
class ToolRequirement:
    """Capability requested by an operation before a real tool is selected."""

    tool_type: str
    min_diameter_mm: float = 0.0
    max_diameter_mm: Optional[float] = None
    min_flute_length_mm: float = 0.0
    feature: str = ""
    reason: str = ""
    prefer_largest: bool = False

    def to_dict(self) -> dict:
        return {
            "tool_type": self.tool_type,
            "min_diameter_mm": self.min_diameter_mm,
            "max_diameter_mm": self.max_diameter_mm,
            "min_flute_length_mm": self.min_flute_length_mm,
            "feature": self.feature,
            "reason": self.reason,
            "prefer_largest": self.prefer_largest,
        }


@dataclass
class ToolSelectionResult:
    """Structured result of resolving a requested capability to inventory."""

    requirement: ToolRequirement
    selected_tool: Optional[ToolSpec] = None
    rejected_tools: list[dict] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return self.selected_tool is not None and not self.errors

    def to_dict(self) -> dict:
        return {
            "ok": self.ok,
            "requirement": self.requirement.to_dict(),
            "selected_tool_id": (
                self.selected_tool.catalog_id if self.selected_tool else None
            ),
            "reason": self.requirement.reason,
            "rejected_tools": self.rejected_tools,
            "warnings": list(self.warnings),
            "errors": list(self.errors),
        }


def select_tool(requirement: ToolRequirement) -> ToolSelectionResult:
    """Select an available catalog tool and record rejected candidates."""
    ToolCatalog._ensure_initialised()
    result = ToolSelectionResult(requirement=requirement)
    candidates: list[ToolSpec] = []

    for name, tool in sorted(ToolCatalog._tools.items(), key=lambda item: item[1].diameter):
        reasons: list[str] = []
        if tool.tool_type != requirement.tool_type:
            reasons.append("wrong_type")
        if tool.inventory_count <= 0:
            reasons.append("unavailable")
        if tool.diameter < requirement.min_diameter_mm:
            reasons.append("diameter_too_small")
        if (
            requirement.max_diameter_mm is not None
            and tool.diameter > requirement.max_diameter_mm
        ):
            reasons.append("diameter_too_large")
        if requirement.min_flute_length_mm:
            reach = tool.reach_mm or tool.flute_length
            if reach < requirement.min_flute_length_mm:
                reasons.append("reach_too_short")

        if reasons:
            if tool.tool_type == requirement.tool_type:
                result.rejected_tools.append({
                    "tool_id": tool.catalog_id or name,
                    "diameter_mm": tool.diameter,
                    "flute_length_mm": tool.flute_length,
                    "reach_mm": tool.reach_mm or tool.flute_length,
                    "inventory_count": tool.inventory_count,
                    "reasons": reasons,
                })
            continue
        candidates.append(tool)

    if candidates:
        candidates.sort(key=lambda tool: tool.diameter)
        result.selected_tool = candidates[-1] if requirement.prefer_largest else candidates[0]
        return result

    message = (
        f"No available {requirement.tool_type} satisfies "
        f"diameter {requirement.min_diameter_mm:g}"
    )
    if requirement.max_diameter_mm is not None:
        message += f"..{requirement.max_diameter_mm:g}"
    if requirement.min_flute_length_mm:
        message += f" and reach {requirement.min_flute_length_mm:g}mm"
    result.errors.append(message)
    return result


def select_or_fallback(requirement: ToolRequirement, fallback: ToolSpec) -> tuple[ToolSpec, ToolSelectionResult]:
    """Return selected inventory, or a fallback tool with a structured error."""
    result = select_tool(requirement)
    if result.selected_tool is not None:
        return result.selected_tool, result
    result.selected_tool = fallback
    result.warnings.append("Using fallback tool so legacy geometry can still be generated.")
    return fallback, result
