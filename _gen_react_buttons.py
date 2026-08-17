#!/usr/bin/env python3
"""DevSnips React Buttons migration generator.

Regenerates code.tsx, code.jsx, preview.html, metadata.json, and README.md
for every button in React/Components/Buttons/ from one declarative source
of truth (the COMPONENTS table below), keeping all 30 buttons in sync with
React/DESIGN_TOKENS.md and guaranteeing TSX/JSX parity, consistent APIs,
and consistent metadata.

    python3 _gen_react_buttons.py            # write everything
    python3 _gen_react_buttons.py --check   # report drift, no writes

Previews load React 18 UMD + Babel standalone and a Tailwind CDN script +
a shared --ds-* token :root block. The component classes are identical to
code.tsx (Tailwind utilities consuming the semantic tokens).
"""
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BUTTONS = ROOT / "React/Components/Buttons"
ESBUILD = "/tmp/dsbuild/node_modules/.bin/esbuild"

# ---------------------------------------------------------------------------
# Tailwind config injected into every preview. Maps semantic tokens to the
# ds-* CSS variables so utility classes can stay readable where useful, but
# buttons primarily consume tokens via arbitrary values (var(--ds-...)).
# ---------------------------------------------------------------------------
TAILWIND_CONFIG = """  tailwind.config = {
    theme: {
      extend: {
        colors: {
          "ds-bg": "var(--ds-color-background)",
          "ds-fg": "var(--ds-color-foreground)",
          "ds-surface": "var(--ds-color-surface)",
          "ds-subtle": "var(--ds-color-surface-subtle)",
          "ds-hover": "var(--ds-color-surface-hover)",
          "ds-active": "var(--ds-color-surface-active)",
          "ds-muted": "var(--ds-color-muted-foreground)",
          "ds-border": "var(--ds-color-border)",
          "ds-border-strong": "var(--ds-color-border-strong)",
          "ds-primary": "var(--ds-color-primary)",
          "ds-primary-fg": "var(--ds-color-primary-foreground)",
          "ds-accent": "var(--ds-color-accent)",
          "ds-destructive": "var(--ds-color-destructive)",
          "ds-success": "var(--ds-color-success)",
          "ds-link": "var(--ds-color-link)",
          "ds-focus": "var(--ds-color-focus-ring)",
        },
        fontFamily: {
          sans: ['Inter', 'system-ui', 'sans-serif'],
          mono: ['ui-monospace', 'SF Mono', 'Menlo', 'Consolas', 'monospace'],
        },
      },
    },
  };"""

