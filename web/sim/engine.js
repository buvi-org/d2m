/**
 * engine.js — WebGPU Tri-Dexel Simulation Engine
 *
 * Orchestration layer that manages WebGPU compute pipelines for the entire
 * tri-dexel material removal simulation loop. All compute runs on the browser GPU.
 *
 * Python reference:
 *   src/simulation/material_removal.py — MaterialRemovalEngine
 *   src/simulation/tri_dexel.py — TriDexelModel, DexelGrid, DexelColumn
 *   src/simulation/surface.py — tri_dexel_to_mesh
 *
 * Architecture C: WebGPU Compute + WebGL Render
 *   - WebGPU compute shaders: dexel subtraction, marching cubes
 *   - CPU JavaScript: orchestration, buffer management, culling, readback
 *   - WebGL/Three.js: render output mesh (external)
 */

// ---------------------------------------------------------------------------
// Constants (must match WGSL shader constants)
// ---------------------------------------------------------------------------

const MAX_COLUMN_INTERVALS = 64;   // max [s,e] pairs per column
const MAX_TOOL_INTERVALS = 4;      // max tool intersection pairs
const WORKGROUP_SIZE = 64;

const AXIS_Z = 0;
const AXIS_X = 1;
const AXIS_Y = 2;

// ---------------------------------------------------------------------------
// WebGPUSimulator
// ---------------------------------------------------------------------------

export class WebGPUSimulator {
  /**
   * @param {GPUDevice} device - Initialized WebGPU device
   * @param {Object} stockMesh - { vertices: Float32Array, indices: Uint32Array } (unitless; scaled below)
   * @param {Object} options
   * @param {number} [options.resolution=0.5] - Grid spacing in mm
   * @param {[number,number,number]} [options.origin] - Grid origin in mm (default: mesh min corner)
   * @param {[number,number,number]} [options.gridSize] - Grid dimensions in mm
   */
  constructor(device, stockMesh, options = {}) {
    this.device = device;

    /** Resolution in mm */
    this.resolution = options.resolution || 0.5;

    /** Stock mesh for initialization */
    this.stockMesh = stockMesh;

    // Compute grid bounds from mesh or options
    const v = stockMesh.vertices;
    let minX = Infinity, minY = Infinity, minZ = Infinity;
    let maxX = -Infinity, maxY = -Infinity, maxZ = -Infinity;
    for (let i = 0; i < v.length; i += 3) {
      minX = Math.min(minX, v[i]);   maxX = Math.max(maxX, v[i]);
      minY = Math.min(minY, v[i+1]); maxY = Math.max(maxY, v[i+1]);
      minZ = Math.min(minZ, v[i+2]); maxZ = Math.max(maxZ, v[i+2]);
    }
    this.origin = options.origin || [minX, minY, minZ];
    const gridSize = options.gridSize || [maxX - minX, maxY - minY, maxZ - minZ];

    // Number of cells per axis
    this.nx = Math.max(1, Math.ceil(gridSize[0] / this.resolution));
    this.ny = Math.max(1, Math.ceil(gridSize[1] / this.resolution));
    this.nz = Math.max(1, Math.ceil(gridSize[2] / this.resolution));

    // Axis-specific grid dimensions
    // Z-grid: XY plane, nu = nx, nv = ny
    // X-grid: YZ plane, nu = ny, nv = nz
    // Y-grid: XZ plane, nu = nx, nv = nz
    this.gridDims = {
      [AXIS_Z]: { nu: this.nx, nv: this.ny, total: this.nx * this.ny },
      [AXIS_X]: { nu: this.ny, nv: this.nz, total: this.ny * this.nz },
      [AXIS_Y]: { nu: this.nx, nv: this.nz, total: this.nx * this.nz },
    };

    // Total columns across all grids
    this.totalColumns = this.gridDims[AXIS_Z].total +
                        this.gridDims[AXIS_X].total +
                        this.gridDims[AXIS_Y].total;

    // Buffer sizes
    this._computeBufferSizes();

    // Pipelines (created in initialize())
    /** @type {GPUComputePipeline|null} */
    this.subtractPipeline = null;
    /** @type {GPUComputePipeline|null} */
    this.marchingPipeline = null;

    // Bind groups per axis for subtract shader
    /** @type {Map<number, GPUBindGroup>} */
    this.subtractBindGroups = new Map();
    /** @type {GPUBindGroup|null} */
    this.marchingBindGroup = null;

    // GPU buffers
    this._createBuffers();

    // Statistics
    this.stats = {
      movesExecuted: 0,
      totalGPUtimeMs: 0,
      columnsModified: 0,
      volumeRemoved: 0,
    };

    // Current pose for swept moves
    /** @type {{position: [number,number,number], axis: [number,number,number]}|null} */
    this.lastPose = null;
  }

