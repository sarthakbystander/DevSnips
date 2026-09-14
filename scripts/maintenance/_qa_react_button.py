#!/usr/bin/env python3
"""QA harness for a migrated React button preview.

Usage: python3 _qa_react_button.py <slug> [--base http://localhost:8765]

Checks: page errors, console errors, horizontal overflow at 375/768/1280,
light/dark computed styles for the first themed button, focus-visible
outline, disabled opacity, and a screenshot to /tmp.
"""
import asyncio
import sys
from pathlib import Path
from playwright.async_api import async_playwright

BASE = "http://localhost:8765"


async def main(slug):
    url = f"{BASE}/React/Components/Buttons/{slug}/preview.html"
    fails = []
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context()
        page = await ctx.new_page()
        errors = []
        page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
        page.on("console", lambda m: errors.append(f"console.{m.type}: {m.text}") if m.type == "error" else None)
        await page.goto(url, wait_until="networkidle")
        try:
            await page.wait_for_selector("button", timeout=8000)
        except Exception:
            fails.append("no <button> rendered")
        # overflow at widths
        for w in (375, 768, 1280):
            await page.set_viewport_size({"width": w, "height": 900})
            await page.wait_for_timeout(200)
            ov = await page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            if ov > 0:
                fails.append(f"overflow {ov}px at {w}")
        # light/dark styles on first button
        await page.set_viewport_size({"width": 1280, "height": 900})
        await page.evaluate("document.documentElement.setAttribute('data-theme','light')")
        await page.wait_for_timeout(250)
        btn = page.locator("#ds-root button").first
        if await btn.count():
            h = await btn.bounding_box()
            h = h["height"] if h else 0
            bgl = await btn.evaluate("e => getComputedStyle(e).backgroundColor")
            await page.evaluate("document.documentElement.setAttribute('data-theme','dark')")
            await page.wait_for_timeout(250)
            bgd = await btn.evaluate("e => getComputedStyle(e).backgroundColor")
            transparent = bgl in ("rgba(0, 0, 0, 0)", "transparent")
            print(f"{slug}: height={h:.0f} light_bg={bgl} dark_bg={bgd}")
            if not transparent and bgl == bgd:
                fails.append(f"theme not switching (bg identical): {bgl}")
            # link-button is intentionally inline (no fixed height); others 28-48
            if slug != "link-button" and not (20 <= h <= 64):
                fails.append(f"button height {h} out of 20-64 range")
        # focus-visible (keyboard-focus the first root interactive control)
        await page.evaluate("document.documentElement.setAttribute('data-theme','light')")
        has_btn = await page.evaluate("!!document.querySelector('#ds-root button, #ds-root a')")
        if has_btn:
            await page.evaluate("document.querySelector('#ds-root button, #ds-root a').focus()")
            await page.keyboard.press("Tab")
            await page.wait_for_timeout(300)
            has_fv = await page.evaluate("!!document.querySelector('#ds-root button:focus-visible, #ds-root a:focus-visible')")
            if not has_fv:
                fails.append("no focus-visible after keyboard focus + Tab")
        # disabled opacity if present
        d = page.locator("#ds-root button[disabled]")
        if await d.count():
            op = await d.first.evaluate("e => getComputedStyle(e).opacity")
            if float(op) > 0.9:
                fails.append(f"disabled opacity {op} too high")
        # screenshot
        out = Path(f"/tmp/qa_{slug}.png")
        await page.screenshot(path=str(out), full_page=True)
        if errors:
            fails.extend(errors[:6])
        await browser.close()
    if fails:
        print(f"FAIL {slug}:")
        for f in fails:
            print("  - " + f)
        sys.exit(1)
    print(f"PASS {slug}")


if __name__ == "__main__":
    slug = sys.argv[1]
    asyncio.run(main(slug))