# Shared --ds-* token block (light + dark). Demo theme for previews only.
TOKEN_BLOCK = r"""  :root {
    color-scheme: light;
    --ds-color-background: #FAFAFA;
    --ds-color-foreground: #171717;
    --ds-color-surface: #FFFFFF;
    --ds-color-surface-subtle: #F5F5F5;
    --ds-color-surface-elevated: #FFFFFF;
    --ds-color-surface-hover: #F5F5F5;
    --ds-color-surface-active: #E5E5E5;
    --ds-color-surface-selected: #F5F5F5;
    --ds-color-muted: #F5F5F5;
    --ds-color-muted-foreground: #737373;
    --ds-color-border: #E5E5E5;
    --ds-color-border-subtle: #EFEFEF;
    --ds-color-border-strong: #D4D4D4;
    --ds-color-input: #FFFFFF;
    --ds-color-primary: #171717;
    --ds-color-primary-foreground: #FFFFFF;
    --ds-color-secondary: #F5F5F5;
    --ds-color-secondary-foreground: #171717;
    --ds-color-accent: #2563EB;
    --ds-color-accent-foreground: #FFFFFF;
    --ds-color-accent-soft: rgba(37, 99, 235, 0.10);
    --ds-color-destructive: #C2261B;
    --ds-color-destructive-foreground: #FFFFFF;
    --ds-color-destructive-soft: rgba(194, 38, 27, 0.10);
    --ds-color-success: #15803D;
    --ds-color-success-foreground: #FFFFFF;
    --ds-color-success-soft: rgba(21, 128, 61, 0.12);
    --ds-color-warning: #B45309;
    --ds-color-warning-foreground: #FFFFFF;
    --ds-color-info: #2563EB;
    --ds-color-info-foreground: #FFFFFF;
    --ds-color-link: #2563EB;
    --ds-color-link-hover: #1D4ED8;
    --ds-color-focus-ring: #2563EB;
    --ds-color-overlay: rgba(10, 10, 10, 0.50);
    --ds-radius-none: 0;
    --ds-radius-xs: 3px;
    --ds-radius-sm: 5px;
    --ds-radius-md: 8px;
    --ds-radius-lg: 12px;
    --ds-radius-xl: 16px;
    --ds-radius-full: 9999px;
    --ds-shadow-xs: 0 1px 2px rgba(10, 10, 10, 0.04);
    --ds-shadow-sm: 0 1px 3px rgba(10, 10, 10, 0.08), 0 1px 2px rgba(10, 10, 10, 0.04);
    --ds-shadow-md: 0 4px 12px rgba(10, 10, 10, 0.10), 0 2px 4px rgba(10, 10, 10, 0.06);
    --ds-shadow-lg: 0 12px 32px rgba(10, 10, 10, 0.14), 0 4px 8px rgba(10, 10, 10, 0.08);
    --ds-font-sans: "Inter", system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    --ds-font-mono: ui-monospace, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;
  }
  [data-theme="dark"] {
    color-scheme: dark;
    --ds-color-background: #0A0A0A;
    --ds-color-foreground: #FAFAFA;
    --ds-color-surface: #171717;
    --ds-color-surface-subtle: #1F1F1F;
    --ds-color-surface-elevated: #1F1F1F;
    --ds-color-surface-hover: #1F1F1F;
    --ds-color-surface-active: #2A2A2A;
    --ds-color-surface-selected: #1F1F1F;
    --ds-color-muted: #1F1F1F;
    --ds-color-muted-foreground: #A3A3A3;
    --ds-color-border: #2A2A2A;
    --ds-color-border-subtle: #1F1F1F;
    --ds-color-border-strong: #404040;
    --ds-color-input: #171717;
    --ds-color-primary: #FAFAFA;
    --ds-color-primary-foreground: #0A0A0A;
    --ds-color-secondary: #1F1F1F;
    --ds-color-secondary-foreground: #FAFAFA;
    --ds-color-accent: #3B82F6;
    --ds-color-accent-foreground: #FFFFFF;
    --ds-color-accent-soft: rgba(59, 130, 246, 0.16);
    --ds-color-destructive: #F1635A;
    --ds-color-destructive-foreground: #0A0A0A;
    --ds-color-destructive-soft: rgba(241, 99, 90, 0.16);
    --ds-color-success: #4ADE80;
    --ds-color-success-foreground: #052E16;
    --ds-color-success-soft: rgba(74, 222, 128, 0.18);
    --ds-color-warning: #FBBF24;
    --ds-color-warning-foreground: #1A1206;
    --ds-color-info: #3B82F6;
    --ds-color-info-foreground: #FFFFFF;
    --ds-color-link: #60A5FA;
    --ds-color-link-hover: #93C5FD;
    --ds-color-focus-ring: #3B82F6;
    --ds-color-overlay: rgba(0, 0, 0, 0.65);
    --ds-shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.40);
    --ds-shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.50), 0 1px 2px rgba(0, 0, 0, 0.40);
    --ds-shadow-md: 0 4px 12px rgba(0, 0, 0, 0.55), 0 2px 4px rgba(0, 0, 0, 0.45);
    --ds-shadow-lg: 0 12px 32px rgba(0, 0, 0, 0.65), 0 4px 8px rgba(0, 0, 0, 0.50);
  }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) {
      color-scheme: dark;
      --ds-color-background: #0A0A0A;
      --ds-color-foreground: #FAFAFA;
      --ds-color-surface: #171717;
      --ds-color-surface-subtle: #1F1F1F;
      --ds-color-surface-elevated: #1F1F1F;
      --ds-color-surface-hover: #1F1F1F;
      --ds-color-surface-active: #2A2A2A;
      --ds-color-surface-selected: #1F1F1F;
      --ds-color-muted: #1F1F1F;
      --ds-color-muted-foreground: #A3A3A3;
      --ds-color-border: #2A2A2A;
      --ds-color-border-subtle: #1F1F1F;
      --ds-color-border-strong: #404040;
      --ds-color-input: #171717;
      --ds-color-primary: #FAFAFA;
      --ds-color-primary-foreground: #0A0A0A;
      --ds-color-secondary: #1F1F1F;
      --ds-color-secondary-foreground: #FAFAFA;
      --ds-color-accent: #3B82F6;
      --ds-color-accent-foreground: #FFFFFF;
      --ds-color-accent-soft: rgba(59, 130, 246, 0.16);
      --ds-color-destructive: #F1635A;
      --ds-color-destructive-foreground: #0A0A0A;
      --ds-color-destructive-soft: rgba(241, 99, 90, 0.16);
      --ds-color-success: #4ADE80;
      --ds-color-success-foreground: #052E16;
      --ds-color-success-soft: rgba(74, 222, 128, 0.18);
      --ds-color-warning: #FBBF24;
      --ds-color-warning-foreground: #1A1206;
      --ds-color-info: #3B82F6;
      --ds-color-info-foreground: #FFFFFF;
      --ds-color-link: #60A5FA;
      --ds-color-link-hover: #93C5FD;
      --ds-color-focus-ring: #3B82F6;
      --ds-color-overlay: rgba(0, 0, 0, 0.65);
      --ds-shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.40);
      --ds-shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.50), 0 1px 2px rgba(0, 0, 0, 0.40);
      --ds-shadow-md: 0 4px 12px rgba(0, 0, 0, 0.55), 0 2px 4px rgba(0, 0, 0, 0.45);
      --ds-shadow-lg: 0 12px 32px rgba(0, 0, 0, 0.65), 0 4px 8px rgba(0, 0, 0, 0.50);
    }
  }"""

