// app.js — Main orchestration for d2m CNC simulator web frontend
//
// Handles file upload, simulation control, UI state, and wires together
// the 3D viewer and WebSocket client.

import { Viewer } from './viewer.js';
import { SimulationWSClient } from './ws-client.js';
import { startBrowserSimulation } from './sim-integration.js';

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const API_BASE = window.location.origin;  // same-origin for unified server

// ---------------------------------------------------------------------------
// Application state
// ---------------------------------------------------------------------------

const state = {
  partId: null,
  operationCount: 0,
  currentOpIndex: -1,
  isSimulating: false,
  isPaused: false,
  meshes: [],          // ArrayBuffer for each operation mesh (server path)
  totalOps: 0,
  completed: false,
  simResult: null,     // Result from complete message
  stockFile: null,
  targetFile: null,
  gcodeText: '',
  toolType: 'ball_endmill',
  toolDiameter: 6.0,
  resolution: 1.0,
  toolpathPoints: [],  // [[x,y,z], ...] for toolpath line
  opDetails: [],       // Per-operation stats for operation list
  isBrowserSim: false, // true when using WebGPU browser simulation
  browserMeshes: [],   // [{vertices, indices}, ...] for browser sim playback
  browserInitialMesh: null, // initial stock mesh for browser sim
};

// ---------------------------------------------------------------------------
// DOM element references
// ---------------------------------------------------------------------------

const els = {
  dropZone: document.getElementById('drop-zone'),
  stockInput: document.getElementById('stock-input'),
  targetInput: document.getElementById('target-input'),
  stockLabel: document.getElementById('stock-label'),
  targetLabel: document.getElementById('target-label'),
  gcodeTextarea: document.getElementById('gcode-textarea'),
  simulateBtn: document.getElementById('simulate-btn'),
  progressBar: document.getElementById('progress-bar'),
  progressText: document.getElementById('progress-text'),
  opSlider: document.getElementById('op-slider'),
  opLabel: document.getElementById('op-label'),
  playBtn: document.getElementById('play-btn'),
  pauseBtn: document.getElementById('pause-btn'),
  stepFwdBtn: document.getElementById('step-fwd-btn'),
  stepBackBtn: document.getElementById('step-back-btn'),
  statsVolume: document.getElementById('stat-volume'),
  statsTime: document.getElementById('stat-time'),
  statsGouges: document.getElementById('stat-gouges'),
  statsOps: document.getElementById('stat-ops'),
  toolToggle: document.getElementById('tool-toggle'),
  targetToggle: document.getElementById('target-toggle'),
  wireframeToggle: document.getElementById('wireframe-toggle'),
  heatmapToggle: document.getElementById('heatmap-toggle'),
  toolTypeSelect: document.getElementById('tool-type'),
  toolDiameterInput: document.getElementById('tool-diameter'),
  resolutionInput: document.getElementById('resolution'),
  opList: document.getElementById('op-list'),
  downloadBtnStl: document.getElementById('download-btn-stl'),
  downloadBtnGlb: document.getElementById('download-btn-glb'),
  toast: document.getElementById('toast'),
  toastMsg: document.getElementById('toast-msg'),
};

// ---------------------------------------------------------------------------
// Viewer and WebSocket client
// ---------------------------------------------------------------------------

const viewer = new Viewer();

