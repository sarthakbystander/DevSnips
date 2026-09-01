import { useId } from "react";

/**
 * DevSnips React Stats — Neo-Brutalist direction.
 *
 * The expressive ceiling, kept disciplined (§4.5): four square stat blocks
 * with uniform 2px borders and hard 4px offset shadows (zero blur, zero
 * spread), mono uppercase labels, and a 700-weight numerical voice. The
 * one filled block carries the section's accent (warning tokens — AA in
 * both themes) and the press-down action is the second filled element; the
 * other three blocks stay flat surface.
 *
 * Labels are mono uppercase per §4.5; numbers use the exact §5.2
 * `section.stat` scale with `tabular-nums`. The action translates by its
 * shadow offset on :active (≤100ms) — no grow, no glow.
 */

export interface BrutalistStat {
  value: string;
  label: string;
  description: string;
  /** Renders the one allowed flat accent fill (warning tokens). */
  filled?: boolean;
}

export interface StatsSectionProps {
  eyebrow?: string;
  heading?: string;
  lede?: string;
  stats?: BrutalistStat[];
  actionLabel?: string;
  actionHref?: string;
}

const ACTION_CLASSES =
  "mt-8 inline-flex h-11 items-center justify-center rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] bg-[var(--ds-color-primary)] px-5 text-sm font-semibold leading-5 text-[var(--ds-color-primary-foreground)] shadow-[4px_4px_0_0_var(--ds-color-border-strong)] transition-[transform,box-shadow] duration-100 ease-out active:translate-x-[4px] active:translate-y-[4px] active:shadow-none motion-reduce:transition-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const DEFAULT_STATS: BrutalistStat[] = [
  {
    value: "31",
    label: "Edge regions",
    description: "Storage and compute sit next to your users.",
  },
  {
    value: "42ms",
    label: "p95 read latency",
    description: "Object key to first byte, at the edge.",
  },
  {
    value: "99.99%",
    label: "Uptime, trailing 90 days",
    description: "Published per region on the public status page.",
    filled: true,
  },
  {
    value: "4.2B",
    label: "Objects under management",
    description: "Deduplicated, versioned, restorable to the minute.",
  },
];

export function StatsSection({
  eyebrow = "Bulkhead in numbers",
  heading = "Flat storage numbers. No asterisks.",
  lede = "Bulkhead stores build artifacts and serves them from the edge. These are the operating figures we print on the door — read the report if you want the long division.",
  stats = DEFAULT_STATS,
  actionLabel = "Read the status report",
  actionHref = "#status",
}: StatsSectionProps) {
  const headingId = useId();
  return (
    <section
      aria-labelledby={headingId}
      className="bg-[var(--ds-color-background)] font-[var(--ds-font-sans)] text-[var(--ds-color-foreground)]"
    >
      <div className="mx-auto max-w-[1280px] px-4 py-[clamp(4rem,3rem+4vw,6rem)] sm:px-6 lg:px-8">
        <div className="max-w-2xl">
          <p className="inline-block rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] bg-[var(--ds-color-surface)] px-3 py-1 font-[var(--ds-font-mono)] text-xs font-semibold uppercase leading-[1.3] tracking-[0.05em] shadow-[4px_4px_0_0_var(--ds-color-border-strong)]">
            {eyebrow}
          </p>
          <h2
            id={headingId}
            className="mt-6 text-[clamp(1.875rem,1.65rem+1vw,2.25rem)] font-bold leading-[1.15] tracking-[-0.02em]"
          >
            {heading}
          </h2>
          <p className="mt-4 max-w-xl text-[clamp(1rem,0.95rem+0.25vw,1.125rem)] leading-[1.5] text-[var(--ds-color-muted-foreground)]">
            {lede}
          </p>
        </div>

        <ul className="mt-12 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:mt-16 lg:grid-cols-4">
          {stats.map((stat) => (
            <li
              key={stat.label}
              className={
                "rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] p-6 shadow-[4px_4px_0_0_var(--ds-color-border-strong)] sm:p-8 " +
                (stat.filled
                  ? "bg-[var(--ds-color-warning)] text-[var(--ds-color-warning-foreground)]"
                  : "bg-[var(--ds-color-surface)]")
              }
            >
              <p
                className={
                  "font-[var(--ds-font-mono)] text-xs font-semibold uppercase leading-[1.3] tracking-[0.05em] " +
                  (stat.filled
                    ? ""
                    : "text-[var(--ds-color-muted-foreground)]")
                }
              >
                {stat.label}
              </p>
              <p className="mt-4 text-[clamp(1.75rem,1.5rem+1.2vw,2.25rem)] font-bold leading-[1.2] tracking-[-0.02em] tabular-nums">
                {stat.value}
              </p>
              <p className="mt-2 text-sm font-medium leading-5">
                {stat.description}
              </p>
            </li>
          ))}
        </ul>

        <a href={actionHref} className={ACTION_CLASSES}>
          {actionLabel}
        </a>
      </div>
    </section>
  );
}
