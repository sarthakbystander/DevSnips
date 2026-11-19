#!/usr/bin/env python3
"""Browser QA for Tailwind resources: runtime, console, and overflow checks.

Loads every `preview.html` under `library/Tailwind/` in headless Chromium
(preview.html is a full page that loads the Tailwind CDN, so network access is
required) and, per page, asserts:

- no uncaught page errors (JS exceptions) — required;
- no console errors — required;
- no horizontal overflow at 375px and 1280px — required.

The Playwright harnesses are the heavier QA layer; run them when your change
is visual or interactive. See `agents/resources/qa.md`.

Usage:
  python scripts/qa/resources/qa_tailwind.py                 # full sweep
  python scripts/qa/resources/qa_tailwind.py --only-failures # print failures only
  python scripts/qa/resources/qa_tailwind.py --json          # machine-readable
  python scripts/qa/resources/qa_tailwind.py --limit 10      # smoke subset
"""
import argparse
import asyncio
import json
import sys
from pathlib import Path

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[3]
TAILWIND = ROOT / "library" / "Tailwind"

WIDTHS = [375, 1280]
DEFAULT_WORKERS = 4


def previews():
    for subdir in ("Components", "Sections", "Templates"):
        base = TAILWIND / subdir
        if base.exists():
            yield from sorted(base.rglob("preview.html"))


async def qa_preview(context, path: Path) -> list[str]:
    """Return the list of required-check failures for one preview page."""
    errors = []
    page = await context.new_page()
    try:
        msgs = []
        page.on(
            "console",
            lambda m: msgs.append(f"console.{m.type}: {m.text}") if m.type == "error" else None,
        )
        page.on("pageerror", lambda e: msgs.append(f"pageerror: {e}"))

        await page.goto(path.as_uri(), wait_until="networkidle")
        await page.wait_for_timeout(400)

        for width in WIDTHS:
            await page.set_viewport_size({"width": width, "height": 900})
            await page.wait_for_timeout(150)
            over = await page.evaluate(
                "document.documentElement.scrollWidth - document.documentElement.clientWidth"
            )
            if over > 1:
                errors.append(f"overflow at {width}px: +{over}px")

        if msgs:
            errors.append("console/page errors: " + " | ".join(msgs))
    except Exception as e:  # navigation itself failed
        errors.append(f"page load failed: {e}")
    finally:
        await page.close()
    return errors


async def run_batch(files, workers: int):
    results = {}
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        try:
            sem = asyncio.Semaphore(workers)

            async def one(path: Path):
                async with sem:
                    context = await browser.new_context()
                    try:
                        return path, await qa_preview(context, path)
                    finally:
                        await context.close()

            for path, errs in await asyncio.gather(*(one(f) for f in files)):
                results[path] = errs
        finally:
            await browser.close()
    return results


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--only-failures", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--limit", type=int, default=0, help="check only the first N previews")
    ap.add_argument("--workers", type=int, default=DEFAULT_WORKERS)
    args = ap.parse_args()

    files = list(previews())
    if args.limit:
        files = files[: args.limit]

    results = asyncio.run(run_batch(files, args.workers))

    failures = {str(p.relative_to(ROOT)): errs for p, errs in results.items() if errs}

    if args.json:
        print(json.dumps({"checked": len(results), "failing": failures}, indent=2))
        sys.exit(0 if not failures else 1)

    if args.only_failures:
        for path, errs in failures.items():
            for e in errs:
                print(f"FAIL {path}: {e}")
    else:
        for path, errs in sorted(failures.items()):
            for e in errs:
                print(f"FAIL {path}: {e}")
        print(f"qa: scanned: {len(results)} Tailwind previews")

    if failures:
        print(f"qa: failing previews: {len(failures)}")
        sys.exit(1)
    print("qa: all Tailwind preview checks passed")


if __name__ == "__main__":
    main()
