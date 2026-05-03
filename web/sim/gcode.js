/**
 * gcode.js — Minimal G-Code Parser
 *
 * Parses G-code blocks with modal state tracking into a sequence of
 * { motion, joints } objects suitable for the simulation engine.
 *
 * Python reference:
 *   src/simulation/simulator.py — GCodeParser, GCodeBlock
 */

/**
 * Modal state tracking during G-code parsing.
 */
class ModalState {
  constructor() {
    this.motion = 'G00';   // G00 (rapid) or G01 (linear feed)
    this.feed = null;      // mm/min
    this.units = 'mm';     // G21 (mm) or G20 (inch)
    this.absoluteCoords = true; // G90 (absolute) or G91 (incremental)
    this.plane = 'XY';     // G17 (XY), G18 (XZ), G19 (YZ)
    this.spindleRPM = 0;
    this.spindleOn = false; // M03/M04
    this.coolant = false;   // M08/M09
    this.lineNumber = 0;
  }

  clone() {
    const s = new ModalState();
    Object.assign(s, this);
    return s;
  }
}

/**
 * A single parsed G-code command.
 */
class GCodeCommand {
  /**
   * @param {Object} opts
   * @param {string} opts.motion - 'G00' or 'G01'
   * @param {number} opts.lineNumber
   * @param {Object} opts.coords - { X, Y, Z, A, B, C } in mm/degrees
   * @param {number|null} opts.feed - mm/min or null
   */
  constructor({ motion, lineNumber, coords, feed }) {
    this.motion = motion;
    this.lineNumber = lineNumber;
    this.coords = coords;
    this.feed = feed;
  }
}


/**
 * G-code parser with modal state.
 * Python: simulator.py GCodeParser
 */
export class GCodeParser {
  constructor() {
    this.state = new ModalState();
    /** @type {GCodeCommand[]} */
    this.commands = [];
  }

  /**
   * Parse a G-code program string.
   * @param {string} program - Raw G-code text
   * @returns {GCodeCommand[]}
   */
  parse(program) {
    this.state = new ModalState();
    this.commands = [];

    const lines = program.split('\n');
    for (const rawLine of lines) {
      const line = this._cleanLine(rawLine);
      if (!line) continue;

      this.state.lineNumber++;

      // Parse word-address tokens
      const tokens = this._tokenize(line);
      if (tokens.length === 0) continue;

      this._processTokens(tokens);
    }

    return this.commands;
  }

  /**
   * Strip comments and whitespace.
   */
  _cleanLine(line) {
    // Remove block delete
    let s = line.replace(/^\//, '');
    // Remove comments (parenthesized or semicolon)
    s = s.replace(/\([^)]*\)/g, '');
    const semi = s.indexOf(';');
    if (semi >= 0) s = s.substring(0, semi);
    return s.trim();
  }

  /**
   * Tokenize a G-code line into word-address pairs.
   * e.g. "G01 X10.0 Y-5.0 F500" -> [['G', 1], ['X', 10.0], ['Y', -5.0], ['F', 500]]
   */
  _tokenize(line) {
    const tokens = [];
    const regex = /([A-Za-z])\s*([+-]?\d*\.?\d*)/g;
    let match;
    while ((match = regex.exec(line)) !== null) {
      const letter = match[1].toUpperCase();
      const value = parseFloat(match[2]) || 0;
      tokens.push([letter, value]);
    }
    return tokens;
  }

  /**
   * Process tokens for a single line, updating modal state and emitting commands.
   */
  _processTokens(tokens) {
    // Collect coordinate words
    /** @type {Object<string,number>} */
    const coords = {};
    let motionCode = null;
    let newFeed = null;

    for (const [letter, value] of tokens) {
      switch (letter) {
        case 'G':
          this._handleGCode(value);
          if (value === 0 || value === 1) motionCode = `G${String(value).padStart(2, '0')}`;
          break;
        case 'M':
          this._handleMCode(value);
          break;
        case 'X': coords.X = value; break;
        case 'Y': coords.Y = value; break;
        case 'Z': coords.Z = value; break;
        case 'A': coords.A = value; break;
        case 'B': coords.B = value; break;
        case 'C': coords.C = value; break;
        case 'F': newFeed = value; break;
        case 'S': this.state.spindleRPM = value; break;
        case 'N': /* line number, skip */ break;
        default: break;
      }
    }

    // Update feed if specified
    if (newFeed !== null) {
      this.state.feed = newFeed;
    }

    // Apply incremental offsets if in G91 mode
    if (!this.state.absoluteCoords) {
      // In practice, for simulation we treat all coordinates as absolute
      // (G91 incremental is rare in machining code and handled differently)
    }

    // Emit a motion command if coordinates are given
    // (A line with only G-code and no coordinates is a modal change, e.g., just "G01")
    const motion = motionCode || this.state.motion;
    const hasCoords = Object.keys(coords).length > 0;

    if (hasCoords) {
      this.commands.push(new GCodeCommand({
        motion,
        lineNumber: this.state.lineNumber,
        coords: { ...coords },
        feed: this.state.feed,
      }));
    }
  }

  /**
   * Handle G-code (modal group updates).
   */
  _handleGCode(value) {
    switch (value) {
      case 0: this.state.motion = 'G00'; break;
      case 1: this.state.motion = 'G01'; break;
      case 2: this.state.motion = 'G02'; break; // CW arc (not supported in MVP)
      case 3: this.state.motion = 'G03'; break; // CCW arc (not supported in MVP)
      case 17: this.state.plane = 'XY'; break;
      case 18: this.state.plane = 'XZ'; break;
      case 19: this.state.plane = 'YZ'; break;
      case 20: this.state.units = 'inch'; break;
      case 21: this.state.units = 'mm'; break;
      case 90: this.state.absoluteCoords = true; break;
      case 91: this.state.absoluteCoords = false; break;
      case 94: break; // feed per minute (default)
      case 95: break; // feed per revolution
      default: break;
    }
  }

  /**
   * Handle M-code.
   */
  _handleMCode(value) {
    switch (value) {
      case 2: case 30: break; // program end
      case 3: this.state.spindleOn = true; break;  // spindle CW
      case 4: this.state.spindleOn = true; break;  // spindle CCW
      case 5: this.state.spindleOn = false; break;
      case 8: this.state.coolant = true; break;
      case 9: this.state.coolant = false; break;
      default: break;
    }
  }

  /**
   * Reset parser state.
   */
  reset() {
    this.state = new ModalState();
    this.commands = [];
  }
}


/**
 * Convert GCodeCommand sequence to tool pose sequence.
 *
 * Each command's coordinates (X, Y, Z, A, B, C) are converted to tool poses
 * with position and axis direction in the workpiece frame.
 *
 * @param {GCodeCommand[]} commands
 * @param {{ getToolPose: (coords: Object) => {position: [number,number,number], axis: [number,number,number]} }} kinematics
 * @returns {{ motion: string, pose: {position: [number,number,number], axis: [number,number,number]}, feed: number|null, lineNumber: number }[]}
 */
export function commandsToPoses(commands, kinematics) {
  const result = [];
  for (const cmd of commands) {
    const pose = kinematics.getToolPose(cmd.coords);
    result.push({
      motion: cmd.motion,
      pose,
      feed: cmd.feed,
      lineNumber: cmd.lineNumber,
    });
  }
  return result;
}
