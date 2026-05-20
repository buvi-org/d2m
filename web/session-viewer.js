import { Viewer } from './viewer.js';

const viewer = new Viewer();
const els = {};

document.addEventListener('DOMContentLoaded', () => {
  for (const id of [
    'viewport',
    'session-path',
    'load-session',
    'status',
    'metadata',
    'operations',
    'show-target',
    'show-toolpath',
    'show-tool',
    'show-diff',
    'fit-view',
    'timeline-prev',
    'timeline-next',
    'timeline-range',
    'timeline-label',
    'playback-play',
    'playback-reset',
    'playback-speed',
    'playback-range',
    'playback-label',
  ]) {
    els[id] = document.getElementById(id);
  }

  viewer.init(els.viewport);
  viewer.loadDefaultCube();

  const params = new URLSearchParams(window.location.search);
  const session = params.get('session') || 'sessions/latest/scene.json';
  els['session-path'].value = session;

  els['load-session'].addEventListener('click', () => loadSession(els['session-path'].value));
  els['show-target'].addEventListener('change', () => viewer.setTargetVisible(els['show-target'].checked));
  els['show-tool'].addEventListener('change', () => {
    viewer.setToolVisible(els['show-tool'].checked);
    updatePlaybackAt(window.__playback?.elapsedSec || 0);
  });
  els['show-toolpath'].addEventListener('change', () => {
    if (!els['show-toolpath'].checked) {
      viewer.setToolpath(null);
    } else if (window.__currentToolpathMoves) {
      renderSelectedToolpath();
    } else if (window.__currentToolpath) {
      viewer.setToolpath(window.__currentToolpath);
    }
  });
  els['show-diff'].addEventListener('change', () => {
    if (window.__currentDiffRegions) {
      viewer[els['show-diff'].checked ? 'addDiffMarkers' : 'clearGougeMarkers'](window.__currentDiffRegions);
    }
  });
  els.operations.addEventListener('click', async event => {
    const item = event.target.closest('.op-item');
    if (!item) return;
    window.__selectedToolpathOperation = item.dataset.sequence || 'all';
    await selectTimelineForOperation(window.__selectedToolpathOperation);
    renderSelectedToolpath();
    updateOperationSelection();
  });
  els['timeline-prev'].addEventListener('click', () => selectTimelineState(Number(els['timeline-range'].value) - 1));
  els['timeline-next'].addEventListener('click', () => selectTimelineState(Number(els['timeline-range'].value) + 1));
  els['timeline-range'].addEventListener('input', event => selectTimelineState(Number(event.target.value)));
  els['playback-play'].addEventListener('click', () => togglePlayback());
  els['playback-reset'].addEventListener('click', () => resetPlayback());
  els['playback-speed'].addEventListener('change', () => updatePlaybackLabel());
  els['playback-range'].addEventListener('input', event => scrubPlayback(Number(event.target.value)));
  els['fit-view'].addEventListener('click', () => viewer.fitView());

  loadSession(session);
});

