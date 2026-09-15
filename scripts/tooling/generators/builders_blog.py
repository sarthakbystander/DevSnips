"""Blog section builders — 15 concepts."""
from .helpers import TOKENS, avatar, ic, ICONS
from .layout import head, section

POSTS = [
    ("How we cut our reply time to under 2 minutes", "Engineering", "Maya Chen", "8 min read", "2026-07-28"),
    ("Designing a support workspace that feels calm", "Design", "Sofia Rossi", "6 min read", "2026-07-21"),
    ("The hidden cost of context switching", "Product", "Aisha Karim", "5 min read", "2026-07-14"),
    ("Scaling support without scaling headcount", "Operations", "Ethan Park", "9 min read", "2026-07-07"),
    ("Why we rewrote our queue in Rust", "Engineering", "Daniel Reyes", "11 min read", "2026-06-30"),
    ("Onboarding 200 contractors in an afternoon", "Customer Stories", "Dana Fischer", "7 min read", "2026-06-23"),
    ("The art of the empty state", "Design", "Sofia Rossi", "4 min read", "2026-06-16"),
    ("Pricing for trust, not for lock-in", "Business", "Tom Bradley", "6 min read", "2026-06-09"),
    ("What we learned shipping daily for a year", "Culture", "Ravi Mehta", "8 min read", "2026-06-02"),
    ("A field guide to async support", "Product", "Aisha Karim", "5 min read", "2026-05-26"),
    ("Building a changelog people actually read", "Engineering", "Jordan Fields", "6 min read", "2026-05-19"),
    ("Our journey to SOC 2 Type II", "Security", "Marcus Webb", "10 min read", "2026-05-12"),
]


