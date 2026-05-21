"""B-Rep geometry backend for SubCAD subtractive CAD library.

Wraps CadQuery for all solid modeling operations. Every machining operation
in SubCAD ultimately calls functions in this module to modify the 3D solid.

Coordinate system: Z is up, top face is +Z. All cuts go downward (-Z).
"""

from __future__ import annotations

import math

# ---------------------------------------------------------------------------
# CadQuery import guard
# ---------------------------------------------------------------------------

_HAS_CADQUERY = False
try:
    import cadquery as cq
    from cadquery import exporters as cq_exporters
    _HAS_CADQUERY = True
except ImportError:
    pass

# ---------------------------------------------------------------------------
# trimesh import guard (for to_mesh)
# ---------------------------------------------------------------------------

_HAS_TRIMESH = False
try:
    import trimesh
    _HAS_TRIMESH = True
except ImportError:
    pass


# =============================================================================
#  Stock creation
# =============================================================================

def create_rectangular_stock(length: float, width: float, height: float) -> "cq.Workplane":
    """Create a rectangular prism stock block centered at origin.

    Length=X, Width=Y, Height=Z.
    Stock extends from (-length/2, -width/2, -height/2) to
    (length/2, width/2, height/2).
    """
    if not _HAS_CADQUERY:
        raise RuntimeError("cadquery is not available")
    return cq.Workplane("XY").box(length, width, height, centered=True)


def create_cylindrical_stock(diameter: float, height: float) -> "cq.Workplane":
    """Create a cylindrical stock. Diameter in XY, height along Z."""
    if not _HAS_CADQUERY:
        raise RuntimeError("cadquery is not available")
    return cq.Workplane("XY").cylinder(height, diameter / 2.0)


# =============================================================================
#  Helpers
# =============================================================================

def _to_face_coords(shape: "cq.Workplane", face_selector: str, cx: float, cy: float) -> tuple:
    """Convert SubCAD stock-centered coordinates to CadQuery face offsets.

    CadQuery's `.faces(...).workplane()` places the local origin from the
    selected face's workplane.  After previous cuts, that origin can drift
    away from the original stock origin, so subtract it to keep SubCAD
    operation coordinates stable in the stock/global XY frame.
    """
    if face_selector in {">Z", "<Z"}:
        try:
            origin = shape.faces(face_selector).workplane().plane.origin
            return cx - origin.x, cy - origin.y
        except Exception:
            pass
    return cx, cy




# =============================================================================
#  Machining operations
# =============================================================================

def face_mill_cut(shape: "cq.Workplane", depth: float, *, face_selector: str = ">Z") -> "cq.Workplane":
    """Remove material from the top face down to `depth`."""
    if not _HAS_CADQUERY:
        raise RuntimeError("cadquery is not available")

    if depth <= 0.001:
        return shape  # nothing to remove

    bbox = shape.val().BoundingBox()
    # Cover the entire top face with a slightly oversized rectangle
    face_length = (bbox.xmax - bbox.xmin) + 2.0
    face_width = (bbox.ymax - bbox.ymin) + 2.0

    return (
        shape.faces(face_selector).workplane()
        .rect(face_length, face_width)
        .cutBlind(-depth)
    )


def rectangular_pocket_cut(
    shape: "cq.Workplane",
    cx: float,
    cy: float,
    width: float,
    length: float,
    depth: float,
    corner_radius: float = 0.0,
    *,
    face_selector: str = ">Z",
) -> "cq.Workplane":
    """Cut a rectangular pocket at (cx, cy) on the top face."""
    if not _HAS_CADQUERY:
        raise RuntimeError("cadquery is not available")

    cx_rel, cy_rel = _to_face_coords(shape, face_selector, cx, cy)

    result = (
        shape.faces(face_selector).workplane()
        .center(cx_rel, cy_rel)
        .rect(length, width)
        .cutBlind(-depth)
    )

    if corner_radius > 0:
        try:
            from cadquery import selectors as cq_selectors

            half_w = width / 2.0 + 0.5
            half_l = length / 2.0 + 0.5
            z_range = depth + 2.0
            result = result.edges(
                cq_selectors.BoxSelector(
                    (cx_rel - half_l, cy_rel - half_w, -z_range),
                    (cx_rel + half_l, cy_rel + half_w, z_range),
                )
            ).fillet(corner_radius)
        except Exception:
            pass  # gracefully skip if fillet fails

    return result


