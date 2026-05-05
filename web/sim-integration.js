/**
 * sim-integration.js — Browser-side simulation orchestrator
 *
 * Wires the WebGPU tri-dexel simulator into the main d2m application.
 * Handles ASCII STL parsing, WebGPU device init, G-code execution,
 * and per-operation mesh extraction with progress callbacks.
 *
 * Replaces the server upload + WebSocket flow when WebGPU is available.
 */

import { WebGPUSimulator, initWebGPU } from './sim/engine.js';
import { createTool } from './sim/tools.js';
import { GCodeParser } from './sim/gcode.js';
import { forward, coordsToJoints } from './sim/kinematics.js';

// ---------------------------------------------------------------------------
// ASCII STL parser
// ---------------------------------------------------------------------------

/**
 * Parse an ASCII STL file into vertices and face indices.
 * Deduplicates vertices (keyed by "x,y,z" rounded to 6 decimal places).
 *
 * @param {File|string} stlSource - File object or string content
 * @returns {Promise<{ vertices: Float32Array, indices: Uint32Array }>}
 */
export async function parseSTL(stlSource) {
  let text;
  if (typeof stlSource === 'string') {
    text = stlSource;
  } else if (stlSource instanceof File) {
    text = await stlSource.text();
  } else if (stlSource.text && typeof stlSource.text === 'function') {
    text = await stlSource.text();
  } else {
    throw new Error('STL source must be a File object or string');
  }

  const lines = text.split('\n');
  const rawVertices = []; // flat array of [x,y,z, x,y,z, ...]
  const PRECISION = 6;
  const vertexMap = new Map(); // "x,y,z" -> index
  const uniqueVerts = []; // flat Float32Array builder
  const indices = [];

  let facetVerts = []; // vertices for current facet

  for (const rawLine of lines) {
    const line = rawLine.trim();
    if (line.startsWith('vertex') || line.startsWith('vertex ')) {
      const parts = line.split(/\s+/);
      // "vertex x y z"
      if (parts.length >= 4) {
        const x = parseFloat(parts[1]);
        const y = parseFloat(parts[2]);
        const z = parseFloat(parts[3]);
        if (!isNaN(x) && !isNaN(y) && !isNaN(z)) {
          facetVerts.push([x, y, z]);
        }
      }
    }

    if (line === 'endfacet' || line.startsWith('endfacet')) {
      // Each facet has exactly 3 vertices, emit a triangle
      if (facetVerts.length === 3) {
        for (const v of facetVerts) {
          const key = v.map(c => c.toFixed(PRECISION)).join(',');
          let idx = vertexMap.get(key);
          if (idx === undefined) {
            idx = uniqueVerts.length / 3;
            vertexMap.set(key, idx);
            uniqueVerts.push(v[0], v[1], v[2]);
          }
          indices.push(idx);
        }
      }
      facetVerts = [];
    }
  }

  // Handle case where there's no explicit endfacet (last facet)
  if (facetVerts.length === 3) {
    for (const v of facetVerts) {
      const key = v.map(c => c.toFixed(PRECISION)).join(',');
      let idx = vertexMap.get(key);
      if (idx === undefined) {
        idx = uniqueVerts.length / 3;
        vertexMap.set(key, idx);
        uniqueVerts.push(v[0], v[1], v[2]);
      }
      indices.push(idx);
    }
  }

  if (uniqueVerts.length === 0) {
    throw new Error('STL parsing failed: no vertices found');
  }

  return {
    vertices: new Float32Array(uniqueVerts),
    indices: new Uint32Array(indices),
  };
}

// ---------------------------------------------------------------------------
// Shader source cache
// ---------------------------------------------------------------------------

let _shaderCache = null;

/**
 * Load WGSL shader sources from the server.
 * Results are cached so subsequent calls are instant.
 *
 * @returns {Promise<{ subtractSrc: string, marchingSrc: string }>}
 */
async function loadShaders() {
  if (_shaderCache) return _shaderCache;
  const [subtractSrc, marchingSrc] = await Promise.all([
    fetch('./shaders/dexel_subtract.wgsl').then(r => r.text()),
    fetch('./shaders/marching_cubes.wgsl').then(r => r.text()),
  ]);
  _shaderCache = { subtractSrc, marchingSrc };
  return _shaderCache;
}

// ---------------------------------------------------------------------------
// Main entry point
// ---------------------------------------------------------------------------

/**
 * Start a browser-side (WebGPU) material removal simulation.
 *
 * @param {Object} params
 * @param {File} params.stockFile - ASCII STL File for the stock
 * @param {File} params.targetFile - ASCII STL File for the target (unused in MVP)
 * @param {string} params.gcodeText - G-code program text
 * @param {string} params.toolType - 'ball_endmill' | 'flat_endmill' | 'drill'
 * @param {number} params.toolDiameter - Tool diameter in mm
 * @param {number} params.resolution - Grid resolution in mm
 * @param {Object} callbacks
 * @param {Function} callbacks.onProgress - ({ opIndex, totalOps, vertices, indices, endPosition, volumeRemoved, timeMs })
 * @param {Function} callbacks.onComplete - ({ totalOps, totalVolumeRemoved, totalTimeMs, finalMesh })
 * @param {Function} callbacks.onError - (message)
 * @returns {Promise<{ simulator: WebGPUSimulator, device: GPUDevice, totalTimeMs: number }>}
 */
