import { useId } from "react";
import type { ReactNode } from "react";

/**
 * DevSnips React Features — Grid composition (Minimal direction).
 *
 * The reference composition for the Features family: a left-aligned header
 * block (eyebrow + heading + lede) above an even six-item grid
 * (3 columns at lg, 2 at sm, 1 below — §12.2). Separation comes from
 * whitespace and the items' own rhythm, not from cards: the Minimal
 * direction lets content sit directly on the canvas (§4.2).
 *
 * Each item is icon + title + one-sentence description (§11.3). Icons are
 * decorative — the title carries the meaning — so they are `aria-hidden`.
 * One accent: the two actions below the grid. Everything else is neutral.
 */

export interface FeatureAction {
  label: string;
  href: string;
}

export type FeatureIconName =
  | "parallel"
  | "deterministic"
  | "cache"
  | "preview"
  | "rollback"
  | "analytics";

export interface GridFeature {
  icon: FeatureIconName;
  title: string;
  description: string;
}

export interface FeaturesSectionProps {
  eyebrow?: string;
  heading?: string;
  lede?: string;
  features?: GridFeature[];
  primaryAction?: FeatureAction;
  secondaryAction?: FeatureAction;
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const PRIMARY_ACTION_CLASSES =
  "inline-flex h-11 items-center justify-center rounded-[var(--ds-radius-sm)] bg-[var(--ds-color-primary)] px-5 text-sm font-semibold leading-5 text-[var(--ds-color-primary-foreground)] transition-colors duration-150 ease-out hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)] motion-reduce:transition-none " +
  FOCUS_RING;

const SECONDARY_ACTION_CLASSES =
  "inline-flex h-11 items-center justify-center rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border-strong)] bg-[var(--ds-color-surface)] px-5 text-sm font-semibold leading-5 text-[var(--ds-color-foreground)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] motion-reduce:transition-none " +
  FOCUS_RING;

const ICONS: Record<FeatureIconName, ReactNode> = {
  parallel: (
    <>
      <path d="M4 3v10" />
      <path d="M8 3v10" />
      <path d="M12 3v10" />
    </>
  ),
  deterministic: (
    <>
      <path d="M5 7V5a3 3 0 0 1 6 0v2" />
      <path d="M4 7h8v6H4z" />
    </>
  ),
  cache: (
    <>
      <path d="M3 5h10" />
      <path d="M3 8h10" />
      <path d="M3 11h6" />
    </>
  ),
  preview: (
    <>
      <path d="M2 3.5h12v9H2z" />
      <path d="M2 6h12" />
    </>
  ),
  rollback: (
    <>
      <circle cx="8" cy="8" r="5.5" />
      <path d="M8 5v3l2 2" />
    </>
  ),
  analytics: (
    <>
      <path d="M3.5 13V9" />
      <path d="M8 13V5" />
      <path d="M12.5 13V7" />
    </>
  ),
};

function FeatureIcon({ name }: { name: FeatureIconName }) {
  return (
    <svg
      aria-hidden="true"
      viewBox="0 0 16 16"
      className="h-4 w-4"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      {ICONS[name]}
    </svg>
  );
}

const DEFAULT_FEATURES: GridFeature[] = [
  {
    icon: "parallel",
    title: "Parallel workers",
    description:
      "Every build fans out across isolated runners, so suites that took forty minutes finish in four.",
  },
  {
    icon: "deterministic",
    title: "Deterministic builds",
    description:
      "Locked toolchains and hermetic sandboxes mean the same commit always produces the same artifact.",
  },
  {
    icon: "cache",
    title: "Content-addressed cache",
    description:
      "Dependency layers are cached by hash, not by branch, so clean checkouts still build warm.",
  },
  {
    icon: "preview",
    title: "Preview environments",
    description:
      "Each pull request gets an ephemeral environment with seeded data, torn down automatically on merge.",
  },
  {
    icon: "rollback",
    title: "Instant rollback",
    description:
      "Every deploy is an immutable release; rolling back is a pointer change, not a rebuild.",
  },
  {
    icon: "analytics",
    title: "Build analytics",
    description:
      "Queue time, cache hit rate, and flaky-test frequency are tracked per pipeline, per team.",
  },
];

export function FeaturesSection({
  eyebrow = "Build platform",
  heading = "Everything a pipeline needs, nothing it doesn't.",
  lede = "Branch CI handles the path from commit to production: fast builds, honest caching, and releases you can undo in seconds.",
  features = DEFAULT_FEATURES,
  primaryAction = { label: "Start building", href: "#get-started" },
  secondaryAction = { label: "Read the docs", href: "#docs" },
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

        <ul className="mt-12 grid grid-cols-1 gap-x-8 gap-y-10 sm:grid-cols-2 lg:mt-16 lg:grid-cols-3">
          {features.map((feature) => (
            <li key={feature.title}>
              <div className="flex items-center gap-2 text-[var(--ds-color-muted-foreground)]">
                <FeatureIcon name={feature.icon} />
                <h3 className="text-base font-semibold leading-6 text-[var(--ds-color-foreground)]">
                  {feature.title}
                </h3>
              </div>
              <p className="mt-2 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
                {feature.description}
              </p>
            </li>
          ))}
        </ul>

        <div className="mt-12 flex flex-col gap-3 sm:flex-row lg:mt-16">
          <a href={primaryAction.href} className={PRIMARY_ACTION_CLASSES}>
            {primaryAction.label}
          </a>
          <a href={secondaryAction.href} className={SECONDARY_ACTION_CLASSES}>
            {secondaryAction.label}
          </a>
        </div>
      </div>
    </section>
  );
}
