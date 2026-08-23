import { useId, useRef, useState } from "react";
import type { KeyboardEvent } from "react";

/**
 * DevSnips React Features — Tabs composition (Minimal direction).
 *
 * An interactive feature showcase: one set of capabilities, four lenses.
 * Real tab semantics (per the React Tabs family): `role="tablist"` with
 * `aria-orientation`, native `<button role="tab">` triggers
 * (`aria-selected` / `aria-controls`, roving `tabIndex`, automatic
 * activation), and `role="tabpanel"` regions labelled by their trigger.
 * Arrow keys and Home/End move between tabs; Tab leaves the widget. Panels
 * stay mounted and toggle with the `hidden` attribute, so nothing inside
 * loses state.
 *
 * Each panel is a 5/7 split: copy with a checklist on the left, a real
 * CLI/code artifact on the right. One accent: the active tab indicator —
 * the only place color carries state, reinforced by `aria-selected`.
 */

export interface TabFeature {
  value: string;
  label: string;
  title: string;
  description: string;
  points: string[];
  snippet: string;
}

export interface FeaturesSectionProps {
  eyebrow?: string;
  heading?: string;
  lede?: string;
  features?: TabFeature[];
  defaultValue?: string;
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const DEFAULT_FEATURES: TabFeature[] = [
  {
    value: "build",
    label: "Build",
    title: "Templates that encode your standards",
    description:
      "New services start from golden-path templates — linting, CI, ownership, and dashboards are already wired in, not copied from a wiki.",
    points: [
      "Software templates versioned like the code they generate",
      "Ownership declared in catalog-info.yaml from day one",
      "Drift reports show which services have fallen behind",
    ],
    snippet: `$ waypoint create --template go-service \\
  --name billing-relay --team payments

ok Scaffolded 14 files from go-service@2.3
ok Registered in the service catalog
ok CI pipeline enabled (build, test, scan)

Open a pull request: git push -u origin main`,
  },
  {
    value: "deploy",
    label: "Deploy",
    title: "Progressive delivery without the YAML",
    description:
      "Rollouts are declared once per environment: canary steps, analysis windows, and automatic rollback when error rates move.",
    points: [
      "Canary and blue-green strategies per environment",
      "Metric-gated promotion using your existing monitors",
      "One-command rollback to any previous release",
    ],
    snippet: `$ waypoint deploy billing-relay \\
  --env production --strategy canary

Step 1/4  5%   analysis 5m   passed
Step 2/4  25%  analysis 5m   passed
Step 3/4  50%  analysis 5m   running…

Rollback at any time: waypoint rollback billing-relay`,
  },
  {
    value: "observe",
    label: "Observe",
    title: "Every service ships with its own dashboard",
    description:
      "The catalog page for a service is its dashboard: golden signals, recent deploys, open incidents, and runbooks in one place.",
    points: [
      "Golden signals scraped and charted automatically",
      "Deploy markers overlaid on every latency chart",
      "Runbooks linked where the alerts land",
    ],
    snippet: `$ waypoint status billing-relay

Service    billing-relay      owner: payments
Latency    p50 21ms  p99 118ms   ▂▃▅▃▂▃
Errors     0.02% of requests    budget: 99.9%
Deploys    6 this week          last: 2h ago
Incidents  none open`,
  },
  {
    value: "scale",
    label: "Scale",
    title: "Capacity that follows the traffic curve",
    description:
      "Autoscaling policies are part of the service definition, reviewed in the same pull request as the code they protect.",
    points: [
      "CPU, queue-depth, and custom-metric scaling signals",
      "Scale-to-zero for preview and batch workloads",
      "Cost per service reported back into the catalog",
    ],
    snippet: `$ waypoint scale billing-relay \\
  --min 2 --max 40 --on queue-depth

Policy applied to production
Current: 4 replicas · target utilisation 70%
Last scale event: +6 replicas, 41 minutes ago`,
  },
];

export function FeaturesSection({
  eyebrow = "Internal developer platform",
  heading = "One platform from first commit to on-call.",
  lede = "Waypoint gives every team the same paved road: scaffold, ship, watch, and scale a service without leaving the catalog.",
  features = DEFAULT_FEATURES,
  defaultValue = DEFAULT_FEATURES[0]?.value,
}: FeaturesSectionProps) {
  const baseId = useId();
  const [active, setActive] = useState(defaultValue);
  const tabRefs = useRef<Array<HTMLButtonElement | null>>([]);

  const activeIndex = Math.max(
    0,
    features.findIndex((feature) => feature.value === active),
  );

  function activate(index: number) {
    const feature = features[index];
    if (!feature) return;
    setActive(feature.value);
    tabRefs.current[index]?.focus();
  }

  function onTabListKeyDown(event: KeyboardEvent<HTMLDivElement>) {
    const last = features.length - 1;
    let next: number | null = null;
    if (event.key === "ArrowRight") next = activeIndex === last ? 0 : activeIndex + 1;
    else if (event.key === "ArrowLeft") next = activeIndex === 0 ? last : activeIndex - 1;
    else if (event.key === "Home") next = 0;
    else if (event.key === "End") next = last;
    if (next !== null) {
      event.preventDefault();
      activate(next);
    }
  }

  return (
    <section
      aria-labelledby={`${baseId}-heading`}
      className="bg-[var(--ds-color-background)] font-[var(--ds-font-sans)] text-[var(--ds-color-foreground)]"
    >
      <div className="mx-auto max-w-[1280px] px-4 py-[clamp(4rem,3rem+4vw,6rem)] sm:px-6 lg:px-8">
        <div className="max-w-2xl">
          <p className="text-xs font-semibold uppercase leading-[1.3] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
            {eyebrow}
          </p>
          <h2
            id={`${baseId}-heading`}
            className="mt-3 text-[clamp(1.875rem,1.65rem+1vw,2.25rem)] font-semibold leading-[1.15] tracking-[-0.02em]"
          >
            {heading}
          </h2>
          <p className="mt-4 text-[clamp(1rem,0.95rem+0.25vw,1.125rem)] leading-[1.5] text-[var(--ds-color-muted-foreground)]">
            {lede}
          </p>
        </div>

        <div className="mt-12 lg:mt-16">
          <div
            role="tablist"
            aria-orientation="horizontal"
            aria-label="Platform capabilities"
            onKeyDown={onTabListKeyDown}
            className="flex gap-6 overflow-x-auto border-b border-[var(--ds-color-border)]"
          >
            {features.map((feature, index) => {
              const selected = index === activeIndex;
              return (
                <button
                  key={feature.value}
                  ref={(node) => {
                    tabRefs.current[index] = node;
                  }}
                  type="button"
                  role="tab"
                  id={`${baseId}-tab-${feature.value}`}
                  aria-selected={selected}
                  aria-controls={`${baseId}-panel-${feature.value}`}
                  tabIndex={selected ? 0 : -1}
                  onClick={() => activate(index)}
                  className={
                    "-mb-px shrink-0 border-b-2 pb-3 text-sm font-medium leading-5 transition-colors duration-150 ease-out motion-reduce:transition-none " +
                    (selected
                      ? "border-[var(--ds-color-primary)] text-[var(--ds-color-foreground)]"
                      : "border-transparent text-[var(--ds-color-muted-foreground)] hover:border-[var(--ds-color-border-strong)] hover:text-[var(--ds-color-foreground)]") +
                    " " +
                    FOCUS_RING
                  }
                >
                  {feature.label}
                </button>
              );
            })}
          </div>

          {features.map((feature, index) => {
            const selected = index === activeIndex;
            return (
              <div
                key={feature.value}
                role="tabpanel"
                id={`${baseId}-panel-${feature.value}`}
                aria-labelledby={`${baseId}-tab-${feature.value}`}
                tabIndex={0}
                hidden={!selected}
                className={
                  // A Tailwind display utility would override the `hidden`
                  // attribute's UA display:none, so the layout class is
                  // conditional instead of the attribute alone.
                  (selected
                    ? "grid grid-cols-1 gap-8 pt-8 lg:grid-cols-12 lg:gap-12 lg:pt-12 "
                    : "hidden ") + FOCUS_RING
                }
              >
                <div className="lg:col-span-5">
                  <h3 className="text-2xl font-semibold leading-[1.25] tracking-[-0.01em]">
                    {feature.title}
                  </h3>
                  <p className="mt-3 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
                    {feature.description}
                  </p>
                  <ul className="mt-6 space-y-3">
                    {feature.points.map((point) => (
                      <li key={point} className="flex gap-2">
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
                        <span className="text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
                          {point}
                        </span>
                      </li>
                    ))}
                  </ul>
                </div>
                <div className="lg:col-span-7">
                  <pre className="overflow-x-auto rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border-subtle)] bg-[var(--ds-color-surface-subtle)] p-4 sm:p-6">
                    <code className="font-[var(--ds-font-mono)] text-xs leading-6 text-[var(--ds-color-foreground)]">
                      {feature.snippet}
                    </code>
                  </pre>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
