/* ============================================================
   DevSnips Documentation — runtime + content
   Vanilla JS. Hash router, scrollspy TOC, search, code tools,
   theme toggle, mobile drawer. No dependencies.
   ============================================================ */
(function () {
  'use strict';

  /* ---------- helpers ---------- */
  function $(s, c) { return (c || document).querySelector(s); }
  function $all(s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); }
  function el(tag, attrs, html) {
    var e = document.createElement(tag);
    if (attrs) for (var k in attrs) {
      if (k === 'class') e.className = attrs[k];
      else if (k === 'html') e.innerHTML = attrs[k];
      else if (k.indexOf('on') === 0) e.addEventListener(k.slice(2), attrs[k]);
      else e.setAttribute(k, attrs[k]);
    }
    if (html != null) e.innerHTML = html;
    return e;
  }
  function esc(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  /* ---------- lightweight syntax highlighter ---------- */
  function highlight(code, lang) {
    code = esc(code);
    lang = (lang || '').toLowerCase();
    if (lang === 'html' || lang === 'xml') return hlHtml(code);
    if (lang === 'css') return hlCss(code);
    if (lang === 'js' || lang === 'javascript' || lang === 'json') return hlJs(code);
    if (lang === 'bash' || lang === 'sh') return hlBash(code);
    return code;
  }
  function hlHtml(c) {
    return c
      .replace(/(&lt;!--[\s\S]*?--&gt;)/g, '<span class="tok-com">$1</span>')
      .replace(/(&lt;\/?)([a-zA-Z][\w-]*)/g, '$1<span class="tok-tag">$2</span>')
      .replace(/([\w-]+)=(&quot;[^&]*?&quot;|"[^"]*?")/g, '<span class="tok-att">$1</span>=$2')
      .replace(/(&gt;|&lt;\/?)/g, '<span class="tok-pun">$1</span>');
  }
  function hlCss(c) {
    return c
      .replace(/(\/\*[\s\S]*?\*\/)/g, '<span class="tok-com">$1</span>')
      .replace(/([\w-]+)(\s*:)/g, '<span class="tok-prop">$1</span>$2')
      .replace(/(#[0-9a-fA-F]{3,8}\b)/g, '<span class="tok-num">$1</span>')
      .replace(/(var\(--[\w-]+\))/g, '<span class="tok-fn">$1</span>')
      .replace(/(@media|@keyframes|@supports|!important)/g, '<span class="tok-key">$1</span>');
  }
  function hlJs(c) {
    return c
      .replace(/(\/\/[^\n]*)/g, '<span class="tok-com">$1</span>')
      .replace(/(\/\*[\s\S]*?\*\/)/g, '<span class="tok-com">$1</span>')
      .replace(/(&quot;[^&]*?&quot;|'[^']*?'|`[^`]*?`)/g, '<span class="tok-str">$1</span>')
      .replace(/\b(var|let|const|function|return|if|else|for|while|new|this|class|extends|import|export|from|default|typeof|instanceof|null|undefined|true|false)\b/g, '<span class="tok-key">$1</span>')
      .replace(/\b(\d+)\b/g, '<span class="tok-num">$1</span>')
      .replace(/([a-zA-Z_$][\w$]*)(?=\()/g, '<span class="tok-fn">$1</span>');
  }
  function hlBash(c) {
    return c
      .replace(/(#([^\n]*))/g, '<span class="tok-com">$1</span>')
      .replace(/(^|\s)(npm|pnpm|yarn|git|cd|node|python|pip|curl|mkdir|ls|echo)\b/g, '$1<span class="tok-key">$2</span>')
      .replace(/(--?[a-zA-Z][\w-]*)/g, '<span class="tok-att">$1</span>')
      .replace(/(&quot;[^&]*?&quot;|'[^']*?')/g, '<span class="tok-str">$1</span>');
  }

  /* ---------- code block builders ---------- */
  function codeBlock(codeStr, lang) {
    var id = 'cb' + Math.random().toString(36).slice(2, 8);
    var hl = highlight(codeStr.replace(/^\n/, '').replace(/\s+$/, ''), lang);
    return '<div class="code-block"><div class="code-header"><span class="code-lang">' + esc(lang || '') + '</span>' +
      '<button type="button" class="copy-btn" data-copy="' + id + '" aria-label="Copy code"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg><span class="copy-label"></span></button></div>' +
      '<pre><code id="' + id + '">' + hl + '</code></pre></div>';
  }
  function codeTabs(tabs) {
    var out = '<div class="code-tabs"><div class="tabs-bar" role="tablist">';
    tabs.forEach(function (t, i) {
      out += '<button type="button" class="code-tab" role="tab" id="' + t.id + '-tab" aria-selected="' + (i === 0) + '" aria-controls="' + t.id + '">' + esc(t.label) + '</button>';
    });
    out += '</div>';
    tabs.forEach(function (t, i) {
      var hl = highlight(t.code.replace(/^\n/, '').replace(/\s+$/, ''), t.lang);
      out += '<div class="tab-panel' + (i === 0 ? ' active' : '') + '" role="tabpanel" id="' + t.id + '" aria-labelledby="' + t.id + '-tab"><pre><code>' + hl + '</code></pre></div>';
    });
    out += '</div>';
    return out;
  }
  /* ============================================================
     NAVIGATION CONFIG — nested sidebar
     ============================================================ */
  var NAV = [
    { group: 'Start', items: [
      { id: 'home', label: 'Documentation Home' },
      { id: 'introduction', label: 'Introduction' },
      { id: 'getting-started', label: 'Getting Started', children: [
        { id: 'installation', label: 'Installation' },
        { id: 'quick-start', label: 'Quick Start' }
      ]},
      { id: 'vanilla', label: 'Vanilla' }
    ]},
    { group: 'Library', items: [
      { id: 'components', label: 'Components', children: [
        { id: 'templates', label: 'Templates' }
      ]},
      { id: 'design-tokens', label: 'Design Tokens' },
      { id: 'examples', label: 'Examples' }
    ]},
    { group: 'Reference', items: [
      { id: 'guides', label: 'Guides' },
      { id: 'api', label: 'API Reference' },
      { id: 'faq', label: 'FAQ' },
      { id: 'changelog', label: 'Changelog' }
    ]},
    { group: 'Project', items: [
      { id: 'roadmap', label: 'Roadmap' },
      { id: 'contributing', label: 'Contributing' }
    ]}
  ];

  /* page order for prev/next */
  var ORDER = [
    'home','introduction','getting-started','installation','quick-start',
    'vanilla','components','templates','design-tokens','guides','api',
    'examples','faq','changelog','roadmap','contributing'
  ];

  /* page meta (eyebrow, title, lead, updated, readtime) */
  var META = {
    'home':            { eyebrow: 'Welcome', title: 'DevSnips Documentation', lead: 'The open-source, framework-free frontend component library. Copy-paste components, templates, and design tokens — built with HTML, CSS, and vanilla JavaScript.', updated: 'Aug 12, 2026', readtime: '4 min' },
    'introduction':    { eyebrow: 'Overview', title: 'Introduction', lead: 'DevSnips is an organized collection of production-ready frontend building blocks. No frameworks, no build step — just semantic HTML, modern CSS, and vanilla JS you can drop into any project.', updated: 'Aug 10, 2026', readtime: '6 min' },
    'getting-started': { eyebrow: 'Start', title: 'Getting Started', lead: 'Everything you need to use DevSnips in a new or existing project. The library is framework-free, so there is no install script for a package — this guide covers using the files and tooling directly.', updated: 'Aug 12, 2026', readtime: '5 min' },
    'installation':    { eyebrow: 'Setup', title: 'Installation', lead: 'DevSnips is consumed as source files rather than a runtime dependency. Clone the repository or download a release, then reference the files you need.', updated: 'Aug 12, 2026', readtime: '4 min' },
    'quick-start':     { eyebrow: 'Start', title: 'Quick Start', lead: 'A two-minute tour: grab a component, wire the tokens, and ship. The fastest path from zero to a styled, accessible UI.', updated: 'Aug 12, 2026', readtime: '3 min' },
    'vanilla':         { eyebrow: 'Technology', title: 'Vanilla', lead: 'The Vanilla collection ships framework-free HTML, CSS, and JavaScript. Each component is self-contained and copy-paste ready — no bundler, no compiler, no runtime.', updated: 'Aug 10, 2026', readtime: '7 min' },
    'components':       { eyebrow: 'Library', title: 'Components', lead: 'Reusable UI building blocks organized into design-system families: Accordions, Buttons, Cards, Tables, Modals, and more. Every component is accessible, responsive, and tokenized.', updated: 'Aug 12, 2026', readtime: '8 min' },
    'templates':       { eyebrow: 'Library', title: 'Templates', lead: 'Complete page and site templates built from the same design tokens. Full compositions — dashboards, documentation sites, landing pages — that demonstrate the system at scale.', updated: 'Aug 12, 2026', readtime: '6 min' },
    'design-tokens':   { eyebrow: 'System', title: 'Design Tokens', lead: 'A single canonical token system that makes every DevSnips component speak one visual language. Source of truth: Vanilla/Components/tokens.css and Vanilla/Templates/design-tokens.md.', updated: 'Aug 10, 2026', readtime: '9 min' },
    'guides':          { eyebrow: 'Learn', title: 'Guides', lead: 'Practical, hands-on walkthroughs for the most common DevSnips workflows — from theming a single component to composing a full page.', updated: 'Aug 9, 2026', readtime: '10 min' },
    'api':             { eyebrow: 'Reference', title: 'API Reference', lead: 'The contracts every DevSnips component and template honors. Metadata schema, data attributes, and the optional JavaScript helpers for interactive families.', updated: 'Aug 12, 2026', readtime: '7 min' },
    'examples':        { eyebrow: 'Library', title: 'Examples', lead: 'Annotated, copy-paste examples covering the most-used patterns. Each example is self-contained and renders identically standalone or inside the token system.', updated: 'Aug 8, 2026', readtime: '6 min' },
    'faq':             { eyebrow: 'Help', title: 'FAQ', lead: 'Answers to the questions that come up most often. If something is missing, open a discussion on GitHub.', updated: 'Aug 7, 2026', readtime: '5 min' },
    'changelog':       { eyebrow: 'History', title: 'Changelog', lead: 'A record of notable changes to the DevSnips library. Versions follow a simple major.minor.patch scheme; this log tracks content and architecture changes.', updated: 'Aug 12, 2026', readtime: '4 min' },
    'roadmap':         { eyebrow: 'Project', title: 'Roadmap', lead: 'Where DevSnips is headed. The roadmap is public and driven by contributor interest — pick something and open a PR.', updated: 'Aug 6, 2026', readtime: '5 min' },
    'contributing':    { eyebrow: 'Project', title: 'Contributing', lead: 'DevSnips is built in the open. This guide covers the contribution workflow, code standards, and the quality bar enforced by scripts/validate.py.', updated: 'Aug 12, 2026', readtime: '8 min' }
  };

  /* icon paths (inline, no deps) */
  var ICONS = {
    book: '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>',
    layers: '<path d="m12 2 9 5-9 5-9-5 9-5z"/><path d="m3 12 9 5 9-5"/><path d="m3 17 9 5 9-5"/>',
    terminal: '<path d="m4 17 6-6-6-6"/><path d="M12 19h8"/>',
    palette: '<circle cx="13.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="10.5" r="2.5"/><circle cx="8.5" cy="7.5" r="2.5"/><circle cx="6.5" cy="12.5" r="2.5"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c1.1 0 2-.9 2-2 0-.5-.2-1-.5-1.3-.3-.4-.5-.8-.5-1.2 0-1.1.9-2 2-2h2.5c2.8 0 5-2.2 5-5 0-4.4-4.5-8-10-8z"/>',
    book2: '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>',
    code: '<path d="m16 18 6-6-6-6"/><path d="m8 6-6 6 6 6"/>',
    help: '<circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><path d="M12 17h.01"/>',
    history: '<path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/><path d="M12 7v5l4 2"/>',
    map: '<path d="m9 3-6 2v16l6-2 6 2 6-2V3l-6 2-6-2z"/><path d="M9 3v16"/><path d="m15 5v16"/>',
    users: '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    clock: '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    edit: '<path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4z"/>',
    github: '<path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1a5.07 5.07 0 0 0-.91 3.77 5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/>',
    search: '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    sun: '<circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/>',
    moon: '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9z"/>',
    menu: '<path d="M4 6h16"/><path d="M4 12h16"/><path d="M4 18h16"/>',
    close: '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    copy: '<rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>',
    chevron: '<path d="m9 18 6-6-6-6"/>',
    chevronDown: '<path d="m6 9 6 6 6-6"/>',
    arrowRight: '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    arrowLeft: '<path d="M19 12H5"/><path d="m12 19-7-7 7-7"/>',
    check: '<path d="M20 6 9 17l-5-5"/>',
    lightbulb: '<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/>',
    info: '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>',
    alert: '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3z"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
    xCircle: '<circle cx="12" cy="12" r="10"/><path d="m15 9-6 6"/><path d="m9 9 6 6"/>'
  };
  function ic(name) { return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' + (ICONS[name] || '') + '</svg>'; }
  /* ============================================================
     PAGE CONTENT BUILDERS
     ============================================================ */
  var PAGES = {};

  /* callout helper: {type, bodyHTML} */
  function callout(type, body) {
    var icon = { info: 'info', note: 'book', tip: 'lightbulb', warning: 'alert', danger: 'xCircle' }[type] || 'info';
    return '<div class="callout callout-' + type + '"><div class="callout-icon">' + ic(icon) + '</div><div class="callout-body">' + body + '</div></div>';
  }
  function badge(label, kind) { return '<span class="badge badge-' + (kind || 'neutral') + '">' + label + '</span>'; }
  function apiBlock(name, sig, desc, params, example) {
    var p = '';
    if (params && params.length) {
      p = '<table class="api-params"><thead><tr><th>Param</th><th>Type</th><th>Default</th><th>Description</th></tr></thead><tbody>';
      params.forEach(function (r) {
        p += '<tr><td><code>' + r.name + '</code>' + (r.req ? '<span class="param-req">required</span>' : '') + '</td><td>' + r.type + '</td><td>' + (r.def || '—') + '</td><td>' + r.desc + '</td></tr>';
      });
      p += '</tbody></table>';
    }
    return '<div class="api-block"><div class="api-head"><div class="api-signature">' + sig + '</div></div><div class="api-body"><p>' + desc + '</p>' + p + (example || '') + '</div></div>';
  }

  /* ---- HOME ---- */
  PAGES.home = function (m) {
    var cards = [
      { icon: 'book2', title: 'Introduction', desc: 'What DevSnips is and the principles behind a framework-free component library.', href: '#/introduction' },
      { icon: 'terminal', title: 'Getting Started', desc: 'Set up a project, install the files, and ship your first component.', href: '#/getting-started' },
      { icon: 'palette', title: 'Design Tokens', desc: 'One canonical token system — theme every component from a single file.', href: '#/design-tokens' },
      { icon: 'layers', title: 'Components', desc: 'Reusable, accessible building blocks organized into design-system families.', href: '#/components' },
      { icon: 'code', title: 'Templates', desc: 'Full page and site compositions — dashboards, docs, landing pages.', href: '#/templates' },
      { icon: 'map', title: 'Guides', desc: 'Hands-on walkthroughs for the most common DevSnips workflows.', href: '#/guides' }
    ];
    var cardHTML = '<div class="card-grid">' + cards.map(function (c) {
      return '<a class="doc-card" href="' + c.href + '"><div class="card-icon">' + ic(c.icon) + '</div><div class="card-title">' + c.title + '</div><div class="card-desc">' + c.desc + '</div><span class="card-arrow">Read more ' + ic('arrowRight') + '</span></a>';
    }).join('') + '</div>';

    return '<div class="home-hero">' +
      '<div class="eyebrow">' + m.eyebrow + '</div>' +
      '<h1>' + m.title + '</h1>' +
      '<p class="lead">' + m.lead + '</p>' +
      '<div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:28px">' +
        '<a class="hero-btn primary" href="#/getting-started">' + ic('terminal') + '<span>Get started</span></a>' +
        '<a class="hero-btn" href="#/components">' + ic('layers') + '<span>Browse components</span></a>' +
      '</div>' +
      '</div>' +
      '<h2>Start here</h2>' +
      cardHTML +
      '<h2>By technology</h2>' +
      '<p>DevSnips ships three parallel collections, each using the same design tokens:</p>' +
      '<div class="table-wrap"><table class="docs-table"><thead><tr><th>Technology</th><th>Path</th><th>Contents</th><th>Status</th></tr></thead><tbody>' +
      '<tr><td><strong>Tailwind CSS</strong></td><td><code>Tailwind/Components/</code></td><td>535 variants across 59 families</td>' + badge('Stable', 'stable') + '</td></tr>' +
      '<tr><td><strong>Vanilla HTML/CSS/JS</strong></td><td><code>Vanilla/Components/</code></td><td>311 variants across 47 families</td>' + badge('Stable', 'stable') + '</td></tr>' +
      '<tr><td><strong>React</strong></td><td><code>React/Components/</code></td><td>Reserved for future content</td>' + badge('Planned', 'beta') + '</td></tr>' +
      '</tbody></table></div>' +
      '<h2>How DevSnips is organized</h2>' +
      '<p>The library is organized as design-system <strong>families</strong>. A family groups related variants — for example, the <code>Accordions</code> family contains a basic accordion, a single-open accordion, and so on. Each variant is a self-contained folder.</p>' +
      callout('tip', '<strong>Grand total:</strong> 846 content items across 106 families. Tailwind leads with 535 variants; Vanilla follows with 311.') +
      '<h2>Next steps</h2>' +
      '<p>Read the <a href="#/introduction">introduction</a> for the philosophy, jump to <a href="#/quick-start">quick start</a> for a two-minute tour, or explore the <a href="#/design-tokens">design tokens</a> to understand the shared visual language.</p>';
  };

  /* ---- INTRODUCTION ---- */
  PAGES.introduction = function (m) {
    return '' +
      '<div class="eyebrow">' + m.eyebrow + '</div><h1>' + m.title + '</h1><p class="lead">' + m.lead + '</p>' +
      '<h2>What is DevSnips?</h2>' +
      '<p>DevSnips is an open-source frontend component library built on three principles: <strong>framework-free</strong>, <strong>copy-paste ready</strong>, and <strong>token-driven</strong>. There is no runtime dependency, no compiler, and no package you install. You grab the files you need and drop them into any project — static site, server-rendered app, or existing codebase.</p>' +
      '<p>The library is organized as design-system <strong>families</strong> (Accordions, Buttons, Cards, Tables, …) rather than a flat list of snippets. Each family groups related <strong>variants</strong>, and each variant is a self-contained folder with its source, preview, and metadata.</p>' +
      '<h2>Why framework-free?</h2>' +
      '<p>Most component libraries lock you into a framework. DevSnips deliberately does not. The Tailwind collection uses utility classes; the Vanilla collection uses semantic HTML, modern CSS, and vanilla JavaScript. Both speak the same design-token language, so you can re-theme the entire library by editing one file.</p>' +
      callout('info', '<strong>Design tokens are the contract.</strong> Every component opts into the <code>--ds-*</code> token system with a CSS-variable fallback, so it renders identically standalone <em>and</em> inside the themed system.') +
      '<h2>Three collections</h2>' +
      '<div class="table-wrap"><table class="docs-table"><thead><tr><th>Collection</th><th>Approach</th><th>Best for</th></tr></thead><tbody>' +
      '<tr><td><strong>Tailwind</strong></td><td>Utility classes + CDN</td><td>Rapid prototyping, teams already using Tailwind</td></tr>' +
      '<tr><td><strong>Vanilla</strong></td><td>Semantic HTML + scoped CSS/JS</td><td>Copy-paste fragments, no build step, long-lived design systems</td></tr>' +
      '<tr><td><strong>React</strong></td><td>Component primitives (planned)</td><td>React codebases (reserved for future content)</td></tr>' +
      '</tbody></table></div>' +
      '<h2>Design principles</h2>' +
      '<ul>' +
        '<li><strong>Accessibility first.</strong> Every interactive component ships with ARIA, keyboard support, and <code>:focus-visible</code> rings. The quality bar is enforced by <code>scripts/qa_vanilla.py</code>.</li>' +
        '<li><strong>Copy-paste standalone.</strong> A component must work the moment you paste it — no missing dependencies, no broken styles.</li>' +
        '<li><strong>Tokenized, not hardcoded.</strong> Colors, radii, spacing, and type come from <code>--ds-*</code> variables. Re-theme by editing one file.</li>' +
        '<li><strong>Reduced-motion safe.</strong> Every animation is guarded by <code>prefers-reduced-motion</code>.</li>' +
        '<li><strong>Light + dark.</strong> The token system ships both modes via <code>prefers-color-scheme</code> and an opt-in <code>data-theme</code> attribute.</li>' +
      '</ul>' +
      '<h2>The repository layout</h2>' +
      codeBlock('DevSnips/\n  Tailwind/\n    Components/        # 535 variants, 59 families\n    Templates/         # full site templates\n  Vanilla/\n    Components/        # 311 variants, 47 families\n    Templates/          # full page/site templates\n      SaaS Dashboard/\n      Documentation Site/\n      design-tokens.md  # shared token spec\n  snippets-index.json   # the canonical index\n  scripts/\n    validate.py        # architecture + index consistency\n    qa_vanilla.py       # quality-bar scanner', 'bash') +
      callout('note', 'The filesystem is the source of truth. <code>snippets-index.json</code> is regenerated from the filesystem by <code>_gen/rebuild_index.py</code> and validated by <code>scripts/validate.py</code>.') +
      '<h2>Where to go next</h2>' +
      '<ul>' +
        '<li><a href="#/getting-started">Getting Started</a> — use DevSnips in a real project.</li>' +
        '<li><a href="#/design-tokens">Design Tokens</a> — the shared visual language.</li>' +
        '<li><a href="#/components">Components</a> — browse the families.</li>' +
      '</ul>';
  };

  /* ---- GETTING STARTED ---- */
  PAGES['getting-started'] = function (m) {
    return '' +
      '<div class="eyebrow">' + m.eyebrow + '</div><h1>' + m.title + '</h1><p class="lead">' + m.lead + '</p>' +
      '<h2>Prerequisites</h2>' +
      '<p>DevSnips requires nothing at runtime. To develop and validate locally you need:</p>' +
      '<ul>' +
        '<li>A modern browser (Chrome, Firefox, Safari, or Edge).</li>' +
        '<li>Python 3.8+ to run the validation and QA scripts.</li>' +
        '<li>Git to clone the repository.</li>' +
      '</ul>' +
      callout('info', 'No Node.js, no bundler, no package manager required to <em>use</em> DevSnips. You only need Python if you want to run the validation scripts.') +
      '<h2>Get the code</h2>' +
      '<p>Clone the repository:</p>' +
      codeBlock('git clone https://github.com/sarthakbystander/DevSnips.git\ncd DevSnips', 'bash') +
      '<p>Or download a release archive from the GitHub releases page and extract it.</p>' +
      '<h2>Validate your copy</h2>' +
      '<p>Confirm the architecture, metadata, and index are consistent:</p>' +
      codeBlock('python3 scripts/validate.py', 'bash') +
      '<p>You should see <code>VALIDATION PASSED</code>. If anything fails, the script prints the exact file and reason.</p>' +
      callout('warning', '<strong>Never hand-edit</strong> <code>snippets-index.json</code> to work around a validation failure. The index is generated from the filesystem — fix the on-disk content and re-run <code>_gen/rebuild_index.py</code>.') +
      '<h2>Use a component</h2>' +
      '<ol class="steps">' +
        '<li><h4>Copy the variant folder</h4><p>Copy a component folder (e.g. <code>Vanilla/Components/Accordions/basic/</code>) into your project.</p></li>' +
        '<li><h4>Reference the files</h4><p>Link the CSS and JS, or paste the snippet directly into your page.</p></li>' +
        '<li><h4>Include the tokens (optional)</h4><p>Add <code>tokens.css</code> once to theme every component together. Without it, components still render identically using their fallback values.</p></li>' +
      '</ol>' +
      '<p>For the full, step-by-step path see <a href="#/quick-start">Quick Start</a>.</p>';
  };

  /* ---- INSTALLATION ---- */
  PAGES.installation = function (m) {
    return '' +
      '<div class="eyebrow">' + m.eyebrow + '</div><h1>' + m.title + '</h1><p class="lead">' + m.lead + '</p>' +
      '<h2>Option 1: Clone the repository</h2>' +
      '<p>The recommended way to use DevSnips is to clone the repo and copy the files you need:</p>' +
      codeTabs([
        { id: 'inst-git', label: 'git', lang: 'bash', code: 'git clone https://github.com/sarthakbystander/DevSnips.git\ncd DevSnips\npython3 scripts/validate.py' },
        { id: 'inst-curl', label: 'curl', lang: 'bash', code: 'curl -L https://github.com/sarthakbystander/DevSnips/archive/refs/heads/main.tar.gz | tar xz\nmv DevSnips-main DevSnips\ncd DevSnips' },
        { id: 'inst-wget', label: 'wget', lang: 'bash', code: 'wget https://github.com/sarthakbystander/DevSnips/archive/refs/heads/main.tar.gz\ntar xzf main.tar.gz\nmv DevSnips-main DevSnips' }
      ]) +
      '<h2>Option 2: Copy a single component</h2>' +
      '<p>For a one-off component, copy just the variant folder. A Vanilla variant contains a self-contained <code>.html</code>, <code>metadata.json</code>, and <code>README.md</code>:</p>' +
      codeBlock('cp -r Vanilla/Components/Accordions/basic/ ./my-project/accordions/', 'bash') +
      '<h2>Project structure</h2>' +
      '<p>A typical project consuming DevSnips looks like:</p>' +
      codeBlock('my-project/\n  index.html\n  css/\n    tokens.css      # copied from Vanilla/Components/tokens.css\n    accordion.css\n  js/\n    accordion.js\n  components/\n    accordions/\n      basic.html', 'bash') +
      callout('tip', '<strong>Link tokens once.</strong> Add <code>&lt;link rel="stylesheet" href="css/tokens.css"&gt;</code> in your <code>&lt;head&gt;</code> and every <code>var(--ds-*)</code> reference resolves to the themed value.') +
      '<h2>Fonts</h2>' +
      '<p>The Vanilla token system uses a system font stack by default. To match the DevSnips previews, load Inter and JetBrains Mono from Google Fonts:</p>' +
      codeBlock('<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">', 'html') +
      '<h2>Verify</h2>' +
      '<p>Open your page in a browser. The component should render identically to its DevSnips preview. Run the QA scanner on any Vanilla component you ship:</p>' +
      codeBlock('python3 scripts/qa_vanilla.py --only-failures', 'bash');
  };

  /* ---- QUICK START ---- */
  PAGES['quick-start'] = function (m) {
    return '' +
      '<div class="eyebrow">' + m.eyebrow + '</div><h1>' + m.title + '</h1><p class="lead">' + m.lead + '</p>' +
      '<h2>1. Grab a component</h2>' +
      '<p>Copy the basic accordion from the Vanilla collection:</p>' +
      codeBlock('cp -r Vanilla/Components/Accordions/basic/ ./my-project/', 'bash') +
      '<h2>2. Wire the tokens</h2>' +
      '<p>Include the token file once in your page <code>&lt;head&gt;</code>:</p>' +
      codeBlock('<link rel="stylesheet" href="css/tokens.css">', 'html') +
      '<h2>3. Add the markup</h2>' +
      '<p>Paste the component markup. It already uses <code>var(--ds-*)</code> with fallbacks, so it works standalone and inside the themed system:</p>' +
      codeBlock('<div data-accordion="basic">\n  <div data-accordion-item>\n    <button data-accordion-trigger aria-expanded="false">\n      What is DevSnips?\n    </button>\n    <div role="region" class="panel">\n      An open-source, framework-free frontend component library.\n    </div>\n  </div>\n</div>', 'html') +
      '<h2>4. Add the script</h2>' +
      '<p>The accordion scopes itself with <code>document.currentScript.closest()</code>, so it works as a snippet:</p>' +
      codeBlock('const root = document.currentScript.closest(\'[data-accordion]\');\nroot.querySelectorAll(\'[data-accordion-trigger]\').forEach(btn => {\n  btn.addEventListener(\'click\', () => {\n    const open = btn.getAttribute(\'aria-expanded\') === \'true\';\n    btn.setAttribute(\'aria-expanded\', String(!open));\n  });\n});', 'js') +
      callout('tip', '<strong>That\'s it.</strong> The accordion now toggles, is keyboard-operable, animates with the CSS-grid trick, and respects <code>prefers-reduced-motion</code>.') +
      '<h2>Re-theme everything</h2>' +
      '<p>Change the accent color for the whole library by editing one variable in <code>tokens.css</code>:</p>' +
      codeBlock(':root {\n  --ds-accent: #2563eb;   /* was #0ea5e9 */\n}', 'css') +
      '<p>Every component that references <code>var(--ds-accent, #2563eb)</code> picks up the new value instantly.</p>';
  };

  /* ---- VANILLA ---- */
  PAGES.vanilla = function (m) {
    return '' +
      '<div class="eyebrow">' + m.eyebrow + '</div><h1>' + m.title + '</h1><p class="lead">' + m.lead + '</p>' +
      '<h2>Convention</h2>' +
      '<p>Every Vanilla variant folder contains exactly three files:</p>' +
      '<div class="table-wrap"><table class="docs-table"><thead><tr><th>File</th><th>Purpose</th></tr></thead><tbody>' +
      '<tr><td><code>&lt;slug&gt;.html</code></td><td>Self-contained: inline <code>&lt;style&gt;</code> + <code>&lt;script&gt;</code>, full <code>&lt;!DOCTYPE&gt;</code> page</td></tr>' +
      '<tr><td><code>metadata.json</code></td><td>Name, slug, component, family, variant, tags, features, related</td></tr>' +
      '<tr><td><code>README.md</code></td><td>Features, responsive notes, browser support, usage</td></tr>' +
      '</tbody></table></div>' +
      '<h2>The Swiss design tokens</h2>' +
      '<p>The Vanilla collection speaks a single canonical token system — "Swiss", a neo-minimal, industry-standard palette. Source of truth: <code>Vanilla/Components/tokens.css</code> and <code>Vanilla/Components/DESIGN_TOKENS.md</code>.</p>' +
      '<ul>' +
        '<li><strong>Neutrals</strong> — a stone ramp from <code>--ds-gray-0</code> to <code>--ds-gray-950</code>.</li>' +
        '<li><strong>One accent</strong> — blue-600, <code>--ds-accent</code>.</li>' +
        '<li><strong>Semantic status</strong> — success / warning / danger / info, all WCAG AA.</li>' +
        '<li><strong>Type, spacing, radius, shadow, motion</strong> — full ramps aligned to Tailwind\'s spacing scale.</li>' +
      '</ul>' +
      callout('note', 'Components opt in with <code>var(--ds-&lt;token&gt;, &lt;original-value&gt;)</code>. The original value is the fallback, so a component is copy-paste standalone <strong>and</strong> renders identically until <code>tokens.css</code> is themed.') +
      '<h2>Tokenization status</h2>' +
      '<p>The deterministic, idempotent migrator (<code>_gen/migrate_tokens.py</code>) has tokenized all 201 legacy components:</p>' +
      '<div class="table-wrap"><table class="docs-table"><thead><tr><th>Metric</th><th>Value</th></tr></thead><tbody>' +
      '<tr><td>Components tokenized</td><td>201 / 201</td></tr>' +
      '<tr><td><code>var(--ds-*)</code> references</td><td>654</td></tr>' +
      '<tr><td>Referenced tokens resolving to Swiss values</td><td>24 / 24</td></tr>' +
      '<tr><td>Remaining raw hex (decorative gradients)</td><td>56</td></tr>' +
      '</tbody></table></div>' +
      '<h2>Families</h2>' +
      '<p>The Vanilla collection ships 311 component variants across 47 families, plus 65 neo-brutalist section variants merged into Components:</p>' +
      codeBlock('Vanilla/Components/\n  Accordions/          Buttons/          Cards/\n  Tables/              Modals/           Dropdowns/\n  Tabs/                Navigation/       Tooltips/\n  Loaders/             Forms/            Badges/\n  ... 47 families total\n  tokens.css           DESIGN_TOKENS.md', 'bash') +
      '<h2>Next</h2>' +
      '<p>See <a href="#/components">Components</a> for the family catalog, or <a href="#/design-tokens">Design Tokens</a> for the full token reference.</p>';
  };

  /* ---- COMPONENTS ---- */
  PAGES.components = function (m) {
    return '' +
      '<div class="eyebrow">' + m.eyebrow + '</div><h1>' + m.title + '</h1><p class="lead">' + m.lead + '</p>' +
      '<h2>Families</h2>' +
      '<p>Each family groups related variants and lives under <code>Vanilla/Components/&lt;Family&gt;/</code> or <code>Tailwind/Components/&lt;Family&gt;/</code>. A few representative families:</p>' +
      '<div class="table-wrap"><table class="docs-table"><thead><tr><th>Family</th><th>Variants</th><th>Interactive</th><th>Status</th></tr></thead><tbody>' +
      '<tr><td><strong>Accordions</strong></td><td>single-open, multi, basic</td><td>Yes</td>' + badge('Stable', 'stable') + '</td></tr>' +
      '<tr><td><strong>Buttons</strong></td><td>primary, ghost, icon, loading</td><td>Yes</td>' + badge('Stable', 'stable') + '</td></tr>' +
      '<tr><td><strong>Cards</strong></td><td>article, product, profile</td><td>No</td>' + badge('Stable', 'stable') + '</td></tr>' +
      '<tr><td><strong>Tables</strong></td><td>data, sortable, responsive</td><td>Yes</td>' + badge('Stable', 'stable') + '</td></tr>' +
      '<tr><td><strong>Modals</strong></td><td>dialog, confirm, drawer</td><td>Yes</td>' + badge('Stable', 'stable') + '</td></tr>' +
      '<tr><td><strong>Dropdowns</strong></td><td>menu, select, combobox</td><td>Yes</td>' + badge('Beta', 'beta') + '</td></tr>' +
      '<tr><td><strong>Tabs</strong></td><td>horizontal, vertical, pill</td><td>Yes</td>' + badge('Stable', 'stable') + '</td></tr>' +
      '<tr><td><strong>Navigation</strong></td><td>navbar, breadcrumb, pagination</td><td>Yes</td>' + badge('Stable', 'stable') + '</td></tr>' +
      '<tr><td><strong>Forms</strong></td><td>input, select, checkbox, toggle</td><td>Yes</td>' + badge('Stable', 'stable') + '</td></tr>' +
      '</tbody></table></div>' +
      '<h2>Variant folder convention</h2>' +
      '<p>A Vanilla variant folder is the smallest consumable unit. It always contains:</p>' +
      codeBlock('Vanilla/Components/Accordions/basic/\n  basic.html          # self-contained (inline style + script)\n  metadata.json       # the schema below\n  README.md            # features + usage', 'bash') +
      '<h2>metadata.json schema</h2>' +
      '<p>Every variant ships a metadata file describing it for the index and tooling:</p>' +
      codeBlock('{\n  "name": "Basic Accordion",\n  "slug": "basic",\n  "component": "accordion",\n  "family": "accordions",\n  "variant": "basic",\n  "description": "A single-open accordion using the CSS-grid trick.",\n  "framework": "Vanilla HTML/CSS/JS",\n  "language": "HTML",\n  "tags": ["accordion", "collapse", "faq"],\n  "related": ["single-open"],\n  "features": ["keyboard", "aria", "reduced-motion"]\n}', 'json') +
      callout('info', 'Required keys: <code>name, slug, component, family, variant, description, framework, language, tags, related, features</code>. The <code>slug</code> must equal the folder name.') +
      '<h2>Accordion JS pattern</h2>' +
      '<p>Interactive Vanilla families use a scoped pattern so snippets work standalone. The script scopes itself to its wrapper:</p>' +
      codeBlock('const root = document.currentScript.closest(\'[data-accordion]\');\nroot.querySelectorAll(\'[data-accordion-trigger]\').forEach(btn => {\n  btn.addEventListener(\'click\', () => {\n    const item = btn.closest(\'[data-accordion-item]\');\n    const panel = item.querySelector(\'.panel\');\n    const open = btn.getAttribute(\'aria-expanded\') === \'true\';\n    btn.setAttribute(\'aria-expanded\', String(!open));\n    panel.classList.toggle(\'open\', !open);\n  });\n});', 'js') +
      '<p>Panel animation uses the CSS-grid trick: <code>grid-rows: 0fr</code> toggles to <code>1fr</code> with a transition, wrapped in <code>overflow: hidden</code>.</p>' +
      '<h2>Next</h2>' +
      '<p>For complete page compositions, see <a href="#/templates">Templates</a>. For the token system, see <a href="#/design-tokens">Design Tokens</a>.</p>';
  };

  /* ---- TEMPLATES ---- */
  PAGES.templates = function (m) {
    return '' +
      '<div class="eyebrow">' + m.eyebrow + '</div><h1>' + m.title + '</h1><p class="lead">' + m.lead + '</p>' +
      '<h2>Available templates</h2>' +
      '<p>Templates are complete page or site compositions built from the same design tokens. Each template folder contains a canonical <code>preview.html</code> plus its source files.</p>' +
      '<div class="table-wrap"><table class="docs-table"><thead><tr><th>Template</th><th>Path</th><th>Type</th><th>Status</th></tr></thead><tbody>' +
      '<tr><td><strong>SaaS Dashboard</strong></td><td><code>Vanilla/Templates/SaaS Dashboard/</code></td><td>Single-file</td>' + badge('Stable', 'stable') + '</td></tr>' +
      '<tr><td><strong>Documentation Site</strong></td><td><code>Vanilla/Templates/Documentation Site/</code></td><td>Modular</td>' + badge('Stable', 'stable') + '</td></tr>' +
      '</tbody></table></div>' +
      '<h2>Folder convention</h2>' +
      '<p>A Vanilla template folder contains:</p>' +
      codeBlock('Vanilla/Templates/Documentation Site/\n  code.html            # HTML structure\n  style.css            # the design system\n  script.js            # router + content + interactions\n  preview.html         # canonical single-file preview\n  metadata.json\n  README.md\n  assets/\n    logo.svg\n    favicon.svg', 'bash') +
      callout('note', '<strong>preview.html is the canonical DevSnips preview.</strong> It inlines the CSS and JS so you can open it directly and see exactly how the template looks. The split files (<code>code.html</code>, <code>style.css</code>, <code>script.js</code>) are for development and customization.') +
      '<h2>The shared token spec</h2>' +
      '<p>All Vanilla templates follow <code>Vanilla/Templates/design-tokens.md</code> — the shared design-system source of truth:</p>' +
      '<ul>' +
        '<li><strong>Primitive tokens</strong> — raw values (color, size, weight).</li>' +
        '<li><strong>Semantic tokens</strong> — <code>--ds-*</code> (surface, text, border, accent, status).</li>' +
        '<li><strong>Template tokens</strong> — <code>--template-*</code> (sidebar width, header height, content max).</li>' +
        '<li><strong>Component tokens</strong> — scoped overrides per component.</li>' +
      '</ul>' +
      '<h2>Building a template</h2>' +
      '<ol class="steps">' +
      '<li><h4>Start from the token spec</h4><p>Read <code>design-tokens.md</code> and wire <code>tokens.css</code> first.</p></li>' +
      '<li><h4>Compose from components</h4><p>Templates are built from the same families as standalone components — no special template-only primitives.</p></li>' +
      '<li><h4>Validate</h4><p>Run <code>scripts/validate.py</code> and <code>scripts/qa_vanilla.py</code> before registering.</p></li>' +
      '<li><h4>Register</h4><p>Add the template family to <code>snippets-index.json</code> under <code>category: "Templates"</code>.</p></li>' +
      '</ol>';
  };

  /* ---- DESIGN TOKENS ---- */
  PAGES['design-tokens'] = function (m) {
    return '' +
      '<div class="eyebrow">' + m.eyebrow + '</div><h1>' + m.title + '</h1><p class="lead">' + m.lead + '</p>' +
      '<h2>Token layers</h2>' +
      '<p>The system is layered primitive → semantic → template → component. Each layer references the one below it, so a change at the top cascades everywhere:</p>' +
      codeBlock(':root {\n  /* primitive */\n  --ds-blue-600: #2563eb;\n\n  /* semantic */\n  --ds-accent: var(--ds-blue-600);\n  --ds-text-primary: var(--ds-gray-900);\n\n  /* template */\n  --template-accent: var(--ds-accent);\n  --template-sidebar-width: 264px;\n}', 'css') +
      '<h2>Neutrals</h2>' +
      '<div class="table-wrap"><table class="docs-table"><thead><tr><th>Token</th><th>Light</th><th>Dark</th><th>Used for</th></tr></thead><tbody>' +
      '<tr><td><code>--ds-gray-0</code></td><td>#ffffff</td><td>#111113</td><td>Surface</td></tr>' +
      '<tr><td><code>--ds-gray-50</code></td><td>#fafafa</td><td>#0a0a0b</td><td>Canvas</td></tr>' +
      '<tr><td><code>--ds-gray-100</code></td><td>#f4f4f5</td><td>#18181b</td><td>Sunken</td></tr>' +
      '<tr><td><code>--ds-gray-200</code></td><td>#e4e4e7</td><td>#232327</td><td>Border</td></tr>' +
      '<tr><td><code>--ds-gray-500</code></td><td>#71717a</td><td>#71717a</td><td>Muted text</td></tr>' +
      '<tr><td><code>--ds-gray-900</code></td><td>#18181b</td><td>#ededed</td><td>Primary text</td></tr>' +
      '</tbody></table></div>' +
      '<h2>Accent</h2>' +
      '<p>A single accent — blue-600 — is the DevSnips default. It is used for links, active states, and primary actions. Never violet or neon.</p>' +
      callout('warning', '<strong>Do not override the accent per-component.</strong> Theme the <code>--ds-accent</code> variable in one place; components reference it via <code>var(--ds-accent, #2563eb)</code>.') +
      '<h2>Type scale</h2>' +
      '<div class="table-wrap"><table class="docs-table"><thead><tr><th>Token</th><th>Size</th><th>Typical use</th></tr></thead><tbody>' +
      '<tr><td><code>--ds-text-xs</code></td><td>12px</td><td>Captions, meta, badges</td></tr>' +
      '<tr><td><code>--ds-text-sm</code></td><td>13.5px</td><td>Sidebar nav, secondary</td></tr>' +
      '<tr><td><code>--ds-text-md</code></td><td>15px</td><td>Body</td></tr>' +
      '<tr><td><code>--ds-text-lg</code></td><td>17px</td><td>Lead paragraph</td></tr>' +
      '<tr><td><code>--ds-text-2xl</code></td><td>24px</td><td>Section heading</td></tr>' +
      '<tr><td><code>--ds-text-4xl</code></td><td>36px</td><td>Page title</td></tr>' +
      '</tbody></table></div>' +
      '<h2>Spacing</h2>' +
      '<p>Spacing follows a base-4 scale aligned with Tailwind:</p>' +
      codeBlock('--ds-space-1: 4px;   --ds-space-2: 8px;   --ds-space-3: 12px;\n--ds-space-4: 16px;  --ds-space-5: 20px;  --ds-space-6: 24px;\n--ds-space-8: 32px;  --ds-space-10: 40px; --ds-space-12: 48px;', 'css') +
      '<h2>Radius</h2>' +
      '<p>Small, restrained radii — never pillowy:</p>' +
      codeBlock('--ds-radius-sm: 5px;   --ds-radius-md: 6px;\n--ds-radius-lg: 8px;   --ds-radius-xl: 12px;', 'css') +
      '<h2>Shadow</h2>' +
      '<p>Shadows are subtle and rare — elevation by tone, not by drop shadow:</p>' +
      codeBlock('--ds-shadow-sm: 0 1px 2px rgba(9,9,11,0.05);\n--ds-shadow-md: 0 2px 8px rgba(9,9,11,0.06);', 'css') +
      '<h2>Dark mode</h2>' +
      '<p>The token system ships a dark palette. Toggle it with <code>data-theme="dark"</code> on <code>&lt;html&gt;</code>:</p>' +
      codeBlock('[data-theme="dark"] {\n  --ds-bg-canvas: #0a0a0b;\n  --ds-text-primary: #ededed;\n  --ds-border-default: #232327;\n}', 'css') +
      callout('tip', 'The default is light. A no-flash inline script in <code>&lt;head&gt;</code> reads <code>prefers-color-scheme</code> and persisted preference before first paint.') +
      '<h2>Migrating values</h2>' +
      '<p>The deterministic migrator replaces ad-hoc hex/radius/shadow values with token references:</p>' +
      codeBlock('/* before */\n.foo { color: #18181b; border-radius: 8px; }\n/* after */\n.foo { color: var(--ds-text-primary, #18181b); border-radius: var(--ds-radius-lg, 8px); }', 'css');
  };

  /* ---- GUIDES ---- */
  PAGES.guides = function (m) {
    return '' +
      '<div class="eyebrow">' + m.eyebrow + '</div><h1>' + m.title + '</h1><p class="lead">' + m.lead + '</p>' +
      '<div class="card-grid">' +
      '<a class="doc-card" href="#/design-tokens"><div class="card-icon">' + ic('palette') + '</div><div class="card-title">Theme a component</div><div class="card-desc">Re-color a single component by editing its token references.</div><span class="card-arrow">Guide ' + ic('arrowRight') + '</span></a>' +
      '<a class="doc-card" href="#/components"><div class="card-icon">' + ic('layers') + '</div><div class="card-title">Compose a page</div><div class="card-desc">Build a full page from standalone families.</div><span class="card-arrow">Guide ' + ic('arrowRight') + '</span></a>' +
      '<a class="doc-card" href="#/quick-start"><div class="card-icon">' + ic('terminal') + '</div><div class="card-title">Add interactivity</div><div class="card-desc">Wire scoped vanilla JS to a component.</div><span class="card-arrow">Guide ' + ic('arrowRight') + '</span></a>' +
      '<a class="doc-card" href="#/contributing"><div class="card-icon">' + ic('users') + '</div><div class="card-title">Contribute a component</div><div class="card-desc">Pass the quality bar and register in the index.</div><span class="card-arrow">Guide ' + ic('arrowRight') + '</span></a>' +
      '</div>' +
      '<h2>Scoped JavaScript</h2>' +
      '<p>DevSnips interactive components scope themselves so they work as standalone snippets. The pattern:</p>' +
      codeBlock('const root = document.currentScript.closest(\'[data-widget]\');\nroot.addEventListener(\'click\', (e) => {\n  if (e.target.matches(\'[data-trigger]\')) {\n    /* handle */\n  }\n});', 'js') +
      callout('tip', 'This works because the inline <code>&lt;script&gt;</code> parses inside the root element. <code>document.currentScript</code> refers to the running script, and <code>.closest()</code> walks up to the wrapper.') +
      '<h2>Reduced motion</h2>' +
      '<p>Every animated component must guard its transitions:</p>' +
      codeBlock('@media (prefers-reduced-motion: reduce) {\n  .panel { transition: none; animation: none; }\n}', 'css') +
      '<h2>Accessibility checklist</h2>' +
      '<ul>' +
      '<li>Use native semantics first (<code>&lt;button&gt;</code>, <code>&lt;a&gt;</code>, <code>&lt;details&gt;</code>).</li>' +
      '<li>Add <code>role</code> and <code>aria-*</code> only for custom widgets.</li>' +
      '<li>Every interactive element has a visible <code>:focus-visible</code> ring.</li>' +
      '<li>Keyboard operability: Enter/Space activate, Esc closes, arrow keys navigate lists.</li>' +
      '</ul>';
  };

  /* ---- API REFERENCE ---- */
  PAGES.api = function (m) {
    return '' +
      '<div class="eyebrow">' + m.eyebrow + '</div><h1>' + m.title + '</h1><p class="lead">' + m.lead + '</p>' +
      '<h2>metadata.json</h2>' +
      '<p>The contract every variant ships. Used by the index generator and validation:</p>' +
      apiBlock('metadata.json', '<span class="api-name">metadata.json</span> <span class="api-punct">{ ... }</span>',
        'A JSON file describing a single variant. All keys below are required.',
        [
          { name: 'name', req: true, type: 'string', def: '—', desc: 'Human-readable display name.' },
          { name: 'slug', req: true, type: 'string', def: '—', desc: 'Must equal the folder name.' },
          { name: 'component', req: true, type: 'string', def: '—', desc: 'Singular family noun (e.g. "accordion").' },
          { name: 'family', req: true, type: 'string', def: '—', desc: 'Plural (e.g. "accordions").' },
          { name: 'variant', req: true, type: 'string', def: '—', desc: 'Short variant key (e.g. "basic").' },
          { name: 'framework', req: true, type: 'string', def: '—', desc: '"Tailwind CSS" or "Vanilla HTML/CSS/JS".' },
          { name: 'tags', req: true, type: 'string[]', def: '[]', desc: 'Search tags.' },
          { name: 'features', req: true, type: 'string[]', def: '[]', desc: 'Accessibility/interaction features.' }
        ]) +
      '<h2>Data attributes</h2>' +
      '<p>Interactive families expose a small, consistent set of data attributes:</p>' +
      apiBlock('data-accordion', '<span class="api-name">data-accordion</span><span class="api-punct">=</span><span class="api-type">"name"</span>',
        'Wrapper attribute that scopes an accordion group. The inline script uses it to find its root.',
        [
          { name: 'data-accordion', req: true, type: 'string', def: '—', desc: 'Wrapper; value is a scope name.' },
          { name: 'data-accordion-item', req: true, type: 'boolean', def: '—', desc: 'Marks an item (trigger + panel).' },
          { name: 'data-accordion-trigger', req: true, type: 'boolean', def: '—', desc: 'The toggle button.' },
          { name: 'data-single-open', req: false, type: 'boolean', def: 'false', desc: 'Enables single-open mode.' }
        ]) +
      '<h2>validate.py</h2>' +
      apiBlock('validate.py', '<span class="api-name">python3</span> scripts/validate.py <span class="api-punct">[</span><span class="api-type">--fix</span><span class="api-punct">]</span>',
        'Validates architecture, metadata, and index consistency. Exits 1 on any failure.',
        [
          { name: '--fix', req: false, type: 'flag', def: '—', desc: 'Auto-fix trivial metadata issues.' }
        ],
        codeBlock('$ python3 scripts/validate.py\nVALIDATION PASSED - architecture, metadata, and index all consistent.', 'bash')) +
      '<h2>qa_vanilla.py</h2>' +
      apiBlock('qa_vanilla.py', '<span class="api-name">python3</span> scripts/qa_vanilla.py <span class="api-punct">[</span><span class="api-type">flags</span><span class="api-punct">]</span>',
        'Scans every Vanilla component against the quality bar. Wired into validate.py as a required check.',
        [
          { name: '--only-failures', req: false, type: 'flag', def: '—', desc: 'Print only failing components.' },
          { name: '--json', req: false, type: 'flag', def: '—', desc: 'Machine-readable output.' },
          { name: '--tokens', req: false, type: 'flag', def: '—', desc: 'Report token adoption stats.' }
        ],
        codeBlock('$ python3 scripts/qa_vanilla.py --only-failures\nqa: scanned: 266 components\nqa: failing required checks: 0', 'bash'));
  };

  /* ---- EXAMPLES ---- */
  PAGES.examples = function (m) {
    return '' +
      '<div class="eyebrow">' + m.eyebrow + '</div><h1>' + m.title + '</h1><p class="lead">' + m.lead + '</p>' +
      '<h2>Accordion</h2>' +
      '<p>A single-open accordion using the CSS-grid animation trick:</p>' +
      codeBlock('<div data-accordion="ex" data-single-open>\n  <div data-accordion-item>\n    <button data-accordion-trigger aria-expanded="false">\n      What is DevSnips?\n    </button>\n    <div role="region" class="panel">\n      An open-source, framework-free frontend component library.\n    </div>\n  </div>\n  <div data-accordion-item>\n    <button data-accordion-trigger aria-expanded="false">\n      Is it free?\n    </button>\n    <div role="region" class="panel">\n      Yes — MIT licensed and open for contribution.\n    </div>\n  </div>\n</div>', 'html') +
      '<h2>Card with token references</h2>' +
      '<p>A card that opts into the token system with fallbacks:</p>' +
      codeBlock('<article class="card">\n  <h3>Plan</h3>\n  <p>Styled with var(--ds-*) references.</p>\n</article>\n\n<style>\n.card {\n  background: var(--ds-bg-surface, #fff);\n  border: 1px solid var(--ds-border-default, #e4e4e7);\n  border-radius: var(--ds-radius-md, 6px);\n  padding: var(--ds-space-5, 20px);\n  color: var(--ds-text-primary, #18181b);\n}\n</style>', 'css') +
      callout('tip', 'This card renders correctly standalone (fallbacks apply) <em>and</em> inside the themed system (tokens resolve).') +
      '<h2>Badge</h2>' +
      '<p>Status badges built from semantic tokens:</p>' +
      codeBlock('<span class="badge badge-stable">Stable</span>\n<span class="badge badge-beta">Beta</span>\n<span class="badge badge-deprecated">Deprecated</span>', 'html') +
      '<h2>Responsive table</h2>' +
      '<p>Tables are wrapped in <code>.table-wrap</code> with <code>overflow-x: auto</code> so they never cause page overflow:</p>' +
      codeBlock('<div class="table-wrap">\n  <table class="docs-table">\n    <thead><tr><th>Token</th><th>Value</th></tr></thead>\n    <tbody><tr><td>--ds-accent</td><td>#2563eb</td></tr></tbody>\n  </table>\n</div>', 'html') +
      '<h2>Callout</h2>' +
      codeBlock('<div class="callout callout-tip">\n  <div class="callout-icon"><!-- svg --></div>\n  <div class="callout-body"><strong>Tip.</strong> Re-theme by editing one variable.</div>\n</div>', 'html');
  };

  /* ---- FAQ ---- */
  PAGES.faq = function (m) {
    var items = [
      ['Is DevSnips free?', 'Yes. DevSnips is open-source and MIT licensed. You can use it in personal and commercial projects without restriction.'],
      ['Do I need a framework?', 'No. DevSnips is deliberately framework-free. The Vanilla collection uses semantic HTML, modern CSS, and vanilla JavaScript. The Tailwind collection uses utility classes. Both work without a build step.'],
      ['Do I need a package manager?', 'No. DevSnips is consumed as source files. Clone the repository or copy the folders you need. There is no npm install step for the library itself.'],
      ['How do I re-theme the library?', 'Edit the <code>--ds-*</code> variables in <code>tokens.css</code>. Every component references these tokens with fallbacks, so a single edit re-themes the entire system.'],
      ['What about dark mode?', 'The token system ships a dark palette. Toggle it with <code>data-theme="dark"</code> on <code>&lt;html&gt;</code>. A no-flash script reads <code>prefers-color-scheme</code> before first paint.'],
      ['Are the components accessible?', 'Yes. Every interactive family ships with ARIA, keyboard support, and <code>:focus-visible</code> rings. The quality bar is enforced by <code>scripts/qa_vanilla.py</code>, which is wired into <code>scripts/validate.py</code> as a required check.'],
      ['Can I contribute?', 'Yes — see <a href="#/contributing">Contributing</a>. DevSnips is built in the open. Fork the repo, follow the conventions, pass the quality bar, and open a PR.'],
      ['Why is snippets-index.json generated?', 'The filesystem is the source of truth. <code>snippets-index.json</code> is regenerated from the filesystem by <code>_gen/rebuild_index.py</code> so the index never drifts from the actual content. Hand-editing it is discouraged.']
    ];
    var html = '<div class="eyebrow">' + m.eyebrow + '</div><h1>' + m.title + '</h1><p class="lead">' + m.lead + '</p>';
    items.forEach(function (it) {
      html += '<details class="faq-item"><summary>' + it[0] + ' <span class="chev">' + ic('chevronDown') + '</span></summary><div class="faq-body"><p>' + it[1] + '</p></div></details>';
    });
    return html;
  };

  /* ---- CHANGELOG ---- */
  PAGES.changelog = function (m) {
    var releases = [
      { v: '0.8.0', date: 'Aug 12, 2026', badge: 'New', items: [
        'Added the Documentation Site template (<code>Vanilla/Templates/Documentation Site/</code>).',
        'Split template files into <code>code.html</code>, <code>style.css</code>, <code>script.js</code>.',
        'Light-mode-first design with restrained dark mode.'
      ]},
      { v: '0.7.0', date: 'Aug 10, 2026', badge: 'Migration', items: [
        'Architecture migration to Components + Templates layout.',
        'Merged former Sections into Components across Tailwind and Vanilla.',
        'Regenerated snippets-index.json via _gen/rebuild_index.py.'
      ]},
      { v: '0.6.0', date: 'Jul 28, 2026', badge: 'Enhancement', items: [
        'Tokenized all 201 legacy Vanilla components (was 1.5%).',
        '654 var(--ds-*) references, 24/24 tokens resolve to Swiss values.',
        'Added scripts/qa_vanilla.py quality-bar scanner.'
      ]},
      { v: '0.5.0', date: 'Jul 15, 2026', badge: 'Feature', items: [
        'Added the SaaS Dashboard template.',
        'Introduced Vanilla/Templates/design-tokens.md shared spec.',
        'Registered 90 families / 735 variants.'
      ]},
      { v: '0.4.0', date: 'Jun 30, 2026', badge: 'Feature', items: [
        'Added 165 fifteen-style section components across 11 categories.',
        'Style rotation per category offset for even distribution.',
        'Generated via _gen/ builders.'
      ]}
    ];
    var html = '<div class="eyebrow">' + m.eyebrow + '</div><h1>' + m.title + '</h1><p class="lead">' + m.lead + '</p>';
    releases.forEach(function (r) {
      var kind = r.badge === 'New' ? 'new' : r.badge === 'Migration' ? 'beta' : 'neutral';
      html += '<div class="release"><div class="release-head"><span class="release-version">' + r.v + '</span>' + badge(r.badge, kind) + '<span class="release-date">' + r.date + '</span></div><ul>';
      r.items.forEach(function (it) { html += '<li>' + it + '</li>'; });
      html += '</ul></div>';
    });
    return html;
  };

  /* ---- ROADMAP ---- */
  PAGES.roadmap = function (m) {
    return '' +
      '<div class="eyebrow">' + m.eyebrow + '</div><h1>' + m.title + '</h1><p class="lead">' + m.lead + '</p>' +
      '<div class="table-wrap"><table class="docs-table"><thead><tr><th>Initiative</th><th>Status</th><th>Target</th></tr></thead><tbody>' +
      '<tr><td>React collection</td>' + badge('Planned', 'beta') + '<td>0.9.0</td></tr>' +
      '<tr><td>Form family expansion</td>' + badge('In progress', 'beta') + '<td>0.8.5</td></tr>' +
      '<tr><td>More Vanilla templates</td>' + badge('Planned', 'beta') + '<td>0.9.0</td></tr>' +
      '<tr><td>Interactive playground</td>' + badge('Exploring', 'beta') + '<td>1.0.0</td></tr>' +
      '<tr><td>Token theming UI</td>' + badge('Exploring', 'beta') + '<td>1.0.0</td></tr>' +
      '</tbody></table></div>' +
      '<h2>Near term</h2>' +
      '<ul>' +
      '<li><strong>React collection</strong> — component primitives for React codebases, sharing the same token system.</li>' +
      '<li><strong>Form family</strong> — expand inputs, selects, and validation patterns.</li>' +
      '<li><strong>Templates</strong> — add a landing-page and an admin-panel template.</li>' +
      '</ul>' +
      '<h2>Long term</h2>' +
      '<ul>' +
      '<li><strong>Interactive playground</strong> — edit and preview components in the browser.</li>' +
      '<li><strong>Token theming UI</strong> — generate a custom <code>tokens.css</code> visually.</li>' +
      '</ul>' +
      callout('tip', 'The roadmap is public and driven by contributor interest. To pick something up, open a discussion on GitHub or comment on an existing issue.');
  };

  /* ---- CONTRIBUTING ---- */
  PAGES.contributing = function (m) {
    return '' +
      '<div class="eyebrow">' + m.eyebrow + '</div><h1>' + m.title + '</h1><p class="lead">' + m.lead + '</p>' +
      '<h2>Workflow</h2>' +
      '<ol class="steps">' +
      '<li><h4>Fork & clone</h4><p>Fork <code>sarthakbystander/DevSnips</code> on GitHub and clone your fork locally.</p></li>' +
      '<li><h4>Create a branch</h4><p><code>git checkout -b add-&lt;family&gt;-&lt;variant&gt;</code></p></li>' +
      '<li><h4>Add your component</h4><p>Follow the folder + file convention. Include <code>metadata.json</code>, <code>README.md</code>, and the source files.</p></li>' +
      '<li><h4>Pass the quality bar</h4><p>Run <code>python3 scripts/qa_vanilla.py</code> and ensure zero required failures.</p></li>' +
      '<li><h4>Register & validate</h4><p>Update <code>snippets-index.json</code> and run <code>python3 scripts/validate.py</code>.</p></li>' +
      '<li><h4>Open a PR</h4><p>Push your branch and open a pull request against <code>main</code>.</p></li>' +
      '</ol>' +
      '<h2>Code standards</h2>' +
      '<ul>' +
      '<li>HTML + CSS + vanilla JS only. No React/Vue/Alpine/Bootstrap/jQuery.</li>' +
      '<li>2-space indentation. Semantic HTML.</li>' +
      '<li>Accessibility required: ARIA, keyboard support, focus rings.</li>' +
      '<li>Reduced-motion safe: guard all animations with <code>prefers-reduced-motion</code>.</li>' +
      '<li>Tokenized: use <code>var(--ds-*)</code> with fallbacks, not hardcoded hex.</li>' +
      '</ul>' +
      '<h2>Quality bar</h2>' +
      '<p><code>scripts/qa_vanilla.py</code> enforces four required checks:</p>' +
      '<div class="table-wrap"><table class="docs-table"><thead><tr><th>Check</th><th>Applies to</th><th>Requirement</th></tr></thead><tbody>' +
      '<tr><td><strong>reduced-motion</strong></td><td>Animated components</td><td>Guard transitions/animations with a <code>prefers-reduced-motion</code> rule</td></tr>' +
      '<tr><td><strong>focus-visible</strong></td><td>All components</td><td>A visible <code>:focus-visible</code> ring</td></tr>' +
      '<tr><td><strong>aria/role</strong></td><td>Interactive families</td><td>Custom widgets use <code>role</code>/<code>aria-*</code>; native semantics preferred</td></tr>' +
      '<tr><td><strong>keyboard</strong></td><td>Click-based controls</td><td>Operable via keyboard (button/a/input or tabindex + handlers)</td></tr>' +
      '</tbody></table></div>' +
      '<h2>Validation</h2>' +
      '<p>Before opening a PR, ensure both scripts pass:</p>' +
      codeBlock('python3 scripts/qa_vanilla.py --only-failures\npython3 scripts/validate.py', 'bash') +
      callout('info', 'See the repository <code>CONTRIBUTING.md</code> for the full snippet comment header and detailed conventions.') +
      '<h2>Git conventions</h2>' +
      '<ul>' +
      '<li>Branch naming: <code>add-&lt;family&gt;-&lt;variant&gt;</code> for new components, <code>fix-&lt;topic&gt;</code> for fixes.</li>' +
      '<li>Commit messages: imperative mood, e.g. <code>Add basic accordion variant</code>.</li>' +
      '<li>One PR per logical change. Keep diffs reviewable.</li>' +
      '</ul>';
  };
  /* ============================================================
     RUNTIME — sidebar, router, scrollspy, search, theme, drawer
     ============================================================ */

  /* ---------- build sidebar nav ---------- */
  function buildSidebar() {
    var nav = $('#sidebar-nav');
    if (!nav) return;
    nav.innerHTML = '';
    NAV.forEach(function (grp) {
      var group = el('div', { class: 'nav-group' });
      group.appendChild(el('div', { class: 'nav-group-label' }, grp.group));
      var list = el('ul', { class: 'nav-list' });
      grp.items.forEach(function (item) {
        list.appendChild(navItem(item));
      });
      group.appendChild(list);
      nav.appendChild(group);
    });
  }
  function navItem(item) {
    var li = el('li', { class: 'nav-item' });
    li.setAttribute('data-page', item.id);
    var hasChildren = !!(item.children && item.children.length);
    var link = el('button', { type: 'button', class: 'nav-link', 'data-route': item.id });
    link.innerHTML = '<span>' + item.label + '</span>' + (hasChildren ? '<span class="nav-chev">' + ic('chevron') + '</span>' : '');
    link.addEventListener('click', function () {
      if (hasChildren) li.classList.toggle('expanded');
      go(item.id);
    });
    li.appendChild(link);
    if (hasChildren) {
      var childList = el('ul', { class: 'nav-children' });
      item.children.forEach(function (c) {
        var cli = el('li', { class: 'nav-item', 'data-page': c.id });
        var clink = el('button', { type: 'button', class: 'nav-link', 'data-route': c.id });
        clink.innerHTML = '<span>' + c.label + '</span>';
        clink.addEventListener('click', function () { go(c.id); });
        cli.appendChild(clink);
        childList.appendChild(cli);
      });
      li.appendChild(childList);
    }
    return li;
  }

  /* ---------- breadcrumbs ---------- */
  function buildBreadcrumbs(pageId) {
    var crumbs = [{ label: 'Docs', href: '#/home' }];
    var found = null, parentLabel = null;
    NAV.forEach(function (g) {
      g.items.forEach(function (it) {
        if (it.id === pageId) { found = g.group; }
        if (it.children) it.children.forEach(function (c) {
          if (c.id === pageId) { parentLabel = it.label; found = g.group; }
        });
      });
    });
    if (found) crumbs.push({ label: found });
    if (parentLabel) crumbs.push({ label: parentLabel });
    crumbs.push({ label: META[pageId] ? META[pageId].title : pageId, current: true });
    var out = '<nav class="breadcrumbs" aria-label="Breadcrumb">';
    crumbs.forEach(function (c, i) {
      if (i > 0) out += '<span class="sep">' + ic('chevron') + '</span>';
      if (c.current) out += '<span class="current">' + c.label + '</span>';
      else if (c.href) out += '<a href="' + c.href + '">' + c.label + '</a>';
      else out += '<span>' + c.label + '</span>';
    });
    return out + '</nav>';
  }

  /* ---------- article meta ---------- */
  function buildArticleMeta(m, pageId) {
    if (pageId === 'home') return '';
    var editHref = 'https://github.com/sarthakbystander/DevSnips/edit/main/Vanilla/Templates/Documentation%20Site/script.js';
    return '<div class="article-meta">' +
      '<span class="meta-item">' + ic('clock') + ' Updated ' + m.updated + '</span>' +
      '<span class="meta-sep">·</span>' +
      '<span class="meta-item">' + m.readtime + ' read</span>' +
      '<span class="meta-sep">·</span>' +
      '<a href="' + editHref + '" target="_blank" rel="noopener">' + ic('edit') + ' Edit on GitHub</a>' +
      '</div>';
  }

  /* ---------- prev/next ---------- */
  function buildPager(pageId) {
    var idx = ORDER.indexOf(pageId);
    if (idx < 0) return '';
    var prev = idx > 0 ? ORDER[idx - 1] : null;
    var next = idx < ORDER.length - 1 ? ORDER[idx + 1] : null;
    var out = '<nav class="pager" aria-label="Pagination">';
    if (prev) out += '<a class="pager-prev" href="#/' + prev + '"><span class="pager-label">' + ic('arrowLeft') + ' Previous</span><span class="pager-title">' + (META[prev].title) + '</span></a>';
    else out += '<span></span>';
    if (next) out += '<a class="pager-next" href="#/' + next + '"><span class="pager-label">Next ' + ic('arrowRight') + '</span><span class="pager-title">' + (META[next].title) + '</span></a>';
    return out + '</nav>';
  }

  /* ---------- render page ---------- */
  function renderPage(pageId) {
    var m = META[pageId];
    var root = $('#pages-root');
    if (!m || !root) { if (root) root.innerHTML = '<p>Page not found.</p>'; return; }

    var page = el('div', { class: 'page active fade-in', id: 'page-' + pageId });
    var isHome = pageId === 'home';

    var content = (typeof PAGES[pageId] === 'function') ? PAGES[pageId](m) : '<p>No content.</p>';

    var html = isHome ? content :
      buildBreadcrumbs(pageId) +
      '<div class="eyebrow">' + m.eyebrow + '</div>' +
      '<h1>' + m.title + '</h1>' +
      '<p class="lead">' + m.lead + '</p>' +
      buildArticleMeta(m, pageId) +
      content +
      buildPager(pageId);

    /* mobile TOC toggle (only non-home) */
    if (!isHome) {
      var toggle = el('button', { type: 'button', class: 'toc-mobile-toggle', 'aria-expanded': 'false', 'aria-controls': 'toc-mobile' });
      toggle.innerHTML = '<span>On this page</span><span class="chev">' + ic('chevronDown') + '</span>';
      toggle.addEventListener('click', function () {
        var open = toggle.getAttribute('aria-expanded') === 'true';
        toggle.setAttribute('aria-expanded', String(!open));
        $('#toc-mobile').classList.toggle('open', !open);
      });
      page.appendChild(toggle);
      page.appendChild(el('div', { class: 'toc-mobile', id: 'toc-mobile' }, ''));
    }

    page.appendChild(el('div', { html: html }));
    /* the html above was set via 'html' attr but el() sets innerHTML — rebuild cleanly */
    root.innerHTML = '';
    root.appendChild(page);
    page.querySelector('[html]') ? null : null;

    /* Because el() with 'html' attr sets innerHTML, redo: simpler approach */
    return { page: page, html: html, isHome: isHome, pageId: pageId };
  }

  /* ---------- render page (clean) ---------- */
  function renderPageClean(pageId) {
    var m = META[pageId];
    var root = $('#pages-root');
    if (!m || !root) { if (root) root.innerHTML = '<p>Page not found.</p>'; return []; }

    var isHome = pageId === 'home';
    var content = (typeof PAGES[pageId] === 'function') ? PAGES[pageId](m) : '<p>No content.</p>';

    var html = isHome ? content :
      buildBreadcrumbs(pageId) +
      '<div class="eyebrow">' + m.eyebrow + '</div>' +
      '<h1>' + m.title + '</h1>' +
      '<p class="lead">' + m.lead + '</p>' +
      buildArticleMeta(m, pageId) +
      content +
      buildPager(pageId);

    var page = el('div', { class: 'page active fade-in', id: 'page-' + pageId });
    root.innerHTML = '';
    root.appendChild(page);
    page.innerHTML = html;

    /* mobile TOC toggle */
    if (!isHome) {
      var toggle = el('button', { type: 'button', class: 'toc-mobile-toggle', 'aria-expanded': 'false', 'aria-controls': 'toc-mobile' });
      toggle.innerHTML = '<span>On this page</span><span class="chev">' + ic('chevronDown') + '</span>';
      var tocMobile = el('div', { class: 'toc-mobile', id: 'toc-mobile' });
      /* move toggle + tocMobile to top of page content */
      page.insertBefore(tocMobile, page.firstChild);
      page.insertBefore(toggle, tocMobile);
      toggle.addEventListener('click', function () {
        var open = toggle.getAttribute('aria-expanded') === 'true';
        toggle.setAttribute('aria-expanded', String(!open));
        tocMobile.classList.toggle('open', !open);
      });
    }

    /* collect headings for TOC + scrollspy */
    var headings = $all('h2, h3', page);
    return headings;
  }

  /* ---------- build TOC ---------- */
  function buildTOC(headings) {
    var tocDesktop = $('#toc-list');
    var tocMobile = $('#toc-mobile');
    if (!headings.length) {
      if (tocDesktop) tocDesktop.parentElement.style.display = 'none';
      if (tocMobile) { var t = $('.toc-mobile-toggle'); if (t) t.style.display = 'none'; }
      return;
    }
    var html = '<ul class="toc-list">';
    headings.forEach(function (h, i) {
      if (!h.id) h.id = 'sec-' + i + '-' + (h.textContent.replace(/\s+/g,'-').toLowerCase().slice(0,24));
      var cls = h.tagName === 'H3' ? 'toc-h3' : '';
      html += '<li class="' + cls + '"><a href="#' + h.id + '" data-sec="' + h.id + '">' + esc(h.textContent) + '</a></li>';
    });
    html += '</ul>';
    if (tocDesktop) tocDesktop.innerHTML = html;
    if (tocMobile) tocMobile.innerHTML = html;
  }

  /* ---------- scrollspy ---------- */
  function initScrollspy(headings) {
    if (!headings.length) return;
    var links = $all('[data-sec]');
    function setActive(id) {
      links.forEach(function (l) {
        l.classList.toggle('active', l.getAttribute('data-sec') === id);
      });
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) setActive(e.target.id);
      });
    }, { rootMargin: '-80px 0px -70% 0px', threshold: 0 });
    headings.forEach(function (h) { io.observe(h); });
    /* smooth scroll on click */
    $all('.toc-list a').forEach(function (a) {
      a.addEventListener('click', function (e) {
        var t = $('#' + a.getAttribute('data-sec'));
        if (t) { e.preventDefault(); t.scrollIntoView({ behavior: 'smooth', block: 'start' });
          history.replaceState(null, '', '#' + a.getAttribute('data-sec')); }
      });
    });
  }

  /* ---------- active nav state ---------- */
  function setActiveNav(pageId) {
    $all('.nav-link').forEach(function (l) { l.removeAttribute('aria-current'); });
    var link = $('.nav-link[data-route="' + pageId + '"]');
    if (link) link.setAttribute('aria-current', 'page');
    /* expand parent if child */
    $all('.nav-item').forEach(function (li) {
      var isParent = li.querySelector('.nav-children');
      if (isParent) {
        var childMatch = li.querySelector('.nav-link[data-route="' + pageId + '"]');
        if (childMatch && childMatch.parentElement === li.querySelector('.nav-children')) {
          li.classList.add('expanded');
        } else if (li.getAttribute('data-page') === pageId) {
          li.classList.add('expanded');
        }
      }
    });
  }

  /* ---------- nav filter ---------- */
  function initNavFilter() {
    var input = $('#nav-filter');
    if (!input) return;
    input.addEventListener('input', function () {
      var q = input.value.toLowerCase().trim();
      $all('.nav-item').forEach(function (li) {
        var link = li.querySelector(':scope > .nav-link');
        if (!link) return;
        var text = link.textContent.toLowerCase();
        var match = !q || text.indexOf(q) > -1;
        /* show if matches or any child matches */
        var childMatch = false;
        $all('.nav-children .nav-link', li).forEach(function (cl) {
          cl.parentElement.style.display = (!q || cl.textContent.toLowerCase().indexOf(q) > -1) ? '' : 'none';
          if (cl.textContent.toLowerCase().indexOf(q) > -1) childMatch = true;
        });
        var show = match || childMatch || !q;
        li.style.display = show ? '' : 'none';
        if (childMatch) li.classList.add('expanded');
      });
    });
  }

  /* ---------- code interactions ---------- */
  function initCode(root) {
    /* copy buttons */
    $all('.copy-btn', root).forEach(function (btn) {
      btn.addEventListener('click', function () {
        var id = btn.getAttribute('data-copy');
        var code = $('#' + id);
        if (code) {
          var text = code.textContent;
          if (navigator.clipboard) {
            navigator.clipboard.writeText(text).then(done, done);
          } else {
            var ta = el('textarea'); ta.value = text; document.body.appendChild(ta); ta.select();
            try { document.execCommand('copy'); } catch (e) {} ta.remove(); done();
          }
        }
        function done() { btn.classList.add('copied'); setTimeout(function () { btn.classList.remove('copied'); }, 1600); }
      });
    });
    /* code tabs */
    $all('.code-tabs', root).forEach(function (tabs) {
      var tabsBtns = $all('.code-tab', tabs);
      tabsBtns.forEach(function (tab) {
        tab.addEventListener('click', function () {
          var panelId = tab.getAttribute('aria-controls');
          tabsBtns.forEach(function (t) { t.setAttribute('aria-selected', String(t === tab)); });
          $all('.tab-panel', tabs).forEach(function (p) { p.classList.toggle('active', p.id === panelId); });
        });
      });
    });
  }

  /* ---------- search ---------- */
  var searchState = { active: 0, results: [] };
  function buildSearchIndex() {
    var items = [];
    function walk(label, id, isParent) {
      items.push({ label: label, id: id, path: isParent ? '' : (META[id] ? META[id].title : id) });
    }
    NAV.forEach(function (g) {
      g.items.forEach(function (it) {
        items.push({ label: it.label, id: it.id, group: g.group });
        if (it.children) it.children.forEach(function (c) {
          items.push({ label: c.label, id: c.id, group: g.group + ' / ' + it.label });
        });
      });
    });
    return items;
  }
  function openSearch() {
    var modal = $('#search-modal');
    if (!modal) return;
    modal.classList.add('open');
    var input = $('#search-input');
    if (input) { input.focus(); input.value = ''; renderSearchResults(''); }
  }
  function closeSearch() {
    var modal = $('#search-modal');
    if (modal) modal.classList.remove('open');
  }
  function renderSearchResults(q) {
    var box = $('#search-results');
    if (!box) return;
    q = q.toLowerCase().trim();
    var idx = buildSearchIndex();
    var matches = !q ? idx.slice(0, 6) : idx.filter(function (it) { return it.label.toLowerCase().indexOf(q) > -1 || it.group.toLowerCase().indexOf(q) > -1; });
    searchState.results = matches;
    searchState.active = 0;
    if (!matches.length) { box.innerHTML = '<div class="no-results">No results for "' + esc(q) + '"</div>'; return; }
    /* group */
    var html = '';
    matches.forEach(function (it, i) {
      html += '<a class="result-item' + (i === 0 ? ' active' : '') + '" data-idx="' + i + '" href="#/' + it.id + '">' +
        '<span class="result-label">' + highlightMatch(it.label, q) + '</span>' +
        '<span class="result-path">' + esc(it.group) + '</span></a>';
    });
    box.innerHTML = html;
    $all('.result-item', box).forEach(function (a, i) {
      a.addEventListener('mouseenter', function () { setActiveSearch(i); });
      a.addEventListener('click', function () { closeSearch(); });
    });
  }
  function setActiveSearch(i) {
    searchState.active = i;
    $all('.result-item').forEach(function (a, idx) { a.classList.toggle('active', idx === i); });
    var cur = $('.result-item.active');
    if (cur && cur.scrollIntoView) cur.scrollIntoView({ block: 'nearest' });
  }
  function highlightMatch(text, q) {
    if (!q) return esc(text);
    var i = text.toLowerCase().indexOf(q);
    if (i < 0) return esc(text);
    return esc(text.slice(0, i)) + '<mark>' + esc(text.slice(i, i + q.length)) + '</mark>' + esc(text.slice(i + q.length));
  }

  /* ---------- theme ---------- */
  function initTheme() {
    var stored = null;
    try { stored = localStorage.getItem('ds-docs-theme'); } catch (e) {}
    if (stored === 'dark') document.documentElement.setAttribute('data-theme', 'dark');
    var btn = $('#theme-toggle');
    if (btn) btn.addEventListener('click', function () {
      var cur = document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
      var next = cur === 'dark' ? 'light' : 'dark';
      if (next === 'dark') document.documentElement.setAttribute('data-theme', 'dark');
      else document.documentElement.removeAttribute('data-theme');
      try { localStorage.setItem('ds-docs-theme', next); } catch (e) {}
    });
  }

  /* ---------- drawer ---------- */
  function openDrawer() {
    var sb = $('#sidebar'), bd = $('#drawer-backdrop');
    if (sb) sb.classList.add('open');
    if (bd) bd.classList.add('open');
    document.body.style.overflow = 'hidden';
  }
  function closeDrawer() {
    var sb = $('#sidebar'), bd = $('#drawer-backdrop');
    if (sb) sb.classList.remove('open');
    if (bd) bd.classList.remove('open');
    document.body.style.overflow = '';
  }

  /* ---------- router ---------- */
  function currentRoute() {
    var h = location.hash.replace(/^#\/?/, '');
    if (!h) return 'home';
    /* strip section anchors */
    return h.split('/')[0];
  }
  function go(id) {
    if (location.hash !== '#/' + id) location.hash = '#/' + id;
    else route();
    closeDrawer();
  }
  function route() {
    var pageId = currentRoute();
    if (!META[pageId]) pageId = 'home';
    var headings = renderPageClean(pageId);
    buildTOC(headings);
    initScrollspy(headings);
    initCode($('#pages-root'));
    setActiveNav(pageId);
    /* close mobile TOC */
    var tm = $('#toc-mobile'); if (tm) tm.classList.remove('open');
    var tt = $('.toc-mobile-toggle'); if (tt) tt.setAttribute('aria-expanded', 'false');
    window.scrollTo(0, 0);
  }

  /* ---------- init ---------- */
  function init() {
    document.documentElement.classList.remove('no-js');
    buildSidebar();
    initNavFilter();
    initTheme();
    route();
    window.addEventListener('hashchange', route);

    /* search */
    var trigger = $('#search-trigger');
    if (trigger) trigger.addEventListener('click', openSearch);
    var headerSearch = $('#header-search');
    if (headerSearch) headerSearch.addEventListener('click', openSearch);
    var modal = $('#search-modal');
    if (modal) modal.addEventListener('click', function (e) { if (e.target === modal) closeSearch(); });
    var input = $('#search-input');
    if (input) input.addEventListener('input', function () { renderSearchResults(input.value); });

    /* drawer */
    var mt = $('#menu-toggle');
    if (mt) mt.addEventListener('click', openDrawer);
    var bd = $('#drawer-backdrop');
    if (bd) bd.addEventListener('click', closeDrawer);
    var dc = $('#drawer-close');
    if (dc) dc.addEventListener('click', closeDrawer);
    /* close drawer when resizing up to desktop so scroll-lock never sticks */
    window.addEventListener('resize', function () {
      if (window.innerWidth > 1024) closeDrawer();
    });

    /* keyboard */
    document.addEventListener('keydown', function (e) {
      var searchOpen = $('#search-modal') && $('#search-modal').classList.contains('open');
      if (e.key === 'Escape') {
        if (searchOpen) closeSearch();
        else closeDrawer();
      }
      /* Cmd/Ctrl+K or / opens search */
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); openSearch(); }
      else if (e.key === '/' && !searchOpen && !/^(INPUT|TEXTAREA)$/.test(document.activeElement.tagName)) { e.preventDefault(); openSearch(); }
      /* arrow keys in search */
      if (searchOpen && searchState.results.length) {
        if (e.key === 'ArrowDown') { e.preventDefault(); setActiveSearch(Math.min(searchState.active + 1, searchState.results.length - 1)); }
        if (e.key === 'ArrowUp') { e.preventDefault(); setActiveSearch(Math.max(searchState.active - 1, 0)); }
        if (e.key === 'Enter') { e.preventDefault(); var r = searchState.results[searchState.active]; if (r) { closeSearch(); go(r.id); } }
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
