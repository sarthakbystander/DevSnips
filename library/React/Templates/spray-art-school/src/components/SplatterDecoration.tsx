interface SplatterDecorationProps {
  color?: "green" | "pink";
  className?: string;
  size?: number;
}

/**
 * Decorative spray-splatter blob. Purely presentational, so it's hidden from
 * assistive tech via aria-hidden.
 */
export default function SplatterDecoration({ color = "green", className = "", size = 120 }: SplatterDecorationProps) {
  const fill = color === "green" ? "#39FF14" : "#ff2ec4";

  return (
    <svg
      aria-hidden="true"
      width={size}
      height={size}
      viewBox="0 0 200 200"
      className={`animate-splat-float opacity-70 ${className}`}
    >
      <path
        d="M45 20c10-14 32-18 44-8 8 6 10 18 20 20 16 4 34-2 46 8 14 12 16 34 6 48-6 8-16 12-18 22-2 12 8 22 2 34-8 16-30 20-46 14-10-4-16-14-28-16-14-2-28 6-40-2-14-10-16-30-8-44 4-8 12-12 12-22 0-12-10-20-8-32 2-12 10-16 18-22z"
        fill={fill}
      />
    </svg>
  );
}
