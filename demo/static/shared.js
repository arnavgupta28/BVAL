// BVAL demo: shared shapes and helpers. Everything here builds markup from numbers or escaped text only.
const TONE = { accept: 'g', counter: 'y', decline: 'p', quote: 'b' };
const LABEL = { accept: 'Accept', counter: 'Counter', decline: 'Decline or cut scope', quote: 'Your quote' };

function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

function burst(spikes = 12, inner = 7, outline = false) {
  const pts = [];
  for (let i = 0; i < spikes * 2; i++) {
    const r = i % 2 ? inner : 48, a = Math.PI * i / spikes - Math.PI / 2;
    pts.push(`${(50 + r * Math.cos(a)).toFixed(1)},${(50 + r * Math.sin(a)).toFixed(1)}`);
  }
  const paint = outline ? 'fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"' : 'fill="currentColor"';
  return `<svg class="burst" viewBox="0 0 100 100" aria-hidden="true"><polygon points="${pts.join(' ')}" ${paint}/></svg>`;
}

function sparkle() {
  return '<svg class="burst" viewBox="0 0 40 40" aria-hidden="true"><path d="M20 0C21 13 27 19 40 20C27 21 21 27 20 40C19 27 13 21 0 20C13 19 19 13 20 0Z" fill="currentColor"/></svg>';
}

const STATUS_BAR = `<div class="status" aria-hidden="true"><span>9:41</span><span class="island"></span>
<svg width="66" height="14" viewBox="0 0 66 14"><g fill="currentColor"><rect x="0" y="9" width="3" height="5" rx="1"/><rect x="5" y="6" width="3" height="8" rx="1"/>
<rect x="10" y="3" width="3" height="11" rx="1"/><rect x="15" y="0" width="3" height="14" rx="1"/>
<path d="M30 4a9 9 0 0 1 12 0l-1.6 1.7a6.6 6.6 0 0 0-8.8 0zM32.6 7a5.4 5.4 0 0 1 6.8 0L36 10.6z"/>
<rect x="44" y="1.5" width="19" height="11" rx="3.5" fill="none" stroke="currentColor" stroke-width="1.4" opacity=".5"/><rect x="46" y="3.5" width="13" height="7" rx="2"/></g></svg></div>`;

document.querySelectorAll('[data-status]').forEach(el => { el.outerHTML = STATUS_BAR; });

// The full report opens inside the phone, over the current screen.
function openReport(runId, title = 'Deal report') {
  const ov = document.getElementById('overlay');
  ov.querySelector('.title').textContent = title;
  ov.querySelector('iframe').src = `/report/${encodeURIComponent(runId)}`;
  ov.classList.add('open');
}
function closeReport() {
  const ov = document.getElementById('overlay');
  ov.classList.remove('open');
  ov.querySelector('iframe').src = 'about:blank';
}

// Compact verdict card from a BVAL dataset item: used by both pages.
function verdictCard(item, runId) {
  const tone = TONE[item.nextAction] || 'b';
  const p = item.priceRange || {};
  const tile = (cls, name, v) => `<div class="mini ${cls}"><span class="chip">${name}</span><b class="d">${esc(v)}</b></div>`;
  const rs = item.counterOptions && item.counterOptions.reducedScope;
  return `<div class="card bright ${tone} rise verdict">
    <div class="vb">${burst()}</div>
    <div class="d vt">${esc(LABEL[item.nextAction] || item.verdict)}</div>
    <p class="vs">${esc(item.summary || '')}</p>
    ${item.offerDisplay ? `<span class="chip">Brand offer <b>${esc(item.offerDisplay)}</b></span>` : ''}
  </div>
  <div class="minis rise">${tile('p', 'Walk-away', p.walkAway)}${tile('l', 'Floor', p.floor)}${tile('g', 'Fair', p.fair)}${tile('b', 'Ask', p.ask)}</div>
  ${rs ? `<div class="card glass rise"><div class="d" style="font-size:14px">Or a lighter version</div><p style="margin:6px 0 0"><b>${esc(rs.price)}</b> <span class="muted">drops ${esc((rs.dropped || []).join(', ').replace(/_/g, ' '))}</span></p></div>` : ''}
  <button class="btn block rise" style="margin-top:12px" onclick="openReport('${esc(runId)}')">Open the full report <span class="arrow">&rarr;</span></button>`;
}