# Preview-page CSS (showcase shell). Token-based, shared across previews.
PREVIEW_CSS = r"""  *{box-sizing:border-box;}
  html,body{margin:0;}
  body{font-family:var(--ds-font-sans);background:var(--ds-color-background);color:var(--ds-color-foreground);}
  .ds-page{min-height:100vh;}
  .ds-topbar{position:sticky;top:0;z-index:30;display:flex;align-items:center;justify-content:space-between;height:52px;padding:0 24px;background:color-mix(in srgb,var(--ds-color-surface) 85%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--ds-color-border);}
  .ds-brand{display:flex;align-items:center;gap:8px;font:500 13px/1.4 var(--ds-font-sans);}
  .ds-mark{width:18px;height:18px;border:1.5px solid var(--ds-color-foreground);border-radius:4px;display:inline-flex;align-items:center;justify-content:center;font:700 11px/1 var(--ds-font-sans);}
  .ds-crumb{color:var(--ds-color-muted-foreground);font:400 13px/1.45 var(--ds-font-sans);}
  .ds-crumb b{color:var(--ds-color-foreground);font-weight:500;}
  .ds-theme-toggle{display:inline-flex;align-items:center;gap:8px;height:32px;padding:0 12px;font:500 12px/1.35 var(--ds-font-sans);color:var(--ds-color-foreground);background:var(--ds-color-surface);border:1px solid var(--ds-color-border);border-radius:var(--ds-radius-sm);cursor:pointer;}
  .ds-theme-toggle:hover{background:var(--ds-color-surface-hover);}
  .ds-theme-toggle:focus-visible{outline:2px solid var(--ds-color-focus-ring);outline-offset:2px;}
  .ds-main{max-width:980px;margin:0 auto;padding:32px 24px 64px;}
  .ds-eyebrow{font:600 11px/1.3 var(--ds-font-sans);letter-spacing:0.06em;text-transform:uppercase;color:var(--ds-color-muted-foreground);margin:0 0 8px;}
  .ds-title{font:600 18px/1.35 var(--ds-font-sans);letter-spacing:-0.01em;margin:0 0 8px;}
  .ds-lede{color:var(--ds-color-muted-foreground);font:400 14px/1.5 var(--ds-font-sans);margin:0 0 32px;max-width:60ch;}
  .ds-section{margin-top:32px;}
  .ds-section-h{display:flex;align-items:baseline;justify-content:space-between;margin:0 0 16px;padding-bottom:8px;border-bottom:1px solid var(--ds-color-border-subtle);}
  .ds-section-h h2{font:600 16px/1.4 var(--ds-font-sans);margin:0;letter-spacing:-0.01em;}
  .ds-section-h .ds-note{font:400 12px/1.4 var(--ds-font-sans);color:var(--ds-color-muted-foreground);}
  .ds-row{display:flex;flex-wrap:wrap;align-items:center;gap:12px;}
  .ds-stack{display:flex;flex-direction:column;gap:12px;align-items:flex-start;}
  .ds-label{font:500 12px/1.35 var(--ds-font-sans);color:var(--ds-color-muted-foreground);margin:0 0 8px;text-transform:uppercase;letter-spacing:0.04em;}
  .ds-card{background:var(--ds-color-surface);border:1px solid var(--ds-color-border);border-radius:var(--ds-radius-md);padding:20px;}
  .ds-canvas{background:var(--ds-color-surface);border:1px solid var(--ds-color-border);border-radius:var(--ds-radius-md);padding:20px;}
  .ds-pos-wrap{position:relative;}
  .ds-footer{border-top:1px solid var(--ds-color-border);padding:24px;text-align:center;font:400 12px/1.4 var(--ds-font-sans);color:var(--ds-color-muted-foreground);}
  .ds-footer code{font-family:var(--ds-font-mono);}
  .sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;}
"""

