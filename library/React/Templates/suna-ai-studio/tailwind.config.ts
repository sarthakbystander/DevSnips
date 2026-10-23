import type { Config } from "tailwindcss";

export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        paper: "#F6F4FA",
        surface: "#FFFFFF",
        "surface-2": "#F1EDF8",
        ink: "#211D31",
        "ink-2": "#3B3550",
        muted: "#6D6783",
        faint: "#9B95AD",
        line: "#E6E0F0",
        "line-strong": "#D5CDE4",
        accent: "#6F52D9",
        "accent-deep": "#5136B0",
        "accent-soft": "#ECE6FD",
        lilac: "#CBBFF2",
        "lilac-soft": "#F1ECFC",
        sage: "#8BB8A4",
        "sage-soft": "#E4F2EC",
        gold: "#D7AD62",
        "gold-soft": "#F7EDDA",
        rose: "#E5A6B8",
        "rose-soft": "#FAE7EC",
        night: "#151220",
        "night-2": "#211C30",
        cream: "#F5F1FF",
      },
      fontFamily: {
        display: ["Instrument Serif", "Georgia", "Cambria", "serif"],
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
        mono: ["IBM Plex Mono", "ui-monospace", "SFMono-Regular", "monospace"],
      },
      boxShadow: {
        card: "0 1px 2px rgba(33, 29, 49, 0.04), 0 18px 40px -28px rgba(61, 45, 116, 0.25)",
        lift: "0 2px 4px rgba(33, 29, 49, 0.05), 0 28px 60px -36px rgba(61, 45, 116, 0.32)",
        player: "0 -18px 50px -32px rgba(12, 8, 30, 0.55)",
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
      },
      animation: {
        "fade-up": "fade-up 420ms cubic-bezier(0.22, 1, 0.36, 1) both",
        "fade-in": "fade-in 300ms ease-out both",
        orbit: "orbit 10s linear infinite",
        "pulse-soft": "pulse-soft 2.4s ease-in-out infinite",
        equalize: "equalize 900ms ease-in-out infinite",
      },
    },
  },
  plugins: [],
} satisfies Config;
