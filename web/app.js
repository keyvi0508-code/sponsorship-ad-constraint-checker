const $ = (selector) => document.querySelector(selector);
const ids = {
  caseId: $('#case-id'), caption: $('#caption'), spoken: $('#spoken'), onscreen: $('#onscreen'),
  multipleBrands: $('#multiple-brands'), productUse: $('#product-use'),
};
let savedReference = null;
let reviewState = { caseSnapshot: null, baseline: null, ai: null, final: null };
let observedMedianSeconds = null;
const POLICY_SOURCE = 'https://www.chanel.com/us/makeup/social-media-guidelines/';
const POLICY_ACCESSED = '2026-09-29';
const RULE_SECTIONS = {
  'CH-DISC-01': '1–2',
  'CH-DISC-02': '2',
  'CH-CONTEXT-01': '1',
  'CH-CLAIM-01': '3–4',
};

function toast(message) {
  const element = $('#toast');
  element.textContent = message;
  element.classList.add('show');
  window.clearTimeout(toast.timer);
  toast.timer = window.setTimeout(() => element.classList.remove('show'), 2800);
}

function lines(value) {
  return value.split(/\r?\n/).map((line) => line.trim()).filter(Boolean);
}

function currentCase() {
  const used = ids.productUse.value;
  const spokenLines = lines(ids.spoken.value);
  const onScreenLines = lines(ids.onscreen.value);
  return {
    case_id: ids.caseId.value.trim() || 'LOCAL-DRAFT',
    language: 'en',
    format: 'short_video',
    multiple_brands: ids.multipleBrands.checked,
    caption: lines(ids.caption.value),
    scenes: [{
      verbal_endorsement: spokenLines.length > 0,
      visual_endorsement: onScreenLines.length > 0,
      spoken_text: spokenLines,
      on_screen_text: onScreenLines,
    }],
    creator_used_product: used === 'unknown' ? null : used === 'true',
    claim_reference_sources: [],
  };
}

function clearDecision() {
  reviewState.final = null;
  $('#reviewer-decision').value = '';
  $('#reviewer-note').value = '';
  $('#decision-status').textContent = 'No final decision recorded.';
  $('#export-review').disabled = true;
}

function invalidateDecision() {
  if (!reviewState.final) return;
  reviewState.final = null;
  $('#decision-status').textContent = 'Decision changed; record it again.';
  $('#export-review').disabled = true;
}

function aiSummary(result, source) {
  const cost = Number.isFinite(result.estimated_cost_usd) ? ` · est. $${result.estimated_cost_usd.toFixed(4)}` : '';
  const wait = Number.isFinite(result.latency_seconds) ? ` · ${result.latency_seconds.toFixed(1)}s observed` : '';
  return `${source} · ${result.model || 'AI reviewer'}${cost}${wait}`;
}

function setVerdict(target, verdict, description) {
  const label = $(`#${target}-verdict`);
  label.textContent = verdict || '—';
  label.className = `verdict-name ${String(verdict || '').toLowerCase()}`;
  $(`#${target}-summary`).textContent = description || 'No review has been run.';
}

function addFinding(parent, finding) {
  const card = document.createElement('div');
  card.className = 'finding';
  const rule = document.createElement('strong');
  const ruleId = finding.rule_id || '';
  rule.textContent = ruleId || 'REVIEW NOTE';
  card.append(rule);
  if (ruleId && RULE_SECTIONS[ruleId]) {
    const source = document.createElement('a');
    source.className = 'finding-source';
    source.href = POLICY_SOURCE;
    source.target = '_blank';
    source.rel = 'noopener noreferrer';
    source.textContent = `CHANEL guide §${RULE_SECTIONS[ruleId]}`;
    source.setAttribute('aria-label', `Open CHANEL Social Media Guidelines, source section ${RULE_SECTIONS[ruleId]}`);
    card.append(source);
  }
  const quote = document.createElement('blockquote');
  quote.textContent = finding.evidence || 'No quoted evidence';
  const rationale = document.createElement('small');
  rationale.textContent = finding.rationale || finding.action || '';
  card.append(quote, rationale);
  parent.append(card);
}

function renderFindings(target, findings) {
  const container = $(`#${target}-findings`);
  container.replaceChildren();
  (findings || []).forEach((finding) => addFinding(container, finding));
  if (!findings || findings.length === 0) {
    const empty = document.createElement('small');
    empty.className = 'microcopy';
    empty.textContent = 'No in-scope findings returned.';
    container.append(empty);
  }
}

function showResults() {
  $('#empty-state').classList.add('hidden');
  $('#verdict-compare').classList.remove('hidden');
}

function showReference() {
  if (!savedReference) return;
  const ref = $('#reference-label');
  ref.textContent = `Saved reference label: ${savedReference}. Shown after the model and baseline outputs.`;
  ref.classList.remove('hidden');
}

