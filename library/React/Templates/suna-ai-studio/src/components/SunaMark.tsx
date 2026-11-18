import type { CSSProperties } from "react";

interface SunaMarkProps {
  className?: string;
  cut?: string;
  size?: number;
}

/** A small, original sun-and-seed mark used for Suna Studio. */
export function SunaMark({
  className,
  cut = "#F6F4FA",
  size = 32,
}: SunaMarkProps) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 40 40"
      fill="none"
      aria-hidden="true"
      className={className}
      style={{ "--mark-cut": cut } as CSSProperties}
    >
      <circle cx="20" cy="20" r="18" fill="currentColor" />
      <path
        d="M20 5.5c6.2 4.7 7.4 10.5 3.4 14.5-3.6 3.6-9.6 2.2-10.8 6.9-1.1 4.1 1.8 7.1 5.4 7.1 6.9 0 11.5-5.7 11.5-12.6C29.5 13.2 25.6 8.6 20 5.5Z"
        fill="var(--mark-cut)"
      />
      <circle
        cx="13.6"
        cy="12.6"
        r="1.35"
        fill="var(--mark-cut)"
        opacity="0.82"
      />
    </svg>
  );
}
