/**
 * tools.js — JavaScript Tool Library
 *
 * Mirrors src/simulation/tools.py — APT tool definitions with bounding-box
 * computation and GPU buffer serialization.
 *
 * Python reference:
 *   src/simulation/tools.py — ToolParameters, Tool, BallEndmill, FlatEndmill, etc.
 */

// Tool type enum (must match dexel_subtract.wgsl constants)
export const TOOL_TYPE = Object.freeze({
  BALL: 0,
  FLAT: 1,
  BULLNOSE: 2,
  DRILL: 3,
});

/**
 * Tool parameters matching the WGSL ToolParams struct.
 * Python: tools.py ToolParameters dataclass (line 315)
 */
export class ToolParams {
  /**
   * @param {Object} opts
   * @param {number} opts.diameter - Cutting diameter D (mm)
   * @param {number} [opts.cornerRadius=0] - Corner radius R (mm), 0 for sharp
   * @param {number} [opts.fluteLength=50] - Flute length FL (mm)
   * @param {number} [opts.length=100] - Total tool length L (mm)
   */
  constructor({ diameter, cornerRadius = 0, fluteLength = 50, length = 100 }) {
    this.diameter = diameter;
    this.radius = diameter / 2;
    this.cornerRadius = cornerRadius;
    this.fluteLength = fluteLength;
    this.length = length;
  }
}

/**
 * Abstract base class for cutting tools.
 * Python: tools.py Tool (line 341)
 */
export class Tool {
  /** @param {ToolParams} params */
  constructor(params) {
    this.params = params;
  }

  get diameter() { return this.params.diameter; }
  get radius() { return this.params.radius; }
  get cornerRadius() { return this.params.cornerRadius; }
  get fluteLength() { return this.params.fluteLength; }
  get length() { return this.params.length; }

  /**
   * Axis-aligned bounding box of the tool in its local frame.
   * Python: tools.py Tool.bbox_at_origin() (line 402)
   * @returns {{ min: [number,number,number], max: [number,number,number] }}
   */
  bboxAtOrigin() {
    const r = this.radius;
    return {
      min: [-r, -r, 0],
      max: [r, r, this.fluteLength],
    };
  }

  /**
   * Serialize tool parameters for GPU upload.
   * Returns a Float32Array matching the WGSL ToolParams struct layout:
   *   tool_type: u32 (as f32 bits)
   *   diameter: f32
   *   corner_radius: f32
   *   flute_length: f32
   *   tool_pos_x/y/z: f32
   *   tool_dir_x/y/z: f32
   *   pad1, pad2: f32 (alignment to 48 bytes = 12 floats)
   *
   * @param {{ position: [number,number,number], axis: [number,number,number] }} pose
   * @returns {Float32Array}
   */
  toGPUBuffer(pose) {
    // Python: material_removal.py _remove_at_pose_on_grid
    const buf = new Float32Array(16);
    buf[0] = this.type;           // tool_type
    buf[1] = this.diameter;       // diameter
    buf[2] = this.cornerRadius;   // corner_radius
    buf[3] = this.fluteLength;    // flute_length
    buf[4] = pose.position[0];    // tool_pos_x
    buf[5] = pose.position[1];    // tool_pos_y
    buf[6] = pose.position[2];    // tool_pos_z
    buf[7] = pose.axis[0];        // tool_dir_x
    buf[8] = pose.axis[1];        // tool_dir_y
    buf[9] = pose.axis[2];        // tool_dir_z
    buf[10] = 0; buf[11] = 0;     // padding
    buf[12] = 0; buf[13] = 0; buf[14] = 0; buf[15] = 0;
    return buf;
  }

  /**
   * Compute the world-space AABB of the tool at a given pose.
   * Python: material_removal.py _tool_bbox_in_world() (line 279)
   *
   * @param {{ position: [number,number,number], axis: [number,number,number] }} pose
   * @returns {{ min: [number,number,number], max: [number,number,number] }}
   */
  worldBBox(pose) {
    const local = this.bboxAtOrigin();
    const R = this._rotationMatrixFromAxis(pose.axis);
    const pos = pose.position;
    const corners = [];
    for (const x of [local.min[0], local.max[0]]) {
      for (const y of [local.min[1], local.max[1]]) {
        for (const z of [local.min[2], local.max[2]]) {
          // Rotate corner
          const rx = R[0]*x + R[1]*y + R[2]*z;
          const ry = R[3]*x + R[4]*y + R[5]*z;
          const rz = R[6]*x + R[7]*y + R[8]*z;
          corners.push([rx + pos[0], ry + pos[1], rz + pos[2]]);
        }
      }
    }
    const min = [Infinity, Infinity, Infinity];
    const max = [-Infinity, -Infinity, -Infinity];
    for (const c of corners) {
      for (let k = 0; k < 3; k++) {
        min[k] = Math.min(min[k], c[k]);
        max[k] = Math.max(max[k], c[k]);
      }
    }
    return { min, max };
  }