  /**
   * Compute required buffer sizes for the dexel grids.
   */
  _computeBufferSizes() {
    let maxCols = 0;
    for (const axis of [AXIS_Z, AXIS_X, AXIS_Y]) {
      maxCols = Math.max(maxCols, this.gridDims[axis].total);
    }
    this.maxColumns = maxCols;

    // Interval buffer: maxCols * MAX_COLUMN_INTERVALS * 2 floats
    this.intervalsFloatCount = maxCols * MAX_COLUMN_INTERVALS * 2;
    this.intervalsByteSize = this.intervalsFloatCount * 4;

    // Column metadata: maxCols * 2 u32s = maxCols * 8 bytes
    this.columnsByteSize = maxCols * 8;

    // Affected cols buffer: worst case all columns in largest grid
    this.affectedColsByteSize = maxCols * 4;

    // Output buffers for marching cubes
    this.maxVertices = maxCols * MAX_COLUMN_INTERVALS * 2; // 2 per interval
    this.maxIndices = this.maxVertices * 3; // triangles, conservative

    // Statistics buffer
    this.statsBufferSize = 8; // 2 x u32
  }

  /**
   * Create all GPU buffers.
   */
  _createBuffers() {
    const device = this.device;
    const usage = GPUBufferUsage;

    // Per-axis interval buffers (read_write for subtract, read for marching)
    this.intervalBuffers = {};
    this.columnMetaBuffers = {};
    this.gridParamBuffers = {};
    this.statsBuffers = {};

    for (const axis of [AXIS_Z, AXIS_X, AXIS_Y]) {
      // Interval buffer: storage (read_write)
      this.intervalBuffers[axis] = device.createBuffer({
        size: this.intervalsByteSize,
        usage: usage.STORAGE | usage.COPY_SRC | usage.COPY_DST,
        label: `intervals_axis_${axis}`,
      });

      // Column metadata: storage (read_write)
      this.columnMetaBuffers[axis] = device.createBuffer({
        size: this.columnsByteSize,
        usage: usage.STORAGE | usage.COPY_SRC | usage.COPY_DST,
        label: `columns_axis_${axis}`,
      });

      // Grid params: uniform (read)
      this.gridParamBuffers[axis] = device.createBuffer({
        size: 32, // 8 floats: axis, resolution, nu, nv, origin_xyz
        usage: usage.UNIFORM | usage.COPY_DST,
        label: `grid_params_axis_${axis}`,
      });

      // Statistics: storage (read_write)
      this.statsBuffers[axis] = device.createBuffer({
        size: this.statsBufferSize,
        usage: usage.STORAGE | usage.COPY_SRC,
        label: `stats_axis_${axis}`,
      });
    }

    // Tool params uniform buffer
    this.toolParamsBuffer = device.createBuffer({
      size: 64, // 16 floats (ToolParams + padding)
      usage: usage.UNIFORM | usage.COPY_DST,
      label: 'tool_params',
    });

    // Affected columns buffer (largest grid)
    this.affectedColsBuffer = device.createBuffer({
      size: this.affectedColsByteSize,
      usage: usage.STORAGE | usage.COPY_DST,
      label: 'affected_cols',
    });

    // Output vertex buffer
    this.vertexBuffer = device.createBuffer({
      size: this.maxVertices * 6 * 4, // 6 floats/vertex * 4 bytes
      usage: usage.STORAGE | usage.COPY_SRC,
      label: 'output_vertices',
    });

    // Output index buffer
    this.indexBuffer = device.createBuffer({
      size: this.maxIndices * 4, // u32 per index
      usage: usage.STORAGE | usage.COPY_SRC,
      label: 'output_indices',
    });

    // Atomic counters for marching cubes
    this.vertexCountBuffer = device.createBuffer({
      size: 4,
      usage: usage.STORAGE | usage.COPY_SRC,
      label: 'vertex_count',
    });
    this.indexCountBuffer = device.createBuffer({
      size: 4,
      usage: usage.STORAGE | usage.COPY_SRC,
      label: 'index_count',
    });

    // Staging buffers for readback
    this.stagingVertexBuffer = device.createBuffer({
      size: this.maxVertices * 6 * 4,
      usage: usage.COPY_DST | usage.MAP_READ,
      label: 'staging_vertices',
    });
    this.stagingIndexBuffer = device.createBuffer({
      size: this.maxIndices * 4,
      usage: usage.COPY_DST | usage.MAP_READ,
      label: 'staging_indices',
    });
    this.stagingStatsBuffer = device.createBuffer({
      size: this.statsBufferSize * 3, // all 3 axes
      usage: usage.COPY_DST | usage.MAP_READ,
      label: 'staging_stats',
    });
    this.stagingVertexCountBuffer = device.createBuffer({
      size: 8, // 2x u32 for vertex + index counts
      usage: usage.COPY_DST | usage.MAP_READ,
      label: 'staging_counts',
    });
  }