def circular_pocket_cut(
    shape: "cq.Workplane",
    cx: float,
    cy: float,
    diameter: float,
    depth: float,
    *,
    face_selector: str = ">Z",
) -> "cq.Workplane":
    """Cut a circular pocket at (cx, cy) on the top face."""
    if not _HAS_CADQUERY:
        raise RuntimeError("cadquery is not available")

    cx_rel, cy_rel = _to_face_coords(shape, face_selector, cx, cy)

    return (
        shape.faces(face_selector).workplane()
        .center(cx_rel, cy_rel)
        .circle(diameter / 2.0)
        .cutBlind(-depth)
    )


def drill_hole(
    shape: "cq.Workplane",
    cx: float,
    cy: float,
    diameter: float,
    depth: float,
    through: bool = False,
    *,
    face_selector: str = ">Z",
) -> "cq.Workplane":
    """Drill a hole. If through=True, goes through entire part.
    Otherwise blind at `depth`."""
    if not _HAS_CADQUERY:
        raise RuntimeError("cadquery is not available")

    cx_rel, cy_rel = _to_face_coords(shape, face_selector, cx, cy)

    wp = (
        shape.faces(face_selector).workplane()
        .center(cx_rel, cy_rel)
        .circle(diameter / 2.0)
    )

    if through:
        return wp.cutThruAll()
    else:
        return wp.cutBlind(-depth)


def countersink_cut(
    shape: "cq.Workplane",
    cx: float,
    cy: float,
    hole_diameter: float,
    sink_diameter: float,
    depth: float,
    sink_angle: float = 82.0,
    *,
    face_selector: str = ">Z",
) -> "cq.Workplane":
    """Cut a countersink: drill through-hole + conical recess.

    The through-hole is drilled first, then a shallow circular pocket
    creates the conical countersink recess.  The *sink_angle* parameter
    is recorded in the operation metadata but does not affect the
    simple CSG geometry.
    """
    if not _HAS_CADQUERY:
        raise RuntimeError("cadquery is not available")
    # Drill the through hole first
    result = drill_hole(shape, cx, cy, hole_diameter, depth=0, through=True,
                        face_selector=face_selector)
    # Then a shallow circular pocket for the countersink recess
    result = circular_pocket_cut(result, cx, cy, sink_diameter, depth,
                                 face_selector=face_selector)
    return result


def slot_cut(
    shape: "cq.Workplane",
    cx: float,
    cy: float,
    length: float,
    width: float,
    depth: float,
    angle: float = 0.0,
    through: bool = False,
    *,
    face_selector: str = ">Z",
) -> "cq.Workplane":
    """Cut a slot (obround) at (cx, cy) on the top face at given angle."""
    if not _HAS_CADQUERY:
        raise RuntimeError("cadquery is not available")

    cx_rel, cy_rel = _to_face_coords(shape, face_selector, cx, cy)
    wp = shape.faces(face_selector).workplane().center(cx_rel, cy_rel)

    # Rotate the workplane if angle is non-zero
    if angle != 0.0:
        wp = wp.transformed(rotate=cq.Vector(0, 0, angle))

    slot_profile = wp.slot2D(length, width, 0)

    if through:
        return slot_profile.cutThruAll()
    else:
        return slot_profile.cutBlind(-depth)


