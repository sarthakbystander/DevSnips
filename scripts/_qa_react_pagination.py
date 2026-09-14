#!/usr/bin/env python3
"""QA harness for the DevSnips React Pagination family.

Static checks (per variant):
  - 5-file shape (code.tsx, code.jsx, preview.html, metadata.json, README.md)
  - metadata.json valid + required schema fields
  - no `any` in code.tsx
  - TSX/JSX export parity (same exported component names + default export)

Browser checks (Playwright, per preview):
  - 0 console errors, 0 page errors
  - 0 horizontal overflow at 375 / 768 / 1280
  - exactly one nav landmark with aria-label, exactly one aria-current="page"
  - reference: clicking a page moves aria-current; Previous disabled at page 1
  - ellipsis: window math at boundaries + middle; no ellipsis when all fits
  - compact = 32px, reference = 36px, large = 44px control height
  - page-size select changes the row count and resets to page 1
  - disabled: aria-disabled spans are not focusable/activatable
  - focus-visible outline on keyboard focus; dark-mode token flip;
    reduced-motion transition-none

Run: python3 scripts/_qa_react_pagination.py
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGINATION = ROOT / "React/Components/Pagination"
SLUGS = [
    "pagination",
    "pagination-with-previous-next",
    "pagination-with-numbers",
    "pagination-with-ellipsis",
    "pagination-compact",
    "pagination-large",
    "pagination-with-page-size",
    "pagination-disabled",
]
FILES = ["code.tsx", "code.jsx", "preview.html", "metadata.json", "README.md"]
WIDTHS = [375, 768, 1280]

failures: list[str] = []
checks = 0


def check(ok: bool, label: str):
    global checks
    checks += 1
    if not ok:
        failures.append(label)
        print(f"  FAIL {label}")


def static_checks():
    print("static checks")
    for slug in SLUGS:
        folder = PAGINATION / slug
        check(folder.is_dir(), f"{slug}: folder exists")
        for name in FILES:
            check((folder / name).is_file(), f"{slug}: {name} exists")
        meta = json.loads((folder / "metadata.json").read_text())
        for key in ["id", "name", "slug", "component", "family", "variant", "description",
                    "framework", "language", "languages", "technology", "type", "category",
                    "subcategory", "styling", "tags", "features", "responsive", "darkMode",
                    "accessibility", "interactive", "dependencies", "source", "related"]:
            check(key in meta, f"{slug}: metadata has {key}")
        check(meta["technology"] == "react", f"{slug}: technology react")
        check(meta["type"] == "component", f"{slug}: type component")
        check(meta["category"] == "Pagination", f"{slug}: category Pagination")
        check(meta["styling"] == "Tailwind CSS", f"{slug}: styling Tailwind CSS")
        check(meta["languages"] == ["JSX", "TSX"], f"{slug}: languages JSX+TSX")
        check(meta["slug"] == slug, f"{slug}: metadata slug matches folder")
        tsx = (folder / "code.tsx").read_text()
        jsx = (folder / "code.jsx").read_text()
        check(not re.search(r"\bany\b", tsx), f"{slug}: no any in code.tsx")
        check("<div onClick" not in tsx, f"{slug}: no div onClick")
        tsx_exports = sorted(re.findall(r"export function ([A-Za-z_$][\w$]*)", tsx))
        m = re.search(r"\nexport \{([^}]*)\};", jsx)
        jsx_exports = sorted(x.strip() for x in m.group(1).split(",")) if m else []
        check(tsx_exports == jsx_exports, f"{slug}: export parity {tsx_exports} vs {jsx_exports}")
        check("export default Pagination;" in jsx, f"{slug}: JSX default export")
        check("usePagination" in jsx, f"{slug}: JSX keeps context hook")
        check("sr-only" in tsx, f"{slug}: ellipsis sr-only text")
        check('aria-current' in tsx, f"{slug}: aria-current present")
        check("<nav aria-label={label}" in tsx, f"{slug}: nav landmark")


def link_labels(nav):
    """Visible text of every control inside the nav, in order."""
    return [t.strip() for t in nav.locator("a, button, span[aria-disabled], li > span").all_inner_texts()]


def browser_checks():
    from playwright.sync_api import sync_playwright

    print("browser checks")
    with sync_playwright() as p:
        browser = p.chromium.launch()

        # --- per-preview generic checks -----------------------------------
        for slug in SLUGS:
            page = browser.new_page(viewport={"width": 1280, "height": 900})
            errors = []
            page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.goto((PAGINATION / slug / "preview.html").as_uri())
            page.wait_for_selector("nav[aria-label]", timeout=15000)
            page.wait_for_timeout(400)
            check(not errors, f"{slug}: no console/page errors {errors[:3]}")

            navs = page.locator("nav[aria-label]")
            check(navs.count() >= 1, f"{slug}: nav landmark present")
            first = navs.first
            label = first.get_attribute("aria-label")
            check(bool(label), f"{slug}: nav aria-label ({label})")
            has_page_links = first.locator('[aria-label^="Go to page"], [aria-current="page"]').count() > 0
            current = first.locator('[aria-current="page"]')
            expected = 1 if has_page_links else 0
            check(current.count() == expected, f"{slug}: aria-current count {current.count()} == {expected}")

            # overflow at three widths
            for w in WIDTHS:
                page.set_viewport_size({"width": w, "height": 900})
                page.wait_for_timeout(150)
                overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
                check(overflow <= 0, f"{slug}: no horizontal overflow @ {w} (got {overflow})")
            page.set_viewport_size({"width": 1280, "height": 900})

            # focus-visible ring on the first interactive control
            control = first.locator("a, button").first
            control.focus()
            outline = control.evaluate("e => getComputedStyle(e).outlineStyle")
            check(outline in ("solid", "auto"), f"{slug}: focus-visible outline ({outline})")

            # dark mode flips the background token
            light_bg = page.evaluate("getComputedStyle(document.body).backgroundColor")
            page.click("#ds-theme-toggle")
            page.wait_for_timeout(150)
            dark_bg = page.evaluate("getComputedStyle(document.body).backgroundColor")
            check(light_bg != dark_bg, f"{slug}: dark-mode token flip ({light_bg} -> {dark_bg})")
            page.click("#ds-theme-toggle")
            page.close()

        # --- reference: interaction ----------------------------------------
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto((PAGINATION / "pagination" / "preview.html").as_uri())
        page.wait_for_selector("nav[aria-label]")
        page.wait_for_timeout(400)
        nav = page.locator("nav[aria-label]").first
        # starts on page 1: Previous is a disabled span
        prev = nav.locator("span[aria-disabled]", has_text="Previous")
        check(prev.count() == 1, "reference: Previous disabled on page 1")
        # click page 3 -> aria-current moves, list updates
        nav.get_by_role("button", name="Go to page 3").click()
        page.wait_for_timeout(200)
        current = nav.locator('[aria-current="page"]')
        check(current.count() == 1 and current.inner_text() == "3", "reference: aria-current moves to page 3")
        check("17–24" in page.inner_text("body"), "reference: list status updates (17–24)")
        # accessible names
        check(nav.get_by_role("button", name="Go to page 5").count() == 1, "reference: accessible name 'Go to page 5'")
        check(nav.get_by_role("button", name="Page 3").count() == 1, "reference: accessible name 'Page 3' current")
        # Next steps to 4; at last page Next disables
        nav.get_by_role("button", name="Next").click()
        page.wait_for_timeout(150)
        nav.get_by_role("button", name="Go to page 5").click()
        page.wait_for_timeout(150)
        check(nav.locator("span[aria-disabled]", has_text="Next").count() == 1, "reference: Next disabled on last page")
        # URL-based demo renders anchors and follows the hash
        anchors_nav = page.locator("nav[aria-label]").nth(1)
        check(anchors_nav.locator("a").count() > 0, "reference: URL-based demo renders anchors")
        anchors_nav.locator("a", has_text="4").first.click()
        page.wait_for_timeout(200)
        check("#/components/page/4" in page.url or "page/4" in page.evaluate("location.hash"),
              "reference: anchor navigates the hash")
        current = anchors_nav.locator('[aria-current="page"]')
        check(current.count() == 1 and current.inner_text() == "4", "reference: aria-current follows hash")
        # control height 36px
        h = nav.get_by_role("button", name="Page 5").bounding_box()["height"]
        check(abs(h - 36) < 1, f"reference: md control height 36px (got {h})")
        page.close()

        # --- previous/next variant ------------------------------------------
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto((PAGINATION / "pagination-with-previous-next" / "preview.html").as_uri())
        page.wait_for_selector("nav[aria-label]")
        page.wait_for_timeout(400)
        nav = page.locator("nav[aria-label]").first
        check("Page 1 of 12" in page.inner_text("body"), "prev/next: status shows Page 1 of 12")
        check(nav.locator("span[aria-disabled]", has_text="Previous").count() == 1, "prev/next: Previous disabled at start")
        nav.get_by_role("button", name="Next").click()
        page.wait_for_timeout(200)
        check("Page 2 of 12" in page.inner_text("body"), "prev/next: status advances to Page 2 of 12")
        check("Design tokens" in page.inner_text("body"), "prev/next: chapter content updates")
        check(nav.locator('[aria-live="polite"]', has_text="Page 2 of 12").count() == 1, "prev/next: status is aria-live")
        for _ in range(10):
            nav.get_by_role("button", name="Next").click()
        page.wait_for_timeout(200)
        check(nav.locator("span[aria-disabled]", has_text="Next").count() == 1, "prev/next: Next disabled at end")
        check("Page 12 of 12" in page.inner_text("body"), "prev/next: stops at Page 12 of 12")
        page.close()

        # --- numbers variant -------------------------------------------------
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto((PAGINATION / "pagination-with-numbers" / "preview.html").as_uri())
        page.wait_for_selector("nav[aria-label]")
        page.wait_for_timeout(400)
        nav = page.locator("nav[aria-label]").first
        texts = link_labels(nav)
        check(texts == ["1", "2", "3", "4", "5", "6"], f"numbers: explicit 1-6 ({texts})")
        nav.get_by_role("button", name="Go to page 4").click()
        page.wait_for_timeout(200)
        check(nav.locator('[aria-current="page"]').inner_text() == "4", "numbers: aria-current on page 4")
        check("Gabriel Alvarez" in page.inner_text("body"), "numbers: user list updates")
        page.close()

        # --- ellipsis variant ------------------------------------------------
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto((PAGINATION / "pagination-with-ellipsis" / "preview.html").as_uri())
        page.wait_for_selector("nav[aria-label]")
        page.wait_for_timeout(400)
        nav = page.locator("nav[aria-label]").first

        def visible_pages():
            return [t.split("\n")[0].strip() for t in nav.locator("li").all_inner_texts()]

        check(visible_pages() == ["Previous", "1", "2", "…", "50", "Next"],
              f"ellipsis: page 1 range {visible_pages()}")
        nav.get_by_role("button", name="Go to page 2").click()
        page.wait_for_timeout(150)
        check(visible_pages() == ["Previous", "1", "2", "3", "…", "50", "Next"],
              f"ellipsis: page 2 range {visible_pages()}")
        nav.get_by_role("button", name="Go to page 3").click()
        page.wait_for_timeout(150)
        nav.get_by_role("button", name="Go to page 4").click()
        page.wait_for_timeout(150)
        check(visible_pages() == ["Previous", "1", "…", "3", "4", "5", "…", "50", "Next"],
              f"ellipsis: page 4 range {visible_pages()}")
        nav.get_by_role("button", name="Go to page 50").click()
        page.wait_for_timeout(150)
        check(visible_pages() == ["Previous", "1", "…", "49", "50", "Next"],
              f"ellipsis: last page range {visible_pages()}")
        # ellipsis is informational only
        ell = nav.locator("li > span", has_text="…").first
        check(ell.locator("span[aria-hidden]").count() == 1, "ellipsis: glyph aria-hidden")
        check(ell.locator("span.sr-only").count() == 1, "ellipsis: sr-only text present")
        check(ell.get_attribute("tabindex") is None, "ellipsis: not focusable")
        check(ell.evaluate("e => e.closest('a,button')") is None, "ellipsis: not inside a control")
        # small dataset demo: no ellipsis
        nav2 = page.locator("nav[aria-label]").nth(1)
        items2 = [t.split("\n")[0].strip() for t in nav2.locator("li").all_inner_texts()]
        check(items2 == ["Previous", "1", "2", "3", "4", "Next"], f"ellipsis: small dataset has no ellipsis ({items2})")
        page.close()

        # --- compact / large geometry ---------------------------------------
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto((PAGINATION / "pagination-compact" / "preview.html").as_uri())
        page.wait_for_selector("nav[aria-label]")
        page.wait_for_timeout(400)
        h = page.locator("nav[aria-label]").first.get_by_role("button", name="Go to page 2").bounding_box()["height"]
        check(abs(h - 32) < 1, f"compact: sm control height 32px (got {h})")
        page.locator("nav[aria-label]").first.get_by_role("button", name="Go to page 2").click()
        page.wait_for_timeout(150)
        check("11–20 of 60 orders" in page.inner_text("body"), "compact: orders list updates")
        page.close()

        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto((PAGINATION / "pagination-large" / "preview.html").as_uri())
        page.wait_for_selector("nav[aria-label]")
        page.wait_for_timeout(400)
        h = page.locator("nav[aria-label]").first.get_by_role("button", name="Go to page 2").bounding_box()["height"]
        check(abs(h - 44) < 1, f"large: lg control height 44px (got {h})")
        page.locator("nav[aria-label]").first.get_by_role("button", name="Go to page 3").click()
        page.wait_for_timeout(150)
        check("Stratum — Treasury ops" in page.inner_text("body"), "large: case study updates")
        page.close()

        # --- page-size variant -----------------------------------------------
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto((PAGINATION / "pagination-with-page-size" / "preview.html").as_uri())
        page.wait_for_selector("nav[aria-label]")
        page.wait_for_timeout(400)
        # select is labeled and OUTSIDE the nav landmark
        select = page.get_by_label("Rows per page")
        check(select.count() == 1, "page-size: labeled select present")
        check(select.evaluate("e => e.closest('nav')") is None, "page-size: select outside nav")
        check(page.locator("ul li").count() >= 20, "page-size: 20 rows by default")
        check("Showing 1–20 of 87 customers" in page.inner_text("body"), "page-size: status 1–20")
        select.select_option("50")
        page.wait_for_timeout(250)
        check("Showing 1–50 of 87 customers" in page.inner_text("body"), "page-size: 50 rows after change")
        check(page.locator('[aria-current="page"]').inner_text() == "1", "page-size: resets to page 1")
        nav = page.locator("nav[aria-label]").first
        texts = [t.split("\n")[0].strip() for t in nav.locator("li").all_inner_texts()]
        check(texts == ["Previous", "1", "2", "Next"], f"page-size: 2 pages at size 50 ({texts})")
        select.select_option("10")
        page.wait_for_timeout(250)
        texts = [t.split("\n")[0].strip() for t in nav.locator("li").all_inner_texts()]
        check(texts == ["Previous", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Next"],
              f"page-size: 9 pages at size 10 ({texts})")
        page.close()

        # --- disabled variant -------------------------------------------------
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto((PAGINATION / "pagination-disabled" / "preview.html").as_uri())
        page.wait_for_selector("nav[aria-label]")
        page.wait_for_timeout(400)
        navs = page.locator("nav[aria-label]")
        check(navs.count() == 4, f"disabled: 4 demos (got {navs.count()})")
        first_nav = navs.nth(0)
        check(first_nav.locator("span[aria-disabled]", has_text="Previous").count() == 1,
              "disabled: demo 1 Previous aria-disabled")
        last_nav = navs.nth(1)
        check(last_nav.locator("span[aria-disabled]", has_text="Next").count() == 1,
              "disabled: demo 2 Next aria-disabled")
        third = navs.nth(2)
        d3 = third.locator("span[aria-disabled]", has_text="3")
        check(d3.count() == 1, "disabled: page 3 individually disabled")
        d3.click(force=True)
        page.wait_for_timeout(150)
        check(third.locator('[aria-current="page"]').inner_text() == "2",
              "disabled: disabled page cannot be activated")
        fourth = navs.nth(3)
        check(fourth.locator("a, button").count() == 0, "disabled: fully disabled nav has no interactive controls")
        check(fourth.locator("span[aria-disabled]").count() == 7, "disabled: fully disabled nav all spans")
        check(fourth.locator('[aria-current="page"]').inner_text() == "2",
              "disabled: aria-current preserved while disabled")
        # keyboard: disabled span not reachable via Tab from first nav
        first_nav.get_by_role("button", name="Page 1").focus()
        page.keyboard.press("Tab")
        focused = page.evaluate("document.activeElement.textContent.trim()")
        check(focused == "2", f"disabled: Tab skips disabled Previous (focused '{focused}')")
        page.close()

        # --- reduced motion ---------------------------------------------------
        ctx = browser.new_context(viewport={"width": 1280, "height": 900}, reduced_motion="reduce")
        page = ctx.new_page()
        page.goto((PAGINATION / "pagination" / "preview.html").as_uri())
        page.wait_for_selector("nav[aria-label]")
        page.wait_for_timeout(400)
        transition = page.locator("nav[aria-label] button").first.evaluate(
            "e => getComputedStyle(e).transitionProperty"
        )
        check(transition == "none", f"reduced-motion: transition none (got {transition})")
        ctx.close()

        browser.close()


def main():
    static_checks()
    browser_checks()
    print(f"\n{checks} checks, {len(failures)} failures")
    if failures:
        print("FAILURES:")
        for f in failures:
            print("  - " + f)
        sys.exit(1)
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
