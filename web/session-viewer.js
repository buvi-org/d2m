import { Viewer } from './viewer.js?v=20260617-axis-fix-v10';

const viewer = new Viewer();
window.__viewer = viewer;
const els = {};

document.addEventListener('DOMContentLoaded', () => {
  for (const id of [
    'viewport',
    'session-path',
    'load-session',
    'status',
    'metadata',
    'operations',
    'selected-operation',
    'show-stock',
    'show-target',
    'show-toolpath',
    'show-tool',
    'show-fixture',
    'show-clamps',
    'show-markers',
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
    'export-video',
    'export-video-status',
    'export-progress',
    'export-progress-fill',
  ]) {
    els[id] = document.getElementById(id);
  }

  viewer.init(els.viewport);
  viewer.loadDefaultCube();

  const params = new URLSearchParams(window.location.search);
  const session = params.get('session') || 'sessions/latest/scene.json';
  window.__cacheBust = params.get('v') || String(Date.now());
  els['session-path'].value = session;

  els['load-session'].addEventListener('click', () => loadSession(els['session-path'].value));
  els['show-stock'].addEventListener('change', () => viewer.setStockVisible(els['show-stock'].checked));
  els['show-target'].addEventListener('change', () => viewer.setTargetVisible(els['show-target'].checked));
  els['show-tool'].addEventListener('change', () => {
    viewer.setToolVisible(els['show-tool'].checked);
    updatePlaybackAt(window.__playback?.elapsedSec || 0);
  });
  els['show-fixture'].addEventListener('change', () => viewer.setFixtureVisible(els['show-fixture'].checked));
  els['show-clamps'].addEventListener('change', () => viewer.setClampZoneVisible(els['show-clamps'].checked));
  els['show-markers'].addEventListener('change', () => viewer.setClearanceMarkerVisible(els['show-markers'].checked));
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
  els['export-video'].addEventListener('click', () => exportPlaybackVideo());
  els['fit-view'].addEventListener('click', () => viewer.fitView());

  loadSession(session);
});

