"""Shared layout helpers for section builders."""
from .helpers import TOKENS, ic


def container(inner, max_w="max-w-7xl"):
    return '<div class="mx-auto %s px-5 sm:px-6 lg:px-8">\n%s\n</div>' % (max_w, inner)


def section(body, style, scope=None, max_w="max-w-7xl", decor=None, py="py-20 sm:py-28"):
    attr = scope or ('data-section="%s"' % style)
    b = TOKENS[style]
    inner = (decor or "") + container(body, max_w)
    return '<section class="relative w-full %s %s" %s>\n%s\n</section>' % (
        py, b["text"], attr, inner)


def head(eyebrow, eyebrow_icon, heading, subhead, style, align="center"):
    b = TOKENS[style]
    icn = (ic(eyebrow_icon, "h-3.5 w-3.5") + " ") if eyebrow_icon else ""
    badge = '<p class="mb-4"><span class="%s">%s%s</span></p>' % (b["badge"], icn, eyebrow) if eyebrow else ""
    align_cls = "text-center mx-auto" if align == "center" else ""
    sub = '<p class="mt-4 max-w-2xl %s text-base sm:text-lg leading-relaxed %s">%s</p>' % (
        align_cls, b["text_muted"], subhead) if subhead else ""
    return '<div class="mb-10 %s">%s<h2 class="f-disp text-3xl sm:text-4xl lg:text-5xl font-bold tracking-tight %s">%s</h2>%s</div>' % (
        align_cls, badge, align_cls, heading, sub)
