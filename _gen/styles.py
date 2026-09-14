"""15 design-language style systems for DevSnips sections.

Each STYLE entry is a dict of tokens used by the generator to render
sections that look visually distinct while sharing the same structural
layout. Tokens include font loading, body/surface classes, accent colors,
and class strings for common atoms (cards, buttons, badges, inputs).
"""

# Order is significant: index i -> style i.
STYLES = [
    "neo-brutalism", "edge-glassmorphism", "vercel", "minimal", "apple-inspired",
    "bento-grid", "editorial", "dark-premium", "startup-landing", "futuristic",
    "gradient-mesh", "soft-ui", "cyber", "monochrome", "elegant-luxury",
]

# Human-readable names for file/section naming.
STYLE_NAMES = {
    "neo-brutalism": "Neo Brutalism",
    "edge-glassmorphism": "Edge Glassmorphism",
    "vercel": "Vercel / Linear",
    "minimal": "Minimal",
    "apple-inspired": "Apple Inspired",
    "bento-grid": "Bento Grid",
    "editorial": "Editorial",
    "dark-premium": "Dark Premium",
    "startup-landing": "Startup Landing",
    "futuristic": "Futuristic",
    "gradient-mesh": "Gradient Mesh",
    "soft-ui": "Soft UI (Neumorphism)",
    "cyber": "Cyber",
    "monochrome": "Monochrome",
    "elegant-luxury": "Elegant Luxury",
}

# Per-style visual tokens.
# Keys:
#   title           : display title for metadata/README
#   font_url        : Google Fonts URL (or empty)
#   font_import     : @import or link handled by url; kept for reference
#   body_class      : classes on <body>
#   body_bg_css     : raw CSS for body background (optional, appended to style)
#   head_css        : extra <style> content for preview head (helpers/decor)
#   font_sans       : font-family stack for sans helper class `.f-sans`
#   font_mono       : font-family stack for mono helper class `.f-mono`
#   font_display    : font-family stack for display helper class `.f-disp`
#   accent          : hex accent color
#   accent2         : hex secondary accent (optional)
#   text            : default text color class (tailwind)
#   text_muted      : muted text class
#   surface         : card/panel class string
#   surface_soft    : softer panel class
#   border          : border class string
#   radius          : default radius token e.g. 'rounded-2xl'
#   shadow          : default shadow class
#   btn_primary     : primary button class string
#   btn_secondary   : secondary/ghost button class string
#   badge           : badge/pill class string
#   input           : input field class string
#   hover_card      : hover transform for cards
#   chip            : small chip class string
#   star_color      : text color class for rating stars
#   decor           : optional decorative background block (html) for preview shell

