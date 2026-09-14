#!/usr/bin/env python3
"""Playwright QA for the React Sections Team previews.

Verifies the same behavior-critical guarantees used by the existing React
section-family QA scripts: preview generation fidelity, source hygiene,
metadata, semantic structure, responsive rendering, both page themes,
pinned dark behavior, focus-visible treatment, reduced motion, console/page
errors, and direction-specific rendered composition.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
BASE = "http://127.0.0.1:8765/React/Sections/Team/"
SLUGS = ["minimal", "dark-premium", "bento", "neo-brutalist"]
DIRECTIONS = {
    "minimal": "Minimal",
    "dark-premium": "Dark Premium",
    "bento": "Bento",
    "neo-brutalist": "Neo-Brutalist",
}
WIDTHS = [320, 375, 768, 1024, 1280, 1440]

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
        "[\U0001F000-\U0001FAFF☀-➿\U00020000-\U0002FFFF]", re.UNICODE
    )
    family_dir = ROOT / "React" / "Sections" / "Team"
    dirs = sorted(p.name for p in family_dir.iterdir() if p.is_dir())
    check(dirs == sorted(SLUGS), f"exactly four variant directories, got {dirs}")

    canonical = {
        "eyebrow": "text-xs",
        "heading": "text-[clamp(1.875rem,1.65rem+1vw,2.25rem)]",
        "lede": "text-[clamp(1rem,0.95rem+0.25vw,1.125rem)]",
        "padding": "py-[clamp(4rem,3rem+4vw,6rem)]",
        "container": "max-w-[1280px]",
    }

    for slug in SLUGS:
        folder = family_dir / slug
        files = sorted(p.name for p in folder.iterdir() if p.is_file())
        check(files == ["code.tsx", "metadata.json", "preview.html"], f"{slug}: exact 3-file shape")
        tsx = (folder / "code.tsx").read_text(encoding="utf-8")
        check(not re.search(r":\s*any\b|<any>|\bas\s+any\b", tsx), f"{slug}: no `any`")
        check(not hex_lit.search(tsx.replace("#000", "")), f"{slug}: no hex literals outside sanctioned color-mix")
        check(not palette.search(tsx), f"{slug}: no raw Tailwind palette utilities")
        check("!important" not in tsx, f"{slug}: no !important")
        check("transition-all" not in tsx, f"{slug}: no transition-all")
        check("z-[" not in tsx, f"{slug}: no arbitrary z-index")
        check(not emoji.search(tsx), f"{slug}: no emoji")
        check("style=" not in tsx and "style={" not in tsx, f"{slug}: no inline style props")
        check("<img" not in tsx, f"{slug}: no external-image dependency")
        check("http://" not in tsx and "https://" not in tsx, f"{slug}: no external URLs")
        check("lorem" not in tsx.lower(), f"{slug}: no lorem ipsum")
        check(tsx.count("export function TeamSection") == 1, f"{slug}: one TeamSection export")
        check("export type TeamMember" in tsx, f"{slug}: typed TeamMember")
        check("export interface TeamSectionProps" in tsx, f"{slug}: typed TeamSectionProps")
        for prop in ("eyebrow", "title", "description", "members"):
            check(prop in tsx, f"{slug}: overridable prop `{prop}`")
        for label, needle in canonical.items():
            check(needle in tsx, f"{slug}: canonical section {label} scale")

        meta = json.loads((folder / "metadata.json").read_text(encoding="utf-8"))
        check(meta.get("id") == f"team-{slug}", f"{slug}: metadata id")
        check(meta.get("name") == f"Team — {DIRECTIONS[slug]}", f"{slug}: metadata name")
        check(meta.get("technology") == "React", f"{slug}: metadata technology")
        check(meta.get("category") == "Sections", f"{slug}: metadata category")
        check(meta.get("subcategory") == "Team", f"{slug}: metadata subcategory")
        check(meta.get("family") == "Team", f"{slug}: metadata family")
        check(meta.get("direction") == DIRECTIONS[slug], f"{slug}: metadata direction")
        check(meta.get("type") == "section", f"{slug}: metadata type")
        check(meta.get("responsive") is True, f"{slug}: metadata responsive")
        check(meta.get("dependencies") == [], f"{slug}: metadata dependencies")

        preview = (folder / "preview.html").read_text(encoding="utf-8")
        check("cdn.tailwindcss.com" in preview, f"{slug}: Tailwind CDN")
        check("react@18/umd/react.development.js" in preview, f"{slug}: React 18 UMD")
        check("react-dom@18/umd/react-dom.development.js" in preview, f"{slug}: ReactDOM 18 UMD")
        check("@babel/standalone@7/babel.min.js" in preview, f"{slug}: Babel standalone")
        check(preview.count('type="text/babel"') >= 2, f"{slug}: separate component/mount Babel blocks")
        check('data-presets="react"' in preview, f"{slug}: canonical Babel preset")
        check("ReactDOM.createRoot(document.getElementById(\"ds-root\")).render(<TeamSection />);" in preview, f"{slug}: canonical mount pattern")
        check("--ds-color-surface" in preview, f"{slug}: canonical token block")
        check("--ds-color-border" in preview, f"{slug}: canonical border token")
        check("live render of code.tsx" in preview, f"{slug}: generated preview marker")

        if slug == "dark-premium":
            check('data-theme="dark"' in tsx, "dark-premium: pinned dark root")
        if slug == "bento":
            check("grid-cols-12" in tsx, "bento: 12-column base grid")
            check("lg:col-span-7" in tsx and "lg:col-span-5" in tsx, "bento: 7/5 top-row structure")
            check("gap-4" in tsx and "lg:gap-6" in tsx, "bento: responsive grid gap")
        if slug == "neo-brutalist":
            check("border-2" in tsx, "neo-brutalist: 2px borders")
            check("shadow-[4px_4px_0_0_var(--ds-color-border-strong)]" in tsx, "neo-brutalist: hard offset shadow")
            check("active:translate-x-1" in tsx and "active:translate-y-1" in tsx, "neo-brutalist: press-down interaction")


def browser_checks() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 8765), SimpleHTTPRequestHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            for slug in SLUGS:
                page = browser.new_page(viewport={"width": 1280, "height": 900})
                console_errors: list[str] = []
                page_errors: list[str] = []
                page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
                page.on("pageerror", lambda e: page_errors.append(str(e)))
                page.goto(BASE + slug + "/preview.html", wait_until="networkidle")
                page.wait_for_selector("#ds-root section", timeout=15000)

                section = page.locator("#ds-root section")
                check(section.count() == 1, f"{slug}: section mounts once")
                check(section.locator("h2").count() == 1, f"{slug}: exactly one h2")
                labelledby = section.get_attribute("aria-labelledby")
                check(bool(labelledby), f"{slug}: aria-labelledby exists")
                if labelledby:
                    matched = page.locator("#ds-root section h2").evaluate_all(
                        "(els, id) => els.filter(el => el.id === id).length",
                        labelledby,
                    )
                    check(matched == 1, f"{slug}: aria-labelledby resolves to h2")

                semantic_text = section.text_content() or ""
                for name in ["Alex Morgan", "Maya Chen", "Jon Bell", "Priya Shah"]:
                    check(name in semantic_text, f"{slug}: {name} rendered")
                for role in ["Founder & Product", "Engineering Lead", "Design Director", "Developer Advocate"]:
                    check(role in semantic_text, f"{slug}: {role} rendered")

                links = section.locator("a[href]")
                for index in range(links.count()):
                    link = links.nth(index)
                    check(link.evaluate("el => el.tagName") == "A", f"{slug}: link {index + 1} semantic")
                    check(bool(link.get_attribute("aria-label") or link.text_content().strip()), f"{slug}: link {index + 1} accessible name")

                for width in WIDTHS:
                    page.set_viewport_size({"width": width, "height": 900})
                    for theme in ("light", "dark"):
                        page.evaluate("t => document.documentElement.setAttribute('data-theme', t)", theme)
                        overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
                        check(overflow <= 0, f"{slug}: no horizontal overflow @ {width}px {theme} (got {overflow})")

                page.set_viewport_size({"width": 1280, "height": 900})
                page.evaluate("document.documentElement.setAttribute('data-theme', 'light')")
                for index in range(links.count()):
                    link = links.nth(index)
                    link.focus()
                    check(link.evaluate("el => getComputedStyle(el).outlineWidth") == "2px", f"{slug}: link {index + 1} focus-visible 2px")

                page.emulate_media(reduced_motion="reduce")
                transition_nodes = section.locator("[class*='transition']")
                for index in range(min(transition_nodes.count(), 3)):
                    check(transition_nodes.nth(index).evaluate("el => getComputedStyle(el).transitionProperty") == "none", f"{slug}: reduced-motion transition {index + 1} disabled")
                page.emulate_media(reduced_motion="no-preference")

                def colors(theme: str):
                    page.evaluate("t => document.documentElement.setAttribute('data-theme', t)", theme)
                    return section.evaluate("el => { const c=getComputedStyle(el); return [c.backgroundColor,c.color]; }")

                light = colors("light")
                dark = colors("dark")
                if slug == "dark-premium":
                    check(light == dark, "dark-premium: pinned dark survives page theme toggle")
                    check(light[0] == "rgb(10, 10, 10)", "dark-premium: canvas stays dark")
                else:
                    check(light != dark, f"{slug}: semantic surface/text flip")

                if slug == "minimal":
                    check(section.locator("li").count() == 4, "minimal: four member rows render")
                elif slug == "dark-premium":
                    split = section.locator("div.grid").first
                    cols = split.evaluate("el => getComputedStyle(el).gridTemplateColumns")
                    check(len(cols.split(" ")) >= 2, "dark-premium: rendered split grid has two columns")
                elif slug == "bento":
                    grids = section.locator("div.grid")
                    twelve = any(
                        len(grids.nth(i).evaluate("el => getComputedStyle(el).gridTemplateColumns").split(" ")) == 12
                        for i in range(grids.count())
                    )
                    check(twelve, "bento: rendered grid resolves to 12 columns")
                elif slug == "neo-brutalist":
                    panel = section.locator("article").first
                    check(panel.evaluate("el => getComputedStyle(el).borderTopWidth") == "2px", "neo-brutalist: rendered 2px border")
                    shadow = panel.evaluate("el => getComputedStyle(el).boxShadow")
                    check("4px" in shadow and "0px" in shadow, "neo-brutalist: rendered hard offset shadow")

                check(console_errors == [], f"{slug}: zero console errors ({console_errors[:2]})")
                check(page_errors == [], f"{slug}: zero page errors ({page_errors[:2]})")
                page.close()
            browser.close()
    finally:
        server.shutdown()


def generator_checks() -> None:
    drift = subprocess.run(
        [sys.executable, str(ROOT / "_gen_react_sections_team.py"), "--check"],
        capture_output=True,
        text=True,
    )
    check(drift.returncode == 0, "_gen_react_sections_team.py --check passes")

    validate = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate.py")],
        capture_output=True,
        text=True,
    )
    check(validate.returncode == 0, "scripts/validate.py passes")


def main() -> int:
    static_checks()
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
    raise SystemExit(main())