  // -------------------------------------------------------------------------
  //  INITIALIZATION
  // -------------------------------------------------------------------------

  /**
   * Initialize the simulator: compile shaders, create pipelines,
   * initialize dexel buffers from stock mesh.
   *
   * @param {string} subtractShaderCode - WGSL source for dexel_subtract.wgsl
   * @param {string} marchingShaderCode - WGSL source for marching_cubes.wgsl
   */
  async initialize(subtractShaderCode, marchingShaderCode) {
    const device = this.device;

    // --- Compile shader modules ---
    const subtractModule = device.createShaderModule({
      code: subtractShaderCode,
      label: 'dexel_subtract',
    });
    const marchingModule = device.createShaderModule({
      code: marchingShaderCode,
      label: 'marching_cubes',
    });

    // --- Create compute pipelines ---
    this.subtractPipeline = device.createComputePipeline({
      layout: 'auto',
      compute: { module: subtractModule, entryPoint: 'main' },
      label: 'subtract_pipeline',
    });

    this.marchingPipeline = device.createComputePipeline({
      layout: 'auto',
      compute: { module: marchingModule, entryPoint: 'main' },
      label: 'marching_pipeline',
    });

    // --- Initialize grid param buffers ---
    this._initGridParams();

    // --- Initialize stock dexel data from mesh ---
    await this._initStockFromMesh();

    // --- Create bind groups ---
    this._createBindGroups();

    // --- Clear statistics buffers ---
    const zeroStats = new Uint32Array([0, 0]);
    for (const axis of [AXIS_Z, AXIS_X, AXIS_Y]) {
      device.queue.writeBuffer(this.statsBuffers[axis], 0, zeroStats);
    }
  }

  /**
   * Upload grid parameters for each axis.
   * Python: tri_dexel.py DexelGrid.__init__ (line 406)
   */
  _initGridParams() {
    const device = this.device;

    const gridConfigs = [
      { axis: AXIS_Z, nu: this.nx, nv: this.ny, origin: this.origin },
      { axis: AXIS_X, nu: this.ny, nv: this.nz, origin: this.origin },
      { axis: AXIS_Y, nu: this.nx, nv: this.nz, origin: this.origin },
    ];

    for (const cfg of gridConfigs) {
      const data = new Float32Array([
        cfg.axis,                    // axis enum
        this.resolution,             // resolution
        cfg.nu,                      // nu_cells
        cfg.nv,                      // nv_cells
        cfg.origin[0],               // origin_x
        cfg.origin[1],               // origin_y
        cfg.origin[2],               // origin_z
        0,                           // padding
      ]);
      device.queue.writeBuffer(this.gridParamBuffers[cfg.axis], 0, data);
    }
  }