# Shared React icon set + hooks, embedded into previews that need them.
ICON_JS = r"""function Icon({ name, className }) {
  const common = { width:"1em", height:"1em", viewBox:"0 0 24 24", fill:"none", stroke:"currentColor", strokeWidth:1.75, strokeLinecap:"round", strokeLinejoin:"round", className, "aria-hidden":"true", focusable:"false" };
  switch (name) {
    case "chevron-down": return (<svg {...common}><path d="m6 9 6 6 6-6"/></svg>);
    case "chevron-right": return (<svg {...common}><path d="m9 6 6 6-6 6"/></svg>);
    case "chevron-left": return (<svg {...common}><path d="m15 6-6 6 6 6"/></svg>);
    case "arrow-right": return (<svg {...common}><path d="M5 12h14"/><path d="m13 5 7 7-7 7"/></svg>);
    case "arrow-left": return (<svg {...common}><path d="M19 12H5"/><path d="m11 19-7-7 7-7"/></svg>);
    case "download": return (<svg {...common}><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5"/><path d="M12 15V3"/></svg>);
    case "upload": return (<svg {...common}><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m17 8-5-5-5 5"/><path d="M12 3v12"/></svg>);
    case "copy": return (<svg {...common}><rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>);
    case "check": return (<svg {...common}><path d="M20 6 9 17l-5-5"/></svg>);
    case "x": return (<svg {...common}><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>);
    case "plus": return (<svg {...common}><path d="M12 5v14"/><path d="M5 12h14"/></svg>);
    case "refresh": return (<svg {...common}><path d="M3 12a9 9 0 0 1 15-6.7L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-15 6.7L3 16"/><path d="M3 21v-5h5"/></svg>);
    case "filter": return (<svg {...common}><path d="M22 3H2l8 9.46V19l4 2v-8.54L22 3z"/></svg>);
    case "sort": return (<svg {...common}><path d="M11 5h10"/><path d="M11 9h7"/><path d="M11 13h4"/><path d="m3 17 3 3 3-3"/><path d="M6 18V4"/></svg>);
    case "more": return (<svg {...common}><circle cx="12" cy="5" r="1"/><circle cx="12" cy="12" r="1"/><circle cx="12" cy="19" r="1"/></svg>);
    case "search": return (<svg {...common}><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>);
    case "command": return (<svg {...common}><path d="M18 3a3 3 0 0 0-3 3v12a3 3 0 0 0 3 3 3 3 0 0 0 3-3 3 3 0 0 0-3-3H6a3 3 0 0 0-3 3 3 3 0 0 0 3 3 3 3 0 0 0 3-3V6a3 3 0 0 0-3-3 3 3 0 0 0-3 3 3 3 0 0 0 3 3h12a3 3 0 0 0 3-3 3 3 0 0 0-3-3z"/></svg>);
    case "trash": return (<svg {...common}><path d="M3 6h18"/><path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/></svg>);
    case "edit": return (<svg {...common}><path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg>);
    case "external": return (<svg {...common}><path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/></svg>);
    case "settings": return (<svg {...common}><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>);
    case "archive": return (<svg {...common}><rect x="3" y="4" width="18" height="4" rx="1"/><path d="M5 8v11a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V8"/><path d="M10 12h4"/></svg>);
    case "share": return (<svg {...common}><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="m8.6 13.5 6.8 4"/><path d="m15.4 6.5-6.8 4"/></svg>);
    case "duplicate": return (<svg {...common}><rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>);
    case "pin": return (<svg {...common}><path d="M12 17v5"/><path d="M9 10.76V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v5.76a2 2 0 0 0 .6 1.42l2.4 2.36a1 1 0 0 1-.7 1.7H6.7a1 1 0 0 1-.7-1.7l2.4-2.36a2 2 0 0 0 .6-1.42Z"/></svg>);
    case "bell": return (<svg {...common}><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/></svg>);
    case "save": return (<svg {...common}><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><path d="M17 21v-8H7v8"/><path d="M7 3v5h8"/></svg>);
    case "user": return (<svg {...common}><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/></svg>);
    case "sparkles": return (<svg {...common}><path d="M12 3v4"/><path d="M12 17v4"/><path d="M3 12h4"/><path d="M17 12h4"/><path d="m6.3 6.3 2.8 2.8"/><path d="m14.9 14.9 2.8 2.8"/><path d="m17.7 6.3-2.8 2.8"/><path d="m9.1 14.9-2.8 2.8"/></svg>);
    default: return null;
  }
}

function useClickOutside(onClose, active) {
  const ref = React.useRef(null);
  React.useEffect(() => {
    if (!active) return;
    function onDown(e) { if (ref.current && !ref.current.contains(e.target)) onClose(); }
    function onKey(e) { if (e.key === "Escape") onClose(); }
    document.addEventListener("mousedown", onDown);
    document.addEventListener("keydown", onKey);
    return () => { document.removeEventListener("mousedown", onDown); document.removeEventListener("keydown", onKey); };
  }, [active, onClose]);
  return ref;
}

function useCopy(resetMs) {
  const [copied, setCopied] = React.useState(false);
  const t = React.useRef(null);
  const copy = React.useCallback(async (text) => {
    try {
      if (navigator.clipboard && window.isSecureContext) { await navigator.clipboard.writeText(text); }
      else { const ta = document.createElement("textarea"); ta.value = text; ta.style.position = "fixed"; ta.style.opacity = "0"; document.body.appendChild(ta); ta.select(); document.execCommand("copy"); document.body.removeChild(ta); }
      setCopied(true); clearTimeout(t.current); t.current = setTimeout(() => setCopied(false), resetMs || 2000);
    } catch (e) { /* clipboard unavailable */ }
  }, [resetMs]);
  React.useEffect(() => () => clearTimeout(t.current), []);
  return [copied, copy];
}
"""

