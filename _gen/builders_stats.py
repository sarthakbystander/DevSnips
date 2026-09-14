"""Stats section builders — 15 concepts."""
from .helpers import TOKENS, ic, ICONS
from .layout import head, section


def stats(style, i):
    b = TOKENS[style]
    concepts = [
        ("kpi-cards", "KPI Cards"),
        ("dashboard", "Dashboard Stats"),
        ("company", "Company Metrics"),
        ("startup", "Startup Growth Stats"),
        ("animated", "Animated Counter Stats"),
        ("bento", "Bento Stats"),
        ("minimal", "Minimal Stats"),
        ("premium", "Premium Stats"),
        ("glass", "Glass Stats" if style == "edge-glassmorphism" else "Spotlight Stats"),
        ("brutalist", "Brutalist Stats" if style == "neo-brutalism" else "Bold Stats"),
        ("split", "Split Stats"),
        ("bar", "Progress Bar Stats"),
        ("comparison", "Comparison Stats"),
        ("inline", "Inline Stat Strip"),
        ("circular", "Circular Stats"),
    ]
    key, title = concepts[i]
    h = head("Stats", "trend", "Numbers that matter", "Real performance, measured every single day.", style)

    def stat_card(value, label, iconn="bolt", sub=""):
        return ('<div class="%s %s p-6"><div class="flex items-center justify-between"><span class="flex h-10 w-10 items-center justify-center %s">%s</span>'
                '%s</div><p class="mt-4 f-disp text-3xl sm:text-4xl font-bold">%s</p><p class="mt-1 text-sm %s">%s</p>%s</div>') % (
            b["surface"], b["hover_card"], b["surface_soft"], ic(iconn, "h-5 w-5"),
            '<span class="f-mono text-xs %s">+%s</span>' % (b["text_muted"], sub) if sub else "",
            value, b["text_muted"], label, "")

    if key == "kpi-cards":
        cards = "".join(stat_card(v, l, icn, s) for v, l, icn, s in [
            ("$4.2M", "Annual revenue", "credit", "18"), ("128k", "Active users", "users", "32"), ("99.9%", "Uptime SLA", "shield", "0.1"), ("1m 42s", "Median reply", "clock", "12")])
        body = '<div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">%s</div>' % cards
        feat = ["4 KPI cards", "delta indicators", "iconified", "hover lift", "responsive 1/2/4-col"]

    elif key == "dashboard":
        top = ('<div class="%s p-6 mb-5"><div class="flex items-center justify-between"><div><p class="text-sm %s">Total revenue</p>'
               '<p class="f-disp text-3xl font-bold mt-1">$4,247,820</p></div><span class="%s">%s +18.4%%</span></div>'
               '<div class="mt-4 flex items-end gap-1.5 h-24">%s</div>'
               '<div class="mt-2 flex justify-between text-xs %s"><span>Jan</span><span>Feb</span><span>Mar</span><span>Apr</span><span>May</span><span>Jun</span></div></div>') % (
            b["surface"], b["text_muted"], b["badge"], ic("trend", "h-3.5 w-3.5"),
            "".join('<div class="flex-1 rounded-t %s" style="height:%d%%"></div>' % (b["surface_soft"], h) for h in [40, 55, 48, 70, 65, 90]),
            b["text_muted"])
        mini = "".join(stat_card(v, l, icn, s) for v, l, icn, s in [
            ("12,840", "Tickets", "headset", "8"), ("98%", "CSAT", "heart", "2"), ("3.2h", "Avg resolve", "clock", "15")])
        body = top + '<div class="grid grid-cols-1 gap-5 sm:grid-cols-3">%s</div>' % mini
        feat = ["dashboard stat panel", "bar chart placeholder", "month axis", "3 KPI tiles", "responsive"]

    elif key == "company":
        cards = "".join(stat_card(v, l, icn, s) for v, l, icn, s in [
            ("340+", "Employees", "users", "12"), ("42", "Countries", "globe", "4"), ("$120M", "Funding raised", "credit", "25"), ("6", "Global offices", "building", "0")])
        body = '<div class="grid grid-cols-2 gap-5 lg:grid-cols-4">%s</div>' % cards
        feat = ["company metrics grid", "4 stats", "delta badges", "2-col mobile", "responsive 2/4-col"]

    elif key == "startup":
        body = ('<div class="%s p-8 sm:p-10"><div class="grid grid-cols-1 gap-8 lg:grid-cols-[1.2fr_1fr] items-center">'
                '<div><span class="%s mb-4 inline-flex">%s Growth</span><p class="f-disp text-4xl sm:text-5xl font-bold">340%%</p>'
                '<p class="mt-2 %s">Year-over-year revenue growth, three years running.</p></div>'
                '<div class="space-y-4">%s</div></div></div>') % (
            b["surface"], b["badge"], ic("rocket", "h-3.5 w-3.5"), b["text_muted"],
            "".join('<div><div class="flex justify-between text-sm mb-1"><span class="%s">%s</span><span class="font-semibold">%s</span></div>'
                    '<div class="h-2 rounded-full %s overflow-hidden"><div class="h-full rounded-full" style="width:%s%%;background:%s"></div></div></div>' % (
                        b["text_muted"], label, val, b["surface_soft"], pct, b["accent"])
                    for label, val, pct in [("Users", "128k", 82), ("Revenue", "$4.2M", 75), ("NPS", "72", 90)]))
        feat = ["startup growth panel", "headline percentage", "3 progress bars", "accent fills", "responsive split"]

    elif key == "animated":
        body = ('<div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">%s</div>') % "".join(
            '<div class="%s %s p-6 text-center"><p class="f-disp text-4xl sm:text-5xl font-bold" data-counter data-to="%s" data-suffix="%s">0%s</p>'
            '<p class="mt-2 text-sm %s">%s</p></div>' % (b["surface"], b["hover_card"], to, suf, suf, b["text_muted"], label)
            for to, suf, label in [(128, "k", "Active users"), (99, "%", "Uptime"), (42, "+", "Countries"), (7, "M+", "API calls/day")])
        feat = ["animated counter UI", "data-counter hooks", "4 stats", "suffix support", "responsive 1/2/4-col"]

    elif key == "bento":
        big = ('<div class="lg:col-span-2 lg:row-span-2 %s %s p-8 flex flex-col justify-between min-h-[260px]">'
               '<div><span class="%s">%s Feature</span><p class="mt-4 f-disp text-5xl font-bold">$4.2M</p>'
               '<p class="mt-2 %s">Annual recurring revenue, up 18%% YoY.</p></div>'
               '<div class="flex items-end gap-1.5 h-20">%s</div></div>') % (
            b["surface"], b["hover_card"], b["badge"], ic("credit", "h-3.5 w-3.5"), b["text_muted"],
            "".join('<div class="flex-1 rounded-t %s" style="height:%d%%"></div>' % (b["surface_soft"], h) for h in [30, 50, 45, 70, 60, 85, 75]))
        small = "".join(
            '<div class="%s %s p-6"><p class="f-disp text-2xl font-bold">%s</p><p class="mt-1 text-sm %s">%s</p></div>' % (
                b["surface"], b["hover_card"], v, b["text_muted"], l)
            for v, l in [("128k", "Users"), ("99.9%", "Uptime"), ("42", "Countries"), ("1m 42s", "Reply time")])
        body = '<div class="grid grid-cols-2 gap-4 lg:grid-cols-4">%s%s</div>' % (big, small)
        feat = ["bento stats grid", "large hero stat", "bar chart inset", "4 supporting tiles", "responsive 2/4-col"]

    elif key == "minimal":
        body = ('<div class="grid grid-cols-2 gap-8 lg:grid-cols-4">%s</div>') % "".join(
            '<div class="text-center"><p class="f-disp text-3xl sm:text-4xl font-bold">%s</p><p class="mt-2 text-sm %s">%s</p></div>' % (
                v, b["text_muted"], l)
            for v, l in [("128k", "Users"), ("$4.2M", "ARR"), ("99.9%", "Uptime"), ("42", "Countries")])
        feat = ["minimal text stats", "no cards", "centered values", "2/4-col grid", "low chrome"]

    elif key == "premium":
        body = ('<div class="%s p-8 sm:p-12"><div class="grid grid-cols-2 gap-8 lg:grid-cols-4">%s</div></div>') % (
            b["surface"], "".join(
                '<div class="text-center"><div class="mx-auto mb-3 flex h-12 w-12 items-center justify-center %s">%s</div>'
                '<p class="f-disp text-3xl sm:text-4xl font-bold">%s</p><p class="mt-1 text-sm %s">%s</p></div>' % (
                    b["surface_soft"], ic(icn, "h-5 w-5"), v, b["text_muted"], l)
                for v, l, icn in [("128k", "Users", "users"), ("$4.2M", "ARR", "credit"), ("99.9%", "Uptime", "shield"), ("72", "NPS", "heart")]))
        feat = ["premium stat panel", "iconized tiles", "centered composition", "boxed container", "responsive 2/4-col"]

    elif key == "glass":
        body = ('<div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">%s</div>') % "".join(
            '<div class="%s %s p-6"><div class="flex items-center gap-3"><span class="flex h-10 w-10 items-center justify-center %s">%s</span>'
            '<div><p class="f-disp text-2xl font-bold">%s</p><p class="text-xs %s">%s</p></div></div>'
            '<div class="mt-4 h-1.5 rounded-full %s overflow-hidden"><div class="h-full rounded-full" style="width:%s%%;background:%s"></div></div></div>' % (
                b["surface"], b["hover_card"], b["surface_soft"], ic(icn, "h-4 w-4"), v, b["text_muted"], l, b["surface_soft"], pct, b["accent"])
            for v, l, icn, pct in [("128k", "Active users", "users", 82), ("99.9%", "Uptime", "shield", 99), ("72", "NPS", "heart", 72), ("4.2M", "API calls/day", "bolt", 65), ("1m 42s", "Reply time", "clock", 40), ("340", "Employees", "users", 55)])
        feat = ["spotlight stat cards", "mini progress bars", "6 metrics", "icon + value", "responsive 1/2/3-col"]

    elif key == "brutalist":
        body = ('<div class="grid grid-cols-2 gap-0 %s" >%s</div>') % (b["surface"], "".join(
            '<div class="border-2 border-current p-6 text-center"><p class="f-mono text-3xl font-bold">%s</p><p class="mt-2 f-mono text-xs uppercase tracking-wider %s">%s</p></div>'
            % (v, b["text_muted"], l)
            for v, l in [("128k", "Users"), ("$4.2M", "ARR"), ("99.9%", "Uptime"), ("340", "Team")]))
        feat = ["brutalist stat grid", "edge-to-edge borders", "mono numerals", "2x2 grid", "uppercase labels"]

    elif key == "split":
        body = ('<div class="grid grid-cols-1 gap-8 lg:grid-cols-2 items-center">'
                '<div><span class="%s mb-4 inline-flex">%s Featured</span><p class="f-disp text-5xl sm:text-6xl font-bold">128k</p>'
                '<p class="mt-3 %s text-lg">Active users across 42 countries, growing 32%% quarter over quarter.</p></div>'
                '<div class="grid grid-cols-2 gap-4">%s</div></div>') % (
            b["badge"], ic("users", "h-3.5 w-3.5"), b["text_muted"], "".join(
                '<div class="%s p-5"><p class="f-disp text-2xl font-bold">%s</p><p class="mt-1 text-xs %s">%s</p></div>' % (
                    b["surface"], v, b["text_muted"], l)
                for v, l in [("$4.2M", "ARR"), ("99.9%", "Uptime"), ("72", "NPS"), ("1m 42s", "Reply time")]))
        feat = ["split stat layout", "large headline number", "2x2 supporting grid", "asymmetric balance", "responsive"]

    elif key == "bar":
        body = ('<div class="space-y-5 max-w-3xl mx-auto">%s</div>') % "".join(
            '<div class="%s p-5"><div class="flex items-center justify-between mb-2"><span class="text-sm font-medium">%s</span><span class="f-disp text-lg font-bold">%s</span></div>'
            '<div class="h-3 rounded-full %s overflow-hidden"><div class="h-full rounded-full" style="width:%s%%;background:%s"></div></div></div>' % (
                b["surface"], label, val, b["surface_soft"], pct, b["accent"])
            for label, val, pct in [("Active users", "128k", 82), ["ARR", "$4.2M", 75], ["Uptime", "99.9%", 99], ["NPS", "72", 72], ["Retention", "94%", 94]])
        feat = ["progress bar stats", "horizontal bars", "5 metrics", "value + label", "accent fills"]

    elif key == "comparison":
        body = ('<div class="grid grid-cols-2 gap-5">%s</div>') % "".join(
            '<div class="%s p-6 text-center"><p class="text-xs %s uppercase tracking-wider">%s</p>'
            '<p class="mt-2 f-disp text-3xl font-bold">%s</p>'
            '<div class="mt-3 flex items-end gap-1 h-16 justify-center">%s</div></div>' % (
                b["surface"], b["text_muted"], period, v,
                "".join('<div class="w-3 rounded-t %s" style="height:%d%%"></div>' % (b["surface_soft"], h) for h in [40, 60, 50, 75]))
            for period, v in [("Last year", "$3.6M"), ("This year", "$4.2M")])
        feat = ["year-over-year comparison", "two panels", "mini bar charts", "period labels", "responsive 2-col"]

    elif key == "inline":
        body = ('<div class="%s p-6"><div class="grid grid-cols-2 gap-6 sm:grid-cols-4 sm:divide-x sm:divide-current/10">%s</div></div>') % (
            b["surface"], "".join(
                '<div class="text-center sm:px-4"><p class="f-disp text-2xl sm:text-3xl font-bold">%s</p><p class="mt-1 text-xs %s">%s</p></div>' % (
                    v, b["text_muted"], l)
                for v, l in [("128k", "Users"), ("$4.2M", "ARR"), ("99.9%", "Uptime"), ("42", "Countries")]))
        feat = ["inline stat strip", "divided columns", "compact container", "centered values", "responsive 2/4-col"]

    else:  # circular
        body = ('<div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">%s</div>') % "".join(
            '<div class="%s %s p-6 text-center"><div class="relative mx-auto h-24 w-24">'
            '<svg viewBox="0 0 36 36" class="h-24 w-24 -rotate-90"><circle cx="18" cy="18" r="15.9155" fill="none" stroke="currentColor" stroke-opacity="0.15" stroke-width="3"/>'
            '<circle cx="18" cy="18" r="15.9155" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round" stroke-dasharray="%d 100"/></svg>'
            '<div class="absolute inset-0 flex flex-col items-center justify-center"><p class="f-disp text-xl font-bold">%s</p></div></div>'
            '<p class="mt-3 text-sm %s">%s</p></div>' % (
                b["surface"], b["hover_card"], b["accent"], pct, v, b["text_muted"], l)
            for v, pct, l in [("82%", 82, "Active users"), ("99%", 99, "Uptime"), ("72", 72, "NPS"), ("94%", 94, "Retention")])
        feat = ["circular progress stats", "SVG ring charts", "4 metrics", "dasharray fills", "responsive 1/2/4-col"]

    code = section(h + body, style)
    desc = "%s stats layout: %s." % (TOKENS[style]["title"].split(" (")[0], feat[0].capitalize())
    return dict(code=code, section_name=title, eyebrow="Stats", features=feat,
                tags=["stats", "metrics", "kpi", "numbers"] + [style], desc=desc, scope="stats")