const wsClient = new SimulationWSClient({
  onConnected: () => {
    state.isSimulating = true;
    updateUIState();
  },

  onProgress: async (data) => {
    if (data.opIndex < 0) {
      // Initial state message (opIndex -1) — skip, we already loaded via REST
      return;
    }

    state.currentOpIndex = data.opIndex;
    state.totalOps = data.totalOps;
    state.operationCount = data.opIndex + 1;

    // Update viewer with new mesh (via WebSocket base64 or REST fallback)
    if (data.meshBuffer) {
      state.meshes[data.opIndex + 1] = data.meshBuffer;
      viewer.updateStockMesh(data.meshBuffer).catch(e => console.error('Mesh update error:', e));
    } else if (data.meshTooLarge && state.partId) {
      // Fallback: fetch mesh via REST API
      try {
        const resp = await fetch(`${API_BASE}/api/mesh/${state.partId}/${data.opIndex}`);
        if (resp.ok) {
          const buf = await resp.arrayBuffer();
          state.meshes[data.opIndex + 1] = buf;
          await viewer.updateStockMesh(buf);
        }
      } catch (e) {
        console.error('REST mesh fallback error:', e);
      }
    }

    // Collect toolpath point
    if (data.endPosition) {
      state.toolpathPoints[data.opIndex] = data.endPosition;
      viewer.setToolpath(state.toolpathPoints.filter(p => p !== undefined && p !== null));
    }

    // Update tool position
    if (data.endPosition) {
      viewer.updateTool(
        data.endPosition,
        null,
        state.toolType,
        state.toolDiameter,
        30
      );
    }

    // Store operation detail
    state.opDetails[data.opIndex] = {
      volume: data.volumeThisMove || 0,
      cumulativeVolume: data.volumeRemoved,
      gouges: data.gougesFound,
    };

    // Update UI
    updateProgress(data.opIndex, data.totalOps);
    updateStats(data.volumeRemoved, data.gougesFound, state.operationCount);
    updateOpList(data.opIndex, data.totalOps);
  },

  onComplete: (data) => {
    state.completed = true;
    state.isSimulating = false;
    state.simResult = data;

    // Set the complete toolpath
    if (data.toolpathPositions && data.toolpathPositions.length > 0) {
      state.toolpathPoints = data.toolpathPositions;
      viewer.setToolpath(data.toolpathPositions);
    }

    // Show gouge markers
    viewer.addGougeMarkers(data.gouges || []);

    updateUIState();
    updateStats(data.totalVolumeRemoved, data.gougeCount, data.totalOps, data.totalTimeMs);
    updateOpListComplete(data.totalOps);
    showToast(`Simulation complete: ${data.totalOps} operations, ${data.totalVolumeRemoved.toFixed(1)} mm3 removed`);
  },

  onError: (message) => {
    state.isSimulating = false;
    updateUIState();
    showToast(`Error: ${message}`, true);
  },

  onDisconnected: () => {
    if (state.isSimulating && !state.completed) {
      showToast('WebSocket disconnected unexpectedly', true);
    }
    state.isSimulating = false;
    updateUIState();
  },
});

// ---------------------------------------------------------------------------
// Initialization
// ---------------------------------------------------------------------------

function init() {
  viewer.init(document.getElementById('viewport'));

  // Show a default 20mm cube immediately so the viewport is not empty
  viewer.loadDefaultCube();

  // Sync initial G-code from textarea
  state.gcodeText = els.gcodeTextarea.value.trim();

  // Generate default stock/target STL files so simulate is ready immediately
  if (!state.stockFile) {
    state.stockFile = makeBoxSTLFile('default_stock.stl', 20, 20, 20);
    els.stockLabel.textContent = 'default_stock.stl (20mm cube)';
  }
  if (!state.targetFile) {
    state.targetFile = makeBoxSTLFile('default_target.stl', 20, 20, 16);
    els.targetLabel.textContent = 'default_target.stl (20x20x16mm)';
  }

  // Load initial empty state
  setupEventListeners();
  setupCameraControls();
  updateUIState();
  showToast('Ready — sample G-code and default box meshes loaded');
}

// ---------------------------------------------------------------------------
// Generate a default ASCII STL box mesh as a File object
// ---------------------------------------------------------------------------

