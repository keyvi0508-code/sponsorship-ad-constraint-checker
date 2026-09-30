const $ = (selector) => document.querySelector(selector);
const ids = {
  caseId: $('#case-id'), caption: $('#caption'), spoken: $('#spoken'), onscreen: $('#onscreen'),
  multipleBrands: $('#multiple-brands'), productUse: $('#product-use'),
};
let savedReference = null;
let isSavedExample = false;

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
  rule.textContent = finding.rule_id || 'REVIEW NOTE';
  const quote = document.createElement('blockquote');
  quote.textContent = finding.evidence || 'No quoted evidence';
  const rationale = document.createElement('small');
  rationale.textContent = finding.rationale || finding.action || '';
  card.append(rule, quote, rationale);
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
}

async function loadSample() {
  try {
    const response = await fetch('/api/sample', { cache: 'no-store' });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Could not load saved example');
    applyCase(data.case);
    applyMetrics(data.metrics);
    setVerdict('baseline', data.baseline.verdict, 'Deterministic keyword-pattern result.');
    renderFindings('baseline', data.baseline.findings);
    setVerdict('ai', data.ai.verdict, `Saved two-stage result · ${data.ai.model || 'AI reviewer'}`);
    renderFindings('ai', data.ai.findings);
    savedReference = data.reference_verdict;
    $('#reference-label').classList.add('hidden');
    $('#show-reference').classList.remove('hidden');
    $('#mode-badge').textContent = 'SAVED DEMO · NO API';
    isSavedExample = true;
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
    const result = await requestJson('/api/baseline', { case: currentCase() });
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
    const preflight = await requestJson('/api/preflight', { case: caseData });
    const approved = window.confirm(
      `This AI review sends two requests to ${preflight.model}. The conservative cost estimate is up to US$${preflight.conservative_cost_upper_bound_usd.toFixed(4)} for this script (the provider's actual charge may differ). Proceed?`
    );
    if (!approved) return;
    $('#ai-button').disabled = true;
    $('#ai-button').textContent = 'Reviewing…';
    const result = await requestJson('/api/review', { case: caseData, confirm_paid_run: true });
    setVerdict('ai', result.ai.verdict, `${result.ai.model} · est. $${result.ai.estimated_cost_usd.toFixed(4)}`);
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
  if (!isSavedExample) return;
  isSavedExample = false;
  savedReference = null;
  $('#show-reference').classList.add('hidden');
  $('#reference-label').classList.add('hidden');
  setVerdict('baseline', '—', 'Run the keyword check to review this draft.');
  renderFindings('baseline', []);
  setVerdict('ai', '—', 'Request an AI review after checking its cost estimate.');
  renderFindings('ai', []);
  $('#mode-badge').textContent = 'UNSAVED DRAFT';
}

$('#load-sample').addEventListener('click', loadSample);
$('#load-sample-nav').addEventListener('click', loadSample);
$('#baseline-button').addEventListener('click', runBaseline);
$('#ai-button').addEventListener('click', runAI);
$('#show-reference').addEventListener('click', showReference);
$('#show-limits').addEventListener('click', () => toast('30 synthetic extension cases; revised prompt; development evidence only.'));
$('#record-decision').addEventListener('click', () => {
  if (!$('#reviewer-decision').value) return toast('Choose a human disposition first.');
  toast('Decision noted for this session only; it is not saved or sent.');
});
Object.values(ids).forEach((element) => element.addEventListener('input', markDraftChanged));
Object.values(ids).forEach((element) => element.addEventListener('change', markDraftChanged));
loadSample();
