import { useId } from "react";

/**
 * DevSnips React CTA — Bento composition (Bento direction).
 *
 * A genuine 12-column bento grid (§4.4): one large CTA headline cell
 * (span 7) carrying the lead, description, and both actions; one
 * product/stat cell (span 5) whose integration count is the family's single
 * accent; three single-idea supporting cells (span 4 each) beneath;
 * and a final full-width action strip (span 12) with a ruled footnote
 * rail. Cells share one radius (radius-lg), one 1px border, a uniform
 * gap (16px mobile / 24px desktop), and a border-strong hover lift —
 * no scale, no glow.
 *
 * The CTA reads as part of a product ecosystem rather than a centered
 * card: the action strip completes the grid instead of floating inside a
 * card. Collapse (§12.2): authored spans at lg, 2 equal columns at sm,
 * 1 below. One accent total — the stat number only; every CTA button
 * uses neutral primary tokens (§3.5).
 */

export interface CtaAction {
  label: string;
  href: string;
}

export interface IntegrationStat {
  value: string;
  label: string;
  context: string;
}

export interface BentoCell {
  title: string;
  description: string;
}

export interface CTASectionProps {
  eyebrow?: string;
  title?: string;
  description?: string;
  primaryAction?: CtaAction;
  secondaryAction?: CtaAction;
  highlight?: IntegrationStat;
  cells?: BentoCell[];
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

const CELL_CLASSES =
  "rounded-[var(--ds-radius-lg)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-6 transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] motion-reduce:transition-none lg:p-8";

const DEFAULT_HIGHLIGHT: IntegrationStat = {
  value: "38",
  label: "Maintained integrations",
  context: "CI, registry, alerting, and secret managers — each versioned and tested",
};

const DEFAULT_CELLS: BentoCell[] = [
  {
    title: "One reviewed artifact",
    description:
      "Promotion tracks hash-for-hash; what QA saw is what production runs.",
  },
  {
    title: "Environment parity",
    description:
      "Staging and prod consume the same tokens, hooks, and rollout gates.",
  },
  {
    title: "Instant rollback",
    description:
      "One command rewinds any environment to the last known-good revision.",
  },
];

export function CTASection({
  eyebrow = "Vaporworks",
  title = "Ship every environment from one reviewed artifact.",
  description =
    "Vaporworks routes the same build to staging, preview, and production with policy gates between. Your deploy pipeline becomes a checklist, not a novel.",
  primaryAction = { label: "Explore components", href: "#components" },
  secondaryAction = { label: "Read the docs", href: "#docs" },
  highlight = DEFAULT_HIGHLIGHT,
  cells = DEFAULT_CELLS,
  footnote = "Free to evaluate · No credit card · MIT licensed",
}: CTASectionProps) {
  const headingId = useId();
  return (
    <section
      aria-labelledby={headingId}
      className="bg-[var(--ds-color-background)] font-[var(--ds-font-sans)] text-[var(--ds-color-foreground)]"
    >
      <div className="mx-auto max-w-[1280px] px-4 py-[clamp(4rem,3rem+4vw,6rem)] sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-12 lg:gap-6">
          <div className={CELL_CLASSES + " sm:col-span-2 lg:col-span-7"}>
            <p className="text-xs font-semibold uppercase leading-[1.3] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
              {eyebrow}
            </p>
            <h2
              id={headingId}
              className="mt-3 max-w-2xl text-[clamp(1.875rem,1.65rem+1vw,2.25rem)] font-semibold leading-[1.15] tracking-[-0.02em]"
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

          <div className={CELL_CLASSES + " sm:col-span-2 lg:col-span-5"}>
            <p className="text-[clamp(1.75rem,1.5rem+1.2vw,2.25rem)] font-semibold leading-[1.2] tracking-[-0.02em] tabular-nums text-[var(--ds-color-accent)]">
              {highlight.value}
            </p>
            <p className="mt-2 text-base font-semibold leading-6">
              {highlight.label}
            </p>
            <p className="mt-1 max-w-md text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
              {highlight.context}
            </p>
          </div>

          {cells.map((cell) => (
            <div key={cell.title} className={CELL_CLASSES + " lg:col-span-4"}>
              <p className="text-base font-semibold leading-6">{cell.title}</p>
              <p className="mt-2 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
                {cell.description}
              </p>
            </div>
          ))}

          <div className="flex flex-col gap-3 rounded-[var(--ds-radius-lg)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-6 transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] motion-reduce:transition-none lg:col-span-12 lg:flex-row lg:items-center lg:justify-between lg:gap-6">
            <p className="max-w-2xl text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
              {footnote}
            </p>
            <p className="shrink-0 font-[var(--ds-font-mono)] text-xs uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
              React + TypeScript · Tailwind tokens
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}