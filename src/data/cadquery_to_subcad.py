"""CadQuery ops trace analysis: extract chains, measures, and stock dimensions.

Used by the agentic translator to understand a CadQuery program's structure
before translating it to subCAD.  Provides:

- **Chain reconstruction**: group flattened ops trace entries into logical
  operation chains (e.g., sketch -> extrude -> cut).
- **Chain classification**: label each chain as stock, pocket, hole, boss, etc.
- **STEP bounding box**: read a STEP file and compute oversize stock dimensions.
- **Measure extraction**: pull out named numeric parameters from the trace.

Key design notes:
  - STEP files are loaded via CadQuery (``cadquery.importers.importStep``).
    The ``cascadio`` module is not available, so ``trimesh.load()`` is NOT
    used for STEP files.
  - The ops trace format is a list of dicts.  Each entry has at minimum
    ``lineno`` and ``function`` keys.  Extra keys (``args``, ``kwargs``,
    ``result``) are preserved but optional.
"""

from __future__ import annotations

import json
import os
import tempfile
from typing import Optional, Union


# ---------------------------------------------------------------------------
#  Guard: CadQuery availability
# ---------------------------------------------------------------------------

_HAS_CADQUERY = False
try:
    import cadquery as cq
    _HAS_CADQUERY = True
except ImportError:
    pass


# =============================================================================
#  Chain reconstruction
# =============================================================================

# Operations that begin a new logical chain.
_CHAIN_STARTERS: set[str] = frozenset({
    # Workplane constructors
    "Workplane",
    # Face selection (starts a new workplane context)
    "faces",
    # Construction helpers
    "newObject",
    "tag",
    # Stock-level ops
    "box", "cylinder", "sphere", "cone",
})

# Operations that are intermediate sketching / transformation steps.
_CHAIN_CONTINUERS: set[str] = frozenset({
    "workplane",
    "center",
    "transformed",
    "rotate",
    "moveTo",
    "lineTo",
    "line",
    "threePointArc",
    "sagittaArc",
    "radiusArc",
    "ellipseArc",
    "spline",
    "close",
    "rect",
    "circle",
    "ellipse",
    "polygon",
    "slot2D",
    "rarray",
    "pushPoints",
    "hLine",
    "vLine",
    "polarArray",
    "mirrorX",
    "mirrorY",
    "offset2D",
    "placeSketch",
})

# Operations that are terminal: they produce a 3D solid (end of chain).
_CHAIN_TERMINATORS: set[str] = frozenset({
    "extrude",
    "cutBlind",
    "cutThruAll",
    "loft",
    "revolve",
    "sweep",
    "shell",
    "chamfer",
    "fillet",
    "cboreHole",
    "cskHole",
    "hole",
    "combine",
    "union",
    "cut",
    "intersect",
    "split",
})


def reconstruct_chains(ops_trace: list[dict]) -> list[dict]:
    """Group a flattened CadQuery ops trace into logical operation chains.

    A chain is a sequence of calls that together form one geometric operation
    (e.g., select top face -> sketch rectangle -> extrude-cut to make a pocket).
    The flattened trace is split at each "chain starter" (new Workplane, face
    selection) and each chain ends at its terminal 3D operation.

    Args:
        ops_trace: List of dicts.  Each dict must have at minimum ``lineno``
                   and ``function`` keys.  Typical extras: ``args``, ``kwargs``,
                   ``function_path``.

    Returns:
        List of chain dicts, each with keys:
        - ``lineno``: starting line number (int)
        - ``function_path``: dot-joined chain description (str)
        - ``chain_type``: classification string (set by :func:`classify_chain`)
        - ``children``: list of the original trace entries in this chain
    """
    if not ops_trace:
        return []

    chains: list[dict] = []
    current_chain: list[dict] = []

    for entry in ops_trace:
        # Normalize the entry — ensure it's a dict with expected keys
        if not isinstance(entry, dict):
            continue

        func = _resolve_function_name(entry)

        # A chain starter begins a new chain (flush previous first)
        if func in _CHAIN_STARTERS:
            if current_chain:
                chains.append(_build_chain(current_chain))
            current_chain = [entry]
            continue

        # If we don't have an active chain yet, start one
        if not current_chain:
            current_chain = [entry]
            continue

        # Append to current chain
        current_chain.append(entry)

        # A terminator ends the chain
        if func in _CHAIN_TERMINATORS:
            chains.append(_build_chain(current_chain))
            current_chain = []
            continue

    # Flush any remaining entries
    if current_chain:
        chains.append(_build_chain(current_chain))

    return chains