function applyCase(caseData) {
  ids.caseId.value = caseData.case_id || 'LOCAL-DRAFT';
  ids.caption.value = (caseData.caption || []).join('\n');
  const scene = (caseData.scenes || [])[0] || {};
  ids.spoken.value = (scene.spoken_text || []).join('\n');
  ids.onscreen.value = (scene.on_screen_text || []).join('\n');
  ids.multipleBrands.checked = Boolean(caseData.multiple_brands);
  ids.productUse.value = caseData.creator_used_product === null || caseData.creator_used_product === undefined
    ? 'unknown' : caseData.creator_used_product ? 'true' : 'false';
}

function applyMetrics(metrics) {
  $('#ai-accuracy').textContent = `${(metrics.ai_accuracy * 100).toFixed(1)}%`;
  $('#baseline-accuracy').textContent = `${(metrics.baseline_accuracy * 100).toFixed(1)}%`;
  $('#human-rate').textContent = `${((metrics.ai_human_review / metrics.cases) * 100).toFixed(1)}%`;
  $('#estimated-cost').textContent = `$${metrics.estimated_cost_per_case_usd.toFixed(4)}`;
  observedMedianSeconds = metrics.median_ai_latency_seconds;
  $('#median-latency').textContent = `${observedMedianSeconds.toFixed(2)}s`;
}

async function loadSample() {
  try {
    const response = await fetch('/api/sample', { cache: 'no-store' });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Could not load saved example');
    applyCase(data.case);
    applyMetrics(data.metrics);
    const loadedAt = new Date().toISOString();
    reviewState = {
      caseSnapshot: JSON.stringify(currentCase()),
      baseline: { source: 'saved_demo', displayed_at: loadedAt, result: data.baseline },
      ai: { source: 'saved_api_output', displayed_at: loadedAt, result: data.ai },
      final: null,
    };
    clearDecision();
    setVerdict('baseline', data.baseline.verdict, 'Deterministic keyword-pattern result.');
    renderFindings('baseline', data.baseline.findings);
    setVerdict('ai', data.ai.verdict, aiSummary(data.ai, 'Saved two-stage result'));
    renderFindings('ai', data.ai.findings);
    savedReference = data.reference_verdict;
    $('#reference-label').classList.add('hidden');
    $('#show-reference').classList.remove('hidden');
    $('#mode-badge').textContent = 'SAVED DEMO · NO API';
    showResults();
    toast('Loaded saved case HOLDOUT-03. No API call was made.');
  } catch (error) {
    toast(error.message || 'Could not load the saved example. Start the local workbench again.');
  }
}

async function requestJson(route, payload) {
  const response = await fetch(route, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload),
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || `Request failed (${response.status})`);
  return data;
}

async function runBaseline() {
  try {
    const caseData = currentCase();
    const snapshot = JSON.stringify(caseData);
    const result = await requestJson('/api/baseline', { case: caseData });
    if (snapshot !== JSON.stringify(currentCase())) return toast('Draft changed while reviewing; run the check again.');
    if (reviewState.caseSnapshot !== snapshot) reviewState = { caseSnapshot: snapshot, baseline: null, ai: null, final: null };
    clearDecision();
    reviewState.baseline = { source: 'local_keyword_check', reviewed_at: new Date().toISOString(), result: result.baseline };
    setVerdict('baseline', result.baseline.verdict, 'Deterministic keyword-pattern result.');
    renderFindings('baseline', result.baseline.findings);
    $('#mode-badge').textContent = 'LOCAL KEYWORD CHECK';
    showResults();
    toast('Keyword review complete. No API call was made.');
  } catch (error) { toast(error.message); }
}

async function runAI() {
  try {
    const caseData = currentCase();
    const snapshot = JSON.stringify(caseData);
    const preflight = await requestJson('/api/preflight', { case: caseData });
    if (snapshot !== JSON.stringify(currentCase())) return toast('Draft changed; request a new cost estimate.');
    const waitContext = Number.isFinite(observedMedianSeconds)
      ? ` In the saved 30-case run, the median wait was ${observedMedianSeconds.toFixed(2)} seconds; this is not a live-time guarantee.` : '';
    const approved = window.confirm(
      `This AI review sends two requests to ${preflight.model}. The conservative cost ceiling is US$${preflight.conservative_cost_upper_bound_usd.toFixed(4)} for this script (the provider's actual charge may differ).${waitContext} Proceed?`
    );
    if (!approved) return;
    $('#ai-button').disabled = true;
    $('#ai-button').textContent = 'Reviewing…';
    const result = await requestJson('/api/review', { case: caseData, confirm_paid_run: true });
    if (snapshot !== JSON.stringify(currentCase())) return toast('Paid review completed, but the draft changed. Result not attached to this draft.');
    if (reviewState.caseSnapshot !== snapshot) reviewState = { caseSnapshot: snapshot, baseline: null, ai: null, final: null };
    clearDecision();
    reviewState.ai = { source: 'live_api', reviewed_at: new Date().toISOString(), result: result.ai };
    setVerdict('ai', result.ai.verdict, aiSummary(result.ai, 'Live API result'));
    renderFindings('ai', result.ai.findings);
    $('#mode-badge').textContent = 'LIVE API REVIEW';
    savedReference = null;
    $('#show-reference').classList.add('hidden');
    showResults();
    toast('AI review complete. The result is not saved by this prototype.');
  } catch (error) {
    toast(error.message || 'AI review failed. Check the local API key and connection.');
  } finally {
    $('#ai-button').disabled = false;
    $('#ai-button').innerHTML = '<span>✦</span> Request AI review';
  }
}