async function loadSession(scenePath) {
  setStatus('Loading session...');
  try {
    const sceneUrl = new URL(scenePath, window.location.href);
    const baseUrl = new URL('.', sceneUrl);
    const scene = await fetchJson(cacheBustUrl(sceneUrl.href));

    viewer.clearScene();
    stopPlayback();
    window.__currentScene = scene;
    window.__sceneBaseUrl = baseUrl;
    window.__machiningZOffset = Number(scene.stock_dimensions?.height || 0) / 2;
    window.__simulationTimeline = await loadSimulationTimeline(scene, baseUrl);
    window.__videoManifest = await loadVideoManifest(scene, baseUrl);
    window.__simulationStockKeyframes = window.__simulationTimeline?.stockKeyframes || [];
    const isTurning = isTurningScene(scene, window.__simulationTimeline);
    window.__isTurningScene = isTurning;
    window.__currentMachine = machineForScene(scene, window.__simulationTimeline);
    viewer.setProcessMode(
      isTurning ? 'turning' : 'mill',
      {
        stock_dimensions: scene.stock_dimensions || {},
        machine: window.__currentMachine,
        fixtures: scene.fixtures || window.__simulationTimeline?.fixtures || null,
      },
    );
    window.__currentSimulationKeyframeIndex = -1;
    window.__simulationStockRequestId = 0;
    window.__stockStates = scene.assets?.stock_states || [];
    window.__currentStateIndex = Math.max(0, stockTimelineStates().length - 1);
    window.__currentToolpath = [];
    window.__currentToolpathMoves = [];
    window.__currentDiffRegions = [];
    window.__currentClearanceMarkers = [];
    window.__selectedToolpathOperation = 'all';
    window.__playback = emptyPlayback();

    if (stockTimelineStates().length) {
      await loadTimelineState(window.__currentStateIndex);
    } else if (scene.assets?.stock_mesh) {
      await viewer.loadStockSTL(await fetchArrayBuffer(assetUrl(scene.assets.stock_mesh, baseUrl)));
      viewer.setStockVisible(els['show-stock'].checked);
    } else {
      viewer.loadDefaultCube();
      viewer.setStockVisible(els['show-stock'].checked);
    }

    if (scene.assets?.target_mesh) {
      await viewer.loadTargetSTL(await fetchArrayBuffer(assetUrl(scene.assets.target_mesh, baseUrl)));
      viewer.setTargetVisible(els['show-target'].checked);
    }

    viewer.loadFixtures(scene.fixtures || []);
    viewer.setFixtureVisible(els['show-fixture'].checked);
    viewer.setClampZoneVisible(els['show-clamps'].checked);

    window.__currentClearanceMarkers = await loadSceneMarkers(scene, baseUrl);
    viewer.addClearanceMarkers(window.__currentClearanceMarkers);
    viewer.setClearanceMarkerVisible(els['show-markers'].checked);

    const toolpathAsset = scene.assets?.toolpaths || scene.assets?.toolpath;
    if (isTurning && window.__simulationTimeline?.segments?.length) {
      const extracted = simulationToolpathMoves(window.__simulationTimeline);
      window.__currentToolpath = extracted.points;
      window.__currentToolpathMoves = extracted.operations;
      if (els['show-toolpath'].checked) {
        renderSelectedToolpath();
      }
    } else if (toolpathAsset) {
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
    updateSelectedOperationDetails();
    updateTimelineControls();
    updateExportAvailability();
    const statusParts = [
      `${window.__currentToolpath.length} toolpath points`,
      `${window.__stockStates.length} stock states`,
      `${window.__currentDiffRegions.length} diff regions`,
      `${window.__currentClearanceMarkers.length} clearance markers`,
    ];
    if (window.__simulationTimeline) {
      statusParts.push(`${window.__simulationStockKeyframes.length} sim keyframes`);
    }
    setStatus(
      `Loaded ${scene.title || 'SubCAD visualization session'}; `
      + statusParts.join('; ')
    );
  } catch (err) {
    console.error(err);
    setStatus(`Failed to load session: ${err.message}`, true);
  }
}

function assetUrl(asset, baseUrl) {
  const path = typeof asset === 'string' ? asset : asset.path;
  return cacheBustUrl(new URL(path, baseUrl).href);
}

function cacheBustUrl(url) {
  const next = new URL(url, window.location.href);
  if (window.__cacheBust) {
    next.searchParams.set('v', window.__cacheBust);
  }
  return next.href;
}

async function loadSimulationTimeline(scene, baseUrl) {
  const asset = scene.assets?.simulation_timeline;
  if (!asset) return null;

  try {
    const payload = await fetchJson(assetUrl(asset, baseUrl));
    return normalizeSimulationTimeline(payload);
  } catch (err) {
    console.warn('Could not load simulation_timeline:', err);
    return null;
  }
}

async function loadVideoManifest(scene, baseUrl) {
  const asset = scene.assets?.video_manifest || { path: 'video_manifest.json' };
  if (!asset?.path) return null;

  try {
    return await fetchJson(assetUrl(asset, baseUrl));
  } catch (err) {
    return null;
  }
}

function normalizeSimulationTimeline(payload) {
  const timeline = payload?.timeline || {};
  const segments = normalizeSimulationSegments(timeline.segments || payload?.segments || []);
  const stockKeyframes = normalizeSimulationStockKeyframes(payload?.stock_keyframes || timeline.stock_keyframes || []);
  const declaredTotal = numberOrNull(timeline.total_time_sec ?? timeline.totalTimeSec ?? payload?.total_time_sec);
  const segmentTotal = segments.reduce((max, segment) => Math.max(max, segment.endTimeSec), 0);
  const keyframeTotal = stockKeyframes.reduce((max, keyframe) => Math.max(max, keyframe.time_sec), 0);
  const totalTimeSec = declaredTotal && declaredTotal > 0
    ? declaredTotal
    : Math.max(segmentTotal, keyframeTotal);

  return {
    schema: payload?.schema || payload?.schema_version || '',
    totalTimeSec,
    segments,
    stockKeyframes,
    machines: Array.isArray(payload?.machines) ? payload.machines : [],
    fixtures: payload?.fixtures || null,
  };
}

function normalizeSimulationSegments(rawSegments) {
  if (!Array.isArray(rawSegments)) return [];

  let cursorSec = 0;
  return rawSegments.map((segment, index) => {
    const start = numberOrNull(
      segment.start_time_sec
      ?? segment.startTimeSec
      ?? segment.start_sec
      ?? segment.startSec
      ?? segment.time_sec
    );
    const duration = numberOrNull(segment.duration_sec ?? segment.durationSec);
    const end = numberOrNull(
      segment.end_time_sec
      ?? segment.endTimeSec
      ?? segment.end_sec
      ?? segment.endSec
    );
    const startTimeSec = start ?? cursorSec;
    const endTimeSec = end ?? (duration !== null ? startTimeSec + duration : startTimeSec + 0.25);
    const sequence = segment.sequence_number
      ?? segment.operation_sequence_number
      ?? segment.operationSequenceNumber
      ?? segment.op_sequence
      ?? null;
    const operationLabel = typeof segment.operation === 'string'
      ? segment.operation
      : (segment.operation?.operation || segment.operation_name || segment.label || '');
    const normalized = {
      ...segment,
      index,
      sequence_number: sequence,
      operation_label: operationLabel,
      moveType: segment.move_type || segment.moveType || segment.segment_type || segment.type || 'simulation',
      start: pointOrNull(segment.start_position || segment.startPosition || segment.start),
      end: pointOrNull(segment.end_position || segment.endPosition || segment.end),
      startTimeSec,
      endTimeSec: Math.max(startTimeSec, endTimeSec),
      durationSec: Math.max(0, endTimeSec - startTimeSec),
    };
    cursorSec = normalized.endTimeSec;
    return normalized;
  }).sort((a, b) => a.startTimeSec - b.startTimeSec);
}

function normalizeSimulationStockKeyframes(rawKeyframes) {
  if (!Array.isArray(rawKeyframes)) return [];

  return rawKeyframes.map((keyframe, index) => {
    const path = typeof keyframe === 'string' ? keyframe : keyframe?.path;
    if (!path) return null;

    const rawFormat = typeof keyframe === 'string'
      ? path.split('.').pop()
      : (keyframe.format || path.split('.').pop());
    const format = String(rawFormat || '').toLowerCase();
    if (format && format !== 'stl') return null;

    return {
      ...(typeof keyframe === 'string' ? {} : keyframe),
      index,
      path,
      format: 'stl',
      time_sec: numberOrNull(keyframe?.time_sec ?? keyframe?.timeSec) ?? 0,
      role: keyframe?.role || 'simulation_stock_keyframe',
      source: 'simulation_timeline',
    };
  }).filter(Boolean).sort((a, b) => a.time_sec - b.time_sec);
}

function simulationToolpathMoves(timeline) {
  const operations = [];
  const points = [];
  for (const segment of timeline?.segments || []) {
    if (!segment.start || !segment.end) continue;
    if (String(segment.moveType || segment.move_type || '').toLowerCase().includes('boring')) continue;
    const motion = turningDisplayMotion(segment);
    const start = latheGuidePoint(motion.start, segment);
    const end = latheGuidePoint(motion.end, segment);
    points.push(start, end);
    operations.push({
      sequence_number: segment.sequence_number,
      operation: segment.operation_label || segment.operation || segment.moveType || 'turning',
      tool_type: segment.moveType === 'boring' ? 'boring_bar' : (segment.tool_type || 'turning_tool'),
      tool_diameter_mm: segment.tool_diameter_mm || 8,
      moves: [
        { position: start, move_type: 'rapid' },
        { position: end, move_type: segment.moveType || segment.move_type || 'feed' },
      ],
    });
  }
  return { operations, points };
}

function turningDisplayMotion(segment) {
  const start = pointOrNull(segment?.start);
  const end = pointOrNull(segment?.end);
  if (!start || !end || !isLatheCuttingSegment(segment)) {
    return { start, end, reversed: false };
  }

  const moveType = String(segment?.moveType || segment?.move_type || '').toLowerCase();
  if ((moveType.includes('turn') || moveType.includes('od')) && Math.abs(start[2] - end[2]) > 1e-6) {
    const maxRadius = Math.max(Math.abs(start[0]), Math.abs(end[0]));
    const minRadius = Math.min(Math.abs(start[0]), Math.abs(end[0]));
    const lowZ = start[2] <= end[2] ? start : end;
    const highZ = start[2] > end[2] ? start : end;
    const sign = Number(start[0] || end[0]) < 0 ? -1 : 1;
    const freeEnd = [sign * maxRadius, lowZ[1], lowZ[2]];
    const chuckEnd = [sign * minRadius, highZ[1], highZ[2]];
    const reversed = Math.abs(start[2] - freeEnd[2]) > 1e-6
      || Math.abs(Math.abs(start[0]) - maxRadius) > 1e-6;
    return { start: freeEnd, end: chuckEnd, reversed };
  }

  const startDisplayX = latheDisplayX(start);
  const endDisplayX = latheDisplayX(end);
  if (startDisplayX < endDisplayX) {
    return { start: end, end: start, reversed: true };
  }
  return { start, end, reversed: false };
}

function latheGuidePoint(point, segment) {
  const next = [...point];
  const moveType = String(segment?.moveType || segment?.move_type || '').toLowerCase();
  const stockRadius = currentStockRadius();
  if (stockRadius > 0 && (moveType.includes('turn') || moveType.includes('od'))) {
    next[0] = radialWithSign(point[0], stockRadius);
  }
  return next;
}

function safeLatheToolPoint(point, segment, playback) {
  if (!window.__isTurningScene || !point || !isLatheCuttingSegment(segment)) return point;

  const next = [...point];
  const moveType = String(segment?.moveType || segment?.move_type || '').toLowerCase();
  const stockRadius = currentStockRadius();
  if (stockRadius <= 0) return next;

  if (moveType.includes('turn') || moveType.includes('od')) {
    const progress = segmentAbsoluteProgress(segment, playback);
    const targetRadius = Math.min(Math.abs(next[0]), stockRadius);
    const currentCutRadius = stockRadius - ((stockRadius - targetRadius) * progress);
    next[0] = radialWithSign(next[0], Math.max(targetRadius, currentCutRadius));
  }
  return next;
}

function isLatheCuttingSegment(segment) {
  const text = [
    segment?.operation,
    segment?.operation_label,
    segment?.moveType,
    segment?.move_type,
    segment?.segment_type,
    segment?.tool_type,
  ].filter(Boolean).join(' ').toLowerCase();
  return text.includes('turn') || text.includes('boring') || text.includes('lathe');
}

function latheDisplayX(point) {
  return -Number(point?.[2] || 0);
}

function currentStockRadius() {
  const dimensions = window.__currentScene?.stock_dimensions || {};
  return Number(dimensions.diameter || Math.max(dimensions.length || 0, dimensions.width || 0)) / 2;
}

function radialWithSign(value, radius) {
  const sign = Number(value) < 0 ? -1 : 1;
  return sign * radius;
}

function segmentAbsoluteProgress(segment, playback) {
  const start = numberOrNull(segment?.absoluteStartTimeSec) ?? numberOrNull(segment?.startTimeSec) ?? 0;
  const end = numberOrNull(segment?.absoluteEndTimeSec) ?? numberOrNull(segment?.endTimeSec) ?? start;
  const now = playbackAbsoluteTimeSec(playback);
  const duration = Math.max(end - start, 1e-6);
  return Math.max(0, Math.min(1, (now - start) / duration));
}

function isTurningScene(scene, timeline) {
  const values = [];
  for (const op of scene?.operations || []) {
    values.push(op.operation, op.process, op.tool_type, op.fidelity);
  }
  for (const op of timeline?.operations || []) {
    values.push(op.operation, op.process, op.fidelity);
  }
  for (const segment of timeline?.segments || []) {
    values.push(
      segment.operation,
      segment.operation_label,
      segment.segment_type,
      segment.moveType,
      segment.move_type,
      segment.tool_type,
      segment.fidelity,
    );
  }
  const text = values.filter(Boolean).join(' ').toLowerCase();
  return (
    text.includes('turn')
    || text.includes('lathe')
    || text.includes('boring')
    || text.includes('radius_profile')
  );
}

function machineForScene(scene, timeline) {
  if (scene?.machine && typeof scene.machine === 'object') return scene.machine;
  if (Array.isArray(scene?.machines) && scene.machines.length) return scene.machines[0];
  if (Array.isArray(timeline?.machines) && timeline.machines.length) return timeline.machines[0];
  return null;
}

async function loadSceneMarkers(scene, baseUrl) {
  const markers = [
    ...normalizeMarkers(scene.clearance_markers, 'clearance'),
    ...normalizeMarkers(scene.collision_markers, 'collision'),
    ...normalizeMarkers(scene.validation_markers, 'clearance'),
    ...normalizeMarkers(scene.markers, 'clearance'),
    ...normalizeMarkers(scene.clearance?.markers, 'clearance'),
    ...normalizeMarkers(scene.collision?.markers, 'collision'),
  ];

  for (const key of ['clearance_markers', 'collision_markers', 'validation_markers', 'markers']) {
    const asset = scene.assets?.[key];
    if (!asset) continue;
    try {
      const payload = await fetchJson(assetUrl(asset, baseUrl));
      const defaultType = key.includes('collision') ? 'collision' : 'clearance';
      markers.push(...normalizeMarkers(payload, defaultType));
    } catch (err) {
      console.warn(`Could not load ${key}:`, err);
    }
  }

  return markers;
}

function normalizeMarkers(payload, defaultType) {
  if (!payload) return [];
  if (Array.isArray(payload)) {
    return payload.flatMap(item => normalizeMarkers(item, defaultType));
  }
  if (Array.isArray(payload.markers)) {
    return normalizeMarkers(payload.markers, defaultType);
  }
  if (Array.isArray(payload.clearance_markers) || Array.isArray(payload.collision_markers)) {
    return [
      ...normalizeMarkers(payload.clearance_markers, 'clearance'),
      ...normalizeMarkers(payload.collision_markers, 'collision'),
    ];
  }
  if (typeof payload === 'object') {
    const position = payload.position || payload.center || payload.point || payload.tool_position;
    if (Array.isArray(position) && position.length >= 3) {
      return [{
        ...payload,
        marker_type: payload.marker_type || payload.type || defaultType,
        severity: payload.severity || payload.level || payload.type || defaultType,
      }];
    }
  }
  return [];
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
        setup: op.setup,
        face_selector: op.face_selector,
        tool: op.tool,
        tool_assembly: op.tool_assembly,
        tool_type: op.tool_type,
        tool_diameter_mm: op.tool_diameter_mm,
        summary: op.summary,
        toolpath_summary: op.toolpath_summary,
        tool_selection: op.tool_selection,
        pass_plan: op.pass_plan || op.toolpath?.pass_plan,
        passes: op.passes || op.toolpath?.passes,
        economics: op.economics,
        validation: op.validation,
        warnings: op.warnings,
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
  const economics = scene.economics || {};
  const time = economics.time_breakdown || {};
  const cost = economics.cost_breakdown || {};
  const currency = economics.currency || '';
  const totalMinutes = totalOperationMinutes(scene.operations || []);
  const rows = [
    ['Schema', scene.schema_version || 'unknown'],
    ['Material', scene.material || 'unspecified'],
    ['Stock', JSON.stringify(scene.stock_dimensions || {})],
    ['Operations', String((scene.operations || []).length)],
    ['Cutting time', formatMinutes(time.cutting_time_min ?? totalMinutes)],
    ['Fixtures', String((scene.fixtures || []).length)],
    ['Markers', String((window.__currentClearanceMarkers || []).length)],
  ];
  if (scene.economics) {
    rows.push(['Total time', formatMinutes(time.total_time_per_part_min)]);
    rows.push(['Tool changes', `${time.tool_change_count ?? 0} (${formatMinutes(time.tool_change_time_min || 0)})`]);
    rows.push(['Setup time', formatMinutes(time.setup_time_per_part_min || 0)]);
    rows.push(['Load/unload', formatMinutes(time.load_unload_time_per_part_min || 0)]);
    rows.push(['Machine', economics.machine_id || 'unknown']);
    rows.push(['Total cost', formatMoney(cost.total_cost, currency)]);
    rows.push(['Material cost', formatMoney(cost.material_cost, currency)]);
    rows.push(['Machine cost', formatMoney(cost.machine_cost, currency)]);
    rows.push(['Tooling cost', formatMoney(cost.tooling_cost, currency)]);
    rows.push(['Estimate', economics.quote_status === 'not_a_quote' ? 'engineering only' : economics.quote_status || 'engineering only']);
  }
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
    updateSelectedOperationDetails();
    return;
  }
  els.operations.innerHTML = `
    <button class="op-item complete selected" type="button" data-sequence="all">
      <div>All operations</div>
      <small>Combined toolpath · ${escapeHtml(formatMinutes(totalOperationMinutes(operations)))}</small>
    </button>
  ` + operations.map(op => {
    const detailOp = mergedOperationForSequence(op.sequence_number) || op;
    return `
    <button class="op-item complete" type="button" data-sequence="${escapeHtml(String(op.sequence_number ?? ''))}">
      <div>OP ${escapeHtml(String(op.sequence_number ?? '?'))}: ${escapeHtml(op.operation || '?')}</div>
      <small>${escapeHtml(toolLabel(detailOp))} · ${escapeHtml(passCountLabel(detailOp))} · ${escapeHtml(formatMinutes(operationMinutes(detailOp)))}</small>
      <small>${escapeHtml(op.setup || 'unassigned')} ${escapeHtml(op.face_selector || '')}</small>
    </button>
  `;
  }).join('');
  updateOperationSelection();
}

