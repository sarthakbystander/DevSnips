import { useId } from "react";

/**
 * DevSnips React Hero — Dark Premium direction.
 *
 * A premium dark hero: split composition (5/7 of 12) with the headline block
 * on the left and a bordered product artifact on the right. The section pins
 * itself to the dark theme mapping with `data-theme="dark"` on its root, so
 * it still consumes semantic tokens — no hard-coded palette.
 *
 * One accent per section: the primary CTA and the sparkline stroke in the
 * metric panel. Surfaces lift exactly one step via a 1px border; borders, not
 * shadows or glow, carry the elevation (React/Sections/DESIGN_TOKENS.md §4.3).
 */

export interface HeroAction {
  label: string;
  href: string;
}

export interface HeroSectionProps {
  eyebrow?: string;
  heading?: string;
  lede?: string;
  primaryAction?: HeroAction;
  secondaryAction?: HeroAction;
  proofLogos?: string[];
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const PRIMARY_ACTION_CLASSES =
  "inline-flex h-11 items-center justify-center rounded-[var(--ds-radius-sm)] bg-[var(--ds-color-primary)] px-5 text-sm font-semibold leading-5 text-[var(--ds-color-primary-foreground)] transition-colors duration-150 ease-out hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)] motion-reduce:transition-none " +
  FOCUS_RING;

const SECONDARY_ACTION_CLASSES =
  "inline-flex h-11 items-center justify-center rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border-strong)] px-5 text-sm font-semibold leading-5 text-[var(--ds-color-foreground)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] motion-reduce:transition-none " +
  FOCUS_RING;

const DEFAULT_PROOF_LOGOS = [
  "Northwind Labs",
  "Helio Systems",
  "Flatiron",
  "Sendero",
  "Vantage Works",
];

interface Metric {
  label: string;
  value: string;
}

const PANEL_METRICS: Metric[] = [
  { label: "Deploys per week", value: "1,842" },
  { label: "Median build time", value: "38s" },
  { label: "Bundle delta", value: "-0.4 kB" },
];

/**
 * Decorative product artifact. Renders identical text content to plain DOM;
 * the whole panel is hidden from assistive technology so the headline block
 * stays the sole source of meaning.
 */
function MetricPanel() {
  return (
    <figure
      aria-hidden="true"
      className="rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-6 lg:p-8"
    >
      <div className="flex items-center justify-between gap-4">
        <p className="text-xs font-[var(--ds-font-mono)] uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
          Release pipeline
        </p>
        <p className="rounded-[var(--ds-radius-full)] border border-[var(--ds-color-border)] px-3 py-1 text-xs font-medium leading-[1.4] text-[var(--ds-color-muted-foreground)]">
          Operational
        </p>
      </div>
      <svg viewBox="0 0 320 64" className="mt-6 h-16 w-full">
        <polyline
          points="0,52 32,44 64,46 96,32 128,34 160,22 192,26 224,14 256,18 288,8 320,12"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="text-[var(--ds-color-accent)]"
        />
        {[
          [32, 44],
          [96, 32],
          [160, 22],
          [224, 14],
          [288, 8],
        ].map(([x, y]) => (
          <circle
            key={x}
            cx={x}
            cy={y}
            r="3"
            fill="currentColor"
            className="text-[var(--ds-color-accent)]"
          />
        ))}
      </svg>
      <dl className="mt-6 divide-y divide-[var(--ds-color-border-subtle)] border-t border-[var(--ds-color-border-subtle)]">
        {PANEL_METRICS.map((metric) => (
          <div
            key={metric.label}
            className="flex items-baseline justify-between gap-4 py-3"
          >
            <dt className="text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
              {metric.label}
            </dt>
            <dd className="font-[var(--ds-font-mono)] text-sm font-medium leading-5 tabular-nums text-[var(--ds-color-foreground)]">
              {metric.value}
            </dd>
          </div>
        ))}
      </dl>
    </figure>
  );
}

export function HeroSection({
  eyebrow = "React Sections",
  heading = "Your product deserves a sharper first impression.",
  lede = "Composable hero, feature, and pricing sections with a shared token system — dark surfaces, hairline borders, and hierarchy that reads like a designed page.",
  primaryAction = { label: "Start building", href: "#get-started" },
  secondaryAction = { label: "Explore the library", href: "#library" },
  proofLogos = DEFAULT_PROOF_LOGOS,
}: HeroSectionProps) {
  const headingId = useId();
  return (
    <section
      data-theme="dark"
      aria-labelledby={headingId}
      className="bg-[var(--ds-color-background)] font-[var(--ds-font-sans)] text-[var(--ds-color-foreground)]"
    >
      <div className="mx-auto max-w-[1280px] px-4 py-[clamp(5rem,3.5rem+6vw,8rem)] sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 items-center gap-8 lg:grid-cols-12">
          <div className="max-w-xl lg:col-span-6">
            <p className="text-xs font-semibold uppercase leading-[1.3] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
              {eyebrow}
            </p>
            <h1
              id={headingId}
              className="mt-3 text-[clamp(2.5rem,1.9rem+2.8vw,3.5rem)] font-semibold leading-[1.1] tracking-[-0.02em]"
            >
              {heading}
            </h1>
            <p className="mt-4 text-[clamp(1rem,0.95rem+0.25vw,1.125rem)] leading-[1.5] text-[var(--ds-color-muted-foreground)]">
              {lede}
            </p>
            <div className="mt-8 flex flex-col gap-3 sm:flex-row">
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
            <p className="mt-12 text-xs font-[var(--ds-font-mono)] uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
              Shipping weekly at
            </p>
            <ul className="mt-3 flex flex-wrap items-center gap-x-6 gap-y-2">
              {proofLogos.map((logo) => (
                <li
                  key={logo}
                  className="text-sm font-medium leading-5 text-[var(--ds-color-muted-foreground)]"
                >
                  {logo}
                </li>
              ))}
            </ul>
          </div>
          <div className="lg:col-span-6">
            <MetricPanel />
          </div>
        </div>
      </div>
    </section>
  );
}
