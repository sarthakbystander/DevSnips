import type { ReactNode } from "react";

interface SectionHeadingProps {
  eyebrow?: string;
  children: ReactNode;
  align?: "left" | "center";
  as?: "h1" | "h2";
}

export default function SectionHeading({ eyebrow, children, align = "left", as = "h2" }: SectionHeadingProps) {
  const Heading = as;

  return (
    <div className={align === "center" ? "text-center" : "text-left"}>
      {eyebrow && <p className="mb-2 font-body text-sm text-hot-pink">{eyebrow}</p>}
      <Heading className="font-display text-4xl leading-[1.05] text-bone sm:text-5xl md:text-6xl">{children}</Heading>
    </div>
  );
}
