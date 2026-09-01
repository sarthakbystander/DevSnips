import { useId } from "react";

/**
 * DevSnips React Features — Split composition (Dark Premium direction).
 *
 * A product-focused 6/6 split: feature copy on the left (heading, lede,
 * three icon-marked rows), a live-feel queue-depth panel on the right. The
 * section pins the dark theme mapping with `data-theme="dark"` on its own
 * root, so it consumes the same semantic tokens in both page themes — a
 * theme mapping, not a hard-coded dark page (§4.3).
 *
 * Surfaces lift exactly one step above the canvas via a 1px border; no
 * shadows, no glow, no mesh. One accent: the primary CTA and the panel's
 * bar series. The panel is a decorative artifact and is `aria-hidden`.
 */

export interface SplitFeature {
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
  features?: SplitFeature[];
  primaryAction?: FeatureAction;
  secondaryAction?: FeatureAction;
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const PRIMARY_ACTION_CLASSES =
  "inline-flex h-11 items-center justify-center rounded-[var(--ds-radius-sm)] bg-[var(--ds-color-primary)] px-5 text-sm font-semibold leading-5 text-[var(--ds-color-primary-foreground)] transition-colors duration-150 ease-out hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)] motion-reduce:transition-none " +
  FOCUS_RING;

const SECONDARY_ACTION_CLASSES =
  "inline-flex h-11 items-center justify-center rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border-strong)] px-5 text-sm font-semibold leading-5 text-[var(--ds-color-foreground)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] motion-reduce:transition-none " +
  FOCUS_RING;

const DEFAULT_FEATURES: SplitFeature[] = [
  {
    title: "Sub-millisecond edge reads",
    description:
      "Queues are materialized at every point of presence, so consumers read from the edge they connected to — not from a region an ocean away.",
  },
  {
    title: "Backpressure you can see",
    description:
      "Per-consumer lag is a first-class metric with its own chart, alerting threshold, and scaling hook, not a number buried in logs.",
  },
  {
    title: "Exactly-once semantics",
    description:
      "Delivery is deduplicated end to end; consumer restarts and redeliveries never apply the same message twice.",
  },
];

interface QueueRow {
  label: string;
  value: string;
}

const QUEUE_ROWS: QueueRow[] = [
  { label: "Messages in flight", value: "18,204" },
  { label: "Oldest unconsumed", value: "0.8s" },
  { label: "Consumer lag p99", value: "41ms" },
];

const QUEUE_BARS: number[] = [34, 28, 41, 36, 52, 44, 61, 49, 66, 58, 47, 72];

function RowIcon() {
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

/**
 * Decorative queue-depth panel. Renders identical text content to plain
 * DOM; hidden from assistive technology so the feature copy stays the sole
 * source of meaning.
 */
function QueuePanel() {
  return (
    <figure
      aria-hidden="true"
      className="rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-6 lg:p-8"
    >
      <div className="flex items-center justify-between gap-4">
        <p className="font-[var(--ds-font-mono)] text-xs font-medium uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
          Queue depth · us-east
        </p>
        <p className="rounded-[var(--ds-radius-full)] border border-[var(--ds-color-border)] px-3 py-1 text-xs font-medium leading-[1.4] text-[var(--ds-color-muted-foreground)]">
          Draining
        </p>
      </div>
      <svg viewBox="0 0 320 96" className="mt-6 h-20 w-full">
        {QUEUE_BARS.map((height, index) => (
          <rect
            key={index}
            x={index * 27 + 2}
            y={88 - height}
            width="18"
            height={height}
            rx="2"
            fill="currentColor"
            className="text-[var(--ds-color-accent)]"
          />
        ))}
        <line
          x1="0"
          y1="90"
          x2="320"
          y2="90"
          stroke="currentColor"
          strokeWidth="1"
          className="text-[var(--ds-color-border)]"
        />
      </svg>
      <dl className="mt-6 divide-y divide-[var(--ds-color-border-subtle)] border-t border-[var(--ds-color-border-subtle)]">
        {QUEUE_ROWS.map((row) => (
          <div
            key={row.label}
            className="flex items-baseline justify-between gap-4 py-3"
          >
            <dt className="text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
              {row.label}
            </dt>
            <dd className="font-[var(--ds-font-mono)] text-sm font-medium leading-5 tabular-nums text-[var(--ds-color-foreground)]">
              {row.value}
            </dd>
          </div>
        ))}
      </dl>
    </figure>
  );
}

export function FeaturesSection({
  eyebrow = "Edge message queue",
  heading = "Your queue should live where your users do.",
  lede = "Relay runs durable message queues at the edge, with the delivery guarantees of a regional broker and the latency of a local read.",
  features = DEFAULT_FEATURES,
  primaryAction = { label: "Create a queue", href: "#get-started" },
  secondaryAction = { label: "Benchmarks", href: "#benchmarks" },
}: FeaturesSectionProps) {
  const headingId = useId();
  return (
    <section
      data-theme="dark"
      aria-labelledby={headingId}
      className="bg-[var(--ds-color-background)] font-[var(--ds-font-sans)] text-[var(--ds-color-foreground)]"
    >
      <div className="mx-auto max-w-[1280px] px-4 py-[clamp(4rem,3rem+4vw,6rem)] sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 items-center gap-12 lg:grid-cols-12 lg:gap-8">
          <div className="max-w-xl lg:col-span-6">
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
            <ul className="mt-10 space-y-6">
              {features.map((feature) => (
                <li key={feature.title} className="flex gap-3">
                  <RowIcon />
                  <div>
                    <h3 className="text-base font-semibold leading-6">
                      {feature.title}
                    </h3>
                    <p className="mt-1 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
                      {feature.description}
                    </p>
                  </div>
                </li>
              ))}
            </ul>
            <div className="mt-10 flex flex-col gap-3 sm:flex-row">
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
          <div className="lg:col-span-6">
            <QueuePanel />
          </div>
        </div>
      </div>
    </section>
  );
}
