import { useId } from "react";

/**
 * DevSnips React Features — Neo-Brutalist direction.
 *
 * The expressive ceiling, kept disciplined: four square feature blocks with
 * uniform 2px borders, hard 4px offset shadows (zero blur), and mono index
 * numbers. One cell is a flat accent fill; everything else is surface.
 * Eyebrow is a bordered chip, buttons press down by their shadow offset on
 * :active (≤100ms), and nothing rounds, glows, or gradients (§4.5).
 *
 * Collapse: 2 columns from sm up, 1 column below. Fill budget: one
 * warning-filled cell (a supporting fill that keeps AA contrast in both
 * themes) + the primary button. Every other block is flat surface.
 */

export interface BrutalistFeature {
  title: string;
  description: string;
  filled?: boolean;
}

export interface FeatureAction {
  label: string;
  href: string;
}

export interface FeaturesSectionProps {
  eyebrow?: string;
  heading?: string;
  lede?: string;
  features?: BrutalistFeature[];
  primaryAction?: FeatureAction;
  secondaryAction?: FeatureAction;
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const NB_ACTION_BASE =
  "inline-flex h-11 items-center justify-center rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] px-5 text-sm font-semibold leading-5 shadow-[4px_4px_0_0_var(--ds-color-border-strong)] transition-[transform,box-shadow] duration-100 ease-out active:translate-x-[4px] active:translate-y-[4px] active:shadow-none motion-reduce:transition-none " +
  FOCUS_RING;

const PRIMARY_ACTION_CLASSES =
  NB_ACTION_BASE +
  " bg-[var(--ds-color-primary)] text-[var(--ds-color-primary-foreground)]";

const SECONDARY_ACTION_CLASSES =
  NB_ACTION_BASE +
  " bg-[var(--ds-color-surface)] text-[var(--ds-color-foreground)]";

const DEFAULT_FEATURES: BrutalistFeature[] = [
  {
    title: "Zero configuration",
    description:
      "Point Turbosnap at any repository with a lockfile. It detects the toolchain, the test runner, and the deploy target — no YAML.",
    filled: true,
  },
  {
    title: "Remote execution",
    description:
      "Build steps run on warmed workers next to the cache, so a laptop fan never spins up for a monorepo build again.",
  },
  {
    title: "Flaky-test quarantine",
    description:
      "Tests that fail nondeterministically are detected statistically, quarantined, and reported — the suite stays green and honest.",
  },
  {
    title: "Build-time budgets",
    description:
      "Set a wall-clock budget per pipeline. When a change pushes past it, the build fails loudly with the diff that caused it.",
  },
];

export function FeaturesSection({
  eyebrow = "Build accelerator",
  heading = "Slow builds are a choice.",
  lede = "Turbosnap makes the fast path the default path: remote execution, an honest cache, and budgets that keep pipelines honest.",
  features = DEFAULT_FEATURES,
  primaryAction = { label: "Snap your builds", href: "#get-started" },
  secondaryAction = { label: "How it works", href: "#how-it-works" },
}: FeaturesSectionProps) {
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

        <ul className="mt-12 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:mt-16">
          {features.map((feature, index) => (
            <li
              key={feature.title}
              className={
                "rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] p-6 shadow-[4px_4px_0_0_var(--ds-color-border-strong)] sm:p-8 " +
                (feature.filled
                  ? "bg-[var(--ds-color-warning)] text-[var(--ds-color-warning-foreground)]"
                  : "bg-[var(--ds-color-surface)]")
              }
            >
              <p
                className={
                  "font-[var(--ds-font-mono)] text-xs font-semibold uppercase leading-[1.4] tracking-[0.05em] " +
                  (feature.filled
                    ? ""
                    : "text-[var(--ds-color-muted-foreground)]")
                }
              >
                {String(index + 1).padStart(2, "0")}
              </p>
              <h3 className="mt-3 text-xl font-bold leading-[1.25] tracking-[-0.01em]">
                {feature.title}
              </h3>
              <p className="mt-2 text-sm leading-5">
                {feature.description}
              </p>
            </li>
          ))}
        </ul>

        <div className="mt-12 flex flex-col gap-4 sm:flex-row lg:mt-16">
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