function updateSelectedOperationDetails() {
  if (!els['selected-operation']) return;

  const selected = window.__selectedToolpathOperation || 'all';
  const sceneOps = window.__currentScene?.operations || [];
  const selectedOps = selected === 'all'
    ? sceneOps.map(op => mergedOperationForSequence(op.sequence_number) || op)
    : sceneOps
      .filter(op => String(op.sequence_number) === selected)
      .map(op => mergedOperationForSequence(op.sequence_number) || op);

  if (selected === 'all') {
    const toolIds = uniqueValues(selectedOps.map(op => toolFromOperation(op).toolId).filter(Boolean));
    const holderIds = uniqueValues(selectedOps.map(op => toolFromOperation(op).holderId).filter(Boolean));
    const warnings = selectedOps.flatMap(op => collectOperationWarnings(op));
    const economics = window.__currentScene?.economics || {};
    const time = economics.time_breakdown || {};
    const cost = economics.cost_breakdown || {};
    const currency = economics.currency || '';
    els['selected-operation'].innerHTML = `
      <div class="operation-detail">
        <div class="detail-title">All operations</div>
        <div class="detail-grid">
          ${detailRow('Operations', String(selectedOps.length))}
          ${detailRow('Tools', toolIds.length ? toolIds.join(', ') : 'n/a')}
          ${detailRow('Holders', holderIds.length ? holderIds.join(', ') : 'n/a')}
          ${detailRow('Passes', passCountLabel(selectedOps))}
          ${detailRow('Cutting time', formatMinutes(time.cutting_time_min ?? totalOperationMinutes(selectedOps)))}
          ${window.__currentScene?.economics ? detailRow('Total time', formatMinutes(time.total_time_per_part_min)) : ''}
          ${window.__currentScene?.economics ? detailRow('Total cost', formatMoney(cost.total_cost, currency)) : ''}
        </div>
        ${renderWarnings(warnings)}
      </div>
    `;
    return;
  }

  const operation = mergedOperationForSequence(selected);
  if (!operation) {
    els['selected-operation'].innerHTML = '<div class="detail-empty">Select an operation to inspect tool, passes, time, and warnings.</div>';
    return;
  }

  const playback = window.__playback || emptyPlayback();
  const segment = segmentAtTime(playback, playback.elapsedSec);
  const currentPass = segment?.operation && String(segment.operation.sequence_number) === String(operation.sequence_number)
    ? segment.passNumber
    : null;
  const tool = toolFromOperation(operation);
  const warnings = collectOperationWarnings(operation);
  const selection = operation.tool_selection || operation.tool?.selection || {};
  const economics = operation.economics || {};
  const rejectedCount = Array.isArray(selection.rejected_tools) ? selection.rejected_tools.length : 0;

  els['selected-operation'].innerHTML = `
    <div class="operation-detail">
      <div class="detail-title">OP ${escapeHtml(operation.sequence_number ?? '?')}: ${escapeHtml(operation.operation || '?')}</div>
      <div class="detail-grid">
        ${detailRow('Selected tool', tool.toolId || tool.toolNumber || 'n/a')}
        ${detailRow('Holder', tool.holderId || 'n/a')}
        ${detailRow('Tool dia', `${formatNumber(tool.diameter)} mm`)}
        ${detailRow('Pass', currentPass ? `${currentPass} / ${passCount(operation)}` : passCountLabel(operation))}
        ${detailRow('Operation time', formatMinutes(operationMinutes(operation)))}
        ${operation.economics ? detailRow('Tool cost', formatMoney(economics.tooling_cost, economics.currency || window.__currentScene?.economics?.currency || '')) : ''}
        ${operation.economics ? detailRow('Cost rate', `${formatMoney(economics.tool_cost_per_cutting_min, economics.currency || window.__currentScene?.economics?.currency || '')}/cut min`) : ''}
        ${detailRow('Setup', `${operation.setup || 'unassigned'} ${operation.face_selector || ''}`)}
        ${detailRow('Selection reason', selection.reason || operation.selection_reason || 'n/a')}
        ${rejectedCount ? detailRow('Rejected tools', String(rejectedCount)) : ''}
      </div>
      ${renderWarnings(warnings)}
    </div>
  `;
}