function markDraftChanged() {
  if (reviewState.caseSnapshot === JSON.stringify(currentCase())) return;
  reviewState = { caseSnapshot: null, baseline: null, ai: null, final: null };
  clearDecision();
  savedReference = null;
  $('#show-reference').classList.add('hidden');
  $('#reference-label').classList.add('hidden');
  setVerdict('baseline', '—', 'Run the keyword check to review this draft.');
  renderFindings('baseline', []);
  setVerdict('ai', '—', 'Request an AI review after checking its cost estimate.');
  renderFindings('ai', []);
  $('#mode-badge').textContent = 'UNSAVED DRAFT';
}

function recordDecision() {
  if (!reviewState.baseline && !reviewState.ai) return toast('Run a review before recording a decision.');
  if (reviewState.caseSnapshot !== JSON.stringify(currentCase())) return toast('Draft changed; review this version first.');
  const disposition = $('#reviewer-decision').value;
  if (!disposition) return toast('Choose a human disposition first.');
  reviewState.final = {
    disposition,
    rationale: $('#reviewer-note').value.trim(),
    recorded_at: new Date().toISOString(),
    actor: 'local_reviewer',
  };
  $('#decision-status').textContent = `${disposition} · recorded locally`;
  $('#export-review').disabled = false;
  toast('Decision recorded locally. Export it to keep a copy.');
}

function exportReview() {
  if (!reviewState.final || reviewState.caseSnapshot !== JSON.stringify(currentCase())) {
    return toast('Record a decision on the current draft before exporting.');
  }
  const record = {
    schema_version: '1.0',
    record_type: 'creator_content_review',
    exported_at: new Date().toISOString(),
    script: currentCase(),
    policy: {
      brand: 'CHANEL',
      scope: 'project interpretation of U.S. public social media guidelines',
      source_url: POLICY_SOURCE,
      source_accessed_on: POLICY_ACCESSED,
      rule_source_sections: RULE_SECTIONS,
      campaign_brief: { status: 'not_provided', mandatory_selling_points: 'not_evaluated' },
    },
    checks: { keyword_baseline: reviewState.baseline, ai_assisted: reviewState.ai },
    human_decision: reviewState.final,
    limitations: [
      'Text-only draft review; finished-video visibility and audibility not verified.',
      'A PASS covers only supported public-guideline checks, not campaign-specific selling points.',
      'Estimated API costs are calculated from token usage and a dated price snapshot, not an invoice.',
    ],
  };
  const filename = (record.script.case_id || 'review').replace(/[^a-z0-9_-]/gi, '_').slice(0, 60);
  const blob = new Blob([JSON.stringify(record, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `${filename}_review_${record.exported_at.slice(0, 10)}.json`;
  document.body.append(link);
  link.click();
  link.remove();
  window.setTimeout(() => URL.revokeObjectURL(url), 1000);
  toast('Review record downloaded to this computer.');
}

$('#load-sample').addEventListener('click', loadSample);
$('#load-sample-nav').addEventListener('click', loadSample);
$('#baseline-button').addEventListener('click', runBaseline);
$('#ai-button').addEventListener('click', runAI);
$('#show-reference').addEventListener('click', showReference);
$('#show-limits').addEventListener('click', () => toast('30 synthetic extension cases; the prompt was revised after earlier results; not an independent or real-world estimate.'));
$('#record-decision').addEventListener('click', recordDecision);
$('#export-review').addEventListener('click', exportReview);
$('#reviewer-decision').addEventListener('change', invalidateDecision);
$('#reviewer-note').addEventListener('input', invalidateDecision);
Object.values(ids).forEach((element) => element.addEventListener('input', markDraftChanged));
Object.values(ids).forEach((element) => element.addEventListener('change', markDraftChanged));
loadSample();