  /**
   * Build a 3x3 rotation matrix from tool axis direction.
   * Takes +Z to the given axis direction.
   * Python: dexel_subtract.wgsl build_tool_to_world()
   *
   * @param {[number,number,number]} axis - Unit vector for tool axis in world frame
   * @returns {number[]} 9-element array [m00, m01, m02, m10, m11, m12, m20, m21, m22]
   */
  _rotationMatrixFromAxis(axis) {
    const zAxis = [0, 0, 1];
    const cross = [
      zAxis[1] * axis[2] - zAxis[2] * axis[1],
      zAxis[2] * axis[0] - zAxis[0] * axis[2],
      zAxis[0] * axis[1] - zAxis[1] * axis[0],
    ];
    const sinA = Math.sqrt(cross[0]*cross[0] + cross[1]*cross[1] + cross[2]*cross[2]);
    const cosA = zAxis[0]*axis[0] + zAxis[1]*axis[1] + zAxis[2]*axis[2];

    if (sinA < 1e-9) {
      if (cosA > 0) return [1,0,0, 0,1,0, 0,0,1];
      return [1,0,0, 0,-1,0, 0,0,-1];
    }

    const a = [cross[0]/sinA, cross[1]/sinA, cross[2]/sinA];
    const angle = Math.atan2(sinA, cosA);
    const c = Math.cos(angle);
    const s = Math.sin(angle);
    const t = 1 - c;
    const x = a[0], y = a[1], z = a[2];
    return [
      t*x*x + c,     t*x*y - s*z,   t*x*z + s*y,
      t*x*y + s*z,   t*y*y + c,     t*y*z - s*x,
      t*x*z - s*y,   t*y*z + s*x,   t*z*z + c,
    ];
  }
}


/**
 * Ball Endmill: cylinder + hemisphere at tip.
 * Python: tools.py BallEndmill (line 499)
 */
export class BallEndmill extends Tool {
  get type() { return TOOL_TYPE.BALL; }

  /**
   * @param {number} diameter - mm
   * @param {number} [fluteLength=50] - mm
   * @param {number} [length=100] - mm
   */
  constructor(diameter, fluteLength = 50, length = 100) {
    super(new ToolParams({
      diameter,
      cornerRadius: diameter / 2,
      fluteLength,
      length,
    }));
  }

  bboxAtOrigin() {
    const r = this.radius;
    return { min: [-r, -r, -r], max: [r, r, this.fluteLength] };
  }
}


/**
 * Flat Endmill: cylinder + flat bottom disc.
 * Python: tools.py FlatEndmill (line 440)
 */
export class FlatEndmill extends Tool {
  get type() { return TOOL_TYPE.FLAT; }

  /**
   * @param {number} diameter - mm
   * @param {number} [fluteLength=30] - mm
   * @param {number} [length=80] - mm
   */
  constructor(diameter, fluteLength = 30, length = 80) {
    super(new ToolParams({ diameter, cornerRadius: 0, fluteLength, length }));
  }
}


/**
 * Bull Nose Endmill: cylinder + toroidal corner + flat bottom.
 * Python: tools.py BullNoseEndmill (line 575)
 */
export class BullNoseEndmill extends Tool {
  get type() { return TOOL_TYPE.BULLNOSE; }

  /**
   * @param {number} diameter - mm
   * @param {number} cornerRadius - mm (R_corner < D/2)
   * @param {number} [fluteLength=40] - mm
   * @param {number} [length=90] - mm
   */
  constructor(diameter, cornerRadius, fluteLength = 40, length = 90) {
    super(new ToolParams({ diameter, cornerRadius, fluteLength, length }));
  }
}


/**
 * Drill: cone tip + cylinder body.
 * Python: tools.py Drill (line 647)
 */
export class Drill extends Tool {
  get type() { return TOOL_TYPE.DRILL; }

  /**
   * @param {number} diameter - mm
   * @param {number} [tipAngle=118] - degrees (typical drill point angle)
   * @param {number} [fluteLength=50] - mm
   * @param {number} [length=100] - mm
   */
  constructor(diameter, tipAngle = 118, fluteLength = 50, length = 100) {
    super(new ToolParams({ diameter, cornerRadius: 0, fluteLength, length }));
    this.tipAngleDeg = tipAngle;
    this.tipAngleRad = tipAngle * Math.PI / 180;
  }

  /** Height of conical tip from apex to full diameter (mm). */
  get coneHeight() {
    return this.radius / Math.tan(this.tipAngleRad / 2);
  }
}


/**
 * Tool factory — creates the correct subclass from a type name.
 * Python: tools.py create_tool() (line 887)
 *
 * @param {string} toolType - 'ball_endmill' | 'flat_endmill' | 'bull_nose' | 'drill'
 * @param {Object} kwargs
 * @returns {Tool}
 */
export function createTool(toolType, kwargs = {}) {
  switch (toolType) {
    case 'ball_endmill':
      return new BallEndmill(kwargs.diameter, kwargs.fluteLength, kwargs.length);
    case 'flat_endmill':
      return new FlatEndmill(kwargs.diameter, kwargs.fluteLength, kwargs.length);
    case 'bull_nose':
      return new BullNoseEndmill(kwargs.diameter, kwargs.cornerRadius, kwargs.fluteLength, kwargs.length);
    case 'drill':
      return new Drill(kwargs.diameter, kwargs.tipAngle, kwargs.fluteLength, kwargs.length);
    default:
      throw new Error(`Unknown tool type: ${toolType}. Available: ball_endmill, flat_endmill, bull_nose, drill`);
  }
}
