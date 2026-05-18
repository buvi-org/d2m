"""SubCAD ProcessPlan: records every subtractive operation into a serializable plan.

A ProcessPlan is the output artifact that tells a machinist (or downstream
CAM software) exactly what operations to perform, in what order, with which
tools. It can be serialized to JSON for interchange.
"""

from __future__ import annotations

import json
import tempfile
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class OperationStep:
    """A single step in a subtractive machining process.

    Simplified copy from the rules.py pattern. Each step describes one
    tool engagement (face mill, pocket, drill, etc.) at a specific location
    with feeds/speeds data when available.
    """

    sequence_number: int
    operation: str  # "face_mill", "rough_pocket", "drill", etc.
    tool_type: str
    tool_diameter_mm: float
    depth_mm: float = 0.0
    position: Optional[tuple] = None  # (x, y) on workplane
    feeds_speeds: Optional[dict] = None
    notes: str = ""

    def to_dict(self) -> dict:
        """Return a JSON-serializable dictionary representation."""
        result: dict = {
            "sequence_number": self.sequence_number,
            "operation": self.operation,
            "tool_type": self.tool_type,
            "tool_diameter_mm": self.tool_diameter_mm,
            "depth_mm": self.depth_mm,
            "notes": self.notes,
        }
        if self.position is not None:
            result["position"] = list(self.position)
        if self.feeds_speeds is not None:
            result["feeds_speeds"] = self.feeds_speeds
        return result


