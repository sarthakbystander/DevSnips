import { useId } from "react";

/**
 * DevSnips React Features — Bento composition (Bento direction).
 *
 * A modular 12-column cell grid for 5–8 mixed-weight features (§11.3):
 * one hero cell (span 7) with a small routing diagram, one stat cell
 * (span 5), and four single-idea supporting cells (span 3 each).
 * Cells share one radius (radius-lg), one 1px border, and a uniform gap
 * (16px mobile / 24px desktop). Collapse: authored spans at lg, the two
 * large cells span both columns at sm, everything stacks below (§4.4, §12.2).
 *
 * The accent budget is spent in exactly one place: the stat number. Hover
 * is a border-strong lift only — no scale, no glow. The diagram is
 * decorative and `aria-hidden`.
 */

export interface BentoFeature {
  title: string;
  description: string;
}

export interface FeaturesSectionProps {
  eyebrow?: string;
  heading?: string;
  lede?: string;
  heroFeature?: BentoFeature;
  stat?: { value: string; label: string };
  features?: BentoFeature[];
}

const CELL_CLASSES =
  "rounded-[var(--ds-radius-lg)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-6 transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] motion-reduce:transition-none lg:p-8";

const CELL_TITLE_CLASSES = "text-base font-semibold leading-6";
const CELL_BODY_CLASSES =
  "mt-2 text-sm leading-5 text-[var(--ds-color-muted-foreground)]";

const DEFAULT_HERO_FEATURE: BentoFeature = {
  title: "Exactly-once delivery, end to end",
  description:
    "Every event is deduplicated at ingest and acknowledged at the subscriber, so consumers never apply the same change twice.",
};

const DEFAULT_FEATURES: BentoFeature[] = [
  {
    title: "Schema validation",
    description:
      "Producers publish against versioned schemas; invalid payloads are rejected at the edge, never in your consumer.",
  },
  {
    title: "Replay and backfill",
    description:
      "Rewind any topic to a point in time and re-deliver to a staging subscriber without touching production.",
  },
  {
    title: "Regional routing",
    description:
      "Events are pinned to the region that owns the data, with cross-region failover you configure once.",
  },
  {
    title: "Audit log",
    description:
      "Every publish, redelivery, and schema change is recorded with actor and timestamp for compliance review.",
  },
];

/**
 * Decorative routing diagram: one ingest node fanning out to three labeled
 * subscriber nodes. Pure SVG, hidden from assistive technology.
 */
function RoutingDiagram() {
  const links = [
    { y: 24, label: "api" },
    { y: 72, label: "workers" },
    { y: 120, label: "cdn" },
  ];
  return (
    <svg
      aria-hidden="true"
      viewBox="0 0 360 144"
      className="mt-8 h-28 w-full max-w-md"
      fill="none"
      strokeWidth="1.5"
    >
      {links.map((link, index) => (
        <path
          key={link.label}
          d={
            index === 1
              ? "M92 72h176"
              : `M92 72c60 0 60 ${link.y - 72} 176 ${link.y - 72}`
          }
          stroke="currentColor"
          className="text-[var(--ds-color-border-strong)]"
        />
      ))}
      <g className="fill-[var(--ds-color-surface)] stroke-[var(--ds-color-border-strong)]">
        <rect x="8" y="60" width="84" height="24" rx="4" />
        {links.map((link) => (
          <rect
            key={link.label}
            x="268"
            y={link.y - 12}
            width="84"
            height="24"
            rx="4"
          />
        ))}
      </g>
      <g
        stroke="none"
        className="fill-[var(--ds-color-muted-foreground)]"
        fontSize="10"
        fontFamily="ui-monospace, monospace"
      >
        <text x="20" y="75">
          ingest
        </text>
        {links.map((link) => (
          <text key={link.label} x="280" y={link.y + 3}>
            {link.label}
          </text>
        ))}
      </g>
    </svg>
  );
}

export function FeaturesSection({
  eyebrow = "Event pipeline",
  heading = "One pipeline for every event your product emits.",
  lede = "Conduit moves events from producers to consumers with the guarantees your downstream systems actually need.",
  heroFeature = DEFAULT_HERO_FEATURE,
  stat = { value: "99.99%", label: "Successful deliveries over the last 90 days" },
  features = DEFAULT_FEATURES,
}: FeaturesSectionProps) {
  const headingId = useId();
  return (
    <section
      aria-labelledby={headingId}
      className="bg-[var(--ds-color-background)] font-[var(--ds-font-sans)] text-[var(--ds-color-foreground)]"
    >
      <div className="mx-auto max-w-[1280px] px-4 py-[clamp(4rem,3rem+4vw,6rem)] sm:px-6 lg:px-8">
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

        <div className="mt-12 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:mt-16 lg:grid-cols-12 lg:gap-6">
          <div className={CELL_CLASSES + " sm:col-span-2 lg:col-span-7"}>
            <p className="text-xs font-[var(--ds-font-mono)] uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
              Delivery guarantees
            </p>
            <h3 className="mt-2 text-2xl font-semibold leading-[1.25] tracking-[-0.01em]">
              {heroFeature.title}
            </h3>
            <p className="mt-2 max-w-md text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
              {heroFeature.description}
            </p>
            <RoutingDiagram />
          </div>

          <div className={CELL_CLASSES + " sm:col-span-2 lg:col-span-5"}>
            <p className="text-[clamp(1.75rem,1.5rem+1.2vw,2.25rem)] font-semibold leading-[1.2] tracking-[-0.02em] tabular-nums text-[var(--ds-color-accent)]">
              {stat.value}
            </p>
            <p className="mt-2 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
              {stat.label}
            </p>
            <p className="mt-6 text-xs font-[var(--ds-font-mono)] uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
              Measured across all regions
            </p>
          </div>

          {features.map((feature) => (
            <div key={feature.title} className={CELL_CLASSES + " lg:col-span-3"}>
              <h3 className={CELL_TITLE_CLASSES}>{feature.title}</h3>
              <p className={CELL_BODY_CLASSES}>{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
