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
    _fixture: Optional["FixtureSpec"] = None
    _setups: dict = field(default_factory=dict)  # name -> Setup
    _active_setup: Optional[str] = None
    _state_history: list = field(default_factory=list)

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
        fixture=None,
        setups=None,
        active_setup=None,
        state_history=None,
    ) -> "Stock":
        """Construct directly from components."""
        obj = object.__new__(cls)
        obj._shape = shape
        obj._material = material
        obj._plan = plan
        obj._stock_dims = stock_dims
        obj._next_op_number = next_op_number
        obj._fixture = fixture
        obj._setups = setups if setups is not None else {}
        obj._active_setup = active_setup
        obj._state_history = state_history if state_history is not None else []
        return obj

    def _apply_op(self, op) -> "Stock":
        """Apply a machining operation: modify shape, record in plan, return new Stock."""
        if getattr(op, "sequence_number", 0) == 0:
            op.sequence_number = self._next_op_number

        # Look up active setup and apply its face_selector to the operation
        active_setup = self._active_setup
        if active_setup is not None and active_setup in self._setups:
            setup = self._setups[active_setup]
            if hasattr(op, "face_selector"):
                op.face_selector = setup.face_selector

        new_shape = op.apply(self._shape)
        state_history = list(self._state_history)
        if not state_history:
            state_history.append({
                "sequence_number": 0,
                "operation": "initial_stock",
                "label": "Initial stock",
                "shape": self._shape,
            })
        state_history.append({
            "sequence_number": op.sequence_number,
            "operation": getattr(op, "operation_name", op.__class__.__name__),
            "label": f"After OP {op.sequence_number}",
            "shape": new_shape,
        })

        # Serialize fixture and setups for the plan
        fixture_dict = self._fixture.to_dict() if self._fixture else None
        setups_dict = {name: s.to_dict() for name, s in self._setups.items()}
        work_offsets_dict = {}
        for name, s in self._setups.items():
            wo = getattr(s, "work_offset", "G54")
            wov = getattr(s, "work_offset_values", (0.0, 0.0, 0.0, 0.0, 0.0, 0.0))
            work_offsets_dict[wo] = list(wov)

        new_plan = ProcessPlan(
            material=self._material,
            stock_dimensions=dict(self._stock_dims),
            operations=list(self._plan.operations),
            tools_used=list(self._plan.tools_used),
            fixture=fixture_dict,
            setups=setups_dict,
            work_offsets=work_offsets_dict,
        )

        op_dict = op.to_dict()
        op_dict["sequence_number"] = op.sequence_number

        if hasattr(op, "to_toolpath"):
            try:
                toolpath = op.to_toolpath()
            except Exception:
                toolpath = []
            if toolpath:
                serialized_toolpath = _serialize_toolpath(toolpath)
                if serialized_toolpath:
                    op_dict["toolpath"] = serialized_toolpath

        # Attach setup and face_selector info to the op record
        if active_setup is not None and active_setup in self._setups:
            op_dict["setup"] = active_setup
            op_dict["face_selector"] = self._setups[active_setup].face_selector

        new_plan.add_operation(op_dict)

        return Stock._from_parts(
            new_shape,
            self._material,
            self._stock_dims,
            new_plan,
            self._next_op_number + 1,
            fixture=self._fixture,
            setups=dict(self._setups),
            active_setup=self._active_setup,
            state_history=state_history,
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

    def peck_drill(
        self,
        diameter: float,
        depth: float = 20.0,
        *,
        cx: float = 0.0,
        cy: float = 0.0,
        peck_step: float = 2.0,
        through: bool = False,
        tool: Optional[ToolSpec] = None,
    ) -> "Stock":
        """Peck-drill a deep hole."""
        from .operations import PeckDrillOp

        op = PeckDrillOp(
            cx=cx,
            cy=cy,
            diameter=diameter,
            depth=depth,
            peck_step=peck_step,
            through=through,
            tool=tool,
            material=self._material,
        )
        return self._apply_op(op)

    def ream(
        self,
        diameter: float,
        depth: float = 10.0,
        *,
        cx: float = 0.0,
        cy: float = 0.0,
        through: bool = False,
        tool: Optional[ToolSpec] = None,
    ) -> "Stock":
        """Finish a pre-drilled hole with a reamer."""
        from .operations import ReamOp

        op = ReamOp(
            cx=cx,
            cy=cy,
            diameter=diameter,
            depth=depth,
            through=through,
            tool=tool,
            material=self._material,
        )
        return self._apply_op(op)

    def bore(
        self,
        diameter: float,
        depth: float = 10.0,
        *,
        cx: float = 0.0,
        cy: float = 0.0,
        through: bool = False,
        tool: Optional[ToolSpec] = None,
    ) -> "Stock":
        """Bore a hole for trueness and finish."""
        from .operations import BoreOp

        op = BoreOp(
            cx=cx,
            cy=cy,
            diameter=diameter,
            depth=depth,
            through=through,
            tool=tool,
            material=self._material,
        )
        return self._apply_op(op)

    def countersink(
        self,
        diameter: float,
        countersink_diameter: float,
        *,
        depth: float = 0.0,
        countersink_angle: float = 82.0,
        cx: float = 0.0,
        cy: float = 0.0,
        tool: Optional[ToolSpec] = None,
    ) -> "Stock":
        """Cut a countersunk hole."""
        from .operations import CountersinkOp

        op = CountersinkOp(
            cx=cx,
            cy=cy,
            diameter=diameter,
            countersink_diameter=countersink_diameter,
            depth=depth,
            countersink_angle=countersink_angle,
            tool=tool,
            material=self._material,
        )
        return self._apply_op(op)

    def counterbore(
        self,
        hole_diameter: float,
        counterbore_diameter: float,
        counterbore_depth: float,
        *,
        cx: float = 0.0,
        cy: float = 0.0,
        through: bool = False,
        tool: Optional[ToolSpec] = None,
    ) -> "Stock":
        """Cut a flat-bottom counterbore."""
        from .operations import CounterboreOp

        op = CounterboreOp(
            cx=cx,
            cy=cy,
            hole_diameter=hole_diameter,
            counterbore_diameter=counterbore_diameter,
            counterbore_depth=counterbore_depth,
            through=through,
            tool=tool,
            material=self._material,
        )
        return self._apply_op(op)

    def thread_mill(
        self,
        diameter: float,
        depth: float = 10.0,
        *,
        pitch: float = 0.0,
        cx: float = 0.0,
        cy: float = 0.0,
        through: bool = False,
        tool: Optional[ToolSpec] = None,
    ) -> "Stock":
        """Thread-mill an internal thread."""
        from .operations import ThreadMillOp

        op = ThreadMillOp(
            cx=cx,
            cy=cy,
            diameter=diameter,
            pitch=pitch,
            depth=depth,
            through=through,
            tool=tool,
            material=self._material,
        )
        return self._apply_op(op)

    def t_slot(
        self,
        length: float,
        width: float,
        depth: float = 8.0,
        *,
        angle: float = 0.0,
        cx: float = 0.0,
        cy: float = 0.0,
        tool: Optional[ToolSpec] = None,
    ) -> "Stock":
        """Cut a T-slot, approximated as a rectangular slot."""
        from .operations import TSlotOp

        op = TSlotOp(
            cx=cx,
            cy=cy,
            length=length,
            width=width,
            depth=depth,
            angle=angle,
            tool=tool,
            material=self._material,
        )
        return self._apply_op(op)

    def dovetail(
        self,
        length: float,
        width: float,
        depth: float = 5.0,
        *,
        angle: float = 45.0,
        cx: float = 0.0,
        cy: float = 0.0,
        tool: Optional[ToolSpec] = None,
    ) -> "Stock":
        """Cut a dovetail slot."""
        from .operations import DovetailOp

        op = DovetailOp(
            cx=cx,
            cy=cy,
            length=length,
            width=width,
            depth=depth,
            angle=angle,
            tool=tool,
            material=self._material,
        )
        return self._apply_op(op)

    def groove(
        self,
        length: float,
        width: float,
        depth: float = 5.0,
        *,
        angle: float = 0.0,
        cx: float = 0.0,
        cy: float = 0.0,
        tool: Optional[ToolSpec] = None,
    ) -> "Stock":
        """Cut a rectangular groove."""
        from .operations import GrooveOp

        op = GrooveOp(
            cx=cx,
            cy=cy,
            length=length,
            width=width,
            depth=depth,
            angle=angle,
            tool=tool,
            material=self._material,
        )
        return self._apply_op(op)

    def surface_3d(
        self,
        *,
        stepover: float = 1.0,
        depth: float = 0.5,
        tool: Optional[ToolSpec] = None,
    ) -> "Stock":
        """Record a 3D surfacing pass."""
        from .operations import Surface3DOp

        op = Surface3DOp(
            stepover=stepover,
            depth=depth,
            tool=tool,
            material=self._material,
        )
        return self._apply_op(op)

    def deburr(
        self,
        *,
        edge_selection: str = "all",
        tool_diameter: float = 3.0,
        tool: Optional[ToolSpec] = None,
    ) -> "Stock":
        """Deburr edges using a small chamfer proxy."""
        from .operations import DeburrOp

        op = DeburrOp(
            edge_selection=edge_selection,
            tool_diameter=tool_diameter,
            tool=tool,
            material=self._material,
        )
        return self._apply_op(op)

    def spot_face(
        self,
        diameter: float,
        depth: float = 0.5,
        *,
        cx: float = 0.0,
        cy: float = 0.0,
        tool: Optional[ToolSpec] = None,
    ) -> "Stock":
        """Cut a shallow flat spot-face."""
        from .operations import SpotFaceOp

        op = SpotFaceOp(
            cx=cx,
            cy=cy,
            diameter=diameter,
            depth=depth,
            tool=tool,
            material=self._material,
        )
        return self._apply_op(op)

    # -------------------------------------------------------------------
    #  Fixturing API
    # -------------------------------------------------------------------

    def with_fixture(self, fixture_spec: "FixtureSpec") -> "Stock":
        """Attach a FixtureSpec to this Stock. Returns new Stock."""
        return Stock._from_parts(
            self._shape,
            self._material,
            self._stock_dims,
            self._plan,
            self._next_op_number,
            fixture=fixture_spec,
            setups=dict(self._setups),
            active_setup=self._active_setup,
        )

    def new_setup(self, name: str, face_selector: str = ">Z",
                  work_offset: str = "G54",
                  work_offset_values=(0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
                  description: str = "",
                  rotation_deg: float = 0.0) -> "Stock":
        """Define a new machining setup. Requires .with_fixture() to have been called first."""
        from .fixturing import Setup

        if self._fixture is None:
            raise ValueError("No fixture assigned. Call .with_fixture() first.")
        setup = Setup(name=name, fixture=self._fixture, face_selector=face_selector,
                      work_offset=work_offset, work_offset_values=work_offset_values,
                      rotation_deg=rotation_deg, description=description)
        new_setups = dict(self._setups)
        new_setups[name] = setup
        return Stock._from_parts(
            self._shape,
            self._material,
            self._stock_dims,
            self._plan,
            self._next_op_number,
            fixture=self._fixture,
            setups=new_setups,
            active_setup=name,
        )

    def use_setup(self, name: str) -> "Stock":
        """Switch to an existing setup by name."""
        if name not in self._setups:
            raise KeyError(f"Setup {name!r} not found.")
        return Stock._from_parts(
            self._shape,
            self._material,
            self._stock_dims,
            self._plan,
            self._next_op_number,
            fixture=self._fixture,
            setups=dict(self._setups),
            active_setup=name,
        )

    def validate_fixture_clearance(self) -> list[str]:
        """Check all operations against the active fixture's clamping zones."""
        from .fixturing import check_operation_against_fixture

        warnings = []
        active_name = self._active_setup
        if active_name is None or active_name not in self._setups:
            return warnings
        active_setup = self._setups[active_name]
        for op_dict in self._plan.operations:
            warnings.extend(
                check_operation_against_fixture(op_dict, active_setup, self._stock_dims)
            )
        return warnings

    # -------------------------------------------------------------------
    #  Simulation bridge
    # -------------------------------------------------------------------

    def simulate(self, toolpath_precision: float = 0.5) -> dict:
        """Simulate material removal via the tri-dexel engine.

        Returns a dict with:
          - final_volume_mm3
          - volume_removed_mm3
          - gouges: list of gouge descriptors
          - cycle_time_minutes
          - ops_simulated: count of operations that ran through the engine
        """
        try:
            from src.simulation.material_removal import MaterialRemovalEngine
            from src.simulation.tools import create_tool as sim_create_tool
            from src.simulation.tri_dexel import TriDexelModel
            import numpy as np
        except ImportError:
            # Fallback: try without the src. prefix (if running from within src/)
            try:
                from simulation.material_removal import MaterialRemovalEngine
                from simulation.tools import create_tool as sim_create_tool
                from simulation.tri_dexel import TriDexelModel
                import numpy as np
            except ImportError as e:
                return {"error": f"Simulation not available: {e}"}

        # 1. Build initial tri-dexel grid from stock mesh
        mesh = self.to_mesh()
        if mesh is None:
            return {"error": "Cannot create mesh from shape."}

        bbox = self.bounding_box
        dexel_resolution = float(toolpath_precision)  # mm per dexel

        # Create TriDexelModel from the mesh, then the MaterialRemovalEngine
        tri_model = TriDexelModel.from_mesh(mesh, resolution=dexel_resolution)
        engine = MaterialRemovalEngine(
            tri_dexel=tri_model,
            linear_resolution=dexel_resolution,
        )
        initial_volume = engine.tri_dexel.volume()

        # Tool-type mapping: SubCAD tool_type -> simulation create_tool key
        _TOOL_TYPE_MAP = {
            "flat_endmill": "flat_endmill",
            "ball_endmill": "ball_endmill",
            "drill": "drill",
            "chamfer": "chamfer",
            "thread_mill": "thread_mill",
            "dovetail": "dovetail",
            "end_mill": "flat_endmill",       # alias
            "face_mill": "flat_endmill",      # alias
            "spot_drill": "drill",            # alias
        }

        # 2. Replay each operation's toolpath
        gouges = []
        ops_simulated = 0
        for op_dict in self._plan.operations:
            op_tool_type = op_dict.get("tool_type", "flat_endmill")
            op_tool_dia = op_dict.get("tool_diameter_mm", 10.0)

            # Map SubCAD tool type to simulation tool type
            sim_tool_key = _TOOL_TYPE_MAP.get(op_tool_type, None)
            if sim_tool_key is None:
                # Unknown tool type - skip with a warning-level note
                gouges.append({
                    "operation": op_dict.get("operation", "unknown"),
                    "message": f"Skipped: unknown tool_type={op_tool_type!r}",
                })
                continue

            try:
                sim_tool = sim_create_tool(sim_tool_key, diameter=float(op_tool_dia))
            except (TypeError, ValueError) as e:
                gouges.append({
                    "operation": op_dict.get("operation", "unknown"),
                    "message": f"Tool creation failed: {e}",
                })
                continue

            # Prefer operation-provided toolpath data when available.
            toolpath_data = op_dict.get("toolpath")
            toolpath = (
                _toolpath_from_serialized(toolpath_data)
                if toolpath_data
                else _op_to_simple_toolpath(op_dict, bbox)
            )
            if not toolpath:
                toolpath = _op_to_simple_toolpath(op_dict, bbox)
            for pose in toolpath:
                engine.remove_tool_at_pose(sim_tool, pose)

            ops_simulated += 1

            # Check for gouges (material removed below target)
            if engine.tri_dexel.volume() < 0:
                gouges.append({
                    "operation": op_dict.get("operation", "unknown"),
                    "message": "Gouge detected -- volume went below zero",
                })

        final_volume = max(0.0, engine.tri_dexel.volume())
        return {
            "final_volume_mm3": round(final_volume, 1),
            "volume_removed_mm3": round(initial_volume - final_volume, 1),
            "gouges": gouges,
            "cycle_time_minutes": self._plan.estimated_time_minutes,
            "ops_simulated": ops_simulated,
        }

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

    def setup_sheet(self) -> dict:
        """Return a shop-floor setup sheet dictionary."""
        return self._plan.setup_sheet_dict()

    def to_setup_sheet(self, path: Optional[str] = None):
        """Return or save a shop-floor setup sheet.

        If *path* is provided, writes JSON to that path and returns the sheet
        dict. Without *path*, returns the sheet dict directly.
        """
        sheet = self._plan.setup_sheet_dict()
        if path:
            import json

            with open(path, "w", encoding="utf-8") as fh:
                json.dump(sheet, fh, indent=2)
        return sheet

    def save_setup_sheet(self, path: str) -> dict:
        """Save the setup sheet JSON to *path* and return the sheet dict."""
        return self.to_setup_sheet(path)

    def export_setup_sheet(self, path: str) -> dict:
        """Compatibility alias for save_setup_sheet."""
        return self.save_setup_sheet(path)

    def setup_sheet_markdown(self) -> str:
        """Return a Markdown setup sheet."""
        return self._plan.setup_sheet_markdown()

    def gcode_preview(self) -> str:
        """Return preview-only G-code-like text from neutral toolpaths."""
        return self._plan.gcode_preview()

    def to_gcode_preview(self) -> str:
        """Compatibility alias for gcode_preview."""
        return self.gcode_preview()

    def postprocess(
        self,
        controller: str = "generic_3axis_debug",
        machine: str = "generic_3axis_mill",
        safe_mode: bool = True,
    ) -> str:
        """Return debug-only postprocessor output from the process plan."""
        return self._plan.postprocess(
            controller=controller,
            machine=machine,
            safe_mode=safe_mode,
        )

    def compare_to_target(self, target, tolerance_mm: float = 0.25) -> dict:
        """Compare this stock geometry against a target mesh/STEP/STL/Stock."""
        from .target_compare import compare_to_target

        return compare_to_target(self, target, tolerance_mm=tolerance_mm)

    def visualization_package(
        self,
        output_dir: str,
        *,
        target=None,
        tolerance_mm: float = 0.25,
        include_diff_mesh: bool = True,
    ) -> dict:
        """Export browser-friendly visualization assets into a directory."""
        from .visualization import export_visualization_package

        return export_visualization_package(
            self,
            output_dir,
            target=target,
            tolerance_mm=tolerance_mm,
            include_diff_mesh=include_diff_mesh,
        )

    def validate_shop_floor(self, structured: bool = False):
        """Run shop-floor validation against the current process plan."""
        from .validation import validate_all

        return validate_all(
            self._plan.to_dict(),
            self._stock_dims,
            structured=structured,
        )

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
#  Simulation helper (module-level)
# =============================================================================

def _serialize_toolpath(toolpath):
    """Convert operation toolpath objects into JSON-serializable records."""
    if hasattr(toolpath, "to_dict"):
        return toolpath.to_dict()

    serialized = []
    for pose in toolpath:
        if hasattr(pose, "to_dict"):
            serialized.append(pose.to_dict())
            continue

        if isinstance(pose, dict):
            serialized.append(dict(pose))
            continue

        position = getattr(pose, "position", None)
        orientation = getattr(pose, "orientation", None)
        if position is not None and orientation is not None:
            serialized.append({
                "position": list(position),
                "orientation": list(orientation),
            })
            continue

        if isinstance(pose, (list, tuple)) and len(pose) >= 3:
            serialized.append({
                "position": [pose[0], pose[1], pose[2]],
                "orientation": [1.0, 0.0, 0.0, 0.0],
            })

    return serialized


def _toolpath_from_serialized(toolpath_data) -> list:
    """Rehydrate serialized operation toolpath records for simulation."""
    try:
        from src.simulation.kinematics import ToolPose
    except ImportError:
        from simulation.kinematics import ToolPose

    import numpy as np

    if isinstance(toolpath_data, dict):
        if "moves" in toolpath_data:
            toolpath_data = toolpath_data["moves"]
        elif "positions" in toolpath_data:
            toolpath_data = toolpath_data["positions"]
        else:
            toolpath_data = [toolpath_data]

    toolpath = []
    for record in toolpath_data:
        if hasattr(record, "position") and hasattr(record, "orientation"):
            toolpath.append(record)
            continue

        if isinstance(record, dict):
            position = record.get("position")
            orientation = record.get("orientation", [1.0, 0.0, 0.0, 0.0])
        elif isinstance(record, (list, tuple)) and len(record) >= 3:
            position = record[:3]
            orientation = [1.0, 0.0, 0.0, 0.0]
        else:
            continue

        if position is None:
            continue

        toolpath.append(ToolPose(
            position=np.array(position, dtype=np.float64),
            orientation=np.array(orientation, dtype=np.float64),
        ))

    return toolpath


def _op_to_simple_toolpath(op_dict: dict, bbox: dict) -> list:
    """Generate a minimal toolpath for simulation from an operation dict.

    Returns a list of ToolPose objects in the stock coordinate frame.
    Each pose positions the tool tip at (cx, cy, z) with a vertical
    downward orientation (tool axis = [0, 0, 1] in world, cutting -Z).

    For face_mill and chamfer operations, generates a raster/contour
    pattern across the stock top face.  For pocket/drill/slot operations,
    generates a single plunge at the operation position.
    """
    authored_toolpath = op_dict.get("toolpath")
    if authored_toolpath:
        preferred = _toolpath_from_serialized(authored_toolpath)
        if preferred:
            return preferred

    try:
        from src.simulation.kinematics import ToolPose
    except ImportError:
        from simulation.kinematics import ToolPose

    import numpy as np

    op_type = op_dict.get("operation", "")
    depth = op_dict.get("depth_mm", 0.0)
    pos = op_dict.get("position")
    cx, cy = pos if pos else (0.0, 0.0)
    z_top = bbox.get("z_max", 0.0)

    # Default orientation: tool pointing +Z in world, cutting is -Z
    q_identity = np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float64)

    # Sanity check: depth must be positive
    if depth <= 0.0:
        depth = 1.0

    toolpath: list = []

    if op_type in ("face_mill", "chamfer"):
        # Face mill / chamfer: raster across the top face
        x_min = bbox.get("x_min", 0.0)
        x_max = bbox.get("x_max", 0.0)
        y_min = bbox.get("y_min", 0.0)
        y_max = bbox.get("y_max", 0.0)
        tool_dia = op_dict.get("tool_diameter_mm", 10.0)
        stepover = tool_dia * 0.7

        # Generate raster passes in X with stepover in Y
        steps = max(1, int(depth / 0.5))
        y = y_min
        direction = 1  # alternating
        while y < y_max:
            z = z_top - depth
            toolpath.append(ToolPose(
                position=np.array([x_min, y, z], dtype=np.float64),
                orientation=q_identity.copy(),
            ))
            toolpath.append(ToolPose(
                position=np.array([x_max, y, z], dtype=np.float64),
                orientation=q_identity.copy(),
            ))
            y += stepover
            direction *= -1
    else:
        # Pocket, drill, slot, contour, etc.: plunge at operation position
        steps = max(1, int(depth / 0.5))  # 0.5mm steps
        for i in range(steps):
            z = z_top - (i + 1) * (depth / steps)
            toolpath.append(ToolPose(
                position=np.array([cx, cy, z], dtype=np.float64),
                orientation=q_identity.copy(),
            ))

    return toolpath


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
