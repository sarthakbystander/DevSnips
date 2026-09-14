"""Footer section builders — 15 concepts."""
from .helpers import TOKENS, ic, ICONS, logo_svg


def section(body, style, scope=None):
    attr = scope or ('data-footer="%s"' % style)
    b = TOKENS[style]
    return ('<footer class="relative w-full %s" %s>\n<div class="mx-auto max-w-7xl px-5 sm:px-6 lg:px-8 py-14 sm:py-20">\n%s\n</div>\n</footer>'
            % (b["text"], attr, body))


def footer(style, i):
    b = TOKENS[style]
    concepts = [
        ("mega", "Mega Footer"),
        ("newsletter", "Newsletter Footer"),
        ("saas", "SaaS Footer"),
        ("docs", "Documentation Footer"),
        ("startup", "Startup Footer"),
        ("editorial", "Editorial Footer"),
        ("dark-premium", "Dark Premium Footer" if style == "dark-premium" else "Branded Footer"),
        ("minimal", "Minimal Footer"),
        ("multi-col", "Multi-Column Footer"),
        ("social", "Social-First Footer"),
        ("compact", "Compact Footer"),
        ("cta", "CTA Footer"),
        ("centered", "Centered Footer"),
        ("grid", "Grid Footer"),
        ("columns-4", "Four-Column Footer"),
    ]
    key, title = concepts[i]

    def linkcol(title, links):
        items = "".join('<li><a href="#" class="text-sm %s hover:opacity-100">%s</a></li>' % (b["text_muted"], l) for l in links)
        return '<div><h3 class="text-sm font-semibold">%s</h3><ul class="mt-4 space-y-2.5">%s</ul></div>' % (title, items)

    def social():
        return '<div class="flex gap-2">' + "".join(
            '<a href="#" class="%s flex h-9 w-9 items-center justify-center" aria-label="%s">%s</a>' % (b["surface_soft"], s, ic(s, "h-4 w-4"))
            for s in ["twitter", "github", "linkedin", "instagram"]) + '</div>'

    if key == "mega":
        top = ('<div class="grid grid-cols-2 gap-8 sm:grid-cols-3 lg:grid-cols-6">'
               '<div class="col-span-2">%s<p class="mt-4 text-sm %s max-w-xs">Build, ship, and scale support that feels like a product surface, not a cost center.</p>%s</div>'
               '%s</div>') % (logo_svg("Flowbase"), b["text_muted"], social(), "".join(
                   linkcol(t, ls) for t, ls in [("Product", ["Features", "Pricing", "Changelog", "Integrations"]), ("Company", ["About", "Careers", "Blog", "Customers"]), ("Resources", ["Docs", "API", "Community", "Status"]), ("Legal", ["Privacy", "Terms", "Security", "DPA"])]))
        bottom = '<div class="mt-12 flex flex-col items-center justify-between gap-4 border-t border-current/10 pt-8 sm:flex-row"><p class="text-sm %s">© 2026 Flowbase Inc. All rights reserved.</p><div class="flex items-center gap-4 text-sm %s"><a href="#" class="hover:opacity-100">Privacy</a><a href="#" class="hover:opacity-100">Terms</a><span class="flex items-center gap-1.5">%s All systems operational</span></div></div>' % (b["text_muted"], b["text_muted"], '<span class="h-2 w-2 rounded-full" style="background:%s"></span>' % b["accent"])
        body = top + bottom
        feat = ["mega multi-column", "brand + blurb", "social icons", "legal + status row", "6-col grid"]

    elif key == "newsletter":
        nl = ('<div class="%s p-8"><div class="grid grid-cols-1 gap-6 lg:grid-cols-[1.2fr_1fr] items-center">'
              '<div><h3 class="f-disp text-2xl font-bold">Ship less, deliver more.</h3><p class="mt-2 text-sm %s">Monthly product insights. No spam.</p></div>'
              '<form class="flex gap-2"><input type="email" placeholder="you@email.com" class="%s flex-1" aria-label="Email">'
              '<button type="submit" class="%s">Subscribe</button></form></div></div>') % (
            b["surface"], b["text_muted"], b["input"], b["btn_primary"])
        cols = '<div class="mt-12 grid grid-cols-2 gap-8 sm:grid-cols-4">%s</div>' % "".join(
            linkcol(t, ls) for t, ls in [("Product", ["Features", "Pricing"]), ("Company", ["About", "Careers"]), ("Resources", ["Docs", "Blog"]), ("Legal", ["Privacy", "Terms"])])
        body = nl + cols + '<div class="mt-10 border-t border-current/10 pt-6 flex items-center justify-between"><p class="text-sm %s">© 2026 Flowbase</p>%s</div>' % (b["text_muted"], social())
        feat = ["newsletter banner", "4-col links", "subscribe form", "social row", "responsive split"]

    elif key == "saas":
        body = ('<div class="grid grid-cols-1 gap-8 lg:grid-cols-[1.5fr_1fr_1fr_1fr]">'
                '<div>%s<p class="mt-4 text-sm %s max-w-xs">The all-in-one support workspace for fast-moving teams.</p>'
                '<div class="mt-4 flex flex-wrap gap-2">%s</div></div>%s</div>'
                '<div class="mt-10 border-t border-current/10 pt-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">'
                '<p class="text-sm %s">© 2026 Flowbase Inc.</p>'
                '<p class="text-xs %s">SOC 2 Type II · GDPR · ISO 27001</p></div>') % (
            logo_svg("Flowbase"), b["text_muted"], "".join('<span class="%s">%s</span>' % (b["badge"], x) for x in ["SOC 2", "GDPR", "HIPAA"]),
            "".join(linkcol(t, ls) for t, ls in [("Product", ["Features", "Pricing", "Changelog"]), ("Company", ["About", "Careers", "Blog"]), ("Support", ["Docs", "Status", "Contact"])]),
            b["text_muted"], b["text_muted"])
        feat = ["SaaS footer", "compliance badges", "3 link columns", "brand + blurb", "responsive 4-col"]

    elif key == "docs":
        body = ('<div class="grid grid-cols-1 gap-8 lg:grid-cols-[1.4fr_1fr_1fr_1fr]">'
                '<div>%s<p class="mt-4 text-sm %s">Everything you need to build with Flowbase.</p>'
                '<div class="mt-4 flex items-center gap-2"><span class="%s">%s v3.0</span><span class="%s">Latest</span></div></div>%s</div>'
                '<div class="mt-10 border-t border-current/10 pt-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">'
                '<p class="text-sm %s">© 2026 Flowbase · Docs</p>'
                '<div class="flex gap-4 text-sm %s"><a href="#" class="hover:opacity-100">Edit this page</a><a href="#" class="hover:opacity-100">Report issue</a></div></div>') % (
            logo_svg("Flowbase Docs"), b["text_muted"], b["badge"], ic("doc", "h-3.5 w-3.5"), b["badge"],
            "".join(linkcol(t, ls) for t, ls in [("Guides", ["Quickstart", "Installation", "Config", "Deploy"]), ["Reference", ["API", "SDKs", "Webhooks", "Events"]], ["Community", ["Forum", "Discord", "Examples"]]]),
            b["text_muted"], b["text_muted"])
        feat = ["documentation footer", "version badge", "edit/report links", "3 link columns", "responsive split"]

    elif key == "startup":
        body = ('<div class="grid grid-cols-1 gap-8 lg:grid-cols-[1.4fr_1fr_1fr]">'
                '<div>%s<p class="mt-4 text-sm %s max-w-xs">We are building the calmest way to run support. Join us.</p>'
                '<div class="mt-5 flex gap-2"><a href="#" class="%s">Get started</a><a href="#" class="%s">Talk to us</a></div></div>%s</div>'
                '<div class="mt-10 border-t border-current/10 pt-6 flex items-center justify-between">'
                '<p class="text-sm %s">© 2026 Flowbase</p>%s</div>') % (
            logo_svg("Flowbase"), b["text_muted"], b["btn_primary"], b["btn_secondary"],
            "".join(linkcol(t, ls) for t, ls in [("Product", ["Features", "Pricing"]), ("Company", ["About", "Careers"])]),
            b["text_muted"], social())
        feat = ["startup footer", "dual CTAs", "2 link columns", "social row", "brand + blurb"]

    elif key == "editorial":
        body = ('<div class="grid grid-cols-1 gap-10 lg:grid-cols-[1.5fr_1fr]">'
                '<div><div class="mb-6">%s</div><p class="f-disp text-xl leading-relaxed max-w-lg">Stories and ideas on building products that respect your time.</p>'
                '<div class="mt-6 flex gap-2">%s</div></div>'
                '<div class="grid grid-cols-2 gap-8">%s</div></div>'
                '<div class="mt-10 border-t border-current/10 pt-6 flex items-center justify-between"><p class="text-sm %s">© 2026 Flowbase Journal</p><p class="text-xs %s">Made with care</p></div>') % (
            logo_svg("Flowbase"), social(), "".join(linkcol(t, ls) for t, ls in [("Read", ["Essays", "Interviews"]), ("Topics", ["Design", "Engineering"])]), b["text_muted"], b["text_muted"])
        feat = ["editorial footer", "serif tagline", "2x2 link grid", "social row", "responsive split"]

    elif key == "dark-premium":
        body = ('<div class="text-center mb-10">%s<p class="mt-4 f-disp text-sm %s tracking-[0.3em] uppercase">Crafted for teams who care</p></div>'
                '<div class="grid grid-cols-2 gap-8 sm:grid-cols-4">%s</div>'
                '<div class="mt-10 border-t border-current/10 pt-6 flex flex-col items-center gap-4 sm:flex-row sm:justify-between">'
                '<p class="text-sm %s">© 2026 Flowbase</p>%s</div>') % (
            logo_svg("Flowbase"), b["text_muted"], "".join(linkcol(t, ls) for t, ls in [("Product", ["Features", "Pricing"]), ("Company", ["About", "Careers"]), ["Resources", ["Docs", "Blog"]], ["Legal", ["Privacy", "Terms"]]]),
            b["text_muted"], social())
        feat = ["premium centered footer", "uppercase tagline", "4-col links", "social row", "responsive grid"]

    elif key == "minimal":
        body = ('<div class="flex flex-col items-center justify-between gap-6 sm:flex-row">'
                '<div class="flex items-center gap-3">%s<p class="text-sm %s">© 2026 Flowbase</p></div>'
                '<nav class="flex gap-6 text-sm %s">%s</nav></div>') % (
            logo_svg("Flowbase"), b["text_muted"], b["text_muted"],
            "".join('<a href="#" class="hover:opacity-100">%s</a>' % l for l in ["Privacy", "Terms", "Status", "Contact"]))
        feat = ["minimal footer", "single row", "inline links", "copyright", "responsive stack"]

    elif key == "multi-col":
        body = ('<div class="grid grid-cols-2 gap-8 sm:grid-cols-3 lg:grid-cols-5">%s</div>'
                '<div class="mt-10 border-t border-current/10 pt-6 flex items-center justify-between">'
                '<p class="text-sm %s">© 2026 Flowbase</p>%s</div>') % (
            "".join(linkcol(t, ls) for t, ls in [("Product", ["Features", "Pricing", "Integrations"]), ("Solutions", ["Startups", "Enterprise", "Agencies"]), ("Company", ["About", "Careers", "Blog"]), ("Resources", ["Docs", "API", "Status"]), ("Legal", ["Privacy", "Terms", "DPA"])]),
            b["text_muted"], social())
        feat = ["5-column footer", "15 links", "brand-free", "social row", "responsive collapse"]

    elif key == "social":
        body = (                '<div class="text-center">%s<p class="mt-5 f-disp text-2xl font-bold">Stay connected</p>'
                '<p class="mt-2 text-sm %s">Follow along as we build in public.</p>'
                '<div class="mt-6 flex justify-center gap-3">%s</div></div>'
                '<div class="mt-10 border-t border-current/10 pt-6 text-center"><p class="text-sm %s">© 2026 Flowbase</p></div>') % (
            logo_svg("Flowbase"), b["text_muted"], "".join(
                '<a href="#" class="%s flex h-11 w-11 items-center justify-center" aria-label="%s">%s</a>' % (b["surface"], s, ic(s, "h-5 w-5")) for s in ["twitter", "github", "linkedin", "instagram", "youtube"]), b["text_muted"])
        feat = ["social-first footer", "5 social links", "centered composition", "large icon targets", "follow CTA"]

    elif key == "compact":
        body = ('<div class="flex flex-col items-center justify-between gap-4 sm:flex-row"><div class="flex items-center gap-6">%s<nav class="flex gap-5 text-sm %s">%s</nav></div>'
                '<div class="flex items-center gap-4">%s<p class="text-sm %s">© 2026</p></div></div>') % (
            logo_svg("Flowbase"), b["text_muted"], "".join('<a href="#" class="hover:opacity-100">%s</a>' % l for l in ["Docs", "Pricing", "Blog", "Contact"]),
            social(), b["text_muted"])
        feat = ["compact footer", "single-line layout", "inline nav", "social + copyright", "responsive"]

    elif key == "cta":
        cta = ('<div class="%s p-8 mb-10 text-center"><h3 class="f-disp text-2xl font-bold">Start building today</h3>'
               '<p class="mt-2 text-sm %s">14-day free trial. No credit card required.</p>'
               '<div class="mt-5 flex justify-center gap-3"><a href="#" class="%s">Start free</a><a href="#" class="%s">Book a demo</a></div></div>') % (
            b["surface"], b["text_muted"], b["btn_primary"], b["btn_secondary"])
        body = cta + '<div class="flex flex-col items-center justify-between gap-4 sm:flex-row"><p class="text-sm %s">© 2026 Flowbase</p>%s</div>' % (b["text_muted"], social())
        feat = ["CTA banner footer", "dual buttons", "social row", "copyright", "responsive"]

    elif key == "centered":
        body = ('<div class="text-center">%s<p class="mt-4 text-sm %s max-w-sm mx-auto">A calmer way to run support, built for teams who ship.</p>'
                '<nav class="mt-6 flex flex-wrap justify-center gap-x-6 gap-y-2 text-sm %s">%s</nav>'
                '<div class="mt-6 flex justify-center">%s</div></div>'
                '<div class="mt-10 border-t border-current/10 pt-6 text-center"><p class="text-sm %s">© 2026 Flowbase Inc.</p></div>') % (
            logo_svg("Flowbase"), b["text_muted"], b["text_muted"],
            "".join('<a href="#" class="hover:opacity-100">%s</a>' % l for l in ["Features", "Pricing", "Docs", "Blog", "Careers", "Contact"]),
            social(), b["text_muted"])
        feat = ["centered footer", "inline nav", "blurb", "social row", "copyright"]

    elif key == "grid":
        body = ('<div class="grid grid-cols-2 gap-8 sm:grid-cols-4">%s</div>'
                '<div class="mt-10 grid grid-cols-1 gap-4 border-t border-current/10 pt-6 sm:grid-cols-3">'
                '<p class="text-sm %s">© 2026 Flowbase Inc.</p>'
                '<p class="text-sm %s">548 Market St, San Francisco</p>'
                '<div class="flex gap-3 sm:justify-end">%s</div></div>') % (
            "".join(linkcol(t, ls) for t, ls in [("Product", ["Features", "Pricing"]), ("Company", ["About", "Careers"]), ["Resources", ["Docs", "Blog"]], ["Legal", ["Privacy", "Terms"]]]),
            b["text_muted"], b["text_muted"], social())
        feat = ["grid footer", "4-col links", "3-col meta row", "address", "social end-aligned"]

    else:  # columns-4
        body = ('<div class="grid grid-cols-2 gap-8 lg:grid-cols-4">%s</div>'
                '<div class="mt-10 border-t border-current/10 pt-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">'
                '<div class="flex items-center gap-3">%s<p class="text-sm %s">© 2026 Flowbase</p></div>'
                '<div class="flex gap-4 text-sm %s">%s</div></div>') % (
            "".join(linkcol(t, ls) for t, ls in [("Product", ["Features", "Pricing", "Integrations", "Changelog"]), ("Company", ["About", "Careers", "Blog", "Customers"]), ("Resources", ["Docs", "API", "Community", "Status"]), ("Legal", ["Privacy", "Terms", "Security", "DPA"])]),
            logo_svg("Flowbase"), b["text_muted"], b["text_muted"], "".join('<a href="#" class="hover:opacity-100">%s</a>' % l for l in ["Privacy", "Terms", "Cookies"]))
        feat = ["4-column footer", "16 links", "brand + copyright", "legal inline", "responsive collapse"]

    code = section(body, style)
    desc = "%s footer: %s." % (TOKENS[style]["title"].split(" (")[0], feat[0].capitalize())
    return dict(code=code, section_name=title, eyebrow="Footer", features=feat,
                tags=["footer", "navigation", "site-footer"] + [style], desc=desc, scope="footer")
