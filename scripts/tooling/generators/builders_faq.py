"""FAQ section builders — 15 concepts."""
from .helpers import TOKENS, avatar, ic, ICONS, esc


def C(inner, max_w="max-w-5xl"):
    return '<div class="mx-auto %s px-5 sm:px-6 lg:px-8">\n%s\n</div>' % (max_w, inner)


def section(heading_block, body, style, scope_attr=None):
    attr = scope_attr or ('data-section="%s"' % style)
    b = TOKENS[style]
    return '<section class="relative w-full %s" %s>\n%s\n</section>' % (
        b["text"], attr, C(heading_block + body))


def head(eyebrow, eyebrow_icon, heading, subhead, style, align="center"):
    b = TOKENS[style]
    icn = (ic(eyebrow_icon, "h-3.5 w-3.5") + " ") if eyebrow_icon else ""
    badge = '<p class="mb-4"><span class="%s">%s%s</span></p>' % (b["badge"], icn, eyebrow) if eyebrow else ""
    align_cls = "text-center mx-auto" if align == "center" else ""
    sub = '<p class="mt-4 max-w-2xl %s text-base sm:text-lg leading-relaxed %s">%s</p>' % (
        align_cls, b["text_muted"], subhead) if subhead else ""
    return '<div class="mb-10 %s">%s<h2 class="f-disp text-3xl sm:text-4xl lg:text-5xl font-bold tracking-tight %s">%s</h2>%s</div>' % (
        align_cls, badge, align_cls, heading, sub)


QA = [
    ("How does the free trial work?", "You get 14 days of full access with no card required. Cancel anytime before it ends and you won't be charged."),
    ("Can I change plans later?", "Yes — upgrade or downgrade at any moment. Changes are prorated and applied on your next invoice."),
    ("Do you offer discounts for startups?", "We offer 50% off for early-stage startups under 10 employees, plus an open-source credit program."),
    ("Is my data secure?", "All data is encrypted in transit and at rest. We are SOC 2 Type II and GDPR compliant with audit logs."),
    ("What integrations are supported?", "Slack, GitHub, Linear, Notion, Zapier and 60+ more. A REST and GraphQL API is available on every plan."),
    ("How do I get support?", "Email, in-app chat, and a community forum. Paid plans include a dedicated success manager and 4-hour SLA."),
    ("Can I self-host?", "Enterprise customers can deploy on their own VPC. Contact sales for a self-hosted deployment package."),
    ("What is your refund policy?", "If you're not happy within 30 days, we refund 100% — no questions, no friction."),
]


