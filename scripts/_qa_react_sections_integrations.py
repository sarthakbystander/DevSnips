#!/usr/bin/env python3
"""Playwright QA for the React Sections Integrations previews.

Verifies behavior-critical guarantees (not cosmetics):
  - every variant: renders the actual section, zero console errors, zero
    horizontal overflow at 320/375/768/1024/1280/1440 (light AND dark)
  - static: exactly the 3 required files per variant, metadata schema
    (family/direction/type), no `any` in code.tsx, no hardcoded hex outside
    color-mix(..., #000), no raw Tailwind palette utilities, no `!important`,
    no `transition-all`, no inline `style=`, no emoji, no <img>/external URLs,
    no <style>/<script> embeds, no lorem ipsum
  - structure: exactly one h2 per section, section aria-labelledby points at
    it,,and the authored integration data renders as readable text (name,
    category/description where provided; product node for dark-premium; the
    central system block for neo-brutalist)
  - themes: light/dark page toggle flips computed section surface + text
    colors;the `dark-premium` variant keeps its pinned dark mapping
    in both page themes
  - focus: keyboard focus shows a 2px focus-visible outline on every
    interactive link( all four variants ship exactly one semantic anchor	
  - motion: prefers-reduced-motion kills transitions
  - connection visuals:the dark-premium decorative SVG connection layer
    stays inside its panel at every QA width in both themes;the neo-brutalist
    hard offset shadows stay inside the viewport at every QA width/theme.
  - network: after the preview shell finishes loading, toggling themes,
    resizing, and focusing elements makes zero additional network requests
    (the section itself never fetches anything).
  - types: every code.tsx strict-passes tsc with --noUncheckedIndexedAccess
  - generator: `_gen_react_sections_integrations.py --check` reports no
    drift; `scripts/validate.py` passes

The family ships exactly the four DevSnips visual directions;this script
also asserts no other variant directories exist.

Run from the repo root with a static server on :8765:

    python3 -m http.server 8765 &
    python3 scripts/_qa_react_sections_integrations.py
"""
import json
import re
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
BASE = "http://localhost:8765/React/Sections/Integrations/"
SLUGS = [
    "minimal",
    "dark-premium",
    "bento",
    "neo-brutalist",
]
WIDTHS = [320, 375, 768, 1024, 1280, 1440]

# Expected rendered readable content per variant (authored defaults).
EXPECTED_NAMES = {
    "minimal": ["GitHub", "Slack", "Linear", "Notion", "Figma", "Vercel", "Sentry", "Stripe"],
    "dark-premium": ["DevSnips", "GitHub", "Slack", "Linear", "Notion", "Figma", "Vercel"],
    "bento": ["GitHub", "Slack", "Linear", "Vercel", "Sentry", "Figma", "Notion", "Stripe"],
    "neo-brutalist": ["INTEGRATIONS", "DevSnips", "GitHub", "Slack", "Linear", "Notion", "Figma"],
}

EXPECTED_TEXTS = {
    "minimal": [
        "Connect the tools you already use.",
        "Two-way sync for issues, pull requests,and deploy hooks",
        "Route alerts, approvals,and digests into the channels",
        "View all integrations",
    ],
    "dark-premium": [
        "DevSnips plugs into the tools your team already runs.",
        "Core system",
        "Development",
        "Browse 38 integrations",
    ],
    "bento": [
        "One workspace, every tool your team ships through.",
        "The anchor of your repo workflow",
        "38",
        "maintained integrations",
        "Development",
        "Design",
        "Communication",
        "Browse the connection directory",
    ],
    "neo-brutalist": [
        "INTEGRATIONS",
        "Core system",
        "Module",
        "Channels",
        "Status",
        "Linked",
        "Connect your stack",
    ],
}

# Expected count of interactive labels / structural markers per variant.
LINK_COUNTS = {
    "minimal": 1,
    "dark-premium": 1,
    "bento": 1,
    "neo-brutalist": 1,
}

# Allowed CDN origins: the preview shell fro example loads Tailwind,
# React UMD, Babel, Inter, and JetBrains Mono from these hosts. Any
# request outside them after load is a section-driven network call (fail..
ALLOWED_NETWORK_HOSTS = {
    "cdn.tailwindcss.com",
    "unpkg.com",
    "fonts.googleapis.com",
    "fonts.gstatic.com",
}