@dataclass
class ProcessPlan:
    """Records a complete subtractive manufacturing process plan.

    Every operation in the SubCAD pipeline appends itself to this plan.
    The plan can be serialized to JSON for hand-off to a machinist or
    downstream CAM software.
    """

    material: str = ""
    stock_dimensions: dict = field(default_factory=dict)  # {"length": 100, "width": 50, "height": 20}
    operations: list[dict] = field(default_factory=list)
    tools_used: list[dict] = field(default_factory=list)

    # Fixturing / setup metadata
    fixture: Optional[dict] = None           # serialized FixtureSpec
    setups: dict = field(default_factory=dict)  # setup_name -> serialized Setup
    work_offsets: dict = field(default_factory=dict)  # e.g. {"G54": [300, 200, 50, 0, 0, 0]}

    # ------------------------------------------------------------------
    # Derived properties
    # ------------------------------------------------------------------

    @property
    def total_operations(self) -> int:
        """Return the total number of operations in the plan."""
        return len(self.operations)

    @property
    def estimated_time_minutes(self) -> float:
        """Estimate machining time from feeds/speeds and approximate toolpath lengths.

        Simple model:
          - For each operation, if a feed rate is present in feeds_speeds,
            estimate toolpath length from the feature dimensions in the op dict
            and compute time = length / feed_rate.
          - If no feed rate data is available, fall back to 2 min per op.
        """
        total = 0.0
        for op in self.operations:
            feeds = op.get("feeds_speeds")
            if feeds and feeds.get("feed_rate_mm_per_min"):
                feed_rate = feeds["feed_rate_mm_per_min"]
                # Approximate toolpath length from op dimensions
                dims = op.get("dimensions", {})
                length = float(dims.get("length", 0))
                width = float(dims.get("width", 0))
                depth_pass = float(dims.get("depth", 0))
                # Simple perimeter-based estimate: 2*(L+W) per depth pass
                if length > 0 and width > 0:
                    perimeter = 2 * (length + width)
                    # Estimate number of passes from depth
                    step_down = feeds.get("step_down_mm", 1.0)
                    passes = max(1.0, depth_pass / step_down) if step_down > 0 else 1.0
                    toolpath_approx = perimeter * passes
                    total += toolpath_approx / feed_rate
                else:
                    total += 2.0  # fallback when dims are unavailable
            else:
                total += 2.0  # default 2 min per op
        return round(total, 2)

    @property
    def tool_change_count(self) -> int:
        """Count unique tool changes (when tool type or diameter changes between ops)."""
        changes = 0
        prev_key = None
        for op in self.operations:
            tool_type = op.get("tool_type", "")
            tool_dia = op.get("tool_diameter_mm", 0)
            cur_key = (tool_type, tool_dia)
            if prev_key is not None and cur_key != prev_key:
                changes += 1
            prev_key = cur_key
        return changes

    # ------------------------------------------------------------------
    # Mutators
    # ------------------------------------------------------------------

    def add_operation(self, op_dict: dict) -> None:
        """Add an operation to the plan and track its tool."""
        self.operations.append(op_dict)
        # Register the tool if it hasn't been recorded yet
        tool_type = op_dict.get("tool_type", "")
        tool_dia = op_dict.get("tool_diameter_mm", 0)
        already_tracked = any(
            t.get("tool_type") == tool_type and t.get("tool_diameter_mm") == tool_dia
            for t in self.tools_used
        )
        if not already_tracked and tool_type:
            self.tools_used.append({
                "tool_type": tool_type,
                "tool_diameter_mm": tool_dia,
            })

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """Return a full serializable dict representation of the plan."""
        return {
            "material": self.material,
            "stock_dimensions": self.stock_dimensions,
            "total_operations": self.total_operations,
            "estimated_time_minutes": self.estimated_time_minutes,
            "tool_change_count": self.tool_change_count,
            "tools_used": self.tools_used,
            "operations": self.operations,
            "fixture": self.fixture,
            "setups": self.setups,
            "work_offsets": self.work_offsets,
        }

    def to_json(self, indent: int = 2) -> str:
        """Serialize to a JSON string."""
        return json.dumps(self.to_dict(), indent=indent)

    def save(self, path: str) -> None:
        """Save the plan as a JSON file to *path*."""
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(self.to_json())

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------

    def summary(self) -> str:
        """Return a human-readable summary listing operations in order."""
        lines = [
            f"ProcessPlan: {self.total_operations} operation(s) on {self.material or 'unspecified'} stock",
            f"  Estimated time: {self.estimated_time_minutes} min",
            f"  Tool changes:   {self.tool_change_count}",
            f"  Unique tools:   {len(self.tools_used)}",
        ]
        if self.fixture:
            lines.append(f"  Fixture:        {self.fixture.get('name', '?')}"
                         f" ({self.fixture.get('fixture_type', '?')})")
        if self.setups:
            lines.append("  Setups:")
            for sname, sdata in self.setups.items():
                face = sdata.get("face_selector", "?")
                woff = sdata.get("work_offset", "?")
                desc = sdata.get("description", "")
                lines.append(f"    {sname}: face={face} offset={woff}"
                             + (f" -- {desc}" if desc else ""))
        lines.append("")
        for i, op in enumerate(self.operations, start=1):
            tool = op.get("tool_type", "?")
            dia = op.get("tool_diameter_mm", "?")
            name = op.get("operation", "?")
            notes = op.get("notes", "")
            setup = op.get("setup", "")
            face = op.get("face_selector", "")
            extra = []
            if setup:
                extra.append(setup)
            if face and face != ">Z":
                extra.append(f"face={face}")
            if notes:
                extra.append(notes)
            suffix = " -- " + ", ".join(extra) if extra else ""
            lines.append(f"  {i}. [{tool} D={dia}mm] {name}{suffix}")
        return "\n".join(lines)


