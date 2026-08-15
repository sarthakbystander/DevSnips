"""Team section builders — 15 concepts."""
from .helpers import TOKENS, avatar, ic, ICONS, logo_svg
from .layout import head, section

TEAM = [
    ("Maya Chen", "CEO & Co-founder", "Ex-Stripe. Leads vision and go-to-market."),
    ("Daniel Reyes", "CTO & Co-founder", "Ex-Vercel. Architects the platform."),
    ("Aisha Karim", "Head of Product", "Ex-Linear. Owns the roadmap."),
    ("Tom Bradley", "Head of Engineering", "Ex-Resend. Scales the stack."),
    ("Sofia Rossi", "Head of Design", "Ex-Notion. Crafts the system."),
    ("Jordan Fields", "Dev Advocate", "Ex-Raycast. Builds community."),
    ("Priya Nair", "VP Sales", "Ex-Framer. Closes enterprise."),
    ("Ethan Park", "COO", "Ex-Stripe Ops. Runs the business."),
    ("Lena Vogt", "Staff Engineer", "Ex-GitHub. Loves distributed systems."),
    ("Marcus Webb", "Security Lead", "Ex-Cloudflare. Sleeps well."),
    ("Dana Fischer", "Head of Support", "Ex-Cal.com. Replies fast."),
    ("Ravi Mehta", "Founding Engineer", "Ex-Linear. Ships daily."),
]


