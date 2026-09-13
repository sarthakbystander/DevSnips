import { useId } from "react";

/**
 * DevSnips React CTA — Neo-Brutalist direction.
 *
 * The expressive ceiling, kept disciplined (§4.5): an asymmetric 7/5
 * split with a hard-bordered headline block on the left and two stacked
 * flat-fill metric blocks on the right. Uniform 2px borders, hard offset
 * shadows (zero blur), square corners, bold typography, mono uppercase
 * metadata, one flat primary fill plus one supporting warning fill — within
 * the direction cap. Buttons press down by their shadow offset on :active
 * (≤100ms. Everything is intentionally rigid: aligned edges, full-width
 * rows, no floating chips.
 *
 * Collapse: 5/7-run side by side at lg, stacked below. The bottom action
 * bar spans the full container — two press-down buttons over a ruled mono
 * footnote row.

 * Fill budget: the warning metric block is the one supporting accent;
 * the primary CTA is the second filled element (primary tokens, AA in
 * both themes). Everything else is flat surface. The featured metric is
 * also named in words ("On track"), never carried by color alone.

 */

export interface CtaAction {
  label: string;
  href: string;
}

export interface BrutalistMetric {
  value: string;
  label: string;
  status: string;
}

export interface CTASectionProps {
  eyebrow?: string;
  title?: string;
  description?: string;
  primaryAction?: CtaAction;
  secondaryAction?: CtaAction;
  leftMetric?: BrutalistMetric;
  rightMetric?: BrutalistMetric;
  footnote?: string;
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const NB_BUTTON_BASE =
  "inline-flex h-11 items-center justify-center rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] px-5 text-sm font-semibold leading-5 shadow-[4px_4px_0_0_var(--ds-color-border-strong)] transition-[transform,box-shadow] duration-100 ease-out active:translate-x-[4px] active:translate-y-[4px] active:shadow-none motion-reduce:transition-none " +
  FOCUS_RING;

const PRIMARY_ACTION_CLASSES =
  NB_BUTTON_BASE +
  " bg-[var(--ds-color-primary)] text-[var(--ds-color-primary-foreground)]";

const QUIET_ACTION_CLASSES =
  NB_BUTTON_BASE +
  " bg-[var(--ds-color-surface)] text-[var(--ds-color-foreground)]";

const DEFAULT_LEFT_METRIC: BrutalistMetric = {
  value: "4.8M",
  label: "Previews served last month",
  status: "On track",
};

const DEFAULT_RIGHT_METRIC: BrutalistMetric = {
  value: "11m",
  label: "Median deploy wall time",
  status: "Green",
};

export function CTASection({
  eyebrow = "Vaporworks",
  title = "Deploy with hard edges and honest gates.",
  description =
    "Two buttons, one reviewed artifact, zero drift. Vaporworks makes promotion rules visible as checklists — the deploy pipeline as the source of truth.",
  primaryAction = { label: "Start shipping", href: "#start" },
  secondaryAction = { label: "Read the runbook", href: "#docs" },
  leftMetric = DEFAULT_LEFT_METRIC,
  rightMetric = DEFAULT_RIGHT_METRIC,
  footnote = "Free to evaluate · No credit card · Export anytime",
}: CTASectionProps) {
  const headingId = useId();
  return (
    <section
      aria-labelledby={headingId}
      className="bg-[var(--ds-color-background)] font-[var(--ds-font-sans)] text-[var(--ds-color-foreground)]"
    >
      <div className="mx-auto max-w-[1280px] px-4 py-[clamp(4rem,3rem+4vw,6rem)] sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-12 lg:items-start">
          <div className="lg:col-span-7">
            <p className="inline-block rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] bg-[var(--ds-color-surface)] px-3 py-1 font-[var(--ds-font-mono)] text-xs font-semibold uppercase leading-[1.3] tracking-[0.05em] shadow-[4px_4px_0_0_var(--ds-color-border-strong)]">
              {eyebrow}
            </p>
            <h2
              id={headingId}
              className="mt-6 max-w-2xl text-[clamp(1.875rem,1.65rem+1vw,2.25rem)] font-bold leading-[1.15] tracking-[-0.02em]"
            >
              {title}
            </h2>
            <p className="mt-4 max-w-xl text-[clamp(1rem,0.95rem+0.25vw,1.125rem)] leading-[1.5] text-[var(--ds-color-muted-foreground)]">
              {description}
            </p>
            <div className="mt-8 flex flex-col gap-4 sm:flex-row">
              <a href={primaryAction.href} className={PRIMARY_ACTION_CLASSES}>
                {primaryAction.label}
              </a>
              <a
                href={secondaryAction.href}
                className={QUIET_ACTION_CLASSES}
              >
                {secondaryAction.label}
              </a>
            </div>
          </div>

          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:col-span-5">
            <div className="rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] bg-[var(--ds-color-surface)] p-6 shadow-[4px_4px_0_0_var(--ds-color-border-strong)] sm:p-8">
              <p className="font-[var(--ds-font-mono)] text-xs font-semibold uppercase leading-[1.3] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
                {leftMetric.label}
              </p>
              <p className="mt-4 text-[clamp(1.75rem,1.5rem+1.2vw,2.25rem)] font-bold leading-[1.2] tracking-[-0.02em] tabular-nums">
                {leftMetric.value}
              </p>
              <p className="mt-2 text-sm font-semibold leading-5">
                {leftMetric.status}
              </p>
            </div>
            <div className="rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] bg-[var(--ds-color-warning)] p-6 shadow-[4px_4px_0_0_var(--ds-color-border-strong)] text-[var(--ds-color-warning-foreground)] sm:p-8">
              <p className="font-[var(--ds-font-mono)] text-xs font-semibold uppercase leading-[1.3] tracking-[0.05em]">
                {rightMetric.label}
              </p>
              <p className="mt-4 text-[clamp(1.75rem,1.5rem+1.2vw,2.25rem)] font-bold leading-[1.2] tracking-[-0.02em] tabular-nums">
                {rightMetric.value}
              </p>
              <p className="mt-2 text-sm font-semibold leading-5">
                {rightMetric.status}
              </p>
            </div>
          </div>
        </div>

        <div className="mt-12 border-t-2 border-[var(--ds-color-border-strong)] pt-8 lg:mt-16">
          <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
            <p className="font-[var(--ds-font-mono)] text-xs leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
              {footnote}
            </p>
            <p className="font-[var(--ds-font-mono)] text-xs uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
              Q3 · Gate 1 of 3
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}