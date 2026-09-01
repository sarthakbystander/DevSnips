import { useId } from "react";

/**
 * DevSnips React Stats — Minimal direction (the reference composition).
 *
 * A left-aligned header block above a ruled stat rail (§4.2): four metrics
 * in one hairline-separated list — a horizontal divider stack on mobile,
 * vertical hairline dividers between columns at lg. No cards, no fills, no
 * effects; the design is the spacing (§6) and the numerical hierarchy from
 * `section.stat` + mono labels alone (§5.2–§5.3).
 *
 * The strip is a compact section, so it uses the compact rhythm
 * (`section.padding-y` compact, §8). Every metric carries a label and one
 * line of honest context — no bare numbers. Static by design: nothing
 * here is interactive.
 */

export interface StatItem {
  value: string;
  label: string;
  description: string;
}

export interface StatsSectionProps {
  eyebrow?: string;
  heading?: string;
  lede?: string;
  stats?: StatItem[];
}

const DEFAULT_STATS: StatItem[] = [
  {
    value: "1.2B",
    label: "API requests per month",
    description: "Counted, billed, and explainable down to the endpoint.",
  },
  {
    value: "42ms",
    label: "p95 ingest latency",
    description: "From edge collector to queriable metric, last 24 hours.",
  },
  {
    value: "99.99%",
    label: "Uptime, trailing 12 months",
    description: "One 42-minute incident in May, with a public postmortem.",
  },
  {
    value: "8,400",
    label: "Teams metering in production",
    description: "From two-person shops to public usage-based billers.",
  },
];

export function StatsSection({
  eyebrow = "Meterline in numbers",
  heading = "The metering numbers, in the open.",
  lede = "Meterline measures API traffic for teams that bill on it. These are the operating numbers we publish every quarter, not a marketing page.",
  stats = DEFAULT_STATS,
}: StatsSectionProps) {
  const headingId = useId();
  return (
    <section
      aria-labelledby={headingId}
      className="bg-[var(--ds-color-background)] font-[var(--ds-font-sans)] text-[var(--ds-color-foreground)]"
    >
      <div className="mx-auto max-w-[1280px] px-4 py-[clamp(2.5rem,2rem+2vw,4rem)] sm:px-6 lg:px-8">
        <div className="max-w-2xl">
          <p className="text-xs font-semibold uppercase leading-[1.3] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
            {eyebrow}
          </p>
          <h2
            id={headingId}
            className="mt-3 text-[clamp(1.875rem,1.65rem+1vw,2.25rem)] font-semibold leading-[1.15] tracking-[-0.02em]"
          >
            {heading}
          </h2>
          <p className="mt-4 text-[clamp(1rem,0.95rem+0.25vw,1.125rem)] leading-[1.5] text-[var(--ds-color-muted-foreground)]">
            {lede}
          </p>
        </div>

        <ul className="mt-12 grid grid-cols-1 divide-y divide-[var(--ds-color-border)] border-y border-[var(--ds-color-border)] lg:mt-16 lg:grid-cols-4 lg:divide-x lg:divide-y-0">
          {stats.map((stat) => (
            <li key={stat.label} className="py-6 lg:px-8 lg:py-8 lg:first:pl-0 lg:last:pr-0">
              <p className="text-[clamp(1.75rem,1.5rem+1.2vw,2.25rem)] font-semibold leading-[1.2] tracking-[-0.02em] tabular-nums">
                {stat.value}
              </p>
              <p className="mt-2 font-[var(--ds-font-mono)] text-xs font-medium uppercase leading-[1.3] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
                {stat.label}
              </p>
              <p className="mt-3 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
                {stat.description}
              </p>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
