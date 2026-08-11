/**
 * Snippet Name: SaaS Dashboard
 * Description: Charts, theme toggle, sidebar nav, period filter, and table actions for the Vanilla SaaS Dashboard.
 * Author: DevSnips Contributors
 * Usage Example: <script src="js/dashboard.js" defer></script> at the end of <body>.
 */
(function () {
  'use strict';

  var root = document.documentElement;
  var app = document.querySelector('[data-app]');

  /* ---- Demo data -------------------------------------------------------- */
  var series = {
    '7d': {
      labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      revenue: [4200, 5100, 4800, 6400, 7200, 6100, 7800],
      orders: [120, 148, 139, 188, 210, 176, 229]
    },
    '30d': {
      labels: ['W1', 'W2', 'W3', 'W4'],
      revenue: [28000, 32400, 30100, 38900],
      orders: [820, 945, 880, 1140]
    },
    '12m': {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
      revenue: [82000, 88000, 94000, 86000, 102000, 118000, 126000, 121000, 134000, 142000, 158000, 171000],
      orders: [2400, 2580, 2760, 2510, 2980, 3460, 3690, 3540, 3920, 4150, 4620, 5010]
    }
  };

  var ACTIVITY = [
    { who: 'MA', tone: '#6366f1', text: '<strong>Maya Andersson</strong> upgraded to <span class="tgt">Scale</span>', time: '2m ago' },
    { who: 'JL', tone: '#8b5cf6', text: '<strong>Jonas Lee</strong> invited 3 members to the workspace', time: '18m ago' },
    { who: 'PR', tone: '#10b981', text: '<strong>Priya Raman</strong> paid invoice <span class="tgt">#INV-2043</span> ($240.00)', time: '41m ago' },
    { who: 'DC', tone: '#f59e0b', text: '<strong>Diego Costa</strong> started a 14-day trial', time: '1h ago' },
    { who: 'SY', tone: '#0ea5e9', text: '<strong>Sara Yilmaz</strong> exported the revenue report', time: '2h ago' },
    { who: 'TF', tone: '#ef4444', text: '<strong>Theo Faroe</strong> cancelled the <span class="tgt">Growth</span> plan', time: '3h ago' },
    { who: 'AN', tone: '#6366f1', text: '<strong>Ava Nilsson</strong> added a card on file', time: '5h ago' }
  ];

  var TOAST = document.getElementById('toast');

  /* ---- Theme ----------------------------------------------------------- */
  function applyTheme(dark) {
    root.dataset.theme = dark ? 'dark' : 'light';
    var t = document.querySelector('.theme-toggle');
    if (t) t.setAttribute('aria-pressed', String(dark));
    try { localStorage.setItem('ns-theme', dark ? 'dark' : 'light'); } catch (e) {}
  }
  function storedTheme() {
    try { var v = localStorage.getItem('ns-theme'); if (v) return v === 'dark'; } catch (e) {}
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  }
  applyTheme(storedTheme());
  var themeBtn = document.querySelector('.theme-toggle');
  if (themeBtn) themeBtn.addEventListener('click', function () { applyTheme(root.dataset.theme !== 'dark'); });

  /* ---- Sidebar (mobile) ----------------------------------------------- */
  var menuBtn = document.querySelector('.menu-btn');
  function closeSidebar() { app.classList.remove('sidebar-open'); }
  if (menuBtn) {
    menuBtn.addEventListener('click', function () { app.classList.toggle('sidebar-open'); });
    var backdrop = app.querySelector('.backdrop');
    if (backdrop) backdrop.addEventListener('click', closeSidebar);
  }
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && app.classList.contains('sidebar-open')) closeSidebar();
  });

  /* ---- Number count-up ------------------------------------------------- */
  function animateNumber(el) {
    var target = parseFloat(el.dataset.value);
    var prefix = el.dataset.prefix || '';
    var suffix = el.dataset.suffix || '';
    var dec = parseInt(el.dataset.decimals || '0', 10);
    var dur = 900;
    var start = null;
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduce) { el.textContent = prefix + target.toFixed(dec) + suffix; return; }
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = prefix + (target * eased).toFixed(dec) + suffix;
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  /* ---- Line chart ------------------------------------------------------ */
  var chartSvg = document.getElementById('chart');
  var periodSeg = document.querySelector('[data-period]');
  var current = '30d';

  function fmtNum(n) {
    if (n >= 1000) return (n / 1000).toFixed(n >= 10000 ? 0 : 1) + 'k';
    return String(n);
  }

  function drawChart(key) {
    if (!chartSvg) return;
    var d = series[key];
    var W = 1000, H = 320, padX = 48, padY = 24;
    var innerW = W - padX * 2;
    var innerH = H - padY * 2 - 30;

    var max = Math.max.apply(null, d.revenue);
    var min = Math.min.apply(null, d.revenue);
    var span = Math.max(1, max - min);
    var stepX = innerW / Math.max(1, d.labels.length - 1);

    var pts = d.revenue.map(function (v, i) {
      return { x: padX + i * stepX, y: padY + (1 - (v - min) / span) * innerH + 10, v: v };
    });

    var line = pts.map(function (p, i) { return (i === 0 ? 'M' : 'L') + p.x + ' ' + p.y; }).join(' ');
    var area = line +
      ' L ' + pts[pts.length - 1].x + ' ' + (padY + innerH + 10) +
      ' L ' + pts[0].x + ' ' + (padY + innerH + 10) + ' Z';

    // y gridlines (4)
    var grid = '';
    for (var g = 0; g <= 4; g++) {
      var gy = padY + (g / 4) * innerH + 10;
      var gv = max - (g / 4) * span;
      grid += '<line x1="' + padX + '" y1="' + gy + '" x2="' + (W - padX) + '" y2="' + gy + '" stroke="var(--ds-border)" stroke-width="1" stroke-dasharray="3 4" />';
      grid += '<text x="' + (padX - 12) + '" y="' + (gy + 4) + '" text-anchor="end" font-size="11" fill="var(--ds-faint)">' + fmtNum(gv) + '</text>';
    }

    var xlabels = d.labels.map(function (l, i) {
      return '<text x="' + pts[i].x + '" y="' + (H - 6) + '" text-anchor="middle" font-size="11" fill="var(--ds-muted)">' + l + '</text>';
    }).join('');

    chartSvg.innerHTML =
      '<defs>' +
        '<linearGradient id="area-g" x1="0" y1="0" x2="0" y2="1">' +
          '<stop offset="0" stop-color="var(--ds-accent)" stop-opacity="0.28" />' +
          '<stop offset="1" stop-color="var(--ds-accent)" stop-opacity="0" />' +
        '</linearGradient>' +
      '</defs>' +
      grid +
      '<path d="' + area + '" fill="url(#area-g)" class="chart-area" />' +
      '<path d="' + line + '" fill="none" stroke="var(--ds-accent)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="chart-line" />' +
      pts.map(function (p) {
        return '<circle cx="' + p.x + '" cy="' + p.y + '" r="4" fill="var(--ds-surface)" stroke="var(--ds-accent)" stroke-width="2" class="chart-pt" />';
      }).join('') +
      xlabels +
      '<rect id="chart-overlay" x="0" y="0" width="' + W + '" height="' + H + '" fill="transparent" />' +
      '<line id="hair" x1="0" y1="0" x2="0" y2="0" stroke="var(--ds-border-strong)" stroke-width="1" opacity="0" />' +
      '<g id="tip" opacity="0"><rect x="0" y="0" width="120" height="46" rx="8" fill="var(--ds-surface)" stroke="var(--ds-border)" filter="drop-shadow(0 4px 12px rgba(0,0,0,0.15))" /><text id="tip-label" x="10" y="18" font-size="11" fill="var(--ds-muted)"></text><text id="tip-value" x="10" y="36" font-size="14" font-weight="700" fill="var(--ds-text)"></text></g>';

    wireTooltip(pts, d.labels, d.revenue);
  }

  function wireTooltip(pts, labels, values) {
    var overlay = chartSvg.querySelector('#chart-overlay');
    var hair = chartSvg.querySelector('#hair');
    var tip = chartSvg.querySelector('#tip');
    var tipLabel = chartSvg.querySelector('#tip-label');
    var tipValue = chartSvg.querySelector('#tip-value');
    var W = chartSvg.viewBox.baseVal.width;

    function move(clientX) {
      var rect = chartSvg.getBoundingClientRect();
      var relX = ((clientX - rect.left) / rect.width) * W;
      var i = Math.round((relX - 48) / ((W - 96) / Math.max(1, pts.length - 1)));
      i = Math.max(0, Math.min(pts.length - 1, i));
      var p = pts[i];
      hair.setAttribute('x1', p.x); hair.setAttribute('x2', p.x);
      hair.setAttribute('y1', 24); hair.setAttribute('y2', 300);
      hair.setAttribute('opacity', '1');
      var tx = Math.min(W - 130, Math.max(8, p.x - 60));
      tip.setAttribute('transform', 'translate(' + tx + ',' + (p.y - 58) + ')');
      tip.setAttribute('opacity', '1');
      tipLabel.textContent = labels[i];
      tipValue.textContent = '$' + values[i].toLocaleString();
    }
    overlay.addEventListener('mousemove', function (e) { move(e.clientX); });
    overlay.addEventListener('mouseleave', function () {
      hair.setAttribute('opacity', '0'); tip.setAttribute('opacity', '0');
    });
    overlay.addEventListener('touchmove', function (e) { if (e.touches[0]) move(e.touches[0].clientX); }, { passive: true });
  }

  if (periodSeg) {
    periodSeg.addEventListener('click', function (e) {
      var btn = e.target.closest('button[data-range]');
      if (!btn) return;
      current = btn.dataset.range;
      periodSeg.querySelectorAll('button').forEach(function (b) {
        b.setAttribute('aria-pressed', String(b === btn));
      });
      drawChart(current);
    });
  }

  /* ---- Activity list --------------------------------------------------- */
  var actList = document.getElementById('activity');
  if (actList) {
    actList.innerHTML = ACTIVITY.map(function (a) {
      return '<li><span class="pic" style="background:' + a.tone + '">' + a.who + '</span>' +
        '<div class="txt">' + a.text + '<div class="time">' + a.time + '</div></div></li>';
    }).join('');
  }

  /* ---- Table row actions ---------------------------------------------- */
  document.querySelectorAll('table.data').forEach(function (tbl) {
    tbl.addEventListener('click', function (e) {
      var btn = e.target.closest('.row-act');
      if (!btn) return;
      var row = btn.closest('tr');
      var name = row.querySelector('.nm') ? row.querySelector('.nm').textContent : 'row';
      var action = btn.dataset.action || 'action';
      var msgs = {
        view: 'Opening ' + name + ' details',
        edit: 'Editing ' + name,
        delete: 'Removed ' + name + ' from the list'
      };
      showToast(msgs[action] || (action + ' ' + name));
      if (action === 'delete') {
        row.style.transition = 'opacity .18s, transform .18s';
        row.style.opacity = '0'; row.style.transform = 'translateX(-8px)';
        setTimeout(function () { row.remove(); }, 180);
      }
    });
  });

  /* ---- Upgrade + KPI buttons ------------------------------------------ */
  document.querySelectorAll('[data-action="upgrade"]').forEach(function (b) {
    b.addEventListener('click', function () { showToast('Upgrade flow opening…'); });
  });
  document.querySelectorAll('.page-head .btn').forEach(function (b) {
    b.addEventListener('click', function () { showToast(b.textContent.trim() + ' action'); });
  });

  /* ---- Toast ----------------------------------------------------------- */
  function showToast(msg) {
    if (!TOAST) return;
    TOAST.textContent = msg;
    TOAST.classList.add('show');
    clearTimeout(showToast._t);
    showToast._t = setTimeout(function () { TOAST.classList.remove('show'); }, 2600);
  }

  /* ---- Init ------------------------------------------------------------ */
  function init() {
    document.querySelectorAll('[data-countup]').forEach(animateNumber);
    drawChart(current);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else { init(); }
})();