function makeBoxSTLFile(filename, sx, sy, sz) {
  const hx = sx / 2, hy = sy / 2, hz = sz / 2;

  // 6 faces, each 2 triangles = 12 triangles
  const faces = [
    // +Z face
    { n: [0,0,1], v: [[-hx,-hy,hz],[ hx,-hy,hz],[-hx, hy,hz]] },
    { n: [0,0,1], v: [[ hx,-hy,hz],[ hx, hy,hz],[-hx, hy,hz]] },
    // -Z face
    { n: [0,0,-1], v: [[-hx,-hy,-hz],[-hx, hy,-hz],[ hx,-hy,-hz]] },
    { n: [0,0,-1], v: [[ hx,-hy,-hz],[-hx, hy,-hz],[ hx, hy,-hz]] },
    // +Y face
    { n: [0,1,0], v: [[-hx, hy,-hz],[-hx, hy, hz],[ hx, hy,-hz]] },
    { n: [0,1,0], v: [[ hx, hy,-hz],[-hx, hy, hz],[ hx, hy, hz]] },
    // -Y face
    { n: [0,-1,0], v: [[-hx,-hy,-hz],[ hx,-hy,-hz],[-hx,-hy, hz]] },
    { n: [0,-1,0], v: [[ hx,-hy,-hz],[ hx,-hy, hz],[-hx,-hy, hz]] },
    // +X face
    { n: [1,0,0], v: [[ hx,-hy,-hz],[ hx, hy,-hz],[ hx,-hy, hz]] },
    { n: [1,0,0], v: [[ hx,-hy, hz],[ hx, hy,-hz],[ hx, hy, hz]] },
    // -X face
    { n: [-1,0,0], v: [[-hx,-hy,-hz],[-hx,-hy, hz],[-hx, hy,-hz]] },
    { n: [-1,0,0], v: [[-hx,-hy, hz],[-hx, hy, hz],[-hx, hy,-hz]] },
  ];

  let stl = 'solid ' + filename.replace(/\.stl$/i, '') + '\n';
  for (const f of faces) {
    stl += `  facet normal ${f.n[0]} ${f.n[1]} ${f.n[2]}\n`;
    stl += '    outer loop\n';
    for (const v of f.v) {
      stl += `      vertex ${v[0]} ${v[1]} ${v[2]}\n`;
    }
    stl += '    endloop\n';
    stl += '  endfacet\n';
  }
  stl += 'endsolid\n';

  return new File([stl], filename, { type: 'application/sla' });
}

// ---------------------------------------------------------------------------
// Event listeners
// ---------------------------------------------------------------------------

function setupEventListeners() {
  // Drop zone
  const dz = els.dropZone;
  dz.addEventListener('dragover', (e) => { e.preventDefault(); dz.classList.add('drag-over'); });
  dz.addEventListener('dragleave', () => dz.classList.remove('drag-over'));
  dz.addEventListener('drop', (e) => {
    e.preventDefault();
    dz.classList.remove('drag-over');
    handleDrop(e.dataTransfer.files);
  });

  // File inputs
  els.stockInput.addEventListener('change', () => {
    handleFileSelect(els.stockInput.files, 'stock');
  });
  els.targetInput.addEventListener('change', () => {
    handleFileSelect(els.targetInput.files, 'target');
  });

  // G-code textarea sync
  els.gcodeTextarea.addEventListener('input', () => {
    state.gcodeText = els.gcodeTextarea.value;
    updateUIState();
  });

  // Simulate button
  els.simulateBtn.addEventListener('click', startSimulation);

  // SubCAD preset buttons
  const presets = {
    'preset-pocket-plate': 'pocket_plate',
    'preset-drill-pattern': 'drill_pattern',
    'preset-stepped-block': 'stepped_block',
    'preset-face-mill': 'face_mill_only',
  };
  for (const [elId, presetName] of Object.entries(presets)) {
    const btn = document.getElementById(elId);
    if (btn) {
      btn.addEventListener('click', () => runSubcadPreset(presetName));
    }
  }

  // Playback controls
  els.playBtn.addEventListener('click', () => {
    state.isPaused = false;
    updateUIState();
  });
  els.pauseBtn.addEventListener('click', () => {
    state.isPaused = true;
    updateUIState();
  });
  els.stepFwdBtn.addEventListener('click', stepForward);
  els.stepBackBtn.addEventListener('click', stepBackward);

  // Op slider
  els.opSlider.addEventListener('input', () => {
    const idx = parseInt(els.opSlider.value);
    showOperation(idx);
  });

  // View toggles
  els.toolToggle.addEventListener('change', () => {
    viewer.setToolVisible(els.toolToggle.checked);
  });
  els.targetToggle.addEventListener('change', () => {
    viewer.setTargetVisible(els.targetToggle.checked);
  });
  els.wireframeToggle.addEventListener('change', () => {
    viewer.setWireframeMode(els.wireframeToggle.checked);
  });
  els.heatmapToggle.addEventListener('change', () => {
    viewer.setHeatmapMode(els.heatmapToggle.checked);
  });

  // Download buttons
  els.downloadBtnStl.addEventListener('click', () => downloadResult('stl'));
  els.downloadBtnGlb.addEventListener('click', () => downloadResult('glb'));
}