# ---------------------------------------------------------------------------
# Component source registry. Each entry is the literal code.tsx body for one
# button. The generator writes code.tsx, derives code.jsx via esbuild, and
# builds the preview/metadata/README from shared templates + the showcase JS
# registered separately.
# ---------------------------------------------------------------------------
COMPONENTS: dict[str, dict] = {}  # populated by register() below

def register(slug, *, title, eyebrow, lede, subcategory, tags, features,
             accessibility, interactive, related, tsx, showcase,
             props_doc, variants_doc, sizes_doc, states_doc, a11y_doc, notes_doc,
             extra=None):
    COMPONENTS[slug] = dict(
        title=title, eyebrow=eyebrow, lede=lede, subcategory=subcategory,
        tags=tags, features=features, accessibility=accessibility,
        interactive=interactive, related=related, tsx=tsx, showcase=showcase,
        props_doc=props_doc, variants_doc=variants_doc, sizes_doc=sizes_doc,
        states_doc=states_doc, a11y_doc=a11y_doc, notes_doc=notes_doc,
        extra=extra or [],
    )


# ---------------------------------------------------------------------------
# Renderers
# ---------------------------------------------------------------------------
def _ts_to_jsx(tsx_text: str, export_name: str | None = None) -> str:
    """Strip TS types from a .tsx body to a Babel-compatible .jsx body.

    esbuild (--format=esm --jsx=preserve) removes TypeScript types and keeps
    JSX, but rewrites `export function X` into `function X` + a trailing
    `export { X }` block. We post-process: drop the synthetic default-export
    var + trailing export block, then (when export_name is given) restore
    `export ` on the main declaration and append `export default <name>`,
    so code.jsx is a valid JS module that mirrors code.tsx's exports.
    """
    import re
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".tsx", delete=False) as f:
        f.write(tsx_text)
        path = f.name
    try:
        out = subprocess.run(
            [ESBUILD, path, "--jsx=preserve", "--format=esm"],
            capture_output=True, text=True, check=True,
        ).stdout
    finally:
        Path(path).unlink(missing_ok=True)
    out = out.replace("void 0", "undefined")
    out = re.sub(r"\nvar [a-z0-9_]+_default = [A-Za-z_$][\w$]*;\n", "\n", out)
    out = re.sub(r"\nexport \{[^}]*\};?\s*$", "\n", out, flags=re.S)
    if export_name:
        # Restore `export` on the main function declaration.
        out = re.sub(
            rf"(^|\n)(function {export_name}\()",
            rf"\1export \2",
            out,
            count=1,
        )
        out = out.rstrip() + f"\n\nexport default {export_name};\n"
    return out.rstrip() + "\n"


