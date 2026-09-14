"""Section builders. Each builder returns dict with keys:
   code, eyebrow, heading, subhead, features, tags, desc, scope, section_name.

Every builder produces 15 distinct, copy-paste-ready <section> blocks.
Builders import helpers and pull visual tokens by style so the SAME concept
renders differently across the 15 design languages.
"""

from .helpers import TOKENS, avatar, star_row, icon, ic, ICONS, logo_svg, esc


def C(inner, max_w="max-w-7xl"):
    return '<div class="mx-auto %s px-5 sm:px-6 lg:px-8">\n%s\n</div>' % (max_w, inner)


def section(heading_block, body, style, scope_attr=None, max_w="max-w-7xl", decor=None):
    attr = scope_attr or ('data-section="%s"' % style)
    b = TOKENS[style]
    inner = (decor or "") + C(heading_block + body, max_w)
    return '<section class="relative w-full %s" %s>\n%s\n</section>' % (b["text"], attr, inner)


def head(eyebrow, eyebrow_icon, heading, subhead, style, align="center"):
    b = TOKENS[style]
    icn = (ic(eyebrow_icon, "h-3.5 w-3.5") + " ") if eyebrow_icon else ""
    badge = '<p class="mb-4"><span class="%s">%s%s</span></p>' % (b["badge"], icn, eyebrow) if eyebrow else ""
    align_cls = "text-center mx-auto" if align == "center" else ""
    sub = '<p class="mt-4 max-w-2xl %s text-base sm:text-lg leading-relaxed %s">%s</p>' % (
        align_cls, b["text_muted"], subhead) if subhead else ""
    return '<div class="mb-12 %s">%s<h2 class="f-disp text-3xl sm:text-4xl lg:text-5xl font-bold tracking-tight %s">%s</h2>%s</div>' % (
        align_cls, badge, align_cls, heading, sub)