checks = 0
failures: list[str] = []


def check(cond: bool, label: str) -> None:
    global checks
    checks += 1
    if not cond:
        failures.append(label)
        print("FAIL:", label)


def static_checks() -> None:
    palette = re.compile(
        r"\b(?:bg|text|border|fill|stroke|from|to|via)-(?:slate|gray|zinc|"
        r"neutral|stone|red|orange|amber|yellow|lime|green|emerald|teal|"
        r"cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose)-\d"
    )
    hex_lit = re.compile(r"#[0-9a-fA-F]{3,8}\b")
    emoji = re.compile(
        "[\U0001F000-\U0001FAFF\u2600-\u27FF]", re.UNICODE
    )
    family_dir = ROOT / "React" / "Sections" / "Integrations"
    dirs = sorted(p.name for p in family_dir.iterdir() if p.is_dir())
    check(
        dirs == sorted(SLUGS),
        f"family contains exactly the four direction variants, got {dirs}",
    )
    for slug in SLUGS:

        folder = ROOT / "React" / "Sections" / "Integrations" / slug
        files = sorted(p.name for p in folder.iterdir() if p.is_file())
        check(
            files == ["code.tsx", "metadata.json", "preview.html"],
            f"{slug}: exact 3-file shape, got {files}",
        )
        tsx = (folder / "code.tsx").read_text()
        check(
            not re.search(r":\s*any\b|<any>|\bas\s+any\b", tsx),
            f"{slug}: no `any`",
        )
        # `#000` inside color-mix hover darkening is the one sanctioned
        # literal (React/Sections/DESIGN_TOKENS.md A2) - remove it, then
        # scan for everything else.

        stripped = tsx.replace("#000", "")
        check(
            not hex_lit.search(stripped),
            f"{slug}: no hex literals outside color-mix",
        )
        check(not palette.search(tsx), f"{slug}: no raw palette utilities")
        check("!important" not in tsx, f"{slug}: no !important")
        check("transition-all" not in tsx, f"{slug}: no transition-all")
        check(not emoji.search(tsx), f"{slug}: no emoji")
        check('style={' not in tsx, f"{slug}: no inline style props")
        check("<img" not in tsx, f"{slug}: no <img> elements")
        check("<style" not in tsx, f"{slug}: no <style> embeds")
        check("<script" not in tsx, f"{slug}: no <script> embeds")
        check(
            "http://" not in tsx and "https://" not in tsx,
            f"{slug}: no external URLs",
        )
        check(
            "lorem" not in tsx.lower(),
            f"{slug}: no lorem ipsum",
        )
        check(
            "export function IntegrationsSection(" in tsx,
            f"{slug}: exports the IntegrationsSection component",
        )
        meta = json.loads((folder / "metadata.json").read_text())
        check(meta.get("family") == "Integrations", f"{slug}: metadata family")
        check(meta.get("subcategory") == "Integrations", f"{slug}: metadata subcategory")
        check(meta.get("type") == "section", f"{slug}: metadata type")
        check(meta.get("category") == "Sections", f"{slug}: metadata category")
        check(
            meta.get("direction")
            in ("Minimal", "Dark Premium", "Bento", "Neo-Brutalist"),
            f"{slug}: metadata direction",
        )
        check(meta.get("id") == f"integrations-{slug}", f"{slug}: metadata id")