async function loadSession(scenePath) {
  setStatus('Loading session...');
  try {
    const sceneUrl = new URL(scenePath, window.location.href);
    const baseUrl = new URL('.', sceneUrl);
    const scene = await fetchJson(sceneUrl.href);

    viewer.clearScene();
    stopPlayback();
    window.__currentScene = scene;
    window.__sceneBaseUrl = baseUrl;
    window.__machiningZOffset = Number(scene.stock_dimensions?.height || 0) / 2;
    window.__stockStates = scene.assets?.stock_states || [];
    window.__currentStateIndex = Math.max(0, window.__stockStates.length - 1);
    window.__currentToolpath = [];
    window.__currentToolpathMoves = [];
    window.__currentDiffRegions = [];
    window.__selectedToolpathOperation = 'all';
    window.__playback = emptyPlayback();

    if (window.__stockStates.length) {
      await loadTimelineState(window.__currentStateIndex);
    } else if (scene.assets?.stock_mesh) {
      await viewer.loadStockSTL(await fetchArrayBuffer(assetUrl(scene.assets.stock_mesh, baseUrl)));
    } else {
      viewer.loadDefaultCube();
    }

    if (scene.assets?.target_mesh) {
      await viewer.loadTargetSTL(await fetchArrayBuffer(assetUrl(scene.assets.target_mesh, baseUrl)));
      viewer.setTargetVisible(els['show-target'].checked);
    }

    const toolpathAsset = scene.assets?.toolpaths || scene.assets?.toolpath;
    if (toolpathAsset) {
      const toolpaths = await fetchJson(assetUrl(toolpathAsset, baseUrl));
      const extracted = extractToolpathMoves(toolpaths);
      window.__currentToolpath = extracted.points;
      window.__currentToolpathMoves = extracted.operations;
      if (els['show-toolpath'].checked) {
        renderSelectedToolpath();
      }
    }

    if (scene.assets?.comparison) {
      const comparison = await fetchJson(assetUrl(scene.assets.comparison, baseUrl));
      window.__currentDiffRegions = [
        ...(comparison.overcut_regions || []),
        ...(comparison.undercut_regions || []),
      ];
      if (els['show-diff'].checked) {
        viewer.addDiffMarkers(window.__currentDiffRegions);
      }
      renderMetadata(scene, comparison);
    } else {
      renderMetadata(scene, null);
    }

    renderOperations(scene.operations || []);
    preparePlayback(getSelectedOperations(), { reset: true });
    updateTimelineControls();
    setStatus(
      `Loaded ${scene.title || 'SubCAD visualization session'}; `
      + `${window.__currentToolpath.length} toolpath points; `
      + `${window.__stockStates.length} stock states; `
      + `${window.__currentDiffRegions.length} diff regions`
    );
  } catch (err) {
    console.error(err);
    setStatus(`Failed to load session: ${err.message}`, true);
  }
}

function assetUrl(asset, baseUrl) {
  const path = typeof asset === 'string' ? asset : asset.path;
  return new URL(path, baseUrl).href;
}

function extractToolpathPoints(payload) {
  return extractToolpathMoves(payload).points;
}

function extractToolpathMoves(payload) {
  const extractedOperations = [];
  const points = [];
  const operations = Array.isArray(payload) ? payload : (payload.operations || []);
  for (const op of operations) {
    const moves = op.moves || op.toolpath?.moves || [];
    const extractedMoves = [];
    for (const move of moves) {
      const pos = move.position || move;
      if (Array.isArray(pos) && pos.length >= 3) {
        const point = transformToolpathPoint(pos);
        points.push(point);
        extractedMoves.push({
          position: point,
          move_type: move.move_type || move.type || move.kind || 'feed',
          feed_mm_min: move.feed_mm_min,
          spindle_rpm: move.spindle_rpm,
          coolant: move.coolant,
          dwell_seconds: move.dwell_seconds,
        });
      }
    }
    if (extractedMoves.length) {
      extractedOperations.push({
        operation: op.operation,
        sequence_number: op.sequence_number,
        tool: op.tool,
        tool_type: op.tool_type,
        tool_diameter_mm: op.tool_diameter_mm,
        summary: op.summary,
        moves: extractedMoves,
      });
    }
  }
  return { operations: extractedOperations, points };
}

function transformToolpathPoint(position) {
  return [
    Number(position[0]),
    Number(position[1]),
    Number(position[2]) + (window.__machiningZOffset || 0),
  ];
}

function renderMetadata(scene, comparison) {
  const totalMinutes = totalOperationMinutes(scene.operations || []);
  const rows = [
    ['Schema', scene.schema_version || 'unknown'],
    ['Material', scene.material || 'unspecified'],
    ['Stock', JSON.stringify(scene.stock_dimensions || {})],
    ['Operations', String((scene.operations || []).length)],
    ['Cycle time', formatMinutes(totalMinutes)],
  ];
  if (comparison) {
    rows.push(['Compare', comparison.status || 'unknown']);
    rows.push(['Score', String(comparison.score ?? 'n/a')]);
    rows.push(['RMS error', `${comparison.rms_error_mm ?? 'n/a'} mm`]);
    rows.push(['Max overcut', `${comparison.max_overcut_mm ?? 'n/a'} mm`]);
    rows.push(['Max undercut', `${comparison.max_undercut_mm ?? 'n/a'} mm`]);
  }
  els.metadata.innerHTML = rows.map(([k, v]) => `
    <div class="meta-row"><span>${escapeHtml(k)}</span><strong>${escapeHtml(v)}</strong></div>
  `).join('');
}