# =====================================================================
# TESTIMONIALS
# =====================================================================
def testimonials(style, i):
    b = TOKENS[style]
    persons = [
        ("Maya Chen", "Head of Design", "Northbeam"),
        ("Daniel Reyes", "CTO", "Loop Labs"),
        ("Aisha Karim", "Product Lead", "Pulumi"),
        ("Tom Bradley", "Founder", "Myria Co."),
        ("Sofia Rossi", "Eng Lead", "Vela"),
        ("Jordan Fields", "Dev Advocate", "Cal.com"),
        ("Priya Nair", "VP Product", "Resend"),
        ("Ethan Park", "COO", "Flowbase"),
    ]
    quotes = [
        "The fastest onboarding we have ever shipped. Live in two days.",
        "Replaced four separate tools. Our team finally has breathing room.",
        "Reliable, fast, and beautifully designed. An absolute no-brainer.",
        "Our median reply time dropped 70% in the first week alone.",
        "The automation suite paid for itself within a single month.",
        "It genuinely feels built by people who care about the craft.",
        "Onboarding 200 contractors took an afternoon, not a quarter.",
        "Support that treats our customers like we do. Rare and welcome.",
        "Dashboards our execs actually open. The data just makes sense.",
        "We cut churn 18% by acting on insights we finally could see.",
    ]
    P = lambda n: persons[n % len(persons)]
    Q = lambda n: quotes[n % len(quotes)]

    concepts = [
        ("cards", "Card Grid Testimonials"),
        ("masonry", "Masonry Testimonial Wall"),
        ("carousel", "Carousel-Style Testimonials"),
        ("company", "Company Reviews"),
        ("avatars", "User Avatar Wall"),
        ("ratings", "Rating Summary Testimonials"),
        ("video", "Video Testimonial Placeholders"),
        ("split", "Split Testimonial Spotlight"),
        ("quote", "Large Quote Feature"),
        ("wall", "Minimal Testimonial Wall"),
        ("featured", "Featured + Grid Testimonials"),
        ("logos", "Logo + Quote Testimonials"),
        ("metrics", "Metrics + Testimonials"),
        ("stack", "Stacked Quote Testimonials"),
        ("comparison", "Before/After Testimonials"),
    ]
    key, title = concepts[i]
    h = head("Testimonials", "heart", "Loved by teams who move fast", "Real stories from teams who switched to a faster, calmer workflow.", style)

    if key == "cards":
        cards = ""
        for n in range(6):
            pr = P(n)
            cards += '<article class="%s %s p-6"><div class="mb-4">%s</div><blockquote class="text-base leading-relaxed">"%s"</blockquote><figcaption class="mt-6 flex items-center gap-3">%s<div><p class="text-sm font-semibold">%s</p><p class="text-xs %s">%s · %s</p></div></figcaption></article>' % (
                b["surface"], b["hover_card"], star_row(5, style), Q(n), avatar(pr[0], n), pr[0], b["text_muted"], pr[1], pr[2])
        body = '<div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">%s</div>' % cards
        feat = ["3-column responsive grid", "star ratings", "gradient initial avatars", "hover lift", "semantic article/figcaption"]

    elif key == "masonry":
        cols = 3
        col_items = [[] for _ in range(cols)]
        for n in range(9):
            col_items[n % cols].append(n)
        masonry = ""
        for ci in range(cols):
            inner = ""
            for n in col_items[ci]:
                pr = P(n)
                inner += '<article class="%s %s mb-5 break-inside-avoid p-6"><div class="mb-3">%s</div><blockquote class="text-sm leading-relaxed">"%s"</blockquote><div class="mt-5 flex items-center gap-3">%s<div><p class="text-sm font-semibold">%s</p><p class="text-xs %s">%s</p></div></div></article>' % (
                    b["surface"], b["hover_card"], star_row((n % 3) + 3, style), Q(n), avatar(pr[0], n), pr[0], b["text_muted"], pr[2])
            masonry += '<div class="flex-1">%s</div>' % inner
        body = '<div class="flex flex-col gap-5 sm:grid sm:grid-cols-2 lg:grid-cols-3">%s</div>' % masonry
        feat = ["CSS masonry via columns", "9 testimonials", "varying card heights", "break-inside-avoid", "responsive collapse"]

    elif key == "carousel":
        pr = P(0)
        body = (
            '<div class="relative">'
            + ('<div class="%s %s overflow-hidden p-8 sm:p-12">' % (b["surface"], b["hover_card"]))
            + '<div class="flex snap-x snap-mandatory gap-6 overflow-x-auto pb-4 [scrollbar-width:none] [-ms-overflow-style:none] [&::-webkit-scrollbar]:hidden">'
            + "".join(
                '<figure class="snap-center shrink-0 w-[300px] sm:w-[420px] %s p-6"><div class="mb-4">%s</div><blockquote class="text-base leading-relaxed">"%s"</blockquote><figcaption class="mt-6 flex items-center gap-3">%s<div><p class="text-sm font-semibold">%s</p><p class="text-xs %s">%s · %s</p></div></figcaption></figure>' % (
                    b["surface_soft"], star_row((n % 2) + 4, style), Q(n), avatar(P(n)[0], n), P(n)[0], b["text_muted"], P(n)[1], P(n)[2])
                for n in range(6)
            ) +
            '</div></div>'
            '<div class="mt-4 flex items-center justify-center gap-2" role="tablist" aria-label="Testimonial pagination">'
            + "".join('<span class="h-2 rounded-full %s %s" style="width:%spx"></span>' % (
                "opacity-100" if n == 0 else "opacity-40",
                "bg-current" if style != "soft-ui" else "neu-sm", 24 if n == 0 else 8) for n in range(6))
            + '</div></div>'
        )
        feat = ["horizontal snap carousel (no JS)", "hidden scrollbar", "pagination dots", "responsive card widths", "keyboard scrollable"]

    elif key == "company":
        cards = ""
        for n in range(4):
            pr = P(n)
            cards += '<article class="%s %s p-7"><div class="flex items-center justify-between"><div class="flex items-center gap-3">%s<div><p class="font-semibold">%s</p><p class="text-xs %s">%s</p></div></div><span class="%s">%s Verified</span></div><div class="mt-4">%s</div><blockquote class="mt-3 text-sm leading-relaxed">"%s"</blockquote></article>' % (
                b["surface"], b["hover_card"], avatar(pr[2], n), pr[2], b["text_muted"], pr[1], b["badge"], ic("shield-check", "h-3.5 w-3.5"), star_row(5, style), Q(n))
        body = '<div class="grid grid-cols-1 gap-5 sm:grid-cols-2">%s</div>' % cards
        feat = ["company-branded cards", "verified badges", "company + reviewer", "2-column grid", "rating summary"]

    elif key == "avatars":
        grid = "".join(
            '<figure class="group flex flex-col items-center text-center"><div class="rounded-full">%s</div><figcaption class="mt-3 text-sm font-medium">%s</figcaption><p class="text-xs %s">%s</p></figure>' % (
                avatar(P(n)[0], n, "ring-2 ring-offset-2 " + ("ring-white/20" if style not in ("soft-ui",) else "")), P(n)[0], b["text_muted"], P(n)[1])
            for n in range(12))
        pr = P(7)
        body = ('<div class="%s %s p-8 mb-8"><blockquote class="f-disp text-xl sm:text-2xl font-medium leading-snug">"%s"</blockquote><div class="mt-5 flex items-center gap-3">%s<div><p class="text-sm font-semibold">%s</p><p class="text-xs %s">%s</p></div></div></div>'
                '<div class="grid grid-cols-3 gap-5 sm:grid-cols-4 lg:grid-cols-6">%s</div>'
                '<p class="mt-8 text-center text-sm %s">Join <span class="font-semibold">12,000+</span> happy teams</p>') % (
            b["surface"], b["hover_card"], Q(9), avatar(pr[0], 7), pr[0], b["text_muted"], pr[1], grid, b["text_muted"])
        feat = ["avatar wall", "featured quote banner", "12 profile tiles", "responsive 3/4/6-col", "community count"]

    elif key == "ratings":
        pr = P(0)
        body = (
            '<div class="grid grid-cols-1 gap-8 lg:grid-cols-[1fr_1.2fr]">'
            + ('<div class="%s p-8"><div class="flex items-end gap-3"><span class="f-disp text-5xl font-bold">4.9</span><span class="text-sm %s pb-1">/ 5.0</span></div><div class="mt-3">%s</div><p class="mt-3 text-sm %s">Based on 2,847 verified reviews</p>' % (
                b["surface"], b["text_muted"], star_row(5, style), b["text_muted"]))
            + '<div class="mt-6 space-y-2">' + "".join(
                '<div class="flex items-center gap-2"><span class="w-4 text-xs %s">%d</span><div class="h-2 flex-1 rounded-full %s overflow-hidden"><div class="h-full rounded-full" style="width:%s%%"></div></div><span class="w-10 text-right text-xs %s">%d</span></div>' % (
                    b["text_muted"], star, b["surface_soft"] if style != "soft-ui" else "neu-in", pct, b["text_muted"], count)
                for star, pct, count in [(5, 86, 2450), (4, 10, 284), (3, 3, 85), (2, 1, 28)]
            ) + '</div></div>'
            '<div class="space-y-4">' + "".join(
                '<figure class="%s %s p-6"><blockquote class="text-sm leading-relaxed">"%s"</blockquote><figcaption class="mt-4 flex items-center gap-3">%s<div><p class="text-sm font-semibold">%s</p><p class="text-xs %s">%s</p></div></figcaption></figure>' % (
                    b["surface"], b["hover_card"], Q(n), avatar(P(n)[0], n), P(n)[0], b["text_muted"], P(n)[1])
                for n in range(4)) + '</div></div>'
        )
        feat = ["aggregate rating summary", "distribution bars", "4.9/5 headline", "review count", "side-by-side quotes"]

    elif key == "video":
        tiles = ""
        for n in range(3):
            pr = P(n)
            tiles += '<article class="%s %s p-0 overflow-hidden"><div class="relative aspect-[4/3] flex items-center justify-center" style="background:linear-gradient(135deg,#%s22,#%s11)"><button type="button" class="flex h-16 w-16 items-center justify-center rounded-full %s" aria-label="Play %s testimonial">%s</button><span class="absolute bottom-3 left-3 %s">2:14</span></div><div class="p-5"><div class="flex items-center gap-3">%s<div><p class="text-sm font-semibold">%s</p><p class="text-xs %s">%s · %s</p></div></div></div></article>' % (
                b["surface"], b["hover_card"], b["accent"].lstrip("#"), b["accent2"].lstrip("#") if b.get("accent2") else b["accent"].lstrip("#"), b["btn_primary"], pr[0], ic("play", "h-7 w-7"), b["badge"], avatar(pr[0], n), pr[0], b["text_muted"], pr[1], pr[2])
        body = '<div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">%s</div>' % tiles
        feat = ["video placeholder tiles", "play button overlay", "duration badge", "gradient poster", "captioned profiles"]

    elif key == "split":
        pr = P(3)
        body = (
            '<div class="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">'
            + ('<div class="%s p-8 sm:p-12"><div class="mb-5">%s</div><blockquote class="f-disp text-2xl sm:text-3xl font-medium leading-snug">"%s"</blockquote><div class="mt-8 flex items-center gap-4">%s<div><p class="font-semibold">%s</p><p class="text-sm %s">%s, %s</p></div></div></div>' % (
                b["surface"], star_row(5, style), Q(3), avatar(pr[0], 3), pr[0], b["text_muted"], pr[1], pr[2]))
            + '<div class="grid grid-cols-2 gap-4">' + "".join(
                '<figure class="%s %s p-5"><div class="mb-3">%s</div><blockquote class="text-sm leading-relaxed">"%s"</blockquote><figcaption class="mt-4 text-xs %s">%s</figcaption></figure>' % (
                    b["surface_soft"], b["hover_card"], star_row(5, style), Q(n + 1), b["text_muted"], P(n + 1)[0])
                for n in range(4)) + '</div></div>'
        )
        feat = ["split spotlight layout", "large feature quote", "2x2 supporting grid", "asymmetric balance", "rating stars"]

    elif key == "quote":
        pr = P(4)
        body = (
            '<figure class="%s %s p-10 sm:p-16 text-center">'
            '<div class="mx-auto mb-6 h-12 w-12 %s flex items-center justify-center">%s</div>'
            '<blockquote class="f-disp text-2xl sm:text-4xl lg:text-5xl font-medium leading-tight">"%s"</blockquote>'
            '<figcaption class="mt-8 flex items-center justify-center gap-4">%s<div class="text-left"><p class="font-semibold">%s</p><p class="text-sm %s">%s, %s</p></div></figcaption>'
            '<div class="mt-6 flex items-center justify-center gap-2">%s</div></figure>'
        ) % (b["surface"], b["hover_card"], b["surface_soft"], ic("quote", "h-7 w-7"), Q(5), avatar(pr[0], 4), pr[0], b["text_muted"], pr[1], pr[2], star_row(5, style))
        feat = ["oversized pull quote", "centered composition", "decorative quote glyph", "avatar + role", "5-star rating"]

    elif key == "wall":
        wall = "".join(
            '<figure class="%s %s p-5"><blockquote class="text-sm leading-relaxed">"%s"</blockquote><figcaption class="mt-3 text-xs %s">— %s</figcaption></figure>' % (
                b["surface_soft"], b["hover_card"], Q(n), b["text_muted"], P(n)[0])
            for n in range(12))
        body = '<div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">%s</div>' % wall
        feat = ["dense minimal wall", "12 short quotes", "4-column grid", "low-chrome cards", "author attribution"]

    elif key == "featured":
        pr = P(2)
        sub = "".join(
            '<figure class="%s %s p-6"><div class="mb-3">%s</div><blockquote class="text-sm leading-relaxed">"%s"</blockquote><figcaption class="mt-4 text-xs %s">%s</figcaption></figure>' % (
                b["surface"], b["hover_card"], star_row(5, style), Q(n + 3), b["text_muted"], P(n + 3)[0])
            for n in range(4))
        body = (
            '<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">'
            '<figure class="lg:col-span-2 %s %s p-8 sm:p-10"><div class="mb-4">%s</div><blockquote class="f-disp text-xl sm:text-2xl font-medium leading-snug">"%s"</blockquote><figcaption class="mt-6 flex items-center gap-3">%s<div><p class="font-semibold">%s</p><p class="text-sm %s">%s, %s</p></div></figcaption></figure>'
            '%s</div>'
        ) % (b["surface"], b["hover_card"], star_row(5, style), Q(2), avatar(pr[0], 2), pr[0], b["text_muted"], pr[1], pr[2], sub)
        feat = ["featured wide card", "2/3 + 1/3 split", "secondary quotes grid", "visual hierarchy", "responsive stack"]

    elif key == "logos":
        pr = P(5)
        sub = "".join(
            '<figure class="%s %s p-5"><div class="mb-2">%s</div><p class="text-xs %s">%s says</p><blockquote class="mt-1 text-sm leading-relaxed">"%s"</blockquote></figure>' % (
                b["surface_soft"], b["hover_card"], star_row(5, style), b["text_muted"], P(n)[2], Q(n))
            for n in range(4))
        body = (
            '<div class="grid grid-cols-1 gap-8 lg:grid-cols-[1.1fr_1fr] items-center">'
            '<div><blockquote class="f-disp text-2xl sm:text-3xl font-medium leading-snug">"%s"</blockquote>'
            '<div class="mt-6 flex items-center gap-3">%s<div><p class="font-semibold">%s</p><p class="text-sm %s">%s, %s</p></div></div></div>'
            '<div class="grid grid-cols-2 gap-4">%s</div></div>'
        ) % (Q(6), avatar(pr[0], 5), pr[0], b["text_muted"], pr[1], pr[2], sub)
        feat = ["logo-tagged quotes", "split spotlight", "company attribution", "star ratings", "responsive 2-col"]

    elif key == "metrics":
        pr = P(6)
        sub = "".join(
            '<div class="%s p-5"><p class="f-disp text-2xl font-bold">%s</p><p class="mt-1 text-xs %s">%s</p></div>' % (
                b["surface"], val, b["text_muted"], label)
            for val, label in [("4.9/5", "Average rating"), ("2.8k", "Reviews"), ("98%", "Would recommend"), ("12k+", "Teams")])
        body = (
            '<div class="grid grid-cols-1 gap-6 lg:grid-cols-3">'
            '<figure class="lg:col-span-2 %s %s p-8"><blockquote class="f-disp text-xl sm:text-2xl font-medium leading-snug">"%s"</blockquote>'
            '<figcaption class="mt-6 flex items-center gap-3">%s<div><p class="font-semibold">%s</p><p class="text-sm %s">%s, %s</p></div></figcaption></figure>'
            '<div class="grid grid-cols-2 gap-4">%s</div></div>'
        ) % (b["surface"], b["hover_card"], Q(7), avatar(pr[0], 6), pr[0], b["text_muted"], pr[1], pr[2], sub)
        feat = ["quote + metric tiles", "quantified proof", "2/3 + 1/3 grid", "KPI cards", "responsive stack"]

    elif key == "stack":
        items = "".join(
            '<figure class="%s %s p-6 flex items-start gap-4">%s<div><blockquote class="text-sm leading-relaxed">"%s"</blockquote><figcaption class="mt-3 text-xs %s">%s · %s</figcaption></div></figure>' % (
                b["surface"], b["hover_card"], avatar(P(n)[0], n), Q(n), b["text_muted"], P(n)[0], P(n)[2])
            for n in range(5))
        body = '<div class="space-y-4 max-w-3xl mx-auto">%s</div>' % items
        feat = ["stacked single-column", "horizontal avatar-quote", "5 testimonials", "narrow max width", "sequential reading"]

    else:  # comparison
        pr = P(1)
        body = (
            '<div class="grid grid-cols-1 gap-6 lg:grid-cols-2">'
            '<div class="%s p-8"><span class="%s mb-4 inline-flex">%s Before</span><blockquote class="text-base leading-relaxed %s">"%s"</blockquote><p class="mt-4 text-sm %s">%s, %s</p></div>'
            '<div class="%s p-8" style="%s"><span class="%s mb-4 inline-flex">%s After</span><blockquote class="text-base leading-relaxed">"%s"</blockquote><p class="mt-4 text-sm %s">%s, %s</p></div></div>'
        ) % (
            b["surface_soft"], b["badge"], ic("warning", "h-3.5 w-3.5"), b["text_muted"],
            "We were drowning in disconnected tools and slow replies.",
            b["text_muted"], pr[0], pr[2],
            b["surface"], ("background:linear-gradient(135deg,#%s15,transparent)" % b["accent"].lstrip("#")) if b["accent"].startswith("#") else "",
            b["badge"], ic("check", "h-3.5 w-3.5"),
            "Now everything lives in one fast, calm workspace.",
            b["text_muted"], pr[0], pr[2])
        feat = ["before/after comparison", "two-panel layout", "state badges", "accent-tinted after card", "narrative arc"]

    code = section(h, body, style)
    desc = "%s testimonials layout: %s." % (TOKENS[style]["title"].split(" (")[0], feat[0].capitalize())
    return dict(
        code=code, section_name=title, eyebrow="Testimonials", features=feat,
        tags=["testimonials", "social-proof", "ratings"] + [style],
        desc=desc, scope="testimonials",
    )
