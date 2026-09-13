interface TornDividerProps {
  color?: "green" | "pink" | "bone";
  flip?: boolean;
  className?: string;
}

/**
 * A ripped-paper strip used between sections. Decorative only.
 */
export default function TornDivider({ color = "green", flip = false, className = "" }: TornDividerProps) {
  const fill = color === "green" ? "#39FF14" : color === "pink" ? "#ff2ec4" : "#f2f0e6";

  return (
    <div
      aria-hidden="true"
      className={`clip-torn h-16 w-full ${flip ? "rotate-180" : ""} ${className}`}
      style={{ backgroundColor: fill }}
    />
  );
}
