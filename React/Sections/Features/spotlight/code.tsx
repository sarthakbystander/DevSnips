import { useId } from "react";

/**
 * DevSnips React Features — Spotlight composition (Minimal direction).
 *
 * One large featured capability plus a row of supporting ones: a centered
 * header block, a full-width featured panel (5/7 split of 12 inside:
 * copy + a real query-plan artifact), then three supporting features below
 * a single hairline. The featured capability earns its size — it is the
 * product's reason to exist; the supporting row is deliberately quieter
 * (§11.2: one idea per section, expressed at two weights).
 *
 * One accent: the two actions inside the featured panel. The artifact is
 * a code sample — real SQL, mono stack — bordered like every other surface.
 */

export interface SpotlightPoint {
  label: string;
}

export interface SupportingFeature {
  title: string;
  description: string;
}

export interface FeatureAction {
  label: string;
  href: string;
}

export interface FeaturesSectionProps {
  eyebrow?: string;
  heading?: string;
  lede?: string;
  featuredTitle?: string;
  featuredDescription?: string;
  featuredPoints?: SpotlightPoint[];
  primaryAction?: FeatureAction;
  secondaryAction?: FeatureAction;
  features?: SupportingFeature[];
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const PRIMARY_ACTION_CLASSES =
  "inline-flex h-11 items-center justify-center rounded-[var(--ds-radius-sm)] bg-[var(--ds-color-primary)] px-5 text-sm font-semibold leading-5 text-[var(--ds-color-primary-foreground)] transition-colors duration-150 ease-out hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)] motion-reduce:transition-none " +
  FOCUS_RING;

const SECONDARY_ACTION_CLASSES =
  "inline-flex h-11 items-center justify-center rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border-strong)] bg-[var(--ds-color-surface)] px-5 text-sm font-semibold leading-5 text-[var(--ds-color-foreground)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] motion-reduce:transition-none " +
  FOCUS_RING;

const DEFAULT_FEATURED_POINTS: SpotlightPoint[] = [
  { label: "Plans compared against your last 30 days of production traffic" },
  { label: "Index suggestions ship with the estimated read amplification" },
  { label: "Regressions roll back to the previous plan automatically" },
];

const DEFAULT_FEATURES: SupportingFeature[] = [
  {
    title: "Instant branching",
    description:
      "Copy-on-write branches of the full database in under a second, for every pull request and migration rehearsal.",
  },
  {
    title: "Pooled connections",
    description:
      "Transaction-level pooling absorbs serverless fan-out; ten thousand functions share one sane connection budget.",
  },
  {
    title: "Point-in-time recovery",
    description:
      "Continuous WAL archiving restores any second of the last thirty days to a new cluster, rehearsed weekly.",
  },
];

const QUERY_PLAN = `explain (analyze, buffers)
select o.id, sum(o.total_cents)
from orders o
join customers c on c.id = o.customer_id
where c.region = 'emea'
  and o.created_at > now() - interval '30 days'
group by o.id
order by 2 desc
limit 50;

-- Seq Scan on orders  (cost=0.00..18124.00)
--   Filter: created_at > ...
--   Buffers: shared hit=412 read=11880
--
-- Querybase suggests:
--   create index concurrently idx_orders_created
--     on orders (created_at);`;

function CheckIcon() {
  return (
    <svg
      aria-hidden="true"
      viewBox="0 0 16 16"
      className="mt-1 h-4 w-4 shrink-0 text-[var(--ds-color-muted-foreground)]"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="m3.5 8.5 2.5 2.5 6.5-6.5" />
    </svg>
  );
}

export function FeaturesSection({
  eyebrow = "Managed Postgres",
  heading = "The database is the product. Act like it.",
  lede = "Querybase runs Postgres for teams that read query plans: branching, pooling, and recovery are table stakes — the query analyzer is the reason to switch.",
  featuredTitle = "A query analyzer that has seen your traffic",
  featuredDescription = "Every plan is explained against real production behavior, not a guess. When a deploy makes a query slower, you find out before your users do.",
  featuredPoints = DEFAULT_FEATURED_POINTS,
  primaryAction = { label: "Analyze a query", href: "#get-started" },
  secondaryAction = { label: "See a sample report", href: "#sample-report" },
  features = DEFAULT_FEATURES,
}: FeaturesSectionProps) {
  const headingId = useId();
  return (
    <section
      aria-labelledby={headingId}
      className="bg-[var(--ds-color-background)] font-[var(--ds-font-sans)] text-[var(--ds-color-foreground)]"
    >
      <div className="mx-auto max-w-[1280px] px-4 py-[clamp(4rem,3rem+4vw,6rem)] sm:px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
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

        <div className="mt-12 rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] lg:mt-16">
          <div className="grid grid-cols-1 gap-8 p-6 sm:p-8 lg:grid-cols-12 lg:gap-12 lg:p-12">
            <div className="lg:col-span-5">
              <h3 className="text-2xl font-semibold leading-[1.25] tracking-[-0.01em]">
                {featuredTitle}
              </h3>
              <p className="mt-3 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
                {featuredDescription}
              </p>
              <ul className="mt-6 space-y-3">
                {featuredPoints.map((point) => (
                  <li key={point.label} className="flex gap-2">
                    <CheckIcon />
                    <span className="text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
                      {point.label}
                    </span>
                  </li>
                ))}
              </ul>
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
            </div>
            <div className="lg:col-span-7">
              <pre className="h-full overflow-x-auto rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border-subtle)] bg-[var(--ds-color-surface-subtle)] p-4 sm:p-6">
                <code className="font-[var(--ds-font-mono)] text-xs leading-6 text-[var(--ds-color-foreground)]">
                  {QUERY_PLAN}
                </code>
              </pre>
            </div>
          </div>
        </div>

        <div className="mt-12 grid grid-cols-1 gap-x-8 gap-y-10 border-t border-[var(--ds-color-border)] pt-12 sm:grid-cols-3 lg:mt-16 lg:pt-16">
          {features.map((feature) => (
            <div key={feature.title}>
              <h3 className="text-base font-semibold leading-6">
                {feature.title}
              </h3>
              <p className="mt-2 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
