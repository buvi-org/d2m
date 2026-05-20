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
    if (window.__currentToolpath) {
      viewer.setToolpath(els['show-toolpath'].checked ? window.__currentToolpath : null);
    }
  });
  els['show-diff'].addEventListener('change', () => {
    if (window.__currentDiffRegions) {
      viewer[els['show-diff'].checked ? 'addDiffMarkers' : 'clearGougeMarkers'](window.__currentDiffRegions);
    }
  });
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
    window.__currentToolpath = [];
    window.__currentDiffRegions = [];

    if (scene.assets?.stock_mesh) {
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
      window.__currentToolpath = extractToolpathPoints(toolpaths);
      if (els['show-toolpath'].checked) {
        viewer.setToolpath(window.__currentToolpath);
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
    setStatus(
      `Loaded ${scene.title || 'SubCAD visualization session'}; `
      + `${window.__currentToolpath.length} toolpath points; `
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
  const points = [];
  const operations = Array.isArray(payload) ? payload : (payload.operations || []);
  for (const op of operations) {
    const moves = op.moves || op.toolpath?.moves || [];
    for (const move of moves) {
      const pos = move.position || move;
      if (Array.isArray(pos) && pos.length >= 3) {
        points.push([Number(pos[0]), Number(pos[1]), Number(pos[2])]);
      }
    }
  }
  return points;
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
  els.operations.innerHTML = operations.map(op => `
    <div class="op-item complete">
      <div>OP ${escapeHtml(String(op.sequence_number ?? '?'))}: ${escapeHtml(op.operation || '?')}</div>
      <small>${escapeHtml(op.setup || 'unassigned')} ${escapeHtml(op.face_selector || '')}</small>
    </div>
  `).join('');
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