function renderOperations(operations) {
  if (!operations.length) {
    els.operations.innerHTML = '<div class="op-item pending">No operations in session.</div>';
    return;
  }
  els.operations.innerHTML = `
    <button class="op-item complete selected" type="button" data-sequence="all">
      <div>All operations</div>
      <small>Combined toolpath · ${escapeHtml(formatMinutes(totalOperationMinutes(operations)))}</small>
    </button>
  ` + operations.map(op => `
    <button class="op-item complete" type="button" data-sequence="${escapeHtml(String(op.sequence_number ?? ''))}">
      <div>OP ${escapeHtml(String(op.sequence_number ?? '?'))}: ${escapeHtml(op.operation || '?')}</div>
      <small>${escapeHtml(formatMinutes(operationMinutes(op)))} · ${escapeHtml(op.setup || 'unassigned')} ${escapeHtml(op.face_selector || '')}</small>
    </button>
  `).join('');
  updateOperationSelection();
}

function renderSelectedToolpath() {
  if (!els['show-toolpath'].checked) {
    viewer.setToolpath(null);
  } else {
    const selectedOperations = getSelectedOperations();
    viewer.setToolpathMoves(selectedOperations);
  }

  preparePlayback(getSelectedOperations(), { reset: true });
}

function getSelectedOperations() {
  const operations = window.__currentToolpathMoves || [];
  const selected = window.__selectedToolpathOperation || 'all';
  if (selected === '0') {
    return [];
  }
  if (selected === 'all') {
    return operations;
  }

  return operations.filter(op => String(op.sequence_number) === selected);
}

function updateOperationSelection() {
  const selected = window.__selectedToolpathOperation || 'all';
  for (const item of els.operations.querySelectorAll('.op-item')) {
    item.classList.toggle('selected', item.dataset.sequence === selected);
  }
}

function emptyPlayback() {
  return {
    segments: [],
    totalTimeSec: 0,
    elapsedSec: 0,
    isPlaying: false,
    lastTimestamp: null,
    rafId: null,
  };
}

function preparePlayback(operations, options = {}) {
  stopPlayback();
  const playback = buildPlayback(operations || []);
  if (options.reset !== false) {
    playback.elapsedSec = 0;
  } else if (window.__playback) {
    playback.elapsedSec = Math.min(window.__playback.elapsedSec || 0, playback.totalTimeSec);
  }
  window.__playback = playback;
  updatePlaybackAt(playback.elapsedSec);
  updatePlaybackLabel();
}

function buildPlayback(operations) {
  const playback = emptyPlayback();

  for (const operation of operations) {
    const moves = operation.moves || [];
    const rawSegments = [];
    for (let i = 1; i < moves.length; i += 1) {
      const start = moves[i - 1].position;
      const end = moves[i].position;
      if (!start || !end) continue;

      const length = distance3(start, end);
      const moveType = moveTypeOf(moves[i]);
      const feed = Number(moves[i].feed_mm_min || 0);
      let durationSec = 0.25;
      if (moveType === 'dwell') {
        durationSec = Number(moves[i].dwell_seconds || 0.5);
      } else if (moveType === 'rapid') {
        durationSec = Math.max(length / 5000 * 60, 0.08);
      } else if (feed > 0) {
        durationSec = Math.max(length / feed * 60, 0.12);
      } else {
        durationSec = Math.max(length / 1000 * 60, 0.12);
      }
      rawSegments.push({
        start,
        end,
        length,
        durationSec,
        moveType,
        operation,
        tool: toolFromOperation(operation),
      });
    }

    const expectedSec = operationMinutes(operation) * 60;
    const rawTotal = rawSegments.reduce((sum, segment) => sum + segment.durationSec, 0);
    const scale = expectedSec > 0 && rawTotal > 0 ? expectedSec / rawTotal : 1;
    for (const segment of rawSegments) {
      segment.startTimeSec = playback.totalTimeSec;
      segment.durationSec *= scale;
      segment.endTimeSec = segment.startTimeSec + segment.durationSec;
      playback.totalTimeSec = segment.endTimeSec;
      playback.segments.push(segment);
    }
  }

  return playback;
}

function togglePlayback() {
  const playback = window.__playback || emptyPlayback();
  if (!playback.segments.length) return;
  if (playback.isPlaying) {
    stopPlayback();
    updatePlaybackLabel();
    return;
  }
  if (playback.elapsedSec >= playback.totalTimeSec) {
    playback.elapsedSec = 0;
    updatePlaybackAt(0);
  }
  playback.isPlaying = true;
  playback.lastTimestamp = null;
  window.__playback = playback;
  els['playback-play'].textContent = 'Pause';
  playback.rafId = requestAnimationFrame(playbackTick);
}

