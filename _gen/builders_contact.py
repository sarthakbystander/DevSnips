"""Contact section builders — 15 concepts."""
from .helpers import TOKENS, avatar, ic, ICONS, fill
from .layout import head, section


def contact(style, i):
    b = TOKENS[style]
    concepts = [
        ("split", "Split Contact Layout"),
        ("map", "Contact with Map"),
        ("cards", "Contact Method Cards"),
        ("team", "Team Contact Directory"),
        ("support", "Support Center"),
        ("offices", "Office Locations"),
        ("minimal-form", "Minimal Contact Form"),
        ("startup", "Startup Contact"),
        ("dark", "Dark Premium Contact" if style == "dark-premium" else "Centered Contact"),
        ("glass", "Glass Contact" if style == "edge-glassmorphism" else "Floating Contact"),
        ("mega", "Mega Contact Grid"),
        ("sidebar", "Contact + Sidebar Info"),
        ("inline", "Inline Contact Cards"),
        ("onboarding", "Onboarding Contact"),
        ("newsletter-contact", "Contact + Subscribe"),
    ]
    key, title = concepts[i]
    h = head("Contact", "mail", "Let's talk", "Reach out and our team will reply within one business day.", style)

    def field(label, name, typ="text", ph=""):
        return ('<div><label class="mb-1.5 block text-sm font-medium %s" for="%s">%s</label>'
                '<input id="%s" name="%s" type="%s" placeholder="%s" class="%s"></div>') % (
            b["text_muted"], name, label, name, name, typ, ph, b["input"])

    if key == "split":
        form = (
            '<form class="space-y-4">%s%s%s<div><label class="mb-1.5 block text-sm font-medium %s" for="msg">Message</label>'
            '<textarea id="msg" name="msg" rows="5" placeholder="Tell us a bit about your project..." class="%s"></textarea></div>'
            '<button type="submit" class="%s w-full justify-center">Send message %s</button></form>'
        ) % (field("Full name", "name", "text", "Jane Doe"), field("Email", "email", "email", "jane@company.com"),
             field("Company", "company", "text", "Acme Inc."), b["text_muted"], b["input"], b["btn_primary"], ic("send", "h-4 w-4"))
        info = (
            '<div class="space-y-5"><div class="flex items-start gap-3">%s<div><p class="font-semibold">Email us</p>'
            '<a href="mailto:hello@company.com" class="text-sm %s">hello@company.com</a></div></div>'
            '<div class="flex items-start gap-3">%s<div><p class="font-semibold">Call us</p>'
            '<a href="tel:+15551234567" class="text-sm %s">+1 (555) 123-4567</a></div></div>'
            '<div class="flex items-start gap-3">%s<div><p class="font-semibold">Visit us</p>'
            '<p class="text-sm %s">548 Market Street, San Francisco, CA</p></div></div></div>'
        ) % (ic("mail", "h-5 w-5"), b["text_muted"], ic("phone", "h-5 w-5"), b["text_muted"], ic("pin", "h-5 w-5"), b["text_muted"])
        body = ('<div class="grid grid-cols-1 gap-8 lg:grid-cols-2"><div class="%s p-8">%s</div>'
                '<div class="p-2 lg:p-4">%s</div></div>') % (b["surface"], form, info)
        feat = ["split form + info", "email/phone/address", "accessible labels", "submit CTA", "responsive 2-col"]

    elif key == "map":
        form = '<form class="space-y-4">%s%s<button type="submit" class="%s w-full justify-center">Send message</button></form>' % (
            field("Name", "name"), field("Email", "email", "email"), b["btn_primary"])
        info = ('<div class="space-y-3"><div class="flex items-center gap-3">%s<div><p class="text-sm font-semibold">Headquarters</p>'
                '<p class="text-sm %s">548 Market St, SF, CA 94104</p></div></div>'
                '<div class="flex items-center gap-3">%s<div><p class="text-sm font-semibold">Hours</p>'
                '<p class="text-sm %s">Mon–Fri, 9am–6pm PT</p></div></div></div>') % (
            ic("pin", "h-5 w-5"), b["text_muted"], ic("clock", "h-5 w-5"), b["text_muted"])
        body = ('<div class="grid grid-cols-1 gap-6 lg:grid-cols-2">'
                '<div class="%s overflow-hidden"><div class="relative h-64 lg:h-full min-h-[280px] %s" aria-label="Map placeholder">'
                '<div class="absolute inset-0 opacity-30" style="background-image:linear-gradient(0deg,#%s11 1px,transparent 1px),linear-gradient(90deg,#%s11 1px,transparent 1px);background-size:28px 28px"></div>'
                '<div class="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2"><div class="flex h-12 w-12 items-center justify-center rounded-full %s">%s</div>'
                '<p class="mt-2 text-center text-xs %s">You are here</p></div></div></div>'
                '<div class="space-y-6"><div class="%s p-6">%s</div>%s</div></div>') % (
            b["surface"], b["surface_soft"], b["accent"].lstrip("#"), b["accent"].lstrip("#"), b["btn_primary"], ic("pin", "h-6 w-6"), b["text_muted"], b["surface"], form, info)
        feat = ["map placeholder panel", "grid overlay", "you-are-here pin", "contact form", "location + hours"]

    elif key == "cards":
        cards = "".join(
            '<a href="#" class="%s %s p-6 text-center"><div class="mx-auto mb-4 flex h-12 w-12 items-center justify-center %s">%s</div>'
            '<h3 class="font-semibold">%s</h3><p class="mt-1 text-sm %s">%s</p></a>' % (
                b["surface"], b["hover_card"], b["surface_soft"], ic(icn, "h-6 w-6"), titlec, b["text_muted"], desc)
            for icn, titlec, desc in [("mail", "Email", "Replies within 1 business day"), ("chat", "Live chat", "Mon–Fri 9am–6pm PT"), ("phone", "Phone", "+1 555 123 4567"), ("headset", "Support center", "Browse 200+ articles")])
        body = '<div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">%s</div>' % cards
        feat = ["contact method cards", "4 channels", "iconified", "hover lift", "responsive 1/2/4-col"]

    elif key == "team":
        team = [("Maya Chen", "Sales", "maya@", "phone"), ("Daniel Reyes", "Support", "daniel@", "chat"), ("Aisha Karim", "Partnerships", "aisha@", "globe"), ("Tom Bradley", "Press", "tom@", "mail")]
        cards = "".join(
            '<article class="%s %s p-5"><div class="flex items-center gap-3">%s<div><p class="font-semibold">%s</p>'
            '<p class="text-xs %s">%s</p></div></div><a href="#" class="mt-4 inline-flex items-center gap-2 text-sm %s">%s %s</a></article>' % (
                b["surface"], b["hover_card"], avatar(name, n), name, b["text_muted"], role, b["text_muted"], ic(icn, "h-4 w-4"), email + "company.com")
            for n, (name, role, email, icn) in enumerate(team))
        body = '<div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">%s</div>' % cards
        feat = ["team contact directory", "role-tagged profiles", "direct emails", "4 contacts", "responsive grid"]

    elif key == "support":
        cards = "".join(
            '<a href="#" class="%s %s p-6"><div class="flex items-start justify-between"><div class="flex h-11 w-11 items-center justify-center %s">%s</div>%s</div>'
            '<h3 class="mt-4 font-semibold">%s</h3><p class="mt-1 text-sm %s">%s</p></a>' % (
                b["surface"], b["hover_card"], b["surface_soft"], ic(icn, "h-5 w-5"), ic("arrow", "h-4 w-4"), titlec, b["text_muted"], desc)
            for icn, titlec, desc in [("doc", "Documentation", "Guides, API reference, and tutorials"), ["help", "Community", "Ask and answer with other users"], ["chat", "Live chat", "Talk to support in real time"], ["video", "Video walkthroughs", "Watch step-by-step demos"], ["headset", "Contact support", "Open a ticket with our team"], ["shield-check", "Status page", "Live system status and incidents"]][:6])
        body = '<div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">%s</div>' % cards
        feat = ["support center grid", "6 channels", "arrow indicators", "iconified cards", "responsive 1/2/3-col"]

    elif key == "offices":
        offices = [("San Francisco", "548 Market St", "USA", "HQ", "10:00"), ("London", "1 Finsbury Avenue", "UK", "EMEA", "02:00"), ("Singapore", "8 Marina Blvd", "SG", "APAC", "06:00")]
        cards = "".join(
            '<article class="%s %s p-6"><div class="flex items-center justify-between"><div class="flex h-11 w-11 items-center justify-center %s">%s</div>'
            '<span class="%s">%s</span></div><h3 class="mt-4 font-semibold">%s</h3><p class="text-sm %s">%s, %s</p>'
            '<p class="mt-3 text-xs %s">Local time %s:00</p></article>' % (
                b["surface"], b["hover_card"], b["surface_soft"], ic("building", "h-5 w-5"), b["badge"], region, city, b["text_muted"], addr, country, b["text_muted"], t)
            for city, addr, country, region, t in offices)
        body = '<div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">%s</div>' % cards
        feat = ["office location cards", "regional badges", "local time display", "3 regions", "responsive grid"]

    elif key == "minimal-form":
        form = ('<form class="mx-auto max-w-2xl space-y-4">%s%s<textarea rows="4" placeholder="How can we help?" class="%s" aria-label="Message"></textarea>'
                '<button type="submit" class="%s w-full justify-center">Send %s</button></form>') % (
            field("Name", "name"), field("Email", "email", "email"), b["input"], b["btn_primary"], ic("send", "h-4 w-4"))
        body = '<div class="text-center">%s</div>' % form
        feat = ["minimal centered form", "aligned content width", "3 fields", "accessible", "single CTA"]

    elif key == "startup":
        form = ('<form class="space-y-4">%s<div class="grid grid-cols-2 gap-4">%s%s</div>%s<button type="submit" class="%s w-full justify-center">%s Start the conversation</button></form>') % (
            field("Full name", "name"), field("Work email", "email", "email"), field("Company", "company"), field("What do you need?", "need", "text", "A demo of your product"), b["btn_primary"], ic("rocket", "h-4 w-4"))
        aside = ('<div class="%s p-6"><p class="text-sm %s">Prefer email?</p>'
                 '<a href="mailto:hi@startup.dev" class="font-semibold">hi@startup.dev</a>'
                 '<div class="mt-5 flex gap-2">%s</div></div>') % (b["surface_soft"], b["text_muted"], "".join(
                     '<a href="#" class="%s" aria-label="%s">%s</a>' % (b["chip"], s, ic(s, "h-4 w-4")) for s in ["twitter", "github", "linkedin"]))
        body = '<div class="grid grid-cols-1 gap-6 lg:grid-cols-[1.4fr_1fr]"><div class="%s p-8">%s</div>%s</div>' % (b["surface"], form, aside)
        feat = ["startup contact form", "social aside", "2-col field grid", "single CTA", "responsive split"]

    elif key == "dark":
        form = ('<form class="space-y-4">%s<textarea rows="4" placeholder="Your message" class="%s" aria-label="Message"></textarea>'
                '<button type="submit" class="%s w-full justify-center">%s Send message</button></form>') % (
            field("Email", "email", "email", "you@company.com"), b["input"], b["btn_primary"], ic("send", "h-4 w-4"))
        body = ('<div class="mx-auto max-w-2xl"><div class="%s p-8 sm:p-10">%s</div>'
                '<p class="mt-4 text-center text-sm %s">Or email us directly at <a href="mailto:hello@company.com" class="font-semibold">hello@company.com</a></p></div>') % (
            b["surface"], form, b["text_muted"])
        feat = ["centered hero form", "single email field", "direct email fallback", "max-width panel", "submit CTA"]

    elif key == "glass":
        form = ('<form class="space-y-4">%s%s<textarea rows="4" placeholder="Message" class="%s" aria-label="Message"></textarea>'
                '<button type="submit" class="%s w-full justify-center">%s Send</button></form>') % (
            field("Name", "name"), field("Email", "email", "email"), b["input"], b["btn_primary"], ic("send", "h-4 w-4"))
        body = ('<div class="grid grid-cols-1 gap-6 lg:grid-cols-3">'
                '<div class="lg:col-span-2 %s p-8">%s</div>'
                '<aside class="%s p-6"><h3 class="font-semibold">Reach us</h3>'
                '<ul class="mt-4 space-y-3 text-sm %s"><li class="flex items-center gap-2">%s hello@company.com</li>'
                '<li class="flex items-center gap-2">%s +1 555 123 4567</li>'
                '<li class="flex items-center gap-2">%s San Francisco, CA</li></ul></aside></div>') % (
            b["surface"], form, b["surface_soft"], b["text_muted"], ic("mail", "h-4 w-4"), ic("phone", "h-4 w-4"), ic("pin", "h-4 w-4"))
        feat = ["floating contact panel", "2/3 + 1/3 split", "contact aside list", "3 fields", "responsive stack"]

    elif key == "mega":
        channels = "".join(
            '<a href="#" class="%s %s p-5 flex items-center gap-3">%s<div><p class="text-sm font-semibold">%s</p><p class="text-xs %s">%s</p></div></a>' % (
                b["surface"], b["hover_card"], ic(icn, "h-5 w-5") if False else '<span class="%s flex h-10 w-10 items-center justify-center">%s</span>' % (b["surface_soft"], ic(icn, "h-5 w-5")), t, b["text_muted"], d)
            for icn, t, d in [("mail", "Email", "hello@company.com"), ("phone", "Phone", "+1 555 123 4567"), ("chat", "Live chat", "9am–6pm PT"), ("headset", "Support", "24/7 tickets")])
        form = ('<form class="space-y-4">%s%s<textarea rows="4" placeholder="Message" class="%s" aria-label="Message"></textarea>'
                '<button type="submit" class="%s w-full justify-center">Send message %s</button></form>') % (
            field("Name", "name"), field("Email", "email", "email"), b["input"], b["btn_primary"], ic("send", "h-4 w-4"))
        body = ('<div class="grid grid-cols-1 gap-6 lg:grid-cols-2"><div class="grid grid-cols-1 gap-4 sm:grid-cols-2">%s</div>'
                '<div class="%s p-8">%s</div></div>') % (channels, b["surface"], form)
        feat = ["mega contact grid", "4 channel cards", "side form", "2-col layout", "responsive collapse"]

    elif key == "sidebar":
        form = ('<form class="space-y-4">%s%s%s<textarea rows="4" placeholder="Message" class="%s" aria-label="Message"></textarea>'
                '<button type="submit" class="%s w-full justify-center">Send %s</button></form>') % (
            field("Name", "name"), field("Email", "email", "email"), field("Subject", "subject"), b["input"], b["btn_primary"], ic("send", "h-4 w-4"))
        sidebar = ('<aside class="%s p-6 space-y-5"><div><p class="text-xs font-semibold uppercase tracking-wider %s">Response time</p>'
                   '<p class="mt-1 text-sm">Under 2 hours on weekdays</p></div>'
                   '<div><p class="text-xs font-semibold uppercase tracking-wider %s">Office</p>'
                   '<p class="mt-1 text-sm">548 Market St, San Francisco</p></div>'
                   '<div><p class="text-xs font-semibold uppercase tracking-wider %s">Follow</p>'
                   '<div class="mt-2 flex gap-2">%s</div></div></aside>') % (
            b["surface_soft"], b["text_muted"], b["text_muted"], b["text_muted"], "".join(
                '<a href="#" class="%s" aria-label="%s">%s</a>' % (b["chip"], s, ic(s, "h-4 w-4")) for s in ["twitter", "github", "linkedin"]))
        body = '<div class="grid grid-cols-1 gap-6 lg:grid-cols-[1fr_280px]"><div class="%s p-8">%s</div>%s</div>' % (b["surface"], form, sidebar)
        feat = ["form + sidebar info", "response time + office", "social follow", "1fr+280px split", "responsive stack"]

    elif key == "inline":
        rows = "".join(
            '<li class="flex items-center gap-3 %s p-4"><span class="flex h-10 w-10 items-center justify-center %s">%s</span>'
            '<div class="flex-1"><p class="text-sm font-semibold">%s</p><p class="text-sm %s">%s</p></div>'
            '<a href="#" class="%s">Contact</a></li>' % (
                b["surface"], b["surface_soft"], ic(icn, "h-5 w-5"), t, b["text_muted"], d, b["btn_secondary"])
            for icn, t, d in [("mail", "Email", "hello@company.com"), ("phone", "Phone", "+1 555 123 4567"), ("chat", "Live chat", "Weekdays 9–6 PT")])
        body = '<ul class="mx-auto max-w-3xl space-y-3">%s</ul>' % rows
        feat = ["inline contact rows", "list-based layout", "per-row CTA", "narrow max width", "responsive"]

    elif key == "onboarding":
        steps = [("1", "Tell us about your team", "Size, stack, and goals"), ("2", "Book a kickoff call", "30 minutes with a solutions engineer"), ("3", "Start your trial", "14 days, full access, no card")]
        cards = "".join(
            '<div class="%s %s p-6"><div class="mb-3 flex h-10 w-10 items-center justify-center %s font-bold">%s</div>'
            '<h3 class="font-semibold">%s</h3><p class="mt-1 text-sm %s">%s</p></div>' % (
                b["surface"], b["hover_card"], b["surface_soft"], num, t, b["text_muted"], d)
            for num, t, d in steps)
        cta = ('<div class="%s p-6 text-center"><h3 class="f-disp text-lg font-bold">Ready to begin?</h3>'
               '<p class="mt-1 text-sm %s">We onboard teams in under a week.</p>'
               '<a href="#" class="mt-4 inline-flex items-center gap-2 %s">%s Get started</a></div>') % (
            b["surface_soft"], b["text_muted"], b["btn_primary"], ic("arrow", "h-4 w-4"))
        body = '<div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">%s%s</div>' % (cards, cta)
        feat = ["onboarding steps", "numbered cards", "final CTA tile", "4-col bento", "responsive"]

    else:  # newsletter-contact
        form = ('<form class="space-y-4">%s<textarea rows="3" placeholder="Message" class="%s" aria-label="Message"></textarea>'
                '<button type="submit" class="%s w-full justify-center">%s Send</button></form>') % (
            field("Email", "email", "email"), b["input"], b["btn_primary"], ic("send", "h-4 w-4"))
        subscribe = ('<div class="%s p-6"><div class="flex items-center gap-2 mb-2">%s<h3 class="font-semibold">Get product updates</h3></div>'
                     '<p class="text-sm %s">Monthly newsletter. No spam, unsubscribe anytime.</p>'
                     '<form class="mt-4 flex gap-2"><input type="email" placeholder="you@email.com" class="%s flex-1" aria-label="Email">'
                     '<button type="submit" class="%s">Subscribe</button></form></div>') % (
            b["surface_soft"], ic("bell", "h-5 w-5"), b["text_muted"], b["input"], b["btn_secondary"])
        body = '<div class="grid grid-cols-1 gap-6 lg:grid-cols-2"><div class="%s p-8">%s</div>%s</div>' % (b["surface"], form, subscribe)
        feat = ["contact + newsletter combo", "dual forms", "subscribe aside", "responsive split", "two CTAs"]

    code = section(h + body, style)
    desc = "%s contact layout: %s." % (TOKENS[style]["title"].split(" (")[0], feat[0].capitalize())
    return dict(code=code, section_name=title, eyebrow="Contact", features=feat,
                tags=["contact", "form", "get-in-touch"] + [style], desc=desc, scope="contact")