TOKENS = {
    "neo-brutalism": {
        "title": "Neo Brutalism",
        "font_url": "https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700;800;900&family=JetBrains+Mono:wght@400;600;700;800&display=swap",
        "font_sans": "'Archivo', ui-sans-serif, system-ui, sans-serif",
        "font_mono": "'JetBrains Mono', ui-monospace, monospace",
        "font_display": "'Archivo', ui-sans-serif, system-ui, sans-serif",
        "accent": "#FF4FA3",
        "accent2": "#00E676",
        "body_class": "bg-[#FFFDF5] text-black antialiased",
        "head_css": """
      .f-sans{font-family:'Archivo',sans-serif}.f-mono{font-family:'JetBrains Mono',monospace}.f-disp{font-family:'Archivo',sans-serif}
      .nb-grid{background-image:linear-gradient(#0001px,transparent 1px),linear-gradient(90deg,#0001px,transparent 1px);background-size:28px 28px;background-image:linear-gradient(rgba(0,0,0,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(0,0,0,.06) 1px,transparent 1px);background-size:28px 28px}
      .nb-shadow{box-shadow:8px 8px 0 0 #000}.nb-shadow-sm{box-shadow:4px 4px 0 0 #000}.nb-press{transition:transform .1s ease,box-shadow .1s ease}.nb-press:hover{transform:translate(2px,2px);box-shadow:2px 2px 0 0 #000}
""",
        "text": "text-black",
        "text_muted": "text-black/60",
        "surface": "bg-white border-2 border-black nb-shadow",
        "surface_soft": "bg-[#FFFDF5] border-2 border-black nb-shadow-sm",
        "border": "border-2 border-black",
        "radius": "rounded-none",
        "shadow": "nb-shadow",
        "btn_primary": "bg-[#FF4FA3] text-black border-2 border-black nb-shadow-sm nb-press font-bold",
        "btn_secondary": "bg-white text-black border-2 border-black nb-shadow-sm nb-press font-bold",
        "badge": "inline-flex items-center gap-1.5 border-2 border-black bg-[#FFE600] px-2.5 py-1 f-mono text-[11px] font-bold uppercase tracking-wider",
        "input": "w-full border-2 border-black bg-white px-4 py-3 f-sans font-semibold placeholder:text-black/40 focus:outline-none focus:nb-shadow-sm",
        "chip": "inline-flex items-center border-2 border-black bg-white px-3 py-1.5 f-mono text-xs font-bold",
        "hover_card": "nb-press",
        "star_color": "text-black",
    },
    "edge-glassmorphism": {
        "title": "Edge Glassmorphism",
        "font_url": "https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap",
        "font_sans": "'Sora', ui-sans-serif, system-ui, sans-serif",
        "font_mono": "'JetBrains Mono', ui-monospace, monospace",
        "font_display": "'Sora', ui-sans-serif, system-ui, sans-serif",
        "accent": "#6ee7ff",
        "accent2": "#a855f7",
        "body_class": "text-white antialiased",
        "head_css": """
      .f-sans{font-family:'Sora',sans-serif}.f-mono{font-family:'JetBrains Mono',monospace}.f-disp{font-family:'Sora',sans-serif}
      .eg-mesh{background:radial-gradient(at 18% 18%,rgba(236,72,153,.45) 0,transparent 50%),radial-gradient(at 82% 12%,rgba(99,102,241,.45) 0,transparent 50%),radial-gradient(at 75% 78%,rgba(34,211,238,.4) 0,transparent 50%),radial-gradient(at 22% 82%,rgba(168,85,247,.45) 0,transparent 50%),#0b0a1f;background-size:180% 180%;animation:eg-pan 18s ease-in-out infinite alternate}
      @keyframes eg-pan{0%{background-position:0 0}100%{background-position:100% 100%}}
      .eg-glass{background:rgba(255,255,255,.08);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,.16)}
      .eg-soft{background:rgba(255,255,255,.06);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border:1px solid rgba(255,255,255,.12)}
""",
        "text": "text-white",
        "text_muted": "text-white/60",
        "surface": "eg-glass rounded-2xl",
        "surface_soft": "eg-soft rounded-xl",
        "border": "border border-white/15",
        "radius": "rounded-2xl",
        "shadow": "shadow-[0_8px_40px_-12px_rgba(168,85,247,.45)]",
        "btn_primary": "bg-gradient-to-r from-fuchsia-500 to-indigo-500 text-white rounded-xl font-semibold shadow-lg hover:shadow-fuchsia-500/30",
        "btn_secondary": "eg-glass text-white rounded-xl font-medium hover:bg-white/15",
        "badge": "inline-flex items-center gap-1.5 eg-soft rounded-full px-3 py-1 f-mono text-[11px] font-medium uppercase tracking-wider text-white/80",
        "input": "w-full eg-soft rounded-xl px-4 py-3 text-white placeholder:text-white/40 focus:outline-none focus:ring-2 focus:ring-cyan-300/40",
        "chip": "inline-flex items-center eg-soft rounded-full px-3 py-1.5 f-mono text-xs text-white/85",
        "hover_card": "transition-transform duration-300 hover:-translate-y-1.5",
        "star_color": "text-cyan-300",
        "decor": '<div class="eg-mesh fixed inset-0 -z-10" aria-hidden="true"></div>',
    },
    "vercel": {
        "title": "Vercel / Linear",
        "font_url": "https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700&family=Geist+Mono:wght@400;500&display=swap",
        "font_sans": "'Geist', ui-sans-serif, system-ui, sans-serif",
        "font_mono": "'Geist Mono', ui-monospace, monospace",
        "font_display": "'Geist', ui-sans-serif, system-ui, sans-serif",
        "accent": "#50e3c2",
        "accent2": "#50e3c2",
        "body_class": "bg-[#050505] text-white antialiased",
        "head_css": """
      .f-sans{font-family:'Geist',sans-serif}.f-mono{font-family:'Geist Mono',monospace}.f-disp{font-family:'Geist',sans-serif}
      .vc-grid{background-image:linear-gradient(rgba(255,255,255,.025) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.025) 1px,transparent 1px);background-size:44px 44px;mask-image:radial-gradient(80% 60% at 50% 0%,#000 40%,transparent 100%)}
      .vc-dot{display:inline-block;height:6px;width:6px;border-radius:9999px;background:#50e3c2;box-shadow:0 0 8px #50e3c2}
      .vc-panel{box-shadow:0 0 0 1px rgba(255,255,255,.02),0 20px 60px -20px rgba(0,0,0,.9)}
""",
        "text": "text-white",
        "text_muted": "text-white/50",
        "surface": "bg-[#0a0a0a] border border-white/10 rounded-[14px] vc-panel",
        "surface_soft": "bg-white/[0.03] border border-white/10 rounded-lg",
        "border": "border border-white/10",
        "radius": "rounded-[14px]",
        "shadow": "vc-panel",
        "btn_primary": "bg-white text-black rounded-lg font-medium hover:bg-white/90",
        "btn_secondary": "border border-white/10 bg-white/[0.02] text-white rounded-lg hover:border-white/20 hover:text-white",
        "badge": "inline-flex items-center gap-1.5 rounded-full border border-white/10 bg-white/[0.04] px-3 py-1 f-mono text-[11px] text-white/60",
        "input": "w-full rounded-lg border border-white/10 bg-white/[0.03] px-4 py-3 text-white placeholder:text-white/40 focus:outline-none focus:ring-2 focus:ring-white/20",
        "chip": "inline-flex items-center rounded-full border border-white/10 bg-white/[0.03] px-3 py-1.5 f-mono text-xs text-white/70 hover:bg-white/[0.06]",
        "hover_card": "transition-colors hover:border-white/20",
        "star_color": "text-[#50e3c2]",
    },
    "minimal": {
        "title": "Minimal",
        "font_url": "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap",
        "font_sans": "'Inter', ui-sans-serif, system-ui, sans-serif",
        "font_mono": "'Inter', ui-sans-serif, system-ui, sans-serif",
        "font_display": "'Inter', ui-sans-serif, system-ui, sans-serif",
        "accent": "#111111",
        "accent2": "#6b7280",
        "body_class": "bg-white text-neutral-900 antialiased",
        "head_css": """
      .f-sans{font-family:'Inter',sans-serif}.f-mono{font-family:'Inter',sans-serif}.f-disp{font-family:'Inter',sans-serif}
""",
        "text": "text-neutral-900",
        "text_muted": "text-neutral-500",
        "surface": "bg-white border border-neutral-200 rounded-xl",
        "surface_soft": "bg-neutral-50 border border-neutral-200 rounded-lg",
        "border": "border border-neutral-200",
        "radius": "rounded-xl",
        "shadow": "shadow-sm",
        "btn_primary": "bg-neutral-900 text-white rounded-lg font-medium hover:bg-neutral-800",
        "btn_secondary": "border border-neutral-300 text-neutral-800 rounded-lg font-medium hover:bg-neutral-50",
        "badge": "inline-flex items-center gap-1.5 rounded-full border border-neutral-200 px-3 py-1 text-[11px] font-medium uppercase tracking-wider text-neutral-600",
        "input": "w-full rounded-lg border border-neutral-300 bg-white px-4 py-3 text-neutral-900 placeholder:text-neutral-400 focus:outline-none focus:ring-2 focus:ring-neutral-900/10 focus:border-neutral-400",
        "chip": "inline-flex items-center rounded-full border border-neutral-200 px-3 py-1.5 text-xs text-neutral-700 hover:bg-neutral-50",
        "hover_card": "transition-all duration-300 hover:shadow-md hover:-translate-y-0.5",
        "star_color": "text-neutral-900",
    },
    "apple-inspired": {
        "title": "Apple Inspired",
        "font_url": "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap",
        "font_sans": "'Inter', ui-sans-serif, system-ui, sans-serif",
        "font_mono": "'Inter', ui-sans-serif, system-ui, sans-serif",
        "font_display": "'Inter', ui-sans-serif, system-ui, sans-serif",
        "accent": "#0071e3",
        "accent2": "#147ce5",
        "body_class": "bg-[#fbfbfd] text-[#1d1d1f] antialiased",
        "head_css": """
      .f-sans{font-family:'Inter',sans-serif}.f-mono{font-family:'Inter',sans-serif}.f-disp{font-family:'Inter',sans-serif}
""",
        "text": "text-[#1d1d1f]",
        "text_muted": "text-[#6e6e73]",
        "surface": "bg-white rounded-2xl shadow-[0_4px_24px_-8px_rgba(0,0,0,.12)]",
        "surface_soft": "bg-white/70 backdrop-blur rounded-2xl",
        "border": "border border-black/5",
        "radius": "rounded-2xl",
        "shadow": "shadow-[0_4px_24px_-8px_rgba(0,0,0,.12)]",
        "btn_primary": "bg-[#0071e3] text-white rounded-full font-medium hover:bg-[#0077ed] px-6 py-3",
        "btn_secondary": "bg-white text-[#0071e3] rounded-full font-medium hover:bg-white/90 px-6 py-3 shadow-sm",
        "badge": "inline-flex items-center gap-1.5 rounded-full bg-[#0071e3]/10 px-3 py-1 text-[11px] font-semibold uppercase tracking-wide text-[#0071e3]",
        "input": "w-full rounded-xl bg-white border border-black/5 px-4 py-3 text-[#1d1d1f] placeholder:text-[#6e6e73] focus:outline-none focus:ring-2 focus:ring-[#0071e3]/30",
        "chip": "inline-flex items-center rounded-full bg-[#0071e3]/10 px-3 py-1.5 text-xs font-medium text-[#0071e3]",
        "hover_card": "transition-transform duration-300 hover:-translate-y-1 hover:shadow-[0_12px_40px_-12px_rgba(0,0,0,.18)]",
        "star_color": "text-[#0071e3]",
    },
    "bento-grid": {
        "title": "Bento Grid",
        "font_url": "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap",
        "font_sans": "'Inter', ui-sans-serif, system-ui, sans-serif",
        "font_mono": "'JetBrains Mono', ui-monospace, monospace",
        "font_display": "'Inter', ui-sans-serif, system-ui, sans-serif",
        "accent": "#6366f1",
        "accent2": "#ec4899",
        "body_class": "bg-[#0f1020] text-white antialiased",
        "head_css": """
      .f-sans{font-family:'Inter',sans-serif}.f-mono{font-family:'JetBrains Mono',monospace}.f-disp{font-family:'Inter',sans-serif}
      .bento{background:linear-gradient(135deg,rgba(99,102,241,.12),rgba(236,72,153,.08))}
""",
        "text": "text-white",
        "text_muted": "text-white/55",
        "surface": "bg-white/[0.04] border border-white/10 rounded-3xl",
        "surface_soft": "bg-white/[0.03] border border-white/10 rounded-2xl",
        "border": "border border-white/10",
        "radius": "rounded-3xl",
        "shadow": "shadow-[0_8px_30px_-12px_rgba(99,102,241,.4)]",
        "btn_primary": "bg-gradient-to-br from-indigo-500 to-pink-500 text-white rounded-2xl font-semibold hover:opacity-90",
        "btn_secondary": "border border-white/15 bg-white/5 text-white rounded-2xl font-medium hover:bg-white/10",
        "badge": "inline-flex items-center gap-1.5 rounded-full border border-white/10 bg-white/5 px-3 py-1 f-mono text-[11px] font-medium text-white/70",
        "input": "w-full rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-white placeholder:text-white/40 focus:outline-none focus:ring-2 focus:ring-indigo-400/40",
        "chip": "inline-flex items-center rounded-full border border-white/10 bg-white/5 px-3 py-1.5 f-mono text-xs text-white/75",
        "hover_card": "transition-transform duration-300 hover:-translate-y-1",
        "star_color": "text-indigo-300",
    },
    "editorial": {
        "title": "Editorial",
        "font_url": "https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600&display=swap",
        "font_sans": "'Inter', ui-sans-serif, system-ui, sans-serif",
        "font_mono": "'Inter', ui-sans-serif, system-ui, sans-serif",
        "font_display": "'Fraunces', ui-serif, Georgia, serif",
        "accent": "#b45309",
        "accent2": "#92400e",
        "body_class": "bg-[#f7f3ec] text-[#1c1917] antialiased",
        "head_css": """
      .f-sans{font-family:'Inter',sans-serif}.f-mono{font-family:'Inter',sans-serif}.f-disp{font-family:'Fraunces',serif}
""",
        "text": "text-[#1c1917]",
        "text_muted": "text-[#78716c]",
        "surface": "bg-[#fffdf8] border border-[#1c1917]/10 rounded-sm",
        "surface_soft": "bg-[#f7f3ec] border border-[#1c1917]/10 rounded-sm",
        "border": "border border-[#1c1917]/10",
        "radius": "rounded-sm",
        "shadow": "shadow-[0_1px_0_0_rgba(28,25,23,.06)]",
        "btn_primary": "bg-[#1c1917] text-[#f7f3ec] rounded-sm font-medium hover:bg-[#2a2522]",
        "btn_secondary": "border border-[#1c1917]/20 text-[#1c1917] rounded-sm font-medium hover:bg-[#1c1917]/5",
        "badge": "inline-flex items-center gap-1.5 rounded-sm border border-[#1c1917]/15 px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.18em] text-[#78716c]",
        "input": "w-full rounded-sm border border-[#1c1917]/15 bg-[#fffdf8] px-4 py-3 text-[#1c1917] placeholder:text-[#a8a29e] focus:outline-none focus:ring-1 focus:ring-[#b45309]/40",
        "chip": "inline-flex items-center rounded-sm border border-[#1c1917]/15 px-3 py-1.5 text-xs text-[#1c1917] hover:bg-[#1c1917]/5",
        "hover_card": "transition-colors hover:border-[#1c1917]/25",
        "star_color": "text-[#b45309]",
    },
    "dark-premium": {
        "title": "Dark Premium",
        "font_url": "https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&display=swap",
        "font_sans": "'Manrope', ui-sans-serif, system-ui, sans-serif",
        "font_mono": "'Manrope', ui-sans-serif, system-ui, sans-serif",
        "font_display": "'Manrope', ui-sans-serif, system-ui, sans-serif",
        "accent": "#fbbf24",
        "accent2": "#f59e0b",
        "body_class": "bg-[#0a0a0f] text-white antialiased",
        "head_css": """
      .f-sans{font-family:'Manrope',sans-serif}.f-mono{font-family:'Manrope',sans-serif}.f-disp{font-family:'Manrope',sans-serif}
      .dp-glow{background:radial-gradient(60% 50% at 50% 0%,rgba(251,191,36,.10),transparent 70%)}
""",
        "text": "text-white",
        "text_muted": "text-white/55",
        "surface": "bg-gradient-to-b from-white/[0.06] to-white/[0.02] border border-white/10 rounded-2xl",
        "surface_soft": "bg-white/[0.04] border border-white/10 rounded-xl",
        "border": "border border-white/10",
        "radius": "rounded-2xl",
        "shadow": "shadow-[0_8px_40px_-12px_rgba(0,0,0,.7)]",
        "btn_primary": "bg-gradient-to-r from-amber-400 to-yellow-500 text-[#0a0a0f] rounded-xl font-semibold hover:from-amber-300 hover:to-yellow-400",
        "btn_secondary": "border border-white/15 bg-white/5 text-white rounded-xl font-medium hover:bg-white/10",
        "badge": "inline-flex items-center gap-1.5 rounded-full border border-amber-400/30 bg-amber-400/10 px-3 py-1 text-[11px] font-semibold uppercase tracking-wider text-amber-300",
        "input": "w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-white placeholder:text-white/40 focus:outline-none focus:ring-2 focus:ring-amber-400/30",
        "chip": "inline-flex items-center rounded-full border border-white/10 bg-white/5 px-3 py-1.5 text-xs text-white/80",
        "hover_card": "transition-all duration-300 hover:-translate-y-1 hover:border-amber-400/30",
        "star_color": "text-amber-400",
    },
    "startup-landing": {
        "title": "Startup Landing",
        "font_url": "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap",
        "font_sans": "'Plus Jakarta Sans', ui-sans-serif, system-ui, sans-serif",
        "font_mono": "'Plus Jakarta Sans', ui-sans-serif, system-ui, sans-serif",
        "font_display": "'Plus Jakarta Sans', ui-sans-serif, system-ui, sans-serif",
        "accent": "#4f46e5",
        "accent2": "#06b6d4",
        "body_class": "bg-white text-slate-900 antialiased",
        "head_css": """
      .f-sans{font-family:'Plus Jakarta Sans',sans-serif}.f-mono{font-family:'Plus Jakarta Sans',sans-serif}.f-disp{font-family:'Plus Jakarta Sans',sans-serif}
""",
        "text": "text-slate-900",
        "text_muted": "text-slate-500",
        "surface": "bg-white border border-slate-200 rounded-2xl shadow-[0_2px_12px_-4px_rgba(15,23,42,.08)]",
        "surface_soft": "bg-slate-50 border border-slate-200 rounded-xl",
        "border": "border border-slate-200",
        "radius": "rounded-2xl",
        "shadow": "shadow-[0_2px_12px_-4px_rgba(15,23,42,.08)]",
        "btn_primary": "bg-indigo-600 text-white rounded-xl font-semibold hover:bg-indigo-700 shadow-lg shadow-indigo-600/20",
        "btn_secondary": "border border-slate-300 text-slate-800 rounded-xl font-semibold hover:bg-slate-50",
        "badge": "inline-flex items-center gap-1.5 rounded-full bg-indigo-50 border border-indigo-100 px-3 py-1 text-[11px] font-semibold uppercase tracking-wide text-indigo-600",
        "input": "w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/30 focus:border-indigo-400",
        "chip": "inline-flex items-center rounded-full border border-slate-200 bg-slate-50 px-3 py-1.5 text-xs font-medium text-slate-700 hover:bg-slate-100",
        "hover_card": "transition-all duration-300 hover:shadow-[0_12px_32px_-8px_rgba(79,70,229,.25)] hover:-translate-y-1",
        "star_color": "text-amber-400",
    },
    "futuristic": {
        "title": "Futuristic",
        "font_url": "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap",
        "font_sans": "'Space Grotesk', ui-sans-serif, system-ui, sans-serif",
        "font_mono": "'JetBrains Mono', ui-monospace, monospace",
        "font_display": "'Space Grotesk', ui-sans-serif, system-ui, sans-serif",
        "accent": "#22d3ee",
        "accent2": "#a78bfa",
        "body_class": "bg-[#070b14] text-white antialiased",
        "head_css": """
      .f-sans{font-family:'Space Grotesk',sans-serif}.f-mono{font-family:'JetBrains Mono',monospace}.f-disp{font-family:'Space Grotesk',sans-serif}
      .ft-grid{background-image:linear-gradient(rgba(34,211,238,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(34,211,238,.07) 1px,transparent 1px);background-size:40px 40px;mask-image:radial-gradient(70% 60% at 50% 30%,#000,transparent 100%)}
      .ft-glow{box-shadow:0 0 0 1px rgba(34,211,238,.2),0 0 30px -8px rgba(34,211,238,.4)}
""",
        "text": "text-white",
        "text_muted": "text-cyan-100/50",
        "surface": "bg-[#0b1220]/80 border border-cyan-400/20 rounded-2xl ft-glow",
        "surface_soft": "bg-[#0b1220]/60 border border-cyan-400/15 rounded-xl",
        "border": "border border-cyan-400/20",
        "radius": "rounded-2xl",
        "shadow": "ft-glow",
        "btn_primary": "bg-cyan-400 text-[#070b14] rounded-xl font-bold hover:bg-cyan-300 shadow-[0_0_24px_-6px_rgba(34,211,238,.7)]",
        "btn_secondary": "border border-cyan-400/30 text-cyan-100 rounded-xl font-medium hover:bg-cyan-400/10",
        "badge": "inline-flex items-center gap-1.5 rounded-full border border-cyan-400/30 bg-cyan-400/10 px-3 py-1 f-mono text-[11px] font-medium uppercase tracking-wider text-cyan-200",
        "input": "w-full rounded-xl border border-cyan-400/20 bg-[#0b1220]/60 px-4 py-3 text-white placeholder:text-cyan-100/40 focus:outline-none focus:ring-2 focus:ring-cyan-400/40",
        "chip": "inline-flex items-center rounded-full border border-cyan-400/20 bg-cyan-400/5 px-3 py-1.5 f-mono text-xs text-cyan-100",
        "hover_card": "transition-transform duration-300 hover:-translate-y-1",
        "star_color": "text-cyan-300",
        "decor": '<div class="ft-grid pointer-events-none absolute inset-0 -z-10" aria-hidden="true"></div>',
    },
    "gradient-mesh": {
        "title": "Gradient Mesh",
        "font_url": "https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap",
        "font_sans": "'Outfit', ui-sans-serif, system-ui, sans-serif",
        "font_mono": "'Outfit', ui-sans-serif, system-ui, sans-serif",
        "font_display": "'Outfit', ui-sans-serif, system-ui, sans-serif",
        "accent": "#8b5cf6",
        "accent2": "#ec4899",
        "body_class": "text-white antialiased",
        "head_css": """
      .f-sans{font-family:'Outfit',sans-serif}.f-mono{font-family:'Outfit',sans-serif}.f-disp{font-family:'Outfit',sans-serif}
      .gm-bg{background:linear-gradient(120deg,#7c3aed,#ec4899,#f97316,#06b6d4);background-size:300% 300%;animation:gm 16s ease infinite}
      @keyframes gm{0%{background-position:0 50%}50%{background-position:100% 50%}100%{background-position:0 50%}}
""",
        "text": "text-white",
        "text_muted": "text-white/70",
        "surface": "bg-white/15 backdrop-blur-xl border border-white/20 rounded-3xl",
        "surface_soft": "bg-white/10 backdrop-blur-md border border-white/15 rounded-2xl",
        "border": "border border-white/20",
        "radius": "rounded-3xl",
        "shadow": "shadow-2xl shadow-purple-900/30",
        "btn_primary": "bg-white text-purple-700 rounded-full font-bold hover:bg-white/90 shadow-lg",
        "btn_secondary": "border border-white/40 text-white rounded-full font-semibold hover:bg-white/15",
        "badge": "inline-flex items-center gap-1.5 rounded-full bg-white/20 border border-white/30 px-3 py-1 text-[11px] font-semibold uppercase tracking-wide text-white",
        "input": "w-full rounded-full bg-white/15 border border-white/30 px-4 py-3 text-white placeholder:text-white/60 focus:outline-none focus:ring-2 focus:ring-white/50",
        "chip": "inline-flex items-center rounded-full bg-white/15 border border-white/25 px-3 py-1.5 text-xs text-white",
        "hover_card": "transition-transform duration-300 hover:-translate-y-1 hover:bg-white/20",
        "star_color": "text-white",
        "decor": '<div class="gm-bg fixed inset-0 -z-10" aria-hidden="true"></div>',
    },
    "soft-ui": {
        "title": "Soft UI (Neumorphism)",
        "font_url": "https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&display=swap",
        "font_sans": "'Manrope', ui-sans-serif, system-ui, sans-serif",
        "font_mono": "'Manrope', ui-sans-serif, system-ui, sans-serif",
        "font_display": "'Manrope', ui-sans-serif, system-ui, sans-serif",
        "accent": "#6366f1",
        "accent2": "#8b5cf6",
        "body_class": "bg-[#e6e7ee] text-[#3a3b45] antialiased",
        "head_css": """
      .f-sans{font-family:'Manrope',sans-serif}.f-mono{font-family:'Manrope',sans-serif}.f-disp{font-family:'Manrope',sans-serif}
      .neu{background:#e6e7ee;box-shadow:8px 8px 18px #c8c9d0,-8px -8px 18px #ffffff}
      .neu-sm{background:#e6e7ee;box-shadow:5px 5px 10px #c8c9d0,-5px -5px 10px #ffffff}
      .neu-in{background:#e6e7ee;box-shadow:inset 5px 5px 10px #c8c9d0,inset -5px -5px 10px #ffffff}
      .neu-press:active{box-shadow:inset 4px 4px 8px #c8c9d0,inset -4px -4px 8px #ffffff}
""",
        "text": "text-[#3a3b45]",
        "text_muted": "text-[#8a8b95]",
        "surface": "neu rounded-2xl",
        "surface_soft": "neu-sm rounded-xl",
        "border": "border-0",
        "radius": "rounded-2xl",
        "shadow": "neu",
        "btn_primary": "neu-sm rounded-xl font-semibold text-[#6366f1] neu-press",
        "btn_secondary": "neu-sm rounded-xl font-medium text-[#3a3b45] neu-press",
        "badge": "inline-flex items-center gap-1.5 neu-sm rounded-full px-3 py-1 text-[11px] font-semibold uppercase tracking-wide text-[#6366f1]",
        "input": "w-full neu-in rounded-xl px-4 py-3 text-[#3a3b45] placeholder:text-[#a0a1aa] focus:outline-none",
        "chip": "inline-flex items-center neu-sm rounded-full px-3 py-1.5 text-xs text-[#3a3b45]",
        "hover_card": "transition-transform duration-300 hover:-translate-y-0.5",
        "star_color": "text-[#6366f1]",
    },
    "cyber": {
        "title": "Cyber",
        "font_url": "https://fonts.googleapis.com/css2?family=Chakra:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600;700&display=swap",
        "font_sans": "'Chakra', ui-sans-serif, system-ui, sans-serif",
        "font_mono": "'JetBrains Mono', ui-monospace, monospace",
        "font_display": "'Chakra', ui-sans-serif, system-ui, sans-serif",
        "accent": "#39ff14",
        "accent2": "#ff00aa",
        "body_class": "bg-[#0a0e0a] text-[#c8ffd0] antialiased",
        "head_css": """
      .f-sans{font-family:'Chakra',sans-serif}.f-mono{font-family:'JetBrains Mono',monospace}.f-disp{font-family:'Chakra',sans-serif}
      .cy-grid{background-image:linear-gradient(rgba(57,255,20,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(57,255,20,.06) 1px,transparent 1px);background-size:32px 32px}
      .cy-glow{box-shadow:0 0 0 1px rgba(57,255,20,.3),0 0 24px -6px rgba(57,255,20,.4)}
      .cy-clip{clip-path:polygon(0 0,calc(100% - 14px) 0,100% 14px,100% 100%,14px 100%,0 calc(100% - 14px))}
""",
        "text": "text-[#c8ffd0]",
        "text_muted": "text-[#5a8c5e]",
        "surface": "bg-[#0d130d]/80 border border-[#39ff14]/25 cy-clip cy-glow",
        "surface_soft": "bg-[#0d130d]/60 border border-[#39ff14]/15 cy-clip",
        "border": "border border-[#39ff14]/25",
        "radius": "",
        "shadow": "cy-glow",
        "btn_primary": "bg-[#39ff14] text-[#0a0e0a] cy-clip font-bold uppercase tracking-wide hover:bg-[#7fff5f]",
        "btn_secondary": "border border-[#39ff14]/40 text-[#39ff14] cy-clip font-semibold uppercase tracking-wide hover:bg-[#39ff14]/10",
        "badge": "inline-flex items-center gap-1.5 border border-[#39ff14]/40 bg-[#39ff14]/10 px-3 py-1 f-mono text-[11px] font-bold uppercase tracking-wider text-[#39ff14]",
        "input": "w-full cy-clip bg-[#0d130d]/80 border border-[#39ff14]/25 px-4 py-3 text-[#c8ffd0] placeholder:text-[#5a8c5e] focus:outline-none focus:cy-glow",
        "chip": "inline-flex items-center border border-[#39ff14]/30 bg-[#39ff14]/5 px-3 py-1.5 f-mono text-xs text-[#39ff14]",
        "hover_card": "transition-transform duration-200 hover:-translate-y-1",
        "star_color": "text-[#39ff14]",
        "decor": '<div class="cy-grid pointer-events-none absolute inset-0 -z-10" aria-hidden="true"></div>',
    },
    "monochrome": {
        "title": "Monochrome",
        "font_url": "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap",
        "font_sans": "'Inter', ui-sans-serif, system-ui, sans-serif",
        "font_mono": "'JetBrains Mono', ui-monospace, monospace",
        "font_display": "'Inter', ui-sans-serif, system-ui, sans-serif",
        "accent": "#000000",
        "accent2": "#525252",
        "body_class": "bg-white text-black antialiased",
        "head_css": """
      .f-sans{font-family:'Inter',sans-serif}.f-mono{font-family:'JetBrains Mono',monospace}.f-disp{font-family:'Inter',sans-serif}
""",
        "text": "text-black",
        "text_muted": "text-black/50",
        "surface": "bg-white border border-black/15 rounded-lg",
        "surface_soft": "bg-black/[0.03] border border-black/10 rounded-lg",
        "border": "border border-black/15",
        "radius": "rounded-lg",
        "shadow": "shadow-sm",
        "btn_primary": "bg-black text-white rounded-lg font-medium hover:bg-black/85",
        "btn_secondary": "border border-black/20 text-black rounded-lg font-medium hover:bg-black/5",
        "badge": "inline-flex items-center gap-1.5 rounded-full border border-black/15 px-3 py-1 f-mono text-[11px] font-medium uppercase tracking-wider text-black/60",
        "input": "w-full rounded-lg border border-black/20 bg-white px-4 py-3 text-black placeholder:text-black/40 focus:outline-none focus:ring-2 focus:ring-black/15",
        "chip": "inline-flex items-center rounded-full border border-black/15 px-3 py-1.5 text-xs text-black/70 hover:bg-black/5",
        "hover_card": "transition-colors hover:border-black/30",
        "star_color": "text-black",
    },
    "elegant-luxury": {
        "title": "Elegant Luxury",
        "font_url": "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Jost:wght@300;400;500;600&display=swap",
        "font_sans": "'Jost', ui-sans-serif, system-ui, sans-serif",
        "font_mono": "'Jost', ui-sans-serif, system-ui, sans-serif",
        "font_display": "'Cormorant Garamond', ui-serif, Georgia, serif",
        "accent": "#c5a572",
        "accent2": "#a3855a",
        "body_class": "bg-[#0c0c0d] text-[#ece7df] antialiased",
        "head_css": """
      .f-sans{font-family:'Jost',sans-serif}.f-mono{font-family:'Jost',sans-serif}.f-disp{font-family:'Cormorant Garamond',serif}
      .el-line{background:linear-gradient(90deg,transparent,rgba(197,165,114,.6),transparent)}
""",
        "text": "text-[#ece7df]",
        "text_muted": "text-[#9a948a]",
        "surface": "bg-[#131312] border border-[#c5a572]/20 rounded-sm",
        "surface_soft": "bg-[#161615] border border-[#c5a572]/12 rounded-sm",
        "border": "border border-[#c5a572]/20",
        "radius": "rounded-sm",
        "shadow": "shadow-[0_8px_40px_-16px_rgba(0,0,0,.8)]",
        "btn_primary": "bg-[#c5a572] text-[#0c0c0d] rounded-sm font-medium tracking-wider uppercase hover:bg-[#d4b883]",
        "btn_secondary": "border border-[#c5a572]/40 text-[#c5a572] rounded-sm font-medium tracking-wider uppercase hover:bg-[#c5a572]/10",
        "badge": "inline-flex items-center gap-1.5 rounded-sm border border-[#c5a572]/30 px-3 py-1 text-[11px] font-medium uppercase tracking-[0.22em] text-[#c5a572]",
        "input": "w-full rounded-sm border border-[#c5a572]/25 bg-[#131312] px-4 py-3 text-[#ece7df] placeholder:text-[#9a948a] focus:outline-none focus:ring-1 focus:ring-[#c5a572]/50",
        "chip": "inline-flex items-center rounded-sm border border-[#c5a572]/25 px-3 py-1.5 text-xs tracking-wider text-[#c5a572]",
        "hover_card": "transition-colors hover:border-[#c5a572]/40",
        "star_color": "text-[#c5a572]",
    },
}
