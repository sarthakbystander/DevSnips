import { useId } from "react";

/**
 * DevSnips React CTA — Minimal direction (the reference composition).
 *
 * A restrained editorial call to action: a single left-aligned block —
 * eyebrow, heading, lede, two actions — separated from the canvas by
 * whitespace alone (§4.2). A hairline border-t rule beneath the actions
 * carries one quiet mono metadata row. No cards, no fills, no effects;
 * the hierarchy comes from type scale, weight, spacing, and one 1px
 * border (§7). Compact but premium: standard section rhythm (§8),
 * 56–68 character measure (§5.4), and at most two actions (§11.1).
 */

export interface CtaAction {
  label: string;
  href: string;
}

export interface CTASectionProps {
  eyebrow?: string;
  title?: string;
  description?: string;
  primaryAction?: CtaAction;
  secondaryAction?: CtaAction;
  footnote?: string;
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const PRIMARY_ACTION_CLASSES =
  "inline-flex h-11 items-center justify-center rounded-[var(--ds-radius-sm)] bg-[var(--ds-color-primary)] px-5 text-sm font-semibold leading-5 text-[var(--ds-color-primary-foreground)] transition-colors duration-150 ease-out hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)] motion-reduce:transition-none " +
  FOCUS_RING;

const SECONDARY_ACTION_CLASSES =
  "inline-flex h-11 items-center justify-center rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border-strong)] bg-[var(--ds-color-surface)] px-5 text-sm font-semibold leading-5 text-[var(--ds-color-foreground)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] motion-reduce:transition-none " +
  FOCUS_RING;

export function CTASection({
  eyebrow = "DevSnips",
  title = "Build something worth shipping.",
  description =
    "Production-ready interface building blocks for modern products — accessible, theme-aware, and responsive from mobile to wide desktop.",
  primaryAction = { label: "Explore components", href: "#components" },
  secondaryAction = { label: "Read the docs", href: "#docs" },
  footnote = "Free to evaluate · No credit card · MIT licensed",
}: CTASectionProps) {
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
            {title}
          </h2>
          <p className="mt-4 max-w-xl text-[clamp(1rem,0.95rem+0.25vw,1.125rem)] leading-[1.5] text-[var(--ds-color-muted-foreground)]">
            {description}
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
        </div>

        <div className="mt-12 flex flex-col gap-2 border-t border-[var(--ds-color-border-subtle)] pt-6 sm:flex-row sm:items-center sm:justify-between">
          <p className="font-[var(--ds-font-mono)] text-xs leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
            {footnote}
          </p>
          <p className="text-xs leading-[1.4] text-[var(--ds-color-muted-foreground)]">
            React + TypeScript · Tailwind tokens
          </p>
        </div>
      </div>
    </section>
  );
}