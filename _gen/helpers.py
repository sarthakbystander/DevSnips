"""Helpers for rendering section HTML using style tokens."""

import html as _html

from .styles import TOKENS, STYLE_NAMES

# re-export ICONS here so builders can `from .helpers import ICONS`


def esc(s):
    return _html.escape(s, quote=False)


def fill(template, *args):
    """Safe token substitution that replaces ~ markers in order.

    Unlike % formatting, this is immune to literal percent signs in content.
    Tokens are written as {0}, {1}, ... in the template string.
    """
    out = template
    for idx, val in enumerate(args):
        out = out.replace("{" + str(idx) + "}", str(val))
    return out


def star_row(count, style, star_color=None):
    """Return 5 SVG stars filled up to `count`."""
    color = star_color if star_color else TOKENS[style]["star_color"]
    out = ['<span class="inline-flex items-center gap-0.5" aria-label="%d out of 5 stars">' % count]
    for i in range(5):
        fill = "currentColor" if i < count else "none"
        op = "" if i < count else " opacity-30"
        out.append(
            '<svg class="h-4 w-4 %s%s" viewBox="0 0 24 24" fill="%s" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>' % (color, op, fill)
        )
    out.append("</span>")
    return "".join(out)


def avatar(name, seed=0, ring=""):
    """SVG initials avatar using deterministic gradient by seed."""
    initials = "".join([w[0] for w in name.split()[:2]]).upper() or "?"
    grads = [
        ("#f97316", "#ef4444"), ("#6366f1", "#8b5cf6"), ("#06b6d4", "#3b82f6"),
        ("#ec4899", "#f43f5e"), ("#10b981", "#22c55e"), ("#f59e0b", "#eab308"),
        ("#8b5cf6", "#6366f1"), ("#14b8a6", "#06b6d4"),
    ]
    c1, c2 = grads[seed % len(grads)]
    return (
        '<span class="inline-flex h-11 w-11 shrink-0 items-center justify-center rounded-full text-white font-semibold text-sm %s" '
        'style="background:linear-gradient(135deg,%s,%s)" aria-hidden="true">%s</span>'
    ) % (ring, c1, c2, initials)


def logo_svg(name, size="h-7", fill="currentColor"):
    """Wordmark-style logo span."""
    return (
        '<span class="inline-flex items-center gap-2 %s" style="color:%s">' % (size, fill)
        + '<svg viewBox="0 0 24 24" fill="none" class="h-full w-auto" aria-hidden="true"><path d="M12 2 2 19h20L12 2z" fill="currentColor"/></svg>'
        + '<span class="font-semibold tracking-tight">%s</span>' % name
        + '</span>'
    )


def icon(path, cls="h-5 w-5"):
    return '<svg class="%s" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">%s</svg>' % (cls, path)


