"""FastAPI backend for d2m 5-axis CNC simulator.

Serves a REST + WebSocket API that wraps the FiveAxisSimulator:
  - POST /api/upload          Upload stock + target mesh, get part_id
  - POST /api/simulate         Run simulation, get operation list
  - GET  /api/mesh/{part_id}/{op_index}  Mesh after operation N (GLB binary)
  - GET  /api/deviation/{part_id}        Deviation heatmap data
  - WS   /ws/simulate/{part_id}          Stream per-operation progress + GLB meshes
"""

from __future__ import annotations

import base64
import io
import json
import uuid
import sys
import os
from pathlib import Path
from typing import Optional

import numpy as np
import trimesh

from fastapi import FastAPI, UploadFile, File, WebSocket, WebSocketDisconnect, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

# Ensure project root on path so src.simulation imports work
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.simulation.simulator import FiveAxisSimulator, GCodeParser
from src.simulation.kinematics import ToolPose, MachineConfig, FiveAxisKinematics
from src.simulation.tools import BallEndmill, FlatEndmill, create_tool
from src.simulation.material_removal import Gouge


# =============================================================================
#  App setup
# =============================================================================

app = FastAPI(title="d2m CNC Simulator API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================================================================
#  In-memory state
# =============================================================================

# part_id -> dict with keys: stock_mesh, target_mesh, stock_file, target_file
_parts: dict[str, dict] = {}

# part_id -> FiveAxisSimulator
_simulators: dict[str, FiveAxisSimulator] = {}

# part_id -> list of operation snapshots (each a dict with mesh, stats)
_snapshots: dict[str, list[dict]] = {}


# =============================================================================
#  Helpers
# =============================================================================

def _load_mesh_from_upload(upload: UploadFile) -> trimesh.Trimesh:
    """Load a mesh from an uploaded file (STL, OBJ, PLY, GLB, or STEP via cadquery)."""
    content = upload.filename or ""
    suffix = Path(content).suffix.lower() if content else ""

    data = upload.file.read()

    if suffix in (".step", ".stp"):
        try:
            import cadquery as cq
            shape = cq.importers.importStep(io.BytesIO(data).read())
            # CadQuery 2.x importers return a Workplane or Shape; tessellate
            if hasattr(shape, "val"):
                shape = shape.val()
            if hasattr(shape, "tessellate"):
                verts, faces = shape.tessellate(0.1)  # linear deflection 0.1mm
            else:
                verts, faces = shape.tessellate(0.1)
            verts = np.asarray(verts, dtype=np.float64)
            faces = np.asarray(faces, dtype=np.int64)
            return trimesh.Trimesh(vertices=verts, faces=faces)
        except ImportError:
            raise RuntimeError("cadquery not available for STEP import")

    # Let trimesh auto-detect format (STL, OBJ, PLY, GLB, etc.)
    try:
        mesh = trimesh.load(io.BytesIO(data), file_type=suffix.lstrip(".") or None)
    except Exception:
        # Try as STL
        mesh = trimesh.load(io.BytesIO(data), file_type="stl")

    if isinstance(mesh, trimesh.Scene):
        # Merge all geometries
        meshes = [g for g in mesh.geometry.values() if isinstance(g, trimesh.Trimesh)]
        if not meshes:
            raise ValueError("Uploaded file contains no mesh geometry")
        return trimesh.util.concatenate(meshes)

    if not isinstance(mesh, trimesh.Trimesh):
        raise ValueError(f"Uploaded file could not be loaded as a mesh")

    return mesh


def _decimate_mesh(mesh: trimesh.Trimesh, target_vertices: int = 2000) -> trimesh.Trimesh:
    """Reduce mesh vertex count to avoid memory blowup in simulation.

    The tri-dexel surface extraction computes a dense point-cloud-to-mesh
    distance matrix that is O(N_cells * N_verts).  Large CadQuery tessellations
    (50k+ vertices) can cause multi-GB allocations.  This helper reduces the
    mesh to a manageable size before simulation.
    """
    n = len(mesh.vertices)
    if n <= target_vertices:
        return mesh

    # For simple shapes (boxes, cylinders), just use trimesh primitives
    bbox = mesh.bounds
    extents = bbox[1] - bbox[0]
    if max(extents) / min(extents) < 10:
        # Approximately box-like: use trimesh box primitive
        center = (bbox[0] + bbox[1]) / 2.0
        simple = trimesh.creation.box(extents=extents)
        simple.apply_translation(center - simple.centroid)
        return simple

    # Otherwise, decimate by percentage (quadric edge collapse decimation)
    fraction = target_vertices / n
    try:
        return mesh.simplify_quadric_decimation(int(n * fraction))
    except Exception:
        # Fallback: reduce to a very coarse mesh by face count
        return mesh


def _mesh_to_glb_bytes(mesh: trimesh.Trimesh) -> bytes:
    """Export a trimesh.Trimesh to GLB binary bytes."""
    if mesh is None or len(mesh.vertices) == 0:
        # Return minimal empty GLB
        empty = trimesh.creation.box(extents=[0.001] * 3)
        return empty.export(file_type="glb")

    # Ensure mesh has faces
    if len(mesh.faces) == 0:
        return mesh.export(file_type="glb")

    return mesh.export(file_type="glb")


def _make_simulator(stock: trimesh.Trimesh, target: trimesh.Trimesh,
                    resolution: float = 0.5) -> FiveAxisSimulator:
    """Create a FiveAxisSimulator with default parameters."""
    return FiveAxisSimulator(
        stock_mesh=stock,
        target_mesh=target,
        machine=MachineConfig.TABLE_TABLE,
        resolution=resolution,
        primary_axis="B",
        secondary_axis="C",
    )


# =============================================================================
#  REST endpoints
# =============================================================================

@app.post("/api/upload")
async def upload(
    stock: UploadFile = File(...),
    target: UploadFile = File(...),
    resolution: float = Form(0.5),
):
    """Upload stock and target mesh files. Returns a part_id for subsequent operations."""
    part_id = uuid.uuid4().hex[:12]

    stock_mesh = _load_mesh_from_upload(stock)
    target_mesh = _load_mesh_from_upload(target)

    _parts[part_id] = {
        "stock_mesh": stock_mesh,
        "target_mesh": target_mesh,
        "stock_vertices": len(stock_mesh.vertices),
        "stock_faces": len(stock_mesh.faces),
        "target_vertices": len(target_mesh.vertices),
        "target_faces": len(target_mesh.faces),
        "resolution": resolution,
    }

    return {
        "part_id": part_id,
        "stock_vertices": len(stock_mesh.vertices),
        "stock_faces": len(stock_mesh.faces),
        "target_vertices": len(target_mesh.vertices),
        "target_faces": len(target_mesh.faces),
        "stock_volume_mm3": float(stock_mesh.volume if stock_mesh.is_watertight else 0),
    }


@app.get("/api/mesh/{part_id}/initial")
async def get_initial_mesh(part_id: str):
    """Get the initial (un-machined) stock mesh as GLB binary."""
    if part_id not in _parts:
        return Response(status_code=404, content="Part not found")

    stock_mesh = _parts[part_id]["stock_mesh"]
    glb_bytes = _mesh_to_glb_bytes(stock_mesh)
    return Response(
        content=glb_bytes,
        media_type="model/gltf-binary",
    )


@app.get("/api/mesh/{part_id}/target")
async def get_target_mesh(part_id: str):
    """Get the target CAD mesh as GLB binary."""
    if part_id not in _parts:
        return Response(status_code=404, content="Part not found")

    target_mesh = _parts[part_id]["target_mesh"]
    glb_bytes = _mesh_to_glb_bytes(target_mesh)
    return Response(
        content=glb_bytes,
        media_type="model/gltf-binary",
    )


@app.get("/api/mesh/{part_id}/final")
async def get_final_mesh(part_id: str):
    """Get the final stock mesh after all operations as GLB binary."""
    if part_id not in _snapshots or not _snapshots[part_id]:
        return Response(status_code=404, content="No simulation data")

    glb_bytes = _snapshots[part_id][-1].get("glb_bytes")
    if glb_bytes is None:
        return Response(status_code=500, content="Mesh data missing")

    return Response(
        content=glb_bytes,
        media_type="model/gltf-binary",
    )


@app.get("/api/mesh/{part_id}/{op_index}")
async def get_mesh(part_id: str, op_index: int):
    """Get the stock mesh after operation N as GLB binary."""
    if part_id not in _snapshots:
        return Response(status_code=404, content="Part not found")

    snaps = _snapshots[part_id]
    if op_index < 0 or op_index >= len(snaps):
        return Response(status_code=404, content=f"Operation {op_index} not found (0-{len(snaps)-1})")

    glb_bytes = snaps[op_index].get("glb_bytes")
    if glb_bytes is None:
        return Response(status_code=500, content="Mesh data missing")

    return Response(
        content=glb_bytes,
        media_type="model/gltf-binary",
        headers={"Content-Disposition": f"inline; filename={part_id}_op{op_index}.glb"},
    )


@app.get("/api/deviation/{part_id}")
async def get_deviation(part_id: str):
    """Get deviation map data: per-vertex signed distance to target.

    Returns arrays of vertex positions and deviation values for heatmap rendering.
    """
    if part_id not in _simulators:
        # Check if we at least have the part data
        if part_id not in _parts:
            return {"error": "Part not found"}
        # Return zero deviations for un-simulated part
        target = _parts[part_id]["target_mesh"]
        return {
            "part_id": part_id,
            "vertex_count": len(target.vertices),
            "deviations": [0.0] * len(target.vertices),
            "mesh_has_simulation": False,
        }

    sim = _simulators[part_id]
    deviations = sim.deviation_map

    return {
        "part_id": part_id,
        "vertex_count": len(deviations),
        "min_deviation": float(deviations.min()),
        "max_deviation": float(deviations.max()),
        "mean_deviation": float(deviations.mean()),
        "deviations": deviations.tolist(),
        "gouge_count": len(sim.gouges),
        "mesh_has_simulation": True,
    }


@app.get("/api/gouges/{part_id}")
async def get_gouges(part_id: str):
    """Get list of detected gouges with positions."""
    if part_id not in _simulators:
        return {"gouges": []}

    gouges = _simulators[part_id].gouges
    return {
        "part_id": part_id,
        "gouge_count": len(gouges),
        "gouges": [
            {
                "position": g.position.tolist(),
                "depth": float(g.depth),
                "severity": g.severity,
            }
            for g in gouges
        ],
    }


@app.get("/api/download/{part_id}/stl")
async def download_stl(part_id: str):
    """Download the final stock mesh as STL binary."""
    mesh = None

    # Try to get latest simulated mesh
    if part_id in _snapshots and _snapshots[part_id]:
        glb_bytes = _snapshots[part_id][-1].get("glb_bytes")
        if glb_bytes:
            try:
                mesh = trimesh.load(io.BytesIO(glb_bytes), file_type="glb")
            except Exception:
                pass

    # Fallback: use the simulator's current mesh
    if mesh is None and part_id in _simulators:
        mesh = _simulators[part_id].current_stock_mesh

    # Fallback: use the original stock
    if mesh is None and part_id in _parts:
        mesh = _parts[part_id]["stock_mesh"]

    if mesh is None:
        return Response(status_code=404, content="No mesh data available")

    stl_bytes = mesh.export(file_type="stl")
    return Response(
        content=stl_bytes,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={part_id}_result.stl"},
    )


@app.get("/api/download/{part_id}/glb")
async def download_glb(part_id: str):
    """Download the final stock mesh as GLB binary (convenience alias for /final)."""
    if part_id not in _snapshots or not _snapshots[part_id]:
        return Response(status_code=404, content="No simulation data")

    glb_bytes = _snapshots[part_id][-1].get("glb_bytes")
    if glb_bytes is None:
        return Response(status_code=500, content="Mesh data missing")

    return Response(
        content=glb_bytes,
        media_type="model/gltf-binary",
        headers={"Content-Disposition": f"attachment; filename={part_id}_result.glb"},
    )


@app.get("/api/health")
async def health():
    return {"status": "ok", "parts_loaded": len(_parts)}


# =============================================================================
#  WebSocket endpoint — streaming simulation
# =============================================================================

@app.websocket("/ws/simulate/{part_id}")
async def ws_simulate(websocket: WebSocket, part_id: str):
    """WebSocket endpoint that streams per-operation simulation results.

    Protocol:
      Client connects, then sends a JSON start message:
        {
          "type": "start",
          "gcode": "G01 X10 Y5 Z-2 ...",
          "tool_type": "ball_endmill",
          "tool_diameter": 6.0,
          "resolution": 0.5
        }

      Server responds with per-operation progress:
        {
          "type": "progress",
          "op_index": 0,
          "total_ops": 50,
          "mesh_glb_base64": "...",
          "volume_removed": 0.123,
          "gouges_found": 0
        }

      On completion:
        {
          "type": "complete",
          "total_ops": 50,
          "total_volume_removed": 12.5,
          "total_time_ms": 340.0,
          "gouges": [...]
        }

      On error:
        {"type": "error", "message": "..."}
    """
    await websocket.accept()

    if part_id not in _parts:
        await websocket.send_json({"type": "error", "message": f"Part '{part_id}' not found"})
        await websocket.close()
        return

    part = _parts[part_id]
    stock_mesh = part["stock_mesh"]
    target_mesh = part["target_mesh"]

    try:
        # Wait for the start message
        raw = await websocket.receive_text()
        msg = json.loads(raw)

        if msg.get("type") != "start":
            await websocket.send_json({"type": "error", "message": "Expected 'start' message"})
            await websocket.close()
            return

        gcode_text = msg["gcode"]
        tool_type = msg.get("tool_type", "ball_endmill")
        tool_diameter = float(msg.get("tool_diameter", 6.0))
        resolution = float(msg.get("resolution", part.get("resolution", 0.5)))

        # Create simulator
        sim = _make_simulator(stock_mesh, target_mesh, resolution)
        _simulators[part_id] = sim

        # Load tool
        try:
            tool = create_tool(tool_type, diameter=tool_diameter, flute_length=30.0)
        except ValueError:
            # Fallback to ball endmill
            tool = BallEndmill(diameter=tool_diameter, flute_length=30.0)
        sim.load_tool(tool)

        # Parse G-code and build move list (G01 feed moves only)
        parser = GCodeParser()
        parser.reset()

        raw_moves = []  # list of (start_joints, end_joints, line_no)
        prev_joints = None

        for line_no, line in enumerate(gcode_text.strip().split('\n'), start=1):
            parsed = parser.parse_block(line)
            if parsed is None:
                continue
            joints = parser.to_joints(parsed)
            motion = parsed.get("motion", 0)

            if prev_joints is not None and motion == 1:
                # G01 feed move with material removal
                raw_moves.append((prev_joints.copy(), joints.copy(), line_no))

            prev_joints = joints.copy()

        total_ops = len(raw_moves)

        if total_ops == 0:
            await websocket.send_json({
                "type": "error",
                "message": "No G01 feed moves found in G-code",
            })
            await websocket.close()
            return

        # Send initial state
        initial_glb = _mesh_to_glb_bytes(stock_mesh)
        await websocket.send_json({
            "type": "progress",
            "op_index": -1,
            "total_ops": total_ops,
            "mesh_glb_base64": base64.b64encode(initial_glb).decode("ascii"),
            "volume_removed": 0.0,
            "gouges_found": 0,
        })

        # Execute moves one at a time, snapshotting after each
        move_results = []
        total_vol = 0.0
        toolpath_positions = []  # Collect end positions for toolpath viz
        _snapshots[part_id] = []

        for op_idx, (start_joints, end_joints, line_no) in enumerate(raw_moves):
            start_pose = sim.kinematics.forward(start_joints)
            end_pose = sim.kinematics.forward(end_joints)

            result = sim.execute_move(start_pose, end_pose)
            move_results.append(result)

            if result.success:
                total_vol += result.removal.volume_removed

            # Collect toolpath
            ep = end_pose.position.tolist()
            toolpath_positions.append(ep)

            # Extract mesh and serialize
            mesh = sim.current_stock_mesh
            glb_bytes = _mesh_to_glb_bytes(mesh)

            # Store snapshot
            snap = {
                "op_index": op_idx,
                "line_no": line_no,
                "volume_removed_cumulative": total_vol,
                "volume_this_move": result.removal.volume_removed,
                "glb_bytes": glb_bytes,
                "success": result.success,
                "end_position": ep,
            }
            _snapshots[part_id].append(snap)

            # Check GLB size — if too large, skip mesh in message and use REST fallback
            glb_b64 = base64.b64encode(glb_bytes).decode("ascii")
            mesh_included = len(glb_bytes) < 2_000_000  # up to ~2MB GLB (~2.6MB b64)

            await websocket.send_json({
                "type": "progress",
                "op_index": op_idx,
                "total_ops": total_ops,
                "mesh_glb_base64": glb_b64 if mesh_included else None,
                "mesh_too_large": not mesh_included,
                "volume_removed": total_vol,
                "volume_this_move": result.removal.volume_removed,
                "gouges_found": len(sim.gouges),
                "columns_modified": result.removal.columns_modified,
                "end_position": ep,
            })

        # Final deviation check
        gouges = sim.gouges

        await websocket.send_json({
            "type": "complete",
            "total_ops": total_ops,
            "total_volume_removed": total_vol,
            "total_time_ms": sum(r.removal.time_ms for r in move_results),
            "gouges": [
                {
                    "position": g.position.tolist(),
                    "depth": float(g.depth),
                    "severity": g.severity,
                }
                for g in gouges
            ],
            "gouge_count": len(gouges),
            "stock_volume_mm3": float(sim.stock_volume),
            "toolpath_positions": toolpath_positions,
        })

    except WebSocketDisconnect:
        pass
    except Exception as e:
        try:
            await websocket.send_json({"type": "error", "message": str(e)})
        except Exception:
            pass
    finally:
        try:
            await websocket.close()
        except Exception:
            pass


# =============================================================================
#  SubCAD preset simulation endpoint
# =============================================================================

import traceback as _traceback_module

from pydantic import BaseModel as _BaseModel


class _PresetRequest(_BaseModel):
    """Request body for SubCAD preset simulation."""
    preset: str = "pocket_plate"  # one of: pocket_plate, drill_pattern, stepped_block, face_mill_only
    width: float = 50.0
    length: float = 80.0
    height: float = 20.0
    resolution: float = 0.5


_PRESET_DEFS = {
    "pocket_plate": {
        "label": "Pocket Plate",
        "description": "Rectangular stock with face mill + pocket + chamfer"
    },
    "drill_pattern": {
        "label": "Drill Pattern",
        "description": "Plate with 4 drilled holes"
    },
    "stepped_block": {
        "label": "Stepped Block",
        "description": "Rectangular stock with two levels of face milling"
    },
    "face_mill_only": {
        "label": "Face Mill Only",
        "description": "Single face mill pass"
    },
}


def _build_stock_from_preset(preset: str, width: float, length: float,
                              height: float) -> tuple:
    """Build a SubCAD Stock from a preset name.

    Returns (part, initial_stock_mesh, final_part_mesh, process_plan).
    - initial_stock_mesh: the original un-cut rectangular stock
    - final_part_mesh: the smooth CadQuery B-Rep mesh after all operations
    """
    try:
        from src.subcad.stock import Stock
        import numpy as np
    except ImportError as e:
        raise RuntimeError(f"SubCAD module not available: {e}")

    raw_stock = Stock.rectangular(length, width, height, material="aluminum_6061")
    initial_stock_mesh = raw_stock.to_mesh()  # save before any operations

    part = raw_stock
    if preset == "face_mill_only":
        part = part.face_mill(depth=2.0)
    elif preset == "pocket_plate":
        part = (part
            .face_mill(depth=1.0)
            .pocket(width=width * 0.4, length=length * 0.5, depth=5.0,
                    cx=0, cy=0, corner_radius=2.0)
            .chamfer(width=0.5)
        )
    elif preset == "drill_pattern":
        half_l = length / 4
        half_w = width / 4
        part = (part
            .face_mill(depth=1.0)
            .drill(diameter=6, depth=15, cx=half_l, cy=half_w)
            .drill(diameter=6, depth=15, cx=-half_l, cy=half_w)
            .drill(diameter=6, depth=15, cx=half_l, cy=-half_w)
            .drill(diameter=6, depth=15, cx=-half_l, cy=-half_w)
        )
    elif preset == "stepped_block":
        half_h = height * 0.4
        part = (part
            .face_mill(depth=half_h)
            .pocket(width=width, length=length * 0.5, depth=half_h,
                    cx=0, cy=0)
        )
    else:
        raise ValueError(f"Unknown preset: {preset}")

    final_part_mesh = part.to_mesh()
    plan = part.process_plan()
    return part, initial_stock_mesh, final_part_mesh, plan


def _run_subcad_simulation(stock_mesh, target_mesh, process_plan, resolution):
    """Run the five-axis simulation on a SubCAD-generated stock.

    Returns dict with glb_bytes, stats.
    """
    import numpy as np

    # Decimate meshes if they have too many vertices (CadQuery can generate
    # very dense tessellations that blow up the SDF computation in surface.py)
    max_verts = 2000
    if len(stock_mesh.vertices) > max_verts:
        stock_mesh = _decimate_mesh(stock_mesh, max_verts)
    if len(target_mesh.vertices) > max_verts:
        target_mesh = _decimate_mesh(target_mesh, max_verts)

    # Ensure resolution is coarse enough to avoid memory issues
    # The point cloud size in _point_cloud_to_sdf = O(N_cells * N_verts)
    stock_bbox = stock_mesh.bounds
    stock_size = max(stock_bbox[1] - stock_bbox[0])
    min_resolution = stock_size / 15.0  # max ~15 cells per axis
    effective_resolution = max(resolution, min_resolution)

    sim = _make_simulator(stock_mesh, target_mesh, effective_resolution)
    tool = BallEndmill(diameter=6.0, flute_length=30.0)
    sim.load_tool(tool)

    # Build G-code from the process plan operations
    gcode_lines = ["G00 X0 Y0 Z5"]

    # Use actual stock mesh bounding box for toolpath bounds
    s_bbox = stock_mesh.bounds
    bx_min, by_min, bz_min = s_bbox[0]
    bx_max, by_max, bz_max = s_bbox[1]
    bl = bx_max - bx_min
    bw = by_max - by_min
    z_safe = bz_max + 2.0

    # Generate sparse toolpath from operations (minimal passes for visual demo)
    for op in process_plan.get("operations", []):
        op_type = op.get("operation", "")
        depth = op.get("depth_mm", 1.0)
        pos = op.get("position")
        cx, cy = pos if pos else (0.0, 0.0)

        z_cut = bz_max - depth

        if op_type in ("face_mill",):
            # Single zigzag pass
            y_mid = by_min + bw * 0.5
            gcode_lines.append(f"G01 X{bx_min:.1f} Y{y_mid:.1f} Z{z_cut:.1f} F800")
            gcode_lines.append(f"G01 X{bx_max:.1f} Y{y_mid:.1f} Z{z_cut:.1f} F800")
            gcode_lines.append(f"G00 Z{z_safe}")

        elif op_type in ("rough_pocket",):
            # Single outline pass at full depth
            pw = bw * 0.4
            pl = bl * 0.5
            gcode_lines.append(f"G01 X{cx - pl/2:.1f} Y{cy - pw/2:.1f} Z{z_cut:.1f} F600")
            gcode_lines.append(f"G01 X{cx + pl/2:.1f} Y{cy - pw/2:.1f} Z{z_cut:.1f} F600")
            gcode_lines.append(f"G01 X{cx + pl/2:.1f} Y{cy + pw/2:.1f} Z{z_cut:.1f} F600")
            gcode_lines.append(f"G01 X{cx - pl/2:.1f} Y{cy + pw/2:.1f} Z{z_cut:.1f} F600")
            gcode_lines.append(f"G00 Z{z_safe}")

        elif op_type in ("drill", "spot_drill"):
            gcode_lines.append(f"G00 X{cx:.1f} Y{cy:.1f} Z{z_safe}")
            gcode_lines.append(f"G01 Z{z_cut:.1f} F300")
            gcode_lines.append(f"G00 Z{z_safe}")

        elif op_type == "chamfer":
            z_chamfer = bz_max - 0.5
            gcode_lines.append(f"G01 X{bx_min:.1f} Y{by_min:.1f} Z{z_chamfer:.1f} F500")
            gcode_lines.append(f"G01 X{bx_max:.1f} Y{by_min:.1f} Z{z_chamfer:.1f} F500")
            gcode_lines.append(f"G01 X{bx_max:.1f} Y{by_max:.1f} Z{z_chamfer:.1f} F500")
            gcode_lines.append(f"G01 X{bx_min:.1f} Y{by_max:.1f} Z{z_chamfer:.1f} F500")
            gcode_lines.append(f"G00 Z{z_safe}")

    gcode_lines.append("G00 Z10")
    gcode = "\n".join(gcode_lines)

    # Run simulation
    result = sim.execute_gcode(gcode)

    # Get final mesh
    final_mesh = sim.current_stock_mesh
    glb_bytes = _mesh_to_glb_bytes(final_mesh)

    return {
        "glb_bytes": glb_bytes,
        "initial_glb_bytes": _mesh_to_glb_bytes(stock_mesh),
        "target_glb_bytes": _mesh_to_glb_bytes(target_mesh),
        "moves_executed": result.moves_executed,
        "total_volume_removed": result.total_volume_removed,
        "total_time_ms": result.total_time_ms,
        "warnings": result.warnings,
        "gouge_count": len(result.gouges),
        "simulation_success": result.success,
    }


@app.post("/api/subcad/presets")
async def subcad_preset_simulate(req: _PresetRequest):
    """Simulate a SubCAD preset part."""
    try:
        # Build stock from preset
        part, initial_stock_mesh, final_part_mesh, plan = _build_stock_from_preset(
            req.preset, req.width, req.length, req.height
        )
    except ImportError as e:
        return Response(
            content=json.dumps({"error": f"SubCAD not available: {e}"}),
            status_code=500,
            media_type="application/json",
        )
    except ValueError as e:
        return Response(
            content=json.dumps({"error": str(e)}),
            status_code=400,
            media_type="application/json",
        )
    except Exception as e:
        return Response(
            content=json.dumps({"error": f"Failed to build part: {e}"}),
            status_code=500,
            media_type="application/json",
        )

    # Preset simulations use a synthetic, scaled stock mesh as a visual
    # reference for gouge/deviation stats. It is demo-only and must not be
    # treated as CAD validation of the generated SubCAD part.
    demo_reference_scale = 0.95
    demo_reference_mesh = initial_stock_mesh.copy()
    demo_reference_mesh.vertices = demo_reference_mesh.vertices * demo_reference_scale

    try:
        result = _run_subcad_simulation(
            initial_stock_mesh, demo_reference_mesh, plan, req.resolution
        )
    except Exception as e:
        traceback_str = _traceback_module.format_exc()
        return Response(
            content=json.dumps({
                "error": f"Simulation failed: {e}",
                "traceback": traceback_str,
            }),
            status_code=500,
            media_type="application/json",
        )

    # Return smooth CadQuery meshes for display, simulation stats for analysis
    import base64

    return {
        "success": result["simulation_success"],
        "moves_executed": result["moves_executed"],
        "total_volume_removed": round(result["total_volume_removed"], 2),
        "total_time_ms": round(result["total_time_ms"], 1),
        "gouge_count": result["gouge_count"],
        "warnings": result["warnings"],
        "glb_base64": base64.b64encode(
            _mesh_to_glb_bytes(final_part_mesh)
        ).decode("ascii"),
        "initial_glb_base64": base64.b64encode(
            _mesh_to_glb_bytes(initial_stock_mesh)
        ).decode("ascii"),
        "target_glb_base64": base64.b64encode(
            _mesh_to_glb_bytes(demo_reference_mesh)
        ).decode("ascii"),
        "target_reference": {
            "source": "demo_scaled_stock",
            "scale": demo_reference_scale,
            "validation": False,
            "description": (
                "Synthetic preset reference only; not real CAD validation."
            ),
        },
        "preset": req.preset,
        "operations_count": len(plan.get("operations", [])),
    }


@app.get("/api/subcad/presets")
async def list_subcad_presets():
    """List available SubCAD presets."""
    return {
        "presets": [
            {"id": k, **v} for k, v in _PRESET_DEFS.items()
        ]
    }


# =============================================================================
#  CLI entry point
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.api:app", host="0.0.0.0", port=8000, reload=True)