  /**
   * Initialize dexel data from stock mesh by CPU ray-casting.
   * Python: tri_dexel.py DexelGrid.init_from_mesh() (line 548)
   *
   * For each grid axis, for each column, cast a ray through the triangle mesh
   * and record entry/exit intervals.
   */
  async _initStockFromMesh() {
    const mesh = this.stockMesh;
    const verts = mesh.vertices;   // Float32Array, [x,y,z, x,y,z, ...]
    const indices = mesh.indices;  // Uint32Array, [i0,i1,i2, i0,i1,i2, ...]

    // Build triangle list
    const tris = [];
    for (let i = 0; i < indices.length; i += 3) {
      const a = indices[i] * 3, b = indices[i + 1] * 3, c = indices[i + 2] * 3;
      tris.push({
        v0: [verts[a], verts[a + 1], verts[a + 2]],
        v1: [verts[b], verts[b + 1], verts[b + 2]],
        v2: [verts[c], verts[c + 1], verts[c + 2]],
      });
    }

    // For each grid axis, CPU ray-cast
    const axisConfigs = [
      { axis: AXIS_Z, nu: this.nx, nv: this.ny, rayDir: [0, 0, 1],  axNu: 0, axNv: 1, axRay: 2 },
      { axis: AXIS_X, nu: this.ny, nv: this.nz, rayDir: [1, 0, 0],  axNu: 1, axNv: 2, axRay: 0 },
      { axis: AXIS_Y, nu: this.nx, nv: this.nz, rayDir: [0, 1, 0],  axNu: 0, axNv: 2, axRay: 1 },
    ];

    for (const cfg of axisConfigs) {
      const { axis, nu, nv, rayDir, axNu, axNv, axRay } = cfg;
      const total = nu * nv;

      // Create interval data array
      const intervalData = new Float32Array(total * MAX_COLUMN_INTERVALS * 2);
      const columnMeta = new Uint32Array(total * 2); // [count, padding] per column

      // For each column, cast a ray
      const res = this.resolution;
      for (let i = 0; i < nu; i++) {
        for (let j = 0; j < nv; j++) {
          const colIdx = i * nv + j;
          const slot = colIdx * MAX_COLUMN_INTERVALS * 2;

          // Compute ray origin
          const origin = [this.origin[0], this.origin[1], this.origin[2]];
          origin[axNu] += (i + 0.5) * res;
          origin[axNv] += (j + 0.5) * res;

          // Collect all ray-triangle intersections along this ray
          const hits = [];
          for (const tri of tris) {
            const t = this._rayTriangleIntersect(origin, rayDir, tri.v0, tri.v1, tri.v2);
            if (t !== null && t > 1e-9) {
              hits.push(t);
            }
          }

          // Sort hits and pair into intervals
          hits.sort((a, b) => a - b);

          let ivCount = 0;
          for (let k = 0; k + 1 < hits.length; k += 2) {
            const entry = hits[k];
            const exit = hits[k + 1];
            if (exit - entry > 1e-9 && ivCount < MAX_COLUMN_INTERVALS) {
              intervalData[slot + ivCount * 2] = entry;
              intervalData[slot + ivCount * 2 + 1] = exit;
              ivCount++;
            }
          }
          // Handle odd number of hits (non-watertight mesh)
          if (hits.length % 2 === 1 && ivCount < MAX_COLUMN_INTERVALS) {
            intervalData[slot + ivCount * 2] = hits[hits.length - 1];
            intervalData[slot + ivCount * 2 + 1] = hits[hits.length - 1] + res;
            ivCount++;
          }

          columnMeta[colIdx * 2] = ivCount;
        }
      }

      // Upload to GPU
      this.device.queue.writeBuffer(this.intervalBuffers[axis], 0, intervalData);
      this.device.queue.writeBuffer(this.columnMetaBuffers[axis], 0, columnMeta);
    }
  }

  /**
   * Moller-Trumbore ray-triangle intersection.
   * Returns t (distance along ray) or null if no intersection.
   *
   * @param {number[]} origin
   * @param {number[]} dir
   * @param {number[]} v0
   * @param {number[]} v1
   * @param {number[]} v2
   * @returns {number|null}
   */
  _rayTriangleIntersect(origin, dir, v0, v1, v2) {
    const EPS = 1e-9;

    const e1 = [v1[0] - v0[0], v1[1] - v0[1], v1[2] - v0[2]];
    const e2 = [v2[0] - v0[0], v2[1] - v0[1], v2[2] - v0[2]];

    const h = [
      dir[1] * e2[2] - dir[2] * e2[1],
      dir[2] * e2[0] - dir[0] * e2[2],
      dir[0] * e2[1] - dir[1] * e2[0],
    ];
    const a = e1[0] * h[0] + e1[1] * h[1] + e1[2] * h[2];

    if (Math.abs(a) < EPS) return null;

    const f = 1 / a;
    const s = [origin[0] - v0[0], origin[1] - v0[1], origin[2] - v0[2]];
    const u = f * (s[0] * h[0] + s[1] * h[1] + s[2] * h[2]);

    if (u < 0 || u > 1) return null;

    const q = [
      s[1] * e1[2] - s[2] * e1[1],
      s[2] * e1[0] - s[0] * e1[2],
      s[0] * e1[1] - s[1] * e1[0],
    ];
    const v = f * (dir[0] * q[0] + dir[1] * q[1] + dir[2] * q[2]);

    if (v < 0 || u + v > 1) return null;

    const t = f * (e2[0] * q[0] + e2[1] * q[1] + e2[2] * q[2]);

    return t > EPS ? t : null;
  }