// ---------------------------------------------------------------------------
// Camera controls (overlay buttons on viewport)
// ---------------------------------------------------------------------------

function setupCameraControls() {
  document.getElementById('cam-zoom-in').addEventListener('click', () => viewer.zoomIn());
  document.getElementById('cam-zoom-out').addEventListener('click', () => viewer.zoomOut());
  document.getElementById('cam-fit').addEventListener('click', () => viewer.fitView());
  document.getElementById('cam-reset').addEventListener('click', () => viewer.resetCamera());
}

// ---------------------------------------------------------------------------
// File handling
// ---------------------------------------------------------------------------

function handleDrop(files) {
  for (const file of files) {
    const name = file.name.toLowerCase();
    if (name.endsWith('.stl') || name.endsWith('.step') || name.endsWith('.stp') || name.endsWith('.obj')) {
      if (name.includes('stock') || name.includes('blank')) {
        state.stockFile = file;
        els.stockLabel.textContent = file.name;
      } else if (name.includes('target') || name.includes('cad') || name.includes('design')) {
        state.targetFile = file;
        els.targetLabel.textContent = file.name;
      } else if (!state.stockFile) {
        state.stockFile = file;
        els.stockLabel.textContent = file.name;
      } else {
        state.targetFile = file;
        els.targetLabel.textContent = file.name;
      }
    } else if (name.endsWith('.nc') || name.endsWith('.gcode') || name.endsWith('.tap') || name.endsWith('.txt')) {
      const reader = new FileReader();
      reader.onload = (e) => {
        state.gcodeText = e.target.result;
        els.gcodeTextarea.value = state.gcodeText;
      };
      reader.readAsText(file);
    }
  }
  updateUIState();
}

function handleFileSelect(fileList, type) {
  if (!fileList || fileList.length === 0) return;
  const file = fileList[0];
  if (type === 'stock') {
    state.stockFile = file;
    els.stockLabel.textContent = file.name;
  } else {
    state.targetFile = file;
    els.targetLabel.textContent = file.name;
  }
  updateUIState();
}

// ---------------------------------------------------------------------------
// Simulation control
// ---------------------------------------------------------------------------

function _resetSimulationState() {
  state.meshes = [];
  state.browserMeshes = [];
  state.browserInitialMesh = null;
  state.currentOpIndex = -1;
  state.operationCount = 0;
  state.totalOps = 0;
  state.completed = false;
  state.isSimulating = false;
  state.simResult = null;
  state.toolpathPoints = [];
  state.opDetails = [];
  state.isBrowserSim = false;
  viewer.setToolpath(null);
  viewer.clearGougeMarkers();
  els.opList.innerHTML = '';
}