def render_code_tsx(spec):
    body = spec["tsx"].strip("\n")
    return body + "\n"


def _export_name(spec) -> str | None:
    """Pull the primary `export function <Name>` from the tsx body."""
    import re
    m = re.search(r"export function ([A-Za-z_$][\w$]*)", spec["tsx"])
    return m.group(1) if m else None


def render_code_jsx(spec):
    name = _export_name(spec)
    body = _ts_to_jsx(render_code_tsx(spec), export_name=name)
    header = (
        "/* DevSnips React — JavaScript parity build.\n"
        " * Same API, behavior, and classes as code.tsx; TypeScript types removed.\n"
        " * Regenerated from code.tsx — edit code.tsx and re-run the generator.\n"
        " */\n\n"
    )
    return header + body


def _tsx_to_babel_component(tsx_text: str, expose_name: str | None = None) -> str:
    """Transform a code.tsx body to Babel-compatible JSX (no types, no
    `export` keywords, no `import` statements) for inlining into a preview
    <script>. React/ReactDOM are UMD globals in the preview, so value imports
    from "react" become a destructure from `React`. When `expose_name` is
    given, the body is wrapped in an IIFE that assigns the component to
    `window.<expose_name>` so sibling helpers (cx, Spinner, SIZES, local
    Icon) stay scoped and don't collide across injected components.
    """
    import re
    body = _ts_to_jsx(tsx_text)
    body = re.sub(r"\bexport (function|const|class|let|var)\b", r"\1", body)
    body = re.sub(r"\nexport default [A-Za-z_$][\w$]*;\s*$", "\n", body)
    def _conv(m):
        return f"const {{ {m.group(1)} }} = React;\n"
    body = re.sub(r'(?m)^import \{([^}]+)\} from "react";\n', _conv, body)
    body = re.sub(r"(?m)^import .*?;\n", "", body)
    if expose_name:
        indented = "\n".join("  " + ln if ln else ln for ln in body.splitlines())
        return f"(function() {{\n{indented}\n  window.{expose_name} = {expose_name};\n}})();\n"
    return body


