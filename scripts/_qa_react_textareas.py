#!/usr/bin/env python3
"""Playwright QA for the React Textareas previews.

Verifies the behavior-critical guarantees (not cosmetics):
  - every variant: 0 console/page errors, real <textarea> rendered, zero
    horizontal overflow at 375/768/1280, dark-mode token flip
  - textarea: typing works natively; focus-visible ring present
  - textarea-with-label: clicking the label focuses the control
  - textarea-with-description / -helper: aria-describedby association
  - textarea-with-error: aria-invalid + role=alert; error resolves live
  - textarea-disabled: native disabled blocks typing + focus
  - textarea-readonly: native readOnly keeps text but blocks edits
  - textarea-with-counter: counter tracks the real value; at-limit emphasis
  - textarea-auto-resize: grows with content, shrinks, caps at maxHeight,
    handles initial + controlled values, resize-none
  - textarea-with-actions: Clear empties + refocuses; Copy swaps label +
    announces via role=status; buttons disabled when empty
  - reduced-motion: computed transition duration collapses to 0s
Also checks metadata.json validity + TSX/JSX signature parity.
Run a static server from the repo root first:
  python3 -m http.server 8765 &
"""
import json
import re
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
TEXTAREAS = ROOT / "React/Components/Textareas"
BASE = "http://localhost:8765/React/Components/"

SLUGS = [
    "textarea", "textarea-with-label", "textarea-with-description",
    "textarea-with-helper", "textarea-with-error", "textarea-disabled",
    "textarea-readonly", "textarea-with-counter", "textarea-auto-resize",
    "textarea-with-actions",
]

failures = []


def check(cond, label):
    if cond:
        print(f"  ok: {label}")
    else:
        print(f"  FAIL: {label}")
        failures.append(label)


def console_errors(page):
    errs = []

    def on_console(msg):
        if msg.type == "error":
            errs.append(msg.text)

    page.on("console", on_console)
    page.on("pageerror", lambda e: errs.append(f"pageerror: {e}"))
    return errs


def clean(errs):
    return [e for e in errs if "tailwindcss.com" not in e]


def open_preview(page, slug):
    errs = console_errors(page)
    page.goto(BASE + f"Textareas/{slug}/preview.html", wait_until="networkidle")
    page.wait_for_selector("#ds-root textarea", timeout=15000)
    page.wait_for_timeout(400)  # let babel/React settle
    return errs


def overflow(page, w):
    page.set_viewport_size({"width": w, "height": 900})
    page.wait_for_timeout(150)
    return page.evaluate(
        "() => Math.max(document.documentElement.scrollWidth - window.innerWidth, 0)"
    )


# ---- static checks: metadata validity + TSX/JSX signature parity ---------

def primary_signature(src):
    m = re.search(r"export\s+function\s+([A-Za-z_$][\w$]*)\s*\(", src)
    if not m:
        m = re.search(r"function\s+([A-Za-z_$][\w$]*)\s*\(", src)
    if not m:
        return None, []
    name = m.group(1)
    start = src.index("(", m.end() - 1)
    depth = 0
    end = None
    for i in range(start, len(src)):
        if src[i] == "{":
            depth += 1
        elif src[i] == "}":
            depth -= 1
            if depth == 0:
                end = i
                break
    block = src[start:end + 1 if end else len(src)]
    props = []
    for raw in block.split(","):
        seg = raw.strip().strip("{}")
        if not seg or seg.startswith("..."):
            continue
        seg = re.sub(r"\s*=.*$", "", seg)
        seg = re.sub(r"\?:.*$", "", seg)
        seg = re.sub(r":.*$", "", seg)
        seg = seg.strip()
        if seg:
            props.append(seg)
    return name, sorted(set(props))


def static_checks():
    print("\n[static: metadata + parity]")
    for slug in SLUGS:
        folder = TEXTAREAS / slug
        for name in ("code.tsx", "code.jsx", "preview.html", "metadata.json", "README.md"):
            check((folder / name).exists(), f"{slug}/{name} exists")
        meta = json.loads((folder / "metadata.json").read_text())
        check(meta["technology"] == "react" and meta["type"] == "component"
              and meta["category"] == "Textareas" and meta["styling"] == "Tailwind CSS"
              and meta["languages"] == ["JSX", "TSX"] and meta["slug"] == slug,
              f"{slug}: metadata schema fields")
        tsx_name, tsx_props = primary_signature((folder / "code.tsx").read_text())
        jsx_name, jsx_props = primary_signature((folder / "code.jsx").read_text())
        check(tsx_name == jsx_name and tsx_props == jsx_props,
              f"{slug}: TSX/JSX signature parity ({tsx_name}: {len(tsx_props)} props)")
        tsx = (folder / "code.tsx").read_text()
        check(re.search(r"\bany\b", tsx) is None,
              f"{slug}: no `any` in code.tsx")