function mergedOperationForSequence(sequence) {
  const sceneOp = (window.__currentScene?.operations || [])
    .find(op => String(op.sequence_number) === String(sequence)) || {};
  const toolpathOp = (window.__currentToolpathMoves || [])
    .find(op => String(op.sequence_number) === String(sequence)) || {};
  if (!sceneOp.sequence_number && !toolpathOp.sequence_number) return null;
  return {
    ...sceneOp,
    ...toolpathOp,
    tool: toolpathOp.tool || sceneOp.tool,
    tool_assembly: toolpathOp.tool_assembly || sceneOp.tool_assembly,
    toolpath_summary: sceneOp.toolpath_summary || toolpathOp.toolpath_summary || toolpathOp.summary,
    summary: toolpathOp.summary || sceneOp.summary,
    pass_plan: toolpathOp.pass_plan || sceneOp.pass_plan,
    passes: toolpathOp.passes || sceneOp.passes,
    economics: toolpathOp.economics || sceneOp.economics,
    validation: mergeValidation(sceneOp.validation, toolpathOp.validation),
    warnings: [
      ...(Array.isArray(sceneOp.warnings) ? sceneOp.warnings : []),
      ...(Array.isArray(toolpathOp.warnings) ? toolpathOp.warnings : []),
    ],
  };
}

function detailRow(label, value) {
  return `<div class="detail-row"><span>${escapeHtml(label)}</span><strong>${escapeHtml(value)}</strong></div>`;
}

