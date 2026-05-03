// ws-client.js — WebSocket client for d2m simulation streaming
//
// Handles connection to the FastAPI WebSocket endpoint, parsing of incoming
// JSON messages, base64 GLB decoding, and reconnection logic.

// ---------------------------------------------------------------------------
// WebSocket client class
// ---------------------------------------------------------------------------

export class SimulationWSClient {
  /**
   * @param {Object} callbacks
   * @param {Function} callbacks.onProgress - ({op_index, total_ops, mesh_glb_base64, volume_removed, gouges_found})
   * @param {Function} callbacks.onComplete - ({total_ops, total_volume_removed, gouges, ...})
   * @param {Function} callbacks.onError - (message)
   * @param {Function} callbacks.onConnected - ()
   * @param {Function} callbacks.onDisconnected - ()
   */
  constructor(callbacks = {}) {
    this._ws = null;
    this._url = '';
    this._callbacks = callbacks;
    this._reconnectAttempts = 0;
    this._maxReconnectAttempts = 3;
    this._reconnectDelay = 2000;
    this._intentionalClose = false;
    this._pendingMessages = [];
  }

  // -----------------------------------------------------------------------
  // Public API
  // -----------------------------------------------------------------------

  /**
   * Connect to the simulation WebSocket.
   * @param {string} partId - The part UUID
   * @param {string} host - Backend host (default: localhost:8000)
   */
  connect(partId, host = 'localhost:8000') {
    this._intentionalClose = false;
    const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
    this._url = `${protocol}://${host}/ws/simulate/${partId}`;

    this._createConnection();
  }

  /**
   * Send the start message to begin simulation.
   * @param {Object} params
   * @param {string} params.gcode - G-code program text
   * @param {string} params.toolType - e.g. 'ball_endmill'
   * @param {number} params.toolDiameter - tool diameter in mm
   * @param {number} params.resolution - simulation resolution in mm
   */
  sendStart(params) {
    this._send({
      type: 'start',
      gcode: params.gcode,
      tool_type: params.toolType || 'ball_endmill',
      tool_diameter: params.toolDiameter || 6.0,
      resolution: params.resolution || 1.0,
    });
  }

  /**
   * Close the WebSocket connection.
   */
  disconnect() {
    this._intentionalClose = true;
    if (this._ws) {
      this._ws.close();
      this._ws = null;
    }
  }

  /** Whether the WebSocket is currently connected and open. */
  get isConnected() {
    return this._ws && this._ws.readyState === WebSocket.OPEN;
  }

  // -----------------------------------------------------------------------
  // Internal
  // -----------------------------------------------------------------------

  _createConnection() {
    if (this._ws) {
      this._ws.close();
      this._ws = null;
    }

    const ws = new WebSocket(this._url);
    this._ws = ws;

    ws.onopen = () => {
      this._reconnectAttempts = 0;
      // Flush any queued messages
      while (this._pendingMessages.length > 0) {
        ws.send(this._pendingMessages.shift());
      }
      if (this._callbacks.onConnected) {
        this._callbacks.onConnected();
      }
    };

    ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data);
        this._handleMessage(msg);
      } catch (e) {
        console.error('Failed to parse WS message:', e);
      }
    };

    ws.onerror = (event) => {
      console.error('WebSocket error:', event);
      if (this._callbacks.onError) {
        this._callbacks.onError('WebSocket connection error');
      }
    };

    ws.onclose = (event) => {
      if (this._callbacks.onDisconnected) {
        this._callbacks.onDisconnected();
      }

      if (!this._intentionalClose && this._reconnectAttempts < this._maxReconnectAttempts) {
        this._reconnectAttempts++;
        console.log(`WebSocket reconnecting (${this._reconnectAttempts}/${this._maxReconnectAttempts})...`);
        setTimeout(() => this._createConnection(), this._reconnectDelay);
      }
    };
  }

  _handleMessage(msg) {
    switch (msg.type) {
      case 'progress':
        if (this._callbacks.onProgress) {
          // Decode base64 GLB to ArrayBuffer if present
          let meshBuffer = null;
          if (msg.mesh_glb_base64) {
            meshBuffer = this._base64ToArrayBuffer(msg.mesh_glb_base64);
          }
          this._callbacks.onProgress({
            opIndex: msg.op_index,
            totalOps: msg.total_ops,
            meshBuffer: meshBuffer,
            meshTooLarge: msg.mesh_too_large || false,
            volumeRemoved: msg.volume_removed,
            volumeThisMove: msg.volume_this_move,
            gougesFound: msg.gouges_found,
            columnsModified: msg.columns_modified,
            endPosition: msg.end_position || null,
          });
        }
        break;

      case 'complete':
        if (this._callbacks.onComplete) {
          this._callbacks.onComplete({
            totalOps: msg.total_ops,
            totalVolumeRemoved: msg.total_volume_removed,
            totalTimeMs: msg.total_time_ms,
            gouges: msg.gouges || [],
            gougeCount: msg.gouge_count || 0,
            stockVolumeMm3: msg.stock_volume_mm3,
            toolpathPositions: msg.toolpath_positions || [],
          });
        }
        break;

      case 'error':
        console.error('Simulation error:', msg.message);
        if (this._callbacks.onError) {
          this._callbacks.onError(msg.message);
        }
        break;

      default:
        console.log('Unknown message type:', msg.type);
    }
  }

  _send(data) {
    if (this._ws && this._ws.readyState === WebSocket.OPEN) {
      this._ws.send(JSON.stringify(data));
    } else if (this._ws && this._ws.readyState === WebSocket.CONNECTING) {
      // Queue the message — it will be sent when onopen fires
      this._pendingMessages.push(JSON.stringify(data));
    } else {
      console.error('WebSocket not connected (state: '
        + (this._ws ? this._ws.readyState : 'null') + ')');
      if (this._callbacks.onError) {
        this._callbacks.onError('WebSocket not connected');
      }
    }
  }

  /**
   * Decode a base64 string to an ArrayBuffer.
   */
  _base64ToArrayBuffer(base64) {
    // Use the data URI approach — avoids atob Unicode issues
    const dataUrl = 'data:application/octet-stream;base64,' + base64;
    const binary = atob(base64);
    const bytes = Uint8Array.from(binary, c => c.charCodeAt(0) & 0xFF);
    return bytes.buffer;
  }
}