  /**
   * Create bind groups for each pipeline.
   */
  _createBindGroups() {
    const device = this.device;

    for (const axis of [AXIS_Z, AXIS_X, AXIS_Y]) {
      const bindGroup = device.createBindGroup({
        layout: this.subtractPipeline.getBindGroupLayout(0),
        entries: [
          { binding: 0, resource: { buffer: this.intervalBuffers[axis] } },
          { binding: 1, resource: { buffer: this.columnMetaBuffers[axis] } },
          { binding: 2, resource: { buffer: this.toolParamsBuffer } },
          { binding: 3, resource: { buffer: this.affectedColsBuffer } },
          { binding: 4, resource: { buffer: this.gridParamBuffers[axis] } },
          { binding: 5, resource: { buffer: this.statsBuffers[axis] } },
          { binding: 6, resource: { buffer: this.statsBuffers[axis], offset: 4 } },
        ],
        label: `subtract_bind_group_axis_${axis}`,
      });
      this.subtractBindGroups.set(axis, bindGroup);
    }

    // Marching cubes bind group
    this.marchingBindGroup = device.createBindGroup({
      layout: this.marchingPipeline.getBindGroupLayout(0),
      entries: [
        { binding: 0, resource: { buffer: this.intervalBuffers[AXIS_Z] } },
        { binding: 1, resource: { buffer: this.columnMetaBuffers[AXIS_Z] } },
        { binding: 2, resource: { buffer: this.intervalBuffers[AXIS_X] } },
        { binding: 3, resource: { buffer: this.columnMetaBuffers[AXIS_X] } },
        { binding: 4, resource: { buffer: this.intervalBuffers[AXIS_Y] } },
        { binding: 5, resource: { buffer: this.columnMetaBuffers[AXIS_Y] } },
        { binding: 6, resource: { buffer: this.gridParamBuffers[AXIS_Z] } },
        { binding: 7, resource: { buffer: this.vertexBuffer } },
        { binding: 8, resource: { buffer: this.vertexCountBuffer } },
        { binding: 9, resource: { buffer: this.indexBuffer } },
        { binding: 10, resource: { buffer: this.indexCountBuffer } },
      ],
      label: 'marching_bind_group',
    });
  }

  // -------------------------------------------------------------------------
  //  BOUNDING-BOX CULLING (CPU)
  // -------------------------------------------------------------------------

  /**
   * Compute affected column indices for a grid axis given a world-space AABB.
   * Python: tri_dexel.py DexelGrid.affected_columns() (line 510)
   *
   * @param {number} axis - AXIS_Z, AXIS_X, or AXIS_Y
   * @param {{ min: [number,number,number], max: [number,number,number] }} bbox
   * @returns {Uint32Array}
   */
  _affectedColumns(axis, bbox) {
    const dim = this.gridDims[axis];
    const res = this.resolution;

    // Map bbox to grid-plane coordinates
    let iminF, imaxF, jminF, jmaxF;
    switch (axis) {
      case AXIS_Z: // XY plane, nu=X, nv=Y
        iminF = (bbox.min[0] - this.origin[0]) / res;
        imaxF = (bbox.max[0] - this.origin[0]) / res;
        jminF = (bbox.min[1] - this.origin[1]) / res;
        jmaxF = (bbox.max[1] - this.origin[1]) / res;
        break;
      case AXIS_X: // YZ plane, nu=Y, nv=Z
        iminF = (bbox.min[1] - this.origin[1]) / res;
        imaxF = (bbox.max[1] - this.origin[1]) / res;
        jminF = (bbox.min[2] - this.origin[2]) / res;
        jmaxF = (bbox.max[2] - this.origin[2]) / res;
        break;
      case AXIS_Y: // XZ plane, nu=X, nv=Z
        iminF = (bbox.min[0] - this.origin[0]) / res;
        imaxF = (bbox.max[0] - this.origin[0]) / res;
        jminF = (bbox.min[2] - this.origin[2]) / res;
        jmaxF = (bbox.max[2] - this.origin[2]) / res;
        break;
    }

    const imin = Math.max(0, Math.floor(iminF));
    const imax = Math.min(dim.nu - 1, Math.ceil(imaxF));
    const jmin = Math.max(0, Math.floor(jminF));
    const jmax = Math.min(dim.nv - 1, Math.ceil(jmaxF));

    if (imin > imax || jmin > jmax) {
      return new Uint32Array(0);
    }

    const cols = [];
    for (let i = imin; i <= imax; i++) {
      for (let j = jmin; j <= jmax; j++) {
        cols.push(i * dim.nv + j);
      }
    }
    return new Uint32Array(cols);
  }

  // -------------------------------------------------------------------------
  //  EXECUTE MOVE
  // -------------------------------------------------------------------------