function renderWarnings(warnings) {
  if (!warnings.length) {
    return '<div class="warning-list"><div class="warning-item ok">No warnings for selected operation.</div></div>';
  }
  return `<div class="warning-list">${warnings.map(warning => {
    const level = String(warning.level || warning.severity || warning.type || '').toLowerCase();
    const isError = level.includes('error') || level.includes('fail') || level.includes('collision');
    return `<div class="warning-item ${isError ? 'error' : ''}">${escapeHtml(warningText(warning))}</div>`;
  }).join('')}</div>`;
}

function warningText(warning) {
  if (typeof warning === 'string') return warning;
  return warning.message || warning.text || warning.description || warning.code || JSON.stringify(warning);
}

function collectOperationWarnings(operation) {
  if (!operation) return [];
  const warnings = [];
  for (const source of [
    operation.warnings,
    operation.validation?.warnings,
    operation.validation?.errors,
    operation.tool_selection?.warnings,
    operation.tool_selection?.errors,
    operation.tool?.selection?.warnings,
    operation.tool?.selection?.errors,
  ]) {
    if (Array.isArray(source)) warnings.push(...source);
  }

  const selected = String(operation.sequence_number ?? '');
  for (const marker of window.__currentClearanceMarkers || []) {
    const markerSeq = marker.sequence_number ?? marker.operation_sequence ?? marker.operation_id ?? marker.op;
    if (markerSeq !== undefined && String(markerSeq) === selected) {
      warnings.push({
        severity: marker.severity || marker.marker_type || 'clearance',
        message: marker.message || marker.label || `${marker.marker_type || 'clearance'} marker near operation`,
      });
    }
  }
  return warnings;
}

function mergeValidation(a, b) {
  if (!a && !b) return undefined;
  return {
    warnings: [
      ...(Array.isArray(a?.warnings) ? a.warnings : []),
      ...(Array.isArray(b?.warnings) ? b.warnings : []),
    ],
    errors: [
      ...(Array.isArray(a?.errors) ? a.errors : []),
      ...(Array.isArray(b?.errors) ? b.errors : []),
    ],
  };
}

function renderSelectedToolpath() {
  if (!els['show-toolpath'].checked) {
    viewer.setToolpath(null);
  } else {
    const selectedOperations = getSelectedOperations();
    viewer.setToolpathMoves(selectedOperations);
  }

  preparePlayback(getSelectedOperations(), { reset: true });
  updateSelectedOperationDetails();
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
  updateSelectedOperationDetails();
}

function emptyPlayback() {
  return {
    source: 'toolpath',
    segments: [],
    totalTimeSec: 0,
    elapsedSec: 0,
    timeOriginSec: 0,
    toolpathFallback: null,
    isPlaying: false,
    lastTimestamp: null,
    rafId: null,
  };
}

function preparePlayback(operations, options = {}) {
  stopPlayback();
  const toolpathPlayback = buildPlayback(operations || []);
  const playback = buildSimulationPlayback(window.__simulationTimeline, operations || [], toolpathPlayback)
    || toolpathPlayback;
  if (options.reset !== false) {
    playback.elapsedSec = 0;
  } else if (window.__playback) {
    playback.elapsedSec = Math.min(window.__playback.elapsedSec || 0, playback.totalTimeSec);
  }
  window.__playback = playback;
  updatePlaybackAt(playback.elapsedSec);
  updatePlaybackLabel();
}

function buildSimulationPlayback(timeline, operations, toolpathPlayback) {
  if (!timeline) return null;

  const selected = window.__selectedToolpathOperation || 'all';
  let sourceSegments = timeline.segments || [];
  if (selected !== 'all') {
    sourceSegments = sourceSegments.filter(segment => String(segment.sequence_number) === selected);
  }

  const hasSelectedSegments = sourceSegments.length > 0;
  const originSec = selected === 'all' || !hasSelectedSegments
    ? 0
    : Math.min(...sourceSegments.map(segment => segment.startTimeSec));
  const segmentTotalSec = hasSelectedSegments
    ? Math.max(...sourceSegments.map(segment => segment.endTimeSec)) - originSec
    : 0;
  const totalTimeSec = selected === 'all'
    ? timeline.totalTimeSec
    : segmentTotalSec;

  if (!hasSelectedSegments && !(totalTimeSec > 0)) return null;

  const playback = emptyPlayback();
  playback.source = 'simulation_timeline';
  playback.timeOriginSec = originSec;
  playback.totalTimeSec = Math.max(0, totalTimeSec || segmentTotalSec);
  playback.toolpathFallback = toolpathPlayback?.segments?.length ? toolpathPlayback : null;

  if (hasSelectedSegments) {
    playback.segments = sourceSegments.map(segment => {
      const startTimeSec = Math.max(0, segment.startTimeSec - originSec);
      const endTimeSec = Math.max(startTimeSec, segment.endTimeSec - originSec);
      const operation = operationForSimulationSegment(segment, operations);
      const motion = window.__isTurningScene ? turningDisplayMotion(segment) : { start: segment.start, end: segment.end };
      return {
        ...segment,
        start: motion.start,
        end: motion.end,
        startTimeSec,
        endTimeSec,
        absoluteStartTimeSec: segment.startTimeSec,
        absoluteEndTimeSec: segment.endTimeSec,
        displayMotionReversed: Boolean(motion.reversed),
        durationSec: Math.max(0, endTimeSec - startTimeSec),
        operation,
        tool: toolFromOperation({
          ...(operation || {}),
          tool_type: segment.moveType === 'boring'
            ? 'boring_bar'
            : (segment.tool_type || operation?.tool_type),
          tool_diameter_mm: segment.tool_diameter_mm || operation?.tool_diameter_mm,
        }),
      };
    });
  } else {
    playback.segments = [{
      startTimeSec: 0,
      endTimeSec: playback.totalTimeSec,
      durationSec: playback.totalTimeSec,
      moveType: 'simulation',
      operation: null,
      passNumber: null,
    }];
  }

  if (playback.totalTimeSec <= 0) {
    playback.totalTimeSec = playback.segments.reduce((max, segment) => Math.max(max, segment.endTimeSec), 0);
  }
  return playback.segments.length ? playback : null;
}

function operationForSimulationSegment(segment, selectedOperations) {
  const sequence = segment.sequence_number;
  const operation = (selectedOperations || [])
    .find(op => String(op.sequence_number) === String(sequence))
    || mergedOperationForSequence(sequence);
  if (operation) return operation;
  if (sequence === null && !segment.operation_label) return null;
  return {
    sequence_number: sequence,
    operation: segment.operation_label || segment.label || segment.moveType || 'simulation',
  };
}