def blog(style, i):
    b = TOKENS[style]
    concepts = [
        ("featured", "Featured Article"),
        ("magazine", "Magazine Layout"),
        ("bento", "Bento Articles"),
        ("editorial", "Editorial Grid"),
        ("startup", "Startup Blog"),
        ("dark", "Dark Blog" if style in ("dark-premium", "vercel") else "Modern Blog"),
        ("cards", "Card Layout"),
        ("sidebar", "Sidebar Blog"),
        ("news", "News Layout"),
        ("minimal", "Minimal Articles"),
        ("list", "Article List"),
        ("grid-3", "Three-Column Grid"),
        ("split-feature", "Split Featured Blog"),
        ("category", "Category Blog"),
        ("recent", "Recent Posts"),
    ]
    key, title = concepts[i]
    h = head("Blog", "doc", "Ideas worth your time", "Essays on building support that respects everyone's time.", style)

    def meta(author, read, date, n):
        return ('<div class="mt-5 flex items-center gap-3">%s<div class="text-xs"><p class="font-medium">%s</p>'
                '<p class="%s">%s · %s</p></div></div>') % (avatar(author, n, "h-9 w-9"), author, b["text_muted"], date, read)

    def cover(n, cls="aspect-[16/9]"):
        c1, c2 = [("#6366f1", "#8b5cf6"), ("#06b6d4", "#3b82f6"), ("#ec4899", "#f43f5e"), ("#f59e0b", "#eab308"), ("#10b981", "#22c55e"), ("#8b5cf6", "#6366f1")][n % 6]
        cat = POSTS[n % len(POSTS)][1]
        return ('<div class="%s relative overflow-hidden" style="background:linear-gradient(135deg,%s,%s)">'
                '<div class="absolute inset-0 opacity-20" style="background-image:radial-gradient(circle at 30%% 20%%, #fff 0, transparent 40%%)"></div>'
                '<span class="absolute bottom-3 left-3 %s">%s</span></div>') % (cls, c1, c2, b["badge"], cat)

    if key == "featured":
        p = POSTS[0]
        body = ('<article class="%s %s overflow-hidden"><div class="grid grid-cols-1 lg:grid-cols-2">'
                '%s<div class="p-8 sm:p-10"><span class="%s mb-4 inline-flex">%s</span>'
                '<h3 class="f-disp text-2xl sm:text-3xl font-bold leading-tight">%s</h3>'
                '<p class="mt-3 text-sm %s leading-relaxed">A deep dive into the architecture and trade-offs behind our sub-2-minute median reply time.</p>'
                '%s<a href="#" class="mt-6 inline-flex items-center gap-2 %s">%s Read article</a></div></div></article>') % (
            b["surface"], b["hover_card"], cover(0), b["badge"], p[1], p[0], b["text_muted"], meta(p[2], p[3], p[4], 0), b["btn_secondary"], ic("arrow", "h-4 w-4"))
        feat = ["featured article hero", "2-col split", "gradient cover", "read CTA", "author meta"]

    elif key == "magazine":
        lead = POSTS[0]
        body = ('<div class="grid grid-cols-1 gap-6 lg:grid-cols-3">'
                '<article class="lg:col-span-2 lg:row-span-2 %s %s overflow-hidden">%s<div class="p-7"><span class="%s mb-3 inline-flex">%s</span>'
                '<h3 class="f-disp text-2xl font-bold leading-tight">%s</h3>%s</div></article>'
                '%s</div>') % (
            b["surface"], b["hover_card"], cover(0, "aspect-[16/10]"), b["badge"], lead[1], lead[0], meta(lead[2], lead[3], lead[4], 0),
            "".join('<article class="%s %s overflow-hidden">%s<div class="p-5"><span class="%s mb-2 inline-flex">%s</span>'
                    '<h3 class="font-semibold leading-snug">%s</h3>%s</div></article>' % (
                        b["surface"], b["hover_card"], cover(n + 1, "aspect-[16/9]"), b["badge"], p[1], p[0], meta(p[2], p[3], p[4], n + 1))
                    for n, p in enumerate(POSTS[1:5])))
        feat = ["magazine layout", "large lead + 4 side", "3-col grid", "gradient covers", "author meta"]

    elif key == "bento":
        body = '<div class="grid grid-cols-2 gap-4 lg:grid-cols-4">%s</div>' % (
            '<article class="col-span-2 lg:row-span-2 %s %s overflow-hidden">%s<div class="p-6"><span class="%s mb-2 inline-flex">%s</span><h3 class="f-disp text-xl font-bold leading-tight">%s</h3>%s</div></article>' % (
                b["surface"], b["hover_card"], cover(0, "h-full min-h-[280px]"), b["badge"], POSTS[0][1], POSTS[0][0], meta(POSTS[0][2], POSTS[0][3], POSTS[0][4], 0)) +
            "".join('<article class="%s %s overflow-hidden">%s<div class="p-4"><span class="%s mb-2 inline-flex">%s</span><h3 class="font-semibold text-sm leading-snug">%s</h3></div></article>' % (
                b["surface"], b["hover_card"], cover(n + 1, "aspect-[16/9]"), b["badge"], p[1], p[0]) for n, p in enumerate(POSTS[1:7])))
        feat = ["bento articles", "1 large + 6 small", "2/4-col grid", "gradient covers", "responsive"]

    elif key == "editorial":
        body = ('<div class="grid grid-cols-1 gap-8 lg:grid-cols-2">'
                '%s<div class="space-y-6">%s</div></div>') % (
            '<article class="%s p-8"><span class="%s mb-3 inline-flex">%s Lead</span>'
            '<h3 class="f-disp text-3xl font-bold leading-tight">%s</h3>'
            '<p class="mt-4 text-base %s leading-relaxed">An in-depth essay on the philosophy and practice behind our product decisions.</p>%s</article>' % (
                b["surface"], b["badge"], ic("spark", "h-3.5 w-3.5"), POSTS[0][0], b["text_muted"], meta(POSTS[0][2], POSTS[0][3], POSTS[0][4], 0)),
            "".join('<article class="%s %s p-5"><div class="flex items-center gap-2 mb-2"><span class="%s">%s</span><span class="text-xs %s">%s</span></div>'
                    '<h3 class="font-semibold leading-snug">%s</h3></article>' % (b["surface_soft"], b["hover_card"], b["badge"], p[1], b["text_muted"], p[3], p[0])
                    for n, p in enumerate(POSTS[1:5])))
        feat = ["editorial grid", "lead essay + list", "serif headline", "category tags", "responsive split"]

    elif key == "startup":
        cards = "".join(
            '<article class="%s %s overflow-hidden">%s<div class="p-6"><span class="%s mb-2 inline-flex">%s</span>'
            '<h3 class="font-semibold leading-snug">%s</h3>%s<a href="#" class="mt-4 inline-flex items-center gap-1 text-sm font-medium">%s %s</a></div></article>' % (
                b["surface"], b["hover_card"], cover(n, "aspect-[16/9]"), b["badge"], p[1], p[0], meta(p[2], p[3], p[4], n), ic("arrow", "h-4 w-4"), "Read")
            for n, p in enumerate(POSTS[:3]))
        body = '<div class="grid grid-cols-1 gap-6 lg:grid-cols-3">%s</div>' % cards
        feat = ["startup blog grid", "3 posts", "read links", "category tags", "responsive 1/3-col"]

    elif key == "dark":
        body = ('<article class="%s %s overflow-hidden mb-6"><div class="grid grid-cols-1 lg:grid-cols-[1.3fr_1fr]">'
                '%s<div class="p-8"><span class="%s mb-3 inline-flex">%s Featured</span>'
                '<h3 class="f-disp text-2xl font-bold leading-tight">%s</h3>'
                '<p class="mt-3 text-sm %s">The story of how a small team shipped something used by thousands.</p>%s</div></div></article>'
                '<div class="grid grid-cols-1 gap-5 sm:grid-cols-3">%s</div>') % (
            b["surface"], b["hover_card"], cover(0), b["badge"], ic("star", "h-3.5 w-3.5") if "star" in ICONS else ic("spark", "h-3.5 w-3.5"), POSTS[0][0], b["text_muted"], meta(POSTS[0][2], POSTS[0][3], POSTS[0][4], 0),
            "".join('<article class="%s %s overflow-hidden">%s<div class="p-5"><h3 class="font-semibold text-sm leading-snug">%s</h3>%s</div></article>' % (
                b["surface"], b["hover_card"], cover(n + 1, "aspect-[16/9]"), p[0], meta(p[2], p[3], p[4], n + 1)) for n, p in enumerate(POSTS[1:4])))
        feat = ["modern blog layout", "featured + 3 grid", "gradient covers", "author meta", "responsive"]

    elif key == "cards":
        body = '<div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">%s</div>' % "".join(
            '<article class="%s %s overflow-hidden flex flex-col">%s<div class="p-6 flex-1 flex flex-col">'
            '<span class="%s mb-3 inline-flex">%s</span><h3 class="font-semibold text-lg leading-snug flex-1">%s</h3>%s</div></article>' % (
                b["surface"], b["hover_card"], cover(n, "aspect-[16/9]"), b["badge"], p[1], p[0], meta(p[2], p[3], p[4], n))
            for n, p in enumerate(POSTS[:6]))
        feat = ["card layout", "6 posts", "equal-height cards", "gradient covers", "responsive 1/2/3-col"]

    elif key == "sidebar":
        main = '<div class="space-y-5">%s</div>' % "".join(
            '<article class="%s %s p-5 flex gap-5">%s<div class="flex-1"><span class="%s mb-2 inline-flex">%s</span>'
            '<h3 class="font-semibold leading-snug">%s</h3>%s</div></article>' % (
                b["surface"], b["hover_card"], cover(n, "w-28 h-28 shrink-0"), b["badge"], p[1], p[0], meta(p[2], p[3], p[4], n))
            for n, p in enumerate(POSTS[:4]))
        side = ('<aside class="%s p-6"><h3 class="font-semibold mb-4">Categories</h3><ul class="space-y-2">%s</ul>'
                '<h3 class="font-semibold mt-6 mb-4">Popular tags</h3><div class="flex flex-wrap gap-2">%s</div></aside>') % (
            b["surface_soft"], "".join('<li><a href="#" class="flex items-center justify-between text-sm %s hover:opacity-100"><span>%s</span><span class="%s">%d</span></a>' % (
                b["text_muted"], c, b["text_muted"], n) for n, c in enumerate(["Engineering", "Design", "Product", "Security", "Culture"])),
            "".join('<a href="#" class="%s">%s</a>' % (b["chip"], t) for t in ["rust", "design", "saas", "startup", "dx", "api"]))
        body = '<div class="grid grid-cols-1 gap-6 lg:grid-cols-[1fr_280px]">%s%s</div>' % (main, side)
        feat = ["sidebar blog layout", "horizontal post rows", "category counts", "tag cloud", "responsive split"]

    elif key == "news":
        body = ('<div class="grid grid-cols-1 gap-5 lg:grid-cols-4">'
                '<article class="lg:col-span-2 lg:row-span-2 %s %s overflow-hidden">%s<div class="p-6"><span class="%s mb-3 inline-flex">%s</span>'
                '<h3 class="f-disp text-xl font-bold leading-tight">%s</h3>%s</div></article>%s</div>') % (
            b["surface"], b["hover_card"], cover(0, "aspect-[16/10]"), b["badge"], POSTS[0][1], POSTS[0][0], meta(POSTS[0][2], POSTS[0][3], POSTS[0][4], 0),
            "".join('<article class="%s %s overflow-hidden">%s<div class="p-4"><span class="%s mb-1.5 inline-flex">%s</span>'
                    '<h3 class="font-semibold text-sm leading-snug">%s</h3></div></article>' % (
                        b["surface"], b["hover_card"], cover(n + 1, "aspect-[16/9]"), b["badge"], p[1], p[0]) for n, p in enumerate(POSTS[1:6])))
        feat = ["news layout", "lead + 5 side", "4-col grid", "dense composition", "gradient covers"]

    elif key == "minimal":
        body = '<div class="divide-y divide-current/10 max-w-3xl mx-auto">%s</div>' % "".join(
            '<article class="py-6"><div class="flex items-center gap-3 mb-2"><span class="%s">%s</span><span class="text-xs %s">%s</span></div>'
            '<a href="#"><h3 class="f-disp text-xl font-semibold leading-snug hover:opacity-70">%s</h3></a>'
            '<p class="mt-2 text-sm %s">%s</p></article>' % (b["badge"], p[1], b["text_muted"], p[4], p[0], b["text_muted"], p[2])
            for n, p in enumerate(POSTS[:6]))
        feat = ["minimal article list", "no images", "hairline dividers", "typographic", "narrow max width"]

    elif key == "list":
        body = '<ul class="space-y-4 max-w-3xl mx-auto">%s</ul>' % "".join(
            '<li><a href="#" class="%s %s p-5 flex items-center gap-5"><span class="flex h-12 w-12 shrink-0 items-center justify-center %s">%s</span>'
            '<div class="flex-1"><div class="flex items-center gap-2"><span class="%s">%s</span><span class="text-xs %s">%s</span></div>'
            '<h3 class="font-semibold mt-1">%s</h3></div>%s</a></li>' % (
                b["surface"], b["hover_card"], b["surface_soft"], ic("doc", "h-5 w-5"), b["badge"], p[1], b["text_muted"], p[3], p[0], ic("arrow", "h-4 w-4"))
            for n, p in enumerate(POSTS[:6]))
        feat = ["article list", "icon rows", "clickable cards", "6 posts", "narrow max width"]

    elif key == "grid-3":
        body = '<div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">%s</div>' % "".join(
            '<article class="%s %s overflow-hidden">%s<div class="p-5"><span class="%s mb-2 inline-flex">%s</span>'
            '<h3 class="font-semibold leading-snug">%s</h3><p class="mt-3 text-xs %s">%s · %s</p></div></article>' % (
                b["surface"], b["hover_card"], cover(n, "aspect-[16/9]"), b["badge"], p[1], p[0], b["text_muted"], p[3], p[4])
            for n, p in enumerate(POSTS[:9]))
        feat = ["three-column grid", "9 posts", "gradient covers", "read time + date", "responsive 1/2/3-col"]

    elif key == "split-feature":
        body = ('<div class="grid grid-cols-1 gap-8 lg:grid-cols-2">%s<div class="space-y-4">%s</div></div>') % (
            '<article class="%s %s overflow-hidden">%s<div class="p-7"><span class="%s mb-3 inline-flex">%s Featured</span>'
            '<h3 class="f-disp text-2xl font-bold leading-tight">%s</h3><p class="mt-3 text-sm %s">The full story behind the headline.</p>%s</div></article>' % (
                b["surface"], b["hover_card"], cover(0, "aspect-[16/10]"), b["badge"], ic("spark", "h-3.5 w-3.5"), POSTS[0][0], b["text_muted"], meta(POSTS[0][2], POSTS[0][3], POSTS[0][4], 0)),
            "".join('<article class="%s %s p-4 flex gap-4">%s<div><span class="%s mb-1 inline-flex">%s</span>'
                    '<h3 class="font-semibold text-sm leading-snug">%s</h3><p class="mt-1 text-xs %s">%s</p></div></article>' % (
                        b["surface_soft"], b["hover_card"], cover(n + 1, "w-20 h-20 shrink-0"), b["badge"], p[1], p[0], b["text_muted"], p[3])
                    for n, p in enumerate(POSTS[1:5])))
        feat = ["split featured blog", "large + list", "2-col split", "gradient covers", "responsive"]

    elif key == "category":
        cats = ["All", "Engineering", "Design", "Product", "Culture"]
        tabs = '<div class="mb-6 flex flex-wrap gap-2">%s</div>' % "".join(
            '<button type="button" class="%s px-4 py-2 text-sm font-medium %s" aria-selected="%s">%s</button>' % (
                b["surface"] if n == 0 else b["surface_soft"], b["text"] if n == 0 else b["text_muted"], "true" if n == 0 else "false", c)
            for n, c in enumerate(cats))
        body = tabs + '<div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">%s</div>' % "".join(
            '<article class="%s %s overflow-hidden">%s<div class="p-5"><span class="%s mb-2 inline-flex">%s</span>'
            '<h3 class="font-semibold leading-snug">%s</h3>%s</div></article>' % (
                b["surface"], b["hover_card"], cover(n, "aspect-[16/9]"), b["badge"], p[1], p[0], meta(p[2], p[3], p[4], n))
            for n, p in enumerate(POSTS[:6]))
        feat = ["category blog", "filter tabs", "active state", "6 posts", "responsive 1/2/3-col"]

    else:  # recent
        body = ('<div class="flex items-center justify-between mb-6"><h3 class="f-disp text-xl font-bold">Recent posts</h3>'
                '<a href="#" class="%s inline-flex items-center gap-2 text-sm">%s View all</a></div>'
                '<div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">%s</div>') % (
            b["btn_secondary"], ic("arrow", "h-4 w-4"),
            "".join('<article class="%s %s overflow-hidden">%s<div class="p-4"><span class="%s mb-2 inline-flex">%s</span>'
                    '<h3 class="font-semibold text-sm leading-snug">%s</h3><p class="mt-2 text-xs %s">%s</p></div></article>' % (
                        b["surface"], b["hover_card"], cover(n, "aspect-[16/9]"), b["badge"], p[1], p[0], b["text_muted"], p[3])
                    for n, p in enumerate(POSTS[:4])))
        feat = ["recent posts", "view-all link", "4 posts", "section header", "responsive 1/2/4-col"]

    code = section(h + body, style)
    desc = "%s blog layout: %s." % (TOKENS[style]["title"].split(" (")[0], feat[0].capitalize())
    return dict(code=code, section_name=title, eyebrow="Blog", features=feat,
                tags=["blog", "articles", "content", "posts"] + [style], desc=desc, scope="blog")