  /**
   * Execute a material removal move on the GPU.
   *
   * @param {import('./tools.js').Tool} tool - Cutting tool
   * @param {{ position: [number,number,number], axis: [number,number,number] }} startPose
   * @param {{ position: [number,number,number], axis: [number,number,number] }} endPose
   * @param {{ samples?: number, linearRes?: number }} [options]
   * @returns {Promise<{ columnsModified: number, volumeRemoved: number, timeMs: number }>}
   */
  async executeMove(tool, startPose, endPose, options = {}) {
    const tStart = performance.now();
    const device = this.device;

    // Interpolate poses for swept volume
    // Python: swept_volume.py SweptVolumeSampler.sample_poses() (line 107)
    const linearRes = options.linearRes || this.resolution;
    const transDist = Math.sqrt(
      (endPose.position[0] - startPose.position[0]) ** 2 +
      (endPose.position[1] - startPose.position[1]) ** 2 +
      (endPose.position[2] - startPose.position[2]) ** 2
    );
    const nSamples = Math.max(2, Math.ceil(transDist / linearRes) + 1);
    const poses = this._interpolatePoses(startPose, endPose, nSamples);

    let totalColsModified = 0;
    let totalVolRemoved = 0;

    // For each interpolated pose, dispatch subtract shader on all 3 grids
    for (const pose of poses) {
      // Upload tool params
      const toolBuf = tool.toGPUBuffer(pose);
      device.queue.writeBuffer(this.toolParamsBuffer, 0, toolBuf);

      // Compute swept bbox for this pose
      const toolBBox = tool.worldBBox(pose);

      for (const axis of [AXIS_Z, AXIS_X, AXIS_Y]) {
        // CPU bounding-box cull
        const affected = this._affectedColumns(axis, toolBBox);
        if (affected.length === 0) continue;

        // Upload affected column indices
        device.queue.writeBuffer(this.affectedColsBuffer, 0, affected);

        // Encode and dispatch compute
        const encoder = device.createCommandEncoder({ label: `subtract_axis_${axis}` });

        // Push error scope for debugging
        device.pushErrorScope('validation');

        const pass = encoder.beginComputePass();
        pass.setPipeline(this.subtractPipeline);
        pass.setBindGroup(0, this.subtractBindGroups.get(axis));
        const workgroups = Math.ceil(affected.length / WORKGROUP_SIZE);
        pass.dispatchWorkgroups(workgroups);
        pass.end();

        device.queue.submit([encoder.finish()]);
      }
    }

    // Wait for GPU to finish
    await device.queue.onSubmittedWorkDone();

    // Check for errors
    const error = await device.popErrorScope();
    if (error) {
      console.error(`GPU error in executeMove: ${error.message}`);
    }

    const tEnd = performance.now();
    const timeMs = tEnd - tStart;

    this.stats.movesExecuted++;
    this.stats.totalGPUtimeMs += timeMs;
    this.lastPose = endPose;

    return {
      columnsModified: totalColsModified,
      volumeRemoved: totalVolRemoved,
      timeMs,
    };
  }

  /**
   * Interpolate tool poses between start and end.
   * Position: linear. Orientation: SLERP.
   * Python: swept_volume.py sample_poses() (line 107)
   *
   * @returns {{ position: [number,number,number], axis: [number,number,number] }[]}
   */
  _interpolatePoses(start, end, n) {
    const poses = [];
    for (let k = 0; k < n; k++) {
      const t = n > 1 ? k / (n - 1) : 0;
      const pos = [
        start.position[0] + t * (end.position[0] - start.position[0]),
        start.position[1] + t * (end.position[1] - start.position[1]),
        start.position[2] + t * (end.position[2] - start.position[2]),
      ];
      const axis = this._slerp(start.axis, end.axis, t);
      poses.push({ position: pos, axis });
    }
    return poses;
  }

  /**
   * SLERP for unit vectors (spherical linear interpolation of directions).
   *
   * @param {[number,number,number]} a - Start direction
   * @param {[number,number,number]} b - End direction
   * @param {number} t - Interpolation parameter [0, 1]
   * @returns {[number,number,number]}
   */
  _slerp(a, b, t) {
    const dot = a[0]*b[0] + a[1]*b[1] + a[2]*b[2];
    const clampedDot = Math.max(-1, Math.min(1, dot));

    if (clampedDot > 0.9995) {
      // Near-parallel: linear interpolation + normalize
      const result = [
        a[0] + t * (b[0] - a[0]),
        a[1] + t * (b[1] - a[1]),
        a[2] + t * (b[2] - a[2]),
      ];
      const len = Math.sqrt(result[0]**2 + result[1]**2 + result[2]**2);
      return [result[0]/len, result[1]/len, result[2]/len];
    }

    const theta0 = Math.acos(clampedDot);
    const sinTheta0 = Math.sin(theta0);
    const theta = theta0 * t;
    const sinTheta = Math.sin(theta);

    const s0 = Math.cos(theta) - clampedDot * sinTheta / sinTheta0;
    const s1 = sinTheta / sinTheta0;

    return [
      s0 * a[0] + s1 * b[0],
      s0 * a[1] + s1 * b[1],
      s0 * a[2] + s1 * b[2],
    ];
  }