def _build_chain(entries: list[dict]) -> dict:
    """Build a chain dict from a list of trace entries."""
    lineno = entries[0].get("lineno", entries[0].get("line", 0))
    if isinstance(lineno, str):
        try:
            lineno = int(lineno)
        except (ValueError, TypeError):
            lineno = 0

    # Build a readable function path
    func_names = []
    for e in entries:
        fn = _resolve_function_name(e)
        if fn:
            func_names.append(fn)

    function_path = " -> ".join(func_names)

    chain = {
        "lineno": lineno,
        "function_path": function_path,
        "chain_type": "unknown",
        "children": entries,
    }

    # Pre-classify the chain
    chain["chain_type"] = classify_chain(chain)

    return chain


def _resolve_function_name(entry: dict) -> str:
    """Extract the short function name from a trace entry.

    Handles various formats:
      - ``"function": "Workplane.box"`` -> ``"box"``
      - ``"function": "box"`` -> ``"box"``
      - ``"call": "extrude"`` -> ``"extrude"``
      - ``"op": "cutBlind"`` -> ``"cutBlind"``
    """
    # Try standard keys
    for key in ("function", "call", "op", "method", "name"):
        val = entry.get(key)
        if isinstance(val, str) and val:
            # Strip class prefix: "Workplane.box" -> "box"
            return val.rsplit(".", 1)[-1]

    # Try function_path
    fp = entry.get("function_path")
    if isinstance(fp, str) and fp:
        # "Workplane.faces.workplane.rect.cutBlind" -> "cutBlind"
        parts = fp.split(".")
        return parts[-1]

    return ""


# =============================================================================
#  Chain classification
# =============================================================================

def classify_chain(chain: dict) -> str:
    """Classify a reconstructed chain as a specific operation type.

    Uses the ``function_path`` and ``children`` of the chain to determine
    what geometric operation it represents.

    Args:
        chain: A chain dict from :func:`reconstruct_chains`, or any dict
               with a ``function_path`` (str) key.

    Returns:
        One of:
        ``"stock"``, ``"pocket"``, ``"hole"``, ``"boss"``, ``"cutout"``,
        ``"chamfer"``, ``"fillet"``, ``"contour"``, ``"unknown"``.
    """
    fp = chain.get("function_path", "")
    fp_lower = fp.lower()

    # --- Stock creation ---
    if any(keyword in fp_lower for keyword in ("box", "cylinder", "sphere")):
        # A box/cylinder/sphere without a preceding faces() is stock
        # If faces is in the path, it's probably a feature, not stock
        if "faces" not in fp_lower:
            return "stock"

    # --- Chamfer ---
    if "chamfer" in fp_lower:
        return "chamfer"

    # --- Fillet ---
    if "fillet" in fp_lower:
        return "fillet"

    # --- Hole operations ---
    if any(kw in fp_lower for kw in ("cborehole", "cskhole", "hole")):
        return "hole"

    # --- Drill / circular cut ---
    if "circle" in fp_lower and any(
        kw in fp_lower for kw in ("cutblind", "cutthruall")
    ):
        return "hole"

    # --- Pocket (rectangular cut) ---
    if "rect" in fp_lower and any(
        kw in fp_lower for kw in ("cutblind", "cutthruall")
    ):
        return "pocket"

    if "slot2d" in fp_lower and any(
        kw in fp_lower for kw in ("cutblind", "cutthruall")
    ):
        return "pocket"

    # --- Boss / extrusion (additive) ---
    if any(kw in fp_lower for kw in ("extrude", "loft", "revolve", "sweep")):
        # Extrude/cutBlind means subtractive, extrude alone means additive
        if any(kw in fp_lower for kw in ("cutblind", "cutthruall", "cut")):
            # Has both extrude and cut -> probably a pocket
            if "rect" in fp_lower:
                return "pocket"
            if "circle" in fp_lower:
                return "hole"
            return "cutout"
        return "boss"

    # --- Cut / subtract operations ---
    if any(kw in fp_lower for kw in ("cutblind", "cutthruall")):
        return "cutout"

    if "union" in fp_lower:
        return "boss"

    if "cut" in fp_lower or "intersect" in fp_lower:
        return "cutout"

    # --- Contour / shell ---
    if "shell" in fp_lower:
        return "contour"
    if "contour" in fp_lower:
        return "contour"

    # --- Fallback: analyze children for clues ---
    children = chain.get("children", [])
    if children:
        for child in children:
            fn = _resolve_function_name(child)
            if fn in ("chamfer",):
                return "chamfer"
            if fn in ("fillet",):
                return "fillet"
            if fn in ("cboreHole", "cskHole", "hole"):
                return "hole"

    return "unknown"