def team(style, i):
    b = TOKENS[style]
    concepts = [
        ("grid", "Team Grid"),
        ("exec", "Executive Cards"),
        ("founders", "Startup Founders"),
        ("bento", "Bento Team"),
        ("editorial", "Editorial Team"),
        ("circular", "Circular Profiles"),
        ("glass", "Glass Team Cards" if style == "edge-glassmorphism" else "Spotlight Team"),
        ("brutalist", "Brutalist Team Cards" if style == "neo-brutalism" else "Bold Team Cards"),
        ("hierarchy", "Company Hierarchy"),
        ("minimal", "Minimal Profiles"),
        ("feature", "Featured Team"),
        ("compact", "Compact Team Grid"),
        ("detailed", "Detailed Profile Cards"),
        ("avatar-wall", "Avatar Wall Team"),
        ("leadership", "Leadership Row"),
    ]
    key, title = concepts[i]
    h = head("Team", "users", "Meet the people behind it", "A small, senior team obsessed with making support feel calm.", style)

    def socials():
        return '<div class="flex gap-2">' + "".join(
            '<a href="#" class="flex h-7 w-7 items-center justify-center %s" aria-label="%s">%s</a>' % (b["surface_soft"], s, ic(s, "h-3.5 w-3.5"))
            for s in ["twitter", "github", "linkedin"]) + '</div>'

    def card(name, role, bio, n):
        return ('<article class="%s %s p-6"><div class="mb-4">%s</div>'
                '<h3 class="font-semibold">%s</h3><p class="text-sm %s">%s</p>'
                '<p class="mt-3 text-sm %s leading-relaxed">%s</p>'
                '<div class="mt-5">%s</div></article>') % (
            b["surface"], b["hover_card"], avatar(name, n, "ring-2 ring-offset-2 ring-offset-transparent ring-white/15"), name, b["text_muted"], role, b["text_muted"], bio, socials())

    if key == "grid":
        body = '<div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">%s</div>' % "".join(
            card(name, role, bio, n) for n, (name, role, bio) in enumerate(TEAM[:8]))
        feat = ["team grid", "8 members", "social links", "hover lift", "responsive 1/2/4-col"]

    elif key == "exec":
        body = '<div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">%s</div>' % "".join(
            ('<article class="%s %s p-7"><div class="flex items-center gap-4">%s<div><h3 class="font-semibold text-lg">%s</h3>'
             '<p class="text-sm %s">%s</p></div></div><p class="mt-4 text-sm %s leading-relaxed">%s</p>'
             '<div class="mt-5 flex items-center justify-between">%s<span class="%s">%s yrs</span></div></article>') % (
                b["surface"], b["hover_card"], avatar(name, n), name, b["text_muted"], role, b["text_muted"], bio, socials(), b["badge"], exp)
            for n, (name, role, bio, exp) in enumerate([(t[0], t[1], t[2], e) for t, e in zip(TEAM[:6], [12, 10, 9, 11, 8, 7])]))
        feat = ["executive cards", "experience badges", "6 leaders", "social links", "responsive 1/2/3-col"]

    elif key == "founders":
        f1, f2, f3 = TEAM[0], TEAM[1], TEAM[5]
        big = ('<div class="lg:col-span-2 %s %s p-8"><div class="grid grid-cols-1 gap-6 sm:grid-cols-[160px_1fr] items-center">'
               '%s<div><span class="%s mb-3 inline-flex">%s Co-founder</span><h3 class="f-disp text-2xl font-bold">%s</h3>'
               '<p class="text-sm %s">%s</p><p class="mt-3 text-sm %s leading-relaxed">%s</p>'
               '<div class="mt-5">%s</div></div></div></div>') % (
            b["surface"], b["hover_card"], avatar(f1[0], 0, "h-40 w-40"), b["badge"], ic("rocket", "h-3.5 w-3.5"), f1[0], b["text_muted"], f1[1], b["text_muted"], f1[2], socials())
        sides = "".join(
            ('<div class="%s %s p-6"><div class="flex items-center gap-3">%s<div><h3 class="font-semibold">%s</h3>'
             '<p class="text-xs %s">%s</p></div></div><p class="mt-3 text-sm %s">%s</p>%s</div>') % (
                b["surface"], b["hover_card"], avatar(t[0], n), t[0], b["text_muted"], t[1], b["text_muted"], t[2], '<div class="mt-4">' + socials() + '</div>')
            for n, t in enumerate([f2, f3]))
        body = '<div class="grid grid-cols-1 gap-5 lg:grid-cols-3">%s%s</div>' % (big, sides)
        feat = ["founders spotlight", "large feature card", "2 supporting cards", "2/3 + 1/3 split", "social links"]

    elif key == "bento":
        body = '<div class="grid grid-cols-2 gap-4 lg:grid-cols-4">%s</div>' % "".join(
            '<article class="%s %s p-5 text-center"><div class="mx-auto mb-3">%s</div>'
            '<h3 class="font-semibold text-sm">%s</h3><p class="text-xs %s">%s</p></article>' % (
                b["surface"], b["hover_card"], avatar(name, n, "h-16 w-16"), name, b["text_muted"], role)
            for n, (name, role, bio) in enumerate(TEAM[:8]))
        feat = ["bento team grid", "compact tiles", "8 members", "centered avatars", "responsive 2/4-col"]

    elif key == "editorial":
        body = '<div class="grid grid-cols-1 gap-8 lg:grid-cols-[1.3fr_1fr]">%s<div class="space-y-6">%s</div></div>' % (
            ('<article class="%s p-8"><div class="mb-6">%s</div><span class="%s mb-3 inline-flex">%s Feature</span>'
             '<h3 class="f-disp text-3xl font-bold">%s</h3><p class="text-sm %s mt-1">%s</p>'
             '<p class="mt-4 text-sm leading-relaxed %s">%s</p><div class="mt-6">%s</div></article>') % (
                b["surface"], avatar(TEAM[0][0], 0, "h-32 w-32"), b["badge"], ic("spark", "h-3.5 w-3.5"), TEAM[0][0], b["text_muted"], TEAM[0][1], b["text_muted"], TEAM[0][2], socials()),
            "".join('<article class="%s p-5 flex items-center gap-4">%s<div><h3 class="font-semibold">%s</h3><p class="text-xs %s">%s</p></div></article>' % (
                b["surface_soft"], avatar(t[0], n, "h-12 w-12"), t[0], b["text_muted"], t[1]) for n, t in enumerate(TEAM[1:5])))
        feat = ["editorial team layout", "featured profile", "side list", "serif headline", "responsive split"]

    elif key == "circular":
        body = '<div class="grid grid-cols-2 gap-8 sm:grid-cols-3 lg:grid-cols-6">%s</div>' % "".join(
            '<figure class="text-center"><div class="mx-auto">%s</div><figcaption class="mt-3"><p class="font-semibold text-sm">%s</p><p class="text-xs %s">%s</p></figcaption></figure>' % (
                avatar(name, n, "h-24 w-24 ring-2 ring-offset-4 ring-offset-transparent ring-white/15"), name, b["text_muted"], role)
            for n, (name, role, bio) in enumerate(TEAM[:6]))
        feat = ["circular profiles", "6 members", "ringed avatars", "centered captions", "responsive 2/3/6-col"]

    elif key == "glass":
        body = '<div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">%s</div>' % "".join(
            ('<article class="%s %s p-6"><div class="flex items-center gap-4">%s<div class="flex-1"><h3 class="font-semibold">%s</h3>'
             '<p class="text-sm %s">%s</p></div><span class="%s">%s</span></div>'
             '<p class="mt-4 text-sm %s leading-relaxed">%s</p><div class="mt-5">%s</div></article>') % (
                b["surface"], b["hover_card"], avatar(name, n), name, b["text_muted"], role, b["badge"], ic("shield-check", "h-3.5 w-3.5"), b["text_muted"], bio, socials())
            for n, (name, role, bio) in enumerate(TEAM[:6]))
        feat = ["spotlight team cards", "verified badges", "6 members", "social links", "responsive 1/2/3-col"]

    elif key == "brutalist":
        body = '<div class="grid grid-cols-2 gap-4 lg:grid-cols-4">%s</div>' % "".join(
            '<article class="%s %s p-5"><div class="mb-4">%s</div><h3 class="f-mono text-sm font-bold uppercase">%s</h3>'
            '<p class="f-mono text-xs %s">%s</p></article>' % (
                b["surface"], b["hover_card"], avatar(name, n, "h-20 w-20"), name, b["text_muted"], role)
            for n, (name, role, bio) in enumerate(TEAM[:8]))
        feat = ["brutalist team cards", "mono labels", "uppercase names", "8 members", "responsive 2/4-col"]

    elif key == "hierarchy":
        ceo = TEAM[0]
        clevel = TEAM[1:4]
        leads = TEAM[4:8]
        top = ('<div class="flex justify-center mb-6"><article class="%s %s p-6 text-center w-full max-w-xs">%s<h3 class="mt-4 font-semibold text-lg">%s</h3>'
               '<p class="text-sm %s">%s</p></article></div>') % (b["surface"], b["hover_card"], avatar(ceo[0], 0, "h-24 w-24"), ceo[0], b["text_muted"], ceo[1])
        mid = '<div class="grid grid-cols-1 gap-4 sm:grid-cols-3 mb-6">%s</div>' % "".join(
            '<article class="%s %s p-5 text-center">%s<h3 class="mt-3 font-semibold text-sm">%s</h3><p class="text-xs %s">%s</p></article>' % (
                b["surface_soft"], b["hover_card"], avatar(t[0], n, "h-16 w-16"), t[0], b["text_muted"], t[1]) for n, t in enumerate(clevel))
        bot = '<div class="grid grid-cols-2 gap-4 sm:grid-cols-4">%s</div>' % "".join(
            '<article class="%s %s p-4 text-center">%s<h3 class="mt-2 font-medium text-xs">%s</h3><p class="text-xs %s">%s</p></article>' % (
                b["surface_soft"], b["hover_card"], avatar(t[0], n, "h-12 w-12"), t[0], b["text_muted"], t[1]) for n, t in enumerate(leads))
        body = top + mid + bot
        feat = ["org hierarchy", "3-tier layout", "CEO + C-level + leads", "tree composition", "responsive"]

    elif key == "minimal":
        body = '<div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">%s</div>' % "".join(
            '<article class="flex items-center gap-4">%s<div><h3 class="font-semibold">%s</h3><p class="text-sm %s">%s</p></div></article>' % (
                avatar(name, n, "h-12 w-12"), name, b["text_muted"], role)
            for n, (name, role, bio) in enumerate(TEAM[:6]))
        feat = ["minimal profiles", "inline rows", "avatar + name", "no cards", "responsive 1/2/3-col"]

    elif key == "feature":
        body = ('<div class="grid grid-cols-1 gap-6 lg:grid-cols-2 items-center">'
                '<article class="%s %s p-8"><div class="mb-6">%s</div><h3 class="f-disp text-2xl font-bold">%s</h3>'
                '<p class="text-sm %s">%s</p><p class="mt-4 text-sm leading-relaxed %s">%s</p>'
                '<div class="mt-6">%s</div></article>'
                '<div class="grid grid-cols-2 gap-4">%s</div></div>') % (
            b["surface"], b["hover_card"], avatar(TEAM[1][0], 1, "h-32 w-32"), TEAM[1][0], b["text_muted"], TEAM[1][1], b["text_muted"], TEAM[1][2], socials(),
            "".join('<article class="%s %s p-4 text-center">%s<h3 class="mt-2 font-medium text-sm">%s</h3><p class="text-xs %s">%s</p></article>' % (
                b["surface_soft"], b["hover_card"], avatar(t[0], n, "h-14 w-14"), t[0], b["text_muted"], t[1]) for n, t in enumerate(TEAM[2:6])))
        feat = ["featured + grid team", "large profile card", "2x2 supporting", "responsive split", "social links"]

    elif key == "compact":
        body = '<div class="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-6">%s</div>' % "".join(
            '<article class="%s %s p-3 text-center"><div class="mx-auto mb-2">%s</div><p class="text-xs font-medium truncate">%s</p><p class="text-xs %s truncate">%s</p></article>' % (
                b["surface_soft"], b["hover_card"], avatar(name, n, "h-12 w-12"), name, b["text_muted"], role)
            for n, (name, role, bio) in enumerate(TEAM[:12]))
        feat = ["compact team grid", "12 members", "small tiles", "responsive 2/3/6-col", "truncate names"]

    elif key == "detailed":
        body = '<div class="grid grid-cols-1 gap-5 sm:grid-cols-2">%s</div>' % "".join(
            ('<article class="%s %s p-6"><div class="flex gap-4">%s<div class="flex-1"><div class="flex items-center gap-2"><h3 class="font-semibold">%s</h3>'
             '<span class="%s">%s</span></div><p class="text-sm %s">%s</p></div></div><p class="mt-4 text-sm %s leading-relaxed">%s</p>'
             '<div class="mt-5 grid grid-cols-3 gap-2 text-center">%s</div><div class="mt-5">%s</div></article>') % (
                b["surface"], b["hover_card"], avatar(name, n, "h-20 w-20"), name, b["badge"], ic("shield-check", "h-3 w-3.5"), b["text_muted"], role, b["text_muted"], bio,
                "".join('<div class="%s p-2"><p class="text-xs font-bold">%s</p><p class="text-xs %s">%s</p></div>' % (b["surface_soft"], v, b["text_muted"], l) for v, l in [("8y", "Tenure"), ("42", "Projects"), ("4.9", "Rating")]),
                socials())
            for n, (name, role, bio) in enumerate(TEAM[:4]))
        feat = ["detailed profile cards", "stat sub-tiles", "verified badge", "4 members", "responsive 1/2-col"]

    elif key == "avatar-wall":
        body = ('<div class="%s %s p-8 text-center"><div class="flex flex-wrap justify-center gap-3 mb-6">%s</div>'
                '<h3 class="f-disp text-2xl font-bold">We are 340 strong</h3><p class="mt-2 text-sm %s">Across 6 offices and 42 countries.</p>'
                '<a href="#" class="mt-5 inline-flex items-center gap-2 %s">%s Join the team</a></div>') % (
            b["surface"], b["hover_card"],
            "".join(avatar(TEAM[n % len(TEAM)][0], n, "h-12 w-12 ring-2 ring-offset-2 ring-offset-transparent ring-white/10") for n in range(24)),
            b["text_muted"], b["btn_primary"], ic("arrow", "h-4 w-4"))
        feat = ["avatar wall", "24 avatars", "headline count", "careers CTA", "centered composition"]

    else:  # leadership
        body = '<div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">%s</div>' % "".join(
            ('<article class="%s %s p-6 text-center"><div class="mx-auto mb-4">%s</div>'
             '<h3 class="font-semibold">%s</h3><p class="text-sm %s">%s</p>'
             '<div class="mt-4 flex justify-center">%s</div></article>') % (
                b["surface"], b["hover_card"], avatar(name, n, "h-24 w-24 ring-2 ring-offset-4 ring-offset-transparent ring-white/15"), name, b["text_muted"], role, socials())
            for n, (name, role, bio) in enumerate(TEAM[:4]))
        feat = ["leadership row", "4 executives", "centered cards", "ringed avatars", "responsive 1/2/4-col"]

    code = section(h + body, style)
    desc = "%s team layout: %s." % (TOKENS[style]["title"].split(" (")[0], feat[0].capitalize())
    return dict(code=code, section_name=title, eyebrow="Team", features=feat,
                tags=["team", "people", "about", "profiles"] + [style], desc=desc, scope="team")