def render_preview(spec, slug):
    title = spec["title"]
    main_name = _export_name(spec) or ""
    # The preview renders the actual component (transformed from code.tsx)
    # plus a standalone Showcase. Keeps the preview faithful to code.tsx.
    component_js = _tsx_to_babel_component(spec["tsx"], expose_name=main_name)
    # Sibling components the showcase references (e.g. a SolidButton shown
    # beside an OutlineButton). Each is wrapped in an IIFE that exposes it
    # on window so helper names don't collide across components.
    extra_js = ""
    for dep_slug in spec.get("extra", []):
        if dep_slug in COMPONENTS and dep_slug != slug:
            dep_name = _export_name(COMPONENTS[dep_slug]) or ""
            extra_js += "\n// sibling component: " + dep_slug + "\n"
            extra_js += _tsx_to_babel_component(COMPONENTS[dep_slug]["tsx"], expose_name=dep_name)
    showcase = spec["showcase"].strip("\n")
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title} — DevSnips React</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
<script src="https://cdn.tailwindcss.com"></script>
<script>
{TAILWIND_CONFIG}
  // Apply token CSS variables before paint to avoid a flash in dark mode.
</script>
<style>
{TOKEN_BLOCK}
{PREVIEW_CSS}
</style>
</head>
<body>
<div class="ds-page">
  <header class="ds-topbar">
    <div class="ds-brand"><span class="ds-mark" aria-hidden="true">D</span><span>DevSnips</span><span class="ds-crumb" aria-hidden="true">/ <b>React</b> / Buttons / {slug}</span></div>
    <button class="ds-theme-toggle" id="ds-theme-toggle" type="button" aria-pressed="false">
      <span id="ds-theme-label">Dark</span>
    </button>
  </header>
  <main class="ds-main">
    <p class="ds-eyebrow">{spec["eyebrow"]}</p>
    <h1 class="ds-title">{title}</h1>
    <p class="ds-lede">{spec["lede"]}</p>
    <div id="ds-root" class="ds-pos-wrap"></div>
  </main>
  <footer class="ds-footer">DevSnips React · Buttons · <code>{slug}</code> · preview demonstration of code.tsx</footer>