async function _runBrowserSimulation() {
  state.isBrowserSim = true;
  state.isSimulating = true;
  els.simulateBtn.disabled = true;
  els.simulateBtn.textContent = 'Simulating on GPU...';
  updateUIState();

  const gpuSimStart = performance.now();

  try {
    await startBrowserSimulation(
      {
        stockFile: state.stockFile,
        targetFile: state.targetFile,
        gcodeText: state.gcodeText,
        toolType: state.toolType,
        toolDiameter: state.toolDiameter,
        resolution: state.resolution,
      },
      {
        onProgress: (data) => {
          if (data.opIndex < 0) {
            // Stage message (parsing, init, etc.) — skip
            return;
          }

          state.currentOpIndex = data.opIndex;
          state.totalOps = data.totalOps;
          state.operationCount = data.opIndex + 1;

          // Update viewer with raw arrays from GPU
          if (data.vertices && data.indices) {
            viewer.loadMeshFromArrays(data.vertices, data.indices);
            // Store for playback
            state.browserMeshes[data.opIndex + 1] = {
              vertices: data.vertices,
              indices: data.indices,
            };
          }

          // Collect toolpath point
          if (data.endPosition) {
            const ep = data.endPosition;
            state.toolpathPoints[data.opIndex] = [ep[0], ep[1], ep[2]];
            viewer.setToolpath(
              state.toolpathPoints.filter(p => p !== undefined && p !== null)
            );
          }

          // Update tool position visualization
          if (data.endPosition) {
            viewer.updateTool(
              data.endPosition,
              null,
              state.toolType,
              state.toolDiameter,
              30
            );
          }

          // Store operation detail
          state.opDetails[data.opIndex] = {
            volume: data.timeMs || 0,
            cumulativeVolume: data.volumeRemoved || 0,
            gouges: 0,
          };

          // Update UI
          updateProgress(data.opIndex, data.totalOps);
          updateStats(
            data.volumeRemoved || 0,
            0,
            state.operationCount
          );
          updateOpList(data.opIndex, data.totalOps);
        },

        onComplete: (data) => {
          const totalTimeMs = performance.now() - gpuSimStart;
          state.completed = true;
          state.isSimulating = false;
          state.simResult = data;

          // Store initial mesh for playback
          if (data.initialMesh) {
            state.browserInitialMesh = data.initialMesh;
          }

          // Final toolpath
          if (state.toolpathPoints.length > 0) {
            viewer.setToolpath(
              state.toolpathPoints.filter(p => p !== undefined && p !== null)
            );
          }

          updateUIState();
          updateStats(
            data.totalVolumeRemoved || 0,
            0,
            data.totalOps,
            totalTimeMs
          );
          updateOpListComplete(data.totalOps);

          const volText = (data.totalVolumeRemoved || 0).toFixed(1);
          showToast(
            `GPU Simulation complete: ${data.totalOps} ops in ${(totalTimeMs / 1000).toFixed(1)}s`
          );

          els.simulateBtn.disabled = false;
          els.simulateBtn.textContent = 'Simulate';
        },

        onError: (message) => {
          state.isSimulating = false;
          state.isBrowserSim = false;
          updateUIState();
          showToast(`Browser sim error: ${message}`, true);
          els.simulateBtn.disabled = false;
          els.simulateBtn.textContent = 'Simulate';
        },
      }
    );
  } catch (err) {
    state.isSimulating = false;
    state.isBrowserSim = false;
    updateUIState();
    showToast(`GPU Simulation error: ${err.message}`, true);
    els.simulateBtn.disabled = false;
    els.simulateBtn.textContent = 'Simulate';
  }
}

// ---------------------------------------------------------------------------
// SubCAD preset simulation
// ---------------------------------------------------------------------------

