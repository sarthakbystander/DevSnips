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

  // Monthly / yearly pricing
  var toggleBtns = document.querySelectorAll('[data-billing]');
  var prices = document.querySelectorAll('[data-price-monthly]');
  toggleBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var mode = btn.getAttribute('data-billing');
      toggleBtns.forEach(function (b) {
        b.setAttribute('aria-pressed', b === btn ? 'true' : 'false');
      });
      prices.forEach(function (el) {
        var monthly = el.getAttribute('data-price-monthly');
        var yearly = el.getAttribute('data-price-yearly');
        el.innerHTML = mode === 'yearly'
          ? yearly + '<span>/mo</span>'
          : monthly + '<span>/mo</span>';
      });
    });
  });
})();