</div>
<script>
(function(){{
  var root = document.documentElement;
  function apply(t){{ root.setAttribute("data-theme", t); try{{ localStorage.setItem("ds-react-theme", t); }}catch(e){{}} var b=document.getElementById("ds-theme-toggle"); var l=document.getElementById("ds-theme-label"); if(b){{b.setAttribute("aria-pressed", t==="dark"?"true":"false");}} if(l){{l.textContent = t==="dark"?"Light":"Dark";}} }}
  var saved = null; try{{ saved = localStorage.getItem("ds-react-theme"); }}catch(e){{}}
  if(!saved){{ saved = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark":"light"; }}
  apply(saved);
  document.getElementById("ds-theme-toggle").addEventListener("click", function(){{ var cur = root.getAttribute("data-theme") === "dark" ? "light":"dark"; apply(cur); }});
}})();
</script>
<script src="https://unpkg.com/react@18/umd/react.development.js" crossorigin></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js" crossorigin></script>
<script src="https://unpkg.com/@babel/standalone@7/babel.min.js"></script>
<script type="text/babel" data-presets="react">
// Preview demonstration environment. The component below is the actual
// code.tsx implementation (JSX inlined for Babel). The shared Icon set +
// hooks are inlined so the preview is fully standalone.
{ICON_JS}
</script>
<script type="text/babel" data-presets="react">
// The component below is the actual code.tsx implementation, transformed to
// JSX (types removed) so Babel standalone can run it. It is identical in
// behavior to code.tsx/code.jsx.
{component_js}
{extra_js}
</script>
<script type="text/babel" data-presets="react">
{showcase}
</script>
</body>
</html>
"""


def render_metadata(spec, slug):
    return json.dumps({
        "id": f"{slug}-react-001",
        "name": spec["title"],
        "slug": slug,
        "component": "button",
        "family": "buttons",
        "variant": slug,
        "description": spec["lede"],
        "framework": "React",
        "language": "TSX",
        "languages": ["JSX", "TSX"],
        "technology": "react",
        "type": "component",
        "category": "Buttons",
        "subcategory": spec["subcategory"],
        "styling": "Tailwind CSS",
        "tags": spec["tags"],
        "features": spec["features"],
        "responsive": True,
        "darkMode": True,
        "accessibility": spec["accessibility"],
        "interactive": spec["interactive"],
        "dependencies": [],
        "source": "DevSnips",
        "related": spec["related"],
    }, indent=2) + "\n"


def render_readme(spec, slug):
    return f"""# {spec["title"]}

{spec["lede"]}

## Installation

This component requires **React** and **Tailwind CSS**. Drop `code.tsx` (or `code.jsx` for JavaScript projects) into your project. Tailwind utility classes are included directly in the component, so no separate CSS file is required.

The component consumes the DevSnips semantic design tokens through Tailwind arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the `--ds-*` tokens once in your theme — see [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the full token spec.

## Usage

```tsx
{spec["props_doc"]["usage"]}
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

## Props

{spec["props_doc"]["table"]}

## Variants

{spec["variants_doc"]}

## Sizes

{spec["sizes_doc"]}

## States

{spec["states_doc"]}

## Accessibility

{spec["a11y_doc"]}

## Styling

Tailwind classes are included directly in the component and consume the DevSnips semantic design tokens (`--ds-*`) via arbitrary values. The button themes with the surface automatically in light and dark mode. No component-specific CSS file is needed.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This button uses the semantic color, radius, and motion tokens; define them once in your project theme and every button in the family stays in sync.

## Notes

{spec["notes_doc"]}
"""


def main(check=False):
    if not COMPONENTS:
        import importlib.util
        # import the registry module (same dir) so register() calls run
        reg = ROOT / "_gen_react_buttons_registry.py"
        spec = importlib.util.spec_from_file_location("_gen_react_buttons_registry", reg)
        mod = importlib.util.module_from_spec(spec)
        # this module is already imported; re-inject COMPONENTS
        import sys as _s
        _s.modules["_gen_react_buttons"] = _s.modules[__name__]
        spec.loader.exec_module(mod)
    drift = []
    for slug, spec in COMPONENTS.items():
        folder = BUTTONS / slug
        folder.mkdir(parents=True, exist_ok=True)
        files = {
            "code.tsx": render_code_tsx(spec),
            "code.jsx": render_code_jsx(spec),
            "preview.html": render_preview(spec, slug),
            "metadata.json": render_metadata(spec, slug),
            "README.md": render_readme(spec, slug),
        }
        for name, content in files.items():
            p = folder / name
            if check:
                if not p.exists() or p.read_text(encoding="utf-8") != content:
                    drift.append(str(p))
            else:
                p.write_text(content, encoding="utf-8")
    if check:
        if drift:
            print("DRIFT detected in:")
            for d in drift:
                print("  " + d)
            sys.exit(1)
        print(f"OK: {len(COMPONENTS)} buttons up to date.")
    else:
        print(f"Wrote {len(COMPONENTS)} buttons.")

if __name__ == "__main__":
    import sys as _sys
    if len(_sys.argv) > 1 and _sys.argv[1] == "--check":
        main(check=True)
    else:
        main()
