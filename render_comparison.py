"""Extract reference renders and generate subCAD comparison views.

Usage:
    python render_comparison.py --sample 1          # single sample
    python render_comparison.py --sample 1 --translate  # translate then compare
    python render_comparison.py --sample 1 --output-dir renders/sample_1
"""

import argparse
import json
import os
import sys
from pathlib import Path

os.chdir(Path(__file__).resolve().parent)


def extract_reference_images(sample_dir: str, output_dir: str) -> list[str]:
    """Extract the 8 reference view images from the parquet dataset.

    Returns list of saved image paths.
    """
    import pyarrow.parquet as pq

    # Load metadata to find which parquet file + row
    meta_path = os.path.join(sample_dir, "metadata.json")
    if not os.path.exists(meta_path):
        print(f"No metadata.json in {sample_dir}")
        return []

    with open(meta_path) as f:
        meta = json.load(f)

    source_file = meta.get("source_file", "")
    row_index = meta.get("row_index", 0)

    # Reconstruct parquet path
    parquet_dir = "data/zero_to_cad_100k/data"
    pf_path = None
    for split in ["train", "val", "test"]:
        candidate = os.path.join(parquet_dir, split, source_file)
        if os.path.exists(candidate):
            pf_path = candidate
            break

    if pf_path is None:
        print(f"Parquet file not found: {source_file}")
        return []

    table = pq.read_table(pf_path)
    row = table.to_pydict()

    os.makedirs(output_dir, exist_ok=True)
    saved = []
    for i in range(8):
        col = f"image_{i}"
        data = row[col][row_index]
        if data:
            path = os.path.join(output_dir, f"ref_view_{i}.png")
            with open(path, "wb") as f:
                f.write(data)
            saved.append(path)

    print(f"Extracted {len(saved)} reference images to {output_dir}/")
    return saved


def render_subcad_views(
    step_path: str,
    output_dir: str,
    resolution: tuple = (512, 512),
) -> list[str]:
    """Render the subCAD STEP file from 8 standard viewpoints.

    Uses trimesh with pyrender (if available) or falls back to a simple
    trimesh scene save which renders one view.
    """
    import trimesh
    import numpy as np

    # Load mesh via CadQuery (cascadio unavailable for trimesh STEP load)
    try:
        import cadquery as cq
        shape = cq.importers.importStep(step_path).val()
        verts, faces = shape.tessellate(0.1)
        mesh = trimesh.Trimesh(
            vertices=[(v.x, v.y, v.z) for v in verts],
            faces=faces,
        )
    except Exception as e:
        print(f"Failed to load STEP: {e}")
        return []

    os.makedirs(output_dir, exist_ok=True)

    # Try pyrender for proper offscreen rendering
    try:
        import pyrender
        return _render_with_pyrender(mesh, output_dir, resolution)
    except ImportError:
        pass

    # Fallback: save 8 views using trimesh scene camera
    return _render_with_trimesh(mesh, output_dir, resolution)


def _render_with_pyrender(
    mesh: "trimesh.Trimesh",
    output_dir: str,
    resolution: tuple,
) -> list[str]:
    """Render 8 views using trimesh scene (more reliable camera)."""
    import numpy as np
    import trimesh as _trimesh

    # Normalize mesh
    mesh_copy = mesh.copy()
    mesh_copy.vertices -= mesh_copy.centroid
    scale = 1.8 / max(mesh_copy.extents) if max(mesh_copy.extents) > 0 else 1.0
    mesh_copy.vertices *= scale

    # Use trimesh scene for rendering
    scene = _trimesh.Scene(mesh_copy)
    scene.graph.clear()
    scene.add_geometry(mesh_copy, geom_name='part')

    saved = []
    d = 2.5

    # Camera angles for standard views (azimuth, elevation in degrees)
    # trimesh: azimuth=0 is +X, 90 is +Y; elevation=0 is XY plane, 90 is +Z
    view_angles = {
        "front":  (0, 0),       # looking along X axis at XY plane
        "right":  (90, 0),      # looking along Y axis
        "back":   (180, 0),     # looking along -X
        "left":   (270, 0),     # looking along -Y
        "top":    (0, 90),      # looking along +Z
        "bottom": (0, -90),     # looking along -Z
        "iso_1":  (45, 35.26),  # standard isometric
        "iso_2":  (225, 35.26), # opposite isometric
    }

    for name in ["front", "right", "back", "left", "top", "bottom", "iso_1", "iso_2"]:
        try:
            azimuth, elevation = view_angles[name]
            # Convert to radians
            az_rad = np.radians(azimuth)
            el_rad = np.radians(elevation)

            # Set camera angles using trimesh
            # trimesh expects (azimuth, elevation, distance) relative to centroid
            scene.set_camera(angles=(az_rad, el_rad, d * 1.5))

            png = scene.save_image(resolution=resolution)
            if png is not None:
                from PIL import Image
                import io
                img = Image.open(io.BytesIO(png))
                arr = np.array(img)
                # Alpha → white background
                if arr.shape[-1] == 4:
                    alpha = arr[:, :, 3:4] / 255.0
                    white_bg = np.ones_like(arr[:, :, :3]) * 255
                    arr_rgb = (arr[:, :, :3] * alpha + white_bg * (1 - alpha)).astype(np.uint8)
                else:
                    arr_rgb = arr[:, :, :3]
                path = os.path.join(output_dir, f"subcad_{name}.png")
                Image.fromarray(arr_rgb).save(path)
                saved.append(path)
                print(f"  Rendered {name}")
        except Exception as e:
            print(f"  Failed {name}: {e}")

    return saved


