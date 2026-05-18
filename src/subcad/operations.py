"""SubCAD operations -- MachiningOperation ABC and Phase 1 concrete operations.

Each machining operation is BOTH a geometry modifier AND a manufacturing
instruction.  Operations modify a CadQuery B-Rep solid AND record themselves
into a ProcessPlan.

Phase 1 concrete operations (8 ops):
    FaceMillOp       -- face milling on top surface
    PocketOp         -- rectangular pocket (rough + optional finish)
    CircularPocketOp -- circular pocket
    DrillOp          -- drilling (with optional spot-drill)
    TapOp            -- thread tapping (geometry unchanged)
    ChamferOp        -- edge chamfering
    ContourOp        -- profile / contour milling
    SlotOp           -- slot milling

Plus the internal SpotDrillOp used by DrillOp when spot_drill=True.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, Tuple

from .geometry import (
    face_mill_cut,
    rectangular_pocket_cut,
    circular_pocket_cut,
    drill_hole,
    countersink_cut,
    slot_cut,
    contour_cut_outer,
    chamfer_edges,
)
from .tool_library import ToolSpec, ToolCatalog
from .material import get_feeds_speeds

# ---------------------------------------------------------------------------
# Tool-type mapping for feeds/speeds lookup
# ---------------------------------------------------------------------------
# ToolSpec.tool_type values (e.g. "flat_endmill") do not always match the
# keys expected by the knowledge-graph feeds/speeds engine (e.g. "end_mill").
# This mapping bridges the two.  An unrecognised type is passed through
# unchanged so that the callee can return its standard error dict.

_TOOL_TYPE_FS_MAP: dict[str, str] = {
    "flat_endmill": "end_mill",
    "ball_endmill": "ball_endmill",
    "drill":        "drill",
    "chamfer":      "chamfer",
    "thread_mill":  "tap",
    "bull_nose":    "end_mill",
    "dovetail":     "end_mill",
    "reamer":       "drill",
    "spot_drill":   "drill",
}


def _resolve_fs_tool_type(tool_type: str) -> str:
    """Map a ToolSpec tool_type to the key expected by get_feeds_speeds."""
    return _TOOL_TYPE_FS_MAP.get(tool_type, tool_type)


def _pick_slot_tool(slot_width: float) -> ToolSpec:
    """Pick the best flat endmill that fits within *slot_width*.

    Tries to return a tool close to 80 % of the slot width.  If no catalog
    tool fits, falls back to the smallest available flat endmill and relies
    on the caller's validation note to warn.
    """
    target_dia = max(slot_width * 0.8, 1.0)

    # Gather all flat endmills sorted by diameter
    ToolCatalog._ensure_initialised()
    candidates = sorted(
        (t for t in ToolCatalog._tools.values() if t.tool_type == "flat_endmill"),
        key=lambda t: t.diameter,
    )

    if not candidates:
        return ToolSpec("flat_endmill", target_dia)

    # 1st choice: largest tool that fits (<= slot_width) AND is >= target_dia
    fitting = [t for t in candidates if t.diameter <= slot_width]
    for t in reversed(fitting):
        if t.diameter >= target_dia:
            return t

    # 2nd choice: largest tool that fits at all
    if fitting:
        return fitting[-1]

    # Fallback: nothing fits -- return the smallest available tool
    return candidates[0]


def _pick_reamer(hole_diameter: float) -> ToolSpec:
    """Pick the closest reamer tool for a given hole diameter.

    Searches the catalog for tools whose name starts with ``REAM_`` and
    returns the smallest reamer whose diameter >= *hole_diameter*.  If no
    reamer is large enough, the largest available reamer is returned.
    Falls back to a generic drill-type tool with a 45-degree tip angle
    when the catalog contains no reamers at all.
    """
    ToolCatalog._ensure_initialised()
    reamers = sorted(
        (t for name, t in ToolCatalog._tools.items() if name.startswith("REAM_")),
        key=lambda t: t.diameter,
    )
    if reamers:
        for r in reamers:
            if r.diameter >= hole_diameter:
                return r
        return reamers[-1]
    # Fallback: no reamers in catalog
    return ToolSpec("drill", hole_diameter, tip_angle=45.0)


# =============================================================================
#  Abstract base class
# =============================================================================

@dataclass
class MachiningOperation(ABC):
    """Abstract base for all subtractive machining operations.

    Attributes:
        sequence_number: Order within a ProcessPlan (assigned externally).
        tool: The ToolSpec chosen for this operation.
        feeds_speeds: dict with rpm, feed_rate_mm_min, etc.; empty if unknown.
        position: (x, y) on the top workplane (None for whole-face ops).
    """

    sequence_number: int = 0
    tool: Optional[ToolSpec] = None
    feeds_speeds: dict = field(default_factory=dict)
    position: Optional[Tuple[float, float]] = None
    face_selector: str = ">Z"

    # -- abstract interface --------------------------------------------------

    @abstractmethod
    def apply(self, shape):
        """Apply this operation to a CadQuery shape.  Returns modified shape."""
        ...

    @abstractmethod
    def to_dict(self) -> dict:
        """Serialize to dict for inclusion in a ProcessPlan."""
        ...

    @abstractmethod
    def to_toolpath(self) -> list:
        """Generate approximate toolpath waypoints for simulation.

        Phase 3 stub -- returns an empty list.
        """
        ...


# =============================================================================
#  Phase 1 concrete operations
# =============================================================================

# ---------------------------------------------------------------------------
#  1. FaceMillOp
# ---------------------------------------------------------------------------

@dataclass
class FaceMillOp(MachiningOperation):
    """Face milling -- removes material from the entire top face.

    Auto-selects a flat endmill from the catalog; chooses ~50 mm (EM_50mm_FACE)
    for large parts and 10 mm for smaller parts when no tool is given.
    """

    depth: float = 1.0
    """Depth of cut from the top face (mm)."""

    stepover: Optional[float] = None
    """Width of each pass; defaults to tool_diameter * 0.7 when None."""

    finish_pass: bool = False
    """If True, record a finishing pass with lighter parameters."""

    tool: Optional[ToolSpec] = None
    """Face mill tool.  Auto-selected if None."""

    material: str = "aluminum_6061"
    """Workpiece material key."""

    def __post_init__(self):
        if self.tool is None:
            try:
                self.tool = ToolCatalog.get("EM_50mm_FACE")
            except KeyError:
                try:
                    self.tool = ToolCatalog.get_best_for("flat_endmill", 10.0)
                except ValueError:
                    self.tool = ToolSpec("flat_endmill", 10.0)

        tool_type_fs = _resolve_fs_tool_type(self.tool.tool_type)
        self.feeds_speeds = get_feeds_speeds(
            tool_type_fs, self.tool.diameter, self.material
        )
        self.position = None  # face mill covers entire surface

    # ------------------------------------------------------------------

    def apply(self, shape):
        return face_mill_cut(shape, self.depth, face_selector=self.face_selector)

    def to_dict(self) -> dict:
        return {
            "operation": "face_mill",
            "tool_type": self.tool.tool_type,
            "tool_diameter_mm": self.tool.diameter,
            "depth_mm": self.depth,
            "stepover_mm": (
                self.stepover if self.stepover is not None
                else self.tool.diameter * 0.7
            ),
            "feeds_speeds": self.feeds_speeds
            if "error" not in self.feeds_speeds
            else None,
            "finish_pass": self.finish_pass,
            "face_selector": self.face_selector,
            "notes": "Finishing pass included" if self.finish_pass else "",
        }

    def to_toolpath(self) -> list:
        return []


# ---------------------------------------------------------------------------
#  2. PocketOp
# ---------------------------------------------------------------------------

@dataclass
class PocketOp(MachiningOperation):
    """Rectangular pocket at a given position.

    If *corner_radius* > 0 and the auto-selected tool radius exceeds the
    corner radius, a secondary finish operation with a smaller tool is
    automatically created and stored in ``finish_op``.
    """

    cx: float = 0.0
    cy: float = 0.0
    width: float = 20.0
    length: float = 30.0
    depth: float = 5.0
    corner_radius: float = 0.0

    tool: Optional[ToolSpec] = None
    material: str = "aluminum_6061"

    finish_op: Optional["PocketOp"] = field(default=None, repr=False)
    """Auto-created finish operation for small corner radii (internal)."""

    def __post_init__(self):
        if self.tool is None:
            min_tool_dia = min(self.width, self.length) * 0.8
            try:
                self.tool = ToolCatalog.get_best_for("flat_endmill", min_tool_dia)
            except ValueError:
                self.tool = ToolSpec("flat_endmill", min_tool_dia)

        tool_type_fs = _resolve_fs_tool_type(self.tool.tool_type)
        self.feeds_speeds = get_feeds_speeds(
            tool_type_fs, self.tool.diameter, self.material
        )
        self.position = (self.cx, self.cy)

        # Auto-finish: a large tool cannot reach into a tight corner radius
        if self.corner_radius > 0 and self.tool.radius > self.corner_radius:
            finish_tool_dia = self.corner_radius * 2.0
            try:
                finish_tool = ToolCatalog.get_best_for(
                    "flat_endmill", max(finish_tool_dia, 2.0)
                )
            except ValueError:
                finish_tool = ToolSpec("flat_endmill", max(finish_tool_dia, 2.0))

            # Only create a finish op if the finish tool is actually smaller
            if finish_tool.diameter < self.tool.diameter:
                self.finish_op = PocketOp(
                    cx=self.cx,
                    cy=self.cy,
                    width=self.width,
                    length=self.length,
                    depth=self.depth,
                    corner_radius=self.corner_radius,
                    tool=finish_tool,
                    material=self.material,
                    sequence_number=self.sequence_number + 1,
                )

    # ------------------------------------------------------------------

    def apply(self, shape):
        result = rectangular_pocket_cut(
            shape,
            self.cx, self.cy,
            self.width, self.length,
            self.depth,
            self.corner_radius,
            face_selector=self.face_selector,
        )
        # Apply finish pass if one was created
        if self.finish_op is not None:
            self.finish_op.face_selector = self.face_selector
            result = self.finish_op.apply(result)
        return result

    def to_dict(self) -> dict:
        d: dict = {
            "operation": "rough_pocket",
            "tool_type": self.tool.tool_type,
            "tool_diameter_mm": self.tool.diameter,
            "depth_mm": self.depth,
            "dimensions": {
                "length": self.length,
                "width": self.width,
                "depth": self.depth,
            },
            "corner_radius_mm": self.corner_radius,
            "position": list(self.position) if self.position else None,
            "face_selector": self.face_selector,
            "feeds_speeds": self.feeds_speeds
            if "error" not in self.feeds_speeds
            else None,
            "has_finish_pass": self.finish_op is not None,
            "notes": (
                "Finish pass available" if self.finish_op is not None
                else ""
            ),
        }
        return d

    def to_toolpath(self) -> list:
        return []


# ---------------------------------------------------------------------------
#  3. CircularPocketOp
# ---------------------------------------------------------------------------

@dataclass
class CircularPocketOp(MachiningOperation):
    """Circular pocket at a given position."""

    cx: float = 0.0
    cy: float = 0.0
    diameter: float = 20.0
    depth: float = 5.0

    tool: Optional[ToolSpec] = None
    material: str = "aluminum_6061"

    def __post_init__(self):
        if self.tool is None:
            # Prefer a tool no larger than ~80% of the pocket diameter
            tool_dia = self.diameter * 0.8
            try:
                self.tool = ToolCatalog.get_best_for("flat_endmill", tool_dia)
            except ValueError:
                self.tool = ToolSpec("flat_endmill", tool_dia)

        tool_type_fs = _resolve_fs_tool_type(self.tool.tool_type)
        self.feeds_speeds = get_feeds_speeds(
            tool_type_fs, self.tool.diameter, self.material
        )
        self.position = (self.cx, self.cy)

    # ------------------------------------------------------------------

    def apply(self, shape):
        return circular_pocket_cut(shape, self.cx, self.cy, self.diameter, self.depth,
                                   face_selector=self.face_selector)

    def to_dict(self) -> dict:
        return {
            "operation": "circular_pocket",
            "tool_type": self.tool.tool_type,
            "tool_diameter_mm": self.tool.diameter,
            "depth_mm": self.depth,
            "pocket_diameter_mm": self.diameter,
            "position": list(self.position) if self.position else None,
            "face_selector": self.face_selector,
            "feeds_speeds": self.feeds_speeds
            if "error" not in self.feeds_speeds
            else None,
            "notes": "",
        }

    def to_toolpath(self) -> list:
        return []


# ---------------------------------------------------------------------------
#  4. SpotDrillOp  (internal helper used by DrillOp)
# ---------------------------------------------------------------------------

@dataclass
class SpotDrillOp(MachiningOperation):
    """Spot-drilling operation -- creates a shallow conical start for a drill.

    This is normally created internally by ``DrillOp`` when
    ``spot_drill=True`` (the default).  Geometry is unchanged -- a spot
    drill is primarily a process-planning step.
    """

    cx: float = 0.0
    cy: float = 0.0
    hole_diameter: float = 6.0
    """Target hole diameter (the spot drill is sized slightly larger)."""

    material: str = "aluminum_6061"

    tool: Optional[ToolSpec] = None

    def __post_init__(self):
        if self.tool is None:
            # Pick a spot drill whose diameter covers the hole
            spot_dia = self.hole_diameter + 2.0  # slightly larger
            try:
                self.tool = ToolCatalog.get_best_for("drill", spot_dia)
            except ValueError:
                self.tool = ToolSpec("drill", spot_dia, tip_angle=120.0)

        tool_type_fs = _resolve_fs_tool_type(self.tool.tool_type)
        self.feeds_speeds = get_feeds_speeds(
            tool_type_fs, self.tool.diameter, self.material
        )
        self.position = (self.cx, self.cy)

    # ------------------------------------------------------------------

    def apply(self, shape):
        # Spot-drill does not change the final hole geometry -- it is a
        # planning step that precedes the actual drill.
        return shape

    def to_dict(self) -> dict:
        return {
            "operation": "spot_drill",
            "tool_type": self.tool.tool_type,
            "tool_diameter_mm": self.tool.diameter,
            "depth_mm": 1.0,  # spot-drill is shallow
            "position": list(self.position) if self.position else None,
            "face_selector": self.face_selector,
            "feeds_speeds": self.feeds_speeds
            if "error" not in self.feeds_speeds
            else None,
            "notes": "Spot drill for hole alignment",
        }

    def to_toolpath(self) -> list:
        return []


# ---------------------------------------------------------------------------
#  5. DrillOp
# ---------------------------------------------------------------------------

@dataclass
class DrillOp(MachiningOperation):
    """Drilling operation -- creates a hole at a given position.

    When ``spot_drill=True`` (default) an internal ``SpotDrillOp`` is
    created and applied first (process-planning only -- the spot drill
    does not modify the B-Rep).

    When ``peck=True`` the feeds/speeds are adjusted for peck-drilling
    (reduced feed rate).
    """

    cx: float = 0.0
    cy: float = 0.0
    diameter: float = 6.0
    depth: float = 10.0
    through: bool = False
    spot_drill: bool = True
    peck: bool = False

    tool: Optional[ToolSpec] = None
    """Drill bit.  Auto-selected to match hole diameter when None."""

    spot_op: Optional[SpotDrillOp] = field(default=None, repr=False)
    """Internal spot-drill operation created when spot_drill=True."""

    material: str = "aluminum_6061"

    def __post_init__(self):
        if self.tool is None:
            try:
                self.tool = ToolCatalog.get_best_for("drill", self.diameter)
            except ValueError:
                self.tool = ToolSpec("drill", self.diameter, tip_angle=118.0)

        tool_type_fs = _resolve_fs_tool_type(self.tool.tool_type)
        self.feeds_speeds = get_feeds_speeds(
            tool_type_fs, self.tool.diameter, self.material
        )

        # Peck drilling adjusts feed rate downward
        if self.peck and "error" not in self.feeds_speeds:
            peck_fs = dict(self.feeds_speeds)
            orig = peck_fs.get("feed_rate_mm_min", 0)
            peck_fs["feed_rate_mm_min"] = orig * 0.5 if orig else 0
            peck_fs["peck_drilling"] = True
            self.feeds_speeds = peck_fs

        if self.spot_drill:
            self.spot_op = SpotDrillOp(
                cx=self.cx,
                cy=self.cy,
                hole_diameter=self.diameter,
                material=self.material,
            )

        self.position = (self.cx, self.cy)

    # ------------------------------------------------------------------

    def apply(self, shape):
        if self.spot_op is not None:
            self.spot_op.face_selector = self.face_selector
            shape = self.spot_op.apply(shape)
        return drill_hole(shape, self.cx, self.cy, self.diameter, self.depth, self.through,
                          face_selector=self.face_selector)

    def to_dict(self) -> dict:
        return {
            "operation": "drill",
            "tool_type": self.tool.tool_type,
            "tool_diameter_mm": self.tool.diameter,
            "depth_mm": self.depth,
            "hole_diameter_mm": self.diameter,
            "through": self.through,
            "peck_drilling": self.peck,
            "position": list(self.position) if self.position else None,
            "face_selector": self.face_selector,
            "feeds_speeds": self.feeds_speeds
            if "error" not in self.feeds_speeds
            else None,
            "has_spot_drill": self.spot_op is not None,
            "notes": "Peck drilling" if self.peck else "",
        }

    def to_toolpath(self) -> list:
        return []


# ---------------------------------------------------------------------------
#  6. TapOp
# ---------------------------------------------------------------------------

# Standard ISO metric coarse thread pitches (mm)
_METRIC_COARSE_PITCH: dict[float, float] = {
    1.0: 0.25, 1.2: 0.25, 1.6: 0.35,
    2.0: 0.4, 2.5: 0.45,
    3.0: 0.5, 4.0: 0.7, 5.0: 0.8,
    6.0: 1.0, 8.0: 1.25, 10.0: 1.5, 12.0: 1.75,
    14.0: 2.0, 16.0: 2.0, 18.0: 2.5, 20.0: 2.5,
    24.0: 3.0, 30.0: 3.5, 36.0: 4.0,
}


def _standard_pitch(diameter: float) -> float:
    """Return the standard ISO metric coarse pitch for *diameter*, or a
    rough estimate (diameter * 0.16) when the diameter is non-standard."""
    return _METRIC_COARSE_PITCH.get(diameter, round(diameter * 0.16, 2))


def _expected_tap_drill(diameter: float, pitch: float) -> float:
    """Standard metric tap-drill diameter = major_diameter - pitch."""
    return diameter - pitch


@dataclass
class TapOp(MachiningOperation):
    """Thread-tapping operation.

    Tapping does not appreciably change the B-Rep hole diameter; the
    operation is recorded in the process plan for downstream CAM.

    Validates that the *tap_drill_diameter* is within a reasonable range
    for the given thread diameter and pitch.
    """

    cx: float = 0.0
    cy: float = 0.0
    diameter: float = 6.0
    """Thread major diameter (mm)."""

    pitch: float = 1.0
    """Thread pitch (mm).  Defaults to standard coarse for the diameter."""

    depth: float = 10.0
    """Tapping depth (mm)."""

    through: bool = False

    tap_drill_diameter: float = 5.0
    """Diameter of the hole to be tapped (should be ~diameter - pitch)."""

    tool: Optional[ToolSpec] = None
    """Tap tool.  Auto-selected from catalog by diameter."""

    material: str = "aluminum_6061"

    _validation_note: str = field(default="", repr=False)
    """Populated during __post_init__ with any tap-drill validation notes."""

    def __post_init__(self):
        # Auto-select pitch if not explicitly set (pitch=0 or default)
        if self.pitch <= 0:
            self.pitch = _standard_pitch(self.diameter)

        if self.tool is None:
            # Try named tap first, fall back to best thread_mill
            tap_name = f"TAP_M{int(self.diameter)}"
            try:
                self.tool = ToolCatalog.get(tap_name)
            except KeyError:
                try:
                    self.tool = ToolCatalog.get_best_for("thread_mill", self.diameter)
                except ValueError:
                    self.tool = ToolSpec("thread_mill", self.diameter)

        tool_type_fs = _resolve_fs_tool_type(self.tool.tool_type)
        self.feeds_speeds = get_feeds_speeds(
            tool_type_fs, self.tool.diameter, self.material
        )

        # Validate tap-drill diameter
        expected = _expected_tap_drill(self.diameter, self.pitch)
        tolerance = self.pitch * 0.3
        if abs(self.tap_drill_diameter - expected) > tolerance:
            self._validation_note = (
                f"Tap-drill {self.tap_drill_diameter:.2f} mm differs from "
                f"recommended {expected:.2f} mm (M{self.diameter:.1f}x{self.pitch})"
            )

        self.position = (self.cx, self.cy)

    # ------------------------------------------------------------------

    def apply(self, shape):
        # Tapping does not change the B-Rep hole diameter appreciably
        return shape

    def to_dict(self) -> dict:
        return {
            "operation": "tap",
            "tool_type": self.tool.tool_type,
            "thread_diameter_mm": self.diameter,
            "thread_pitch_mm": self.pitch,
            "tap_drill_size_mm": self.tap_drill_diameter,
            "depth_mm": self.depth,
            "through": self.through,
            "position": list(self.position) if self.position else None,
            "face_selector": self.face_selector,
            "feeds_speeds": self.feeds_speeds
            if "error" not in self.feeds_speeds
            else None,
            "notes": self._validation_note,
        }

    def to_toolpath(self) -> list:
        return []


# ---------------------------------------------------------------------------
#  7. ChamferOp
# ---------------------------------------------------------------------------

@dataclass
class ChamferOp(MachiningOperation):
    """Edge chamfering -- bevels the top edges of the part.

    Auto-selects a 90-degree chamfer tool from the catalog.
    """

    width: float = 1.0
    """Chamfer width / depth (mm)."""

    tool: Optional[ToolSpec] = None
    """Chamfer tool.  Auto-selected (90-degree) when None."""

    material: str = "aluminum_6061"

    def __post_init__(self):
        if self.tool is None:
            try:
                self.tool = ToolCatalog.get_best_for("chamfer", 6.0)
            except ValueError:
                self.tool = ToolSpec("chamfer", 6.0, tip_angle=90.0, tip_diameter=1.0)

        tool_type_fs = _resolve_fs_tool_type(self.tool.tool_type)
        self.feeds_speeds = get_feeds_speeds(
            tool_type_fs, self.tool.diameter, self.material
        )
        self.position = None  # applies to perimeter edges

    # ------------------------------------------------------------------

    def apply(self, shape):
        return chamfer_edges(shape, self.width, face_selector=self.face_selector)

    def to_dict(self) -> dict:
        return {
            "operation": "chamfer",
            "tool_type": self.tool.tool_type,
            "tool_diameter_mm": self.tool.diameter,
            "chamfer_width_mm": self.width,
            "tool_tip_angle_deg": self.tool.tip_angle,
            "face_selector": self.face_selector,
            "feeds_speeds": self.feeds_speeds
            if "error" not in self.feeds_speeds
            else None,
            "notes": "",
        }

    def to_toolpath(self) -> list:
        return []


# ---------------------------------------------------------------------------
#  8. ContourOp
# ---------------------------------------------------------------------------

@dataclass
class ContourOp(MachiningOperation):
    """Profile / contour milling -- trims the outer perimeter of the part.

    Supports multiple Z-level passes via the *stepdown* parameter.
    """

    depth: float = 5.0
    """Total depth of the contour cut (mm)."""

    stepdown: float = 1.0
    """Depth per Z-level pass.  Set to 0 or negative for single pass."""

    tool: Optional[ToolSpec] = None
    """End mill for contouring.  Auto-selected when None."""

    material: str = "aluminum_6061"

    def __post_init__(self):
        if self.tool is None:
            try:
                self.tool = ToolCatalog.get_best_for("flat_endmill", 10.0)
            except ValueError:
                self.tool = ToolSpec("flat_endmill", 10.0)

        tool_type_fs = _resolve_fs_tool_type(self.tool.tool_type)
        self.feeds_speeds = get_feeds_speeds(
            tool_type_fs, self.tool.diameter, self.material
        )
        self.position = None  # contour follows the part perimeter

    # ------------------------------------------------------------------

    def apply(self, shape):
        return contour_cut_outer(shape, self.depth, self.stepdown,
                                 face_selector=self.face_selector)

    def to_dict(self) -> dict:
        return {
            "operation": "contour",
            "tool_type": self.tool.tool_type,
            "tool_diameter_mm": self.tool.diameter,
            "depth_mm": self.depth,
            "stepdown_mm": self.stepdown,
            "face_selector": self.face_selector,
            "feeds_speeds": self.feeds_speeds
            if "error" not in self.feeds_speeds
            else None,
            "notes": f"Multi-pass (stepdown={self.stepdown} mm)" if self.stepdown > 0 else "",
        }

    def to_toolpath(self) -> list:
        return []


# ---------------------------------------------------------------------------
#  9. SlotOp
# ---------------------------------------------------------------------------

@dataclass
class SlotOp(MachiningOperation):
    """Slot milling -- cuts an obround slot at a given position and angle.

    Validates that the selected tool diameter is not larger than the slot
    width.
    """

    cx: float = 0.0
    cy: float = 0.0
    length: float = 30.0
    width: float = 8.0
    depth: float = 5.0
    angle: float = 0.0
    """Rotation angle of the slot in degrees."""

    through: bool = False
    """If True, cut through entire part."""

    tool: Optional[ToolSpec] = None
    """End mill.  Auto-selected to fit within the slot width."""

    material: str = "aluminum_6061"

    _validation_note: str = field(default="", repr=False)

    def __post_init__(self):
        if self.tool is None:
            # Choose the best tool that still fits within the slot width.
            # Prefer a tool close to 80% of the slot width, but never exceed it.
            self.tool = _pick_slot_tool(self.width)

        # Validate: tool must not exceed slot width
        if self.tool.diameter > self.width:
            self._validation_note = (
                f"Tool diameter ({self.tool.diameter:.1f} mm) exceeds "
                f"slot width ({self.width:.1f} mm)"
            )

        tool_type_fs = _resolve_fs_tool_type(self.tool.tool_type)
        self.feeds_speeds = get_feeds_speeds(
            tool_type_fs, self.tool.diameter, self.material
        )
        self.position = (self.cx, self.cy)

    # ------------------------------------------------------------------

    def apply(self, shape):
        return slot_cut(
            shape,
            self.cx, self.cy,
            self.length, self.width,
            self.depth,
            self.angle,
            self.through,
            face_selector=self.face_selector,
        )

    def to_dict(self) -> dict:
        return {
            "operation": "slot",
            "tool_type": self.tool.tool_type,
            "tool_diameter_mm": self.tool.diameter,
            "depth_mm": self.depth,
            "slot_length_mm": self.length,
            "slot_width_mm": self.width,
            "slot_angle_deg": self.angle,
            "through": self.through,
            "position": list(self.position) if self.position else None,
            "face_selector": self.face_selector,
            "feeds_speeds": self.feeds_speeds
            if "error" not in self.feeds_speeds
            else None,
            "notes": self._validation_note,
        }

    def to_toolpath(self) -> list:
        return []


# =============================================================================
#  Convenience factory
# =============================================================================

_OP_REGISTRY: dict[str, type[MachiningOperation]] = {
    "face_mill":        FaceMillOp,
    "pocket":           PocketOp,
    "circular_pocket":  CircularPocketOp,
    "drill":            DrillOp,
    "tap":              TapOp,
    "spot_drill":       SpotDrillOp,
    "chamfer":          ChamferOp,
    "contour":          ContourOp,
    "slot":             SlotOp,
}


def create_operation(op_type: str, **kwargs) -> MachiningOperation:
    """Factory to create a MachiningOperation by name.

    Args:
        op_type: One of 'face_mill', 'pocket', 'circular_pocket', 'drill',
                 'tap', 'spot_drill', 'chamfer', 'contour', 'slot'.
        **kwargs: Forwarded to the operation class constructor.

    Returns:
        A concrete ``MachiningOperation`` instance.

    Raises:
        ValueError: If *op_type* is not a recognised operation name.
    """
    cls = _OP_REGISTRY.get(op_type)
    if cls is None:
        raise ValueError(
            f"Unknown operation type {op_type!r}. "
            f"Available: {sorted(_OP_REGISTRY.keys())}"
        )
    return cls(**kwargs)


# =============================================================================
#  Auto-operations helper
# =============================================================================

def threaded_hole_ops(
    diameter: float,
    depth: float,
    position: Tuple[float, float],
    material: str = "aluminum_6061",
    through: bool = False,
    face_selector: str = ">Z",
) -> list[MachiningOperation]:
    """Generate the full sequence for a threaded hole.

    Produces three operations in order:
        1. ``SpotDrillOp``  -- spot-drill for alignment
        2. ``DrillOp``      -- drill the tap-drill hole
        3. ``TapOp``        -- tap the threads

    The tap-drill diameter is computed using the standard ISO metric
    coarse formula: tap_drill = major_diameter - pitch.

    Args:
        diameter: Thread major diameter (mm), e.g. 6.0 for M6.
        depth: Hole / tap depth (mm).
        position: (cx, cy) on the top workplane.
        material: Workpiece material key.
        through: If True, drill and tap through the entire part.
        face_selector: CadQuery face selector (e.g. \">Z\", \"<Z\").

    Returns:
        A list of 3 ``MachiningOperation`` instances: [spot, drill, tap].
    """
    cx, cy = position
    pitch = _standard_pitch(diameter)
    tap_drill = _expected_tap_drill(diameter, pitch)

    spot = SpotDrillOp(
        cx=cx,
        cy=cy,
        hole_diameter=tap_drill,
        material=material,
        face_selector=face_selector,
    )

    drill = DrillOp(
        cx=cx,
        cy=cy,
        diameter=tap_drill,
        depth=depth,
        through=through,
        spot_drill=False,  # we already create a separate spot op
        material=material,
        face_selector=face_selector,
    )

    tap = TapOp(
        cx=cx,
        cy=cy,
        diameter=diameter,
        pitch=pitch,
        depth=depth,
        through=through,
        tap_drill_diameter=tap_drill,
        material=material,
        face_selector=face_selector,
    )

    return [spot, drill, tap]


# =============================================================================
#  Self-test
# =============================================================================

if __name__ == "__main__":
    import sys

    # ------------------------------------------------------------------
    # CadQuery guard
    # ------------------------------------------------------------------
    try:
        import cadquery as cq
        _HAS_CQ = True
    except ImportError:
        _HAS_CQ = False

    from .geometry import (
        create_rectangular_stock,
        compute_bounding_box,
        compute_volume,
    )
    from .tool_library import ToolCatalog

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

    # Ensure catalog is initialised
    ToolCatalog._ensure_initialised()

    print("=" * 60)
    print("SubCAD operations self-tests")
    print("=" * 60)

    # ==================================================================
    # Test 1: Each operation class instantiates with defaults
    # ==================================================================
    print("\n1. Instantiation with defaults ...")

    ops_default: list[MachiningOperation] = [
        FaceMillOp(),
        PocketOp(),
        CircularPocketOp(),
        DrillOp(),
        TapOp(),
        ChamferOp(),
        ContourOp(),
        SlotOp(),
    ]
    names = [
        "FaceMillOp", "PocketOp", "CircularPocketOp",
        "DrillOp", "TapOp", "ChamferOp", "ContourOp", "SlotOp",
    ]
    for op, name in zip(ops_default, names):
        check(isinstance(op, MachiningOperation), f"{name} is MachiningOperation")
        check(op.tool is not None, f"{name} auto-tool populated")
        check(isinstance(op.feeds_speeds, dict), f"{name} feeds_speeds is dict")

    # ==================================================================
    # Test 1b: DrillOp auto-creates spot_op when spot_drill=True
    # ==================================================================
    print("\n1b. DrillOp spot_drill ...")
    d_op = DrillOp(spot_drill=True)
    check(d_op.spot_op is not None, "DrillOp creates SpotDrillOp when spot_drill=True")
    check(isinstance(d_op.spot_op, SpotDrillOp), "spot_op is SpotDrillOp instance")

    d_op2 = DrillOp(spot_drill=False)
    check(d_op2.spot_op is None, "DrillOp without spot_drill has no spot_op")

    # ==================================================================
    # Test 1c: DrillOp peck drilling adjusts feeds
    # ==================================================================
    print("\n1c. DrillOp peck drilling ...")
    d_peck = DrillOp(peck=True)
    check("peck_drilling" in d_peck.feeds_speeds,
          "peck=True sets peck_drilling flag")
    check(d_peck.feeds_speeds.get("peck_drilling") is True,
          "peck_drilling value is True")

    # ==================================================================
    # Test 2: to_dict() returns correct structure
    # ==================================================================
    print("\n2. to_dict() structure ...")

    op_dicts: list[tuple[str, dict]] = [
        ("FaceMillOp", FaceMillOp().to_dict()),
        ("PocketOp", PocketOp().to_dict()),
        ("CircularPocketOp", CircularPocketOp().to_dict()),
        ("DrillOp", DrillOp().to_dict()),
        ("TapOp", TapOp().to_dict()),
        ("ChamferOp", ChamferOp().to_dict()),
        ("ContourOp", ContourOp().to_dict()),
        ("SlotOp", SlotOp().to_dict()),
        ("SpotDrillOp", SpotDrillOp().to_dict()),
    ]

    # Expected keys per operation type
    expected_keys = {
        "FaceMillOp":       ["operation", "tool_type", "tool_diameter_mm", "depth_mm", "feeds_speeds"],
        "PocketOp":         ["operation", "tool_type", "tool_diameter_mm", "depth_mm", "dimensions", "position"],
        "CircularPocketOp": ["operation", "tool_type", "tool_diameter_mm", "depth_mm", "pocket_diameter_mm"],
        "DrillOp":          ["operation", "tool_type", "tool_diameter_mm", "depth_mm", "hole_diameter_mm", "through"],
        "TapOp":            ["operation", "tool_type", "thread_diameter_mm", "thread_pitch_mm", "tap_drill_size_mm"],
        "ChamferOp":        ["operation", "tool_type", "chamfer_width_mm"],
        "ContourOp":        ["operation", "tool_type", "depth_mm", "stepdown_mm"],
        "SlotOp":           ["operation", "tool_type", "slot_length_mm", "slot_width_mm"],
        "SpotDrillOp":      ["operation", "tool_type", "depth_mm"],
    }

    for name, d in op_dicts:
        check(isinstance(d, dict), f"{name}.to_dict returns dict")
        for key in expected_keys.get(name, []):
            check(key in d, f"{name}.to_dict has key {key!r}")

    # ==================================================================
    # Test 3: Auto-tool selection works
    # ==================================================================
    print("\n3. Auto-tool selection ...")

    # FaceMillOp should pick a flat endmill
    fm = FaceMillOp()
    check(fm.tool.tool_type == "flat_endmill",
          f"FaceMillOp tool_type = {fm.tool.tool_type!r}")
    check(fm.tool.diameter >= 10.0,
          f"FaceMillOp diameter >= 10 mm (got {fm.tool.diameter})")

    # PocketOp should pick ~80% of pocket width
    p = PocketOp(width=20.0, length=30.0)
    expected_tool = 20.0 * 0.8  # 16.0
    check(p.tool.diameter >= expected_tool,
          f"PocketOp tool >= {expected_tool} mm (got {p.tool.diameter})")

    # DrillOp should match hole diameter
    d = DrillOp(diameter=8.0)
    check(d.tool.tool_type == "drill",
          f"DrillOp tool_type = {d.tool.tool_type!r}")
    check(d.tool.diameter >= 8.0,
          f"DrillOp diameter >= 8.0 mm (got {d.tool.diameter})")

    # TapOp should pick thread_mill
    t = TapOp(diameter=6.0)
    check(t.tool.tool_type == "thread_mill",
          f"TapOp tool_type = {t.tool.tool_type!r}")

    # ChamferOp should pick chamfer tool
    ch = ChamferOp()
    check(ch.tool.tool_type == "chamfer",
          f"ChamferOp tool_type = {ch.tool.tool_type!r}")

    # SlotOp should fit within slot width
    s = SlotOp(width=8.0)
    check(s.tool.diameter <= s.width,
          f"SlotOp tool diameter ({s.tool.diameter}) <= slot width ({s.width})")

    # ==================================================================
    # Test 4: create_operation factory
    # ==================================================================
    print("\n4. create_operation factory ...")

    for op_type in ["face_mill", "pocket", "circular_pocket", "drill",
                    "tap", "chamfer", "contour", "slot"]:
        try:
            op = create_operation(op_type)
            check(isinstance(op, MachiningOperation),
                  f"create_operation({op_type!r}) returns MachiningOperation")
        except Exception as exc:
            check(False, f"create_operation({op_type!r}) raised {exc}")

    # Unknown op_type should raise
    try:
        create_operation("laser_blast")
        check(False, "create_operation('laser_blast') should raise")
    except ValueError:
        check(True, "create_operation('laser_blast') raises ValueError")
    except Exception as exc:
        check(False, f"create_operation('laser_blast') wrong exception: {exc}")

    # ==================================================================
    # Test 5: threaded_hole_ops returns 3 operations
    # ==================================================================
    print("\n5. threaded_hole_ops ...")

    seq = threaded_hole_ops(diameter=6.0, depth=12.0, position=(10, 20),
                             material="aluminum_6061")
    check(len(seq) == 3,
          f"threaded_hole_ops returns 3 ops (got {len(seq)})")
    check(isinstance(seq[0], SpotDrillOp),
          f"seq[0] is SpotDrillOp (got {type(seq[0]).__name__})")
    check(isinstance(seq[1], DrillOp),
          f"seq[1] is DrillOp (got {type(seq[1]).__name__})")
    check(isinstance(seq[2], TapOp),
          f"seq[2] is TapOp (got {type(seq[2]).__name__})")

    # Spot drill should NOT have spot_drill=True (avoid infinite chain)
    d_op3 = seq[1]
    check(d_op3.spot_op is None,
          "threaded_hole_ops DrillOp has no spot_op (spot created separately)")

    # Tap should have correct drill size
    tap_op = seq[2]
    expected_td = 6.0 - 1.0  # M6 pitch = 1.0
    check(abs(tap_op.tap_drill_diameter - expected_td) < 0.01,
          f"tap_drill_diameter = {tap_op.tap_drill_diameter} "
          f"(expected {expected_td})")

    # ==================================================================
    # Test 6: apply() modifies geometry (requires CadQuery)
    # ==================================================================
    if _HAS_CQ:
        print("\n6. apply() modifies geometry ...")

        # 6a. FaceMillOp
        try:
            stock = create_rectangular_stock(100, 60, 20)
            fm_op = FaceMillOp(depth=3.0)
            result = fm_op.apply(stock)
            bb = compute_bounding_box(result)
            check(abs(bb["height"] - 17) < 0.5,
                  f"FaceMillOp reduces height to ~17 (got {bb['height']:.2f})")
        except Exception as exc:
            check(False, f"FaceMillOp.apply crashed: {exc}")

        # 6b. DrillOp
        try:
            stock = create_rectangular_stock(100, 60, 20)
            d_op6 = DrillOp(cx=0, cy=0, diameter=10.0, depth=0, through=True,
                            spot_drill=False)
            result = d_op6.apply(stock)
            vol_after = compute_volume(result)
            check(vol_after < compute_volume(stock),
                  f"DrillOp reduces volume")
        except Exception as exc:
            check(False, f"DrillOp.apply crashed: {exc}")

        # 6c. PocketOp
        try:
            stock = create_rectangular_stock(100, 60, 20)
            p_op = PocketOp(cx=0, cy=0, width=30, length=40, depth=5)
            result = p_op.apply(stock)
            vol_after = compute_volume(result)
            vol_expected = 100 * 60 * 20 - 30 * 40 * 5
            check(abs(vol_after - vol_expected) < 5.0,
                  f"PocketOp volume ~ {vol_expected} (got {vol_after:.1f})")
        except Exception as exc:
            check(False, f"PocketOp.apply crashed: {exc}")

        # 6d. ChamferOp
        try:
            stock = create_rectangular_stock(100, 60, 20)
            ch_op = ChamferOp(width=2.0)
            result = ch_op.apply(stock)
            vol_after = compute_volume(result)
            check(vol_after < compute_volume(stock),
                  "ChamferOp reduces volume")
        except Exception as exc:
            check(False, f"ChamferOp.apply crashed: {exc}")

        # 6e. TapOp geometry unchanged
        try:
            stock = create_rectangular_stock(100, 60, 20)
            t_op = TapOp()
            result = t_op.apply(stock)
            vol_before = compute_volume(stock)
            vol_after = compute_volume(result)
            check(abs(vol_after - vol_before) < 0.1,
                  f"TapOp does not change volume ({vol_before:.1f} vs {vol_after:.1f})")
        except Exception as exc:
            check(False, f"TapOp.apply crashed: {exc}")

        # 6f. SlotOp
        try:
            stock = create_rectangular_stock(100, 60, 20)
            s_op = SlotOp(cx=10, cy=0, length=30, width=8, depth=10)
            result = s_op.apply(stock)
            vol_after = compute_volume(result)
            check(vol_after < compute_volume(stock),
                  "SlotOp reduces volume")
        except Exception as exc:
            check(False, f"SlotOp.apply crashed: {exc}")

        # 6g. ContourOp
        try:
            stock = create_rectangular_stock(100, 60, 20)
            co_op = ContourOp(depth=5, stepdown=2.0)
            result = co_op.apply(stock)
            vol_after = compute_volume(result)
            check(vol_after < compute_volume(stock),
                  "ContourOp reduces volume")
        except Exception as exc:
            check(False, f"ContourOp.apply crashed: {exc}")

        # 6h. CircularPocketOp
        try:
            stock = create_rectangular_stock(100, 60, 20)
            cp_op = CircularPocketOp(cx=0, cy=0, diameter=30, depth=5)
            result = cp_op.apply(stock)
            vol_after = compute_volume(result)
            check(vol_after < compute_volume(stock),
                  "CircularPocketOp reduces volume")
        except Exception as exc:
            check(False, f"CircularPocketOp.apply crashed: {exc}")
    else:
        print("\n6. apply() geometry tests SKIPPED (CadQuery not available)")

    # ==================================================================
    # Test 7: PocketOp auto-finish
    # ==================================================================
    print("\n7. PocketOp auto-finish ...")
    # Corner radius >= tool radius -> no finish needed
    # For width=50 the tool is ~50 mm (radius ~25), so corner_radius=30 avoids finish
    p_no_finish = PocketOp(width=50, length=60, corner_radius=30.0)
    check(p_no_finish.finish_op is None,
          "No finish when corner_radius >= tool radius (got "
          f"tool_radius={p_no_finish.tool.radius:.1f}, corner_radius=30.0)")

    # Tight corner, large tool -> finish needed
    p_finish = PocketOp(width=20, length=30, corner_radius=1.0)
    # tool is ~16mm dia (80% of 20) -> radius 8 > corner 1
    if p_finish.tool.radius > 1.0:
        check(p_finish.finish_op is not None,
              "Finish op created when tool radius > corner_radius")
    else:
        # Tool happened to be smaller -- still a valid path
        check(True, "Tool happens to be small enough (no finish needed)")

    # ==================================================================
    # Test 8: TapOp validation note
    # ==================================================================
    print("\n8. TapOp validation ...")
    # Correct tap-drill: M6 coarse -> 5.0
    t_ok = TapOp(diameter=6.0, pitch=1.0, tap_drill_diameter=5.0)
    check(t_ok._validation_note == "",
          "Correct tap-drill yields empty validation note")

    # Wrong tap-drill
    t_bad = TapOp(diameter=6.0, pitch=1.0, tap_drill_diameter=3.0)
    check(t_bad._validation_note != "",
          "Incorrect tap-drill produces validation note")
    check("differs from recommended" in t_bad._validation_note,
          "Validation note mentions the discrepancy")

    # ==================================================================
    # Test 9: SlotOp width validation
    # ==================================================================
    print("\n9. SlotOp width validation ...")
    s_ok = SlotOp(width=20.0)
    check(s_ok._validation_note == "",
          "Tool fits in slot -> no validation note")

    s_narrow = SlotOp(width=2.0)
    if s_narrow.tool.diameter > 2.0:
        check(s_narrow._validation_note != "",
              "Tool too wide -> validation note populated")
    else:
        check(True, "Tool fits (unexpected but valid)")

    # ==================================================================
    # Test 10: to_toolpath stubs
    # ==================================================================
    print("\n10. to_toolpath stubs ...")
    for op in ops_default:
        tp = op.to_toolpath()
        check(isinstance(tp, list),
              f"{op.__class__.__name__}.to_toolpath returns list")
        check(len(tp) == 0,
              f"{op.__class__.__name__}.to_toolpath is empty (Phase 3 stub)")

    # ==================================================================
    # Test 11: Position tracking
    # ==================================================================
    print("\n11. Position tracking ...")
    check(FaceMillOp().position is None, "FaceMillOp position is None")
    check(ChamferOp().position is None, "ChamferOp position is None")
    check(ContourOp().position is None, "ContourOp position is None")

    d_pos = DrillOp(cx=12.5, cy=25.0)
    check(d_pos.position == (12.5, 25.0),
          f"DrillOp position = {d_pos.position}")

    p_pos = PocketOp(cx=-5.0, cy=10.0)
    check(p_pos.position == (-5.0, 10.0),
          f"PocketOp position = {p_pos.position}")

    s_pos = SlotOp(cx=30.0, cy=-15.0)
    check(s_pos.position == (30.0, -15.0),
          f"SlotOp position = {s_pos.position}")

    # ==================================================================
    # Test 12: face_selector in operations
    # ==================================================================
    print("\n12. face_selector ...")
    check(FaceMillOp().face_selector == ">Z", "default face_selector is >Z")
    check(FaceMillOp(face_selector="<Z").to_dict()["face_selector"] == "<Z",
          "to_dict includes face_selector")
    check(DrillOp(face_selector=">X").to_dict()["face_selector"] == ">X",
          "DrillOp face_selector in dict")
    check(ChamferOp(face_selector="<Z").to_dict()["face_selector"] == "<Z",
          "ChamferOp face_selector in dict")

    # threaded_hole_ops with face_selector
    seq = threaded_hole_ops(diameter=6, depth=10, position=(0, 0),
                            face_selector="<Z")
    for op in seq:
        check(op.face_selector == "<Z",
              f"{op.__class__.__name__} face_selector forwarded")

    if _HAS_CQ:
        try:
            stock = create_rectangular_stock(100, 60, 20)
            d_op = DrillOp(cx=0, cy=0, diameter=10, depth=0, through=True,
                          spot_drill=False, face_selector="<Z")
            result = d_op.apply(stock)
            check(compute_volume(result) < compute_volume(stock),
                  "DrillOp from bottom face reduces volume")
        except Exception as exc:
            check(False, f"DrillOp bottom face apply crashed: {exc}")

    # ==================================================================
    # Summary
    # ==================================================================
    total = passed + failed
    print(f"\n{'=' * 60}")
    print(f"Results: {passed}/{total} passed, {failed}/{total} failed")
    if failed > 0:
        sys.exit(1)
