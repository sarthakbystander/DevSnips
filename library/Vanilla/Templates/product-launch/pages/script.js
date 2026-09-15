/* Product Launch — interactions
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
      try { localStorage.setItem('pl-theme', next); } catch (e) {}
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

  /* ---------- FAQ accordion (single-open) ---------- */
  var acc = document.querySelector('[data-accordion="faq"]');
  if (acc) {
    var triggers = Array.prototype.slice.call(
      acc.querySelectorAll('.faq-trigger')
    );
    triggers.forEach(function (trigger) {
      trigger.addEventListener('click', function () {
        var panelId = trigger.getAttribute('aria-controls');
        var panel = document.getElementById(panelId);
        var willOpen = trigger.getAttribute('aria-expanded') !== 'true';
        // Close all
        triggers.forEach(function (t) {
          t.setAttribute('aria-expanded', 'false');
          var p = document.getElementById(t.getAttribute('aria-controls'));
          if (p) p.setAttribute('data-open', 'false');
        });
        if (willOpen && panel) {
          trigger.setAttribute('aria-expanded', 'true');
          panel.setAttribute('data-open', 'true');
        }
      });
    });
  }

  /* ---------- Waitlist form ---------- */
  var form = document.getElementById('waitlist-form');
  if (form) {
    var nameInput = document.getElementById('wl-name');
    var emailInput = document.getElementById('wl-email');
    var nameError = document.getElementById('wl-name-error');
    var emailError = document.getElementById('wl-email-error');
    var success = document.getElementById('wl-success');
    var countEl = document.getElementById('wl-count');

    function showError(input, errEl, msg) {
      input.setAttribute('aria-invalid', 'true');
      errEl.textContent = msg;
    }
    function clearError(input, errEl) {
      input.removeAttribute('aria-invalid');
      errEl.textContent = '';
    }

    var emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = true;

      if (!nameInput.value.trim()) {
        showError(nameInput, nameError, 'Please enter your name.');
        ok = false;
      } else {
        clearError(nameInput, nameError);
      }

      var email = emailInput.value.trim();
      if (!email) {
        showError(emailInput, emailError, 'Please enter your work email.');
        ok = false;
      } else if (!emailRe.test(email)) {
        showError(emailInput, emailError, 'That email address looks invalid.');
        ok = false;
      } else {
        clearError(emailInput, emailError);
      }

      if (!ok) {
        var firstBad = form.querySelector('[aria-invalid="true"]');
        if (firstBad) firstBad.focus();
        return;
      }

      // Simulate submission (no backend).
      form.setAttribute('hidden', '');
      success.setAttribute('data-visible', 'true');
      // Bump the count.
      if (countEl) {
        var n = parseInt(countEl.textContent.replace(/[^\d]/g, ''), 10) || 0;
        countEl.textContent = (n + 1).toLocaleString() + ' joined';
      }
    });

    // Clear error on input
    nameInput.addEventListener('input', function () { clearError(nameInput, nameError); });
    emailInput.addEventListener('input', function () { clearError(emailInput, emailError); });
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