async function runSubcadPreset(preset) {
  const width = parseFloat(document.getElementById('preset-width')?.value) || 50;
  const length = parseFloat(document.getElementById('preset-length')?.value) || 80;
  const height = parseFloat(document.getElementById('preset-height')?.value) || 20;
  const resolution = parseFloat(els.resolutionInput.value) || 0.5;

  _resetSimulationState();
  state.isSimulating = true;
  state.isBrowserSim = false;
  els.simulateBtn.disabled = true;
  els.simulateBtn.textContent = 'Building...';
  updateUIState();

  showToast(`Building ${preset} via SubCAD and simulating...`);

  try {
    const resp = await fetch(`${API_BASE}/api/subcad/presets`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        preset,
        width,
        length,
        height,
        resolution,
      }),
    });

    if (!resp.ok) {
      const err = await resp.json();
      throw new Error(err.error || `Server error ${resp.status}`);
    }

    const data = await resp.json();

    if (data.error) {
      throw new Error(data.error);
    }

    // Decode GLB base64 to ArrayBuffer
    function b64ToBuffer(b64) {
      const binary = atob(b64);
      const bytes = new Uint8Array(binary.length);
      for (let i = 0; i < binary.length; i++) {
        bytes[i] = binary.charCodeAt(i);
      }
      return bytes.buffer;
    }

    // Load initial (stock) mesh first
    if (data.initial_glb_base64) {
      await viewer.loadStockMesh(b64ToBuffer(data.initial_glb_base64));
    }

    // Load simulated result mesh
    if (data.glb_base64) {
      await viewer.updateStockMesh(b64ToBuffer(data.glb_base64));
    }

    // Load target mesh as reference
    if (data.target_glb_base64) {
      await viewer.loadTargetMesh(b64ToBuffer(data.target_glb_base64));
    }

    // Update stats
    state.completed = true;
    state.simResult = data;
    state.totalOps = data.moves_executed || 0;
    state.operationCount = state.totalOps;
    state.currentOpIndex = state.totalOps;

    updateStats(
      data.total_volume_removed || 0,
      data.gouge_count || 0,
      data.moves_executed || 0,
      data.total_time_ms || 0
    );

    els.progressBar.style.width = '100%';
    els.progressText.textContent = `SubCAD: ${preset} — ${data.moves_executed || 0} moves`;

    showToast(
      `SubCAD ${preset}: ${data.moves_executed || 0} moves, ` +
      `${(data.total_volume_removed || 0).toFixed(1)} mm3 removed, ` +
      `${(data.total_time_ms || 0).toFixed(0)}ms`
    );

  } catch (err) {
    showToast(`Preset error: ${err.message}`, true);
  } finally {
    state.isSimulating = false;
    els.simulateBtn.disabled = false;
    els.simulateBtn.textContent = 'Simulate';
    updateUIState();
  }
}

async function startSimulation() {
  // Read G-code from textarea
  state.gcodeText = els.gcodeTextarea.value.trim();
  if (!state.gcodeText) {
    showToast('Please enter G-code', true);
    return;
  }
  if (!state.stockFile || !state.targetFile) {
    showToast('Please upload stock and target mesh files', true);
    return;
  }

  // Read tool settings
  state.toolType = els.toolTypeSelect.value;
  state.toolDiameter = parseFloat(els.toolDiameterInput.value) || 6.0;
  state.resolution = parseFloat(els.resolutionInput.value) || 1.0;

  // Reset state
  _resetSimulationState();

  // --- Browser WebGPU path ---
  if (navigator.gpu) {
    showToast('Running simulation on GPU (WebGPU)...');
    await _runBrowserSimulation();
    return;
  }

  // --- Server WebSocket path (fallback) ---
  state.isSimulating = true;

  try {
    // Upload meshes
    els.simulateBtn.disabled = true;
    els.simulateBtn.textContent = 'Uploading...';
    showToast('Uploading meshes...');

    const formData = new FormData();
    formData.append('stock', state.stockFile);
    formData.append('target', state.targetFile);
    formData.append('resolution', state.resolution.toString());

    const uploadResp = await fetch(`${API_BASE}/api/upload`, {
      method: 'POST',
      body: formData,
    });

    if (!uploadResp.ok) {
      throw new Error(`Upload failed: ${uploadResp.status}`);
    }

    const uploadData = await uploadResp.json();
    state.partId = uploadData.part_id;
    showToast(`Part uploaded: ${state.partId}`);

    // Load initial stock and target meshes
    await loadInitialMeshes(state.partId);

    // Start WebSocket simulation
    els.simulateBtn.textContent = 'Simulating...';
    showToast('Simulation started...');

    wsClient.connect(state.partId, 'localhost:8000');
    wsClient.sendStart({
      gcode: state.gcodeText,
      toolType: state.toolType,
      toolDiameter: state.toolDiameter,
      resolution: state.resolution,
    });

  } catch (err) {
    showToast(`Error: ${err.message}`, true);
    els.simulateBtn.disabled = false;
    els.simulateBtn.textContent = 'Simulate';
    state.isSimulating = false;
  }
}

