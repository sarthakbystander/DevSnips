/**
 * DevSnips Product Launch — shared behavior
 * Theme toggle, mobile nav, waitlist form (demo only)
 */
(function () {
  'use strict';

  const root = document.documentElement;
  const stored = localStorage.getItem('ds-theme');

  if (stored === 'dark' || (!stored && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    root.setAttribute('data-theme', 'dark');
  }

  // Theme toggle
  document.querySelectorAll('[data-theme-toggle]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const isDark = root.getAttribute('data-theme') === 'dark';
      if (isDark) {
        root.removeAttribute('data-theme');
        localStorage.setItem('ds-theme', 'light');
      } else {
        root.setAttribute('data-theme', 'dark');
        localStorage.setItem('ds-theme', 'dark');
      }
    });
  });

  // Mobile nav
  const menuToggle = document.querySelector('[data-menu-toggle]');
  const navLinks = document.querySelector('[data-nav-links]');

  if (menuToggle && navLinks) {
    menuToggle.addEventListener('click', function () {
      const open = navLinks.classList.toggle('is-open');
      menuToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // Waitlist form (front-end only demo)
  document.querySelectorAll('[data-waitlist-form]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      const email = form.querySelector('input[type="email"]');
      const success = form.parentElement.querySelector('[data-waitlist-success]');

      if (!email || !email.value.trim()) return;

      form.style.display = 'none';
      if (success) {
        success.classList.add('is-visible');
        success.setAttribute('role', 'status');
      }
    });
  });
})();
