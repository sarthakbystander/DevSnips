#!/usr/bin/env python3
"""Interaction QA for Tailwind resources: wiring smoke test.

Runs the changed `preview.html` files under `library/Tailwind/` (working-tree
diff vs HEAD; pass `--all` for the full sweep) in headless Chromium and, per
page, asserts:

- the page never produces page errors or console errors;
- every `[aria-haspopup]` trigger toggles its `aria-controls` target open
  (visibility + `aria-expanded=true`), and Escape closes it again
  (`aria-expanded=false` + hidden, polled so animated closes pass);
- every `[data-bind]` element activates without error (click, or `change`
  dispatch for form controls).

Run it after editing Tailwind resources and before committing, so the
working-tree diff still shows what changed. `qa_tailwind.py` covers the
runtime/console/overflow layer; this one covers the interaction layer.

Usage:
  python scripts/qa/resources/qa_tailwind_interactions.py             # changed vs HEAD
  python scripts/qa/resources/qa_tailwind_interactions.py --all       # full sweep
  python scripts/qa/resources/qa_tailwind_interactions.py --limit 10  # smoke subset
"""
import argparse
import asyncio
import shutil
import subprocess
import sys
from pathlib import Path

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[3]
TAILWIND = ROOT / "library" / "Tailwind"


def changed_previews():
    r = subprocess.run(
        [shutil.which("git"), "diff", "--name-only", "HEAD", "--", "library/Tailwind"],
        capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=ROOT,
    )
    return sorted(ROOT / line for line in r.stdout.splitlines()
                  if line.endswith("preview.html"))


def all_previews():
    return sorted(TAILWIND.rglob("preview.html"))


async def qa(page, path):
    problems = []
    msgs = []
    page.on("pageerror", lambda e: msgs.append(f"pageerror: {e}"))
    page.on("console", lambda m: msgs.append(f"console.error: {m.text}")
            if m.type == "error" else None)
    try:
        await page.goto(path.as_uri(), wait_until="networkidle")
        await page.wait_for_timeout(250)

        triggers = page.locator("[aria-haspopup]")
        n = await triggers.count()
        for i in range(n):
            t = triggers.nth(i)
            controls = await t.get_attribute("aria-controls")
            if not controls:
                if await t.is_visible():
                    await t.click(timeout=3000)
                    await page.wait_for_timeout(120)
                continue
            menu = page.locator(f"#{controls}")
            before = await menu.evaluate("el => el.classList.contains('hidden')")
            if "mega-menu" in str(path):
                # products-menu is hover-driven; the nested docs-menu is
                # click-driven. Try hover first, fall back to click.
                await t.hover()
                await page.wait_for_timeout(150)
                after = await menu.evaluate("el => el.classList.contains('hidden')")
                if after:
                    await t.click(timeout=3000)
                    await page.wait_for_timeout(150)
                    after = await menu.evaluate("el => el.classList.contains('hidden')")
                    if after:
                        problems.append(f"{controls}: neither hover nor click opened")
                        continue
                await page.mouse.move(10, 400)
                await page.keyboard.press("Escape")
                await page.wait_for_timeout(150)
                closed = await menu.evaluate("el => el.classList.contains('hidden')")
                if not closed:
                    problems.append(f"{controls}: did not close after Escape")
                continue
            if not await t.is_visible():
                continue
            await t.click(timeout=3000)
            after = await menu.evaluate("el => el.classList.contains('hidden')")
            expanded = await t.get_attribute("aria-expanded")
            if before == after:
                problems.append(f"{controls}: click did not toggle visibility")
            if expanded != "true":
                problems.append(f"{controls}: aria-expanded={expanded} after open")
            await page.keyboard.press("Escape")
            closed = False
            exp2 = None
            for _ in range(10):  # close may be animated (e.g. slide-over 300ms)
                await page.wait_for_timeout(100)
                closed = await menu.evaluate("el => el.classList.contains('hidden')")
                if closed:
                    exp2 = await t.get_attribute("aria-expanded")
                    break
            if not closed:
                problems.append(f"{controls}: Escape did not close")
            if exp2 != "false":
                problems.append(f"{controls}: aria-expanded={exp2} after Escape")

        bound = page.locator("[data-bind]")
        n = await bound.count()
        for i in range(n):
            el = bound.nth(i)
            if await el.is_visible():
                tag = (await el.evaluate("el => el.tagName")).lower()
                if tag in ("input", "select", "textarea"):
                    await el.dispatch_event("change")
                    await page.wait_for_timeout(80)
                else:
                    await el.click(timeout=3000)
                    await page.wait_for_timeout(80)

        if msgs:
            problems.append("errors: " + " | ".join(msgs))
    except Exception as e:
        problems.append(f"load failed: {e}")
    return problems


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true",
                    help="sweep every Tailwind preview instead of the changed ones")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()
    files = all_previews() if args.all else changed_previews()
    if args.limit:
        files = files[: args.limit]
    print(f"{len(files)} previews to check")
    failing = []
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        for f in files:
            problems = await qa(page, f)
            rel = f.relative_to(ROOT)
            if problems:
                failing.append(rel)
                for pr in problems:
                    print(f"FAIL {rel}: {pr}")
            else:
                print(f"pass {rel}")
        await browser.close()
    print(f"\n{len(failing)} failing of {len(files)}")
    sys.exit(1 if failing else 0)


if __name__ == "__main__":
    asyncio.run(main())