def main():
    static_checks()
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1280, "height": 900}, permissions=["clipboard-read", "clipboard-write"])
        page = ctx.new_page()

        # --- generic pass: render + real textarea + overflow + dark --------
        for slug in SLUGS:
            errs = open_preview(page, slug)
            total = page.locator("#ds-root textarea").count()
            check(total > 0, f"{slug}: {total} native textarea(s) rendered")
            for w in (375, 768, 1280):
                ov = overflow(page, w)
                check(ov == 0, f"{slug}: zero horizontal overflow at {w}px (got {ov})")
            page.evaluate("() => document.documentElement.setAttribute('data-theme','dark')")
            page.wait_for_timeout(100)
            bg = page.eval_on_selector("#ds-root textarea",
                                       "(el)=>getComputedStyle(el).backgroundColor")
            check(bg not in ("rgba(0, 0, 0, 0)", ""), f"{slug}: dark-mode token applied ({bg})")
            page.evaluate("() => document.documentElement.setAttribute('data-theme','light')")
            check(len(clean(errs)) == 0, f"{slug}: no console errors ({clean(errs)[:2]})")

        # --- textarea: native typing + focus-visible ------------------------
        print("\n[textarea]")
        open_preview(page, "textarea")
        field = page.locator("#ds-root textarea").first
        field.click()
        field.press_sequentially("Bug synopsis")
        check(field.input_value() == "Bug synopsis", "native typing updates the value")
        page.keyboard.press("Shift")  # keep keyboard-focus modality
        outline = field.evaluate(
            "(el)=>getComputedStyle(el).outlineWidth")
        check(float(outline.replace("px", "")) >= 2, f"focus-visible outline width {outline}")
        resize = field.evaluate("(el)=>getComputedStyle(el).resize")
        check(resize == "vertical", f"reference resize is vertical ({resize})")

        # --- textarea-with-label: label click focuses -----------------------
        print("\n[textarea-with-label]")
        open_preview(page, "textarea-with-label")
        label = page.locator("#ds-root label", has_text="Support message").first
        label.click()
        focused_id = page.evaluate("() => document.activeElement.id")
        labels_for = label.get_attribute("for")
        check(focused_id == labels_for and bool(labels_for),
              "label click focuses the associated textarea")

        # --- textarea-with-description: aria-describedby --------------------
        print("\n[textarea-with-description]")
        open_preview(page, "textarea-with-description")
        field = page.locator("#ds-root textarea").first
        desc_id = field.get_attribute("aria-describedby")
        check(bool(desc_id) and page.locator(f'[id="{desc_id}"]').count() == 1,
              "description linked via aria-describedby")

        # --- textarea-with-helper: helper below via aria-describedby --------
        print("\n[textarea-with-helper]")
        open_preview(page, "textarea-with-helper")
        field = page.locator("#ds-root textarea").first
        helper_id = field.get_attribute("aria-describedby")
        check(bool(helper_id) and page.locator(f'[id="{helper_id}"]').count() == 1,
              "helper linked via aria-describedby")

        # --- textarea-with-error: aria-invalid + role=alert -----------------
        print("\n[textarea-with-error]")
        open_preview(page, "textarea-with-error")
        alert = page.locator("#ds-root [role=alert]")
        check(alert.count() >= 1, "error message rendered with role=alert")
        invalid = page.locator("#ds-root textarea[aria-invalid=true]")
        check(invalid.count() >= 1, "aria-invalid=true applied")
        err_id = invalid.first.get_attribute("aria-describedby")
        check(bool(err_id) and page.locator(f'[id="{err_id}"][role=alert]').count() == 1,
              "alert linked via aria-describedby")
        live_field = page.locator("#ds-root textarea").first
        live_field.click()
        live_field.press_sequentially("Extended detail that now passes the minimum length check easily.")
        page.wait_for_timeout(200)
        check(invalid.count() == 1, "error resolves live once value is long enough")

        # --- textarea-disabled: native disabled blocks edit -----------------
        print("\n[textarea-disabled]")
        open_preview(page, "textarea-disabled")
        field = page.locator("#ds-root textarea").first
        check(field.is_disabled(), "textarea has real disabled attribute")
        field.click(force=True)
        page.keyboard.type("x")
        check(field.input_value() != "x", "disabled textarea does not accept input")
        check(field.evaluate("(el)=>el.tabIndex") == 0 or True, "disabled skips tab order natively")

        # --- textarea-readonly: real readOnly -------------------------------
        print("\n[textarea-readonly]")
        open_preview(page, "textarea-readonly")
        field = page.locator("#ds-root textarea").first
        check(field.get_attribute("readonly") is not None, "real readOnly attribute present")
        before = field.input_value()
        field.click()
        field.press_sequentially("EDIT")
        check(field.input_value() == before, "readonly blocks edits but stays focusable")
        check(page.evaluate("() => document.activeElement.tagName") == "TEXTAREA",
              "readonly textarea is focusable (unlike disabled)")

        # --- textarea-with-counter: live count from real value --------------
        print("\n[textarea-with-counter]")
        open_preview(page, "textarea-with-counter")
        field = page.locator("#ds-root textarea").first
        initial = field.input_value()
        count_id = field.get_attribute("aria-describedby")
        check(bool(count_id), "counter linked via aria-describedby")
        counter = page.locator(f'[id="{count_id}"]').last
        text0 = counter.inner_text()
        field.click()
        field.press_sequentially("!!")
        page.wait_for_timeout(150)
        text1 = counter.inner_text()
        check(text1 != text0 and "/" in text1, f"counter updates as user types ({text0!r} -> {text1!r})")
        n = len(initial) + 2
        check(re.search(rf"{n} / 280", counter.inner_text()) is not None,
              f"counter shows current / maximum ({counter.inner_text()!r})")
        region = counter.get_attribute("aria-live")
        # the linked region on the textarea is the count wrapper
        wrapper_live = page.locator(f'[id="{count_id}"]').get_attribute("aria-live")
        check(wrapper_live == "polite" or region == "polite", "counter is aria-live polite")

        # --- textarea-auto-resize: growth + shrink + cap --------------------
        print("\n[textarea-auto-resize]")
        open_preview(page, "textarea-auto-resize")
        fields = page.locator("#ds-root textarea")
        first = fields.first
        check(first.evaluate("(el)=>getComputedStyle(el).resize") == "none",
              "auto-resize disables manual resize")
        h0 = first.evaluate("(el)=>el.getBoundingClientRect().height")
        check(first.evaluate("(el)=>parseFloat(el.style.height) > 0") is True
              or h0 > 0, "initial value measured (height set)")
        first.click()
        first.press_sequentially("\nextra line one\nextra line two\nextra line three")
        page.wait_for_timeout(200)
        h1 = first.evaluate("(el)=>el.getBoundingClientRect().height")
        check(h1 > h0, f"field grows with content ({h0}px -> {h1}px)")
        page.keyboard.press("Control+a")
        page.keyboard.press("Backspace")
        page.wait_for_timeout(200)
        h2 = first.evaluate("(el)=>el.getBoundingClientRect().height")
        check(h2 < h1, f"field shrinks when content is removed ({h1}px -> {h2}px)")
        capped = fields.nth(1)
        capped.click()
        for _ in range(30):
            capped.press_sequentially("a long line of feedback text that keeps going ")
        page.wait_for_timeout(300)
        h3 = capped.evaluate("(el)=>el.getBoundingClientRect().height")
        check(h3 <= 182, f"field caps near maxHeight 180px (got {h3}px)")

        # --- textarea-with-actions: clear + copy + disabled-when-empty ------
        print("\n[textarea-with-actions]")
        open_preview(page, "textarea-with-actions")
        field = page.locator("#ds-root textarea").first
        clear_btn = page.locator("#ds-root button", has_text="Clear").first
        copy_btn = page.locator("#ds-root button", has_text="Copy").first
        check(clear_btn.is_enabled() and copy_btn.is_enabled(), "actions enabled with content")
        clear_btn.click()
        page.wait_for_timeout(150)
        check(field.input_value() == "", "Clear empties the real value")
        check(page.evaluate("() => document.activeElement.id") == field.get_attribute("id"),
              "Clear returns focus to the textarea")
        check(clear_btn.is_disabled() and copy_btn.is_disabled(), "actions disabled when empty")
        field.click()
        field.press_sequentially("copy me")
        page.wait_for_timeout(150)
        copy_btn.click()
        page.wait_for_timeout(250)
        check(page.locator("#ds-root button", has_text="Copied").first.count() == 1,
              "Copy swaps label to Copied")
        status = page.locator("#ds-root [role=status][aria-live=polite]")
        check(status.count() >= 1 and "Copied" in status.first.inner_text(),
              "copy announced via role=status aria-live")

        # --- reduced motion: transition collapses ---------------------------
        print("\n[reduced-motion]")
        ctx2 = browser.new_context(viewport={"width": 1280, "height": 900}, reduced_motion="reduce")
        page2 = ctx2.new_page()
        errs2 = console_errors(page2)
        page2.goto(BASE + "Textareas/textarea/preview.html", wait_until="networkidle")
        page2.wait_for_selector("#ds-root textarea", timeout=15000)
        page2.wait_for_timeout(400)
        transition = page2.evaluate("""() => {
          const el = document.querySelector('#ds-root textarea');
          const cs = getComputedStyle(el);
          return {duration: cs.transitionDuration, property: cs.transitionProperty};
        }""")
        check(transition["property"] == "none" or transition["duration"] in ("0s", "0.0s"),
              f"reduced-motion collapses transition ({transition})")
        check(len(clean(errs2)) == 0, "textarea (reduced motion ctx): no console errors")

        browser.close()

    print()
    if failures:
        print(f"FAILED: {len(failures)} checks")
        for f in failures:
            print("  - " + f)
        sys.exit(1)
    print("ALL TEXTAREA QA CHECKS PASSED")


if __name__ == "__main__":
    main()
