(function () {
  'use strict';
  var root = document.documentElement;
  var stored = localStorage.getItem('ds-theme');
  if (stored === 'dark' || (!stored && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    root.setAttribute('data-theme', 'dark');
  }

  document.querySelectorAll('[data-theme-toggle]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var isDark = root.getAttribute('data-theme') === 'dark';
      if (isDark) {
        root.removeAttribute('data-theme');
        localStorage.setItem('ds-theme', 'light');
      } else {
        root.setAttribute('data-theme', 'dark');
        localStorage.setItem('ds-theme', 'dark');
      }
    });
  });

  var menuToggle = document.querySelector('[data-menu-toggle]');
  var navLinks = document.querySelector('[data-nav-links]');
  if (menuToggle && navLinks) {
    menuToggle.addEventListener('click', function () {
      var open = navLinks.classList.toggle('is-open');
      menuToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // Schedule tabs
  var tabs = document.querySelectorAll('[data-tab]');
  var panels = document.querySelectorAll('[data-panel]');
  tabs.forEach(function (tab) {
    tab.addEventListener('click', function () {
      var id = tab.getAttribute('data-tab');
      tabs.forEach(function (t) {
        t.setAttribute('aria-selected', t === tab ? 'true' : 'false');
      });
      panels.forEach(function (p) {
        p.classList.toggle('is-active', p.getAttribute('data-panel') === id);
      });
    });
  });

  // Countdown to fixed event date (15 Sep 2026 09:00 UTC)
  var eventDate = new Date('2026-09-15T09:00:00Z').getTime();
  function tick() {
    var now = Date.now();
    var dist = eventDate - now;
    var days = document.getElementById('cd-days');
    var hours = document.getElementById('cd-hours');
    var mins = document.getElementById('cd-mins');
    var secs = document.getElementById('cd-secs');
    if (!days) return;
    if (dist < 0) {
      days.textContent = '00';
      hours.textContent = '00';
      mins.textContent = '00';
      secs.textContent = '00';
      return;
    }
    days.textContent = String(Math.floor(dist / 86400000)).padStart(2, '0');
    hours.textContent = String(Math.floor((dist % 86400000) / 3600000)).padStart(2, '0');
    mins.textContent = String(Math.floor((dist % 3600000) / 60000)).padStart(2, '0');
    secs.textContent = String(Math.floor((dist % 60000) / 1000)).padStart(2, '0');
  }
  tick();
  setInterval(tick, 1000);

  // Registration form demo
  var form = document.querySelector('[data-reg-form]');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      form.style.display = 'none';
      var success = document.querySelector('[data-reg-success]');
      if (success) success.classList.add('is-visible');
    });
  }
})();
