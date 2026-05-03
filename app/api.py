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
#  CLI entry point
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.api:app", host="0.0.0.0", port=8000, reload=True)
