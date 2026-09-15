import { useId } from "react";

/**
 * DevSnips React Stats — Dark Premium direction.
 *
 * An asymmetric 4/8 editorial split on a pinned dark canvas (§4.3, §10.2):
 * the header block and one quiet link sit left; a single raised telemetry
 * panel sits right, one elevation step above the canvas with a 1px border
 * and no shadow. The panel leads with two featured metrics, then a ruled
 * definition list of secondary latency and delivery numbers.
 *
 * The section pins `data-theme="dark"` on its own root, so it consumes the
 * same semantic tokens in both page themes — a theme mapping, not a
 * hard-coded dark page. One accent, spent exactly twice per §3.6: the
 * uptime figure (the one data highlight) and the link. No glow, no mesh,
 * no gradients.
 */

export interface FeaturedStat {
  value: string;
  label: string;
  context: string;
  accent?: boolean;
}

export interface RateStat {
  label: string;
  value: string;
}

export interface StatsSectionProps {
  eyebrow?: string;
  heading?: string;
  lede?: string;
  linkLabel?: string;
  linkHref?: string;
  panelCaption?: string;
  featured?: FeaturedStat[];
  rates?: RateStat[];
}

const LINK_CLASSES =
  "mt-6 inline-flex items-center rounded-[var(--ds-radius-sm)] text-sm font-medium leading-5 text-[var(--ds-color-link)] underline underline-offset-4 transition-colors duration-150 ease-out hover:text-[var(--ds-color-link-hover)] motion-reduce:transition-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const DEFAULT_FEATURED: FeaturedStat[] = [
  {
    value: "4.8B",
    label: "Requests processed in the last 30 days",
    context: "Across 62 edge regions",
  },
  {
    value: "99.995%",
    label: "Uptime, trailing 12 months",
    context: "All customer-facing write paths",
    accent: true,
  },
];

const DEFAULT_RATES: RateStat[] = [
  { label: "p99 authorization latency", value: "82ms" },
  { label: "p99 capture latency", value: "141ms" },
  { label: "Webhook delivery success", value: "99.98%" },
  { label: "Tokens in rotation", value: "2.4M" },
];

export function StatsSection({
  eyebrow = "Ledgerline telemetry",
  heading = "Payments infrastructure, measured in the open.",
  lede = "Ledgerline moves money between ledgers. Every number here is computed from production traffic and published monthly — the same figures our own team runs on.",
  linkLabel = "Read the latest monthly telemetry report",
  linkHref = "#telemetry",
  panelCaption = "Telemetry — last 24 hours",
  featured = DEFAULT_FEATURED,
  rates = DEFAULT_RATES,
}: StatsSectionProps) {
  const headingId = useId();
  return (
    <section
      data-theme="dark"
      aria-labelledby={headingId}
      className="bg-[var(--ds-color-background)] font-[var(--ds-font-sans)] text-[var(--ds-color-foreground)]"
    >
      <div className="mx-auto max-w-[1280px] px-4 py-[clamp(4rem,3rem+4vw,6rem)] sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 gap-8 lg:grid-cols-12">
          <div className="lg:col-span-4">
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
            <a href={linkHref} className={LINK_CLASSES}>
              {linkLabel}
            </a>
          </div>

          <div className="rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-6 lg:col-span-8 lg:p-8">
            <p className="font-[var(--ds-font-mono)] text-xs font-medium uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
              {panelCaption}
            </p>
            <div className="mt-6 grid grid-cols-1 gap-6 border-t border-[var(--ds-color-border-subtle)] pt-6 sm:grid-cols-2 sm:gap-8">
              {featured.map((stat) => (
                <div key={stat.label}>
                  <p
                    className={
                      "text-[clamp(1.75rem,1.5rem+1.2vw,2.25rem)] font-semibold leading-[1.2] tracking-[-0.02em] tabular-nums " +
                      (stat.accent
                        ? "text-[var(--ds-color-accent)]"
                        : "text-[var(--ds-color-foreground)]")
                    }
                  >
                    {stat.value}
                  </p>
                  <p className="mt-2 text-sm leading-5">
                    {stat.label}
                  </p>
                  <p className="mt-1 font-[var(--ds-font-mono)] text-xs leading-[1.4] text-[var(--ds-color-muted-foreground)]">
                    {stat.context}
                  </p>
                </div>
              ))}
            </div>
            <dl className="mt-6 divide-y divide-[var(--ds-color-border-subtle)] border-t border-[var(--ds-color-border-subtle)]">
              {rates.map((rate) => (
                <div
                  key={rate.label}
                  className="flex items-baseline justify-between gap-4 py-4"
                >
                  <dt className="text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
                    {rate.label}
                  </dt>
                  <dd className="font-[var(--ds-font-mono)] text-sm font-medium leading-5 tabular-nums">
                    {rate.value}
                  </dd>
                </div>
              ))}
            </dl>
          </div>
        </div>
      </div>
    </section>
  );
}
