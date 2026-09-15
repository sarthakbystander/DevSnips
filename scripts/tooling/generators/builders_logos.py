"""Logos section builders — 15 concepts."""
from .helpers import TOKENS, ic, ICONS, logo_svg
from .layout import head, section

BRANDS = ["Vercel", "Linear", "Stripe", "Resend", "Raycast", "Notion", "Framer", "Cal.com", "Clerk", "Supabase", "Clerk", "PostHog"]


def _mark(name, n, style):
    """SVG wordmark-style logo span sized for a grid cell."""
    shapes = [
        '<path d="M12 2 2 19h20L12 2z"/>',
        '<rect x="3" y="3" width="18" height="18" rx="4"/>',
        '<circle cx="12" cy="12" r="9"/>',
        '<path d="M4 4h16v16H4z"/>',
        '<path d="M12 2v20M2 12h20"/>',
        '<polygon points="12,2 22,12 12,22 2,12"/>',
    ]
    return '<span class="inline-flex items-center gap-2" aria-label="%s"><svg viewBox="0 0 24 24" class="h-6 w-6" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true">%s</svg><span class="font-semibold tracking-tight text-base">%s</span></span>' % (name, shapes[n % len(shapes)], name)


def logos(style, i):
    b = TOKENS[style]
    concepts = [
        ("infinite", "Infinite-Scroll Logos"),
        ("brand-wall", "Brand Wall"),
        ("grid", "Grid Logos"),
        ("partners", "Partner Showcase"),
        ("investors", "Investors"),
        ("trusted-by", "Trusted By"),
        ("bento", "Bento Logos"),
        ("monochrome", "Minimal Monochrome Logos"),
        ("premium", "Premium Logos"),
        ("startup", "Startup Logos"),
        ("strip", "Logo Strip"),
        ("categorized", "Categorized Logos"),
        ("stat", "Stat + Logos"),
        ("gradient", "Gradient Logo Cloud"),
        ("marquee", "Marquee Logos"),
    ]
    key, title = concepts[i]
    h = head("Logos", "globe", "Trusted by the best", "Teams at category-defining companies build on our platform.", style, align="center")

    def grid_marks(count, cell_cls=None, op=""):
        cell = cell_cls or (b["surface"] + " " + b["hover_card"] + " p-6 flex items-center justify-center")
        marks = "".join(
            '<div class="%s"><span class="%s" style="opacity:1">%s</span></div>' % (cell, op, _mark(BRANDS[n % len(BRANDS)], n, style))
            for n in range(count))
        return marks

    if key == "infinite":
        row = "".join('<div class="shrink-0 px-8 flex items-center"><span class="opacity-70 hover:opacity-100 transition-opacity">%s</span></div>' % _mark(BRANDS[n % len(BRANDS)], n, style) for n in range(12))
        body = ('<div class="relative overflow-hidden" aria-label="Customer logos">'
                '<div class="pointer-events-none absolute inset-y-0 left-0 w-24 z-10" style="background:linear-gradient(to right,%s,transparent)"></div>'
                '<div class="pointer-events-none absolute inset-y-0 right-0 w-24 z-10" style="background:linear-gradient(to left,%s,transparent)"></div>'
                '<div class="flex w-max" style="animation:logo-scroll 30s linear infinite">%s%s</div></div>'
                '<style>@keyframes logo-scroll{0%%{transform:translateX(0)}100%%{transform:translateX(-50%%)}}</style>') % (
            b.get("body_class", "").split()[0] if b.get("body_class") else "transparent", b.get("body_class", "").split()[0] if b.get("body_class") else "transparent", row, row)
        # Use a simpler robust fade with currentColor-aware masks
        body = ('<div class="relative overflow-hidden" aria-label="Customer logos">'
                '<div class="pointer-events-none absolute inset-y-0 left-0 z-10 w-16 sm:w-32" style="background:linear-gradient(to right,var(--logo-fade,transparent),transparent)"></div>'
                '<div class="pointer-events-none absolute inset-y-0 right-0 z-10 w-16 sm:w-32" style="background:linear-gradient(to left,var(--logo-fade,transparent),transparent)"></div>'
                '<div class="flex w-max gap-12 px-6" style="animation:logoScroll 30s linear infinite">%s</div>'
                '<style>@keyframes logoScroll{0%%{transform:translateX(0)}100%%{transform:translateX(-50%%)}}</style></div>') % (row + row)
        feat = ["infinite-scroll marquee", "duplicated track", "edge fades", "hover opacity", "pure CSS animation"]

    elif key == "brand-wall":
        body = ('<div class="%s %s p-8 sm:p-12"><div class="grid grid-cols-2 gap-6 sm:grid-cols-3 lg:grid-cols-6">%s</div></div>') % (
            b["surface"], b["hover_card"], "".join(
                '<div class="flex items-center justify-center"><span class="opacity-80 hover:opacity-100">%s</span></div>' % _mark(BRANDS[n % len(BRANDS)], n, style)
                for n in range(12)))
        feat = ["brand wall", "12 logos", "boxed container", "hover opacity", "responsive 2/3/6-col"]

    elif key == "grid":
        body = '<div class="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">%s</div>' % "".join(
            '<div class="%s %s p-6 flex items-center justify-center"><span class="opacity-75 hover:opacity-100">%s</span></div>' % (
                b["surface"], b["hover_card"], _mark(BRANDS[n % len(BRANDS)], n, style)) for n in range(8))
        feat = ["logo grid", "8 cells", "card-style tiles", "hover lift", "responsive 2/3/4-col"]

    elif key == "partners":
        body = ('<div class="grid grid-cols-1 gap-6 lg:grid-cols-[1fr_1.2fr] items-center">'
                '<div><span class="%s mb-3 inline-flex">%s Partners</span><h3 class="f-disp text-2xl font-bold">Build with the best</h3>'
                '<p class="mt-2 text-sm %s">Certified partners who deliver and extend our platform.</p>'
                '<a href="#" class="mt-4 inline-flex items-center gap-2 %s">%s Become a partner</a></div>'
                '<div class="grid grid-cols-2 gap-4">%s</div></div>') % (
            b["badge"], ic("users", "h-3.5 w-3.5"), b["text_muted"], b["btn_secondary"], ic("arrow", "h-4 w-4"),
            "".join('<div class="%s %s p-5 flex items-center justify-center"><span class="opacity-80 hover:opacity-100">%s</span></div>' % (
                b["surface"], b["hover_card"], _mark(BRANDS[n % len(BRANDS)], n, style)) for n in range(6)))
        feat = ["partner showcase", "split + grid", "partner CTA", "6 logos", "responsive"]

    elif key == "investors":
        body = ('<div class="text-center mb-8"><span class="%s mb-3 inline-flex">%s Backed by</span></div>'
                '<div class="grid grid-cols-2 gap-6 sm:grid-cols-3 lg:grid-cols-5">%s</div>') % (
            b["badge"], ic("credit", "h-3.5 w-3.5"), "".join(
                '<div class="flex items-center justify-center"><span class="opacity-80 hover:opacity-100">%s</span></div>' % _mark(BRANDS[n % len(BRANDS)], n, style)
                for n in range(10)))
        feat = ["investors grid", "10 logos", "backed-by badge", "centered tiles", "responsive 2/3/5-col"]

    elif key == "trusted-by":
        body = ('<div class="text-center"><p class="text-sm %s uppercase tracking-wider mb-6">Trusted by 12,000+ teams</p>'
                '<div class="flex flex-wrap items-center justify-center gap-x-8 gap-y-5">%s</div></div>') % (
            b["text_muted"], "".join('<span class="opacity-70 hover:opacity-100">%s</span>' % _mark(BRANDS[n % len(BRANDS)], n, style) for n in range(6)))
        feat = ["trusted-by row", "wrap-friendly", "inline logos", "headline count", "low chrome"]

    elif key == "bento":
        body = ('<div class="%s %s p-6"><div class="grid grid-cols-2 gap-4 sm:grid-cols-4">%s</div></div>') % (
            b["surface"], b["hover_card"], "".join(
                '<div class="flex items-center justify-center p-4"><span class="opacity-80 hover:opacity-100">%s</span></div>' % _mark(BRANDS[n % len(BRANDS)], n, style)
                for n in range(8)))
        feat = ["bento logo cloud", "boxed container", "8 logos", "4-col grid", "responsive 2/4-col"]

    elif key == "monochrome":
        body = ('<div class="flex flex-wrap items-center justify-center gap-x-10 gap-y-6">%s</div>') % "".join(
            '<span class="opacity-50 hover:opacity-100 transition-opacity">%s</span>' % _mark(BRANDS[n % len(BRANDS)], n, style) for n in range(8))
        feat = ["minimal monochrome logos", "no cards", "opacity hover", "inline wrap", "8 logos"]

    elif key == "premium":
        body = ('<div class="%s p-8 sm:p-10 text-center"><div class="mx-auto mb-5">%s</div>'
                '<p class="text-sm %s uppercase tracking-[0.25em]">As used by industry leaders</p>'
                '<div class="mt-6 flex flex-wrap items-center justify-center gap-x-8 gap-y-4">%s</div></div>') % (
            b["surface"], logo_svg("Flowbase"), b["text_muted"], "".join(
                '<span class="opacity-80 hover:opacity-100">%s</span>' % _mark(BRANDS[n % len(BRANDS)], n, style) for n in range(6)))
        feat = ["premium logo panel", "brand header", "uppercase tagline", "6 logos", "centered"]

    elif key == "startup":
        body = ('<div class="text-center mb-6"><h3 class="f-disp text-xl font-bold">Powering the next generation</h3></div>'
                '<div class="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-6">%s</div>') % "".join(
            '<div class="%s %s p-4 flex items-center justify-center"><span class="opacity-80 hover:opacity-100 scale-90">%s</span></div>' % (
                b["surface_soft"], b["hover_card"], _mark(BRANDS[n % len(BRANDS)], n, style)) for n in range(12))
        feat = ["startup logos", "12 tiles", "soft cards", "section header", "responsive 2/3/6-col"]

    elif key == "strip":
        body = '<div class="%s p-6 flex flex-wrap items-center justify-center gap-x-8 gap-y-4">%s</div>' % (
            b["surface_soft"], "".join('<span class="opacity-70 hover:opacity-100">%s</span>' % _mark(BRANDS[n % len(BRANDS)], n, style) for n in range(8)))
        feat = ["logo strip", "single container", "inline logos", "opacity hover", "wrap-friendly"]

    elif key == "categorized":
        cats = [("Tech", ["Vercel", "Linear", "Stripe", "Resend"]), ("Media", ["Notion", "Framer", "Cal.com"]), ("Dev tools", ["Raycast", "Supabase", "PostHog"])]
        body = '<div class="space-y-8">%s</div>' % "".join(
            '<div><p class="text-xs %s uppercase tracking-wider mb-4">%s</p><div class="flex flex-wrap items-center gap-x-8 gap-y-4">%s</div></div>' % (
                b["text_muted"], c, "".join('<span class="opacity-75 hover:opacity-100">%s</span>' % _mark(name, n, style) for n, name in enumerate(logos)))
            for c, logos in cats)
        feat = ["categorized logos", "grouped by sector", "3 groups", "inline wrap", "uppercase labels"]

    elif key == "stat":
        body = ('<div class="grid grid-cols-1 gap-8 lg:grid-cols-[1fr_1.4fr] items-center">'
                '<div class="text-center"><p class="f-disp text-5xl font-bold">12k+</p><p class="mt-2 text-sm %s">Teams building with us</p></div>'
                '<div class="grid grid-cols-2 gap-4 sm:grid-cols-3">%s</div></div>') % (
            b["text_muted"], "".join('<div class="%s %s p-4 flex items-center justify-center"><span class="opacity-80 hover:opacity-100">%s</span></div>' % (
                b["surface_soft"], b["hover_card"], _mark(BRANDS[n % len(BRANDS)], n, style)) for n in range(6)))
        feat = ["stat + logos", "headline count", "split layout", "6 tiles", "responsive"]

    elif key == "gradient":
        body = ('<div class="relative %s p-8 sm:p-12 overflow-hidden" style="background:linear-gradient(120deg,#%s22,#%s22,transparent)">'
                '<div class="relative z-10 flex flex-wrap items-center justify-center gap-x-8 gap-y-5">%s</div></div>') % (
            b["surface"], b["accent"].lstrip("#"), (b.get("accent2") or b["accent"]).lstrip("#"), "".join(
                '<span class="opacity-90 hover:opacity-100">%s</span>' % _mark(BRANDS[n % len(BRANDS)], n, style) for n in range(8)))
        feat = ["gradient logo cloud", "tinted backdrop", "8 logos", "inline wrap", "hover opacity"]

    else:  # marquee
        row = "".join('<div class="shrink-0 px-8"><span class="opacity-75 hover:opacity-100">%s</span></div>' % _mark(BRANDS[n % len(BRANDS)], n, style) for n in range(10))
        body = ('<div class="relative overflow-hidden [mask-image:linear-gradient(to right,transparent,black 15%%,black 85%%,transparent)]">'
                '<div class="flex w-max" style="animation:marqueeScroll 25s linear infinite">%s</div>'
                '<style>@keyframes marqueeScroll{0%%{transform:translateX(0)}100%%{transform:translateX(-50%%)}}</style></div>') % (row + row)
        feat = ["marquee logos", "CSS mask fades", "duplicated track", "hover opacity", "pure CSS"]

    code = section(h + body, style)
    desc = "%s logos layout: %s." % (TOKENS[style]["title"].split(" (")[0], feat[0].capitalize())
    return dict(code=code, section_name=title, eyebrow="Logos", features=feat,
                tags=["logos", "brand-cloud", "social-proof", "customers"] + [style], desc=desc, scope="logos")