def tsc_checks() -> None:
    """Strict-check every code.tsx via the esbuild/typescript toolchain.

    The copy lives under /tmp/dsbuild/src so tsconfig-free module resolution
    finds @types/react (same as the React Components gates).
    """
    esbuild_bin = Path("/tmp/dsbuild/node_modules/.bin/tsc")
    if not esbuild_bin.exists():
        check(False, "tsc toolchain missing at /tmp/dsbuild")
        return
    src = Path("/tmp/dsbuild/src")
    src.mkdir(parents=True, exist_ok=True)
    files = []
    for slug in SLUGS:
        out = src / f"integrations-{slug}.tsx"
        out.write_bytes(
            (ROOT / "React" / "Sections" / "Integrations" / slug / "code.tsx").read_bytes()
        )
        files.append(str(out))
    r = subprocess.run(
        [
            str(esbuild_bin),
            "--strict",
            "--noUncheckedIndexedAccess",
            "--jsx",
            "react-jsx",
            "--moduleResolution",
            "bundler",
            "--module",
            "esnext",
            "--target",
            "es2022",
            "--lib",
            "es2022,dom,dom.iterable",
            "--noEmit",
            "--skipLibCheck",
            *files,
        ],
        capture_output=True,
        text=True,
    )
    check(r.returncode == 0, f"tsc --strict --noUncheckedIndexedAccess passes ({r.stdout[:300]})")



