"""Unified server for d2m CNC simulator.

Starts a FastAPI server on port 8080 that:
  - Serves the web/ frontend as static files
  - Hosts the simulation REST + WebSocket API
  - Provides SubCAD preset simulation endpoints

Usage:
    python serve.py                # start on port 8080
    python serve.py --port 3000    # custom port
    python serve.py --reload       # auto-reload on file changes
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))


def build_app():
    """Build the full FastAPI application with API routes and static files."""
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.staticfiles import StaticFiles

    app = FastAPI(
        title="d2m CNC Simulator",
        version="0.2.0",
        description="5-Axis CNC material removal simulator with SubCAD integration",
    )

    # CORS for dev
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register API routes from app.api
    from app.api import (
        upload, get_initial_mesh, get_target_mesh, get_final_mesh,
        get_mesh, get_deviation, get_gouges, download_stl, download_glb,
        health, ws_simulate,
    )
    app.post("/api/upload")(upload)
    app.get("/api/mesh/{part_id}/initial")(get_initial_mesh)
    app.get("/api/mesh/{part_id}/target")(get_target_mesh)
    app.get("/api/mesh/{part_id}/final")(get_final_mesh)
    app.get("/api/mesh/{part_id}/{op_index}")(get_mesh)
    app.get("/api/deviation/{part_id}")(get_deviation)
    app.get("/api/gouges/{part_id}")(get_gouges)
    app.get("/api/download/{part_id}/stl")(download_stl)
    app.get("/api/download/{part_id}/glb")(download_glb)
    app.get("/api/health")(health)
    app.websocket("/ws/simulate/{part_id}")(ws_simulate)

    # Register SubCAD preset endpoints
    from app.api import subcad_preset_simulate, list_subcad_presets
    app.post("/api/subcad/presets")(subcad_preset_simulate)
    app.get("/api/subcad/presets")(list_subcad_presets)

    # Serve web frontend as static files
    web_dir = PROJECT_ROOT / "web"
    if web_dir.is_dir():
        app.mount("/", StaticFiles(directory=str(web_dir), html=True), name="static")

    return app


def main():
    parser = argparse.ArgumentParser(
        description="d2m CNC Simulator - Unified Server",
    )
    parser.add_argument("--port", type=int, default=8080, help="Port to listen on (default: 8080)")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload on file changes")
    args = parser.parse_args()

    print(f"""
  ============================================
    d2m - 5-Axis CNC Simulator
  ============================================
    Frontend:  http://localhost:{args.port}
    API:       http://localhost:{args.port}/api
    Health:    http://localhost:{args.port}/api/health
    API Docs:  http://localhost:{args.port}/docs
  ============================================
""")

    import uvicorn

    app = build_app()

    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level="info",
    )


if __name__ == "__main__":
    main()