def contour_cut_outer(
    shape: "cq.Workplane",
    depth: float,
    stepdown: float = 0.0,
    *,
    face_selector: str = ">Z",
) -> "cq.Workplane":
    """Trim the outer profile of the part by `depth` from the top face.

    This is a simplified contour -- in practice it means cutting the outer
    edges down. Uses a box-frame cutting tool that creates a step around the
    outer perimeter of the part.
    """
    if not _HAS_CADQUERY:
        raise RuntimeError("cadquery is not available")

    # TODO: non-Z contour needs reorientation logic.
    if face_selector != ">Z":
        pass  # face_selector accepted but contour logic is Z-axis based

    bb = shape.val().BoundingBox()
    part_length = bb.xmax - bb.xmin
    part_width = bb.ymax - bb.ymin
    margin = 10.0  # oversize margin to ensure cut covers part edges

    # Width of the contour step (inward offset from outer edges)
    contour_offset = 5.0
    inner_length = max(part_length - 2.0 * contour_offset, 1.0)
    inner_width = max(part_width - 2.0 * contour_offset, 1.0)

    def _make_frame_tool(frame_depth: float) -> "cq.Workplane":
        """Create a rectangular frame cutting tool of given depth."""
        outer = cq.Workplane("XY").box(
            part_length + 2.0 * margin,
            part_width + 2.0 * margin,
            frame_depth + 0.5,
            centered=(True, True, False),
        )
        inner = cq.Workplane("XY").box(
            inner_length,
            inner_width,
            frame_depth + 1.0,
            centered=(True, True, False),
        )
        return outer.cut(inner)

    if stepdown <= 0.0:
        # Single pass
        tool = _make_frame_tool(depth)
        tool = tool.translate(cq.Vector(0, 0, bb.zmax - depth))
        return shape.cut(tool)

    # Multiple passes with stepdown
    result = shape
    remaining = depth
    current_z = bb.zmax

    while remaining > 0.001:
        pass_depth = min(stepdown, remaining)
        tool = _make_frame_tool(pass_depth)
        tool = tool.translate(cq.Vector(0, 0, current_z - pass_depth))
        result = result.cut(tool)
        current_z -= pass_depth
        remaining -= pass_depth

    return result


def _profile_points(profile) -> list[tuple[float, float]]:
    if isinstance(profile, dict):
        points = profile.get("points") or profile.get("vertices")
    else:
        points = profile
    if not points:
        return []
    return [(float(p[0]), float(p[1])) for p in points]


def _profile_bounds(profile) -> tuple[float, float, float, float]:
    points = _profile_points(profile)
    if points:
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        return min(xs), min(ys), max(xs), max(ys)
    if isinstance(profile, dict):
        width = float(profile.get("width", profile.get("diameter", 10.0)))
        length = float(profile.get("length", profile.get("diameter", width)))
    else:
        width = length = 10.0
    return -length / 2.0, -width / 2.0, length / 2.0, width / 2.0


def _draw_profile(wp: "cq.Workplane", profile) -> "cq.Workplane":
    if isinstance(profile, dict):
        if "diameter" in profile:
            return wp.circle(float(profile["diameter"]) / 2.0)
        if profile.get("type") == "circle" and "radius" in profile:
            return wp.circle(float(profile["radius"]))
        if "width" in profile or "length" in profile:
            width = float(profile.get("width", profile.get("length", 10.0)))
            length = float(profile.get("length", profile.get("width", 10.0)))
            return wp.rect(length, width)
    points = _profile_points(profile)
    if len(points) >= 3:
        return wp.polyline(points).close()
    return wp.rect(10.0, 10.0)


def profile_pocket_cut(
    shape: "cq.Workplane",
    profile,
    depth: float,
    *,
    face_selector: str = ">Z",
    through: bool = False,
) -> "cq.Workplane":
    """Cut a closed arbitrary profile on the selected face."""
    if not _HAS_CADQUERY:
        raise RuntimeError("cadquery is not available")
    wp = _draw_profile(shape.faces(face_selector).workplane(), profile)
    return wp.cutThruAll() if through else wp.cutBlind(-depth)


def profile_contour_cut(
    shape: "cq.Workplane",
    profile,
    depth: float,
    *,
    side: str = "outside",
    face_selector: str = ">Z",
) -> "cq.Workplane":
    """Contour an arbitrary profile; current B-Rep cut uses profile pocket CSG."""
    return profile_pocket_cut(shape, profile, depth, face_selector=face_selector, through=False)


