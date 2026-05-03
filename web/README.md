# d2m Web Frontend

Browser-based 3D viewer for the d2m 5-axis CNC simulator.

## Setup

1. Start the Python backend (from project root):

   ```bash
   python -m app.api
   ```

   The FastAPI server starts at `http://localhost:8000`.

2. Serve the frontend (from the `web/` directory):

   ```bash
   cd web
   python -m http.server 8080
   ```

   Or open `web/index.html` directly in a browser (some features require a local HTTP server).

3. Open `http://localhost:8080` in a modern browser (Chrome/Firefox recommended).

## Usage

1. **Upload meshes**: Drag and drop STL/STEP files for stock and target, or use the file buttons.
2. **Enter G-code**: Type or paste your G-code program, or drop a `.nc` file.
3. **Configure tool**: Select tool type, diameter, and simulation resolution.
4. **Simulate**: Click "Simulate" to upload meshes, run the simulation, and stream results.
5. **Playback**: After simulation completes, use the playback controls to step through operations.
6. **Download**: Export the final machined part as STL or GLB.

## Files

- `index.html` -- Main page layout (dark theme, sidebar + viewport)
- `style.css` -- Dark theme styling
- `app.js` -- Application orchestration (upload, simulation control, UI)
- `viewer.js` -- Three.js 3D viewer module
- `ws-client.js` -- WebSocket client for streaming simulation

## Dependencies

All loaded from CDN -- no bundler required.

- Three.js 0.160.0 (3D rendering)
- Modern browser with WebGL and ES modules support

## API Backend

The frontend expects the FastAPI backend at `http://localhost:8000`. See `../app/api.py` for the API.
