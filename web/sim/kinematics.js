/**
 * kinematics.js — JavaScript port of FiveAxisKinematics.forward()
 *
 * Table-Table (BC trunnion) forward kinematics for 5-axis CNC.
 * Joint vector: [X, Y, Z, A_unused, B, C] in mm and degrees.
 * Returns tool pose in workpiece frame.
 *
 * Python reference:
 *   src/simulation/kinematics.py — FiveAxisKinematics._forward_table_table
 */

// ---------------------------------------------------------------------------
// Quaternion helpers (scalar-first: [w, x, y, z])
// ---------------------------------------------------------------------------

function quatMultiply(q1, q2) {
  const [w1, x1, y1, z1] = q1;
  const [w2, x2, y2, z2] = q2;
  return [
    w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
    w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
    w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
    w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2,
  ];
}

function quatFromRotY(angle) {
  const half = angle / 2;
  return [Math.cos(half), 0, Math.sin(half), 0];
}

function quatFromRotZ(angle) {
  const half = angle / 2;
  return [Math.cos(half), 0, 0, Math.sin(half)];
}

// ---------------------------------------------------------------------------
// 3x3 rotation matrices
// ---------------------------------------------------------------------------

function rotationMatrixY(angle) {
  const c = Math.cos(angle);
  const s = Math.sin(angle);
  return [
    [c, 0, s],
    [0, 1, 0],
    [-s, 0, c],
  ];
}

function rotationMatrixZ(angle) {
  const c = Math.cos(angle);
  const s = Math.sin(angle);
  return [
    [c, -s, 0],
    [s, c, 0],
    [0, 0, 1],
  ];
}

// Multiply two 3x3 matrices: A * B
function mat3Mul(A, B) {
  const result = [[0, 0, 0], [0, 0, 0], [0, 0, 0]];
  for (let i = 0; i < 3; i++) {
    for (let j = 0; j < 3; j++) {
      for (let k = 0; k < 3; k++) {
        result[i][j] += A[i][k] * B[k][j];
      }
    }
  }
  return result;
}

// Transpose 3x3 matrix
function mat3Transpose(M) {
  return [
    [M[0][0], M[1][0], M[2][0]],
    [M[0][1], M[1][1], M[2][1]],
    [M[0][2], M[1][2], M[2][2]],
  ];
}

// Multiply 3x3 matrix by 3-vector: M * v
function mat3VecMul(M, v) {
  return [
    M[0][0] * v[0] + M[0][1] * v[1] + M[0][2] * v[2],
    M[1][0] * v[0] + M[1][1] * v[1] + M[1][2] * v[2],
    M[2][0] * v[0] + M[2][1] * v[1] + M[2][2] * v[2],
  ];
}

// ---------------------------------------------------------------------------
// Forward kinematics
// ---------------------------------------------------------------------------

const DEFAULT_TABLE_PIVOT = [0, 0, 0];

/**
 * Forward kinematics for TABLE_TABLE (BC trunnion) configuration.
 *
 * Chain: world -> linear axes -> tool (fixed orientation)
 *        world -> B-axis -> C-axis -> part
 *
 * Python: kinematics.py _forward_table_table (line 274)
 *
 * @param {number[]} joints - [X, Y, Z, A_unused, B_deg, C_deg] in mm and deg
 * @param {Object} [options]
 * @param {number[]} [options.tablePivotOffset=[0,0,0]] - table pivot offset (mm)
 * @returns {{ position: number[], orientation: number[], axis: number[] }}
 */
export function forward(joints, options = {}) {
  const tablePivot = options.tablePivotOffset || DEFAULT_TABLE_PIVOT;

  const X = joints[0];
  const Y = joints[1];
  const Z = joints[2];
  const B_deg = joints[4];
  const C_deg = joints[5];
  const B_rad = B_deg * Math.PI / 180;
  const C_rad = C_deg * Math.PI / 180;

  // Part rotation: R_y(B) * R_z(C)
  const RyB = rotationMatrixY(B_rad);
  const RzC = rotationMatrixZ(C_rad);
  const R_part = mat3Mul(RyB, RzC);
  const R_part_T = mat3Transpose(R_part);

  // Tool axis in workpiece frame: [sin(B), 0, cos(B)]
  // (derived from R_part^T * [0,0,1])
  const toolAxis = [Math.sin(B_rad), 0, Math.cos(B_rad)];

  // Tool tip position in workpiece frame:
  //   P_wp = R_part^T * (P_machine - table_pivot) + table_pivot
  const P_machine = [X, Y, Z];
  const diff = [
    P_machine[0] - tablePivot[0],
    P_machine[1] - tablePivot[1],
    P_machine[2] - tablePivot[2],
  ];
  const rotated = mat3VecMul(R_part_T, diff);
  const position = [
    rotated[0] + tablePivot[0],
    rotated[1] + tablePivot[1],
    rotated[2] + tablePivot[2],
  ];

  // Tool orientation: rotation about Y by -B (takes +Z to toolAxis)
  const q_tool = quatFromRotY(-B_rad);

  return {
    position,
    orientation: q_tool, // [w, x, y, z], scalar-first
    axis: toolAxis, // unit vector, tool axis direction in workpiece frame
  };
}

/**
 * Build a joints vector from G-code coordinates and previous joint state.
 * Tracks modal position for axes not specified in the current command.
 *
 * @param {Object} coords - { X, Y, Z, A, B, C } from GCodeCommand
 * @param {number[]} prevJoints - previous [X, Y, Z, A, B, C]
 * @returns {number[]} new joints vector
 */
export function coordsToJoints(coords, prevJoints) {
  const j = prevJoints ? [...prevJoints] : [0, 0, 0, 0, 0, 0];
  if (coords.X !== undefined) j[0] = coords.X;
  if (coords.Y !== undefined) j[1] = coords.Y;
  if (coords.Z !== undefined) j[2] = coords.Z;
  if (coords.A !== undefined) j[3] = coords.A;
  if (coords.B !== undefined) j[4] = coords.B;
  if (coords.C !== undefined) j[5] = coords.C;
  return j;
}
