"""
SubCAD Tool Library
===================
Tool specification and standard tool catalog for the subtractive CAD system.

Defines ``ToolSpec`` dataclass and ``ToolCatalog`` with standard industry tools.
Also provides a bridge function to convert ``ToolSpec`` to simulation-suitable
``Tool`` instances from ``src.simulation.tools``.

Usage::

    from src.subcad.tool_library import ToolSpec, ToolCatalog, to_sim_tool

    em6 = ToolCatalog.get("EM_6mm")
    print(em6)

    # Run the built-in self-test:
    #   python -m src.subcad.tool_library
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


# =========================================================================
#   ToolSpec
# =========================================================================

@dataclass
class ToolSpec:
    """Specification for a subtractive machining tool.

    All linear dimensions are in millimetres.  Follows the APT 7-parameter
    model with additional manufacturing metadata (flute count, coating, material).

    Attributes:
        tool_type: One of ``"flat_endmill"``, ``"ball_endmill"``, ``"drill"``,
            ``"chamfer"``, ``"bull_nose"``, ``"thread_mill"``, ``"dovetail"``.
        diameter: Cutting diameter in mm.
        corner_radius: Corner radius in mm (0 for sharp corners).
        flute_length: Length of the cutting flutes in mm.
        num_flutes: Number of flutes / cutting edges.
        coating: Tool coating (``"uncoated"``, ``"TiN"``, ``"TiAlN"``, etc.).
        material: Tool material (``"carbide"``, ``"HSS"``, etc.).
        tip_angle: Tip angle in degrees (e.g. 118 for standard drills).
        tip_diameter: Diameter at the very tip in mm (for chamfer tools,
            dovetail cutters, step drills).
    """

    tool_type: str
    diameter: float
    corner_radius: float = 0.0
    flute_length: float = 50.0
    num_flutes: int = 2
    coating: str = "uncoated"
    material: str = "carbide"
    tip_angle: float = 0.0
    tip_diameter: float = 0.0

    @property
    def radius(self) -> float:
        """Nominal tool radius (diameter / 2)."""
        return self.diameter / 2.0


# =========================================================================
#   ToolCatalog
# =========================================================================

class ToolCatalog:
    """Catalog of standard cutting tools organised by category.

    Tools are stored in class-level dictionaries.  Use ``get(name)`` to
    retrieve a ``ToolSpec``.  Custom tools can be added at runtime via
    ``register(name, tool)``.

    Category keys (for ``list_all()``):
        - ``flat_endmills``
        - ``ball_endmills``
        - ``bull_nose``
        - ``drills``
        - ``chamfer_tools``
        - ``taps``
        - ``reamers``
        - ``spot_drills``
        - ``custom``
    """

    # -----------------------------------------------------------------
    #   Class state
    # -----------------------------------------------------------------

    _tools: dict[str, ToolSpec] = {}

    # User-facing category grouping -- maps a display name to a list of
    # tool names that *would* exist in the catalog once it is initialised.
    _categories: dict[str, list[str]] = {
        "flat_endmills": [
            "EM_1mm", "EM_3mm", "EM_6mm", "EM_10mm",
            "EM_12mm", "EM_16mm", "EM_20mm", "EM_50mm_FACE",
        ],
        "ball_endmills": [
            "BEM_3mm", "BEM_6mm", "BEM_10mm", "BEM_12mm", "BEM_16mm",
        ],
        "bull_nose": [
            "BN_10mm_R2", "BN_12mm_R3", "BN_16mm_R4",
        ],
        "drills": [
            "DR_1mm", "DR_3mm", "DR_6mm", "DR_8mm",
            "DR_10mm", "DR_12mm", "DR_16mm",
        ],
        "chamfer_tools": [
            "CH_6mm_90deg", "CH_10mm_90deg",
        ],
        "taps": [
            "TAP_M3", "TAP_M4", "TAP_M5", "TAP_M6",
            "TAP_M8", "TAP_M10", "TAP_M12",
        ],
        "reamers": [
            "REAM_3mm", "REAM_4mm", "REAM_5mm", "REAM_6mm",
            "REAM_8mm", "REAM_10mm",
        ],
        "spot_drills": [
            "SPOT_6mm", "SPOT_10mm",
        ],
    }

    # The catalogue of preset tools.  These instances are only created
    # once (lazily) and then cached in ``_tools``.
    _presets: dict[str, ToolSpec] = {}

    # -----------------------------------------------------------------
    #   Lazy initialisation
    # -----------------------------------------------------------------

    @classmethod
    def _ensure_initialised(cls) -> None:
        """Populate the catalog from presets on first access."""
        if cls._tools:
            return

        def _e(tool_type: str, diameter: float, **kw) -> ToolSpec:
            return ToolSpec(tool_type=tool_type, diameter=diameter, **kw)

        cls._tools.update({
            # --- Flat Endmills ---
            "EM_1mm":       _e("flat_endmill", 1.0),
            "EM_3mm":       _e("flat_endmill", 3.0),
            "EM_6mm":       _e("flat_endmill", 6.0),
            "EM_10mm":      _e("flat_endmill", 10.0),
            "EM_12mm":      _e("flat_endmill", 12.0),
            "EM_16mm":      _e("flat_endmill", 16.0),
            "EM_20mm":      _e("flat_endmill", 20.0),
            "EM_50mm_FACE": _e("flat_endmill", 50.0,
                               flute_length=80.0, num_flutes=6),

            # --- Ball Endmills ---
            "BEM_3mm":  _e("ball_endmill", 3.0),
            "BEM_6mm":  _e("ball_endmill", 6.0),
            "BEM_10mm": _e("ball_endmill", 10.0),
            "BEM_12mm": _e("ball_endmill", 12.0),
            "BEM_16mm": _e("ball_endmill", 16.0),

            # --- Bull Nose ---
            "BN_10mm_R2": _e("bull_nose", 10.0, corner_radius=2.0),
            "BN_12mm_R3": _e("bull_nose", 12.0, corner_radius=3.0),
            "BN_16mm_R4": _e("bull_nose", 16.0, corner_radius=4.0),

            # --- Drills (118 deg tip) ---
            "DR_1mm":  _e("drill", 1.0,  tip_angle=118.0),
            "DR_3mm":  _e("drill", 3.0,  tip_angle=118.0),
            "DR_6mm":  _e("drill", 6.0,  tip_angle=118.0),
            "DR_8mm":  _e("drill", 8.0,  tip_angle=118.0),
            "DR_10mm": _e("drill", 10.0, tip_angle=118.0),
            "DR_12mm": _e("drill", 12.0, tip_angle=118.0),
            "DR_16mm": _e("drill", 16.0, tip_angle=118.0),

            # --- Chamfer Tools ---
            "CH_6mm_90deg":  _e("chamfer", 6.0,
                                tip_angle=90.0, tip_diameter=1.0),
            "CH_10mm_90deg": _e("chamfer", 10.0,
                                tip_angle=90.0, tip_diameter=2.0),

            # --- Taps (modelled as thread mills) ---
            "TAP_M3":  _e("thread_mill", 3.0),
            "TAP_M4":  _e("thread_mill", 4.0),
            "TAP_M5":  _e("thread_mill", 5.0),
            "TAP_M6":  _e("thread_mill", 6.0),
            "TAP_M8":  _e("thread_mill", 8.0),
            "TAP_M10": _e("thread_mill", 10.0),
            "TAP_M12": _e("thread_mill", 12.0),

            # --- Reamers (shallow tip angle) ---
            "REAM_3mm":  _e("drill", 3.0,  tip_angle=45.0),
            "REAM_4mm":  _e("drill", 4.0,  tip_angle=45.0),
            "REAM_5mm":  _e("drill", 5.0,  tip_angle=45.0),
            "REAM_6mm":  _e("drill", 6.0,  tip_angle=45.0),
            "REAM_8mm":  _e("drill", 8.0,  tip_angle=45.0),
            "REAM_10mm": _e("drill", 10.0, tip_angle=45.0),

            # --- Spot Drills (wider tip than standard drills) ---
            "SPOT_6mm":  _e("drill", 6.0,  tip_angle=120.0),
            "SPOT_10mm": _e("drill", 10.0, tip_angle=120.0),
        })

    # -----------------------------------------------------------------
    #   Public API
    # -----------------------------------------------------------------

    @classmethod
    def get(cls, name: str) -> ToolSpec:
        """Retrieve a tool specification by name.

        Args:
            name: Tool name, e.g. ``"EM_10mm"``, ``"BEM_6mm"``.

        Returns:
            The matching ``ToolSpec``.

        Raises:
            KeyError: If the tool name is not found in the catalog.
        """
        cls._ensure_initialised()
        if name not in cls._tools:
            available = ", ".join(sorted(cls._tools.keys()))
            raise KeyError(
                f"Tool {name!r} not found in catalog. "
                f"Available: {available}"
            )
        return cls._tools[name]

    @classmethod
    def list_all(cls) -> dict[str, list[str]]:
        """List all tools organised by category.

        Returns:
            A dictionary mapping category name (``str``) to a list of
            tool names (``list[str]``).
        """
        cls._ensure_initialised()
        result: dict[str, list[str]] = {}
        for category, names in cls._categories.items():
            present = [n for n in names if n in cls._tools]
            if present:
                result[category] = present

        # Collect any registered tools that do not belong to a standard
        # category and put them under "custom".
        categorised = {n for names in result.values() for n in names}
        custom = [n for n in cls._tools if n not in categorised]
        if custom:
            result["custom"] = custom

        return result

    @classmethod
    def register(cls, name: str, tool: ToolSpec) -> None:
        """Register a custom tool in the catalog at runtime.

        Args:
            name: Unique name for the tool.
            tool: ``ToolSpec`` instance to register.

        Raises:
            ValueError: If a tool with *name* already exists.
        """
        cls._ensure_initialised()
        if name in cls._tools:
            raise ValueError(
                f"Tool {name!r} already exists in the catalog. "
                f"Use a different name or remove it first."
            )
        cls._tools[name] = tool

    @classmethod
    def get_best_for(cls, tool_type: str, min_diameter: float) -> ToolSpec:
        """Auto-select the closest tool of *tool_type* with diameter
        greater than or equal to *min_diameter*.

        Selection logic:
            1. Filter all tools of the requested *tool_type*.
            2. Pick the **smallest** tool whose diameter >= *min_diameter*.
            3. If no tool is large enough, return the largest available
               tool of that type.

        Args:
            tool_type: One of the recognised tool-type strings
                (``"flat_endmill"``, ``"ball_endmill"``, etc.).
            min_diameter: Minimum acceptable diameter in mm.

        Returns:
            The best-matching ``ToolSpec``.

        Raises:
            ValueError: If the catalog contains no tools of the requested
                *tool_type*.
        """
        cls._ensure_initialised()
        candidates = [
            t for t in cls._tools.values() if t.tool_type == tool_type
        ]
        if not candidates:
            raise ValueError(
                f"No tools of type {tool_type!r} in the catalog."
            )

        candidates.sort(key=lambda t: t.diameter)

        # Smallest tool that meets or exceeds the requirement
        for tool in candidates:
            if tool.diameter >= min_diameter:
                return tool

        # Fall back to the largest available
        return candidates[-1]


# =========================================================================
#   Bridge to simulation tools
# =========================================================================

def to_sim_tool(spec: ToolSpec):
    """Convert a ``ToolSpec`` to a simulation-suitable ``Tool`` instance.

    Imports from ``src.simulation.tools`` and calls ``create_tool()`` with
    the appropriate arguments for the tool type.  Returns ``None`` if the
    simulation module cannot be imported (graceful degradation).

    Args:
        spec: The ``ToolSpec`` to convert.

    Returns:
        A ``Tool`` subclass instance (``FlatEndmill``, ``BallEndmill``,
        ``Drill``, etc.) or ``None`` if the simulation package is not
        available.
    """
    try:
        from src.simulation.tools import create_tool
    except ImportError:
        return None

    # Base keyword arguments present for every tool type
    kwargs: dict = {
        "diameter": spec.diameter,
        "flute_length": spec.flute_length,
    }

    tt = spec.tool_type

    if tt == "flat_endmill":
        if spec.corner_radius:
            kwargs["corner_radius"] = spec.corner_radius

    elif tt == "ball_endmill":
        pass  # ball_endmill only uses diameter + flute_length

    elif tt == "bull_nose":
        kwargs["corner_radius"] = spec.corner_radius

    elif tt == "drill":
        kwargs["tip_angle"] = spec.tip_angle if spec.tip_angle else 118.0

    elif tt == "chamfer":
        if spec.tip_diameter:
            kwargs["tip_diameter"] = spec.tip_diameter
        if spec.tip_angle:
            kwargs["tip_angle"] = spec.tip_angle

    elif tt == "dovetail":
        if spec.tip_diameter:
            kwargs["tip_diameter"] = spec.tip_diameter

    elif tt == "thread_mill":
        pass  # approximated as a plain cylinder

    return create_tool(tt, **kwargs)


# =========================================================================
#   Self-test
# =========================================================================

if __name__ == "__main__":
    print("=== SubCAD Tool Library Self-Test ===\n")
    errors: list[str] = []

    # ------------------------------------------------------------------
    # 1. ToolSpec properties
    # ------------------------------------------------------------------
    print("1. ToolSpec properties ...")
    ts = ToolSpec("flat_endmill", 10.0, corner_radius=1.0, num_flutes=4)
    assert ts.tool_type == "flat_endmill"
    assert ts.diameter == 10.0
    assert ts.radius == 5.0
    assert ts.corner_radius == 1.0
    assert ts.num_flutes == 4
    assert ts.coating == "uncoated"
    assert ts.material == "carbide"
    print(f"   diameter={ts.diameter}, radius={ts.radius}, "
          f"tool_type={ts.tool_type}")
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 2. Catalog lookups
    # ------------------------------------------------------------------
    print("2. Catalog lookups ...")
    em10 = ToolCatalog.get("EM_10mm")
    assert em10.tool_type == "flat_endmill"
    assert em10.diameter == 10.0

    bem6 = ToolCatalog.get("BEM_6mm")
    assert bem6.tool_type == "ball_endmill"
    assert bem6.diameter == 6.0

    dr8 = ToolCatalog.get("DR_8mm")
    assert dr8.tool_type == "drill"
    assert dr8.tip_angle == 118.0

    tap_m6 = ToolCatalog.get("TAP_M6")
    assert tap_m6.tool_type == "thread_mill"
    assert tap_m6.diameter == 6.0

    chamf = ToolCatalog.get("CH_10mm_90deg")
    assert chamf.tool_type == "chamfer"
    assert chamf.tip_angle == 90.0

    spot = ToolCatalog.get("SPOT_6mm")
    assert spot.tool_type == "drill"
    assert spot.tip_angle == 120.0

    # Missing tool must raise KeyError
    try:
        ToolCatalog.get("NONEXISTENT")
        errors.append("get('NONEXISTENT') should have raised KeyError")
    except KeyError:
        pass

    print(f"   EM_10mm: {em10}")
    print(f"   BEM_6mm: {bem6}")
    print(f"   DR_8mm: {dr8}")
    print(f"   TAP_M6: {tap_m6}")
    print(f"   CH_10mm_90deg: {chamf}")
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 3. get_best_for auto-selection
    # ------------------------------------------------------------------
    print("3. get_best_for auto-selection ...")

    best = ToolCatalog.get_best_for("flat_endmill", 5.5)
    assert best.diameter == 6.0, f"Expected 6.0, got {best.diameter}"
    print(f"   best flat_endmill >= 5.5 mm:  EM_{best.diameter:.0f}mm")

    best = ToolCatalog.get_best_for("flat_endmill", 11.0)
    assert best.diameter == 12.0, f"Expected 12.0, got {best.diameter}"
    print(f"   best flat_endmill >= 11 mm:  EM_{best.diameter:.0f}mm")

    best = ToolCatalog.get_best_for("flat_endmill", 60.0)
    assert best.diameter == 50.0, \
        f"Fallback: expected 50.0, got {best.diameter}"
    print(f"   best flat_endmill >= 60 mm (fallback):  "
          f"EM_{best.diameter:.0f}mm_FACE")

    best = ToolCatalog.get_best_for("ball_endmill", 7.0)
    assert best.diameter == 10.0, f"Expected 10.0, got {best.diameter}"
    print(f"   best ball_endmill >= 7 mm:  BEM_{best.diameter:.0f}mm")

    try:
        ToolCatalog.get_best_for("laser_cutter", 10.0)
        errors.append("get_best_for('laser_cutter') should have raised"
                       " ValueError")
    except ValueError:
        pass

    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 4. list_all categories
    # ------------------------------------------------------------------
    print("4. list_all categories ...")
    all_cats = ToolCatalog.list_all()
    expected = {"flat_endmills", "ball_endmills", "bull_nose", "drills",
                "chamfer_tools", "taps", "reamers", "spot_drills"}
    actual = set(all_cats.keys())
    missing_cats = expected - actual
    if missing_cats:
        errors.append(f"Missing categories: {missing_cats}")
    for cat in sorted(all_cats.keys()):
        print(f"   {cat}: {len(all_cats[cat])} tools")
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 5. register custom tool
    # ------------------------------------------------------------------
    print("5. register custom tool ...")
    custom = ToolSpec("flat_endmill", 7.5)
    ToolCatalog.register("EM_7.5mm_CUSTOM", custom)
    retrieved = ToolCatalog.get("EM_7.5mm_CUSTOM")
    assert retrieved.diameter == 7.5
    assert "custom" in ToolCatalog.list_all()
    # Duplicate registration must raise
    try:
        ToolCatalog.register("EM_7.5mm_CUSTOM", custom)
        errors.append("Duplicate register() should have raised ValueError")
    except ValueError:
        pass
    print(f"   Registered and retrieved: {retrieved}")
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 6. to_sim_tool bridge
    # ------------------------------------------------------------------
    print("6. to_sim_tool bridge ...")
    try:
        from src.simulation.tools import FlatEndmill, BallEndmill, Drill

        spec1 = ToolSpec("flat_endmill", 10.0, flute_length=30.0)
        sim1 = to_sim_tool(spec1)
        assert sim1 is not None, "to_sim_tool returned None"
        assert sim1.diameter == 10.0
        assert sim1.flute_length == 30.0
        assert isinstance(sim1, FlatEndmill)
        print(f"   flat_endmill: {sim1}")

        spec2 = ToolSpec("ball_endmill", 6.0, flute_length=25.0)
        sim2 = to_sim_tool(spec2)
        assert sim2 is not None
        assert sim2.diameter == 6.0
        assert isinstance(sim2, BallEndmill)
        print(f"   ball_endmill: {sim2}")

        spec3 = ToolSpec("drill", 8.0, tip_angle=118.0)
        sim3 = to_sim_tool(spec3)
        assert sim3 is not None
        assert sim3.diameter == 8.0
        assert isinstance(sim3, Drill)
        print(f"   drill: {sim3}")

        print("   PASSED\n")
    except ImportError:
        print("   SKIPPED (simulation module not available)\n")
    except Exception as exc:
        errors.append(f"to_sim_tool bridge: {exc}")
        print(f"   FAILED: {exc}\n")

    # ------------------------------------------------------------------
    # Final report
    # ------------------------------------------------------------------
    if errors:
        print("=== TESTS COMPLETED WITH ERRORS ===")
        for err in errors:
            print(f"  ERROR: {err}")
        raise SystemExit(1)
    else:
        print("=== ALL TESTS PASSED ===")