  // -------------------------------------------------------------------------
  //  SURFACE EXTRACTION (MARCHING CUBES)
  // -------------------------------------------------------------------------

  /**
   * Extract surface mesh from the current tri-dexel state.
   * Python: surface.py tri_dexel_to_mesh() (line 313)
   *
   * @returns {Promise<{ vertices: Float32Array, indices: Uint32Array }>}
   */
  async getStockMesh() {
    const device = this.device;

    // Zero out atomic counters
    device.queue.writeBuffer(this.vertexCountBuffer, 0, new Uint32Array([0]));
    device.queue.writeBuffer(this.indexCountBuffer, 0, new Uint32Array([0]));

    // Zero out output buffers
    device.queue.writeBuffer(this.vertexBuffer, 0,
      new Float32Array(this.maxVertices * 6));
    device.queue.writeBuffer(this.indexBuffer, 0,
      new Uint32Array(this.maxIndices));

    // Dispatch marching cubes compute shader
    const encoder = device.createCommandEncoder({ label: 'marching_cubes' });
    device.pushErrorScope('validation');

    const pass = encoder.beginComputePass();
    pass.setPipeline(this.marchingPipeline);
    pass.setBindGroup(0, this.marchingBindGroup);

    // Use Z-grid total columns as dispatch size (each thread processes one Z column)
    const zTotal = this.gridDims[AXIS_Z].total;
    const workgroups = Math.ceil(zTotal / WORKGROUP_SIZE);
    pass.dispatchWorkgroups(workgroups);
    pass.end();

    // Copy vertex/index buffers to staging
    encoder.copyBufferToBuffer(this.vertexBuffer, 0,
      this.stagingVertexBuffer, 0, this.maxVertices * 6 * 4);
    encoder.copyBufferToBuffer(this.indexBuffer, 0,
      this.stagingIndexBuffer, 0, this.maxIndices * 4);
    encoder.copyBufferToBuffer(this.vertexCountBuffer, 0,
      this.stagingVertexCountBuffer, 0, 8);

    device.queue.submit([encoder.finish()]);
    await device.queue.onSubmittedWorkDone();

    const error = await device.popErrorScope();
    if (error) {
      console.error(`GPU error in marching cubes: ${error.message}`);
    }

    // Read back vertex count
    await this.stagingVertexCountBuffer.mapAsync(GPUMapMode.READ);
    const countData = new Uint32Array(this.stagingVertexCountBuffer.getMappedRange());
    const vertexCount = countData[0];
    const indexCount = countData[1];
    this.stagingVertexCountBuffer.unmap();

    if (vertexCount === 0) {
      return { vertices: new Float32Array(0), indices: new Uint32Array(0) };
    }

    // Read back vertices (6 floats per vertex)
    await this.stagingVertexBuffer.mapAsync(GPUMapMode.READ);
    const vertexData = new Float32Array(
      this.stagingVertexBuffer.getMappedRange(0, vertexCount * 6 * 4)
    );
    const vertices = new Float32Array(vertexData.slice(0, vertexCount * 3)); // extract just positions
    this.stagingVertexBuffer.unmap();

    // Read back indices
    await this.stagingIndexBuffer.mapAsync(GPUMapMode.READ);
    const actualIdxCount = Math.min(indexCount, this.maxIndices);
    const indexData = new Uint32Array(
      this.stagingIndexBuffer.getMappedRange(0, actualIdxCount * 4)
    );
    const indices = new Uint32Array(indexData);
    this.stagingIndexBuffer.unmap();

    return { vertices, indices };
  }

  /**
   * Build index buffer from vertex positions on CPU.
   * This is a simplified approach: since the shader only extracts vertices,
   * we build indices by grouping vertices from adjacent columns into triangles.
   *
   * For the demo: returns the vertex buffer from getStockMesh() + a very simple
   * point-based rendering (no indices needed for point clouds).
   * A full marching cubes index construction is done in a separate dispatch
   * or on CPU for simplicity.
   */
  async getPointCloud() {
    return this.getStockMesh();
  }

  // -------------------------------------------------------------------------
  //  DEVIATION MAP
  // -------------------------------------------------------------------------