function stopPlayback() {
  const playback = window.__playback;
  if (playback?.rafId) {
    cancelAnimationFrame(playback.rafId);
  }
  if (playback) {
    playback.isPlaying = false;
    playback.lastTimestamp = null;
    playback.rafId = null;
  }
  if (els['playback-play']) {
    els['playback-play'].textContent = 'Play';
  }
}

function resetPlayback() {
  stopPlayback();
  updatePlaybackAt(0);
  updatePlaybackLabel();
}

function scrubPlayback(value) {
  stopPlayback();
  const playback = window.__playback || emptyPlayback();
  const ratio = Math.max(0, Math.min(1, Number(value) / 1000));
  updatePlaybackAt(playback.totalTimeSec * ratio);
  updatePlaybackLabel();
}

function playbackTick(timestamp) {
  const playback = window.__playback || emptyPlayback();
  if (!playback.isPlaying) return;

  if (playback.lastTimestamp === null) {
    playback.lastTimestamp = timestamp;
  }
  const deltaSec = (timestamp - playback.lastTimestamp) / 1000;
  playback.lastTimestamp = timestamp;
  const speed = Number(els['playback-speed'].value || 1);
  const nextElapsed = Math.min(playback.totalTimeSec, playback.elapsedSec + deltaSec * speed);
  updatePlaybackAt(nextElapsed);
  updatePlaybackLabel();

  if (nextElapsed >= playback.totalTimeSec) {
    stopPlayback();
    return;
  }
  playback.rafId = requestAnimationFrame(playbackTick);
}

function updatePlaybackAt(elapsedSec) {
  const playback = window.__playback || emptyPlayback();
  playback.elapsedSec = Math.max(0, Math.min(playback.totalTimeSec || 0, Number(elapsedSec || 0)));
  window.__playback = playback;

  if (!playback.segments.length) {
    viewer.setToolVisible(false);
    els['playback-range'].value = 0;
    return;
  }

  const segment = segmentAtTime(playback, playback.elapsedSec);
  if (!segment) return;

  const local = segment.durationSec > 0
    ? (playback.elapsedSec - segment.startTimeSec) / segment.durationSec
    : 1;
  const position = lerp3(segment.start, segment.end, Math.max(0, Math.min(1, local)));
  if (els['show-tool'].checked) {
    viewer.updateTool(
      position,
      null,
      segment.tool.toolType,
      segment.tool.diameter,
      segment.tool.fluteLength,
    );
    viewer.setToolVisible(true);
  } else {
    viewer.setToolVisible(false);
  }

  els['playback-range'].value = playback.totalTimeSec > 0
    ? Math.round((playback.elapsedSec / playback.totalTimeSec) * 1000)
    : 0;
}

function updatePlaybackLabel() {
  const playback = window.__playback || emptyPlayback();
  if (!playback.segments.length) {
    els['playback-label'].textContent = 'No toolpath loaded';
    els['playback-play'].disabled = true;
    els['playback-reset'].disabled = true;
    return;
  }

  els['playback-play'].disabled = false;
  els['playback-reset'].disabled = false;
  const segment = segmentAtTime(playback, playback.elapsedSec) || playback.segments[0];
  const opLabel = segment?.operation
    ? `OP ${segment.operation.sequence_number}: ${segment.operation.operation}`
    : 'Toolpath';
  els['playback-label'].textContent = `${opLabel} · ${segment.moveType} · `
    + `${formatTime(playback.elapsedSec)} / ${formatTime(playback.totalTimeSec)} `
    + `(${els['playback-speed'].value}x)`;
}

function segmentAtTime(playback, elapsedSec) {
  if (!playback.segments.length) return null;
  return playback.segments.find(segment => elapsedSec >= segment.startTimeSec && elapsedSec <= segment.endTimeSec)
    || playback.segments[playback.segments.length - 1];
}

function toolFromOperation(operation) {
  const tool = operation.tool || {};
  return {
    toolType: tool.tool_type || operation.tool_type || 'flat_endmill',
    diameter: Number(tool.diameter_mm || operation.tool_diameter_mm || 6),
    fluteLength: Number(tool.flute_length_mm || tool.fluteLength || 30),
  };
}