# ======================================================================
# Self-test – runs when the module is executed directly
# ======================================================================
if __name__ == "__main__":
    import sys

    passed = 0
    failed = 0

    def check(condition, label):
        global passed, failed
        if condition:
            passed += 1
            print(f"  PASS  {label}")
        else:
            failed += 1
            print(f"  FAIL  {label}")

    print("=== ProcessPlan self-tests ===\n")

    # --- Create a ProcessPlan and add operations ---
    plan = ProcessPlan(
        material="6061-T6 Aluminum",
        stock_dimensions={"length": 100, "width": 50, "height": 20},
    )

    plan.add_operation({
        "operation": "face_mill",
        "tool_type": "face_mill",
        "tool_diameter_mm": 50.0,
        "dimensions": {"length": 100, "width": 50, "depth": 1.0},
        "feeds_speeds": {"feed_rate_mm_per_min": 500, "step_down_mm": 1.0},
        "notes": "Face top surface",
    })

    plan.add_operation({
        "operation": "rough_pocket",
        "tool_type": "end_mill",
        "tool_diameter_mm": 10.0,
        "dimensions": {"length": 60, "width": 30, "depth": 10.0},
        "feeds_speeds": {"feed_rate_mm_per_min": 300, "step_down_mm": 2.0},
        "notes": "Rough pocket",
    })

    plan.add_operation({
        "operation": "drill",
        "tool_type": "drill",
        "tool_diameter_mm": 6.0,
        "notes": "Drill mounting holes",
    })

    print("1. Plan construction and add_operation")
    check(plan.total_operations == 3, "total_operations == 3")
    check(len(plan.tools_used) == 3, "3 unique tools tracked")
    print()

    # --- to_dict ---
    d = plan.to_dict()
    print("2. to_dict")
    check(isinstance(d, dict), "to_dict returns dict")
    check(d["material"] == "6061-T6 Aluminum", "material preserved")
    check(d["total_operations"] == 3, "total_operations in dict")
    check("operations" in d, "operations key present")
    check("tools_used" in d, "tools_used key present")
    check("estimated_time_minutes" in d, "estimated_time_minutes key present")
    check("tool_change_count" in d, "tool_change_count key present")
    print()

    # --- to_json ---
    json_str = plan.to_json()
    print("3. to_json")
    check(isinstance(json_str, str), "to_json returns str")
    parsed = json.loads(json_str)
    check(isinstance(parsed, dict), "to_json produces valid JSON")
    check(parsed["total_operations"] == 3, "JSON round-trips total_operations")
    print()

    # --- estimated_time_minutes ---
    est = plan.estimated_time_minutes
    print("4. estimated_time_minutes")
    check(isinstance(est, (int, float)) and est > 0, f"estimated_time > 0 (got {est})")
    # First op: perimeter=300, passes=1, time=300/500=0.6
    # Second op: perimeter=180, passes=5, toolpath=900, time=900/300=3.0
    # Third op: no feed data -> 2.0 fallback
    # Total = 0.6 + 3.0 + 2.0 = 5.6
    check(abs(est - 5.6) < 0.01, f"estimated_time ~ 5.6 (got {est})")
    print()

    # --- tool_change_count ---
    print("5. tool_change_count")
    # face_mill/50 -> end_mill/10  (change)
    # end_mill/10  -> drill/6      (change)
    # = 2 changes
    check(plan.tool_change_count == 2, f"tool_change_count == 2 (got {plan.tool_change_count})")
    print()

    # --- save ---
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as tmp:
        tmp_path = tmp.name
    try:
        plan.save(tmp_path)
        with open(tmp_path, "r", encoding="utf-8") as fh:
            reloaded = json.load(fh)
        print("6. save")
        check(isinstance(reloaded, dict), "save writes valid JSON")
        check(reloaded["material"] == "6061-T6 Aluminum", "save preserves material")
        check(reloaded["total_operations"] == 3, "save preserves total_operations")
    finally:
        import os
        os.unlink(tmp_path)
    print()

    # --- summary ---
    print("7. summary (human-readable output)")
    print(plan.summary())
    print()

    # --- OperationStep ---
    print("8. OperationStep")
    step = OperationStep(
        sequence_number=1,
        operation="face_mill",
        tool_type="face_mill",
        tool_diameter_mm=50.0,
        depth_mm=1.0,
        position=(0, 0),
        feeds_speeds={"rpm": 3000, "feed_rate_mm_per_min": 500},
        notes="Face top surface",
    )
    sd = step.to_dict()
    check(sd["sequence_number"] == 1, "OperationStep sequence_number")
    check(sd["operation"] == "face_mill", "OperationStep operation")
    check(sd["position"] == [0, 0], "OperationStep position serialized as list")
    check("feeds_speeds" in sd, "OperationStep feeds_speeds present")
    print()

    # --- Report ---
    print(f"=== Results: {passed} passed, {failed} failed ===")
    sys.exit(0 if failed == 0 else 1)
