/**
 * Snippet Name: SaaS Dashboard
 * Description: Data layer, polished SVG charts, metric sparklines, table sort/paginate/filter, activity, theme, and sidebar for the Vanilla SaaS Dashboard.
 * Author: DevSnips Contributors
 * Usage Example: include this script at the end of the dashboard body (inline or via a script src).
 *
 * Data abstraction: all demo data lives in the DASHBOARD object below. Replace the
 * DASHBOARD fields (or fetch them from your API and assign before init()) to wire
 * the template to a real backend — the render functions read from DASHBOARD only.
 */
(function () {
  'use strict';

  var root = document.documentElement;
  var app = document.querySelector('[data-app]');

  /* =====================================================================
     DATA LAYER  — replace these fields with real API responses.
  ===================================================================== */
  var DASHBOARD = {
    workspace: { name: 'Northstar', plan: 'Scale', owner: 'Alex Morgan', initials: 'AM' },
    kpis: {
      mrr: { value: 284920, prefix: '$', delta: 12.4, spark: [248, 252, 251, 258, 263, 269, 271, 278, 281, 285] },
      customers: { value: 12482, delta: 8.1, spark: [11200, 11420, 11610, 11780, 11920, 12010, 12110, 12240, 12360, 12482] },
      conversion: { value: 8.42, suffix: '%', delta: 1.3, deltaDown: true, spark: [8.1, 8.2, 8.05, 8.3, 8.5, 8.4, 8.35, 8.45, 8.4, 8.42] },
      arpu: { value: 22.81, prefix: '$', delta: 3.7, spark: [21.4, 21.6, 21.8, 22.0, 22.1, 22.3, 22.4, 22.5, 22.7, 22.81] }
    },
    revenue: {
      '7d': { labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], current: [38200, 42100, 39800, 47600, 52300, 45100, 54800], previous: [35100, 38900, 37200, 43100, 47600, 41800, 50200] },
      '30d': { labels: ['W1', 'W2', 'W3', 'W4'], current: [248000, 271000, 263000, 285000], previous: [221000, 244000, 239000, 258000] },
      '12m': { labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], current: [182000, 196000, 211000, 198000, 224000, 246000, 258000, 251000, 272000, 289000, 312000, 331000], previous: [156000, 168000, 182000, 171000, 194000, 212000, 224000, 218000, 236000, 251000, 272000, 289000] }
    },
    plans: [
      { name: 'Scale', customers: 1284, share: 0.41, mrr: 116200, color: '#4f46e5' },
      { name: 'Growth', customers: 3420, share: 0.31, mrr: 68400, color: '#0ea5e9' },
      { name: 'Starter', customers: 5680, share: 0.18, mrr: 28400, color: '#10b981' },
      { name: 'Trial', customers: 2098, share: 0.10, mrr: 0, color: '#94a3b8' }
    ],
    activity: [
      { who: 'Maya Andersson', initials: 'MA', tone: '#4f46e5', action: 'upgraded to', target: 'Scale', time: '2m ago', status: 'success' },
      { who: 'Priya Raman', initials: 'PR', tone: '#10b981', action: 'paid invoice', target: '#INV-2043 · $240.00', time: '14m ago', status: 'success' },
      { who: 'Jonas Lee', initials: 'JL', tone: '#0ea5e9', action: 'invited 3 members to', target: 'Bright Labs', time: '38m ago', status: 'info' },
      { who: 'Diego Costa', initials: 'DC', tone: '#f59e0b', action: 'started a 14-day trial of', target: 'Growth', time: '1h ago', status: 'info' },
      { who: 'Sara Yilmaz', initials: 'SY', tone: '#8b5cf6', action: 'exported the', target: 'Revenue report', time: '2h ago', status: 'neutral' },
      { who: 'Theo Faroe', initials: 'TF', tone: '#ef4444', action: 'cancelled the', target: 'Growth plan', time: '3h ago', status: 'danger' },
      { who: 'Ava Nilsson', initials: 'AN', tone: '#4f46e5', action: 'added a card on file to', target: 'billing', time: '5h ago', status: 'success' }
    ],
    transactions: [
      { id: 'INV-2043', name: 'Priya Raman', company: 'Kepler Co.', amount: 240.00, status: 'paid', date: 'Aug 11' },
      { id: 'INV-2042', name: 'Maya Andersson', company: 'Northwind', amount: 840.00, status: 'paid', date: 'Aug 11' },
      { id: 'INV-2041', name: 'Jonas Lee', company: 'Bright Labs', amount: 240.00, status: 'pending', date: 'Aug 10' },
      { id: 'INV-2040', name: 'Sara Yilmaz', company: 'Altapine', amount: 840.00, status: 'paid', date: 'Aug 10' },
      { id: 'INV-2039', name: 'Theo Faroe', company: 'Summit App', amount: 240.00, status: 'failed', date: 'Aug 9' },
      { id: 'INV-2038', name: 'Ava Nilsson', company: 'Vantage', amount: 1160.00, status: 'paid', date: 'Aug 9' }
    ],
    customers: [
      { name: 'Maya Andersson', email: 'maya@northwind.io', initials: 'MA', tone: '#4f46e5', plan: 'Scale', status: 'active', mrr: 840, last: '2 min ago' },
      { name: 'Priya Raman', email: 'priya@keplerco.com', initials: 'PR', tone: '#10b981', plan: 'Scale', status: 'active', mrr: 840, last: '14 min ago' },
      { name: 'Jonas Lee', email: 'jonas@brightlabs.dev', initials: 'JL', tone: '#0ea5e9', plan: 'Growth', status: 'trial', mrr: 240, last: '38 min ago' },
      { name: 'Sara Yilmaz', email: 'sara@altapine.co', initials: 'SY', tone: '#8b5cf6', plan: 'Scale', status: 'active', mrr: 840, last: '2 hours ago' },
      { name: 'Diego Costa', email: 'diego@summit.app', initials: 'DC', tone: '#f59e0b', plan: 'Starter', status: 'trial', mrr: 49, last: '4 hours ago' },
      { name: 'Ava Nilsson', email: 'ava@vantage.io', initials: 'AN', tone: '#4f46e5', plan: 'Scale', status: 'active', mrr: 1160, last: '5 hours ago' },
      { name: 'Theo Faroe', email: 'theo@altapine.co', initials: 'TF', tone: '#ef4444', plan: 'Growth', status: 'pastdue', mrr: 240, last: '1 day ago' },
      { name: 'Liam Chen', email: 'liam@orbit.dev', initials: 'LC', tone: '#0ea5e9', plan: 'Growth', status: 'active', mrr: 240, last: '1 day ago' },
      { name: 'Noor Aziz', email: 'noor@meridian.co', initials: 'NA', tone: '#10b981', plan: 'Scale', status: 'active', mrr: 840, last: '2 days ago' },
      { name: 'Elena Vasquez', email: 'elena@helix.io', initials: 'EV', tone: '#8b5cf6', plan: 'Starter', status: 'active', mrr: 49, last: '2 days ago' },
      { name: 'Marcus Webb', email: 'marcus@vertex.app', initials: 'MW', tone: '#f59e0b', plan: 'Trial', status: 'trial', mrr: 0, last: '3 days ago' },
      { name: 'Yuki Tanaka', email: 'yuki@lumen.dev', initials: 'YT', tone: '#4f46e5', plan: 'Growth', status: 'active', mrr: 240, last: '3 days ago' }
    ],
    usage: { seats: 18, seatsMax: 25, apiCalls: 482300, apiMax: 1000000, storage: 184, storageMax: 500 }
  };
  window.DASHBOARD = DASHBOARD;

  /* =====================================================================
     THEME
  ===================================================================== */
  function applyTheme(dark) {
    root.dataset.theme = dark ? 'dark' : 'light';
    var t = document.querySelector('.theme-toggle');
    if (t) t.setAttribute('aria-pressed', String(dark));
    try { localStorage.setItem('ns-theme', dark ? 'dark' : 'light'); } catch (e) {}
    redrawCharts();
  }
  function storedTheme() {
    try { var v = localStorage.getItem('ns-theme'); if (v) return v === 'dark'; } catch (e) {}
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  }
  var themeBtn = document.querySelector('.theme-toggle');
  if (themeBtn) themeBtn.addEventListener('click', function () { applyTheme(root.dataset.theme !== 'dark'); });

  /* =====================================================================
     SIDEBAR (mobile drawer)
  ===================================================================== */
  var menuBtn = document.querySelector('.menu-btn');
  function closeSidebar() { app.classList.remove('sidebar-open'); if (menuBtn) menuBtn.setAttribute('aria-expanded', 'false'); }
  if (menuBtn) {
    menuBtn.addEventListener('click', function () {
      var open = app.classList.toggle('sidebar-open');
      menuBtn.setAttribute('aria-expanded', String(open));
    });
    var backdrop = app.querySelector('.backdrop');
    if (backdrop) backdrop.addEventListener('click', closeSidebar);
  }
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && app.classList.contains('sidebar-open')) closeSidebar();
  });

  /* =====================================================================
     HELPERS
  ===================================================================== */
  function fmt(n, prefix, suffix, decimals) {
    var d = decimals == null ? (n % 1 === 0 ? 0 : 2) : decimals;
    var s = n.toLocaleString('en-US', { minimumFractionDigits: d, maximumFractionDigits: d });
    return (prefix || '') + s + (suffix || '');
  }
  function compact(n) {
    if (n >= 1000000) return (n / 1000000).toFixed(n % 1000000 === 0 ? 0 : 1) + 'M';
    if (n >= 1000) return (n / 1000).toFixed(n % 1000 === 0 ? 0 : 1) + 'k';
    return String(Math.round(n));
  }
  function money(n) { return '$' + n.toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 0 }); }
  function cssVar(name) { return getComputedStyle(root).getPropertyValue(name).trim(); }

  /* =====================================================================
     NUMBER COUNT-UP
  ===================================================================== */
  function animateNumber(el) {
    var target = parseFloat(el.dataset.value);
    var prefix = el.dataset.prefix || '';
    var suffix = el.dataset.suffix || '';
    var dec = parseInt(el.dataset.decimals || '0', 10);
    var dur = 800;
    var start = null;
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduce) { el.textContent = fmt(target, prefix, suffix, dec); return; }
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = fmt(target * eased, prefix, suffix, dec);
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  /* =====================================================================
     SPARKLINES
  ===================================================================== */
  function sparkPath(values, w, h, pad) {
    pad = pad || 2;
    var min = Math.min.apply(null, values);
    var max = Math.max.apply(null, values);
    var span = Math.max(1e-9, max - min);
    var stepX = (w - pad * 2) / Math.max(1, values.length - 1);
    return values.map(function (v, i) {
      return (i === 0 ? 'M' : 'L') + (pad + i * stepX).toFixed(1) + ' ' + (h - pad - ((v - min) / span) * (h - pad * 2)).toFixed(1);
    }).join(' ');
  }
  function renderSparklines() {
    var success = cssVar('--ds-success') || '#10b981';
    var danger = cssVar('--ds-danger') || '#ef4444';
    document.querySelectorAll('[data-spark]').forEach(function (el) {
      var key = el.dataset.spark;
      var k = DASHBOARD.kpis[key];
      if (!k) return;
      var w = 120, h = 36;
      var line = sparkPath(k.spark, w, h, 3);
      var area = line + ' L ' + (w - 3) + ' ' + h + ' L 3 ' + h + ' Z';
      var col = k.deltaDown ? danger : success;
      var gid = 'sp-' + key;
      el.innerHTML =
        '<svg viewBox="0 0 ' + w + ' ' + h + '" preserveAspectRatio="none" role="img" aria-label="' + key + ' trend">' +
        '<defs><linearGradient id="' + gid + '" x1="0" y1="0" x2="0" y2="1">' +
        '<stop offset="0" stop-color="' + col + '" stop-opacity="0.22"/>' +
        '<stop offset="1" stop-color="' + col + '" stop-opacity="0"/>' +
        '</linearGradient></defs>' +
        '<path d="' + area + '" fill="url(#' + gid + ')"/>' +
        '<path d="' + line + '" fill="none" stroke="' + col + '" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>' +
        '</svg>';
    });
  }

  /* =====================================================================
     REVENUE CHART
  ===================================================================== */
  var chartSvg = document.getElementById('chart');
  var periodSeg = document.querySelector('[data-period]');
  var current = '30d';

  function fmtAxis(n) { return n >= 1000 ? '$' + compact(n) : '$' + Math.round(n); }
  function niceBounds(min, max) {
    var range = max - min || max || 1;
    var raw = range * 0.15;
    var mag = Math.pow(10, Math.floor(Math.log10(raw)));
    var nice = Math.ceil(raw / mag) * mag;
    return { lo: Math.max(0, min - nice), hi: max + nice };
  }

  function drawRevenueChart(key) {
    if (!chartSvg) return;
    var d = DASHBOARD.revenue[key];
    var W = 980, H = 320;
    var mL = 52, mR = 16, mT = 16, mB = 34;
    var innerW = W - mL - mR;
    var innerH = H - mT - mB;
    var n = d.labels.length;
    var all = d.current.concat(d.previous);
    var b = niceBounds(Math.min.apply(null, all), Math.max.apply(null, all));
    var stepX = innerW / Math.max(1, n - 1);

    function toPts(arr) {
      return arr.map(function (v, i) {
        return { x: mL + i * stepX, y: mT + (1 - (v - b.lo) / (b.hi - b.lo)) * innerH, v: v };
      });
    }
    var cur = toPts(d.current);
    var prev = toPts(d.previous);
    function lineOf(pts) { return pts.map(function (p, i) { return (i === 0 ? 'M' : 'L') + p.x.toFixed(1) + ' ' + p.y.toFixed(1); }).join(' '); }
    var curLine = lineOf(cur);
    var curArea = curLine + ' L ' + cur[cur.length - 1].x.toFixed(1) + ' ' + (mT + innerH) + ' L ' + cur[0].x.toFixed(1) + ' ' + (mT + innerH) + ' Z';

    var grid = '';
    var steps = 4;
    for (var g = 0; g <= steps; g++) {
      var gy = mT + (g / steps) * innerH;
      var gv = b.hi - (g / steps) * (b.hi - b.lo);
      grid += '<line x1="' + mL + '" y1="' + gy.toFixed(1) + '" x2="' + (W - mR) + '" y2="' + gy.toFixed(1) + '" class="g-grid"/>';
      grid += '<text x="' + (mL - 10) + '" y="' + (gy + 3.5).toFixed(1) + '" text-anchor="end" class="g-axis">' + fmtAxis(gv) + '</text>';
    }
    var xlabels = d.labels.map(function (l, i) {
      return '<text x="' + cur[i].x.toFixed(1) + '" y="' + (H - 12) + '" text-anchor="middle" class="g-axis">' + l + '</text>';
    }).join('');

    var accent = cssVar('--ds-accent') || '#4f46e5';
    var faint = cssVar('--ds-faint') || '#94a3b8';

    chartSvg.innerHTML =
      '<defs>' +
        '<linearGradient id="rev-area" x1="0" y1="0" x2="0" y2="1">' +
          '<stop offset="0" stop-color="' + accent + '" stop-opacity="0.18"/>' +
          '<stop offset="1" stop-color="' + accent + '" stop-opacity="0"/>' +
        '</linearGradient>' +
      '</defs>' +
      grid +
      '<path d="' + lineOf(prev) + '" fill="none" stroke="' + faint + '" stroke-width="1.5" stroke-dasharray="4 4" class="g-prev" opacity="0.7"/>' +
      '<path d="' + curArea + '" fill="url(#rev-area)"/>' +
      '<path d="' + curLine + '" fill="none" stroke="' + accent + '" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" class="g-line"/>' +
      cur.map(function (p) { return '<circle cx="' + p.x.toFixed(1) + '" cy="' + p.y.toFixed(1) + '" r="3.2" class="g-pt"/>'; }).join('') +
      xlabels +
      '<line id="hair" x1="0" y1="' + mT + '" x2="0" y2="' + (mT + innerH) + '" class="g-hair" opacity="0"/>' +
      '<g id="tip" opacity="0"><rect x="0" y="0" width="132" height="58" rx="8" class="g-tip-bg"/><text id="tip-label" x="12" y="20" class="g-tip-label"></text><text id="tip-cur" x="12" y="40" class="g-tip-cur"></text><text id="tip-prev" x="12" y="54" class="g-tip-prev"></text></g>' +
      '<rect id="overlay" x="0" y="0" width="' + W + '" height="' + H + '" fill="transparent"/>';

    wireChartTooltip(cur, d.labels, d.current, d.previous, mL, W);
  }

  function wireChartTooltip(cur, labels, curVals, prevVals, mL, W) {
    var overlay = chartSvg.querySelector('#overlay');
    var hair = chartSvg.querySelector('#hair');
    var tip = chartSvg.querySelector('#tip');
    var tipLabel = chartSvg.querySelector('#tip-label');
    var tipCur = chartSvg.querySelector('#tip-cur');
    var tipPrev = chartSvg.querySelector('#tip-prev');
    var mR = 16, innerW = W - mL - mR;
    var stepX = innerW / Math.max(1, cur.length - 1);

    function move(clientX) {
      var rect = chartSvg.getBoundingClientRect();
      var relX = ((clientX - rect.left) / rect.width) * W;
      var i = Math.round((relX - mL) / stepX);
      i = Math.max(0, Math.min(cur.length - 1, i));
      var p = cur[i];
      hair.setAttribute('x1', p.x); hair.setAttribute('x2', p.x); hair.setAttribute('opacity', '1');
      var tx = Math.min(W - 140, Math.max(8, p.x - 66));
      tip.setAttribute('transform', 'translate(' + tx + ',' + (p.y - 70) + ')');
      tip.setAttribute('opacity', '1');
      tipLabel.textContent = labels[i];
      tipCur.textContent = 'This period  ' + money(curVals[i]);
      tipPrev.textContent = 'Last period  ' + money(prevVals[i]);
    }
    overlay.addEventListener('mousemove', function (e) { move(e.clientX); });
    overlay.addEventListener('mouseleave', function () { hair.setAttribute('opacity', '0'); tip.setAttribute('opacity', '0'); });
    overlay.addEventListener('touchmove', function (e) { if (e.touches[0]) move(e.touches[0].clientX); }, { passive: true });
  }

  if (periodSeg) {
    periodSeg.addEventListener('click', function (e) {
      var btn = e.target.closest('button[data-range]');
      if (!btn) return;
      current = btn.dataset.range;
      periodSeg.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-pressed', String(b === btn)); });
      drawRevenueChart(current);
    });
  }

  /* =====================================================================
     PLAN BREAKDOWN
  ===================================================================== */
  function renderPlanBreakdown() {
    var host = document.getElementById('plans-bar');
    if (!host) return;
    var plans = DASHBOARD.plans;
    var segs = plans.map(function (p) {
      return '<div class="seg-piece" style="flex:' + p.share + ';background:' + p.color + '" title="' + p.name + ': ' + Math.round(p.share * 100) + '%"></div>';
    }).join('');
    var legend = plans.map(function (p) {
      return '<li><span class="sw" style="background:' + p.color + '"></span><span class="nm">' + p.name + '</span><span class="ct">' + p.customers.toLocaleString() + '</span><span class="mr">' + (p.mrr ? money(p.mrr) : '—') + '</span></li>';
    }).join('');
    host.innerHTML = '<div class="stack-bar">' + segs + '</div><ul class="plan-legend">' + legend + '</ul>';
  }

  /* =====================================================================
     ACTIVITY TIMELINE
  ===================================================================== */
  function renderActivity() {
    var host = document.getElementById('activity');
    if (!host) return;
    host.innerHTML = DASHBOARD.activity.map(function (a, i) {
      var last = i === DASHBOARD.activity.length - 1;
      return '<li class="' + (last ? 'last' : '') + '">' +
        '<span class="pic" style="background:' + a.tone + '">' + a.initials + '</span>' +
        '<div class="track">' +
        '<p class="ev"><strong>' + a.who + '</strong> ' + a.action + ' <span class="tgt">' + a.target + '</span></p>' +
        '<p class="mt"><span class="dot ' + a.status + '"></span>' + a.time + '</p>' +
        '</div></li>';
    }).join('');
  }

  /* =====================================================================
     TRANSACTIONS LIST
  ===================================================================== */
  function renderTransactions() {
    var host = document.getElementById('transactions');
    if (!host) return;
    host.innerHTML = DASHBOARD.transactions.map(function (t) {
      return '<li>' +
        '<div class="tx-main"><span class="tx-id mono">' + t.id + '</span><span class="tx-name">' + t.name + ' · ' + t.company + '</span></div>' +
        '<div class="tx-right"><span class="tx-amt mono">' + money(t.amount) + '</span><span class="pill ' + t.status + '">' + t.status + '</span></div>' +
        '</li>';
    }).join('');
  }

  /* =====================================================================
     USAGE BARS
  ===================================================================== */
  function renderUsage() {
    var host = document.getElementById('usage');
    if (!host) return;
    var u = DASHBOARD.usage;
    var rows = [
      { label: 'Seats', val: u.seats + ' / ' + u.seatsMax, pct: (u.seats / u.seatsMax) * 100 },
      { label: 'API calls', val: compact(u.apiCalls) + ' / ' + compact(u.apiMax), pct: (u.apiCalls / u.apiMax) * 100 },
      { label: 'Storage (GB)', val: u.storage + ' / ' + u.storageMax, pct: (u.storage / u.storageMax) * 100 }
    ];
    host.innerHTML = rows.map(function (r) {
      return '<div class="usage-row"><div class="usage-head"><span>' + r.label + '</span><span class="mono">' + r.val + '</span></div>' +
        '<div class="bar"><div class="fill" style="width:' + r.pct.toFixed(1) + '%"></div></div></div>';
    }).join('');
  }

  /* =====================================================================
     CUSTOMERS TABLE
  ===================================================================== */
  var tableState = { sort: 'mrr', dir: -1, page: 1, perPage: 6, filter: '' };
  function statusLabel(s) { return { active: 'Active', trial: 'Trial', pastdue: 'Past due' }[s] || s; }
  function planSortVal(p) { return { Scale: 4, Growth: 3, Starter: 2, Trial: 1 }[p] || 0; }

  function filteredCustomers() {
    var f = tableState.filter.toLowerCase();
    return DASHBOARD.customers.filter(function (c) {
      return !f || c.name.toLowerCase().indexOf(f) > -1 || c.email.toLowerCase().indexOf(f) > -1 || c.plan.toLowerCase().indexOf(f) > -1;
    });
  }
  function sortedCustomers() {
    var rows = filteredCustomers().slice();
    var k = tableState.sort, dir = tableState.dir;
    rows.sort(function (a, b) {
      var av = k === 'plan' ? planSortVal(a.plan) : k === 'name' ? a.name : k === 'mrr' ? a.mrr : a.last;
      var bv = k === 'plan' ? planSortVal(b.plan) : k === 'name' ? b.name : k === 'mrr' ? b.mrr : b.last;
      if (av < bv) return -1 * dir;
      if (av > bv) return 1 * dir;
      return 0;
    });
    return rows;
  }
  function renderTable() {
    var tbody = document.getElementById('cust-rows');
    var rows = sortedCustomers();
    var start = (tableState.page - 1) * tableState.perPage;
    var page = rows.slice(start, start + tableState.perPage);
    tbody.innerHTML = page.map(function (c) {
      return '<tr>' +
        '<td data-label="Customer"><div class="cust"><span class="pic" style="background:' + c.tone + '">' + c.initials + '</span>' +
        '<div class="meta"><div class="nm">' + c.name + '</div><div class="em">' + c.email + '</div></div></div></td>' +
        '<td data-label="Plan" class="plan-cell">' + c.plan + '</td>' +
        '<td data-label="Status"><span class="pill ' + c.status + '">' + statusLabel(c.status) + '</span></td>' +
        '<td data-label="MRR" class="amount mono">' + money(c.mrr) + '</td>' +
        '<td data-label="Last active" class="muted">' + c.last + '</td>' +
        '<td data-label="Actions" class="row-acts"><button class="row-act" data-action="view" aria-label="View ' + c.name + '">' + ICONS.eye + '</button>' +
        '<button class="row-act" data-action="delete" aria-label="Remove ' + c.name + '">' + ICONS.trash + '</button></td>' +
        '</tr>';
    }).join('') || '<tr><td colspan="6" class="empty-row">No customers match your filter.</td></tr>';

    document.querySelectorAll('[data-sort]').forEach(function (th) {
      var active = th.dataset.sort === tableState.sort;
      th.setAttribute('aria-sort', active ? (tableState.dir === 1 ? 'ascending' : 'descending') : 'none');
      th.classList.toggle('is-sorted', active);
    });
    renderPagination(rows.length);
  }
  function renderPagination(total) {
    var host = document.getElementById('pagination');
    if (!host) return;
    var pages = Math.max(1, Math.ceil(total / tableState.perPage));
    if (tableState.page > pages) tableState.page = 1;
    var btns = '';
    for (var i = 1; i <= pages; i++) {
      btns += '<button class="page' + (i === tableState.page ? ' is-current' : '') + '" data-page="' + i + '" aria-label="Page ' + i + '"' + (i === tableState.page ? ' aria-current="page"' : '') + '>' + i + '</button>';
    }
    var from = total === 0 ? 0 : (tableState.page - 1) * tableState.perPage + 1;
    var to = Math.min(total, tableState.page * tableState.perPage);
    host.innerHTML = '<span class="page-info">' + from + '–' + to + ' of ' + total + '</span><div class="page-btns">' + btns + '</div>';
  }
  function wireTable() {
    var thead = document.querySelector('[data-thead]');
    if (thead) {
      thead.addEventListener('click', function (e) {
        var th = e.target.closest('[data-sort]');
        if (!th) return;
        var k = th.dataset.sort;
        if (tableState.sort === k) tableState.dir *= -1;
        else { tableState.sort = k; tableState.dir = (k === 'name') ? 1 : -1; }
        tableState.page = 1;
        renderTable();
      });
    }
    var pag = document.getElementById('pagination');
    if (pag) pag.addEventListener('click', function (e) {
      var b = e.target.closest('[data-page]');
      if (!b) return;
      tableState.page = parseInt(b.dataset.page, 10);
      renderTable();
    });
    var filter = document.getElementById('cust-filter');
    if (filter) filter.addEventListener('input', function () {
      tableState.filter = filter.value; tableState.page = 1; renderTable();
    });
    var tbody = document.getElementById('cust-rows');
    if (tbody) tbody.addEventListener('click', function (e) {
      var btn = e.target.closest('.row-act');
      if (!btn) return;
      var row = btn.closest('tr');
      var name = row.querySelector('.nm') ? row.querySelector('.nm').textContent : 'row';
      var action = btn.dataset.action;
      if (action === 'delete') {
        row.style.transition = 'opacity .16s, transform .16s';
        row.style.opacity = '0'; row.style.transform = 'translateX(-6px)';
        setTimeout(function () { row.remove(); showToast('Removed ' + name); }, 160);
      } else { showToast('Opening ' + name); }
    });
  }

  /* =====================================================================
     TOAST + buttons
  ===================================================================== */
  var TOAST = document.getElementById('toast');
  function showToast(msg) {
    if (!TOAST) return;
    TOAST.textContent = msg;
    TOAST.classList.add('show');
    clearTimeout(showToast._t);
    showToast._t = setTimeout(function () { TOAST.classList.remove('show'); }, 2400);
  }
  document.querySelectorAll('[data-action="upgrade"], .page-actions .btn, .header-actions .icon-btn[data-toast]').forEach(function (b) {
    b.addEventListener('click', function () { showToast(b.dataset.toast || (b.textContent.trim() || 'Action')); });
  });

  /* ICONS (inline svg strings) */
  var ICONS = {
    eye: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>',
    trash: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>'
  };

  /* REDRAW */
  function redrawCharts() { drawRevenueChart(current); renderSparklines(); }
  var resizeT = null;
  window.addEventListener('resize', function () {
    clearTimeout(resizeT);
    resizeT = setTimeout(redrawCharts, 120);
  });

  /* INIT */
  function init() {
    applyTheme(storedTheme());
    document.querySelectorAll('[data-countup]').forEach(animateNumber);
    renderSparklines();
    drawRevenueChart(current);
    renderPlanBreakdown();
    renderActivity();
    renderTransactions();
    renderUsage();
    renderTable();
    wireTable();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
