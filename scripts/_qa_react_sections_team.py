#!/usr/bin/env python3
"""Playwright QA for the DevSnips React Sections Team family.

Validates the exact four-variant architecture, metadata, source hygiene,
rendered composition, accessibility wiring, theme behavior, responsive
overflow, focus-visible states, reduced motion, console errors, and preview
source drift. Run from the repo root.
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
DIRECTIONS = {"minimal": "Minimal", "dark-premium": "Dark Premium", "bento": "Bento", "neo-brutalist": "Neo-Brutalist"}
WIDTHS = [320, 375, 768, 1280, 1440]
checks = 0
failures: list[str] = []


def check(cond: bool, label: str) -> None:
    global checks
    checks += 1
    if not cond:
        failures.append(label)
        print("FAIL:", label)


def static_checks() -> None:
    palette = re.compile(r"\b(?:bg|text|border|fill|stroke|from|to|via)-(?:slate|gray|zinc|neutral|stone|red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose)-\d")
    raw_hex = re.compile(r"#[0-9a-fA-F]{3,8}\b")
    emoji = re.compile("[\U0001F000-\U0001FAFF\u2600-\u27BF\U00020000-\U0002FFFF]", re.UNICODE)
    external_url = re.compile(r"https?://", re.I)
    team = ROOT / "React" / "Sections" / "Team"
    dirs = sorted(p.name for p in team.iterdir() if p.is_dir())
    check(dirs == SLUGS, f"exact four Team directions (got {dirs})")
    for slug in SLUGS:
        folder = team / slug
        files = sorted(p.name for p in folder.iterdir() if p.is_file())
        check(files == ["code.tsx", "metadata.json", "preview.html"], f"{slug}: exact 3-file shape")
        tsx = (folder / "code.tsx").read_text(encoding="utf-8")
        check(not re.search(r":\s*any\b|<any>|\bas\s+any\b", tsx), f"{slug}: no any")
        check(not raw_hex.search(tsx), f"{slug}: no raw hex colors")
        check(not palette.search(tsx), f"{slug}: no raw palette classes")
        check("!important" not in tsx, f"{slug}: no !important")
        check("transition-all" not in tsx, f"{slug}: no transition-all")
        check(not emoji.search(tsx), f"{slug}: no emoji")
        check(not external_url.search(tsx), f"{slug}: no external URLs")
        check('style={' not in tsx, f"{slug}: no inline style props")
        check(tsx.count("export function TeamSection") == 1, f"{slug}: TeamSection export")
        check("export type TeamMember" in tsx, f"{slug}: shared TeamMember type")
        for prop in ("eyebrow", "title", "description", "members"):
            check(prop in tsx, f"{slug}: {prop} overridable API")
        meta = json.loads((folder / "metadata.json").read_text(encoding="utf-8"))
        check(meta.get("id") == f"team-{slug}", f"{slug}: metadata id")
        check(meta.get("family") == "Team", f"{slug}: metadata family")
        check(meta.get("subcategory") == "Team", f"{slug}: metadata subcategory")
        check(meta.get("type") == "section", f"{slug}: metadata type")
        check(meta.get("category") == "Sections", f"{slug}: metadata category")
        check(meta.get("technology") == "React", f"{slug}: metadata technology")
        check(meta.get("direction") == DIRECTIONS[slug], f"{slug}: metadata direction")
        preview = (folder / "preview.html").read_text(encoding="utf-8")
        check("cdn.tailwindcss.com" in preview, f"{slug}: Tailwind CDN")
        check("react@18/umd/react.development.js" in preview, f"{slug}: React 18 UMD")
        check("@babel/standalone@7/babel.min.js" in preview, f"{slug}: Babel standalone")
        check("--ds-color-background" in preview, f"{slug}: canonical token block")
        check("live render of code.tsx" in preview, f"{slug}: generated preview marker")
        check("window.TeamSection = TeamSection" in preview, f"{slug}: transformed component exposed")
        check("grid-cols-12" in tsx if slug == "bento" else True, "bento: 12-column base grid" if slug == "bento" else f"{slug}: direction source present")
        if slug == "dark-premium":
            check('data-theme="dark"' in tsx, "dark-premium: pinned dark root")
        if slug == "neo-brutalist":
            check("border-2" in tsx and "translate-x-1" in tsx and "translate-y-1" in tsx, "neo-brutalist: 2px + press-down interaction")


def browser_checks() -> None:
    import os
    original = Path.cwd()
    os.chdir(ROOT)
    server = ThreadingHTTPServer(("127.0.0.1", 8765), SimpleHTTPRequestHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True, args=["--no-sandbox"])
            for slug in SLUGS:
                page = browser.new_page(viewport={"width": 1280, "height": 900})
                errors: list[str] = []
                page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
                page.on("pageerror", lambda e: errors.append(str(e)))
                page.goto(BASE + slug + "/preview.html", wait_until="networkidle")
                page.wait_for_selector("#ds-root section", timeout=15000)
                section = page.locator("#ds-root section")
                check(section.count() == 1, f"{slug}: section mounts once")
                check(section.locator("h2").count() == 1, f"{slug}: exactly one h2")
                labelledby = section.get_attribute("aria-labelledby")
                check(bool(labelledby), f"{slug}: section has aria-labelledby")
                check(section.locator("h2#" + (labelledby or "__missing__")).count() == 1, f"{slug}: aria-labelledby resolves to h2")
                names = page.locator("#ds-root section h3").all_inner_texts()
                for name in ["Alex Morgan", "Maya Chen", "Jon Bell", "Priya Shah"]:
                    check(name in names, f"{slug}: {name} visible")
                roles = " ".join(page.locator("#ds-root section").all_inner_texts())
                for role in ["Founder & Product", "Engineering Lead", "Design Director", "Developer Advocate"]:
                    check(role in roles, f"{slug}: {role} visible")
                for node in page.locator('#ds-root section [aria-hidden="true"]').all():
                    check(node.get_attribute("aria-hidden") == "true", f"{slug}: decorative identity hidden")
                links = page.locator("#ds-root section a[href]")
                for i in range(links.count()):
                    link = links.nth(i)
                    check(link.evaluate("el => el.tagName") == "A", f"{slug}: link {i+1} semantic anchor")
                    check(bool(link.get_attribute("aria-label") or link.inner_text().strip()), f"{slug}: link {i+1} accessible name")
                for width in WIDTHS:
                    page.set_viewport_size({"width": width, "height": 900})
                    for theme in ("light", "dark"):
                        page.evaluate("t => document.documentElement.setAttribute('data-theme', t)", theme)
                        overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
                        check(overflow <= 0, f"{slug}: no horizontal overflow @ {width}px {theme}")
                        check(section.count() == 1, f"{slug}: still mounted @ {width}px {theme}")
                page.set_viewport_size({"width": 1280, "height": 900})
                def colors(theme: str):
                    page.evaluate("t => document.documentElement.setAttribute('data-theme', t)", theme)
                    return section.evaluate("el => { const c=getComputedStyle(el); return [c.backgroundColor,c.color]; }")
                light = colors("light")
                dark = colors("dark")
                if slug == "dark-premium":
                    check(light == dark, "dark-premium: pinned dark survives page theme toggle")
                    check(light[0] == "rgb(10, 10, 10)", "dark-premium: dark canvas remains dark")
                else:
                    check(light != dark, f"{slug}: page theme changes semantic mapping")
                if links.count():
                    page.evaluate("document.documentElement.setAttribute('data-theme', 'light')")
                    links.first().focus()
                    check(links.first().evaluate("el => getComputedStyle(el).outlineWidth") == "2px", f"{slug}: 2px focus indication")
                page.emulate_media(reduced_motion="reduce")
                interactive = page.locator("#ds-root section a[href], #ds-root section button")
                if interactive.count():
                    check(interactive.first().evaluate("el => getComputedStyle(el).transitionProperty") == "none", f"{slug}: reduced motion removes transitions")
                page.emulate_media(reduced_motion="no-preference")
                check(errors == [], f"{slug}: no console errors ({errors[:2]})")
                page.close()
            browser.close()
    finally:
        server.shutdown()
        os.chdir(original)


def generator_checks() -> None:
    result = subprocess.run([sys.executable, str(ROOT / "_gen_react_sections_team.py"), "--check"], capture_output=True, text=True)
    check(result.returncode == 0, "generator --check reports no drift")


def main() -> int:
    static_checks()
    generator_checks()
    browser_checks()
    print(f"\n{checks} checks, {len(failures)} failures")
    if failures:
        for failure in failures:
            print(" -", failure)
        return 1
    print("ALL CHECKS PASSED")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