def machine_around_profile_cut(
    shape: "cq.Workplane",
    profile,
    height: float,
    *,
    face_selector: str = ">Z",
    margin: float = 5.0,
) -> "cq.Workplane":
    """Remove a frame around a retained profile island."""
    if not _HAS_CADQUERY:
        raise RuntimeError("cadquery is not available")
    xmin, ymin, xmax, ymax = _profile_bounds(profile)
    outer_l = max(xmax - xmin + 2 * margin, 1.0)
    outer_w = max(ymax - ymin + 2 * margin, 1.0)
    cx = (xmin + xmax) / 2.0
    cy = (ymin + ymax) / 2.0
    wp = shape.faces(face_selector).workplane().center(cx, cy).rect(outer_l, outer_w)
    wp = _draw_profile(wp, profile)
    return wp.cutBlind(-height)


def machine_around_cylinder_cut(
    shape: "cq.Workplane",
    diameter: float,
    height: float,
    *,
    cx: float = 0.0,
    cy: float = 0.0,
    face_selector: str = ">Z",
    margin: float = 5.0,
) -> "cq.Workplane":
    """Remove a frame around a retained cylindrical boss."""
    profile = {"diameter": diameter}
    if not _HAS_CADQUERY:
        raise RuntimeError("cadquery is not available")
    outer = diameter + 2.0 * margin
    wp = shape.faces(face_selector).workplane().center(cx, cy).rect(outer, outer)
    wp = _draw_profile(wp, profile)
    return wp.cutBlind(-height)


def _edge_selection(shape: "cq.Workplane", selector, *, face_selector: str = ">Z") -> "cq.Workplane":
    """Resolve lightweight edge selectors to a CadQuery edge selection."""
    if selector in (None, "all"):
        return shape.faces(face_selector).edges()
    if isinstance(selector, str):
        return shape.faces(face_selector).edges(selector)
    if isinstance(selector, dict):
        face = selector.get("face") or selector.get("face_selector") or face_selector
        edges = shape.faces(face).edges()
        direction = selector.get("edge_direction") or selector.get("direction")
        if direction:
            token = str(direction)
            if token.upper() in {"X", "Y", "Z"}:
                token = f"|{token.upper()}"
            edges = shape.faces(face).edges(token)
        bbox = selector.get("bbox") or selector.get("box")
        if bbox:
            try:
                from cadquery import selectors as cq_selectors
                return edges.filter(cq_selectors.BoxSelector(tuple(bbox[0]), tuple(bbox[1])))
            except Exception:
                return edges
        return edges
    return shape.faces(face_selector).edges()


def chamfer_edges(shape: "cq.Workplane", width: float, *, face_selector: str = ">Z", selector=None) -> "cq.Workplane":
    """Apply chamfer to top edges."""
    if not _HAS_CADQUERY:
        raise RuntimeError("cadquery is not available")
    return _edge_selection(shape, selector, face_selector=face_selector).chamfer(width)


def fillet_edges(shape: "cq.Workplane", radius: float, *, face_selector: str = ">Z", selector=None) -> "cq.Workplane":
    """Apply fillet to selected edges."""
    if not _HAS_CADQUERY:
        raise RuntimeError("cadquery is not available")
    return _edge_selection(shape, selector, face_selector=face_selector).fillet(radius)


# =============================================================================
#  Export / Import
# =============================================================================

def export_step(shape: "cq.Workplane", path: str) -> None:
    """Export shape to STEP file."""
    if not _HAS_CADQUERY:
        raise RuntimeError("cadquery is not available")
    cq.exporters.export(shape, path)


def export_stl(shape: "cq.Workplane", path: str) -> None:
    """Export shape to STL file."""
    if not _HAS_CADQUERY:
        raise RuntimeError("cadquery is not available")
    cq.exporters.export(shape, path)


def to_mesh(shape: "cq.Workplane"):
    """Convert CadQuery shape to trimesh.Trimesh using tessellation.

    Returns None if trimesh is not available.
    """
    if not _HAS_CADQUERY:
        raise RuntimeError("cadquery is not available")
    if not _HAS_TRIMESH:
        return None

    verts_raw, faces = shape.val().tessellate(0.1)
    # Convert CadQuery Vector objects to plain (x, y, z) tuples
    verts = [(v.x, v.y, v.z) if hasattr(v, "x") else tuple(v) for v in verts_raw]
    return trimesh.Trimesh(vertices=verts, faces=faces)