def _render_with_trimesh(
    mesh: "trimesh.Trimesh",
    output_dir: str,
    resolution: tuple,
) -> list[str]:
    """Fallback: save one view using trimesh scene."""
    import numpy as np

    scene = trimesh.Scene(mesh)
    saved = []

    # 8 camera angles
    views = [
        ("front", [0, 0, 2.5], [0, 0, 0]),
        ("right", [2.5, 0, 0], [0, 0, 0]),
        ("back", [0, 0, -2.5], [0, 0, 0]),
        ("left", [-2.5, 0, 0], [0, 0, 0]),
        ("top", [0, 2.5, 0.001], [0, 0, 0]),
        ("bottom", [0, -2.5, 0.001], [0, 0, 0]),
        ("iso_1", [1.8, 1.2, 1.8], [0, 0, 0]),
        ("iso_2", [-1.8, 1.2, -1.8], [0, 0, 0]),
    ]

    for name, cam_pos, look_at in views:
        try:
            # Set up camera transform
            camera = trimesh.scene.Camera(
                fov=(60, 60),
                resolution=resolution,
                z_near=0.01,
            )
            scene.set_camera()
            # Save scene as PNG
            path = os.path.join(output_dir, f"subcad_{name}.png")
            png_data = scene.save_image(resolution=resolution, visible=True)
            if png_data is not None:
                with open(path, "wb") as f:
                    f.write(png_data)
                saved.append(path)
        except Exception as e:
            print(f"  Failed to render {name}: {e}")

    if not saved:
        # Last resort: just save the mesh as STL
        stl_path = os.path.join(output_dir, "subcad_model.stl")
        mesh.export(stl_path)
        print(f"  Saved STL to {stl_path} (no renderer available)")
        saved.append(stl_path)

    return saved


def _look_at(eye, target, up):
    """Build a 4x4 view matrix (world-to-camera transform) for pyrender."""
    import numpy as np
    eye = np.array(eye, dtype=np.float64)
    target = np.array(target, dtype=np.float64)
    up = np.array(up, dtype=np.float64)

    # Camera basis vectors
    f = target - eye                    # forward (look direction)
    f = f / np.linalg.norm(f)
    r = np.cross(up, f)                 # right
    r = r / np.linalg.norm(r)
    u = np.cross(f, r)                  # up (re-orthogonalized)

    # Build 4x4 pose matrix: [R | t; 0 0 0 1]
    # Camera looks along +Z in pyrender convention, so:
    # rotate world so that camera's right = world X, up = world Y, -forward = world Z
    m = np.eye(4)
    m[0, 0:3] = r
    m[1, 0:3] = u
    m[2, 0:3] = -f
    m[0, 3] = -np.dot(r, eye)
    m[1, 3] = -np.dot(u, eye)
    m[2, 3] = np.dot(f, eye)
    return m


def _translation_matrix(pos):
    """Build a 4x4 translation matrix."""
    import numpy as np
    m = np.eye(4)
    m[0:3, 3] = pos
    return m