# =============================================================================
#  STEP -> stock dimensions
# =============================================================================

def step_to_stock_dims(
    step_input: Union[str, bytes, bytearray],
    margin: float = 10.0,
) -> dict:
    """Compute oversize stock dimensions from a STEP file.

    Reads the STEP geometry (passed as a file path, or raw bytes), computes
    its bounding box, and adds *margin* mm on each side.

    Uses CadQuery's built-in STEP importer.  ``cascadio`` is unavailable, so
    ``trimesh.load()`` is NOT used.

    Args:
        step_input: Either a file path (str) or raw STEP file bytes (bytes).
        margin: Extra material added to each side of the bounding box (mm).
                Default 10.0 mm.

    Returns:
        ``{"length": float, "width": float, "height": float}``
        All values are in mm.
    """
    if not _HAS_CADQUERY:
        raise RuntimeError(
            "CadQuery is required for STEP import. "
            "Install with: pip install cadquery"
        )

    # Resolve input: if bytes, write to a temp file first
    if isinstance(step_input, (bytes, bytearray)):
        fd, tmp_path = tempfile.mkstemp(suffix=".step")
        os.close(fd)
        try:
            with open(tmp_path, "wb") as f:
                f.write(step_input)
            return _step_path_to_stock_dims(tmp_path, margin)
        finally:
            os.unlink(tmp_path)

    # Assume it's a file path
    return _step_path_to_stock_dims(str(step_input), margin)


def _step_path_to_stock_dims(step_path: str, margin: float) -> dict:
    """Core implementation: load STEP from path and compute bbox + margin."""
    shape = cq.importers.importStep(step_path)
    bbox = shape.val().BoundingBox()

    length = (bbox.xmax - bbox.xmin) + 2.0 * margin
    width = (bbox.ymax - bbox.ymin) + 2.0 * margin
    height = (bbox.zmax - bbox.zmin) + margin  # only one margin in Z

    return {
        "length": round(length, 2),
        "width": round(width, 2),
        "height": round(height, 2),
    }


# =============================================================================
#  Measure extraction
# =============================================================================

# Mapping from function names to the measure name we assign their arguments.
# Each entry: (arg_index, measure_name)
# For kwargs-based entries we also search kwargs dicts.
_DEFAULT_MEASURE_MAP: dict[str, dict[int, str]] = {
    # --- Holes ---
    "cboreHole": {0: "bore_diameter", 1: "bore_depth"},
    "cskHole":   {0: "sink_diameter", 1: "sink_angle"},
    "hole":      {0: "hole_diameter", 1: "hole_depth"},
    "circle":    {0: "radius", "kwargs_diameter": "diameter"},
    # --- Rectangular features ---
    "rect":      {0: "width", 1: "length"},
    "box":       {0: "length", 1: "width", 2: "height"},
    "cylinder":  {0: "height", 1: "radius", "kwargs_diameter": "diameter"},
    # --- Extrusion / cut ---
    "extrude":   {0: "extrude_distance"},
    "cutBlind":  {0: "cut_depth"},
    "cutThruAll": {"kwargs_depth": "cut_depth"},
    # --- Pocket / slot ---
    "slot2D":    {0: "slot_length", 1: "slot_width"},
    # --- Chamfer / fillet ---
    "chamfer":   {0: "chamfer_width"},
    "fillet":    {0: "fillet_radius"},
    # --- Shell ---
    "shell":     {0: "shell_thickness"},
}