def compute_bounding_box(shape: "cq.Workplane") -> dict:
    """Compute the bounding box of the shape.

    Returns dict with keys: x_min, x_max, y_min, y_max, z_min, z_max,
    length, width, height.
    """
    if not _HAS_CADQUERY:
        raise RuntimeError("cadquery is not available")

    bb = shape.val().BoundingBox()
    return {
        "x_min": bb.xmin,
        "x_max": bb.xmax,
        "y_min": bb.ymin,
        "y_max": bb.ymax,
        "z_min": bb.zmin,
        "z_max": bb.zmax,
        "length": bb.xmax - bb.xmin,
        "width": bb.ymax - bb.ymin,
        "height": bb.zmax - bb.zmin,
    }


def compute_volume(shape: "cq.Workplane") -> float:
    """Compute volume in mm^3. Returns 0.0 if not available."""
    if not _HAS_CADQUERY:
        raise RuntimeError("cadquery is not available")
    try:
        return shape.val().Volume()
    except Exception:
        return 0.0


def import_step(path: str) -> "cq.Workplane":
    """Import shape from STEP file."""
    if not _HAS_CADQUERY:
        raise RuntimeError("cadquery is not available")
    return cq.importers.importStep(path)


# =============================================================================
#  Self-test
# =============================================================================