def create_comparison_grid(
    ref_dir: str,
    subcad_dir: str,
    output_path: str,
):
    """Create a side-by-side comparison grid image."""
    try:
        from PIL import Image
    except ImportError:
        print("PIL not available, skipping comparison grid")
        return

    view_names = ["front", "right", "back", "left", "top", "bottom", "iso_1", "iso_2"]
    ref_prefix = "ref_view_"
    subcad_prefix = "subcad_"

    rows = []
    for i, name in enumerate(view_names):
        ref_path = os.path.join(ref_dir, f"{ref_prefix}{i}.png")
        subcad_path = os.path.join(subcad_dir, f"{subcad_prefix}{name}.png")

        ref_img = Image.open(ref_path) if os.path.exists(ref_path) else None
        sub_img = Image.open(subcad_path) if os.path.exists(subcad_path) else None

        if ref_img is None and sub_img is None:
            continue

        # Resize to consistent size
        w, h = 256, 256
        if ref_img:
            ref_img = ref_img.resize((w, h))
        if sub_img:
            sub_img = sub_img.resize((w, h))

        # Create row: [ref] [label] [subcad]
        row = Image.new("RGB", (w * 3 + 40, h + 40), (40, 40, 40))
        if ref_img:
            row.paste(ref_img, (0, 20))
        if sub_img:
            row.paste(sub_img, (w + 40, 20))

        # Add label
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(row)
        draw.text((w // 2, 2), f"REF {name}", fill=(200, 200, 200))
        draw.text((w + 40 + w // 2, 2), f"SUBCAD {name}", fill=(200, 200, 200))

        rows.append(row)

    if rows:
        grid = Image.new("RGB", (rows[0].width, sum(r.height for r in rows)), (40, 40, 40))
        y = 0
        for row in rows:
            grid.paste(row, (0, y))
            y += row.height
        grid.save(output_path)
        print(f"Comparison grid saved to {output_path}")
    else:
        print("No images to create comparison grid")


def main():
    parser = argparse.ArgumentParser(description="Render subCAD vs reference comparison")
    parser.add_argument("--sample", type=int, default=1)
    parser.add_argument("--sample-dir", type=str, default=None)
    parser.add_argument("--subcad-step", type=str, default=None,
                        help="Path to subCAD STEP file (auto-generates if not set)")
    parser.add_argument("--translate", action="store_true",
                        help="Run agentic translation to generate subCAD STEP")
    parser.add_argument("--output-dir", type=str, default=None)
    args = parser.parse_args()

    if args.sample_dir:
        sample_dir = args.sample_dir
    else:
        sample_dir = f"data/zero_to_cad_exploration/sample_{args.sample}"

    if args.output_dir:
        output_dir = args.output_dir
    else:
        output_dir = f"renders/sample_{args.sample}"

    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Extract reference images
    ref_dir = os.path.join(output_dir, "reference")
    extract_reference_images(sample_dir, ref_dir)

    # Step 2: Get subCAD STEP
    subcad_step = args.subcad_step
    if subcad_step is None and args.translate:
        from dotenv import load_dotenv
        load_dotenv()
        from src.data.agentic_translator import AgenticTranslator
        import json

        with open(os.path.join(sample_dir, "cadquery_code.py")) as f:
            cq_code = f.read()
        with open(os.path.join(sample_dir, "ops_trace.json")) as f:
            ops_trace = json.load(f)

        translator = AgenticTranslator(
            provider="deepseek",
            tolerance=0.05,
            stagnation_limit=5,
            safety_cap=15,
            verbose=True,
        )

        result = translator.translate(
            {
                "cadquery_file": cq_code,
                "cadquery_ops_json": json.dumps(ops_trace),
                "uuid": os.path.basename(sample_dir),
            },
            step_path=os.path.join(sample_dir, "model.step"),
        )

        if result["success"] and result.get("exec_result", {}).get("step_path"):
            subcad_step = result["exec_result"]["step_path"]
            # Save the code too
            code_path = os.path.join(output_dir, "subcad_code.py")
            with open(code_path, "w") as f:
                f.write(result["subcad_code"])
            print(f"Translation SUCCESS (ratio={result['comparison']['volume_ratio']:.4f})")
            print(f"SubCAD code saved to {code_path}")
        else:
            print(f"Translation FAILED: {result.get('stop_reason', '?')}")
            return

    if subcad_step and os.path.exists(subcad_step):
        # Step 3: Render subCAD views
        subcad_dir = os.path.join(output_dir, "subcad")
        render_subcad_views(subcad_step, subcad_dir)

        # Step 4: Create comparison grid
        grid_path = os.path.join(output_dir, "comparison.png")
        create_comparison_grid(ref_dir, subcad_dir, grid_path)

        print(f"\nAll outputs in: {output_dir}/")
        print(f"  reference/  - 8 original PNG renders")
        print(f"  subcad/     - 8 subCAD PNG renders")
        if os.path.exists(os.path.join(output_dir, "comparison.png")):
            print(f"  comparison.png - side-by-side grid")
    else:
        print("No subCAD STEP available for rendering")
        print(f"Reference images extracted to: {ref_dir}/")


if __name__ == "__main__":
    main()