async function loadInitialMeshes(partId) {
  try {
    // Load stock mesh
    const stockResp = await fetch(`${API_BASE}/api/mesh/${partId}/initial`);
    if (stockResp.ok) {
      const buf = await stockResp.arrayBuffer();
      await viewer.loadStockMesh(buf);
    }

    // Load target mesh
    const targetResp = await fetch(`${API_BASE}/api/mesh/${partId}/target`);
    if (targetResp.ok) {
      const buf = await targetResp.arrayBuffer();
      await viewer.loadTargetMesh(buf);
      viewer.setTargetVisible(els.targetToggle.checked);
    }
  } catch (err) {
    console.error('Failed to load meshes:', err);
  }
}

// ---------------------------------------------------------------------------
// Progress and stats
// ---------------------------------------------------------------------------

function updateProgress(currentOp, totalOps) {
  const pct = totalOps > 0 ? ((currentOp + 1) / totalOps) * 100 : 0;
  els.progressBar.style.width = `${pct}%`;
  els.progressText.textContent = `Operation ${currentOp + 1} of ${totalOps}`;
  els.opSlider.max = totalOps;
  els.opSlider.value = currentOp + 1;
  els.opLabel.textContent = `Op ${currentOp + 1}/${totalOps}`;
}

function updateStats(volumeRemoved, gougesFound, opsCount, totalTimeMs) {
  els.statsVolume.textContent = volumeRemoved.toFixed(1);
  els.statsGouges.textContent = gougesFound;
  els.statsOps.textContent = opsCount;

  if (totalTimeMs !== undefined) {
    els.statsTime.textContent = (totalTimeMs / 1000).toFixed(1) + 's';
  }
}

function updateOpList(currentOp, totalOps) {
  const container = els.opList;

  // Remove initial placeholder
  if (container.children.length === 1 &&
      container.children[0].textContent.includes('Waiting')) {
    container.innerHTML = '';
  }

  // Extend list if needed
  while (container.children.length <= currentOp) {
    const idx = container.children.length;
    const item = document.createElement('div');
    item.className = 'op-item pending';
    item.title = `Operation ${idx + 1}`;
    item.textContent = `Op ${idx + 1}`;
    container.appendChild(item);
  }

  // Mark status and add volume detail
  for (let i = 0; i < container.children.length; i++) {
    const detail = state.opDetails[i];
    let cls = 'op-item pending';
    let text = `Op ${i + 1}`;

    if (i <= currentOp) {
      cls = 'op-item done';
      if (detail) {
        text = `Op ${i + 1}  Δ${detail.volume.toFixed(1)}mm³`;
      }
    } else if (i === currentOp + 1 && i < totalOps) {
      cls = 'op-item in-progress';
    }

    container.children[i].className = cls;
    container.children[i].textContent = text;
    container.children[i].title = detail
      ? `Vol: ${detail.cumulativeVolume.toFixed(1)} mm³ | Gouges: ${detail.gouges}`
      : text;
  }

  // Scroll to current
  if (container.children[currentOp]) {
    container.children[currentOp].scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }
}

function updateOpListComplete(totalOps) {
  const container = els.opList;
  for (let i = 0; i < container.children.length; i++) {
    if (i < totalOps) {
      const detail = state.opDetails[i];
      container.children[i].className = 'op-item done';
      if (detail) {
        container.children[i].textContent = `Op ${i + 1}  Δ${detail.volume.toFixed(1)}mm³`;
      }
    }
  }
}

// ---------------------------------------------------------------------------
// Playback controls
// ---------------------------------------------------------------------------

function stepForward() {
  if (!state.completed) return;
  const max = state.totalOps;
  const next = Math.min(state.currentOpIndex + 2, max); // +1 for 0-index, +1 for step
  showOperation(next);
}

function stepBackward() {
  if (!state.completed) return;
  const prev = Math.max(state.currentOpIndex, 0);
  showOperation(prev);
}

