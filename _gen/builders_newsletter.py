"""Newsletter section builders — 15 concepts."""
from .helpers import TOKENS, ic, ICONS, logo_svg
from .layout import head, section


def newsletter(style, i):
    b = TOKENS[style]
    concepts = [
        ("centered", "Centered Newsletter CTA"),
        ("split", "Split Newsletter"),
        ("glass", "Glass Newsletter CTA" if style == "edge-glassmorphism" else "Floating Newsletter CTA"),
        ("brutalist", "Brutalist Newsletter CTA" if style == "neo-brutalism" else "Bold Newsletter CTA"),
        ("gradient", "Gradient Newsletter CTA"),
        ("bento", "Bento Newsletter CTA"),
        ("minimal", "Minimal Subscribe"),
        ("premium", "Premium Newsletter CTA"),
        ("startup", "Startup Newsletter CTA"),
        ("footer", "Footer Newsletter"),
        ("inline", "Inline Newsletter Strip"),
        ("card", "Card Newsletter CTA"),
        ("stat", "Stat + Newsletter CTA"),
        ("benefits", "Benefits Newsletter CTA"),
        ("compact", "Compact Newsletter CTA"),
    ]
    key, title = concepts[i]

    def form(inline=False):
        if inline:
            return ('<form class="flex flex-col sm:flex-row gap-2 max-w-md mx-auto w-full">'
                    '<label for="nl-email" class="sr-only">Email address</label>'
                    '<input id="nl-email" type="email" placeholder="you@email.com" class="%s flex-1" aria-label="Email">'
                    '<button type="submit" class="%s justify-center">%s Subscribe</button></form>') % (b["input"], b["btn_primary"], ic("send", "h-4 w-4"))
        return ('<form class="flex flex-col gap-2 max-w-md mx-auto w-full">'
                '<label for="nl-email" class="sr-only">Email address</label>'
                '<input id="nl-email" type="email" placeholder="you@email.com" class="%s" aria-label="Email">'
                '<button type="submit" class="%s justify-center">%s Subscribe to the newsletter</button></form>') % (b["input"], b["btn_primary"], ic("send", "h-4 w-4"))

    h = head("Newsletter", "mail", "Stay in the loop", "Monthly product updates and ideas. No spam, unsubscribe anytime.", style)

    if key == "centered":
        body = ('<div class="%s %s p-8 sm:p-12 text-center"><div class="mx-auto mb-5 flex h-14 w-14 items-center justify-center %s">%s</div>'
                '<h3 class="f-disp text-2xl sm:text-3xl font-bold">Join 24,000+ subscribers</h3>'
                '<p class="mt-3 text-sm %s max-w-md mx-auto">Get one email a month with product updates, ideas, and no spam.</p>'
                '<div class="mt-6">%s</div>'
                '<p class="mt-3 text-xs %s">We respect your privacy. Unsubscribe in one click.</p></div>') % (
            b["surface"], b["hover_card"], b["surface_soft"], ic("mail", "h-7 w-7"), b["text_muted"], form(inline=True), b["text_muted"])
        feat = ["centered CTA", "icon header", "subscriber count", "privacy note", "inline form"]

    elif key == "split":
        body = ('<div class="grid grid-cols-1 gap-8 lg:grid-cols-2 items-center">'
                '<div><span class="%s mb-3 inline-flex">%s Newsletter</span><h3 class="f-disp text-2xl sm:text-3xl font-bold">Ideas worth your inbox</h3>'
                '<p class="mt-3 text-sm %s">A monthly letter on building calmer software, written by the team.</p></div>'
                '<div class="%s p-6">%s<p class="mt-3 text-xs %s">24,000+ readers · 4.9/5 rating</p></div></div>') % (
            b["badge"], ic("spark", "h-3.5 w-3.5"), b["text_muted"], b["surface"], form(inline=True), b["text_muted"])
        feat = ["split newsletter", "left intro + right form", "subscriber stats", "badge header", "responsive"]

    elif key == "glass":
        body = ('<div class="%s %s p-8 sm:p-12 text-center relative overflow-hidden">'
                '<div class="absolute inset-0 opacity-30" style="background:radial-gradient(circle at 30%% 20%%,#%s,transparent 50%%)" aria-hidden="true"></div>'
                '<div class="relative z-10"><h3 class="f-disp text-2xl sm:text-3xl font-bold">Never miss an update</h3>'
                '<p class="mt-3 text-sm %s max-w-md mx-auto">The product letter for teams who ship.</p>'
                '<div class="mt-6">%s</div></div></div>') % (
            b["surface"], b["hover_card"], b["accent"].lstrip("#"), b["text_muted"], form(inline=True))
        feat = ["floating glass CTA", "radial glow", "centered headline", "inline form", "responsive"]

    elif key == "brutalist":
        body = ('<div class="%s p-8 sm:p-10 text-center" style="background:linear-gradient(135deg,#%s22,transparent)">'
                '<div class="mb-4 flex justify-center">%s</div>'
                '<h3 class="f-disp text-2xl sm:text-3xl font-bold">SUBSCRIBE</h3>'
                '<p class="mt-3 text-sm %s">One email a month. Pure signal.</p>'
                '<div class="mt-6">%s</div></div>') % (
            b["surface"], b["accent"].lstrip("#"), '<span class="%s flex h-14 w-14 items-center justify-center">%s</span>' % (b["surface_soft"], ic("mail", "h-7 w-7")), b["text_muted"], form(inline=True))
        feat = ["bold newsletter CTA", "accent-tinted panel", "icon header", "inline form", "centered"]

    elif key == "gradient":
        body = ('<div class="relative overflow-hidden rounded-3xl p-8 sm:p-12 text-center text-white" style="background:linear-gradient(120deg,%s,%s)">'
                '<div class="absolute inset-0 opacity-20" style="background:radial-gradient(circle at 80%% 20%%, #fff, transparent 50%%)" aria-hidden="true"></div>'
                '<div class="relative z-10"><h3 class="f-disp text-2xl sm:text-3xl font-bold">Join the inner circle</h3>'
                '<p class="mt-3 text-sm text-white/80 max-w-md mx-auto">Monthly insights from the team. No fluff.</p>'
                '<div class="mt-6"><form class="flex flex-col sm:flex-row gap-2 max-w-md mx-auto w-full">'
                '<label for="nl-email" class="sr-only">Email address</label>'
                '<input id="nl-email" type="email" placeholder="you@email.com" class="flex-1 rounded-full px-4 py-3 bg-white/20 border border-white/30 text-white placeholder:text-white/60 focus:outline-none focus:ring-2 focus:ring-white/50" aria-label="Email">'
                '<button type="submit" class="rounded-full bg-white px-6 py-3 font-bold hover:bg-white/90">%s Subscribe</button></form></div></div></div>') % (
            b["accent"], b.get("accent2") or b["accent"], ic("send", "h-4 w-4"))
        feat = ["gradient CTA", "full-bleed color", "glass input", "white CTA button", "centered"]

    elif key == "bento":
        body = ('<div class="grid grid-cols-1 gap-4 lg:grid-cols-3">'
                '<div class="lg:col-span-2 %s %s p-8"><h3 class="f-disp text-2xl font-bold">The product letter</h3>'
                '<p class="mt-2 text-sm %s">Monthly. Curated. Free.</p><div class="mt-6">%s</div></div>'
                '<div class="%s %s p-6 flex flex-col justify-center"><p class="f-disp text-3xl font-bold">24k+</p><p class="mt-1 text-sm %s">Subscribers</p>'
                '<div class="mt-3 flex -space-x-2">%s</div></div></div>') % (
            b["surface"], b["hover_card"], b["text_muted"], form(inline=True), b["surface"], b["hover_card"], b["text_muted"],
            "".join('<span class="h-8 w-8 rounded-full border-2 border-current/0" style="background:linear-gradient(135deg,%s,%s)"></span>' % (c1, c2) for c1, c2 in [("#6366f1", "#8b5cf6"), ("#06b6d4", "#3b82f6"), ("#ec4899", "#f43f5e")]))
        feat = ["bento newsletter", "form + stat tile", "2/3 + 1/3 split", "subscriber count", "avatar stack"]

    elif key == "minimal":
        body = ('<div class="text-center"><h3 class="f-disp text-2xl font-bold">Subscribe</h3>'
                '<p class="mt-2 text-sm %s">One email a month.</p><div class="mt-5">%s</div></div>') % (b["text_muted"], form(inline=True))
        feat = ["minimal subscribe", "no container", "inline form", "centered", "low chrome"]

    elif key == "premium":
        body = ('<div class="%s p-8 sm:p-12 text-center"><div class="mx-auto mb-5">%s</div>'
                '<span class="%s mb-4 inline-flex">%s Members</span>'
                '<h3 class="f-disp text-2xl sm:text-3xl font-bold">The premium briefing</h3>'
                '<p class="mt-3 text-sm %s max-w-md mx-auto">A monthly deep dive for teams building at the edge.</p>'
                '<div class="mt-6">%s</div></div>') % (
            b["surface"], logo_svg("Flowbase"), b["badge"], ic("sparkle", "h-3.5 w-3.5"), b["text_muted"], form(inline=True))
        feat = ["premium newsletter CTA", "brand header", "members badge", "inline form", "centered"]

    elif key == "startup":
        body = ('<div class="%s %s p-8"><div class="grid grid-cols-1 gap-6 lg:grid-cols-2 items-center">'
                '<div><span class="%s mb-3 inline-flex">%s Launch</span><h3 class="f-disp text-2xl font-bold">Be first to know</h3>'
                '<p class="mt-2 text-sm %s">Product launches and founder notes, monthly.</p></div>'
                '<div>%s</div></div></div>') % (
            b["surface"], b["hover_card"], b["badge"], ic("rocket", "h-3.5 w-3.5"), b["text_muted"], form(inline=False).replace("mx-auto", "sm:mx-0"))
        feat = ["startup newsletter CTA", "split panel", "launch badge", "stacked form", "responsive"]

    elif key == "footer":
        body = ('<div class="grid grid-cols-1 gap-8 lg:grid-cols-[1.2fr_1fr]">'
                '<div><div class="mb-4">%s</div><p class="text-sm %s max-w-xs">The calmest support workspace for fast teams.</p>'
                '<div class="mt-4 flex gap-2">%s</div></div>'
                '<div><h3 class="font-semibold mb-3">Subscribe</h3><p class="text-sm %s mb-4">Monthly updates. No spam.</p>%s</div></div>') % (
            logo_svg("Flowbase"), b["text_muted"], "".join('<a href="#" class="%s flex h-9 w-9 items-center justify-center" aria-label="%s">%s</a>' % (b["surface_soft"], s, ic(s, "h-4 w-4")) for s in ["twitter", "github", "linkedin"]), b["text_muted"], form(inline=False).replace("mx-auto", ""))
        feat = ["footer newsletter", "brand + social", "split layout", "stacked form", "responsive"]

    elif key == "inline":
        body = ('<div class="%s p-5 flex flex-col sm:flex-row items-center justify-between gap-4">'
                '<div><h3 class="font-semibold">Get the newsletter</h3><p class="text-sm %s">Monthly. No spam.</p></div>'
                '<form class="flex gap-2 w-full sm:w-auto"><label for="nl-email" class="sr-only">Email address</label><input id="nl-email" type="email" placeholder="you@email.com" class="%s flex-1 sm:w-64" aria-label="Email">'
                '<button type="submit" class="%s">Subscribe</button></form></div>') % (
            b["surface_soft"], b["text_muted"], b["input"], b["btn_primary"])
        feat = ["inline strip", "horizontal layout", "compact form", "side-by-side", "responsive stack"]

    elif key == "card":
        body = ('<div class="%s %s p-8 sm:p-10 text-center max-w-2xl mx-auto">'
                '<div class="mx-auto mb-5 flex h-14 w-14 items-center justify-center %s">%s</div>'
                '<h3 class="f-disp text-2xl font-bold">The signal, not the noise</h3>'
                '<p class="mt-3 text-sm %s">One thoughtful email a month.</p>'
                '<div class="mt-6">%s</div></div>') % (
            b["surface"], b["hover_card"], b["surface_soft"], ic("mail", "h-7 w-7"), b["text_muted"], form(inline=True))
        feat = ["card newsletter CTA", "narrow max width", "icon header", "inline form", "centered"]

    elif key == "stat":
        body = ('<div class="grid grid-cols-1 gap-6 lg:grid-cols-2 items-center">'
                '<div class="text-center lg:text-left"><p class="f-disp text-5xl font-bold">24k+</p>'
                '<p class="mt-2 text-sm %s">subscribers already reading</p></div>'
                '<div class="%s %s p-6"><h3 class="font-semibold mb-2">Join them</h3>%s</div></div>') % (
            b["text_muted"], b["surface"], b["hover_card"], form(inline=False).replace("mx-auto", "sm:mx-0"))
        feat = ["stat + newsletter", "big number", "split layout", "stacked form", "responsive"]

    elif key == "benefits":
        perks = [("doc", "Monthly essays", "Deep, long-form reads"), ("shield", "No spam", "We never sell your email"), ("x", "One-click exit", "Unsubscribe anytime")]
        body = ('<div class="%s %s p-8 sm:p-10"><div class="grid grid-cols-1 gap-8 lg:grid-cols-2 items-center">'
                '<div><h3 class="f-disp text-2xl font-bold">The product letter</h3>'
                '<p class="mt-2 text-sm %s">Ideas on building calm software.</p>'
                '<div class="mt-6">%s</div></div>'
                '<ul class="space-y-4">%s</ul></div></div>') % (
            b["surface"], b["hover_card"], b["text_muted"], form(inline=False).replace("mx-auto", "sm:mx-0"),
            "".join('<li class="flex items-start gap-3"><span class="flex h-9 w-9 shrink-0 items-center justify-center %s">%s</span><div><p class="text-sm font-semibold">%s</p><p class="text-xs %s">%s</p></div></li>' % (
                b["surface_soft"], ic(icn, "h-4 w-4"), t, b["text_muted"], d) for icn, t, d in perks))
        feat = ["benefits newsletter", "split + perks list", "3 benefit rows", "stacked form", "responsive"]

    else:  # compact
        body = ('<div class="%s %s p-6 flex flex-col sm:flex-row items-center gap-4">'
                '<div class="text-center sm:text-left sm:flex-1"><h3 class="font-semibold">Subscribe</h3>'
                '<p class="text-xs %s">Monthly. Free.</p></div>'
                '<form class="flex gap-2 w-full sm:w-auto"><label for="nl-email" class="sr-only">Email address</label><input id="nl-email" type="email" placeholder="Email" class="%s flex-1 sm:w-48" aria-label="Email">'
                '<button type="submit" class="%s">%s</button></form></div>') % (
            b["surface"], b["hover_card"], b["text_muted"], b["input"], b["btn_primary"], ic("send", "h-4 w-4"))
        feat = ["compact newsletter CTA", "horizontal panel", "inline mini form", "responsive stack", "low height"]

    code = section(h + body, style)
    desc = "%s newsletter layout: %s." % (TOKENS[style]["title"].split(" (")[0], feat[0].capitalize())
    return dict(code=code, section_name=title, eyebrow="Newsletter", features=feat,
                tags=["newsletter", "subscribe", "email", "cta"] + [style], desc=desc, scope="newsletter")
