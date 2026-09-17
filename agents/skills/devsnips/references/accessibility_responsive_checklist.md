# Accessibility & responsive verification checklist

Use this during SKILL.md Phase 6 (Adapt) and Phase 7 (Verify). This is a
checklist to run through, not boilerplate to paste into a reply — only report
what was actually checked.

## Accessibility — preserve or improve, never regress

Confirm for the integrated resource, in its final (adapted) state:

- [ ] Semantic elements retained (`<button>` stays a button, `<nav>` stays
      `<nav>`, headings aren't demoted/promoted arbitrarily to fit a design).
- [ ] Every interactive control has an accessible name (visible label,
      `aria-label`, or `aria-labelledby` — not just a placeholder).
- [ ] Labels/descriptions carried over or re-wired (`aria-describedby` for
      helper/error text, `<label for>`/`htmlFor` for form fields).
- [ ] Keyboard interaction still works: Tab order is sane, custom widgets
      (menus, tabs, accordions, dialogs) follow their expected key model
      (Arrow keys, Home/End, Escape as applicable — check the resource's own
      README/metadata for what it originally implemented).
- [ ] Visible focus indicator survives any restyling (`focus-visible` rings
      not stripped by a global reset or a token swap).
- [ ] Native form behavior intact (required/validation still fires, submit
      still works, no `<div onClick>` substituted for a real `<button>` or
      `<a href>`).
- [ ] Status/error messaging still announces (`role="alert"`/`role="status"`/
      `aria-live` regions preserved, not silently dropped during adaptation).
- [ ] ARIA used only to supplement, not replace, native semantics — no
      `role="button"` on a div when a real `<button>` would do.
- [ ] Heading structure stays logical in the page it's integrated into (an
      imported Section's `<h2>` doesn't collide with or skip past the host
      page's outline).
- [ ] State/meaning isn't color-only (check icons/text/patterns accompany
      any color-coded state the resource uses).

## Responsive — check at real viewport sizes, don't assume

Check the *final integrated* implementation (not just the isolated preview)
at minimum:

- [ ] Narrow mobile width (≈375px) — no horizontal overflow/scroll.
- [ ] Navigation collapses/adapts correctly if the resource includes any.
- [ ] Text wraps instead of clipping or overflowing fixed-width containers.
- [ ] Multi-column layouts collapse to a usable single/stacked column below
      their breakpoint.
- [ ] Long real content (the project's actual copy, not the resource's demo
      lorem/placeholder text) doesn't break the layout.
- [ ] Fixed-width controls (buttons, inputs) don't force overflow on narrow
      widths.
- [ ] Sticky/fixed elements don't obscure content or overlap other fixed
      elements once integrated into the host page.
- [ ] Touch targets are reasonably sized/spaced on touch viewports.

Do not sign off on desktop appearance alone and call responsive behavior
verified — the SKILL.md Phase 7 contract requires this checked, not assumed.

## Reporting

When reporting Phase 7 results, name what was actually exercised (e.g. "Tab
order and Escape-to-close verified on the dialog; checked layout at 375/768/
1280px") rather than a blanket "accessible and responsive" claim with nothing
behind it.