def faq(style, i):
    b = TOKENS[style]
    concepts = [
        ("accordion", "Accordion FAQ"),
        ("two-col", "Two-Column FAQ"),
        ("search", "Searchable FAQ UI"),
        ("sidebar", "Sidebar Categories FAQ"),
        ("modern-cards", "Modern FAQ Cards"),
        ("pricing", "Pricing FAQ"),
        ("saas", "SaaS FAQ"),
        ("docs", "Documentation FAQ"),
        ("glass", "Glass FAQ" if style == "edge-glassmorphism" else "Spotlight FAQ"),
        ("brutalist", "Brutalist FAQ" if style == "neo-brutalism" else "Compact FAQ"),
        ("minimal", "Minimal FAQ"),
        ("categorized", "Categorized FAQ"),
        ("tabs", "Tabbed FAQ UI"),
        ("rich", "Rich Content FAQ"),
        ("contact-cta", "FAQ with Contact CTA"),
    ]
    key, title = concepts[i]
    h = head("FAQ", "help", "Frequently asked questions", "Everything you need to know about the product, billing, and onboarding.", style)

    def qrow(idx, qid=None):
        q, a = QA[idx % len(QA)]
        id_attr = ' id="q%d"' % qid if qid is not None else ""
        return (
            '<details class="group %s %s"' + id_attr + '><summary class="flex cursor-pointer items-center justify-between gap-4 p-5 font-semibold">'
            '<span>%s</span><svg class="h-5 w-5 shrink-0 transition-transform group-open:rotate-45" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg></summary>'
            '<div class="px-5 pb-5 text-sm leading-relaxed %s">%s</div></details>' % (
                b["surface"], b["hover_card"], q, b["text_muted"], a)
        )

    if key == "accordion":
        body = '<div class="space-y-3 max-w-3xl mx-auto">' + "".join(qrow(n) for n in range(6)) + '</div>'
        feat = ["native <details> accordion", "rotating plus icon", "no-JS expand", "keyboard focusable", "6 questions"]

    elif key == "two-col":
        half = 4
        col1 = "".join(qrow(n) for n in range(half))
        col2 = "".join(qrow(n + half) for n in range(half))
        body = '<div class="grid grid-cols-1 gap-4 md:grid-cols-2">%s%s</div>' % (col1, col2)
        feat = ["two-column layout", "8 questions", "responsive collapse", "native accordions", "balanced height"]

    elif key == "search":
        search = (
            '<div class="mb-6 max-w-xl mx-auto"><div class="relative"><span class="absolute left-4 top-1/2 -translate-y-1/2">%s</span>'
            '<input type="search" placeholder="Search questions..." aria-label="Search FAQ" class="%s pl-11">'
            '<kbd class="absolute right-3 top-1/2 -translate-y-1/2 %s hidden sm:inline-flex">⌘K</kbd></div></div>'
        ) % (ic("search", "h-4 w-4"), b["input"], b["badge"])
        body = search + '<div class="space-y-3 max-w-3xl mx-auto">' + "".join(qrow(n) for n in range(5)) + '</div>'
        feat = ["search bar (UI only)", "keyboard hint chip", "filtered-looking list", "native accordions", "centered search"]

    elif key == "sidebar":
        cats = ["Getting started", "Billing & plans", "Security", "Integrations", "API"]
        nav = "".join(
            '<li><a href="#" class="block rounded-lg px-3 py-2 text-sm font-medium %s %s">%s</a></li>' % (
                b["text_muted"] if n else b["text"], "bg-current/5" if not n else "", c)
            for n, c in enumerate(cats))
        body = (
            '<div class="grid grid-cols-1 gap-6 lg:grid-cols-[220px_1fr]">'
            '<aside class="%s p-4"><p class="mb-3 text-xs font-semibold uppercase tracking-wider %s">Categories</p><ul class="space-y-1">%s</ul></aside>'
            '<div class="space-y-3">%s</div></div>'
        ) % (b["surface_soft"], b["text_muted"], nav, "".join(qrow(n) for n in range(6)))
        feat = ["sidebar categories nav", "active state", "sticky-ish aside", "responsive stack", "scoped accordion list"]

    elif key == "modern-cards":
        cards = "".join(
            '<details class="group %s %s p-6"><summary class="flex cursor-pointer items-start justify-between gap-4">'
            '<span class="flex items-start gap-3"><span class="%s flex h-9 w-9 shrink-0 items-center justify-center">%s</span><span class="font-semibold">%s</span></span>'
            '<svg class="h-5 w-5 shrink-0 mt-0.5 transition-transform group-open:rotate-180" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg></summary>'
            '<p class="mt-4 pl-12 text-sm leading-relaxed %s">%s</p></details>' % (
                b["surface"], b["hover_card"], b["surface_soft"], ic(ICONS["help"], "h-4 w-4"), QA[n % len(QA)][0], b["text_muted"], QA[n % len(QA)][1])
            for n in range(6))
        body = '<div class="grid grid-cols-1 gap-4 sm:grid-cols-2">%s</div>' % cards
        feat = ["card-style accordions", "iconized questions", "chevron rotation", "2-column grid", "hover lift"]

    elif key == "pricing":
        body = (
            '<div class="grid grid-cols-1 gap-6 lg:grid-cols-[1fr_1.4fr]">'
            '<aside class="%s p-7"><span class="%s mb-3 inline-flex">%s Pricing</span><h3 class="f-disp text-xl font-bold">Billing questions</h3>'
            '<p class="mt-3 text-sm %s">Everything about plans, refunds, and invoices.</p>'
            '<a href="#" class="mt-6 inline-flex items-center gap-2 %s">View pricing %s</a></aside>'
            '<div class="space-y-3">%s</div></div>'
        ) % (b["surface"], b["badge"], ic("credit", "h-3.5 w-3.5"), b["text_muted"], b["btn_secondary"], ic("arrow", "h-4 w-4"), "".join(qrow(n) for n in range(5)))
        feat = ["pricing-specific FAQ", "split intro panel", "CTA to pricing", "scoped accordion list", "responsive split"]

    elif key == "saas":
        feat = ["SaaS feature FAQ grid", "3-column cards", "iconized categories", "disclosure answers", "responsive collapse"]
        cards = ""
        for icn, q, a in [("rocket", "Quick start", "Install our CLI and run one command to scaffold your first project."), ("shield", "Security", "Enterprise-grade encryption, SSO, and audit logs on every workspace."), ("trend", "Analytics", "Real-time dashboards and weekly summaries delivered to your inbox."), ("code", "Developer API", "A typed SDK and GraphQL endpoint with 99.99% uptime SLA."), ("bolt", "Performance", "Sub-50ms response globally via edge compute and smart caching."), ("headset", "Support", "Email, chat, and a dedicated CSM on Business and Enterprise.")]:
            cards += (
                '<div class="' + b["surface"] + ' ' + b["hover_card"] + ' p-6">'
                '<div class="mb-4 flex h-10 w-10 items-center justify-center ' + b["surface_soft"] + '">' + ic(icn, "h-5 w-5") + '</div>'
                '<h3 class="font-semibold">' + q + '</h3>'
                '<details class="group mt-3"><summary class="cursor-pointer text-sm ' + b["text_muted"] + ' font-medium">Show answer</summary>'
                '<p class="mt-2 text-sm leading-relaxed ' + b["text_muted"] + '">' + a + '</p></details></div>'
            )
        body = '<div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">' + cards + '</div>'

    elif key == "docs":
        body = (
            '<div class="grid grid-cols-1 gap-6 lg:grid-cols-[260px_1fr]">'
            '<nav class="%s p-4"><p class="mb-3 text-xs font-semibold uppercase tracking-wider %s">On this page</p><ul class="space-y-1 text-sm">%s</ul></nav>'
            '<div class="space-y-3">%s</div></div>'
        ) % (b["surface_soft"], b["text_muted"],
             "".join('<li><a href="#q%d" class="block rounded px-2 py-1.5 %s hover:bg-current/5">%.2d. %s</a></li>' % (
                 n, b["text_muted"] if n else "", n, QA[n % len(QA)][0][:24]) for n in range(6)),
             "".join(qrow(n, qid=n) for n in range(6)))
        feat = ["docs-style anchor nav", "table of contents", "numbered questions", "scoped accordions", "responsive stack"]

    elif key == "glass":
        items = "".join(
            '<details class="group %s p-5"><summary class="flex cursor-pointer items-center justify-between gap-4"><span class="font-medium">%s</span>'
            '<span class="flex h-6 w-6 items-center justify-center rounded-full %s text-sm">+</span></summary>'
            '<p class="mt-3 text-sm leading-relaxed %s">%s</p></details>' % (
                b["surface_soft"], QA[n % len(QA)][0], b["surface"], b["text_muted"], QA[n % len(QA)][1])
            for n in range(6))
        body = '<div class="space-y-3 max-w-3xl mx-auto">%s</div>' % items
        feat = ["spotlight accordion", "plus badge toggle", "centered column", "soft panels", "native disclosure"]

    elif key == "brutalist":
        body = '<div class="space-y-0 max-w-3xl mx-auto %s">' % b["surface"] + "".join(
            '<details class="group border-b border-current/10 last:border-0"><summary class="flex cursor-pointer items-center justify-between gap-4 px-5 py-4 font-bold"><span>%s</span>'
            '<span class="f-mono text-sm">%s</span></summary><p class="px-5 pb-5 text-sm %s">%s</p></details>' % (
                QA[n % len(QA)][0], "[+]" if style == "neo-brutalism" else "+", b["text_muted"], QA[n % len(QA)][1])
            for n in range(7)) + '</div>'
        feat = ["single-panel list", "divided rows", "monospace toggle", "compact density", "edge-to-edge rules"]

    elif key == "minimal":
        body = '<dl class="divide-y divide-current/10 max-w-3xl mx-auto">' + "".join(
            '<div class="py-5"><dt class="font-semibold">%s</dt><dd class="mt-2 text-sm leading-relaxed %s">%s</dd></div>' % (
                QA[n % len(QA)][0], b["text_muted"], QA[n % len(QA)][1])
            for n in range(6)) + '</dl>'
        feat = ["static definition list", "no interactivity", "hairline dividers", "typographic rhythm", "max readability"]

    elif key == "categorized":
        sections_data = [("Getting started", ["rocket", "bolt"]), ("Billing", ["credit", "shield"]), ("Support", ["headset", "chat"])]
        body = '<div class="space-y-10">' + "".join(
            '<div><div class="mb-4 flex items-center gap-2">%s<h3 class="text-lg font-bold">%s</h3></div><div class="space-y-3">%s</div></div>' % (
                '<span class="%s flex h-8 w-8 items-center justify-center">%s</span>' % (b["surface_soft"], ic(cats[0], "h-4 w-4")) if cats else "", title,
                "".join(qrow(n) for n in range(3)))
            for title, cats in sections_data) + '</div>'
        feat = ["grouped by category", "sectioned accordions", "icon headers", "vertical rhythm", "responsive stack"]

    elif key == "tabs":
        tabs = ["General", "Billing", "Security", "API"]
        tabbar = '<div class="mb-6 flex flex-wrap gap-2 border-b border-current/10 pb-px">' + "".join(
            '<button type="button" class="%s px-4 py-2 text-sm font-medium %s" aria-selected="%s" role="tab">%s</button>' % (
                b["surface_soft"] if n == 0 else "", b["text"] if n == 0 else b["text_muted"], "true" if n == 0 else "false", t)
            for n, t in enumerate(tabs)) + '</div>'
        body = tabbar + '<div class="space-y-3 max-w-3xl mx-auto">' + "".join(qrow(n) for n in range(5)) + '</div>'
        feat = ["tabbed categories (UI)", "active tab state", "role=tab a11y", "tablist nav", "responsive wrap"]

    elif key == "rich":
        body = '<div class="space-y-3 max-w-3xl mx-auto">' + "".join(
            '<details class="group %s %s"><summary class="flex cursor-pointer items-center justify-between gap-4 p-5"><span class="font-semibold">%s</span>'
            '<svg class="h-5 w-5 shrink-0 transition-transform group-open:rotate-180" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg></summary>'
            '<div class="px-5 pb-5"><p class="text-sm leading-relaxed %s">%s</p>'
            '<div class="mt-4 flex flex-wrap items-center gap-2">%s%s</div></div></details>' % (
                b["surface"], b["hover_card"], QA[n % len(QA)][0], b["text_muted"], QA[n % len(QA)][1],
                '<span class="%s">%s %s</span>' % (b["badge"], ic("link", "h-3 w-3"), "Related doc"),
                '<span class="%s">%s %s</span>' % (b["badge"], ic("video", "h-3 w-3"), "Watch"))
            for n in range(5)) + '</div>'
        feat = ["rich answer rows", "related-doc chip", "video chip", "chevron rotation", "scoped accordions"]

    else:  # contact-cta
        body = (
            '<div class="grid grid-cols-1 gap-6 lg:grid-cols-[1.3fr_1fr]">'
            '<div class="space-y-3">%s</div>'
            '<aside class="%s p-7 text-center"><div class="mx-auto mb-4 flex h-12 w-12 items-center justify-center %s">%s</div>'
            '<h3 class="f-disp text-xl font-bold">Still have questions?</h3><p class="mt-2 text-sm %s">Our team replies in under 2 hours on weekdays.</p>'
            '<a href="#" class="mt-5 inline-flex items-center gap-2 %s">%s Contact support</a></aside></div>'
        ) % ("".join(qrow(n) for n in range(4)), b["surface"], b["surface_soft"], ic("headset", "h-5 w-5"), b["text_muted"], b["btn_primary"], ic("mail", "h-4 w-4"))
        feat = ["FAQ + contact CTA", "split aside panel", "support escalation", "scoped accordions", "responsive split"]

    code = section(h, body, style)
    desc = "%s FAQ layout: %s." % (TOKENS[style]["title"].split(" (")[0], feat[0].capitalize())
    return dict(code=code, section_name=title, eyebrow="FAQ", features=feat,
                tags=["faq", "accordion", "questions"] + [style], desc=desc, scope="faq")