ICONS = {
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "minus": '<path d="M5 12h14"/>',
    "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    "mail": '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "quote": '<path d="M3 21c3 0 7-1 7-8V5c0-1.25-.756-2.017-2-2H4c-1.25 0-2 .75-2 1.972V11c0 1.25.75 2 2 2 1 0 1 0 1 1v1c0 1-1 2-2 2s-1 .008-1 1.031V20c0 1 0 1 1 1z"/>',
    "play": '<polygon points="6 3 20 12 6 21 6 3"/>',
    "video": '<path d="m22 8-6 4 6 4V8Z"/><rect width="14" height="12" x="2" y="6" rx="2"/>',
    "menu": '<path d="M4 12h16M4 6h16M4 18h16"/>',
    "x": '<path d="M18 6 6 18M6 6l12 12"/>',
    "chevron": '<path d="m6 9 6 6 6-6"/>',
    "twitter": '<path d="M22 4s-.7 2.1-2 3.4c1.6 5-3.3 9.8-8.3 8.3-1.3 1.3-3.4 2-3.4 2 1.6-1.1 2.5-2.4 2.8-3.6C7.3 12.6 6 8.5 6 4c1.7 2.4 4 4 7 4 .8-1.3 2.2-2 4-2 2 0 3 1 3 1"/>',
    "github": '<path d="M15 22v-4a3.2 3.2 0 0 0-.9-2.3c3-.3 6.1-1.5 6.1-6.7A5.2 5.2 0 0 0 18.7 5a4.9 4.9 0 0 0-.1-3.6s-1.1-.3-3.6 1.4a12.4 12.4 0 0 0-6.4 0C4.6 1.1 3.5 1.4 3.5 1.4A4.9 4.9 0 0 0 3.4 5 5.2 5.2 0 0 0 2 8.4c0 5.2 3.1 6.4 6 6.7A3.2 3.2 0 0 0 7.2 17V22"/>',
    "linkedin": '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6z"/><rect width="4" height="12" x="2" y="9"/><circle cx="4" cy="4" r="2"/>',
    "instagram": '<rect width="20" height="20" x="2" y="2" rx="5"/><path d="M16 11.4a4 4 0 1 1-8 0 4 4 0 0 1 8 0z"/><circle cx="17.5" cy="6.5" r="1"/>',
    "rocket": '<path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="M12 15 9 12a13.5 13.5 0 0 1 3-9c1.5-1.5 6-1.5 6-1.5s0 4.5-1.5 6a13.5 13.5 0 0 1-9 3z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/>',
    "spark": '<path d="M12 3v3M12 18v3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M3 12h3M18 12h3M5.6 18.4l2.1-2.1M16.3 7.7l2.1-2.1"/>',
    "doc": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/>',
    "help": '<circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><path d="M12 17h.01"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
    "bolt": '<path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>',
    "globe": '<circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15 15 0 0 1 0 20 15 15 0 0 1 0-20z"/>',
    "heart": '<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.6l-1-1a5.5 5.5 0 0 0-7.8 7.8l1 1L12 21l7.8-7.6 1-1a5.5 5.5 0 0 0 0-7.8z"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>',
    "trend": '<path d="M22 7 13.5 15.5 8.5 10.5 2 17"/><path d="M16 7h6v6"/>',
    "calendar": '<rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18M8 2v4M16 2v4"/>',
    "tag": '<path d="M12 2H2v10l9.3 9.3a2.4 2.4 0 0 0 3.4 0l6.6-6.6a2.4 2.4 0 0 0 0-3.4z"/><circle cx="7" cy="7" r="1.5"/>',
    "arrow-down": '<path d="M12 5v14M19 12l-7 7-7-7"/>',
    "external": '<path d="M15 3h6v6M10 14 21 3M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>',
    "send": '<path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/>',
    "home": '<path d="M3 9.5 12 3l9 6.5V21a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/>',
    "grid": '<rect width="7" height="7" x="3" y="3" rx="1"/><rect width="7" height="7" x="14" y="3" rx="1"/><rect width="7" height="7" x="14" y="14" rx="1"/><rect width="7" height="7" x="3" y="14" rx="1"/>',
    "bell": '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 20c0-4 4-6 8-6s8 2 8 6"/>',
    "link": '<path d="M10 13a5 5 0 0 0 7.5.5l3-3a5 5 0 0 0-7-7l-1.5 1.5"/><path d="M14 11a5 5 0 0 0-7.5-.5l-3 3a5 5 0 0 0 7 7l1.5-1.5"/>',
    "code": '<path d="m16 18 6-6-6-6M8 6l-6 6 6 6"/>',
    "terminal": '<path d="m4 17 6-6-6-6"/><path d="M12 19h8"/>',
    "warning": '<path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/><path d="M12 9v4M12 17h.01"/>',
    "ghost": '<path d="M9 10h.01M15 10h.01"/><path d="M12 2a8 8 0 0 0-8 8v12l3-3 3 3 2-2 2 2 3-3 3 3V10a8 8 0 0 0-8-8z"/>',
    "compass": '<circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/>',
    "satellite": '<path d="M13 7 9 3 3 9l4 4M9 3l4 4M5 11l-2 2M21 19l-4-4-4 4 4 4M17 15l4 4"/><circle cx="12" cy="12" r="2"/>',
    "lock": '<rect width="18" height="11" x="3" y="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    "map": '<path d="M3 6l6-3 6 3 6-3v15l-6 3-6-3-6 3z"/><path d="M9 3v15M15 6v15"/>',
    "chat": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
    "headset": '<path d="M3 14v-3a9 9 0 0 1 18 0v3"/><path d="M21 16a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 16a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"/>',
    "building": '<rect width="16" height="20" x="4" y="2" rx="2"/><path d="M9 22v-4h6v4M8 6h.01M16 6h.01M8 10h.01M16 10h.01M8 14h.01M16 14h.01"/>',
    "credit": '<rect width="20" height="14" x="2" y="5" rx="2"/><path d="M2 10h20"/>',
    "shield-check": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
    "sparkle": '<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/>',
}


def ic(name, cls="h-5 w-5"):
    return icon(ICONS.get(name, ICONS["spark"]), cls)
