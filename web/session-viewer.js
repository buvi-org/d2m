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
    'show-diff',
    'fit-view',
    'timeline-prev',
    'timeline-next',
    'timeline-range',
    'timeline-label',
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
    window.__sceneBaseUrl = baseUrl;
    window.__stockStates = scene.assets?.stock_states || [];
    window.__currentStateIndex = Math.max(0, window.__stockStates.length - 1);
    window.__currentToolpath = [];
    window.__currentToolpathMoves = [];
    window.__currentDiffRegions = [];
    window.__selectedToolpathOperation = 'all';

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
        const point = [Number(pos[0]), Number(pos[1]), Number(pos[2])];
        points.push(point);
        extractedMoves.push({
          position: point,
          move_type: move.move_type || move.type || move.kind || 'feed',
        });
      }
    }
    if (extractedMoves.length) {
      extractedOperations.push({
        operation: op.operation,
        sequence_number: op.sequence_number,
        moves: extractedMoves,
      });
    }
  }
  return { operations: extractedOperations, points };
}

function renderMetadata(scene, comparison) {
  const rows = [
    ['Schema', scene.schema_version || 'unknown'],
    ['Material', scene.material || 'unspecified'],
    ['Stock', JSON.stringify(scene.stock_dimensions || {})],
    ['Operations', String((scene.operations || []).length)],
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
      <small>Combined toolpath</small>
    </button>
  ` + operations.map(op => `
    <button class="op-item complete" type="button" data-sequence="${escapeHtml(String(op.sequence_number ?? ''))}">
      <div>OP ${escapeHtml(String(op.sequence_number ?? '?'))}: ${escapeHtml(op.operation || '?')}</div>
      <small>${escapeHtml(op.setup || 'unassigned')} ${escapeHtml(op.face_selector || '')}</small>
    </button>
  `).join('');
  updateOperationSelection();
}

function renderSelectedToolpath() {
  if (!els['show-toolpath'].checked) {
    viewer.setToolpath(null);
    return;
  }

  const operations = window.__currentToolpathMoves || [];
  const selected = window.__selectedToolpathOperation || 'all';
  if (selected === '0') {
    viewer.setToolpath(null);
    return;
  }
  if (selected === 'all') {
    viewer.setToolpathMoves(operations);
    return;
  }

  const selectedOperation = operations.filter(op => String(op.sequence_number) === selected);
  viewer.setToolpathMoves(selectedOperation);
}

function updateOperationSelection() {
  const selected = window.__selectedToolpathOperation || 'all';
  for (const item of els.operations.querySelectorAll('.op-item')) {
    item.classList.toggle('selected', item.dataset.sequence === selected);
  }
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
