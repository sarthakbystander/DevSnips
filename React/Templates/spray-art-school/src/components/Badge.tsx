import type { ReactNode } from "react";

interface BadgeProps {
  children: ReactNode;
  tone?: "green" | "pink";
  rotate?: number;
}

export default function Badge({ children, tone = "green", rotate = -2 }: BadgeProps) {
  const toneClasses = tone === "green" ? "bg-neon-green text-ink-black" : "bg-hot-pink text-ink-black";

  return (
    <span
      className={`inline-block border-2 border-ink-black px-3 py-1 font-display text-xs tracking-wide ${toneClasses}`}
      style={{ transform: `rotate(${rotate}deg)` }}
    >
      {children}
    </span>
  );
}
