import { useId } from "react";
import type { ComponentType } from "react";

/**
 * DevSnips React Features — Alternating composition (Minimal direction).
 *
 * An editorial walk through three features: each row is a 5/7 split of 12
 * with copy on one side and a bordered product artifact on the other,
 * alternating sides per row (§10.2). Rows stack copy-first below lg
 * (§12.2). Artifacts reserve their aspect ratio so the layout never shifts
 * (§16) and are `aria-hidden` — the copy carries all meaning.
 *
 * One accent, spent on the single docs link in the header. Artifacts stay
 * monochrome: hairline borders and muted strokes, no shadows.
 */

export interface AlternatingFeature {
  title: string;
  description: string;
  points: string[];
  artifact: "waterfall" | "chart" | "log";
}

export interface FeaturesSectionProps {
  eyebrow?: string;
  heading?: string;
  lede?: string;
  features?: AlternatingFeature[];
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const LINK_CLASSES =
  "text-sm font-semibold leading-5 text-[var(--ds-color-link)] underline underline-offset-4 transition-colors duration-150 ease-out hover:text-[var(--ds-color-link-hover)] motion-reduce:transition-none " +
  FOCUS_RING;

const ARTIFACT_CLASSES =
  "aspect-[4/3] w-full overflow-hidden rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-6";

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

/** Span waterfall for the tracing row. Decorative, hidden from AT. */
function WaterfallArtifact() {
  const spans: Array<[number, number, number]> = [
    [12, 44, 26],
    [32, 22, 52],
    [60, 30, 78],
    [98, 18, 104],
    [140, 36, 130],
    [186, 16, 156],
  ];
  return (
    <svg
      viewBox="0 0 320 208"
      className="h-full w-full"
      fill="none"
      aria-hidden="true"
    >
      {spans.map(([y, width, x], index) => (
        <g key={y}>
          <line
            x1="12"
            y1={y + 4}
            x2="308"
            y2={y + 4}
            stroke="currentColor"
            strokeWidth="1"
            className="text-[var(--ds-color-border-subtle)]"
          />
          <rect
            x={x}
            y={y}
            width={width}
            height="8"
            rx="2"
            className={
              index === 4
                ? "fill-[var(--ds-color-foreground)]"
                : "fill-[var(--ds-color-border-strong)]"
            }
          />
        </g>
      ))}
    </svg>
  );
}

/** Latency chart for the metrics row. Decorative, hidden from AT. */
function ChartArtifact() {
  return (
    <svg
      viewBox="0 0 320 208"
      className="h-full w-full"
      fill="none"
      stroke="currentColor"
      aria-hidden="true"
    >
      {[40, 88, 136, 184].map((y) => (
        <line
          key={y}
          x1="12"
          y1={y}
          x2="308"
          y2={y}
          strokeWidth="1"
          className="text-[var(--ds-color-border-subtle)]"
        />
      ))}
      <polyline
        points="12,150 52,140 92,146 132,110 172,116 212,84 252,92 308,60"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        className="text-[var(--ds-color-foreground)]"
      />
      <polyline
        points="12,168 52,162 92,166 132,150 172,154 212,138 252,144 308,126"
        strokeWidth="1.5"
        strokeDasharray="4 4"
        strokeLinecap="round"
        strokeLinejoin="round"
        className="text-[var(--ds-color-muted-foreground)]"
      />
    </svg>
  );
}

/** Log tail for the alerting row. Decorative, hidden from AT. */
function LogArtifact() {
  const lines: Array<[string, string]> = [
    ["12:04:11", "GET /checkout 200 in 84ms"],
    ["12:04:12", "POST /payments 201 in 121ms"],
    ["12:04:14", "GET /checkout 200 in 79ms"],
    ["12:04:15", "POST /payments 503 in 4ms"],
    ["12:04:15", "alert: error budget burn 2.1x"],
    ["12:04:17", "GET /health 200 in 3ms"],
  ];
  return (
    <div aria-hidden="true" className="flex h-full flex-col justify-center">
      {lines.map(([time, message]) => (
        <p
          key={time + message}
          className="truncate py-1.5 font-[var(--ds-font-mono)] text-xs leading-[1.4] text-[var(--ds-color-muted-foreground)]"
        >
          <span className="text-[var(--ds-color-foreground)]">{time}</span>
          {"  "}
          {message}
        </p>
      ))}
    </div>
  );
}

const ARTIFACTS: Record<AlternatingFeature["artifact"], ComponentType> = {
  waterfall: WaterfallArtifact,
  chart: ChartArtifact,
  log: LogArtifact,
};

const DEFAULT_FEATURES: AlternatingFeature[] = [
  {
    title: "Traces that follow the whole request",
    description:
      "One trace ID threads through every service, queue, and function the request touches — no stitching spans together by hand.",
    points: [
      "Automatic instrumentation for HTTP, gRPC, and common queue clients",
      "Tail-based sampling keeps the interesting 2% at full fidelity",
      "Span links connect async work back to its originating request",
    ],
    artifact: "waterfall",
  },
  {
    title: "Metrics with honest baselines",
    description:
      "Latency, saturation, and error rates are compared against the same window last week, so regressions stand out from normal load.",
    points: [
      "p50, p95, and p99 recorded per endpoint, per region",
      "Seasonal baselines update nightly from your own traffic",
      "Dashboards are generated from the alerting rules, not by hand",
    ],
    artifact: "chart",
  },
  {
    title: "Alerts that page for a reason",
    description:
      "Alerting runs on error budgets, not static thresholds — a page means users are actually affected, and it says why.",
    points: [
      "Burn-rate windows catch slow leaks and sudden spikes alike",
      "Every alert links the exact log lines that triggered it",
      "Routing rules send pages to the team that owns the service",
    ],
    artifact: "log",
  },
];

export function FeaturesSection({
  eyebrow = "Observability",
  heading = "See what production is doing, and why.",
  lede = "Tracepoint brings traces, metrics, and alerting into one workflow, built for teams who read dashboards during incidents, not after them.",
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
          <p className="mt-6">
            <a href="#docs" className={LINK_CLASSES}>
              Read the instrumentation guide
            </a>
          </p>
        </div>

        <div className="mt-12 space-y-16 lg:mt-16 lg:space-y-24">
          {features.map((feature, index) => {
            const Artifact = ARTIFACTS[feature.artifact];
            return (
              <div
                key={feature.title}
                className="grid grid-cols-1 items-center gap-8 lg:grid-cols-12 lg:gap-12"
              >
                <div
                  className={
                    "lg:col-span-5" + (index % 2 === 1 ? " lg:order-2" : "")
                  }
                >
                  <h3 className="text-2xl font-semibold leading-[1.25] tracking-[-0.01em]">
                    {feature.title}
                  </h3>
                  <p className="mt-3 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
                    {feature.description}
                  </p>
                  <ul className="mt-6 space-y-3">
                    {feature.points.map((point) => (
                      <li key={point} className="flex gap-2">
                        <CheckIcon />
                        <span className="text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
                          {point}
                        </span>
                      </li>
                    ))}
                  </ul>
                </div>
                <figure
                  aria-hidden="true"
                  className={"lg:col-span-7" + (index % 2 === 1 ? " lg:order-1" : "")}
                >
                  <div className={ARTIFACT_CLASSES}>
                    <Artifact />
                  </div>
                </figure>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
