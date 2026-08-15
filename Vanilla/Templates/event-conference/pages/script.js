/* Event Conference — interactions
   Scoped, dependency-free. Respects reduced motion. */
(function () {
  'use strict';

  var root = document.documentElement;

  /* ---------- Theme toggle ---------- */
  var themeBtn = document.querySelector('[data-theme-toggle]');
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('ec-theme', next); } catch (e) {}
    });
  }

  /* ---------- Mobile nav ---------- */
  var navToggle = document.querySelector('[data-nav-toggle]');
  var mobileNav = document.getElementById('mobile-nav');
  function setNav(open) {
    if (!navToggle || !mobileNav) return;
    navToggle.setAttribute('aria-expanded', String(open));
    mobileNav.setAttribute('data-open', String(open));
  }
  if (navToggle && mobileNav) {
    navToggle.addEventListener('click', function () {
      setNav(mobileNav.getAttribute('data-open') !== 'true');
    });
    mobileNav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () { setNav(false); });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && mobileNav.getAttribute('data-open') === 'true') {
        setNav(false);
        navToggle.focus();
      }
    });
  }

  /* ---------- Schedule tabs ---------- */
  var tablist = document.querySelector('[role="tablist"][aria-label="Schedule days"]');
  if (tablist) {
    var tabs = Array.prototype.slice.call(tablist.querySelectorAll('[role="tab"]'));
    var panels = {};
    tabs.forEach(function (tab) {
      var panel = document.getElementById(tab.getAttribute('aria-controls'));
      if (panel) panels[tab.getAttribute('data-tab')] = panel;
    });

    function activate(tab) {
      tabs.forEach(function (t) {
        var selected = t === tab;
        t.setAttribute('aria-selected', String(selected));
        t.setAttribute('tabindex', selected ? '0' : '-1');
      });
      Object.keys(panels).forEach(function (key) {
        var p = panels[key];
        var active = p === panels[tab.getAttribute('data-tab')];
        p.setAttribute('data-active', String(active));
        if (active) { p.removeAttribute('hidden'); }
        else { p.setAttribute('hidden', ''); }
      });
      tab.focus();
    }

    tabs.forEach(function (tab) {
      tab.addEventListener('click', function () { activate(tab); });
      tab.addEventListener('keydown', function (e) {
        var idx = tabs.indexOf(tab);
        if (e.key === 'ArrowRight') { e.preventDefault(); tabs[(idx + 1) % tabs.length].click(); }
        else if (e.key === 'ArrowLeft') { e.preventDefault(); tabs[(idx - 1 + tabs.length) % tabs.length].click(); }
        else if (e.key === 'Home') { e.preventDefault(); tabs[0].click(); }
        else if (e.key === 'End') { e.preventDefault(); tabs[tabs.length - 1].click(); }
      });
    });
  }

  /* ---------- Countdown ---------- */
  var dEl = document.getElementById('cd-days');
  var hEl = document.getElementById('cd-hours');
  var mEl = document.getElementById('cd-mins');
  var sEl = document.getElementById('cd-secs');
  // Target: March 18, 2027, 09:00 WET (UTC+0)
  var target = new Date('2027-03-18T09:00:00Z').getTime();

  function pad(n) { return n < 10 ? '0' + n : String(n); }

  function tick() {
    var now = Date.now();
    var diff = Math.max(0, target - now);
    var days = Math.floor(diff / 86400000);
    var hours = Math.floor((diff % 86400000) / 3600000);
    var mins = Math.floor((diff % 3600000) / 60000);
    var secs = Math.floor((diff % 60000) / 1000);
    if (dEl) dEl.textContent = pad(days);
    if (hEl) hEl.textContent = pad(hours);
    if (mEl) mEl.textContent = pad(mins);
    if (sEl) sEl.textContent = pad(secs);
  }
  if (dEl) {
    tick();
    // 1s interval; paused when tab hidden.
    var id = setInterval(function () {
      if (!document.hidden) tick();
    }, 1000);
    document.addEventListener('visibilitychange', tick);
  }

  /* ---------- Reveal on scroll ---------- */
  var reveals = Array.prototype.slice.call(document.querySelectorAll('.reveal'));
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce || !('IntersectionObserver' in window)) {
    reveals.forEach(function (el) { el.classList.add('is-visible'); });
  } else {
    var ro = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        obs.unobserve(entry.target);
      });
    }, { threshold: 0.12 });
    reveals.forEach(function (el) { ro.observe(el); });
  }
})();