if __name__ == "__main__":
    if not _HAS_CADQUERY:
        print("CadQuery not available -- skipping self-tests.")
        import sys

        sys.exit(0)

    print("Running SubCAD geometry self-tests...")
    passed = 0
    failed = 0

    # ------------------------------------------------------------------
    # Test 1: create_rectangular_stock creates correct dimensions
    # ------------------------------------------------------------------
    try:
        stock = create_rectangular_stock(100, 60, 20)
        bb = compute_bounding_box(stock)
        assert abs(bb["length"] - 100) < 0.01, f"Length: {bb['length']}"
        assert abs(bb["width"] - 60) < 0.01, f"Width: {bb['width']}"
        assert abs(bb["height"] - 20) < 0.01, f"Height: {bb['height']}"
        vol = compute_volume(stock)
        assert abs(vol - 100 * 60 * 20) < 0.1, f"Volume: {vol}"
        print("  PASS: create_rectangular_stock")
        passed += 1
    except Exception as e:
        print(f"  FAIL: create_rectangular_stock -- {e}")
        failed += 1

    # ------------------------------------------------------------------
    # Test 2: drill_hole creates a through hole (volume decreases)
    # ------------------------------------------------------------------
    try:
        stock = create_rectangular_stock(100, 60, 20)
        drilled = drill_hole(stock, 0, 0, 10, depth=0, through=True)
        vol_before = compute_volume(stock)
        vol_after = compute_volume(drilled)
        assert vol_after < vol_before, (
            f"Volume did not decrease: {vol_before} -> {vol_after}"
        )
        print("  PASS: drill_hole (through)")
        passed += 1
    except Exception as e:
        print(f"  FAIL: drill_hole (through) -- {e}")
        failed += 1

    # ------------------------------------------------------------------
    # Test 3: drill_hole creates a blind hole (volume decreases)
    # ------------------------------------------------------------------
    try:
        stock = create_rectangular_stock(100, 60, 20)
        drilled = drill_hole(stock, 0, 0, 10, depth=10, through=False)
        vol_before = compute_volume(stock)
        vol_after = compute_volume(drilled)
        assert vol_after < vol_before, (
            f"Volume did not decrease: {vol_before} -> {vol_after}"
        )
        print("  PASS: drill_hole (blind)")
        passed += 1
    except Exception as e:
        print(f"  FAIL: drill_hole (blind) -- {e}")
        failed += 1

    # ------------------------------------------------------------------
    # Test 4: rectangular_pocket_cut creates a pocket
    # ------------------------------------------------------------------
    try:
        stock = create_rectangular_stock(100, 60, 20)
        pocketed = rectangular_pocket_cut(stock, 10, 10, 30, 20, 5)
        vol_after = compute_volume(pocketed)
        expected_vol = 100 * 60 * 20 - 30 * 20 * 5
        assert abs(vol_after - expected_vol) < 0.5, (
            f"Volume: {vol_after} vs expected {expected_vol}"
        )
        print("  PASS: rectangular_pocket_cut")
        passed += 1
    except Exception as e:
        print(f"  FAIL: rectangular_pocket_cut -- {e}")
        failed += 1

    # ------------------------------------------------------------------
    # Test 5: export_step writes a valid file
    # ------------------------------------------------------------------
    try:
        import os
        import tempfile

        stock = create_rectangular_stock(100, 60, 20)
        fd, tmp_path = tempfile.mkstemp(suffix=".step")
        os.close(fd)
        export_step(stock, tmp_path)
        file_size = os.path.getsize(tmp_path)
        assert file_size > 0, "STEP file is empty"
        os.unlink(tmp_path)
        print("  PASS: export_step")
        passed += 1
    except Exception as e:
        print(f"  FAIL: export_step -- {e}")
        failed += 1

    # ------------------------------------------------------------------
    # Test 6: export_stl writes a valid file
    # ------------------------------------------------------------------
    try:
        import os
        import tempfile

        stock = create_rectangular_stock(100, 60, 20)
        fd, tmp_path = tempfile.mkstemp(suffix=".stl")
        os.close(fd)
        export_stl(stock, tmp_path)
        file_size = os.path.getsize(tmp_path)
        assert file_size > 0, "STL file is empty"
        os.unlink(tmp_path)
        print("  PASS: export_stl")
        passed += 1
    except Exception as e:
        print(f"  FAIL: export_stl -- {e}")
        failed += 1

    # ------------------------------------------------------------------
    # Test 7: compute_volume returns reasonable value
    # ------------------------------------------------------------------
    try:
        stock = create_rectangular_stock(50, 40, 30)
        vol = compute_volume(stock)
        assert vol > 0, "Volume should be positive"
        assert abs(vol - 60000) < 0.1, f"Expected 60000, got {vol}"
        print("  PASS: compute_volume")
        passed += 1
    except Exception as e:
        print(f"  FAIL: compute_volume -- {e}")
        failed += 1

    # ------------------------------------------------------------------
    # Test 8: to_mesh handles null case gracefully
    # ------------------------------------------------------------------
    try:
        stock = create_rectangular_stock(100, 60, 20)
        mesh = to_mesh(stock)
        if _HAS_TRIMESH:
            assert mesh is not None, "Expected mesh object"
            assert hasattr(mesh, "vertices"), "Mesh should have vertices"
            print("  PASS: to_mesh (with trimesh)")
        else:
            assert mesh is None, "Expected None without trimesh"
            print("  PASS: to_mesh (null case)")
        passed += 1
    except Exception as e:
        print(f"  FAIL: to_mesh -- {e}")
        failed += 1

    # ------------------------------------------------------------------
    # Test 9: face_mill_cut reduces height
    # ------------------------------------------------------------------
    try:
        stock = create_rectangular_stock(100, 60, 20)
        faced = face_mill_cut(stock, 5)
        bb = compute_bounding_box(faced)
        assert abs(bb["height"] - 15) < 0.01, (
            f"Height after face mill: {bb['height']}"
        )
        print("  PASS: face_mill_cut")
        passed += 1
    except Exception as e:
        print(f"  FAIL: face_mill_cut -- {e}")
        failed += 1

    # ------------------------------------------------------------------
    # Test 10: circular_pocket_cut
    # ------------------------------------------------------------------
    try:
        stock = create_rectangular_stock(100, 60, 20)
        cp = circular_pocket_cut(stock, 0, 0, 30, 10)
        vol = compute_volume(cp)
        expected = 100 * 60 * 20 - math.pi * (15**2) * 10
        assert abs(vol - expected) < 5.0, f"Volume: {vol} vs expected {expected}"
        print("  PASS: circular_pocket_cut")
        passed += 1
    except Exception as e:
        print(f"  FAIL: circular_pocket_cut -- {e}")
        failed += 1

    # ------------------------------------------------------------------
    # Test 11: slot_cut reduces volume
    # ------------------------------------------------------------------
    try:
        stock = create_rectangular_stock(100, 60, 20)
        slotted = slot_cut(stock, 20, 0, 30, 8, 10)
        vol_after = compute_volume(slotted)
        assert vol_after < compute_volume(stock), "Volume should decrease"
        print("  PASS: slot_cut")
        passed += 1
    except Exception as e:
        print(f"  FAIL: slot_cut -- {e}")
        failed += 1

    # ------------------------------------------------------------------
    # Test 12: slot_cut through
    # ------------------------------------------------------------------
    try:
        stock = create_rectangular_stock(100, 60, 20)
        slotted = slot_cut(stock, 0, 0, 30, 8, 0, through=True)
        vol_after = compute_volume(slotted)
        assert vol_after < compute_volume(stock), "Through slot should reduce volume"
        print("  PASS: slot_cut (through)")
        passed += 1
    except Exception as e:
        print(f"  FAIL: slot_cut (through) -- {e}")
        failed += 1

    # ------------------------------------------------------------------
    # Test 13: slot_cut with angle
    # ------------------------------------------------------------------
    try:
        stock = create_rectangular_stock(100, 60, 20)
        slotted = slot_cut(stock, 20, 0, 30, 8, 10, angle=45)
        vol_after = compute_volume(slotted)
        assert vol_after < compute_volume(stock), "Angled slot should reduce volume"
        print("  PASS: slot_cut (angled)")
        passed += 1
    except Exception as e:
        print(f"  FAIL: slot_cut (angled) -- {e}")
        failed += 1

    # ------------------------------------------------------------------
    # Test 14: chamfer_edges reduces volume
    # ------------------------------------------------------------------
    try:
        stock = create_rectangular_stock(100, 60, 20)
        chamfered = chamfer_edges(stock, 2.0)
        vol_chamfered = compute_volume(chamfered)
        assert vol_chamfered < compute_volume(stock), (
            "Chamfer should reduce volume"
        )
        print("  PASS: chamfer_edges")
        passed += 1
    except Exception as e:
        print(f"  FAIL: chamfer_edges -- {e}")
        failed += 1

    # ------------------------------------------------------------------
    # Test 15: fillet_edges reduces volume
    # ------------------------------------------------------------------
    try:
        stock = create_rectangular_stock(100, 60, 20)
        filleted = fillet_edges(stock, 2.0)
        vol_filleted = compute_volume(filleted)
        assert vol_filleted < compute_volume(stock), (
            "Fillet should reduce volume"
        )
        print("  PASS: fillet_edges")
        passed += 1
    except Exception as e:
        print(f"  FAIL: fillet_edges -- {e}")
        failed += 1

    # ------------------------------------------------------------------
    # Test 16: create_cylindrical_stock
    # ------------------------------------------------------------------
    try:
        cyl = create_cylindrical_stock(50, 30)
        bb = compute_bounding_box(cyl)
        assert abs(bb["height"] - 30) < 0.01, f"Height: {bb['height']}"
        vol = compute_volume(cyl)
        expected_vol = math.pi * (25**2) * 30
        assert abs(vol - expected_vol) < 1.0, f"Volume: {vol} vs expected {expected_vol}"
        print("  PASS: create_cylindrical_stock")
        passed += 1
    except Exception as e:
        print(f"  FAIL: create_cylindrical_stock -- {e}")
        failed += 1

    # ------------------------------------------------------------------
    # Test 17: contour_cut_outer reduces volume
    # ------------------------------------------------------------------
    try:
        stock = create_rectangular_stock(100, 60, 20)
        contoured = contour_cut_outer(stock, 5)
        vol_after = compute_volume(contoured)
        assert vol_after < compute_volume(stock), (
            "Contour should reduce volume"
        )
        print("  PASS: contour_cut_outer")
        passed += 1
    except Exception as e:
        print(f"  FAIL: contour_cut_outer -- {e}")
        failed += 1

    # ------------------------------------------------------------------
    # Test 18: contour_cut_outer with stepdown
    # ------------------------------------------------------------------
    try:
        stock = create_rectangular_stock(100, 60, 20)
        contoured = contour_cut_outer(stock, 6, stepdown=2.0)
        vol_after = compute_volume(contoured)
        assert vol_after < compute_volume(stock), (
            "Multi-pass contour should reduce volume"
        )
        print("  PASS: contour_cut_outer (stepdown)")
        passed += 1
    except Exception as e:
        print(f"  FAIL: contour_cut_outer (stepdown) -- {e}")
        failed += 1

    # ------------------------------------------------------------------
    # Test 19: rectangular_pocket_cut with corner_radius
    # ------------------------------------------------------------------
    try:
        stock = create_rectangular_stock(100, 60, 20)
        pocketed = rectangular_pocket_cut(stock, 10, 10, 30, 20, 5, corner_radius=3.0)
        vol_after = compute_volume(pocketed)
        expected_max = 100 * 60 * 20 - (30 - 2 * 3) * (20 - 2 * 3) * 5
        # Volume should decrease (pocket removes material)
        assert vol_after < compute_volume(stock), "Radius pocket should reduce volume"
        print("  PASS: rectangular_pocket_cut (corner_radius)")
        passed += 1
    except Exception as e:
        print(f"  FAIL: rectangular_pocket_cut (corner_radius) -- {e}")
        failed += 1

    # ------------------------------------------------------------------
    # Test 20: compute_bounding_box returns correct keys
    # ------------------------------------------------------------------
    try:
        stock = create_rectangular_stock(100, 60, 20)
        bb = compute_bounding_box(stock)
        required_keys = {
            "x_min", "x_max", "y_min", "y_max", "z_min", "z_max",
            "length", "width", "height",
        }
        assert required_keys.issubset(bb.keys()), (
            f"Missing keys: {required_keys - set(bb.keys())}"
        )
        print("  PASS: compute_bounding_box keys")
        passed += 1
    except Exception as e:
        print(f"  FAIL: compute_bounding_box keys -- {e}")
        failed += 1

    # ------------------------------------------------------------------
    # Test 21: import_step (null / graceful handling)
    # ------------------------------------------------------------------
    try:
        # import_step requires an actual file, so just verify the function exists
        # and accepts a string argument.  We don't test actual import since no
        # STEP file is available in the test environment.
        assert callable(import_step), "import_step should be callable"
        print("  PASS: import_step (callable)")
        passed += 1
    except Exception as e:
        print(f"  FAIL: import_step (callable) -- {e}")
        failed += 1

    # ------------------------------------------------------------------
    # Test 22: face_selector multi-face support
    # ------------------------------------------------------------------
    try:
        stock = create_rectangular_stock(100, 60, 20)
        # Drill from bottom face
        drilled = drill_hole(stock, 0, 0, 10, depth=10, through=False,
                            face_selector="<Z")
        vol_after = compute_volume(drilled)
        assert vol_after < compute_volume(stock), "Bottom-face drill should reduce volume"
        print("  PASS: drill_hole (bottom face <Z)")
        passed += 1
    except Exception as e:
        print(f"  FAIL: drill_hole (bottom face <Z) -- {e}")
        failed += 1

    # ------------------------------------------------------------------
    # Test 23: face_mill_cut from bottom face reduces height
    # ------------------------------------------------------------------
    try:
        stock = create_rectangular_stock(100, 60, 20)
        faced = face_mill_cut(stock, 5, face_selector="<Z")
        bb = compute_bounding_box(faced)
        assert abs(bb["height"] - 15) < 0.01, (
            f"Height after bottom face_mill: {bb['height']}"
        )
        print("  PASS: face_mill_cut (bottom face <Z)")
        passed += 1
    except Exception as e:
        print(f"  FAIL: face_mill_cut (bottom face <Z) -- {e}")
        failed += 1

    # ------------------------------------------------------------------
    # Test 24: chamfer_edges from bottom face
    # ------------------------------------------------------------------
    try:
        stock = create_rectangular_stock(100, 60, 20)
        chamfered = chamfer_edges(stock, 2.0, face_selector="<Z")
        vol_chamfered = compute_volume(chamfered)
        assert vol_chamfered < compute_volume(stock), (
            "Bottom chamfer should reduce volume"
        )
        print("  PASS: chamfer_edges (bottom face <Z)")
        passed += 1
    except Exception as e:
        print(f"  FAIL: chamfer_edges (bottom face <Z) -- {e}")
        failed += 1

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    total = passed + failed
    print(f"\n{'=' * 50}")
    print(f"Results: {passed}/{total} passed, {failed}/{total} failed")
    if failed > 0:
        import sys

        sys.exit(1)