export async function startBrowserSimulation(params, callbacks = {}) {
  const {
    stockFile,
    gcodeText,
    toolType = 'ball_endmill',
    toolDiameter = 6.0,
    resolution = 2.0,
  } = params;

  // ---- 1. Parse stock STL ----
  callbacks.onProgress && callbacks.onProgress({
    opIndex: -1,
    totalOps: 0,
    vertices: null,
    indices: null,
    endPosition: null,
    volumeRemoved: 0,
    timeMs: 0,
    stage: 'parsing_stl',
  });

  let stockMesh;
  try {
    stockMesh = await parseSTL(stockFile);
  } catch (err) {
    callbacks.onError && callbacks.onError(`STL parse error: ${err.message}`);
    throw err;
  }

  // ---- 2. Initialize WebGPU ----
  let device;
  try {
    ({ device } = await initWebGPU());
  } catch (err) {
    callbacks.onError && callbacks.onError(`WebGPU init error: ${err.message}`);
    throw err;
  }

  // ---- 3. Load WGSL shaders ----
  let subtractSrc, marchingSrc;
  try {
    ({ subtractSrc, marchingSrc } = await loadShaders());
  } catch (err) {
    callbacks.onError && callbacks.onError(`Shader load error: ${err.message}`);
    throw err;
  }

  // ---- 4. Create and initialize simulator ----
  const simulator = new WebGPUSimulator(device, stockMesh, { resolution });
  try {
    await simulator.initialize(subtractSrc, marchingSrc);
  } catch (err) {
    callbacks.onError && callbacks.onError(`Simulator init error: ${err.message}`);
    throw err;
  }

  // ---- 5. Parse G-code ----
  const parser = new GCodeParser();
  let commands;
  try {
    commands = parser.parse(gcodeText);
  } catch (err) {
    callbacks.onError && callbacks.onError(`G-code parse error: ${err.message}`);
    throw err;
  }

  if (commands.length === 0) {
    callbacks.onError && callbacks.onError('No G-code motion commands found');
    return { simulator, device, totalTimeMs: 0 };
  }

  // ---- 6. Create tool ----
  const tool = createTool(toolType, {
    diameter: toolDiameter,
    fluteLength: 30,
    length: 80,
  });

  // ---- 7. Execute moves ----
  let prevJoints = [0, 0, 0, 0, 0, 0];
  let lastPose = { position: [0, 0, 5], axis: [0, 0, 1] };
  let cumulativeVolumeRemoved = 0;
  let totalTimeMs = 0;
  const totalOps = commands.length;

  // Capture initial mesh
  let initialMesh = null;
  try {
    initialMesh = await simulator.getStockMesh();
  } catch (e) {
    // non-fatal: proceed without initial mesh capture
  }

  for (let i = 0; i < commands.length; i++) {
    const cmd = commands[i];

    // Build joints from G-code coords
    const joints = coordsToJoints(cmd.coords, prevJoints);

    // Forward kinematics: joint space -> workpiece pose
    const fk = forward(joints);
    const currentPose = {
      position: fk.position,
      axis: fk.axis,
    };

    // Execute the move on GPU (only G01 feed moves remove material)
    let moveResult = { timeMs: 0, columnsModified: 0, volumeRemoved: 0 };
    if (cmd.motion === 'G01') {
      try {
        moveResult = await simulator.executeMove(tool, lastPose, currentPose, {
          linearRes: resolution,
        });
      } catch (err) {
        callbacks.onError && callbacks.onError(
          `GPU error on op ${i + 1}: ${err.message}`
        );
        // Continue with next move
      }
    }

    totalTimeMs += moveResult.timeMs;

    // Extract mesh after this operation
    let meshResult = { vertices: new Float32Array(0), indices: new Uint32Array(0) };
    try {
      meshResult = await simulator.getStockMesh();
    } catch (err) {
      console.error(`Mesh extraction error on op ${i + 1}:`, err);
    }

    // Estimate volume removed (simple heuristic: change in vertex count)
    cumulativeVolumeRemoved += moveResult.timeMs > 0 ? 1 : 0;

    // Progress callback
    callbacks.onProgress && callbacks.onProgress({
      opIndex: i,
      totalOps,
      vertices: meshResult.vertices,
      indices: meshResult.indices,
      endPosition: fk.position,
      volumeRemoved: cumulativeVolumeRemoved,
      timeMs: moveResult.timeMs,
    });

    prevJoints = joints;
    lastPose = currentPose;
  }

  // ---- 8. Final mesh extraction ----
  let finalMesh = { vertices: new Float32Array(0), indices: new Uint32Array(0) };
  try {
    finalMesh = await simulator.getStockMesh();
  } catch (err) {
    console.error('Final mesh extraction error:', err);
  }

  // ---- 9. Complete callback ----
  callbacks.onComplete && callbacks.onComplete({
    totalOps,
    totalVolumeRemoved: cumulativeVolumeRemoved,
    totalTimeMs,
    finalMesh,
    initialMesh,
  });

  return { simulator, device, totalTimeMs, initialMesh, finalMesh };
}
