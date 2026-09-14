"""Navbar section builders — 15 concepts."""
from .helpers import TOKENS, ic, ICONS, logo_svg


def section(body, style, scope=None):
    attr = scope or ('data-navbar="%s"' % style)
    b = TOKENS[style]
    return ('<header class="relative w-full %s" %s>\n<div class="mx-auto max-w-7xl px-5 sm:px-6 lg:px-8">\n%s\n</div>\n</header>'
            % (b["text"], attr, body))


def navbar(style, i):
    b = TOKENS[style]
    concepts = [
        ("transparent", "Transparent Navbar"),
        ("sticky", "Sticky Navbar"),
        ("mega-menu", "Mega Menu Navbar"),
        ("docs", "Documentation Navbar"),
        ("dashboard", "Dashboard Navbar"),
        ("glass", "Glass Navbar" if style == "edge-glassmorphism" else "Spotlight Navbar"),
        ("brutalist", "Brutalist Navbar" if style == "neo-brutalism" else "Bold Navbar"),
        ("floating", "Floating Navbar"),
        ("centered", "Centered Navbar"),
        ("vercel", "Vercel-Style Navbar"),
        ("split", "Split Navbar"),
        ("pill", "Pill Navbar"),
        ("minimal", "Minimal Navbar"),
        ("app-bar", "App Bar Navbar"),
        ("announcement", "Navbar with Announcement"),
    ]
    key, title = concepts[i]
    brand = logo_svg("Flowbase")
    links = ["Product", "Pricing", "Docs", "Changelog"]
    navlinks = lambda extra="": "".join(
        '<a href="#" class="text-sm font-medium %s px-3 py-2 rounded-md hover:opacity-100">%s</a>' % (b["text_muted"], l) for l in links) + extra

    def actions():
        return ('<div class="flex items-center gap-2"><a href="#" class="text-sm font-medium %s px-3 py-2">Sign in</a>'
                '<a href="#" class="%s px-4 py-2 text-sm">Start free %s</a></div>') % (b["text_muted"], b["btn_primary"], ic("arrow", "h-4 w-4"))

    def mobile():
        return '<button type="button" class="md:hidden %s p-2" aria-label="Menu">%s</button>' % (b["surface_soft"], ic("menu", "h-5 w-5"))

    if key == "transparent":
        body = ('<nav class="flex h-16 items-center justify-between">%s'
                '<div class="hidden md:flex items-center">%s</div>'
                '<div class="flex items-center gap-2">%s%s</div></nav>') % (brand, navlinks(), actions(), mobile())
        feat = ["transparent navbar", "centered links", "CTA + sign-in", "mobile menu button", "responsive"]

    elif key == "sticky":
        body = ('<nav class="sticky top-0 z-30 flex h-16 items-center justify-between %s px-4 -mx-4">%s'
                '<div class="hidden md:flex items-center">%s</div>%s%s</nav>') % (
            b["surface_soft"], brand, navlinks(), actions(), mobile())
        feat = ["sticky positioning", "surface-backed bar", "z-30 stacking", "CTA actions", "mobile menu"]

    elif key == "mega-menu":
        megapanel = ('<div class="absolute left-1/2 top-full hidden -translate-x-1/2 md:block"><div class="%s p-6 w-[560px] grid grid-cols-3 gap-4">'
                     '%s</div></div>') % (b["surface"], "".join(
                         '<a href="#" class="flex gap-3 p-3 rounded-lg hover:opacity-100"><span class="flex h-9 w-9 items-center justify-center %s">%s</span><span><span class="block text-sm font-semibold">%s</span><span class="block text-xs %s">%s</span></span></a>' % (
                             b["surface_soft"], ic(icn, "h-4 w-4"), t, b["text_muted"], d)
                         for icn, t, d in [("grid", "Features", "Everything included"), ("trend", "Analytics", "Live dashboards"), ("code", "API", "Full developer API"), ("shield", "Security", "SOC 2 compliant"), ("bolt", "Automations", "No-code workflows"), ("users", "Team", "Roles and permissions")]))
        body = ('<nav class="relative flex h-16 items-center justify-between">%s<div class="hidden md:flex items-center">%s</div>%s%s</nav>') % (
            brand, '<div class="relative group">%s%s</div>' % ('<a href="#" class="text-sm font-medium %s px-3 py-2 rounded-md">Product</a>' % b["text_muted"], megapanel) + navlinks()[len('<a href="#" class="text-sm font-medium %s px-3 py-2 rounded-md hover:opacity-100">Product</a>' % b["text_muted"]):],
            actions(), mobile())
        # simpler robust version
        body = ('<nav class="relative flex h-16 items-center justify-between">%s'
                '<div class="hidden md:flex items-center"><div class="relative group">'
                '<button type="button" class="text-sm font-medium %s px-3 py-2 rounded-md flex items-center gap-1">Product %s</button>'
                '<div class="absolute left-0 top-full hidden w-[560px] group-hover:block z-40"><div class="%s p-6 grid grid-cols-3 gap-2 mt-2">%s</div></div>'
                '</div><a href="#" class="text-sm font-medium %s px-3 py-2">Pricing</a><a href="#" class="text-sm font-medium %s px-3 py-2">Docs</a></div>'
                '%s%s</nav>') % (brand, b["text_muted"], ic("chevron", "h-4 w-4"), b["surface"], megapanel.split('class="%s p-6 w-[560px] grid grid-cols-3 gap-4">' % b["surface"])[-1].replace('</div></div>', ''), b["text_muted"], b["text_muted"], actions(), mobile())
        # The above slicing is fragile; rebuild cleanly:
        mm = "".join('<a href="#" class="flex gap-3 p-3 rounded-lg"><span class="flex h-9 w-9 items-center justify-center %s">%s</span><span><span class="block text-sm font-semibold">%s</span><span class="block text-xs %s">%s</span></span></a>' % (
            b["surface_soft"], ic(icn, "h-4 w-4"), t, b["text_muted"], d) for icn, t, d in [("grid", "Features", "Everything included"), ("trend", "Analytics", "Live dashboards"), ("code", "API", "Full developer API"), ("shield", "Security", "SOC 2 compliant"), ("bolt", "Automations", "No-code workflows"), ("users", "Team", "Roles and permissions")])
        body = ('<nav class="relative flex h-16 items-center justify-between">%s'
                '<div class="hidden md:flex items-center"><div class="relative group">'
                '<button type="button" class="text-sm font-medium %s px-3 py-2 rounded-md flex items-center gap-1">Product %s</button>'
                '<div class="absolute left-0 top-full hidden w-[560px] z-40 group-hover:block"><div class="%s p-6 grid grid-cols-3 gap-2 mt-2">%s</div></div>'
                '</div><a href="#" class="text-sm font-medium %s px-3 py-2">Pricing</a><a href="#" class="text-sm font-medium %s px-3 py-2">Docs</a></div>'
                '%s%s</nav>') % (brand, b["text_muted"], ic("chevron", "h-4 w-4"), b["surface"], mm, b["text_muted"], b["text_muted"], actions(), mobile())
        feat = ["hover mega menu", "6-feature panel", "dropdown positioning", "z-40 stacking", "responsive"]

    elif key == "docs":
        body = ('<nav class="flex h-16 items-center gap-4">%s<span class="%s">v3.0</span>'
                '<div class="relative ml-2 hidden flex-1 max-w-md sm:block"><span class="absolute left-3 top-1/2 -translate-y-1/2">%s</span>'
                '<input type="search" placeholder="Search docs..." class="%s pl-10" aria-label="Search docs">'
                '<kbd class="absolute right-3 top-1/2 -translate-y-1/2 %s">⌘K</kbd></div>'
                '<div class="ml-auto flex items-center gap-2">%s%s</div></nav>') % (
            brand, b["badge"], ic("search", "h-4 w-4"), b["input"], b["badge"], actions(), mobile())
        feat = ["docs navbar", "inline search", "cmd-k hint", "version badge", "responsive search"]

    elif key == "dashboard":
        body = ('<nav class="flex h-16 items-center justify-between">'
                '<div class="flex items-center gap-4">%s<button type="button" class="md:hidden %s p-2" aria-label="Toggle sidebar">%s</button>'
                '<span class="%s">Acme Workspace</span></div>'
                '<div class="flex items-center gap-2"><button type="button" class="%s p-2" aria-label="Search">%s</button>'
                '<button type="button" class="%s p-2 relative" aria-label="Notifications">%s<span class="absolute right-1.5 top-1.5 h-2 w-2 rounded-full" style="background:%s"></span></button>'
                '<div class="flex h-8 w-8 items-center justify-center rounded-full text-white text-xs font-semibold" style="background:linear-gradient(135deg,#6366f1,#8b5cf6)">JD</div></div></nav>') % (
            brand, b["surface_soft"], ic("grid", "h-5 w-5"), b["badge"], b["surface_soft"], ic("search", "h-4 w-4"), b["surface_soft"], ic("bell", "h-4 w-4"), b["accent"])
        feat = ["dashboard navbar", "workspace switcher", "search + notifications", "avatar", "sidebar toggle"]

    elif key == "glass":
        body = ('<nav class="flex h-16 items-center justify-between %s px-4 m-2 rounded-2xl">%s'
                '<div class="hidden md:flex items-center">%s</div>%s%s</nav>') % (
            b["surface"], brand, navlinks(), actions(), mobile())
        feat = ["floating glass nav", "rounded pill bar", "inset margin", "centered links", "CTA actions"]

    elif key == "brutalist":
        body = ('<nav class="flex h-16 items-center justify-between %s px-4">%s'
                '<div class="hidden md:flex items-center gap-1">%s</div>%s%s</nav>') % (
            b["surface"], brand,
            "".join('<a href="#" class="f-mono text-sm font-bold uppercase px-3 py-2 border-2 border-transparent hover:border-current">%s</a>' % l for l in links),
            '<a href="#" class="%s px-4 py-2 text-sm">START FREE</a>', mobile())
        feat = ["bold brutalist nav", "uppercase mono links", "hard borders", "edge CTA", "responsive"]

    elif key == "floating":
        body = ('<div class="absolute left-1/2 top-4 z-40 w-[min(960px,92%%)] -translate-x-1/2 %s">'
                '<nav class="flex h-14 items-center justify-between px-4">%s'
                '<div class="hidden md:flex items-center">%s</div>%s%s</nav></div>'
                '<div class="h-16" aria-hidden="true"></div>') % (
            b["surface"], brand, navlinks(), actions(), mobile())
        feat = ["floating capsule nav", "absolute positioning", "z-40 stacking", "centered links", "spacer block"]

    elif key == "centered":
        body = ('<nav class="flex h-20 flex-col items-center justify-center gap-3">'
                '%s<div class="hidden md:flex items-center gap-1">%s</div>%s</nav>') % (
            brand, navlinks(), actions())
        feat = ["centered stacked nav", "logo on top", "links below", "no hamburger", "minimal height"]

    elif key == "vercel":
        body = ('<nav class="flex h-14 items-center justify-between">%s'
                '<div class="hidden md:flex items-center gap-1">%s</div>'
                '<div class="flex items-center gap-2"><span class="hidden sm:inline-flex %s">%s</span>%s</div></nav>') % (
            brand,
            "".join('<a href="#" class="text-sm %s px-3 py-1.5 rounded-md hover:opacity-100">%s</a>' % (b["text_muted"], l) for l in ["Product", "Pricing", "Docs", "Blog"]),
            b["badge"], ic("github", "h-3.5 w-3.5") + " Star", actions())
        feat = ["vercel-style nav", "low height bar", "github star badge", "ghost links", "CTA actions"]

    elif key == "split":
        right = '<div class="flex items-center gap-3"><span class="text-sm %s">New</span><a href="#" class="%s px-4 py-2 text-sm">Start free</a></div>' % (b["text_muted"], b["btn_primary"])
        body = ('<nav class="flex h-16 items-center justify-between">%s'
                '<div class="hidden md:flex items-center gap-4">%s</div>'
                '<div class="flex items-center gap-2">%s</div>'
                '<div class="hidden md:flex items-center">%s</div>%s</nav>') % (
            brand, "".join('<a href="#" class="text-sm font-medium %s">%s</a>' % (b["text_muted"], l) for l in ["Docs", "Community"]),
            '<a href="#" class="%s px-4 py-2 text-sm">Sign in</a>' % b["btn_secondary"], right, mobile())
        feat = ["split navbar", "links both sides", "centered CTA", "sign-in + start", "responsive"]

    elif key == "pill":
        body = ('<nav class="flex h-16 items-center justify-center"><div class="%s flex items-center gap-1 px-2 py-1.5">'
                '%s<div class="hidden sm:flex items-center gap-1 px-2">%s</div>'
                '<div class="ml-auto">%s</div></div>%s</nav>') % (
            b["surface"], brand, navlinks(), actions(), mobile())
        feat = ["pill navbar", "single container", "contained links", "CTA inside", "responsive collapse"]

    elif key == "minimal":
        body = ('<nav class="flex h-14 items-center justify-between">%s'
                '<div class="hidden sm:flex items-center gap-5">%s</div>%s</nav>') % (
            brand, "".join('<a href="#" class="text-sm %s">%s</a>' % (b["text_muted"], l) for l in ["Docs", "Pricing", "Contact"]), actions())
        feat = ["minimal navbar", "low height", "bare links", "no hamburger", "single CTA"]

    elif key == "app-bar":
        body = ('<nav class="flex h-16 items-center justify-between %s px-4">'
                '<div class="flex items-center gap-3">%s<span class="text-sm font-semibold">Dashboard</span></div>'
                '<div class="hidden md:flex items-center gap-1">%s</div>'
                '<div class="flex items-center gap-2"><span class="%s">12 active</span>'
                '<div class="flex h-8 w-8 items-center justify-center rounded-full text-white text-xs font-semibold" style="background:linear-gradient(135deg,#06b6d4,#3b82f6)">JD</div></div></nav>') % (
            b["surface_soft"], brand, navlinks(), b["badge"])
        feat = ["app bar navbar", "context label", "active count badge", "avatar", "responsive nav"]

    else:  # announcement
        ann = ('<div class="flex items-center justify-center gap-2 py-2 text-sm %s"><span class="%s">%s New</span>'
               'Flowbase 3.0 is live — workflow automations are here. <a href="#" class="font-semibold underline">Read more</a></div>') % (
            b["text_muted"], b["badge"], ic("spark", "h-3.5 w-3.5"))
        body = ann + ('<nav class="flex h-16 items-center justify-between">%s<div class="hidden md:flex items-center">%s</div>%s%s</nav>') % (
            brand, navlinks(), actions(), mobile())
        feat = ["announcement + navbar", "top promo bar", "new badge", "dismissable-looking", "responsive nav"]

    code = section(body, style)
    desc = "%s navbar: %s." % (TOKENS[style]["title"].split(" (")[0], feat[0].capitalize())
    return dict(code=code, section_name=title, eyebrow="Navbar", features=feat,
                tags=["navbar", "navigation", "header"] + [style], desc=desc, scope="navbar")
