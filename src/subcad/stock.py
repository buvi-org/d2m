"""SubCAD Stock class -- the main fluent entry point.

The Stock class wraps a CadQuery B-Rep shape, a material key, and an
accumulating ProcessPlan. Every machining operation returns a new Stock
instance (immutable pattern, like CadQuery), so chains are composable.

Usage:
    part = (Stock.rectangular(100, 50, 20, material="aluminum_6061")
        .face_mill(depth=1.0)
        .pocket(width=30, length=20, depth=5, corner_radius=2)
        .drill(diameter=6, cx=25, cy=10, depth=15)
        .chamfer(width=0.5)
    )
    part.to_step("output.step")
    print(part.process_plan())
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Tuple

from .geometry import (
    create_rectangular_stock,
    create_cylindrical_stock,
    export_step,
    export_stl,
    to_mesh,
    compute_bounding_box,
    compute_volume,
    import_step,
    _HAS_CADQUERY,
)
from .process_plan import ProcessPlan
from .tool_library import ToolSpec


@dataclass
class Stock:
    """An in-process workpiece with an accumulating manufacturing plan.

    Create instances via factory constructors:
      - Stock.rectangular(length, width, height, material)
      - Stock.cylindrical(diameter, height, material)
      - Stock.from_step(path, material)

    Each machining method returns a **new** Stock, so chains are safe:
        s2 = s1.face_mill(1.0).pocket(30, 20, 5)
        # s1 is unchanged, s2 has both operations applied.
    """

    _shape: object                # CadQuery Workplane / Solid
    _material: str                # e.g. "aluminum_6061"
    _plan: ProcessPlan = field(default_factory=ProcessPlan)
    _stock_dims: dict = field(default_factory=dict)
    _next_op_number: int = 1

    # -------------------------------------------------------------------
    #  Internal helpers
    # -------------------------------------------------------------------

    @classmethod
    def _from_parts(
        cls,
        shape: object,
        material: str,
        stock_dims: dict,
        plan: ProcessPlan,
        next_op_number: int,
    ) -> "Stock":
        """Construct directly from components."""
        obj = object.__new__(cls)
        obj._shape = shape
        obj._material = material
        obj._plan = plan
        obj._stock_dims = stock_dims
        obj._next_op_number = next_op_number
        return obj

    def _apply_op(self, op) -> "Stock":
        """Apply a machining operation: modify shape, record in plan, return new Stock."""
        new_shape = op.apply(self._shape)

        new_plan = ProcessPlan(
            material=self._material,
            stock_dimensions=dict(self._stock_dims),
            operations=list(self._plan.operations),
            tools_used=list(self._plan.tools_used),
        )
        new_plan.add_operation(op.to_dict())

        return Stock._from_parts(
            new_shape,
            self._material,
            self._stock_dims,
            new_plan,
            self._next_op_number + 1,
        )

    # -------------------------------------------------------------------
    #  Factory constructors
    # -------------------------------------------------------------------

    @classmethod
    def rectangular(
        cls,
        length: float,
        width: float,
        height: float,
        material: str = "aluminum_6061",
    ) -> "Stock":
        """Create rectangular prismatic stock.

        Args:
            length: X-axis dimension (mm).
            width:  Y-axis dimension (mm).
            height: Z-axis dimension (mm).
            material: Material key.
        """
        shape = create_rectangular_stock(length, width, height)
        dims = {"length": length, "width": width, "height": height}
        return cls(
            _shape=shape,
            _material=material,
            _plan=ProcessPlan(material=material, stock_dimensions=dims),
            _stock_dims=dims,
        )

    @classmethod
    def cylindrical(
        cls,
        diameter: float,
        height: float,
        material: str = "aluminum_6061",
    ) -> "Stock":
        """Create cylindrical stock from round bar."""
        shape = create_cylindrical_stock(diameter, height)
        dims = {"diameter": diameter, "height": height}
        return cls(
            _shape=shape,
            _material=material,
            _plan=ProcessPlan(material=material, stock_dimensions=dims),
            _stock_dims=dims,
        )

    @classmethod
    def from_step(
        cls,
        path: str,
        material: str = "aluminum_6061",
        stock_oversize: float = 5.0,
    ) -> "Stock":
        """Import a STEP file and wrap in an oversize stock billet."""
        imported = import_step(path)
        bbox = compute_bounding_box(imported)
        stock_l = bbox["length"] + 2 * stock_oversize
        stock_w = bbox["width"] + 2 * stock_oversize
        stock_h = bbox["height"] + stock_oversize

        shape = create_rectangular_stock(stock_l, stock_w, stock_h)
        dims = {"length": stock_l, "width": stock_w, "height": stock_h}
        return cls(
            _shape=shape,
            _material=material,
            _plan=ProcessPlan(material=material, stock_dimensions=dims),
            _stock_dims=dims,
        )

    # -------------------------------------------------------------------
    #  Machining operations  (each returns a new Stock)
    # -------------------------------------------------------------------

    def face_mill(
        self,
        depth: float = 1.0,
        *,
        tool: Optional[ToolSpec] = None,
        stepover: Optional[float] = None,
    ) -> "Stock":
        """Face mill the top surface.

        Args:
            depth: Material to remove from top face (mm).
            tool: ToolSpec or None (auto-selects).
            stepover: Radial engagement per pass (default 0.7 * tool_dia).
        """
        from .operations import FaceMillOp

        op = FaceMillOp(
            depth=depth,
            stepover=stepover,
            tool=tool,
            material=self._material,
        )
        op.sequence_number = self._next_op_number
        return self._apply_op(op)

    def pocket(
        self,
        width: float,
        length: float,
        depth: float,
        *,
        corner_radius: float = 0.0,
        cx: float = 0.0,
        cy: float = 0.0,
        tool: Optional[ToolSpec] = None,
    ) -> "Stock":
        """Cut a rectangular pocket.

        If corner_radius < tool.radius, a finish pass is automatically added.

        Args:
            width: Pocket width along Y (mm).
            length: Pocket length along X (mm).
            depth: Total pocket depth (mm).
            corner_radius: Internal corner radius (mm).
            cx, cy: Center position on top face (mm).
            tool: ToolSpec or None (auto-selects ~80% of width).
        """
        from .operations import PocketOp

        op = PocketOp(
            cx=cx,
            cy=cy,
            width=width,
            length=length,
            depth=depth,
            corner_radius=corner_radius,
            tool=tool,
            material=self._material,
        )
        op.sequence_number = self._next_op_number
        result = self._apply_op(op)

        # If PocketOp auto-created a finish op, apply it too
        finish = getattr(op, "finish_op", None)
        if finish is not None:
            finish.sequence_number = result._next_op_number
            result = result._apply_op(finish)

        return result

    def circular_pocket(
        self,
        diameter: float,
        depth: float,
        *,
        cx: float = 0.0,
        cy: float = 0.0,
        tool: Optional[ToolSpec] = None,
    ) -> "Stock":
        """Cut a circular pocket.

        Args:
            diameter: Pocket diameter (mm).
            depth: Total depth (mm).
            cx, cy: Center position on top face (mm).
            tool: ToolSpec or None.
        """
        from .operations import CircularPocketOp

        op = CircularPocketOp(
            cx=cx,
            cy=cy,
            diameter=diameter,
            depth=depth,
            tool=tool,
            material=self._material,
        )
        op.sequence_number = self._next_op_number
        return self._apply_op(op)

    def drill(
        self,
        diameter: float,
        depth: float = 0.0,
        *,
        cx: float = 0.0,
        cy: float = 0.0,
        through: bool = False,
        spot_drill: bool = True,
        peck: bool = False,
        tool: Optional[ToolSpec] = None,
    ) -> "Stock":
        """Drill a hole.

        Args:
            diameter: Hole diameter (mm).
            depth: Hole depth (mm). Ignored if through=True.
            cx, cy: Center position on top face (mm).
            through: If True, drill through entire part.
            spot_drill: If True, auto-add spot-drill first.
            peck: If True, use peck drilling cycle.
            tool: ToolSpec or None.
        """
        from .operations import DrillOp, SpotDrillOp

        result = self

        # Apply spot-drill first so it's recorded in the plan
        if spot_drill:
            spot = SpotDrillOp(
                cx=cx, cy=cy,
                hole_diameter=diameter,
                material=self._material,
            )
            spot.sequence_number = result._next_op_number
            result = result._apply_op(spot)

        # Apply drill (spot_drill=False since spot is already handled above)
        op = DrillOp(
            cx=cx,
            cy=cy,
            diameter=diameter,
            depth=depth,
            through=through,
            spot_drill=False,
            peck=peck,
            tool=tool,
            material=self._material,
        )
        op.sequence_number = result._next_op_number
        return result._apply_op(op)

    def tap(
        self,
        diameter: float,
        thread_pitch: float = 0.0,
        *,
        depth: float = 10.0,
        cx: float = 0.0,
        cy: float = 0.0,
        tool: Optional[ToolSpec] = None,
    ) -> "Stock":
        """Tap a pre-drilled hole.

        Geometry is unchanged (thread form too fine for B-Rep).

        Args:
            diameter: Nominal thread diameter (mm), e.g. 6 for M6.
            thread_pitch: Thread pitch (mm). Auto-derived if 0.
            depth: Tap depth (mm).
            cx, cy: Center position (mm).
            tool: ToolSpec or None.
        """
        from .operations import TapOp

        op = TapOp(
            cx=cx,
            cy=cy,
            diameter=diameter,
            pitch=thread_pitch,
            depth=depth,
            material=self._material,
            tool=tool,
        )
        op.sequence_number = self._next_op_number
        return self._apply_op(op)

    def threaded_hole(
        self,
        diameter: float,
        depth: float = 0.0,
        *,
        cx: float = 0.0,
        cy: float = 0.0,
        through: bool = False,
    ) -> "Stock":
        """Convenience: spot-drill + drill + tap in one call.

        Arg:
            diameter: Nominal thread diameter (mm), e.g. 8 for M8.
            depth: Hole / tap depth (mm). 0 = through.
            cx, cy: Center position (mm).
            through: If True, drill through entire part.
        """
        from .operations import threaded_hole_ops

        ops = threaded_hole_ops(
            diameter=diameter,
            depth=depth,
            position=(cx, cy),
            material=self._material,
            through=through,
        )
        result = self
        for op in ops:
            op.sequence_number = result._next_op_number
            result = result._apply_op(op)
        return result

    def contour(
        self,
        depth: float,
        *,
        tool: Optional[ToolSpec] = None,
        stepdown: Optional[float] = None,
    ) -> "Stock":
        """Profile / contour milling around the outer boundary.

        Args:
            depth: Total depth to profile (mm).
            tool: ToolSpec or None.
            stepdown: Depth per Z-level pass (default 0.3 * tool_dia).
        """
        from .operations import ContourOp

        op = ContourOp(
            depth=depth,
            stepdown=stepdown or 1.0,
            tool=tool,
            material=self._material,
        )
        op.sequence_number = self._next_op_number
        return self._apply_op(op)

    def slot(
        self,
        length: float,
        width: float,
        depth: float = 5.0,
        *,
        angle: float = 0.0,
        cx: float = 0.0,
        cy: float = 0.0,
        through: bool = False,
        tool: Optional[ToolSpec] = None,
    ) -> "Stock":
        """Cut a straight slot (obround).

        Args:
            length: Total slot length (mm).
            width: Slot width (mm).
            depth: Slot depth (mm).
            angle: Rotation angle from X axis (degrees).
            cx, cy: Center position (mm).
            through: If True, cut through entire part.
            tool: ToolSpec or None.
        """
        from .operations import SlotOp

        op = SlotOp(
            cx=cx,
            cy=cy,
            length=length,
            width=width,
            depth=depth,
            angle=angle,
            through=through,
            tool=tool,
            material=self._material,
        )
        op.sequence_number = self._next_op_number
        return self._apply_op(op)

    def chamfer(
        self,
        width: float = 0.5,
        *,
        tool: Optional[ToolSpec] = None,
    ) -> "Stock":
        """Chamfer the top edges.

        Args:
            width: Chamfer width (mm).
            tool: ToolSpec or None.
        """
        from .operations import ChamferOp

        op = ChamferOp(
            width=width,
            tool=tool,
            material=self._material,
        )
        op.sequence_number = self._next_op_number
        return self._apply_op(op)

    # -------------------------------------------------------------------
    #  Output
    # -------------------------------------------------------------------

    def to_step(self, path: str) -> None:
        """Export the current shape to a STEP file."""
        export_step(self._shape, path)

    def to_stl(self, path: str) -> None:
        """Export the current shape to an STL file."""
        export_stl(self._shape, path)

    def to_mesh(self):
        """Convert the current shape to a trimesh.Trimesh."""
        return to_mesh(self._shape)

    def process_plan(self) -> dict:
        """Return the accumulated process plan as a serializable dict."""
        return self._plan.to_dict()

    def save_process_plan(self, path: str) -> None:
        """Save the process plan as a JSON file."""
        self._plan.save(path)

    def plan_summary(self) -> str:
        """Return a human-readable summary of the process plan."""
        return self._plan.summary()

    @property
    def volume(self) -> float:
        """Current volume of the workpiece in mm^3."""
        return compute_volume(self._shape)

    @property
    def bounding_box(self) -> dict:
        """Current bounding box of the workpiece."""
        return compute_bounding_box(self._shape)

    @property
    def material(self) -> str:
        """Workpiece material key."""
        return self._material

    def __repr__(self) -> str:
        bbox = self.bounding_box
        ops = self._plan.total_operations
        return (
            f"Stock(material={self._material!r}, "
            f"dims={bbox.get('length', 0):.0f}x{bbox.get('width', 0):.0f}x{bbox.get('height', 0):.0f} mm, "
            f"ops={ops}, volume={self.volume:.0f} mm^3)"
        )


# =============================================================================
#  Self-test
# =============================================================================

if __name__ == "__main__":
    print("=== Stock Self-Test ===\n")

    if not _HAS_CADQUERY:
        print("SKIP: cadquery not installed. Tests require cadquery.")
        exit(0)

    import tempfile
    import os

    passed = 0
    failed = 0

    def _check(label: str, condition: bool, detail: str = ""):
        global passed, failed
        if condition:
            passed += 1
            print(f"  PASS  {label}")
        else:
            failed += 1
            print(f"  FAIL  {label}  -- {detail}")

    # ------------------------------------------------------------------
    # 1. Factory constructors
    # ------------------------------------------------------------------
    print("1. Factory constructors ...")

    s1 = Stock.rectangular(100, 50, 20, material="aluminum_6061")
    _check("rectangular stock created", s1 is not None)
    _check("material", s1._material == "aluminum_6061")
    _check("plan has 0 ops", s1._plan.total_operations == 0)

    bb = s1.bounding_box
    _check("bbox length ~100", abs(bb["length"] - 100.0) < 1.0)
    _check("bbox width ~50", abs(bb["width"] - 50.0) < 1.0)
    _check("bbox height ~20", abs(bb["height"] - 20.0) < 1.0)

    vol_before = s1.volume
    _check("volume > 0", vol_before > 0, f"got {vol_before}")

    s_cyl = Stock.cylindrical(50, 30, "steel_4140")
    _check("cylindrical stock", s_cyl is not None)
    _check("cyl material", s_cyl._material == "steel_4140")
    print()

    # ------------------------------------------------------------------
    # 2. Face mill
    # ------------------------------------------------------------------
    print("2. Face mill ...")

    s2 = s1.face_mill(depth=1.0)
    _check("returns Stock", isinstance(s2, Stock))
    _check("immutable (s1 unchanged)",
           s1._plan.total_operations == 0 and s2._plan.total_operations == 1)
    _check("volume decreased", s2.volume < s1.volume,
           f"s1={s1.volume:.0f}, s2={s2.volume:.0f}")

    ops = s2.process_plan()["operations"]
    _check("recorded as face_mill", ops[0]["operation"] == "face_mill")
    _check("depth 1.0", abs(ops[0].get("depth_mm", 0) - 1.0) < 0.01)
    _check("feeds_speeds present", ops[0].get("feeds_speeds") is not None)
    print()

    # ------------------------------------------------------------------
    # 3. Pocket
    # ------------------------------------------------------------------
    print("3. Pocket ...")

    s3 = s2.pocket(width=30, length=20, depth=5, corner_radius=0)
    _check("returns Stock", isinstance(s3, Stock))
    _check("2 ops total", s3._plan.total_operations == 2)
    _check("volume decreased", s3.volume < s2.volume)

    pk_ops = [o for o in s3.process_plan()["operations"]
              if o["operation"] == "rough_pocket"]
    _check("recorded as rough_pocket", len(pk_ops) == 1,
           f"got {[o['operation'] for o in s3.process_plan()['operations']]}")
    print()

    # ------------------------------------------------------------------
    # 4. Drill
    # ------------------------------------------------------------------
    print("4. Drill ...")

    s4 = s3.drill(diameter=6, cx=25, cy=10, depth=15, spot_drill=False)
    _check("returns Stock", isinstance(s4, Stock))
    _check("3 ops total", s4._plan.total_operations == 3)

    drill_ops = [o for o in s4.process_plan()["operations"]
                 if o["operation"] == "drill"]
    _check("recorded in plan", len(drill_ops) == 1)
    _check("volume decreased", s4.volume < s3.volume)
    print()

    # ------------------------------------------------------------------
    # 5. Chamfer
    # ------------------------------------------------------------------
    print("5. Chamfer ...")

    s5 = s4.chamfer(width=0.5)
    _check("returns Stock", isinstance(s5, Stock))
    _check("4 ops total", s5._plan.total_operations == 4)

    chamfer_ops = [o for o in s5.process_plan()["operations"]
                   if o["operation"] == "chamfer"]
    _check("recorded in plan", len(chamfer_ops) == 1)
    print()

    # ------------------------------------------------------------------
    # 6. Threaded hole (compound)
    # ------------------------------------------------------------------
    print("6. Threaded hole ...")

    s6 = s2.threaded_hole(diameter=6, depth=12, cx=15, cy=15)
    _check("returns Stock", isinstance(s6, Stock))
    _check("spot+drill+tap = +3 ops",
           s6._plan.total_operations == s2._plan.total_operations + 3,
           f"expected {s2._plan.total_operations + 3}, got {s6._plan.total_operations}")

    th_ops = s6.process_plan()["operations"][-3:]
    th_names = [o["operation"] for o in th_ops]
    _check("spot_drill first", th_names[0] == "spot_drill", f"got {th_names}")
    _check("drill second", th_names[1] == "drill", f"got {th_names}")
    _check("tap third", th_names[2] == "tap", f"got {th_names}")
    print()

    # ------------------------------------------------------------------
    # 7. Full chain
    # ------------------------------------------------------------------
    print("7. Full chain ...")

    s_full = (Stock.rectangular(100, 50, 20, material="aluminum_6061")
        .face_mill(depth=1.0)
        .pocket(width=30, length=20, depth=5, corner_radius=2)
        .drill(diameter=6, cx=25, cy=10, depth=15)
        .chamfer(width=0.5)
    )
    _check("5+ ops", s_full._plan.total_operations >= 5,
           f"got {s_full._plan.total_operations}")
    _check("volume < original", s_full.volume < s1.volume)
    _check("process_plan returns dict", isinstance(s_full.process_plan(), dict))
    _check("plan has operations", "operations" in s_full.process_plan())
    print()

    # ------------------------------------------------------------------
    # 8. Immutability
    # ------------------------------------------------------------------
    print("8. Immutability ...")

    s_a = Stock.rectangular(50, 50, 10)
    s_b = s_a.face_mill(1.0)
    s_c = s_b.pocket(20, 20, 3)

    _check("s_a unchanged", s_a._plan.total_operations == 0)
    _check("s_b unchanged", s_b._plan.total_operations == 1)
    _check("s_c has both", s_c._plan.total_operations == 2)
    print()

    # ------------------------------------------------------------------
    # 9. Export
    # ------------------------------------------------------------------
    print("9. Export ...")

    tmp_step = tempfile.NamedTemporaryFile(suffix=".step", delete=False)
    tmp_step_path = tmp_step.name
    tmp_step.close()
    try:
        s_full.to_step(tmp_step_path)
        size = os.path.getsize(tmp_step_path)
        _check(f"STEP export: {size} bytes", size > 100)
    finally:
        os.unlink(tmp_step_path)

    tmp_json = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
    tmp_json_path = tmp_json.name
    tmp_json.close()
    try:
        s_full.save_process_plan(tmp_json_path)
        size = os.path.getsize(tmp_json_path)
        _check(f"Plan JSON export: {size} bytes", size > 100)
    finally:
        os.unlink(tmp_json_path)

    _check("plan_summary returns str", isinstance(s_full.plan_summary(), str))
    _check("plan_summary non-empty", len(s_full.plan_summary()) > 0)
    _check("__repr__ works", "Stock(" in repr(s_full))
    print()

    # ------------------------------------------------------------------
    # 10. Contour and slot
    # ------------------------------------------------------------------
    print("10. Contour and slot ...")

    s10 = Stock.rectangular(80, 60, 20)
    s10 = s10.contour(depth=5, stepdown=2.0)
    _check("contour: 1 op", s10._plan.total_operations == 1)

    s10 = s10.slot(length=30, width=6, depth=5, cx=10, cy=0)
    _check("slot: 2 ops", s10._plan.total_operations == 2)
    print()

    # ------------------------------------------------------------------
    # 11. from_step
    # ------------------------------------------------------------------
    print("11. from_step ...")

    tmp_step2 = tempfile.NamedTemporaryFile(suffix=".step", delete=False)
    tmp_step2_path = tmp_step2.name
    tmp_step2.close()
    try:
        s_full.to_step(tmp_step2_path)
        s_from = Stock.from_step(tmp_step2_path, material="steel_304", stock_oversize=5.0)
        _check("from_step creates Stock", isinstance(s_from, Stock))
        _check("material is steel_304", s_from._material == "steel_304")
        _check("stock larger than target", s_from.volume > s_full.volume)
    finally:
        os.unlink(tmp_step2_path)
    print()

    # ==================================================================
    #  Summary
    # ==================================================================
    total = passed + failed
    print(f"=== {'ALL TESTS PASSED' if failed == 0 else 'SOME TESTS FAILED'} "
          f"({passed}/{total} passed) ===")
    if failed > 0:
        exit(1)