def _extract_measures(ops_trace: list[dict]) -> dict:
    """Extract named measurements from a CadQuery ops trace.

    Scans the flattened trace for numeric positional arguments and keyword
    arguments and maps them to descriptive names (e.g., ``hole_diameter``,
    ``cut_depth``, ``fillet_radius``).

    Args:
        ops_trace: List of dicts from a CadQuery ops trace.  Each entry
                   should have at minimum a ``function`` key.  Optional keys:
                   ``args`` (list), ``kwargs`` (dict), ``params`` (dict).

    Returns:
        ``{name: value}`` dict.  Values are the raw numbers from the trace
        (floats, ints) or short strings.  Duplicate names are overwritten
        by later entries (last one wins).
    """
    measures: dict = {}

    for entry in ops_trace:
        if not isinstance(entry, dict):
            continue

        func = _resolve_function_name(entry)
        if not func:
            continue

        mapping = _DEFAULT_MEASURE_MAP.get(func)
        if mapping is None:
            continue

        args = entry.get("args", [])
        kwargs = entry.get("kwargs", {})
        params = entry.get("params", {})

        # Merge kwargs and params (params is an alternative name)
        all_kwargs = {}
        if isinstance(kwargs, dict):
            all_kwargs.update(kwargs)
        if isinstance(params, dict):
            all_kwargs.update(params)

        # Gather the set of known measure names for this function's mapping
        known_measures = set(mapping.values())

        for map_key, measure_name in mapping.items():
            if isinstance(map_key, int):
                # Positional arg
                if map_key < len(args):
                    val = args[map_key]
                    if _is_numeric(val):
                        measures[measure_name] = val
            elif isinstance(map_key, str) and map_key.startswith("kwargs_"):
                # Keyword arg lookup
                kw_name = map_key[len("kwargs_"):]
                if kw_name in all_kwargs:
                    val = all_kwargs[kw_name]
                    if _is_numeric(val):
                        measures[measure_name] = val
            elif isinstance(map_key, str):
                # Direct kwarg name
                if map_key in all_kwargs:
                    val = all_kwargs[map_key]
                    if _is_numeric(val):
                        measures[measure_name] = val

        # Also capture any kwargs/params whose key directly matches a known
        # measure name (e.g., rect(width=30, length=20) where the mapping
        # already maps positional args to "width" and "length")
        for kw_key, kw_val in all_kwargs.items():
            if kw_key in known_measures and _is_numeric(kw_val):
                measures[kw_key] = kw_val

    return measures


def _is_numeric(val) -> bool:
    """Return True for ints and floats (not bools, not strings)."""
    if isinstance(val, bool):
        return False
    if isinstance(val, (int, float)):
        return True
    # Try to convert string to numeric
    if isinstance(val, str):
        try:
            float(val)
            return True
        except (ValueError, TypeError):
            pass
    return False


# =============================================================================
#  Self-test
# =============================================================================