async function showOperation(opIndex) {
  if (opIndex < 0 || opIndex > state.totalOps) return;

  // --- Browser simulation playback ---
  if (state.isBrowserSim) {
    if (opIndex === 0) {
      // Show initial mesh
      if (state.browserInitialMesh && state.browserInitialMesh.vertices.length > 0) {
        viewer.loadMeshFromArrays(
          state.browserInitialMesh.vertices,
          state.browserInitialMesh.indices
        );
      } else {
        // Fallback: reload default cube
        viewer.loadDefaultCube();
      }
    } else {
      const mesh = state.browserMeshes[opIndex];
      if (mesh && mesh.vertices.length > 0) {
        viewer.loadMeshFromArrays(mesh.vertices, mesh.indices);
      } else if (state.browserMeshes[opIndex - 1]) {
        // Fallback to previous mesh if current is missing
        const prev = state.browserMeshes[opIndex - 1];
        viewer.loadMeshFromArrays(prev.vertices, prev.indices);
      }
    }

    state.currentOpIndex = opIndex;
    els.opSlider.value = opIndex;
    els.opLabel.textContent = `Op ${opIndex}/${state.totalOps}`;
    return;
  }

  // --- Server simulation playback ---
  if (!state.partId) return;

  if (opIndex === 0) {
    // Show initial mesh
    try {
      const resp = await fetch(`${API_BASE}/api/mesh/${state.partId}/initial`);
      if (resp.ok) {
        const buf = await resp.arrayBuffer();
        await viewer.updateStockMesh(buf);
      }
    } catch (e) { /* ignore */ }
  } else {
    try {
      const resp = await fetch(`${API_BASE}/api/mesh/${state.partId}/${opIndex - 1}`);
      if (resp.ok) {
        const buf = await resp.arrayBuffer();
        await viewer.updateStockMesh(buf);
      }
    } catch (e) {
      showToast(`Failed to load mesh for operation ${opIndex}`, true);
    }
  }

  state.currentOpIndex = opIndex;
  els.opSlider.value = opIndex;
  els.opLabel.textContent = `Op ${opIndex}/${state.totalOps}`;
}

// ---------------------------------------------------------------------------
// Download
// ---------------------------------------------------------------------------

async function downloadResult(format) {
  if (!state.partId || !state.completed) {
    showToast('Simulation must complete before downloading', true);
    return;
  }

  const ext = format === 'stl' ? 'stl' : 'glb';
  try {
    const resp = await fetch(`${API_BASE}/api/download/${state.partId}/${ext}`);
    if (!resp.ok) throw new Error(`Download failed: ${resp.status}`);

    const blob = await resp.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${state.partId}_result.${ext}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    showToast(`${ext.toUpperCase()} download started`);
  } catch (e) {
    showToast(`Download error: ${e.message}`, true);
  }
}

// ---------------------------------------------------------------------------
// UI state
// ---------------------------------------------------------------------------

function updateUIState() {
  const hasFiles = state.stockFile && state.targetFile;
  const hasGcode = state.gcodeText && state.gcodeText.trim().length > 0;
  const isReady = hasFiles && hasGcode && !state.isSimulating;

  els.simulateBtn.disabled = !isReady;
  els.simulateBtn.textContent = state.isSimulating ? 'Simulating...' : 'Simulate';

  els.playBtn.disabled = state.isSimulating || !state.completed || !state.isPaused;
  els.pauseBtn.disabled = state.isSimulating || !state.completed || state.isPaused;
  els.stepFwdBtn.disabled = state.isSimulating || !state.completed;
  els.stepBackBtn.disabled = state.isSimulating || !state.completed;
  els.opSlider.disabled = state.isSimulating || !state.completed;
  els.downloadBtnStl.disabled = !state.completed;
  els.downloadBtnGlb.disabled = !state.completed;
}

// ---------------------------------------------------------------------------
// Toast notifications
// ---------------------------------------------------------------------------

let toastTimer = null;

function showToast(message, isError = false) {
  els.toastMsg.textContent = message;
  els.toast.className = 'toast show' + (isError ? ' toast-error' : '');

  if (toastTimer) clearTimeout(toastTimer);
  toastTimer = setTimeout(() => {
    els.toast.className = 'toast';
  }, 4000);
}

// ---------------------------------------------------------------------------
// Boot
// ---------------------------------------------------------------------------

document.addEventListener('DOMContentLoaded', init);