function buildPlayback(operations) {
  const playback = emptyPlayback();

  for (const operation of operations) {
    const moves = operation.moves || [];
    const rawSegments = [];
    const movePassNumbers = inferMovePassNumbers(operation);
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
        passNumber: movePassNumbers[i] || 1,
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
  if (viewer.setMachinePlayback) {
    viewer.setMachinePlayback({ isPlaying: false, segment: null });
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

async function exportPlaybackVideo() {
  const playback = window.__playback || emptyPlayback();
  if (window.__videoExportActive || !playback.segments.length || playback.totalTimeSec <= 0) {
    return;
  }
  if (typeof MediaRecorder === 'undefined') {
    setExportStatus('MediaRecorder unavailable');
    return;
  }
  if (!viewer.captureStream) {
    setExportStatus('Canvas capture unavailable');
    return;
  }

  const mimeType = supportedVideoMimeType();
  if (!mimeType) {
    setExportStatus('WebM recording unavailable');
    return;
  }

  stopPlayback();
  window.__videoExportActive = true;
  updateExportAvailability();
  setExportProgress(0);
  setExportStatus('Preparing frames');

  const fps = Math.max(1, Number(window.__videoManifest?.fps || 30));
  const speed = Math.max(0.1, Number(els['playback-speed'].value || window.__videoManifest?.playback_rate || 1));
  const stream = viewer.captureStream(fps);
  if (!stream) {
    window.__videoExportActive = false;
    updateExportAvailability();
    setExportStatus('Canvas capture unavailable');
    return;
  }

  let recorder = null;
  try {
    await preloadSimulationStockKeyframes(progress => {
      setExportProgress(progress * 0.12);
      setExportStatus(`Preparing ${Math.round(progress * 100)}%`);
    });

    await setPlaybackFrameForExport(0);
    const chunks = [];
    recorder = new MediaRecorder(stream, {
      mimeType,
      videoBitsPerSecond: 8_000_000,
    });
    const stopped = new Promise((resolve, reject) => {
      recorder.ondataavailable = event => {
        if (event.data && event.data.size > 0) chunks.push(event.data);
      };
      recorder.onerror = event => reject(event.error || new Error('Video recorder failed'));
      recorder.onstop = () => resolve();
    });

    playback.isPlaying = true;
    playback.lastTimestamp = null;
    window.__playback = playback;
    els['playback-play'].textContent = 'Pause';

    recorder.start(250);
    const started = performance.now();
    await new Promise((resolve, reject) => {
      const frame = async now => {
        if (!window.__videoExportActive) {
          resolve();
          return;
        }
        const wallElapsedSec = Math.max(0, (now - started) / 1000);
        const elapsedSec = Math.min(playback.totalTimeSec, wallElapsedSec * speed);
        try {
          await setPlaybackFrameForExport(elapsedSec);
        } catch (err) {
          reject(err);
          return;
        }
        updatePlaybackLabel();
        setExportProgress(0.12 + (elapsedSec / playback.totalTimeSec) * 0.86);
        setExportStatus(`${formatTime(elapsedSec)} / ${formatTime(playback.totalTimeSec)} at ${speed}x`);
        if (elapsedSec >= playback.totalTimeSec) {
          resolve();
          return;
        }
        requestAnimationFrame(frame);
      };
      requestAnimationFrame(frame);
    });

    await setPlaybackFrameForExport(playback.totalTimeSec);
    await new Promise(resolve => setTimeout(resolve, 350));
    recorder.stop();
    await stopped;

    const blob = new Blob(chunks, { type: mimeType });
    if (!blob.size) throw new Error('Recorder produced an empty video');
    downloadBlob(blob, exportVideoFilename(mimeType));
    setExportProgress(1);
    setExportStatus(`${formatBytes(blob.size)} WebM exported`);
  } catch (err) {
    console.error(err);
    if (recorder && recorder.state !== 'inactive') {
      recorder.stop();
    }
    setExportStatus(err?.message || 'Video export failed');
  } finally {
    stream.getTracks().forEach(track => track.stop());
    playback.isPlaying = false;
    playback.lastTimestamp = null;
    window.__playback = playback;
    window.__videoExportActive = false;
    if (viewer.setMachinePlayback) {
      viewer.setMachinePlayback({ isPlaying: false, segment: null });
    }
    if (els['playback-play']) {
      els['playback-play'].textContent = 'Play';
    }
    updatePlaybackLabel();
    updateExportAvailability();
  }
}

async function setPlaybackFrameForExport(elapsedSec) {
  const playback = window.__playback || emptyPlayback();
  updatePlaybackAt(elapsedSec, { skipStockLoad: true });
  if (playback.source === 'simulation_timeline') {
    await loadSimulationStockAt(playbackAbsoluteTimeSec(playback));
  }
  if (viewer.renderFrame) viewer.renderFrame();
}

async function preloadSimulationStockKeyframes(onProgress) {
  const keyframes = (window.__simulationStockKeyframes || []).filter(keyframe => keyframe?.path);
  if (!keyframes.length || !window.__sceneBaseUrl) {
    onProgress?.(1);
    return;
  }
  let completed = 0;
  for (const keyframe of keyframes) {
    if (!keyframe._arrayBufferPromise) {
      keyframe._arrayBufferPromise = fetchArrayBuffer(assetUrl(keyframe, window.__sceneBaseUrl));
    }
    await keyframe._arrayBufferPromise;
    completed += 1;
    onProgress?.(completed / keyframes.length);
  }
}

function supportedVideoMimeType() {
  if (typeof MediaRecorder.isTypeSupported !== 'function') {
    return 'video/webm';
  }
  const candidates = [
    'video/webm;codecs=vp9',
    'video/webm;codecs=vp8',
    'video/webm',
  ];
  return candidates.find(type => MediaRecorder.isTypeSupported(type)) || '';
}

function exportVideoFilename(mimeType) {
  const sceneName = window.__currentScene?.title || els['session-path']?.value || 'subcad-operation-video';
  const slug = String(sceneName)
    .replace(/\.json$/i, '')
    .replace(/[^a-z0-9]+/gi, '-')
    .replace(/^-+|-+$/g, '')
    .toLowerCase()
    .slice(0, 80) || 'subcad-operation-video';
  const extension = mimeType.includes('webm') ? 'webm' : 'video';
  return `${slug}-${new Date().toISOString().replace(/[:.]/g, '-')}.${extension}`;
}

function downloadBlob(blob, filename) {
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  setTimeout(() => URL.revokeObjectURL(url), 30_000);
}

function updateExportAvailability() {
  if (!els['export-video']) return;
  const playback = window.__playback || emptyPlayback();
  const supported = typeof MediaRecorder !== 'undefined' && Boolean(viewer.captureStream);
  els['export-video'].disabled = Boolean(window.__videoExportActive) || !supported || !playback.segments.length;
  if (!supported) {
    setExportStatus('Recording unavailable');
  } else if (!playback.segments.length) {
    setExportStatus('No playback loaded');
  } else if (!window.__videoExportActive && !els['export-video-status'].textContent) {
    setExportStatus('Ready');
  }
}

function setExportStatus(message) {
  if (els['export-video-status']) {
    els['export-video-status'].textContent = message || '';
  }
}

function setExportProgress(value) {
  const progress = Math.max(0, Math.min(1, Number(value || 0)));
  if (els['export-progress']) {
    els['export-progress'].hidden = progress <= 0 || progress >= 1;
  }
  if (els['export-progress-fill']) {
    els['export-progress-fill'].style.width = `${Math.round(progress * 100)}%`;
  }
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

function updatePlaybackAt(elapsedSec, options = {}) {
  const playback = window.__playback || emptyPlayback();
  playback.elapsedSec = Math.max(0, Math.min(playback.totalTimeSec || 0, Number(elapsedSec || 0)));
  window.__playback = playback;
  if (playback.source === 'simulation_timeline' && !options.skipStockLoad) {
    loadSimulationStockAt(playbackAbsoluteTimeSec(playback));
  }

  if (!playback.segments.length) {
    viewer.setToolVisible(false);
    if (viewer.setMachinePlayback) {
      viewer.setMachinePlayback({ isPlaying: false, segment: null });
    }
    els['playback-range'].value = 0;
    return;
  }

  const segment = segmentAtTime(playback, playback.elapsedSec);
  if (!segment) return;
  if (viewer.setMachinePlayback) {
    viewer.setMachinePlayback({ isPlaying: playback.isPlaying, segment });
  }
  const toolSegment = toolMotionSegmentAt(playback, segment);

  if (toolSegment && els['show-tool'].checked) {
    const local = toolSegment.durationSec > 0
      ? (toolSegment.elapsedSec - toolSegment.startTimeSec) / toolSegment.durationSec
      : 1;
    const rawPosition = lerp3(toolSegment.start, toolSegment.end, Math.max(0, Math.min(1, local)));
    const position = safeLatheToolPoint(rawPosition, toolSegment, playback);
    const tool = toolSegment.tool || segment.tool || toolFromOperation(segment.operation || {});
    viewer.updateTool(
      position,
      null,
      tool.toolType,
      tool.diameter,
      tool.fluteLength,
      tool,
    );
    viewer.setToolVisible(true);
  } else {
    viewer.setToolVisible(false);
  }

  els['playback-range'].value = playback.totalTimeSec > 0
    ? Math.round((playback.elapsedSec / playback.totalTimeSec) * 1000)
    : 0;
  updateSelectedOperationDetails();
}

function updatePlaybackLabel() {
  const playback = window.__playback || emptyPlayback();
  if (!playback.segments.length) {
    els['playback-label'].textContent = window.__simulationTimeline ? 'No playback loaded' : 'No toolpath loaded';
    els['playback-play'].disabled = true;
    els['playback-reset'].disabled = true;
    updateExportAvailability();
    return;
  }

  els['playback-play'].disabled = false;
  els['playback-reset'].disabled = false;
  updateExportAvailability();
  const segment = segmentAtTime(playback, playback.elapsedSec) || playback.segments[0];
  const opLabel = segment?.operation
    ? `OP ${segment.operation.sequence_number}: ${segment.operation.operation}`
    : 'Toolpath';
  const passLabel = segment?.passNumber ? ` · pass ${segment.passNumber}/${passCount(segment.operation)}` : '';
  els['playback-label'].textContent = `${opLabel} · ${segment.moveType}${passLabel} · `
    + `${formatTime(playback.elapsedSec)} / ${formatTime(playback.totalTimeSec)} `
    + `(${els['playback-speed'].value}x)`;
}

function playbackAbsoluteTimeSec(playback) {
  return Number(playback?.timeOriginSec || 0) + Number(playback?.elapsedSec || 0);
}

function toolMotionSegmentAt(playback, segment) {
  if (segment?.start && segment?.end) {
    return {
      ...segment,
      elapsedSec: playback.elapsedSec,
    };
  }

  const fallback = playback.toolpathFallback;
  if (!fallback?.segments?.length || playback.totalTimeSec <= 0) return null;

  const fallbackElapsedSec = Math.min(
    fallback.totalTimeSec,
    (playback.elapsedSec / playback.totalTimeSec) * fallback.totalTimeSec,
  );
  const fallbackSegment = segmentAtTime(fallback, fallbackElapsedSec);
  if (!fallbackSegment?.start || !fallbackSegment?.end) return null;
  return {
    ...fallbackSegment,
    elapsedSec: fallbackElapsedSec,
  };
}

function loadSimulationStockAt(absoluteTimeSec) {
  const keyframes = window.__simulationStockKeyframes || [];
  if (!keyframes.length || !window.__sceneBaseUrl) return Promise.resolve();

  const index = simulationStockKeyframeIndexAtTime(keyframes, absoluteTimeSec);
  if (index < 0 || index === window.__currentSimulationKeyframeIndex) return Promise.resolve();

  window.__currentSimulationKeyframeIndex = index;
  if (!(window.__stockStates || []).length) {
    window.__currentStateIndex = index;
    updateTimelineControls();
  }
  const requestId = (window.__simulationStockRequestId || 0) + 1;
  window.__simulationStockRequestId = requestId;
  return loadSimulationStockKeyframe(index, requestId).catch(err => {
    if (requestId === window.__simulationStockRequestId) {
      console.warn('Could not load simulation stock keyframe:', err);
    }
  });
}

function simulationStockKeyframeIndexAtTime(keyframes, absoluteTimeSec) {
  const timeSec = Number(absoluteTimeSec || 0);
  let selectedIndex = -1;
  for (let index = 0; index < keyframes.length; index += 1) {
    if (keyframes[index].time_sec <= timeSec + 1e-6) {
      selectedIndex = index;
    } else {
      break;
    }
  }
  return selectedIndex;
}

async function loadSimulationStockKeyframe(index, requestId) {
  const keyframes = window.__simulationStockKeyframes || [];
  const keyframe = keyframes[index];
  if (!keyframe || !window.__sceneBaseUrl) return;

  if (!keyframe._arrayBufferPromise) {
    keyframe._arrayBufferPromise = fetchArrayBuffer(assetUrl(keyframe, window.__sceneBaseUrl));
  }
  const arrayBuffer = await keyframe._arrayBufferPromise;
  if (requestId !== window.__simulationStockRequestId) return;

  await viewer.loadStockSTL(arrayBuffer);
  viewer.setStockVisible(els['show-stock'].checked);
}

function segmentAtTime(playback, elapsedSec) {
  if (!playback.segments.length) return null;
  return playback.segments.find(segment => elapsedSec >= segment.startTimeSec && elapsedSec <= segment.endTimeSec)
    || (elapsedSec < playback.segments[0].startTimeSec ? playback.segments[0] : null)
    || playback.segments[playback.segments.length - 1];
}

function toolFromOperation(operation) {
  const tool = operation.tool || {};
  const assembly = operation.tool_assembly || tool.assembly || {};
  return {
    toolType: operation.tool_type || tool.tool_type || 'flat_endmill',
    diameter: Number(operation.tool_diameter_mm || assembly.cutter_diameter_mm || tool.diameter_mm || 6),
    fluteLength: Number(assembly.flute_length_mm || tool.flute_length_mm || tool.fluteLength || 30),
    shankDiameter: Number(operation.tool_diameter_mm || assembly.shank_diameter_mm || tool.shank_diameter_mm || tool.diameter_mm || 6),
    stickout: Number(assembly.stickout_mm || tool.stickout_mm || tool.flute_length_mm || 35),
    holderId: assembly.holder_id || tool.holder_id || 'generic_holder',
    holderDiameter: Number(assembly.holder_diameter_mm || tool.holder_diameter_mm || 25),
    holderLength: Number(assembly.holder_length_mm || tool.holder_length_mm || 35),
    toolId: assembly.tool_id || tool.catalog_id || '',
    toolNumber: assembly.tool_number || tool.tool_number || null,
  };
}

function toolLabel(operation) {
  const tool = toolFromOperation(operation || {});
  const toolId = tool.toolId || (tool.toolNumber ? `T${tool.toolNumber}` : 'tool n/a');
  const holderId = tool.holderId || 'holder n/a';
  return `${toolId} / ${holderId}`;
}

function passCountLabel(operationOrOperations) {
  if (Array.isArray(operationOrOperations)) {
    const total = operationOrOperations.reduce((sum, op) => sum + passCount(op), 0);
    return `${total} pass${total === 1 ? '' : 'es'}`;
  }
  const count = passCount(operationOrOperations || {});
  return `${count} pass${count === 1 ? '' : 'es'}`;
}

function passCount(operation) {
  if (!operation) return 0;
  const explicit = Number(
    operation.pass_count
    || operation.summary?.pass_count
    || operation.toolpath_summary?.pass_count
    || operation.pass_plan?.pass_count
  );
  if (explicit > 0) return explicit;
  if (Array.isArray(operation.passes)) return Math.max(1, operation.passes.length);
  if (Array.isArray(operation.pass_plan?.passes)) return Math.max(1, operation.pass_plan.passes.length);
  if (Array.isArray(operation.pass_plan)) return Math.max(1, operation.pass_plan.length);
  return Math.max(1, inferMovePassNumbers(operation).reduce((max, value) => Math.max(max, value), 1));
}

function inferMovePassNumbers(operation) {
  const moves = operation?.moves || [];
  if (!moves.length) return [];

  if (Array.isArray(operation.passes) && operation.passes.length) {
    return mapMovesToExplicitPasses(moves, operation.passes);
  }
  if (Array.isArray(operation.pass_plan?.passes) && operation.pass_plan.passes.length) {
    return mapMovesToExplicitPasses(moves, operation.pass_plan.passes);
  }

  const passNumbers = [];
  const depthLevels = new Map();
  let currentPass = 1;
  for (let i = 0; i < moves.length; i += 1) {
    const move = moves[i];
    const explicit = Number(move.pass_number || move.pass || move.pass_index);
    if (explicit > 0) {
      currentPass = Math.max(1, explicit);
      passNumbers.push(currentPass);
      continue;
    }

    const type = moveTypeOf(move);
    const z = Array.isArray(move.position) ? Number(move.position[2]) : null;
    if ((type === 'feed' || type === 'plunge' || type === 'arc') && Number.isFinite(z)) {
      const key = z.toFixed(3);
      if (!depthLevels.has(key)) {
        depthLevels.set(key, depthLevels.size + 1);
      }
      currentPass = depthLevels.get(key);
    }
    passNumbers.push(currentPass);
  }
  return passNumbers;
}

function mapMovesToExplicitPasses(moves, passes) {
  const labels = moves.map(() => 1);
  for (let index = 0; index < passes.length; index += 1) {
    const pass = passes[index] || {};
    const moveIndexes = pass.move_indexes || pass.move_indices;
    if (Array.isArray(moveIndexes)) {
      for (const moveIndex of moveIndexes) {
        if (moveIndex >= 0 && moveIndex < labels.length) {
          labels[moveIndex] = index + 1;
        }
      }
    }
  }
  return labels;
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

function uniqueValues(values) {
  return [...new Set(values.map(value => String(value)).filter(Boolean))];
}

function formatNumber(value) {
  const numeric = Number(value);
  if (!Number.isFinite(numeric)) return 'n/a';
  return numeric.toFixed(Math.abs(numeric) >= 10 ? 1 : 2);
}

function formatBytes(value) {
  const bytes = Number(value);
  if (!Number.isFinite(bytes) || bytes <= 0) return '0 B';
  const units = ['B', 'KB', 'MB', 'GB'];
  const index = Math.min(Math.floor(Math.log(bytes) / Math.log(1024)), units.length - 1);
  const scaled = bytes / (1024 ** index);
  return `${scaled.toFixed(index === 0 ? 0 : 1)} ${units[index]}`;
}

function numberOrNull(value) {
  const numeric = Number(value);
  return Number.isFinite(numeric) ? numeric : null;
}

function pointOrNull(value) {
  if (!Array.isArray(value) || value.length < 3) return null;
  const point = [Number(value[0]), Number(value[1]), Number(value[2])];
  return point.every(Number.isFinite) ? point : null;
}

function formatMinutes(minutes) {
  const value = Number(minutes || 0);
  if (value < 1) {
    return `${(value * 60).toFixed(1)} s`;
  }
  return `${value.toFixed(2)} min`;
}

function formatMoney(value, currency = '') {
  const numeric = Number(value);
  if (!Number.isFinite(numeric)) return 'n/a';
  const prefix = currency ? `${currency} ` : '';
  return `${prefix}${numeric.toFixed(2)}`;
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
  const states = stockTimelineStates();
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
  const states = stockTimelineStates();
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
  const states = stockTimelineStates();
  const state = states[index];
  if (!state || !window.__sceneBaseUrl) return;

  window.__simulationStockRequestId = (window.__simulationStockRequestId || 0) + 1;
  window.__currentStateIndex = index;
  if (state.source === 'simulation_timeline') {
    window.__currentSimulationKeyframeIndex = index;
  }
  await viewer.loadStockSTL(await fetchArrayBuffer(assetUrl(state, window.__sceneBaseUrl)));
  viewer.setStockVisible(els['show-stock'].checked);
  updateTimelineControls();
}

function updateTimelineControls() {
  const states = stockTimelineStates();
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

  const sequence = state.sequence_number;
  const prefix = sequence === 0
    ? 'Initial'
    : (sequence === null || sequence === undefined ? formatTime(state.time_sec || 0) : `OP ${sequence}`);
  els['timeline-label'].textContent = `${prefix}: ${state.operation || state.label || 'stock state'}`;
}

function stockTimelineStates() {
  const stockStates = window.__stockStates || [];
  if (stockStates.length) return stockStates;
  return window.__simulationStockKeyframes || [];
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
