        (function() {
            'use strict';
            const $ = (s, c) => (c || document).querySelector(s);
            const $a = (s, c) => [...(c || document).querySelectorAll(s)];
            const el = (t, a, h) => { const e = document.createElement(t); if (a)
                    for (const k in a) k === 'class' ? e.className = a[k] : k === 'html' ? e.innerHTML = a[
                        k] : k.startsWith('on') ? e.addEventListener(k.slice(2), a[k]) : e.setAttribute(k, a[
                        k]); if (h != null) e.innerHTML = h; return e; };
            const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
            const IC = {
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
                search: '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
                sun: '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/>',
                moon: '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9z"/>',
                menu: '<path d="M4 6h16M4 12h16M4 18h16"/>',
                close: '<path d="M18 6 6 18M6 6l12 12"/>',
                copy: '<rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>',
                chevron: '<path d="m9 18 6-6-6-6"/>',
                chevronDown: '<path d="m6 9 6 6 6-6"/>',
                arrowRight: '<path d="M5 12h14M12 5l7 7-7 7"/>',
                arrowLeft: '<path d="M19 12H5M12 19l-7-7 7-7"/>',
                lightbulb: '<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6M10 22h4"/>',
                info: '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/>',
                alert: '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3z"/><path d="M12 9v4M12 17h.01"/>',
                xCircle: '<circle cx="12" cy="12" r="10"/><path d="m15 9-6 6M9 9l6 6"/>',
                check: '<path d="M20 6 9 17l-5-5"/>'
            };
            const ic = n => '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' + (
                IC[n] || '') + '</svg>';

            function highlight(code, lang) {
                code = esc(code);
                lang = (lang || '').toLowerCase();
                if (lang === 'html' || lang === 'xml') return code.replace(
                    /(&lt;!--[\s\S]*?--&gt;)/g, '<span class="tok-com">$1</span>').replace(
                    /(&lt;\/?)([a-zA-Z][\w-]*)/g, '$1<span class="tok-tag">$2</span>').replace(
                    /([\w-]+)=(&quot;[^&]*?&quot;|"[^"]*?")/g,
                    '<span class="tok-att">$1</span>=$2').replace(/(&gt;|&lt;\/?)/g,
                    '<span class="tok-pun">$1</span>');
                if (lang === 'css') return code.replace(/(\/\*[\s\S]*?\*\/)/g,
                    '<span class="tok-com">$1</span>').replace(/([\w-]+)(\s*:)/g,
                    '<span class="tok-prop">$1</span>$2').replace(
                    /(#[0-9a-fA-F]{3,8}\b)/g, '<span class="tok-num">$1</span>').replace(
                    /(var\(--[\w-]+\))/g, '<span class="tok-fn">$1</span>').replace(
                    /(@media|@keyframes|@supports|!important)/g,
                    '<span class="tok-key">$1</span>');
                if (lang === 'js' || lang === 'javascript' || lang === 'json') return code.replace(
                    /(\/\/[^\n]*)/g, '<span class="tok-com">$1</span>').replace(
                    /(\/\*[\s\S]*?\*\/)/g, '<span class="tok-com">$1</span>').replace(
                    /(&quot;[^&]*?&quot;|'[^']*?'|`[^`]*?`)/g,
                    '<span class="tok-str">$1</span>').replace(
                    /\b(var|let|const|function|return|if|else|for|while|new|this|class|extends|import|export|from|default|typeof|instanceof|null|undefined|true|false)\b/g,
                    '<span class="tok-key">$1</span>').replace(/\b(\d+)\b/g,
                    '<span class="tok-num">$1</span>').replace(
                    /([a-zA-Z_$][\w$]*)(?=\()/g, '<span class="tok-fn">$1</span>');
                if (lang === 'bash' || lang === 'sh') return code.replace(/(#([^\n]*))/g,
                    '<span class="tok-com">$1</span>').replace(
                    /(^|\s)(npm|pnpm|yarn|git|cd|node|python|pip|curl|mkdir|ls|echo)\b/g,
                    '$1<span class="tok-key">$2</span>').replace(
                    /(--?[a-zA-Z][\w-]*)/g, '<span class="tok-att">$1</span>').replace(
                    /(&quot;[^&]*?&quot;|'[^']*?')/g, '<span class="tok-str">$1</span>');
                return code;
            }

            function codeBlock(codeStr, lang) {
                const id = 'cb' + Math.random().toString(36).slice(2, 8);
                const hl = highlight(codeStr.replace(/^\n/, '').replace(/\s+$/, ''), lang);
                return '<div class="code-block"><div class="code-header"><span class="code-lang">' + esc(lang ||
                    '') +
                    '</span><button type="button" class="copy-btn" data-copy="' + id +
                    '" aria-label="Copy code"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg><span class="copy-label"></span></button></div><pre><code id="' +
                    id + '">' + hl + '</code></pre></div>';
            }

            function codeTabs(tabs) {
                let out = '<div class="code-tabs"><div class="tabs-bar" role="tablist">';
                tabs.forEach((t, i) => { out +=
                        '<button type="button" class="code-tab" role="tab" id="' + t.id + '-tab" aria-selected="' + (
                            i === 0) + '" aria-controls="' + t.id + '">' + esc(t.label) + '</button>'; });
                out += '</div>';
                tabs.forEach((t, i) => { const hl = highlight(t.code.replace(/^\n/, '').replace(/\s+$/, ''),
                        t.lang);
                    out += '<div class="tab-panel' + (i === 0 ? ' active' : '') + '" role="tabpanel" id="' + t
                        .id + '" aria-labelledby="' + t.id + '-tab"><pre><code>' + hl +
                        '</code></pre></div>'; });
                return out + '</div>';
            }

            const NAV = [{ group: 'Start', items: [{ id: 'home', label: 'Documentation Home' }, { id: 'introduction',
                    label: 'Introduction' }, { id: 'getting-started', label: 'Getting Started',
                    children: [{ id: 'installation', label: 'Installation' }, { id: 'quick-start',
                        label: 'Quick Start' }] }, { id: 'vanilla', label: 'Vanilla' }] }, { group: 'Library',
                items: [{ id: 'components', label: 'Components', children: [{ id: 'templates',
                        label: 'Templates' }] }, { id: 'design-tokens', label: 'Design Tokens' }, { id: 'examples',
                    label: 'Examples' }]
            }, { group: 'Reference', items: [{ id: 'guides', label: 'Guides' }, { id: 'api',
                    label: 'API Reference' }, { id: 'faq', label: 'FAQ' }, { id: 'changelog', label: 'Changelog' }] },
            { group: 'Project', items: [{ id: 'roadmap', label: 'Roadmap' }, { id: 'contributing',
                    label: 'Contributing' }] }];
            const ORDER = ['home', 'introduction', 'getting-started', 'installation', 'quick-start', 'vanilla',
                'components', 'templates', 'design-tokens', 'guides', 'api', 'examples', 'faq', 'changelog',
                'roadmap', 'contributing'
            ];
            const META = {
                'home': { eyebrow: 'Welcome', title: 'DevSnips Documentation',
                    lead: 'The open-source, framework-free frontend component library. Copy-paste components, templates, and design tokens — built with HTML, CSS, and vanilla JavaScript.',
                    updated: 'Aug 12, 2026', readtime: '4 min' },
                'introduction': { eyebrow: 'Overview', title: 'Introduction',
                    lead: 'DevSnips is an organized collection of production-ready frontend building blocks. No frameworks, no build step — just semantic HTML, modern CSS, and vanilla JS you can drop into any project.',
                    updated: 'Aug 10, 2026', readtime: '6 min' },
                'getting-started': { eyebrow: 'Start', title: 'Getting Started',
                    lead: 'Everything you need to use DevSnips in a new or existing project. The library is framework-free — this guide covers using the files and tooling directly.',
                    updated: 'Aug 12, 2026', readtime: '5 min' },
                'installation': { eyebrow: 'Setup', title: 'Installation',
                    lead: 'DevSnips is consumed as source files rather than a runtime dependency. Clone the repository or download a release, then reference the files you need.',
                    updated: 'Aug 12, 2026', readtime: '4 min' },
                'quick-start': { eyebrow: 'Start', title: 'Quick Start',
                    lead: 'A two-minute tour: grab a component, wire the tokens, and ship. The fastest path from zero to a styled, accessible UI.',
                    updated: 'Aug 12, 2026', readtime: '3 min' },
                'vanilla': { eyebrow: 'Technology', title: 'Vanilla',
                    lead: 'The Vanilla collection ships framework-free HTML, CSS, and JavaScript. Each component is self-contained and copy-paste ready — no bundler, no compiler, no runtime.',
                    updated: 'Aug 10, 2026', readtime: '7 min' },
                'components': { eyebrow: 'Library', title: 'Components',
                    lead: 'Reusable UI building blocks organized into design-system families: Accordions, Buttons, Cards, Tables, Modals, and more. Every component is accessible, responsive, and tokenized.',
                    updated: 'Aug 12, 2026', readtime: '8 min' },
                'templates': { eyebrow: 'Library', title: 'Templates',
                    lead: 'Complete page and site templates built from the same design tokens. Full compositions — dashboards, documentation sites, landing pages — that demonstrate the system at scale.',
                    updated: 'Aug 12, 2026', readtime: '6 min' },
                'design-tokens': { eyebrow: 'System', title: 'Design Tokens',
                    lead: 'A single canonical token system that makes every DevSnips component speak one visual language. Source of truth: Vanilla/Components/tokens.css and Vanilla/Templates/design-tokens.md.',
                    updated: 'Aug 10, 2026', readtime: '9 min' },
                'guides': { eyebrow: 'Learn', title: 'Guides',
                    lead: 'Practical, hands-on walkthroughs for the most common DevSnips workflows — from theming a single component to composing a full page.',
                    updated: 'Aug 9, 2026', readtime: '10 min' },
                'api': { eyebrow: 'Reference', title: 'API Reference',
                    lead: 'The contracts every DevSnips component and template honors. Metadata schema, data attributes, and the optional JavaScript helpers for interactive families.',
                    updated: 'Aug 12, 2026', readtime: '7 min' },
                'examples': { eyebrow: 'Library', title: 'Examples',
                    lead: 'Annotated, copy-paste examples covering the most-used patterns. Each example is self-contained and renders identically standalone or inside the token system.',
                    updated: 'Aug 8, 2026', readtime: '6 min' },
                'faq': { eyebrow: 'Help', title: 'FAQ',
                    lead: 'Answers to the questions that come up most often. If something is missing, open a discussion on GitHub.',
                    updated: 'Aug 7, 2026', readtime: '5 min' },
                'changelog': { eyebrow: 'History', title: 'Changelog',
                    lead: 'A record of notable changes to the DevSnips library. Versions follow a simple major.minor.patch scheme.',
                    updated: 'Aug 12, 2026', readtime: '4 min' },
                'roadmap': { eyebrow: 'Project', title: 'Roadmap',
                    lead: 'Where DevSnips is headed. The roadmap is public and driven by contributor interest — pick something and open a PR.',
                    updated: 'Aug 6, 2026', readtime: '5 min' },
                'contributing': { eyebrow: 'Project', title: 'Contributing',
                    lead: 'DevSnips is built in the open. This guide covers the contribution workflow, code standards, and the quality bar enforced by scripts/validate.py.',
                    updated: 'Aug 12, 2026', readtime: '8 min' }
            };

            function callout(type, body) {
                const icons = { info: 'info', note: 'book', tip: 'lightbulb', warning: 'alert', danger: 'xCircle' };
                return '<div class="callout callout-' + type + '"><div class="callout-icon">' + ic(icons[type] ||
                    'info') + '</div><div class="callout-body">' + body + '</div></div>';
            }

            function badge(label, kind) { return '<span class="badge badge-' + (kind || 'neutral') + '">' + label +
                    '</span>'; }

            function apiBlock(name, sig, desc, params, example) {
                let p = '';
                if (params && params.length) {
                    p =
                        '<table class="api-params"><thead><tr><th>Param</th><th>Type</th><th>Default</th><th>Description</th></tr></thead><tbody>';
                    params.forEach(r => { p += '<tr><td><code>' + r.name + '</code>' + (r.req ?
                            '<span class="param-req">required</span>' : '') + '</td><td>' + r.type +
                            '</td><td>' + (r.def || '—') + '</td><td>' + r.desc + '</td></tr>'; });
                    p += '</tbody></table>';
                }
                return '<div class="api-block"><div class="api-head"><div class="api-signature">' + sig +
                    '</div></div><div class="api-body"><p>' + desc + '</p>' + p + (example || '') + '</div></div>';
            }

            const PAGES = {
                'home': function(m) {
                    const cards = [
                        { icon: 'book2', title: 'Introduction',
                            desc: 'What DevSnips is and the principles behind a framework-free component library.',
                            href: '#/introduction' }, { icon: 'terminal', title: 'Getting Started',
                            desc: 'Set up a project, install the files, and ship your first component.',
                            href: '#/getting-started' }, { icon: 'palette', title: 'Design Tokens',
                            desc: 'One canonical token system — theme every component from a single file.',
                            href: '#/design-tokens' }, { icon: 'layers', title: 'Components',
                            desc: 'Reusable, accessible building blocks organized into design-system families.',
                            href: '#/components' }, { icon: 'code', title: 'Templates',
                            desc: 'Full page and site compositions — dashboards, docs, landing pages.',
                            href: '#/templates' }, { icon: 'map', title: 'Guides',
                            desc: 'Hands-on walkthroughs for the most common DevSnips workflows.',
                        href: '#/guides' }
                    ];
                    return '<div class="home-hero"><div class="eyebrow">' + m.eyebrow + '</div><h1>' + m.title +
                        '</h1><p class="lead">' + m.lead +
                        '</p><div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:28px"><a class="hero-btn primary" href="#/getting-started">' +
                        ic('terminal') +
                        '<span>Get started</span></a><a class="hero-btn" href="#/components">' + ic('layers') +
                        '<span>Browse components</span></a></div></div><h2>Start here</h2><div class="card-grid">' +
                        cards.map(c =>
                            '<a class="doc-card" href="' + c.href + '"><div class="card-icon">' + ic(c.icon) +
                            '</div><div class="card-title">' + c.title +
                            '</div><div class="card-desc">' + c.desc +
                            '</div><span class="card-arrow">Read more ' + ic('arrowRight') +
                            '</span></a>').join('') +
                        '</div><h2>By technology</h2><p>DevSnips ships three parallel collections:</p><div class="table-wrap"><table class="docs-table"><thead><tr><th>Technology</th><th>Path</th><th>Contents</th><th>Status</th></tr></thead><tbody><tr><td><strong>Tailwind CSS</strong></td><td><code>Tailwind/Components/</code></td><td>535 variants across 59 families</td><td>' +
                        badge('Stable', 'stable') +
                        '</td></tr><tr><td><strong>Vanilla HTML/CSS/JS</strong></td><td><code>Vanilla/Components/</code></td><td>311 variants across 47 families</td><td>' +
                        badge('Stable', 'stable') +
                        '</td></tr><tr><td><strong>React</strong></td><td><code>React/Components/</code></td><td>Reserved for future content</td><td>' +
                        badge('Planned', 'beta') +
                        '</td></tr></tbody></table></div><h2>How DevSnips is organized</h2><p>The library is organized as design-system <strong>families</strong>. A family groups related variants.</p>' +
                        callout('tip',
                            '<strong>Grand total:</strong> 846 content items across 106 families. Tailwind leads with 535 variants; Vanilla follows with 311.'
                            ) + '<h2>Next steps</h2><p>Read the <a href="#/introduction">introduction</a>, jump to <a href="#/quick-start">quick start</a>, or explore the <a href="#/design-tokens">design tokens</a>.</p>';
                },
                'introduction': function(m) {
                    return '<div class="eyebrow">' + m.eyebrow + '</div><h1>' + m.title + '</h1><p class="lead">' + m
                        .lead +
                        '</p><h2>What is DevSnips?</h2><p>DevSnips is an open-source frontend component library built on three principles: <strong>framework-free</strong>, <strong>copy-paste ready</strong>, and <strong>token-driven</strong>.</p>' +
                        '<h2>Why framework-free?</h2><p>Most component libraries lock you into a framework. DevSnips deliberately does not.</p>' +
                        callout('info',
                            '<strong>Design tokens are the contract.</strong> Every component opts into the <code>--ds-*</code> token system with a CSS-variable fallback.'
                            ) +
                        '<h2>Three collections</h2><div class="table-wrap"><table class="docs-table"><thead><tr><th>Collection</th><th>Approach</th><th>Best for</th></tr></thead><tbody><tr><td><strong>Tailwind</strong></td><td>Utility classes + CDN</td><td>Rapid prototyping</td></tr><tr><td><strong>Vanilla</strong></td><td>Semantic HTML + scoped CSS/JS</td><td>Copy-paste fragments, no build step</td></tr><tr><td><strong>React</strong></td><td>Component primitives (planned)</td><td>React codebases</td></tr></tbody></table></div>' +
                        '<h2>Design principles</h2><ul><li><strong>Accessibility first.</strong> ARIA, keyboard support, focus rings.</li><li><strong>Copy-paste standalone.</strong> No missing dependencies.</li><li><strong>Tokenized, not hardcoded.</strong> Re-theme by editing one file.</li><li><strong>Reduced-motion safe.</strong> Every animation guarded.</li></ul>' +
                        '<h2>The repository layout</h2>' + codeBlock(
                            'DevSnips/\n  Tailwind/Components/   # 535 variants, 59 families\n  Vanilla/Components/    # 311 variants, 47 families\n  snippets-index.json\n  scripts/validate.py', 'bash') +
                        '<h2>Where to go next</h2><ul><li><a href="#/getting-started">Getting Started</a></li><li><a href="#/design-tokens">Design Tokens</a></li><li><a href="#/components">Components</a></li></ul>';
                },
                'getting-started': function(m) {
                    return '<div class="eyebrow">' + m.eyebrow + '</div><h1>' + m.title + '</h1><p class="lead">' + m
                        .lead +
                        '</p><h2>Prerequisites</h2><ul><li>A modern browser</li><li>Python 3.8+ to run validation scripts</li><li>Git to clone the repository</li></ul>' +
                        callout('info',
                            'No Node.js, no bundler, no package manager required to <em>use</em> DevSnips.') +
                        '<h2>Get the code</h2>' + codeBlock(
                            'git clone https://github.com/sarthakbystander/DevSnips.git\ncd DevSnips', 'bash') +
                        '<h2>Validate your copy</h2>' + codeBlock('python3 scripts/validate.py', 'bash') +
                        '<p>You should see <code>VALIDATION PASSED</code>.</p>' +
                        '<h2>Use a component</h2><ol class="steps"><li><h4>Copy the variant folder</h4><p>Copy a component folder into your project.</p></li><li><h4>Reference the files</h4><p>Link the CSS and JS.</p></li><li><h4>Include the tokens (optional)</h4><p>Add tokens.css once to theme every component together.</p></li></ol>' +
                        '<p>For the full path see <a href="#/quick-start">Quick Start</a>.</p>';
                },
                'installation': function(m) {
                    return '<div class="eyebrow">' + m.eyebrow + '</div><h1>' + m.title + '</h1><p class="lead">' + m
                        .lead +
                        '</p><h2>Option 1: Clone the repository</h2>' + codeTabs([{ id: 'inst-git',
                            label: 'git', lang: 'bash',
                            code: 'git clone https://github.com/sarthakbystander/DevSnips.git\ncd DevSnips\npython3 scripts/validate.py'
                        }, { id: 'inst-curl', label: 'curl', lang: 'bash',
                            code: 'curl -L https://github.com/sarthakbystander/DevSnips/archive/refs/heads/main.tar.gz | tar xz\nmv DevSnips-main DevSnips'
                        }]) + '<h2>Option 2: Copy a single component</h2>' + codeBlock(
                            'cp -r Vanilla/Components/Accordions/basic/ ./my-project/', 'bash') +
                        callout('tip',
                            '<strong>Link tokens once.</strong> Add <code>&lt;link rel="stylesheet" href="css/tokens.css"&gt;</code> in your <code>&lt;head&gt;</code>.'
                            ) + '<h2>Verify</h2>' + codeBlock('python3 scripts/qa_vanilla.py --only-failures', 'bash');
                },
                'quick-start': function(m) {
                    return '<div class="eyebrow">' + m.eyebrow + '</div><h1>' + m.title + '</h1><p class="lead">' + m
                        .lead +
                        '</p><h2>1. Grab a component</h2>' + codeBlock(
                            'cp -r Vanilla/Components/Accordions/basic/ ./my-project/', 'bash') +
                        '<h2>2. Wire the tokens</h2>' + codeBlock(
                            '<link rel="stylesheet" href="css/tokens.css">', 'html') +
                        '<h2>3. Add the markup</h2>' + codeBlock(
                            '<div data-accordion="basic">\n  <button data-accordion-trigger aria-expanded="false">What is DevSnips?</button>\n  <div role="region" class="panel">An open-source, framework-free component library.</div>\n</div>',
                            'html') + '<h2>4. Add the script</h2>' + codeBlock(
                            'const root = document.currentScript.closest(\'[data-accordion]\');\nroot.querySelectorAll(\'[data-accordion-trigger]\').forEach(btn => {\n  btn.addEventListener(\'click\', () => {\n    const open = btn.getAttribute(\'aria-expanded\') === \'true\';\n    btn.setAttribute(\'aria-expanded\', String(!open));\n  });\n});',
                            'js') + callout('tip',
                            '<strong>That\'s it.</strong> The accordion now toggles, is keyboard-operable, and respects <code>prefers-reduced-motion</code>.'
                            ) + '<h2>Re-theme everything</h2>' + codeBlock(
                            ':root {\n  --ds-accent: #2563eb;\n}', 'css');
                },
                'vanilla': function(m) {
                    return '<div class="eyebrow">' + m.eyebrow + '</div><h1>' + m.title + '</h1><p class="lead">' + m
                        .lead +
                        '</p><h2>Convention</h2><div class="table-wrap"><table class="docs-table"><thead><tr><th>File</th><th>Purpose</th></tr></thead><tbody><tr><td><code>&lt;slug&gt;.html</code></td><td>Self-contained page</td></tr><tr><td><code>metadata.json</code></td><td>Name, slug, tags, features</td></tr><tr><td><code>README.md</code></td><td>Features, usage, browser support</td></tr></tbody></table></div>' +
                        '<h2>The Swiss design tokens</h2><p>One canonical token system. Source of truth: <code>Vanilla/Components/tokens.css</code>.</p>' +
                        callout('note',
                            'Components opt in with <code>var(--ds-&lt;token&gt;, &lt;original-value&gt;)</code>.') +
                        '<h2>Families</h2><p>311 variants across 47 families.</p>' + codeBlock(
                            'Vanilla/Components/\n  Accordions/  Buttons/  Cards/\n  Tables/  Modals/  Dropdowns/\n  ... 47 families total',
                            'bash');
                },
                'components': function(m) {
                    return '<div class="eyebrow">' + m.eyebrow + '</div><h1>' + m.title + '</h1><p class="lead">' + m
                        .lead +
                        '</p><h2>Families</h2><div class="table-wrap"><table class="docs-table"><thead><tr><th>Family</th><th>Variants</th><th>Status</th></tr></thead><tbody><tr><td><strong>Accordions</strong></td><td>single-open, multi, basic</td><td>' +
                        badge('Stable', 'stable') +
                        '</td></tr><tr><td><strong>Buttons</strong></td><td>primary, ghost, icon, loading</td><td>' +
                        badge('Stable', 'stable') +
                        '</td></tr><tr><td><strong>Cards</strong></td><td>article, product, profile</td><td>' + badge(
                            'Stable', 'stable') +
                        '</td></tr><tr><td><strong>Tables</strong></td><td>data, sortable, responsive</td><td>' +
                        badge('Stable', 'stable') +
                        '</td></tr><tr><td><strong>Modals</strong></td><td>dialog, confirm, drawer</td><td>' + badge(
                            'Stable', 'stable') +
                        '</td></tr></tbody></table></div><h2>Variant folder convention</h2>' + codeBlock(
                            'Vanilla/Components/Accordions/basic/\n  basic.html\n  metadata.json\n  README.md',
                            'bash') + '<h2>metadata.json schema</h2>' + codeBlock(
                            '{\n  "name": "Basic Accordion",\n  "slug": "basic",\n  "family": "accordions",\n  "tags": ["accordion", "collapse"],\n  "features": ["keyboard", "aria"]\n}',
                            'json');
                },
                'templates': function(m) {
                    return '<div class="eyebrow">' + m.eyebrow + '</div><h1>' + m.title + '</h1><p class="lead">' + m
                        .lead +
                        '</p><h2>Available templates</h2><div class="table-wrap"><table class="docs-table"><thead><tr><th>Template</th><th>Path</th><th>Status</th></tr></thead><tbody><tr><td><strong>SaaS Dashboard</strong></td><td><code>Vanilla/Templates/SaaS Dashboard/</code></td><td>' +
                        badge('Stable', 'stable') +
                        '</td></tr><tr><td><strong>Documentation Site</strong></td><td><code>Vanilla/Templates/Documentation Site/</code></td><td>' +
                        badge('Stable', 'stable') +
                        '</td></tr></tbody></table></div><h2>Folder convention</h2>' + codeBlock(
                            'Vanilla/Templates/Documentation Site/\n  code.html\n  style.css\n  script.js\n  preview.html\n  metadata.json',
                            'bash');
                },
                'design-tokens': function(m) {
                    return '<div class="eyebrow">' + m.eyebrow + '</div><h1>' + m.title + '</h1><p class="lead">' + m
                        .lead +
                        '</p><h2>Token layers</h2><p>Primitive → semantic → template → component:</p>' + codeBlock(
                            ':root {\n  --ds-blue-600: #2563eb;\n  --ds-accent: var(--ds-blue-600);\n  --ds-text-primary: var(--ds-gray-900);\n}',
                            'css') +
                        '<h2>Neutrals</h2><div class="table-wrap"><table class="docs-table"><thead><tr><th>Token</th><th>Light</th><th>Dark</th></tr></thead><tbody><tr><td><code>--ds-gray-0</code></td><td>#ffffff</td><td>#141618</td></tr><tr><td><code>--ds-gray-50</code></td><td>#f8f9fa</td><td>#0d0e10</td></tr><tr><td><code>--ds-gray-900</code></td><td>#141618</td><td>#e9ecef</td></tr></tbody></table></div>' +
                        '<h2>Dark mode</h2>' + codeBlock(
                            '[data-theme="dark"] {\n  --ds-bg-canvas: #0d0e10;\n  --ds-text-primary: #e9ecef;\n}',
                            'css');
                },
                'guides': function(m) {
                    return '<div class="eyebrow">' + m.eyebrow + '</div><h1>' + m.title + '</h1><p class="lead">' + m
                        .lead +
                        '</p><div class="card-grid"><a class="doc-card" href="#/design-tokens"><div class="card-icon">' +
                        ic('palette') +
                        '</div><div class="card-title">Theme a component</div><div class="card-desc">Re-color a single component by editing its token references.</div><span class="card-arrow">Guide ' +
                        ic('arrowRight') +
                        '</span></a><a class="doc-card" href="#/components"><div class="card-icon">' + ic(
                            'layers') +
                        '</div><div class="card-title">Compose a page</div><div class="card-desc">Build a full page from standalone families.</div><span class="card-arrow">Guide ' +
                        ic('arrowRight') +
                        '</span></a></div><h2>Scoped JavaScript</h2>' + codeBlock(
                            'const root = document.currentScript.closest(\'[data-widget]\');\nroot.addEventListener(\'click\', (e) => {\n  if (e.target.matches(\'[data-trigger]\')) { /* handle */ }\n});',
                            'js') +
                        '<h2>Accessibility checklist</h2><ul><li>Use native semantics first</li><li>ARIA only for custom widgets</li><li>Visible focus rings</li><li>Keyboard operability</li></ul>';
                },
                'api': function(m) {
                    return '<div class="eyebrow">' + m.eyebrow + '</div><h1>' + m.title + '</h1><p class="lead">' + m
                        .lead + '</p>' + apiBlock('metadata.json',
                            '<span class="api-name">metadata.json</span> <span class="api-punct">{ ... }</span>',
                            'A JSON file describing a single variant.', [{ name: 'name', req: true,
                                type: 'string', def: '—', desc: 'Human-readable display name.' }, { name: 'slug',
                                req: true, type: 'string', def: '—',
                                desc: 'Must equal the folder name.' }]) + '<h2>Data attributes</h2>' + apiBlock(
                            'data-accordion',
                            '<span class="api-name">data-accordion</span><span class="api-punct">=</span><span class="api-type">"name"</span>',
                            'Wrapper attribute that scopes an accordion group.', [{ name: 'data-accordion',
                                req: true, type: 'string', def: '—', desc: 'Wrapper scope name.' }]) +
                        '<h2>validate.py</h2>' + apiBlock('validate.py',
                            '<span class="api-name">python3</span> scripts/validate.py',
                            'Validates architecture, metadata, and index consistency.', [], codeBlock(
                                '$ python3 scripts/validate.py\nVALIDATION PASSED', 'bash'));
                },
                'examples': function(m) {
                    return '<div class="eyebrow">' + m.eyebrow + '</div><h1>' + m.title + '</h1><p class="lead">' + m
                        .lead + '</p><h2>Accordion</h2>' + codeBlock(
                            '<div data-accordion="ex" data-single-open>\n  <button data-accordion-trigger aria-expanded="false">What is DevSnips?</button>\n  <div role="region" class="panel">An open-source component library.</div>\n</div>',
                            'html') + '<h2>Card with tokens</h2>' + codeBlock(
                            '<article class="card">\n  <h3>Plan</h3>\n  <p>Styled with var(--ds-*) references.</p>\n</article>',
                            'html') + '<h2>Badge</h2>' + codeBlock(
                            '<span class="badge badge-stable">Stable</span>', 'html');
                },
                'faq': function(m) {
                    const items = [
                        ['Is DevSnips free?',
                            'Yes. DevSnips is open-source and MIT licensed.'], ['Do I need a framework?',
                            'No. DevSnips is deliberately framework-free.'
                        ], ['How do I re-theme the library?',
                            'Edit the <code>--ds-*</code> variables in <code>tokens.css</code>.'],
                        ['Are the components accessible?',
                            'Yes. Every interactive family ships with ARIA, keyboard support, and focus rings.'
                            ], ['Can I contribute?', 'Yes — see <a href="#/contributing">Contributing</a>.']];
                    let html = '<div class="eyebrow">' + m.eyebrow + '</div><h1>' + m.title +
                        '</h1><p class="lead">' + m.lead + '</p>';
                    items.forEach(it => { html +=
                            '<details class="faq-item"><summary>' + it[0] + ' <span class="chev">' + ic(
                                'chevronDown') + '</span></summary><div class="faq-body"><p>' + it[1] +
                            '</p></div></details>'; });
                    return html;
                },
                'changelog': function(m) {
                    const rels = [{ v: '0.8.0', date: 'Aug 12, 2026', badge: 'New',
                        items: ['Added Documentation Site template.', 'Light-mode-first design.']
                    }, { v: '0.7.0', date: 'Aug 10, 2026', badge: 'Migration',
                        items: ['Architecture migration to Components + Templates.']
                    }, { v: '0.6.0', date: 'Jul 28, 2026', badge: 'Enhancement',
                        items: ['Tokenized all 201 legacy Vanilla components.']
                    }, { v: '0.5.0', date: 'Jul 15, 2026', badge: 'Feature',
                    items: ['Added SaaS Dashboard template.'] }];
                    let html = '<div class="eyebrow">' + m.eyebrow + '</div><h1>' + m.title +
                        '</h1><p class="lead">' + m.lead + '</p>';
                    rels.forEach(r => { const kind = r.badge === 'New' ? 'new' : r.badge === 'Migration' ?
                            'beta' : 'neutral';
                        html += '<div class="release"><div class="release-head"><span class="release-version">' +
                            r.v + '</span>' + badge(r.badge, kind) + '<span class="release-date">' + r.date +
                            '</span></div><ul>';
                        r.items.forEach(it => { html += '<li>' + it + '</li>'; });
                        html += '</ul></div>'; });
                    return html;
                },
                'roadmap': function(m) {
                    return '<div class="eyebrow">' + m.eyebrow + '</div><h1>' + m.title + '</h1><p class="lead">' + m
                        .lead +
                        '</p><div class="table-wrap"><table class="docs-table"><thead><tr><th>Initiative</th><th>Status</th><th>Target</th></tr></thead><tbody><tr><td>React collection</td><td>' +
                        badge('Planned', 'beta') +
                        '</td><td>0.9.0</td></tr><tr><td>Form family expansion</td><td>' + badge('In progress',
                            'beta') +
                        '</td><td>0.8.5</td></tr><tr><td>Interactive playground</td><td>' + badge('Exploring',
                            'beta') +
                        '</td><td>1.0.0</td></tr></tbody></table></div><h2>Near term</h2><ul><li><strong>React collection</strong> — component primitives.</li><li><strong>Form family</strong> — expand inputs and selects.</li></ul>' +
                        callout('tip',
                        'The roadmap is public and driven by contributor interest.');
                },
                'contributing': function(m) {
                    return '<div class="eyebrow">' + m.eyebrow + '</div><h1>' + m.title + '</h1><p class="lead">' + m
                        .lead +
                        '</p><h2>Workflow</h2><ol class="steps"><li><h4>Fork & clone</h4><p>Fork the repo on GitHub.</p></li><li><h4>Create a branch</h4><p><code>git checkout -b add-family-variant</code></p></li><li><h4>Add your component</h4><p>Follow the folder convention.</p></li><li><h4>Pass the quality bar</h4><p>Run <code>python3 scripts/qa_vanilla.py</code></p></li><li><h4>Open a PR</h4><p>Push and open a pull request.</p></li></ol>' +
                        '<h2>Code standards</h2><ul><li>HTML + CSS + vanilla JS only</li><li>2-space indentation</li><li>Accessibility required</li><li>Tokenized with fallbacks</li></ul>' +
                        '<h2>Validation</h2>' + codeBlock(
                            'python3 scripts/qa_vanilla.py --only-failures\npython3 scripts/validate.py', 'bash');
                }
            };

            function buildSidebar() {
                const nav = $('#sidebar-nav');
                if (!nav) return;
                nav.innerHTML = '';
                NAV.forEach(grp => {
                    const group = el('div', { class: 'nav-group' });
                    group.appendChild(el('div', { class: 'nav-group-label' }, grp.group));
                    const list = el('ul', { class: 'nav-list' });
                    grp.items.forEach(item => list.appendChild(navItem(item)));
                    group.appendChild(list);
                    nav.appendChild(group);
                });
            }

            function navItem(item) {
                const li = el('li', { class: 'nav-item', 'data-page': item.id });
                const hasChildren = !!(item.children && item.children.length);
                const link = el('button', { type: 'button', class: 'nav-link', 'data-route': item.id });
                link.innerHTML = '<span>' + item.label + '</span>' + (hasChildren ? '<span class="nav-chev">' + ic(
                    'chevron') + '</span>' : '');
                link.addEventListener('click', () => {
                    if (hasChildren) li.classList.toggle('expanded');
                    go(item.id);
                });
                li.appendChild(link);
                if (hasChildren) {
                    const childList = el('ul', { class: 'nav-children' });
                    item.children.forEach(c => {
                        const cli = el('li', { class: 'nav-item', 'data-page': c.id });
                        const clink = el('button', { type: 'button', class: 'nav-link',
                        'data-route': c.id });
                        clink.innerHTML = '<span>' + c.label + '</span>';
                        clink.addEventListener('click', () => go(c.id));
                        cli.appendChild(clink);
                        childList.appendChild(cli);
                    });
                    li.appendChild(childList);
                }
                return li;
            }

            function buildBreadcrumbs(pageId) {
                const crumbs = [{ label: 'Docs', href: '#/home' }];
                let found = null,
                    parentLabel = null;
                NAV.forEach(g => g.items.forEach(it => {
                    if (it.id === pageId) found = g.group;
                    if (it.children) it.children.forEach(c => { if (c.id === pageId) { parentLabel =
                                it.label;
                            found = g.group; } });
                }));
                if (found) crumbs.push({ label: found });
                if (parentLabel) crumbs.push({ label: parentLabel });
                crumbs.push({ label: META[pageId] ? META[pageId].title : pageId, current: true });
                let out = '<nav class="breadcrumbs" aria-label="Breadcrumb">';
                crumbs.forEach((c, i) => {
                    if (i > 0) out += '<span class="sep">' + ic('chevron') + '</span>';
                    if (c.current) out += '<span class="current">' + c.label + '</span>';
                    else if (c.href) out += '<a href="' + c.href + '">' + c.label + '</a>';
                    else out += '<span>' + c.label + '</span>';
                });
                return out + '</nav>';
            }

            function buildArticleMeta(m) {
                return '<div class="article-meta"><span class="meta-item">' + ic('clock') + ' Updated ' + m.updated +
                    '</span><span class="meta-sep">·</span><span class="meta-item">' + m.readtime +
                    ' read</span></div>';
            }

            function buildPager(pageId) {
                const idx = ORDER.indexOf(pageId);
                if (idx < 0) return '';
                const prev = idx > 0 ? ORDER[idx - 1] : null;
                const next = idx < ORDER.length - 1 ? ORDER[idx + 1] : null;
                let out = '<nav class="pager" aria-label="Pagination">';
                if (prev) out += '<a class="pager-prev" href="#/' + prev +
                    '"><span class="pager-label">' + ic('arrowLeft') + ' Previous</span><span class="pager-title">' +
                    META[prev].title + '</span></a>';
                else out += '<span></span>';
                if (next) out += '<a class="pager-next" href="#/' + next +
                    '"><span class="pager-label">Next ' + ic('arrowRight') +
                    '</span><span class="pager-title">' + META[next].title + '</span></a>';
                return out + '</nav>';
            }

            function renderPageClean(pageId) {
                const m = META[pageId];
                const root = $('#pages-root');
                if (!m || !root) { if (root) root.innerHTML = '<p>Page not found.</p>'; return []; }
                const isHome = pageId === 'home';
                const content = (typeof PAGES[pageId] === 'function') ? PAGES[pageId](m) :
                '<p>No content.</p>';
                const html = isHome ? content : buildBreadcrumbs(pageId) + '<div class="eyebrow">' + m.eyebrow +
                    '</div><h1>' + m.title + '</h1><p class="lead">' + m.lead + '</p>' + buildArticleMeta(m) +
                    content + buildPager(pageId);
                const page = el('div', { class: 'page active fade-in', id: 'page-' + pageId });
                root.innerHTML = '';
                root.appendChild(page);
                page.innerHTML = html;
                if (!isHome) {
                    const toggle = el('button', { type: 'button', class: 'toc-mobile-toggle',
                        'aria-expanded': 'false', 'aria-controls': 'toc-mobile' });
                    toggle.innerHTML = '<span>On this page</span><span class="chev">' + ic('chevronDown') +
                        '</span>';
                    const tocMobile = el('div', { class: 'toc-mobile', id: 'toc-mobile' });
                    page.insertBefore(tocMobile, page.firstChild);
                    page.insertBefore(toggle, tocMobile);
                    toggle.addEventListener('click', () => {
                        const open = toggle.getAttribute('aria-expanded') === 'true';
                        toggle.setAttribute('aria-expanded', String(!open));
                        tocMobile.classList.toggle('open', !open);
                    });
                }
                return $a('h2, h3', page);
            }

            function buildTOC(headings) {
                const tocDesktop = $('#toc-list');
                const tocMobile = $('#toc-mobile');
                const toggleEl = $('.toc-mobile-toggle');
                if (!headings.length) {
                    if (tocDesktop) tocDesktop.parentElement.style.display = 'none';
                    if (tocMobile && toggleEl) { tocMobile.style.display = 'none';
                        toggleEl.style.display = 'none'; }
                    return;
                }
                let html = '<ul class="toc-list">';
                headings.forEach((h, i) => {
                    if (!h.id) h.id = 'sec-' + i + '-' + (h.textContent.replace(/\s+/g, '-').toLowerCase()
                        .slice(0, 24));
                    const cls = h.tagName === 'H3' ? 'toc-h3' : '';
                    html += '<li class="' + cls + '"><a href="#' + h.id + '" data-sec="' + h.id + '">' + esc(h
                        .textContent) + '</a></li>';
                });
                html += '</ul>';
                if (tocDesktop) tocDesktop.innerHTML = html;
                if (tocMobile) tocMobile.innerHTML = html;
            }

            function initScrollspy(headings) {
                if (!headings.length) return;
                const links = $a('[data-sec]');
                const setActive = id => links.forEach(l => l.classList.toggle('active', l.getAttribute('data-sec') ===
                    id));
                const io = new IntersectionObserver(entries => entries.forEach(e => { if (e.isIntersecting) setActive(e
                        .target.id); }), { rootMargin: '-80px 0px -70% 0px', threshold: 0 });
                headings.forEach(h => io.observe(h));
                $a('.toc-list a').forEach(a => a.addEventListener('click', function(e) {
                    const t = $('#' + a.getAttribute('data-sec'));
                    if (t) { e.preventDefault();
                        t.scrollIntoView({ behavior: 'smooth', block: 'start' });
                        history.replaceState(null, '', '#' + a.getAttribute('data-sec')); }
                }));
            }

            function setActiveNav(pageId) {
                $a('.nav-link').forEach(l => l.removeAttribute('aria-current'));
                const link = $('.nav-link[data-route="' + pageId + '"]');
                if (link) link.setAttribute('aria-current', 'page');
                $a('.nav-item').forEach(li => {
                    const isParent = li.querySelector('.nav-children');
                    if (isParent) {
                        const childMatch = li.querySelector('.nav-children .nav-link[data-route="' + pageId +
                            '"]');
                        if (childMatch) li.classList.add('expanded');
                        else if (li.getAttribute('data-page') === pageId) li.classList.add('expanded');
                    }
                });
            }

            function initNavFilter() {
                const input = $('#nav-filter');
                if (!input) return;
                input.addEventListener('input', () => {
                    const q = input.value.toLowerCase().trim();
                    $a('.nav-item').forEach(li => {
                        const link = li.querySelector(':scope > .nav-link');
                        if (!link) return;
                        const text = link.textContent.toLowerCase();
                        const match = !q || text.includes(q);
                        let childMatch = false;
                        $a('.nav-children .nav-link', li).forEach(cl => {
                            cl.parentElement.style.display = (!q || cl.textContent
                                .toLowerCase().includes(q)) ? '' : 'none';
                            if (cl.textContent.toLowerCase().includes(q)) childMatch =
                                true;
                        });
                        li.style.display = (match || childMatch || !q) ? '' : 'none';
                        if (childMatch) li.classList.add('expanded');
                    });
                });
            }

            function initCode(root) {
                $a('.copy-btn', root).forEach(btn => btn.addEventListener('click', function() {
                    const id = btn.getAttribute('data-copy');
                    const code = $('#' + id);
                    if (code) {
                        const text = code.textContent;
                        const done = () => { btn.classList.add('copied');
                            setTimeout(() => btn.classList.remove('copied'), 1600); };
                        if (navigator.clipboard) navigator.clipboard.writeText(text).then(done, done);
                        else { const ta = el('textarea');
                            ta.value = text;
                            document.body.appendChild(ta);
                            ta.select(); try { document.execCommand('copy'); } catch (e) {} ta.remove();
                            done(); }
                    }
                }));
                $a('.code-tabs', root).forEach(tabs => {
                    const btns = $a('.code-tab', tabs);
                    btns.forEach(tab => tab.addEventListener('click', () => {
                        const panelId = tab.getAttribute('aria-controls');
                        btns.forEach(t => t.setAttribute('aria-selected', String(t === tab)));
                        $a('.tab-panel', tabs).forEach(p => p.classList.toggle('active',
                            p.id === panelId));
                    }));
                });
            }

            const searchState = { active: 0, results: [] };

            function buildSearchIndex() {
                const items = [];
                NAV.forEach(g => g.items.forEach(it => {
                    items.push({ label: it.label, id: it.id, group: g.group });
                    if (it.children) it.children.forEach(c => items.push({ label: c.label, id: c.id,
                        group: g.group + ' / ' + it.label }));
                }));
                return items;
            }

            function openSearch() {
                const modal = $('#search-modal');
                if (!modal) return;
                modal.classList.add('open');
                const input = $('#search-input');
                if (input) { input.focus();
                    input.value = '';
                    renderSearchResults(''); }
            }

            function closeSearch() { const modal = $('#search-modal'); if (modal) modal.classList.remove('open'); }

            function renderSearchResults(q) {
                const box = $('#search-results');
                if (!box) return;
                q = q.toLowerCase().trim();
                const idx = buildSearchIndex();
                const matches = !q ? idx.slice(0, 6) : idx.filter(it => it.label.toLowerCase().includes(q) || it.group
                    .toLowerCase().includes(q));
                searchState.results = matches;
                searchState.active = 0;
                if (!matches.length) { box.innerHTML = '<div class="no-results">No results for "' + esc(q) +
                        '"</div>'; return; }
                let html = '';
                matches.forEach((it, i) => { html += '<a class="result-item' + (i === 0 ? ' active' : '') +
                        '" data-idx="' + i + '" href="#/' + it.id + '"><span class="result-label">' +
                        highlightMatch(it.label, q) + '</span><span class="result-path">' + esc(it.group) +
                        '</span></a>'; });
                box.innerHTML = html;
                $a('.result-item', box).forEach((a, i) => { a.addEventListener('mouseenter', () => setActiveSearch(
                        i));
                    a.addEventListener('click', () => closeSearch()); });
            }

            function setActiveSearch(i) {
                searchState.active = i;
                $a('.result-item').forEach((a, idx) => a.classList.toggle('active', idx === i));
                const cur = $('.result-item.active');
                if (cur && cur.scrollIntoView) cur.scrollIntoView({ block: 'nearest' });
            }

            function highlightMatch(text, q) {
                if (!q) return esc(text);
                const idx = text.toLowerCase().indexOf(q);
                if (idx < 0) return esc(text);
                return esc(text.slice(0, idx)) + '<mark>' + esc(text.slice(idx, idx + q.length)) + '</mark>' + esc(text
                    .slice(idx + q.length));
            }

            function initTheme() {
                let stored = null;
                try { stored = localStorage.getItem('ds-docs-theme-premium'); } catch (e) {}
                if (stored === 'dark') document.documentElement.setAttribute('data-theme', 'dark');
                const btn = $('#theme-toggle');
                if (btn) btn.addEventListener('click', () => {
                    const cur = document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' :
                        'light';
                    const next = cur === 'dark' ? 'light' : 'dark';
                    if (next === 'dark') document.documentElement.setAttribute('data-theme', 'dark');
                    else document.documentElement.removeAttribute('data-theme');
                    try { localStorage.setItem('ds-docs-theme-premium', next); } catch (e) {}
                });
            }

            function openDrawer() {
                const sb = $('#sidebar'),
                    bd = $('#drawer-backdrop');
                if (sb) sb.classList.add('open');
                if (bd) bd.classList.add('open');
                document.body.style.overflow = 'hidden';
            }

            function closeDrawer() {
                const sb = $('#sidebar'),
                    bd = $('#drawer-backdrop');
                if (sb) sb.classList.remove('open');
                if (bd) bd.classList.remove('open');
                document.body.style.overflow = '';
            }

            function currentRoute() { const h = location.hash.replace(/^#\/?/, ''); return h.split('/')[0] || 'home'; }

            function go(id) {
                if (location.hash !== '#/' + id) location.hash = '#/' + id;
                else route();
                closeDrawer();
            }

            function route() {
                const pageId = currentRoute();
                const headings = renderPageClean(META[pageId] ? pageId : 'home');
                buildTOC(headings);
                initScrollspy(headings);
                initCode($('#pages-root'));
                setActiveNav(pageId);
                const tm = $('#toc-mobile');
                if (tm) tm.classList.remove('open');
                const tt = $('.toc-mobile-toggle');
                if (tt) tt.setAttribute('aria-expanded', 'false');
                window.scrollTo(0, 0);
            }

            function init() {
                document.documentElement.classList.remove('no-js');
                buildSidebar();
                initNavFilter();
                initTheme();
                route();
                window.addEventListener('hashchange', route);
                const headerSearch = $('#header-search-trigger');
                if (headerSearch) headerSearch.addEventListener('click', openSearch);
                const modal = $('#search-modal');
                if (modal) modal.addEventListener('click', e => { if (e.target === modal) closeSearch(); });
                const input = $('#search-input');
                if (input) input.addEventListener('input', () => renderSearchResults(input.value));
                const mt = $('#menu-toggle');
                if (mt) mt.addEventListener('click', openDrawer);
                const bd = $('#drawer-backdrop');
                if (bd) bd.addEventListener('click', closeDrawer);
                const dc = $('#drawer-close');
                if (dc) dc.addEventListener('click', closeDrawer);
                window.addEventListener('resize', () => { if (window.innerWidth > 1024) closeDrawer(); });
                document.addEventListener('keydown', e => {
                    const searchOpen = $('#search-modal') && $('#search-modal').classList.contains('open');
                    if (e.key === 'Escape') { if (searchOpen) closeSearch();
                        else closeDrawer(); }
                    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') { e.preventDefault();
                        openSearch(); } else if (e.key === '/' && !searchOpen && !/^(INPUT|TEXTAREA)$/.test(
                            document.activeElement.tagName)) { e.preventDefault();
                        openSearch(); }
                    if (searchOpen && searchState.results.length) {
                        if (e.key === 'ArrowDown') { e.preventDefault();
                            setActiveSearch(Math.min(searchState.active + 1, searchState.results
                                .length - 1)); }
                        if (e.key === 'ArrowUp') { e.preventDefault();
                            setActiveSearch(Math.max(searchState.active - 1, 0)); }
                        if (e.key === 'Enter') { e.preventDefault(); const r = searchState.results[
                                searchState.active]; if (r) { closeSearch();
                                go(r.id); } }
                    }
                });
            }
            if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
            else init();
        })();
