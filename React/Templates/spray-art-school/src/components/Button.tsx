import type { ButtonHTMLAttributes, ReactNode } from "react";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode;
  variant?: "spray" | "standard";
}

export default function Button({ children, variant = "standard", className = "", ...rest }: ButtonProps) {
  if (variant === "spray") {
    return (
      <button
        className={`clip-spray-btn inline-flex items-center gap-2 bg-neon-green px-8 py-3 font-display text-sm tracking-wide text-ink-black transition-transform hover:-translate-y-0.5 hover:rotate-1 focus-visible:outline-4 ${className}`}
        {...rest}
      >
        {children}
      </button>
    );
  }

  return (
    <button
      className={`rounded-full border-2 border-bone px-6 py-2.5 font-body text-sm font-medium transition-colors hover:border-neon-green hover:text-neon-green ${className}`}
      {...rest}
    >
      {children}
    </button>
  );
}