def browser_checks() -> None:
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for slug in SLUGS:
            page = browser.new_page()
            errors: list[str] = []
            unexpected_requests: list[str] = []

            def _on_request(req):
                from urllib.parse import urlparse
                if req.resource_type == "document":
                    return
                host = urlparse(req.url).hostname or ""
                if host not in ALLOWED_NETWORK_HOSTS:
                    unexpected_requests.append(req.url)

            page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.on("request", _on_request)
            page.goto(BASE + f"{slug}/preview.html", wait_until="networkidle")
            page.wait_for_selector("#ds-root section", timeout=15000)

            # Structure: one h2, aria-labelledby wiring. All rendered
            # integration names and key authored strings appear as readable text.

            h2_count = page.evaluate(
                "document.querySelectorAll('#ds-root section h2').length"
            )
            check(h2_count == 1, f"{slug}: exactly one h2 in the section")
            labelled = page.evaluate(
                """(() => {
                    const s = document.querySelector('#ds-root section');
                    const id = s.getAttribute('aria-labelledby');
                    return !!id && !!document.getElementById(id);
                })()"""
            )
            check(labelled, f"{slug}: section aria-labelledby resolves")
            body_text = page.evaluate("document.querySelector('#ds-root section').textContent")
            for name in EXPECTED_NAMES[slug]:
                check(name in body_text, f"{slug}: renders readable name `{name}`")
            for text in EXPECTED_TEXTS[slug]:
                check(text in body_text, f"{slug}: renders `{text}`")

            # Decorative SVGs are aria-hidden (every glyph + connection layer).
            bad_glyphs = page.evaluate(
                """[...document.querySelectorAll('#ds-root section svg')]
                   .filter(el => el.getAttribute('aria-hidden') !== 'true').length"""
            )
            check(bad_glyphs == 0, f"{slug}: every section svg is aria-hidden")

            # Interactive surface: every variant ships exactly one semantic
            # anchor with a hash href (internal demo navigation, no network..
            links = page.query_selector_all("#ds-root section a[href]")
            check(
                len(links) == LINK_COUNTS[slug],
                f"{slug}: exactly {LINK_COUNTS[slug]} interactive link(s, got {len(links)})",
            )
            for link in links:
                href = link.get_attribute("href") or ""
                check(
                    href.startswith("#"),
                    f"{slug}: anchor href is an internal hash link ({href})",
                )

            # Zero horizontal overflow at every QA width, both themes, and
            # connection/shadow containment for the network variants.

            for width in WIDTHS:
                page.set_viewport_size({"width": width, "height": 900})
                for theme in ("light", "dark"):
                    page.evaluate(
                        "t => document.documentElement.setAttribute('data-theme', t)",
                        theme,
                    )
                    overflow = page.evaluate(
                        "document.documentElement.scrollWidth - document.documentElement.clientWidth"
                    )
                    check(
                        overflow <= 0,
                        f"{slug}: no h-overflow @ {width}px {theme} (got {overflow})",
                    )
                    if slug == "dark-premium":
                        contained = page.evaluate(
                            """(() => {
                                const panel = document.querySelector('#ds-root section .relative');
                                const svg = panel && panel.querySelector('svg');
                                if (!panel || !svg) return false;
                                const rp = panel.getBoundingClientRect();
                                const rs = svg.getBoundingClientRect();
                                return rs.left >= rp.left - 0.5 && rs.right <= rp.right + 0.5;
                            })()"""
                        )
                        check(
                            contained,
                            f"dark-premium: connection layer contained @ {width}px {theme}",
                        )
                    if slug == "neo-brutalist":
                        contained = page.evaluate(
                            """(() => {
                                const dv = document.documentElement.clientWidth;
                                const blocks = [...document.querySelectorAll('#ds-root section *')]
                                  .filter(el => el.className && String(el.className).includes('shadow-[4px'));
                                return blocks.every(b => b.getBoundingClientRect().right <= dv + 0.5);
                            })()"""
                        )
                        check(
                            contained,
                            f"neo-brutalist: offset shadows contained @ {width}px {theme}",
                        )

            # Theme flip: section surface + text change with page theme -
            # except the pinned Dark Premium variant, which must hold dark.
            page.set_viewport_size({"width": 1280, "height": 900})


            def section_colors(theme: str):
                page.evaluate(
                    "t => document.documentElement.setAttribute('data-theme', t)",
                    theme,
                )
                return page.evaluate(
                    """(() => {
                        const s = document.querySelector('#ds-root section');
                        const cs = getComputedStyle(s);
                        return [cs.backgroundColor, cs.color];
                    })()"""
                )


            light_bg, light_fg = section_colors("light")
            dark_bg, dark_fg = section_colors("dark")
            if slug == "dark-premium":
                check(
                    light_bg == dark_bg and light_fg == dark_fg,
                    "dark-premium: pinned dark mapping holds across page themes",
                )
                check(
                    light_bg != "rgb(250, 250, 250)",
                    "dark-premium: section is actually dark in a light page theme",
                )
            else:
                check(
                    light_bg != dark_bg and light_fg != dark_fg,
                    f"{slug}: surface + text flip with page theme",
                )

            # Focus-visible ring on every interactive link. Each variant
            # ships exactly one anchor; each must show a 2px outline. Then
            # ensure focusing + theme toggling + resizing after load triggers no
            # additional network requests beyond the preview shell's own CDNs..
            page.evaluate(
                "document.documentElement.setAttribute('data-theme', 'light')"
            )
            links = page.query_selector_all("#ds-root section a[href]")
            if links:
                for idx, link in enumerate(links):
                    link.focus()
                    outline = link.evaluate("el => getComputedStyle(el).outlineWidth")
                    check(
                        outline == "2px",
                        f"{slug}: link {idx + 1} focus-visible 2px outline (got {outline})",
                    )


            page.evaluate(
                "document.documentElement.setAttribute('data-theme', 'dark')"
            )
            page.evaluate(
                "document.documentElement.setAttribute('data-theme', 'light')"
            )
            page.set_viewport_size({"width": 375, "height": 900})
            page.set_viewport_size({"width": 1280, "height": 900})
            if links:
                links[0].focus()
                links[0].press("Enter")

            check(
                unexpected_requests == [],
                f"{slug}: no section-driven network requests, got {unexpected_requests[:3]}",
            )

            # Reduced motion kills transitions..
            page.emulate_media(reduced_motion="reduce")
            transitioned = page.query_selector(
                "#ds-root section a[href], #ds-root section [class*='transition']"
            )
            if transitioned is not None:
                prop = transitioned.evaluate(
                    "el => getComputedStyle(el).transitionProperty"
                )
                check(
                    prop == "none",
                    f"{slug}: reduced-motion transition-property none (got {prop})",
                )
            page.emulate_media(reduced_motion="no-preference")

            check(errors == [], f"{slug}: zero console errors, got {errors[:3]}")
            page.close()


        browser.close()


def generator_checks() -> None:
    drift = subprocess.run(
        [sys.executable, str(ROOT / "_gen_react_sections_integrations.py"), "--check"],
        capture_output=True,
        text=True,
    )
    check(drift.returncode == 0, "generator --check reports no drift")
    validate = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate.py")],
        capture_output=True,
        text=True,
    )
    check(validate.returncode == 0, "scripts/validate.py passes")


def main() -> int:
    static_checks()
    tsc_checks()
    generator_checks()
    browser_checks()
    print(f"\n{checks} checks, {len(failures)} failures")
    if failures:
        print("FAILURES:")
        for failure in failures:
            print(" -", failure)
        return 1
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())