if __name__ == "__main__":
    import sys

    print("=== cadquery_to_subcad Self-Test ===\n")

    _counts = {"passed": 0, "failed": 0}

    def _check(label: str, condition: bool, detail: str = ""):
        if condition:
            _counts["passed"] += 1
            print(f"  PASS  {label}")
        else:
            _counts["failed"] += 1
            print(f"  FAIL  {label}  -- {detail}")

    # ------------------------------------------------------------------
    # Test 1: reconstruct_chains with typical ops trace
    # ------------------------------------------------------------------
    print("1. reconstruct_chains ...")
    trace = [
        {"lineno": 3, "function": "Workplane"},
        {"lineno": 4, "function": "box", "args": [100, 50, 20]},
        {"lineno": 8, "function": "faces", "args": [">Z"]},
        {"lineno": 9, "function": "workplane"},
        {"lineno": 10, "function": "rect", "args": [30, 20]},
        {"lineno": 11, "function": "cutBlind", "args": [-5]},
        {"lineno": 15, "function": "faces", "args": [">Z"]},
        {"lineno": 16, "function": "workplane"},
        {"lineno": 17, "function": "circle", "args": [5]},
        {"lineno": 18, "function": "cutThruAll"},
        {"lineno": 22, "function": "chamfer", "args": [0.5]},
    ]
    chains = reconstruct_chains(trace)
    _check("got chains", len(chains) >= 1, f"got {len(chains)}")
    _check("each chain has lineno", all("lineno" in c for c in chains))
    _check("each chain has function_path", all("function_path" in c for c in chains))
    _check("each chain has chain_type", all("chain_type" in c for c in chains))
    _check("each chain has children", all("children" in c for c in chains))

    # Show chains for debugging
    for c in chains:
        print(f"    [{c['chain_type']}] {c['function_path']}")

    # Check classification
    types_found = [c["chain_type"] for c in chains]
    _check("stock chain found", "stock" in types_found, f"types: {types_found}")
    _check("pocket chain found", "pocket" in types_found, f"types: {types_found}")
    _check("hole chain found", "hole" in types_found, f"types: {types_found}")
    _check("chamfer chain found", "chamfer" in types_found, f"types: {types_found}")
    print()

    # ------------------------------------------------------------------
    # Test 2: classify_chain for each known type
    # ------------------------------------------------------------------
    print("2. classify_chain ...")
    tests = [
        ({"function_path": "Workplane -> box"}, "stock"),
        ({"function_path": "faces -> workplane -> rect -> cutBlind"}, "pocket"),
        ({"function_path": "faces -> workplane -> circle -> cutThruAll"}, "hole"),
        ({"function_path": "cboreHole"}, "hole"),
        ({"function_path": "Workplane -> rect -> extrude"}, "boss"),
        ({"function_path": "chamfer"}, "chamfer"),
        ({"function_path": "fillet"}, "fillet"),
        ({"function_path": "faces -> workplane -> slot2D -> cutBlind"}, "pocket"),
        ({"function_path": "Workplane -> rect -> extrude -> cutBlind"}, "pocket"),
        ({"function_path": "Workplane.cylinder"}, "stock"),
        ({"function_path": "union"}, "boss"),
        ({"function_path": "shell"}, "contour"),
        ({"function_path": "some_unknown_operation"}, "unknown"),
    ]
    for chain, expected in tests:
        got = classify_chain(chain)
        _check(f"{chain['function_path'][:50]:50s} -> {expected}",
               got == expected, f"got {got}")
    print()

    # ------------------------------------------------------------------
    # Test 3: empty ops trace
    # ------------------------------------------------------------------
    print("3. empty / invalid inputs ...")
    _check("empty trace -> []", reconstruct_chains([]) == [])
    _check("classify empty chain", classify_chain({}) == "unknown")
    _check("empty measures", _extract_measures([]) == {})
    print()

    # ------------------------------------------------------------------
    # Test 4: _extract_measures
    # ------------------------------------------------------------------
    print("4. _extract_measures ...")
    trace2 = [
        {"lineno": 5, "function": "box", "args": [100, 50, 20]},
        {"lineno": 10, "function": "rect", "args": [30, 20]},
        {"lineno": 12, "function": "cutBlind", "args": [-5]},
        {"lineno": 16, "function": "circle", "args": [6]},
        {"lineno": 20, "function": "chamfer", "args": [1.0]},
        {"lineno": 24, "function": "fillet", "args": [2.5]},
        {"lineno": 28, "function": "cboreHole", "args": [8, 12]},
        {"lineno": 30, "function": "rect", "kwargs": {"length": 40, "width": 15}},
    ]
    measures = _extract_measures(trace2)
    _check("length measure present", measures.get("length") in (20, 40, 100, 50),
           f"measures: {measures}")
    _check("width measure present", measures.get("width") in (15, 30, 50),
           f"measures: {measures}")
    _check("box height=20", measures.get("height") == 20, f"measures: {measures}")
    _check("cut depth=5", abs(measures.get("cut_depth", 0)) == 5,
           f"cut_depth={measures.get('cut_depth')}")
    _check("chamfer width=1.0", measures.get("chamfer_width") == 1.0)
    _check("fillet radius=2.5", measures.get("fillet_radius") == 2.5)
    _check("cboreHole diameter=8", measures.get("bore_diameter") == 8)
    print()

    # ------------------------------------------------------------------
    # Test 5: step_to_stock_dims (requires CadQuery)
    # ------------------------------------------------------------------
    print("5. step_to_stock_dims ...")
    if not _HAS_CADQUERY:
        print("  SKIP: cadquery not installed")
    else:
        # Create a simple box, export to STEP, then read back
        try:
            fd, step_path = tempfile.mkstemp(suffix=".step")
            os.close(fd)
            shape = cq.Workplane("XY").box(100, 60, 25)
            cq.exporters.export(shape, step_path)

            # Test with path string
            dims = step_to_stock_dims(step_path, margin=5.0)
            _check("length ~110", abs(dims["length"] - 110) < 5.0,
                   f"got {dims['length']}")
            _check("width ~70", abs(dims["width"] - 70) < 5.0,
                   f"got {dims['width']}")
            _check("height ~30", abs(dims["height"] - 30) < 5.0,
                   f"got {dims['height']}")

            # Test with bytes
            with open(step_path, "rb") as f:
                step_bytes = f.read()
            dims_bytes = step_to_stock_dims(step_bytes, margin=10.0)
            _check("bytes: length ~120", abs(dims_bytes["length"] - 120) < 5.0,
                   f"got {dims_bytes['length']}")
            _check("bytes: width ~80", abs(dims_bytes["width"] - 80) < 5.0,
                   f"got {dims_bytes['width']}")

            os.unlink(step_path)
        except Exception as e:
            _check("step_to_stock_dims raised", False, str(e))
    print()

    # ------------------------------------------------------------------
    # Test 6: ops trace with alternate key names
    # ------------------------------------------------------------------
    print("6. ops trace with alternate key names ...")
    trace3 = [
        {"line": 5, "call": "box", "args": [80, 40, 15]},
        {"line": 10, "method": "faces"},
        {"line": 11, "method": "workplane"},
        {"line": 12, "call": "circle", "params": {"diameter": 10}},
        {"line": 13, "call": "cutBlind", "args": [-8]},
    ]
    chains3 = reconstruct_chains(trace3)
    _check("found chains from alternate keys", len(chains3) > 0,
           f"got {len(chains3)}")
    _check("first chain has function_path",
           len(chains3[0]["function_path"]) > 0)

    # Check function name resolution
    func_names = [_resolve_function_name(e) for e in trace3]
    _check("resolved function names",
           func_names == ["box", "faces", "workplane", "circle", "cutBlind"],
           f"got {func_names}")
    print()

    # ------------------------------------------------------------------
    # Test 7: classify_chain with complex paths
    # ------------------------------------------------------------------
    print("7. classify_chain with complex paths ...")
    complex_tests = [
        ("Workplane -> faces -> workplane -> rect -> extrude", "boss"),
        ("faces -> workplane -> circle -> extrude", "boss"),
        ("Workplane -> faces -> workplane -> slot2D -> cutThruAll", "pocket"),
        ("Workplane -> faces -> workplane -> rect -> cutBlind", "pocket"),
        ("faces -> workplane -> circle -> cutThruAll", "hole"),
    ]
    for fp, expected in complex_tests:
        got = classify_chain({"function_path": fp})
        _check(f"{fp[:60]:60s} -> {expected}",
               got == expected, f"got {got}")
    print()

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    total = _counts["passed"] + _counts["failed"]
    print(f"=== {'ALL TESTS PASSED' if _counts['failed'] == 0 else 'SOME TESTS FAILED'} "
          f"({_counts['passed']}/{total} passed) ===")
    if _counts["failed"] > 0:
        sys.exit(1)
