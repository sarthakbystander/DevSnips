import { useId } from "react";

/**
 * DevSnips React Stats — Bento composition (Bento direction).
 *
 * Statistics as a modular 12-column cell grid (§4.4): one hero cell
 * (span 7) carrying the anchor metric, one highlight cell (span 5) whose
 * number is the family's single accent, and two supporting cells (span 6
 * each) below. Cells share one radius (radius-lg), one 1px border, a
 * uniform gap (16px mobile / 24px desktop), and a border-only hover lift.
 *
 * One idea per cell: number, label, one line of context. Intentionally
 * action-free — the cells are the content. Collapse (§12.2): large cells
 * span both columns at sm, everything stacks to one column below.
 */

export interface StatsCell {
  value: string;
  label: string;
  description: string;
}

export interface StatsSectionProps {
  eyebrow?: string;
  heading?: string;
  lede?: string;
  /** The anchor metric, rendered in the large hero cell. */
  hero?: StatsCell;
  /**
   * Remaining metrics. The first cell is the accent highlight (span 5);
   * the rest render as supporting cells (span 6 each).
   */
  cells?: StatsCell[];
}

const CELL_CLASSES =
  "rounded-[var(--ds-radius-lg)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-6 transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] motion-reduce:transition-none lg:p-8";

const DEFAULT_HERO: StatsCell = {
  value: "1.4M",
  label: "Previews rendered last month",
  description:
    "Every pull request gets a real URL with production-parity build output.",
};

const DEFAULT_CELLS: StatsCell[] = [
  {
    value: "99.99%",
    label: "Uptime, trailing 90 days",
    description: "Includes every customer-facing render endpoint.",
  },
  {
    value: "42ms",
    label: "p95 edge render time",
    description: "Request to first byte, measured across all 38 regions.",
  },
  {
    value: "618K",
    label: "Preview URLs shared per week",
    description: "Design, QA, and product review the same artifact.",
  },
];

export function StatsSection({
  eyebrow = "Shipyard by the numbers",
  heading = "The render numbers behind every preview URL.",
  lede = "Shipyard builds and serves a preview for every pull request. These operating numbers are what make that promise boring — which is the point.",
  hero = DEFAULT_HERO,
  cells = DEFAULT_CELLS,
}: StatsSectionProps) {
  const headingId = useId();
  const [highlight, ...supporting] = cells;
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
            <p className="text-[clamp(1.75rem,1.5rem+1.2vw,2.25rem)] font-semibold leading-[1.2] tracking-[-0.02em] tabular-nums">
              {hero.value}
            </p>
            <p className="mt-2 text-base font-semibold leading-6">
              {hero.label}
            </p>
            <p className="mt-1 max-w-md text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
              {hero.description}
            </p>
          </div>

          {highlight ? (
            <div className={CELL_CLASSES + " sm:col-span-2 lg:col-span-5"}>
              <p className="text-[clamp(1.75rem,1.5rem+1.2vw,2.25rem)] font-semibold leading-[1.2] tracking-[-0.02em] tabular-nums text-[var(--ds-color-accent)]">
                {highlight.value}
              </p>
              <p className="mt-2 text-sm font-semibold leading-5">
                {highlight.label}
              </p>
              <p className="mt-6 font-[var(--ds-font-mono)] text-xs uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
                {highlight.description}
              </p>
            </div>
          ) : null}

          {supporting.map((cell) => (
            <div key={cell.label} className={CELL_CLASSES + " lg:col-span-6"}>
              <p className="text-[clamp(1.75rem,1.5rem+1.2vw,2.25rem)] font-semibold leading-[1.2] tracking-[-0.02em] tabular-nums">
                {cell.value}
              </p>
              <p className="mt-2 text-sm font-semibold leading-5">
                {cell.label}
              </p>
              <p className="mt-1 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
                {cell.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