  /**
   * Compare simulated surface to target CAD mesh.
   * Returns per-vertex signed distance deviation.
   * Python: surface.py compare_to_target() (line 354)
   *
   * @param {{ vertices: Float32Array, indices: Uint32Array }} targetMesh
   * @returns {Promise<Float32Array>}
   */
  async getDeviationMap(targetMesh) {
    // This is a CPU implementation for the MVP.
    // Full GPU implementation would use a compute shader with SDF evaluation.
    const targetVerts = targetMesh.vertices;
    const n = targetVerts.length / 3;
    const deviations = new Float32Array(n);

    // Get current stock mesh
    const stock = await this.getStockMesh();

    if (stock.vertices.length === 0) {
      // No stock -> full deviation (all material removed)
      deviations.fill(this.resolution);
      return deviations;
    }

    // Build KD-tree of stock vertices for nearest-neighbor queries
    // (simplified: brute force for MVP)
    for (let i = 0; i < n; i++) {
      const tx = targetVerts[i * 3];
      const ty = targetVerts[i * 3 + 1];
      const tz = targetVerts[i * 3 + 2];

      // Find nearest stock vertex
      let minDistSq = Infinity;
      for (let j = 0; j < stock.vertices.length; j += 3) {
        const dx = tx - stock.vertices[j];
        const dy = ty - stock.vertices[j + 1];
        const dz = tz - stock.vertices[j + 2];
        const d2 = dx*dx + dy*dy + dz*dz;
        if (d2 < minDistSq) minDistSq = d2;
      }

      deviations[i] = Math.sqrt(minDistSq);
    }

    return deviations;
  }

  // -------------------------------------------------------------------------
  //  UTILITIES
  // -------------------------------------------------------------------------

  /**
   * Reset simulator to initial stock state.
   */
  async reset() {
    await this._initStockFromMesh();
    this.stats = {
      movesExecuted: 0,
      totalGPUtimeMs: 0,
      columnsModified: 0,
      volumeRemoved: 0,
    };
    this.lastPose = null;
  }

  /**
   * Get simulation statistics.
   * @returns {{ movesExecuted: number, totalGPUtimeMs: number, gridRes: [number,number,number], totalColumns: number }}
   */
  getStats() {
    return {
      movesExecuted: this.stats.movesExecuted,
      totalGPUtimeMs: this.stats.totalGPUtimeMs,
      resolution: this.resolution,
      gridRes: [this.nx, this.ny, this.nz],
      totalColumns: this.totalColumns,
    };
  }

  /**
   * Get GPU buffer memory usage estimate.
   * @returns {{ totalMB: number, perGridMB: number }}
   */
  getMemoryUsage() {
    const perGridMB = (this.intervalsByteSize + this.columnsByteSize) / (1024 * 1024);
    const totalMB = perGridMB * 3;
    return { totalMB, perGridMB };
  }

  /**
   * Release GPU resources.
   */
  destroy() {
    for (const axis of [AXIS_Z, AXIS_X, AXIS_Y]) {
      this.intervalBuffers[axis]?.destroy();
      this.columnMetaBuffers[axis]?.destroy();
      this.gridParamBuffers[axis]?.destroy();
      this.statsBuffers[axis]?.destroy();
    }
    this.toolParamsBuffer?.destroy();
    this.affectedColsBuffer?.destroy();
    this.vertexBuffer?.destroy();
    this.indexBuffer?.destroy();
    this.vertexCountBuffer?.destroy();
    this.indexCountBuffer?.destroy();
    this.stagingVertexBuffer?.destroy();
    this.stagingIndexBuffer?.destroy();
    this.stagingStatsBuffer?.destroy();
    this.stagingVertexCountBuffer?.destroy();
  }
}


// =========================================================================
//  WebGPU Device Initialization Helper
// =========================================================================

/**
 * Initialize WebGPU device and adapter.
 * @returns {Promise<{ device: GPUDevice, adapter: GPUAdapter }>}
 */
export async function initWebGPU() {
  if (!navigator.gpu) {
    throw new Error('WebGPU is not supported in this browser. ' +
      'Use Chrome 113+ or Edge 113+ with WebGPU enabled.');
  }

  const adapter = await navigator.gpu.requestAdapter({
    powerPreference: 'high-performance',
  });

  if (!adapter) {
    throw new Error('No WebGPU adapter found.');
  }

  const device = await adapter.requestDevice({
    requiredFeatures: [],
    requiredLimits: {
      maxStorageBufferBindingSize: 512 * 1024 * 1024, // 512 MB
      maxComputeWorkgroupStorageSize: 65536,
      maxComputeInvocationsPerWorkgroup: 256,
      maxComputeWorkgroupSizeX: 256,
    },
  });

  device.lost.then((info) => {
    console.error('WebGPU device lost:', info.message);
  });

  return { device, adapter };
}
