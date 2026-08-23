import { useId } from "react";

/**
 * DevSnips React Hero — Neo-Brutalist direction.
 *
 * The expressive ceiling of the system, kept disciplined: an asymmetric
 * editorial split (7/5 of 12) with a hard-bordered metric panel, plus a row
 * of flat accent stat blocks. Everything is square (radius-none), every
 * border is 2px solid border-strong, and the only shadows are hard offsets
 * with zero blur. Buttons press down by their shadow offset on :active
 * (≤100ms). One primary accent plus two supporting fills — within the
 * direction cap (React/Sections/DESIGN_TOKENS.md §4.5).
 */

export interface HeroAction {
  label: string;
  href: string;
}

export interface HeroStat {
  value: string;
  label: string;
  tone?: "accent" | "info" | "success";
}

export interface HeroSectionProps {
  eyebrow?: string;
  heading?: string;
  lede?: string;
  primaryAction?: HeroAction;
  secondaryAction?: HeroAction;
  stats?: HeroStat[];
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const NB_ACTION_BASE =
  "inline-flex h-11 items-center justify-center rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] px-5 text-sm font-semibold leading-5 shadow-[4px_4px_0_0_var(--ds-color-border-strong)] transition-[transform,box-shadow] duration-100 ease-out active:translate-x-[4px] active:translate-y-[4px] active:shadow-none motion-reduce:transition-none " +
  FOCUS_RING;

const PRIMARY_ACTION_CLASSES =
  NB_ACTION_BASE +
  " bg-[var(--ds-color-accent)] text-[var(--ds-color-accent-foreground)]";

const SECONDARY_ACTION_CLASSES =
  NB_ACTION_BASE +
  " bg-[var(--ds-color-surface)] text-[var(--ds-color-foreground)]";

const TONE_CLASSES: Record<NonNullable<HeroStat["tone"]>, string> = {
  accent:
    "bg-[var(--ds-color-accent)] text-[var(--ds-color-accent-foreground)]",
  info: "bg-[var(--ds-color-info)] text-[var(--ds-color-info-foreground)]",
  success:
    "bg-[var(--ds-color-success)] text-[var(--ds-color-success-foreground)]",
};

const DEFAULT_STATS: HeroStat[] = [
  { value: "663", label: "Ship-ready snippets", tone: "accent" },
  { value: "12ms", label: "Interaction feedback", tone: "info" },
  { value: "AA", label: "Contrast, every theme", tone: "success" },
];

interface Metric {
  label: string;
  value: string;
}

const PANEL_METRICS: Metric[] = [
  { label: "Variants indexed", value: "663" },
  { label: "Design directions", value: "4" },
  { label: "Token coverage", value: "100%" },
];

export function HeroSection({
  eyebrow = "React Sections",
  heading = "Design with hard edges and honest tokens.",
  lede = "A component library that treats constraints as the feature — square corners, 2px borders, flat color, and a design-token contract that never breaks.",
  primaryAction = { label: "Get the library", href: "#get-started" },
  secondaryAction = { label: "See how it's made", href: "#design-tokens" },
  stats = DEFAULT_STATS,
}: HeroSectionProps) {
  const headingId = useId();
  return (
    <section
      aria-labelledby={headingId}
      className="bg-[var(--ds-color-background)] font-[var(--ds-font-sans)] text-[var(--ds-color-foreground)]"
    >
      <div className="mx-auto max-w-[1280px] px-4 py-[clamp(5rem,3.5rem+6vw,8rem)] sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 gap-8 lg:grid-cols-12 lg:items-start">
          <div className="lg:col-span-7">
            <p className="inline-block rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] bg-[var(--ds-color-surface)] px-3 py-1 font-[var(--ds-font-mono)] text-xs font-semibold uppercase leading-[1.3] tracking-[0.05em] shadow-[4px_4px_0_0_var(--ds-color-border-strong)]">
              {eyebrow}
            </p>
            <h1
              id={headingId}
              className="mt-6 max-w-2xl text-[clamp(2.5rem,1.9rem+2.8vw,3.5rem)] font-bold leading-[1.1] tracking-[-0.02em]"
            >
              {heading}
            </h1>
            <p className="mt-4 max-w-xl text-[clamp(1rem,0.95rem+0.25vw,1.125rem)] leading-[1.5] text-[var(--ds-color-muted-foreground)]">
              {lede}
            </p>
            <div className="mt-8 flex flex-wrap gap-4">
              <a href={primaryAction.href} className={PRIMARY_ACTION_CLASSES}>
                {primaryAction.label}
              </a>
              <a
                href={secondaryAction.href}
                className={SECONDARY_ACTION_CLASSES}
              >
                {secondaryAction.label}
              </a>
            </div>
          </div>

          <div className="lg:col-span-5">
            <div className="rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] bg-[var(--ds-color-surface)] shadow-[8px_8px_0_0_var(--ds-color-border-strong)]">
              <div className="flex items-center justify-between border-b-2 border-[var(--ds-color-border-strong)] px-6 py-4">
                <p className="font-[var(--ds-font-mono)] text-xs font-semibold uppercase leading-[1.4] tracking-[0.05em]">
                  Library metrics
                </p>
                <p className="font-[var(--ds-font-mono)] text-xs uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
                  Q3 2026
                </p>
              </div>
              <dl>
                {PANEL_METRICS.map((metric, index) => (
                  <div
                    key={metric.label}
                    className={
                      "flex items-baseline justify-between gap-4 px-6 py-4" +
                      (index < PANEL_METRICS.length - 1
                        ? " border-b-2 border-[var(--ds-color-border-strong)]"
                        : "")
                    }
                  >
                    <dt className="text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
                      {metric.label}
                    </dt>
                    <dd className="font-[var(--ds-font-mono)] text-sm font-semibold leading-5 tabular-nums">
                      {metric.value}
                    </dd>
                  </div>
                ))}
              </dl>
            </div>
          </div>
        </div>

        <div className="mt-12 grid grid-cols-1 gap-6 sm:grid-cols-3">
          {stats.map((stat) => (
            <div
              key={stat.label}
              className={
                "rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] px-6 py-5 shadow-[4px_4px_0_0_var(--ds-color-border-strong)] " +
                TONE_CLASSES[stat.tone ?? "accent"]
              }
            >
              <p className="text-[clamp(1.75rem,1.5rem+1.2vw,2.25rem)] font-bold leading-[1.2] tracking-[-0.02em] tabular-nums">
                {stat.value}
              </p>
              <p className="mt-1 font-[var(--ds-font-mono)] text-xs uppercase leading-[1.4] tracking-[0.05em]">
                {stat.label}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
