import type { Config } from "tailwindcss";

export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        "ink-black": "#0a0a0f",
        "ink-navy": "#0f1220",
        "neon-green": "#39FF14",
        "hot-pink": "#ff2ec4",
        "bone": "#f2f0e6",
      },
      fontFamily: {
        display: ["'Anton'", "sans-serif"],
        body: ["'Space Grotesk'", "sans-serif"],
      },
      keyframes: {
        splatFloat: {
          "0%, 100%": { transform: "translateY(0) rotate(var(--rot, 0deg))" },
          "50%": { transform: "translateY(-14px) rotate(calc(var(--rot, 0deg) + 4deg))" },
        },
        tornShift: {
          "0%, 100%": { transform: "translateX(0)" },
          "50%": { transform: "translateX(6px)" },
        },
      },
      animation: {
        "splat-float": "splatFloat 6s ease-in-out infinite",
        "torn-shift": "tornShift 8s ease-in-out infinite",
      },
    },
  },
  plugins: [],
} satisfies Config;