function operationMinutes(operation) {
  return Number(
    operation?.toolpath_summary?.estimated_time_min
    || operation?.summary?.estimated_time_min
    || operation?.summary?.estimated_time_minutes
    || 0
  );
}

function totalOperationMinutes(operations) {
  return (operations || []).reduce((sum, op) => sum + operationMinutes(op), 0);
}

function formatMinutes(minutes) {
  const value = Number(minutes || 0);
  if (value < 1) {
    return `${(value * 60).toFixed(1)} s`;
  }
  return `${value.toFixed(2)} min`;
}

function formatTime(seconds) {
  const total = Math.max(0, Number(seconds || 0));
  const mins = Math.floor(total / 60);
  const secs = Math.floor(total % 60);
  return `${mins}:${String(secs).padStart(2, '0')}`;
}

function distance3(a, b) {
  return Math.hypot(
    Number(b[0]) - Number(a[0]),
    Number(b[1]) - Number(a[1]),
    Number(b[2]) - Number(a[2]),
  );
}

function lerp3(a, b, t) {
  return [
    Number(a[0]) + (Number(b[0]) - Number(a[0])) * t,
    Number(a[1]) + (Number(b[1]) - Number(a[1])) * t,
    Number(a[2]) + (Number(b[2]) - Number(a[2])) * t,
  ];
}

function moveTypeOf(move) {
  const rawType = String(move?.move_type || move?.type || move?.kind || 'feed').toLowerCase();
  if (rawType.includes('rapid')) return 'rapid';
  if (rawType.includes('plunge')) return 'plunge';
  if (rawType.includes('retract')) return 'retract';
  if (rawType.includes('dwell')) return 'dwell';
  if (rawType.includes('arc')) return 'arc';
  return 'feed';
}

async function selectTimelineForOperation(sequence) {
  const states = window.__stockStates || [];
  if (!states.length) return;

  if (sequence === 'all') {
    await selectTimelineState(states.length - 1, { keepSelection: true });
    return;
  }

  const stateIndex = states.findIndex(state => String(state.sequence_number) === String(sequence));
  if (stateIndex >= 0) {
    await selectTimelineState(stateIndex, { keepSelection: true });
  }
}

async function selectTimelineState(index, options = {}) {
  const states = window.__stockStates || [];
  if (!states.length) return;

  const nextIndex = Math.max(0, Math.min(states.length - 1, Number(index)));
  await loadTimelineState(nextIndex);

  if (!options.keepSelection) {
    const state = states[nextIndex];
    window.__selectedToolpathOperation = String(state.sequence_number || '0');
    renderSelectedToolpath();
    updateOperationSelection();
  }
  updateTimelineControls();
}

async function loadTimelineState(index) {
  const states = window.__stockStates || [];
  const state = states[index];
  if (!state || !window.__sceneBaseUrl) return;

  window.__currentStateIndex = index;
  await viewer.loadStockSTL(await fetchArrayBuffer(assetUrl(state, window.__sceneBaseUrl)));
  updateTimelineControls();
}

function updateTimelineControls() {
  const states = window.__stockStates || [];
  const index = Math.max(0, Math.min(states.length - 1, window.__currentStateIndex || 0));
  const state = states[index];
  const hasTimeline = states.length > 0;

  els['timeline-range'].disabled = !hasTimeline;
  els['timeline-prev'].disabled = !hasTimeline || index <= 0;
  els['timeline-next'].disabled = !hasTimeline || index >= states.length - 1;
  els['timeline-range'].min = 0;
  els['timeline-range'].max = Math.max(0, states.length - 1);
  els['timeline-range'].value = index;

  if (!hasTimeline) {
    els['timeline-label'].textContent = 'No timeline loaded';
    return;
  }

  const prefix = state.sequence_number === 0 ? 'Initial' : `OP ${state.sequence_number}`;
  els['timeline-label'].textContent = `${prefix}: ${state.operation || state.label || 'stock state'}`;
}

async function fetchJson(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`${url} returned ${res.status}`);
  return res.json();
}

async function fetchArrayBuffer(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`${url} returned ${res.status}`);
  return res.arrayBuffer();
}

function setStatus(message, isError = false) {
  els.status.textContent = message;
  els.status.className = isError ? 'status error' : 'status';
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}
