"""404 section builders — 15 concepts."""
from .helpers import TOKENS, ic, ICONS, logo_svg
from .layout import head, section


def error_page(style, i):
    b = TOKENS[style]
    concepts = [
        ("minimal", "Minimal 404"),
        ("funny", "Funny 404"),
        ("dark", "Dark 404" if style in ("dark-premium", "vercel") else "Moody 404"),
        ("brutalist", "Brutalist 404" if style == "neo-brutalism" else "Bold 404"),
        ("glass", "Glass 404" if style == "edge-glassmorphism" else "Spotlight 404"),
        ("space", "Space Theme 404"),
        ("developer", "Developer Theme 404"),
        ("terminal", "Terminal 404"),
        ("illustration", "Illustration 404"),
        ("premium-saas", "Premium SaaS 404"),
        ("dashboard", "Dashboard 404"),
        ("retro", "Retro 404"),
        ("gradient", "Gradient 404"),
        ("abstract", "Abstract 404"),
        ("vercel", "Vercel-Inspired 404"),
    ]
    key, title = concepts[i]

    def actions():
        return ('<div class="mt-8 flex flex-col sm:flex-row gap-3 justify-center">'
                '<a href="/" class="%s inline-flex items-center justify-center gap-2">%s Back home</a>'
                '<a href="#" class="%s inline-flex items-center justify-center gap-2">%s Search</a></div>') % (
            b["btn_primary"], ic("home", "h-4 w-4"), b["btn_secondary"], ic("search", "h-4 w-4"))

    if key == "minimal":
        body = ('<div class="text-center"><p class="f-disp text-7xl sm:text-9xl font-bold tracking-tight">404</p>'
                '<p class="mt-4 text-lg %s">This page could not be found.</p>'
                '<p class="mt-2 text-sm %s">The page you are looking for may have moved or been removed.</p>%s</div>') % (
            b["text_muted"], b["text_muted"], actions())
        feat = ["minimal 404", "oversized numeral", "centered", "dual CTA", "low chrome"]

    elif key == "funny":
        body = ('<div class="text-center"><div class="mx-auto mb-6 flex h-20 w-20 items-center justify-center %s">%s</div>'
                '<h1 class="f-disp text-5xl sm:text-7xl font-bold">Oops!</h1>'
                '<p class="mt-4 text-lg">Looks like this page took the day off.</p>'
                '<p class="mt-2 text-sm %s">Error 404: Page on vacation. Please try another.</p>%s</div>') % (
            b["surface_soft"], ic("ghost", "h-10 w-10"), b["text_muted"], actions())
        feat = ["funny 404", "ghost icon", "playful copy", "dual CTA", "centered"]

    elif key == "dark":
        body = ('<div class="text-center relative">'
                '<div class="absolute inset-0 -z-10 opacity-40" style="background:radial-gradient(circle at 50%% 30%%,%s,transparent 60%%)" aria-hidden="true"></div>'
                '<p class="f-disp text-8xl sm:text-[10rem] font-bold leading-none" style="color:%s">404</p>'
                '<h1 class="mt-4 f-disp text-2xl font-bold">Lost in the dark</h1>'
                '<p class="mt-2 text-sm %s max-w-md mx-auto">The page you are after has vanished into the void.</p>%s</div>') % (
            b["accent"].lstrip("#"), b["accent"], b["text_muted"], actions())
        feat = ["moody 404", "accent glow", "oversized numeral", "dark hero", "dual CTA"]

    elif key == "brutalist":
        body = ('<div class="text-center"><div class="inline-block %s px-6 py-8 nb-shadow" style="transform:rotate(-2deg)">'
                '<p class="f-disp text-7xl sm:text-9xl font-black">404</p></div>'
                '<h1 class="mt-6 f-mono text-sm font-bold uppercase tracking-wider">Page not found</h1>'
                '<p class="mt-2 text-sm %s">This is not the page you are looking for.</p>%s</div>') % (
            b["surface"], b["text_muted"], actions())
        feat = ["brutalist 404", "rotated panel", "hard shadow", "mono label", "dual CTA"]

    elif key == "glass":
        body = ('<div class="%s %s p-8 sm:p-12 text-center relative overflow-hidden max-w-xl mx-auto">'
                '<div class="absolute inset-0 opacity-30" style="background:radial-gradient(circle at 50%% 0%%,%s,transparent 60%%)" aria-hidden="true"></div>'
                '<div class="relative z-10"><div class="mx-auto mb-4 flex h-14 w-14 items-center justify-center %s">%s</div>'
                '<p class="f-disp text-6xl sm:text-7xl font-bold">404</p>'
                '<p class="mt-3 text-sm %s">This page drifted off the map.</p>%s</div></div>') % (
            b["surface"], b["hover_card"], b["accent"].lstrip("#"), b["surface_soft"], ic("compass", "h-7 w-7"), b["text_muted"], actions())
        feat = ["spotlight 404", "glass panel", "radial glow", "compass icon", "dual CTA"]

    elif key == "space":
        body = ('<div class="text-center relative py-8">'
                '<div class="absolute inset-0 -z-10" aria-hidden="true">%s</div>'
                '<div class="relative"><div class="mx-auto mb-6 flex h-20 w-20 items-center justify-center">%s</div>'
                '<p class="f-disp text-7xl sm:text-9xl font-bold" style="text-shadow:0 0 40px %s">404</p>'
                '<h1 class="mt-4 f-disp text-2xl font-bold">Lost in space</h1>'
                '<p class="mt-2 text-sm %s max-w-md mx-auto">Houston, we cannot find the page you requested.</p>%s</div></div>') % (
            '<div class="absolute inset-0" style="background-image:radial-gradient(2px 2px at 20% 30%, #fff, transparent),radial-gradient(1px 1px at 60% 70%, #fff, transparent),radial-gradient(1px 1px at 80% 20%, #fff, transparent),radial-gradient(2px 2px at 40% 80%, #fff, transparent);opacity:0.5"></div>',
            '<span class="flex h-16 w-16 items-center justify-center rounded-full %s">%s</span>' % (b["surface_soft"], ic("satellite", "h-8 w-8")),
            b["accent"], b["text_muted"], actions())
        feat = ["space theme 404", "starfield bg", "satellite icon", "glowing numeral", "dual CTA"]

    elif key == "developer":
        body = ('<div class="max-w-2xl mx-auto"><div class="%s overflow-hidden">'
                '<div class="flex items-center gap-2 border-b border-current/10 px-4 py-3">%s%s'
                '<span class="ml-auto %s">404.sh</span></div>'
                '<div class="p-6 font-mono text-sm space-y-2">'
                '<p class="%s">$ curl <span class="font-semibold">https://yoursite.com/missing</span></p>'
                '<p>status: <span style="color:%s">404</span> Not Found</p>'
                '<p>message: The requested resource does not exist.</p>'
                '<p class="%s">hint: Check the URL or return to safety.</p>'
                '<p class="pt-2">$ <span class="inline-block w-2 h-4 align-middle" style="background:%s;animation:blink 1s steps(1) infinite"></span></p></div></div>'
                '<div class="mt-6">%s</div>'
                '<style>@keyframes blink{50%%{opacity:0}}</style></div>') % (
            b["surface"], "".join('<span class="h-2.5 w-2.5 rounded-full" style="background:currentColor;opacity:0.3"></span>' for _ in range(3)),
            '<span class="ml-2 %s">developer</span>' % b["text_muted"], b["text_muted"], b["text_muted"], b["accent"], b["text_muted"], b["accent"], actions())
        feat = ["developer 404", "terminal window", "shell output", "blinking cursor", "dual CTA"]

    elif key == "terminal":
        body = ('<div class="max-w-xl mx-auto %s p-6" style="font-family:monospace">'
                '<p class="text-sm"><span style="color:%s">user@host</span>:<span class="%s">~</span>$ ls /pages/</p>'
                '<p class="mt-2 text-sm %s">ls: cannot access \'/pages/missing\': No such file or directory</p>'
                '<p class="mt-2 text-sm"><span style="color:%s">user@host</span>:<span class="%s">~</span>$ <span class="inline-block w-2 h-4 align-middle" style="background:%s;animation:blink 1s steps(1) infinite"></span></p>'
                '<p class="mt-6 f-disp text-4xl font-bold" style="font-family:%s">404</p>'
                '<p class="mt-2 text-sm %s">exit code 404 — page not found</p>'
                '<div class="mt-6">%s</div>'
                '<style>@keyframes blink{50%%{opacity:0}}</style></div>') % (
            b["surface"], b["accent"], b["text_muted"], b["text_muted"], b["accent"], b["text_muted"], b["accent"], b["font_mono"], b["text_muted"], actions())
        feat = ["terminal 404", "pure mono layout", "shell prompt", "blinking cursor", "dual CTA"]

    elif key == "illustration":
        body = ('<div class="text-center"><div class="mx-auto mb-8 relative h-40 w-40">'
                '<svg viewBox="0 0 200 200" class="h-full w-full" aria-hidden="true">'
                '<circle cx="100" cy="100" r="60" fill="none" stroke="currentColor" stroke-width="2" stroke-dasharray="6 6" opacity="0.4"/>'
                '<circle cx="100" cy="100" r="30" fill="none" stroke="currentColor" stroke-width="2"/>'
                '<path d="M70 100h60M100 70v60" stroke="currentColor" stroke-width="2"/>'
                '<circle cx="100" cy="100" r="4" fill="%s"/></svg></div>'
                '<p class="f-disp text-6xl font-bold">404</p>'
                '<h1 class="mt-3 f-disp text-xl font-bold">Off the grid</h1>'
                '<p class="mt-2 text-sm %s">The page you seek is outside our map.</p>%s</div>') % (
            b["accent"], b["text_muted"], actions())
        feat = ["illustration 404", "SVG crosshair art", "centered", "dual CTA", "no images needed"]

    elif key == "premium-saas":
        body = ('<div class="text-center"><div class="mx-auto mb-6">%s</div>'
                '<span class="%s mb-4 inline-flex">%s Error 404</span>'
                '<p class="f-disp text-6xl sm:text-7xl font-bold">Page not found</p>'
                '<p class="mt-4 text-sm %s max-w-md mx-auto">The page you are looking for does not exist or has been moved.</p>'
                '<div class="mt-6">%s</div></div>') % (
            logo_svg("Flowbase"), b["badge"], ic("warning", "h-3.5 w-3.5"), b["text_muted"], actions())
        feat = ["premium SaaS 404", "brand header", "error badge", "centered headline", "dual CTA"]

    elif key == "dashboard":
        body = ('<div class="max-w-lg mx-auto %s %s p-8">'
                '<div class="flex items-center justify-between border-b border-current/10 pb-3 mb-6">'
                '<div class="flex items-center gap-2">%s<span class="text-sm font-medium">Workspace</span></div>'
                '<span class="%s">404</span></div>'
                '<div class="text-center py-6"><div class="mx-auto mb-4 flex h-14 w-14 items-center justify-center %s">%s</div>'
                '<p class="font-semibold">Resource not found</p>'
                '<p class="mt-1 text-sm %s">This item may have been deleted or you lack access.</p></div>'
                '<div class="flex gap-2">%s<a href="#" class="%s flex-1 justify-center">%s Report</a></div></div>') % (
            b["surface"], b["hover_card"], logo_svg("Flowbase"), b["badge"], b["surface_soft"], ic("warning", "h-7 w-7"), b["text_muted"],
            '<a href="/" class="%s flex-1 justify-center">%s Back to app</a>' % (b["btn_primary"], ic("home", "h-4 w-4")),
            b["btn_secondary"], ic("help", "h-4 w-4"))
        feat = ["dashboard 404", "app shell panel", "resource framing", "report CTA", "dual CTA"]

    elif key == "retro":
        body = ('<div class="text-center" style="font-family:%s">'
                '<p class="f-disp text-7xl sm:text-8xl font-bold" style="text-shadow:4px 4px 0 %s">404</p>'
                '<p class="mt-4 text-lg font-bold uppercase tracking-widest">Page Not Found</p>'
                '<p class="mt-2 text-sm %s">Error 404 — the page has left the building.</p>'
                '<div class="mt-6">%s</div></div>') % (b["font_display"], b["accent"], b["text_muted"], actions())
        feat = ["retro 404", "drop-shadow numeral", "uppercase tracking", "display font", "dual CTA"]

    elif key == "gradient":
        body = ('<div class="relative overflow-hidden rounded-3xl p-10 sm:p-14 text-center text-white" style="background:linear-gradient(135deg,%s,%s)">'
                '<div class="absolute inset-0 opacity-20" style="background:radial-gradient(circle at 70%% 20%%, #fff, transparent 50%%)" aria-hidden="true"></div>'
                '<div class="relative z-10"><p class="f-disp text-7xl sm:text-9xl font-bold">404</p>'
                '<h1 class="mt-4 f-disp text-2xl font-bold">Page not found</h1>'
                '<p class="mt-2 text-sm text-white/80 max-w-md mx-auto">This page slipped through a gradient rift.</p>'
                '<div class="mt-6"><a href="/" class="inline-flex items-center gap-2 rounded-full bg-white px-5 py-3 font-bold" style="color:%s">%s Back home</a></div></div></div>') % (
            b["accent"], b.get("accent2") or b["accent"], b["accent"], ic("home", "h-4 w-4"))
        feat = ["gradient 404", "full-bleed color", "white CTA", "oversized numeral", "responsive"]

    elif key == "abstract":
        body = ('<div class="grid grid-cols-1 gap-8 lg:grid-cols-2 items-center max-w-4xl mx-auto">'
                '<div class="relative h-64">%s</div>'
                '<div><p class="f-disp text-7xl sm:text-8xl font-bold">404</p>'
                '<h1 class="mt-3 f-disp text-xl font-bold">Nothing here</h1>'
                '<p class="mt-2 text-sm %s">The page you requested could not be located.</p>%s</div></div>') % (
            '<svg viewBox="0 0 200 200" class="h-full w-full" aria-hidden="true">'
            '<circle cx="60" cy="80" r="40" fill="none" stroke="%s" stroke-width="1.5"/>'
            '<rect x="100" y="40" width="70" height="70" rx="12" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.4"/>'
            '<path d="M40 160 Q100 120 160 160" fill="none" stroke="%s" stroke-width="1.5"/>'
            '<circle cx="140" cy="130" r="6" fill="%s"/></svg>' % (b["accent"], b["accent"], b["accent"]),
            b["text_muted"], actions())
        feat = ["abstract 404", "SVG abstract art", "split layout", "geometric shapes", "dual CTA"]

    else:  # vercel
        body = ('<div class="text-center"><div class="mx-auto mb-6 flex h-12 w-12 items-center justify-center %s">%s</div>'
                '<p class="f-mono text-xs %s uppercase tracking-wider mb-3">Error 404</p>'
                '<h1 class="f-disp text-5xl sm:text-6xl font-bold tracking-tight">Page not found</h1>'
                '<p class="mt-4 text-sm %s max-w-md mx-auto">The page you are looking for does not exist. It may have been moved or removed.</p>'
                '<div class="mt-6 flex flex-col sm:flex-row gap-3 justify-center">'
                '<a href="/" class="%s inline-flex items-center justify-center gap-2">%s Go home</a>'
                '<a href="#" class="%s inline-flex items-center justify-center gap-2">%s Contact support</a></div>'
                '<p class="mt-8 %s"><a href="#" class="text-sm hover:opacity-100 underline">%s View status page</a></p></div>') % (
            b["surface_soft"], ic("warning", "h-6 w-6"), b["text_muted"], b["text_muted"], b["btn_primary"], ic("arrow", "h-4 w-4"),
            b["btn_secondary"], ic("headset", "h-4 w-4"), b["text_muted"], ic("shield-check", "h-3.5 w-3.5"))
        feat = ["vercel-inspired 404", "mono error label", "status page link", "support CTA", "low chrome"]

    code = section(body, style)
    desc = "%s 404 page: %s." % (TOKENS[style]["title"].split(" (")[0], feat[0].capitalize())
    return dict(code=code, section_name=title, eyebrow="404", features=feat,
                tags=["404", "error", "not-found", "error-page"] + [style], desc=desc, scope="404")
