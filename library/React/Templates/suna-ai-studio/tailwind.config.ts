import type { Config } from "tailwindcss";

/**
 * "Deep Current" — a cinematic dark design system.
 *
 * The token NAMES are kept from the original light theme so components read
 * logically (paper = canvas, ink = primary text, surface = card, …); the VALUES
 * carry the deep ocean/night mood: near-black blue canvas, glass panels, a
 * luminous violet accent, and a paper-white action color.
 */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        /** Page canvas — near-black deep blue. */
        paper: "#05070D",
        /** Card / glass panel fill. */
        surface: "#0D1322",
        /** Nested well / hover fill, a step lighter. */
        "surface-2": "#131B2C",
        /** Primary text — paper white. */
        ink: "#EDF1FA",
        "ink-2": "#C4CEE0",
        muted: "#8E9BB6",
        faint: "#5B687F",
        line: "#1B2333",
        "line-strong": "#2B3549",
        /** Ice-cyan accent — the ocean reference. */
        accent: "#76CDE0",
        /** Light-accent text for dark tinted chips. */
        "accent-deep": "#BCE7F2",
        "accent-soft": "#0E1E28",
        lilac: "#5FB3C7",
        "lilac-soft": "#0F2027",
        sage: "#5BC89A",
        "sage-soft": "#0F241D",
        gold: "#E3B75F",
        "gold-soft": "#241D10",
        rose: "#F1A2BC",
        "rose-soft": "#27131D",
        /** The darkest layer — player bar / sheets. */
        night: "#030509",
        "night-2": "#0C1220",
        /** Paper white — action fills and player text. */
        cream: "#F2F5FF",
      },
      fontFamily: {
        display: ["Instrument Serif", "Georgia", "Cambria", "serif"],
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
        mono: ["IBM Plex Mono", "ui-monospace", "SFMono-Regular", "monospace"],
      },
      boxShadow: {
        card:
          "inset 0 1px 0 rgba(255, 255, 255, 0.05), 0 26px 60px -34px rgba(0, 0, 0, 0.85)",
        lift:
          "inset 0 1px 0 rgba(255, 255, 255, 0.06), 0 34px 80px -38px rgba(0, 0, 0, 0.9)",
        player: "0 -26px 60px -34px rgba(0, 0, 0, 0.9)",
      },
      keyframes: {
        "fade-up": {
          "0%": { opacity: "0", transform: "translateY(10px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        "fade-in": {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        orbit: {
          "0%": { transform: "rotate(0deg)" },
          "100%": { transform: "rotate(360deg)" },
        },
        "pulse-soft": {
          "0%, 100%": { opacity: "0.45", transform: "scale(0.96)" },
          "50%": { opacity: "1", transform: "scale(1.04)" },
        },
        equalize: {
          "0%, 100%": { transform: "scaleY(0.35)" },
          "50%": { transform: "scaleY(1)" },
        },
        drift: {
          "0%, 100%": { transform: "translate3d(0, 0, 0) scale(1)" },
          "50%": { transform: "translate3d(0, -14px, 0) scale(1.025)" },
        },
      },
      animation: {
        "fade-up": "fade-up 420ms cubic-bezier(0.22, 1, 0.36, 1) both",
        "fade-in": "fade-in 300ms ease-out both",
        orbit: "orbit 10s linear infinite",
        "pulse-soft": "pulse-soft 2.4s ease-in-out infinite",
        equalize: "equalize 900ms ease-in-out infinite",
        drift: "drift 16s ease-in-out infinite",
      },
    },
  },
  plugins: [],
} satisfies Config;
