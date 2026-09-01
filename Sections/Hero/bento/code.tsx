import { useId } from "react";

/**
 * DevSnips React Hero — Bento direction.
 *
 * A modular 12-column cell grid: one hero cell (span 7) carries the headline
 * block and the CTAs, a code cell (span 5) carries a real copy-paste snippet,
 * and three supporting cells (span 4 each) each hold exactly one idea. Cells
 * share one radius (radius-lg), one 1px border, and a uniform gap
 * (16px mobile / 24px desktop). Collapse: authored spans at lg, 2-col equal
 * at sm, 1-col below — per React/Sections/DESIGN_TOKENS.md §4.4 and §12.2.
 *
 * At most two cells may carry accent; here only the hero cell contains accent
 * (the primary CTA). Everything else is surfaces and hairlines.
 */

export interface HeroAction {
  label: string;
  href: string;
}

export interface HeroStat {
  value: string;
  label: string;
}

export interface HeroSectionProps {
  eyebrow?: string;
  heading?: string;
  lede?: string;
  primaryAction?: HeroAction;
  secondaryAction?: HeroAction;
  stats?: HeroStat[];
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const PRIMARY_ACTION_CLASSES =
  "inline-flex h-11 items-center justify-center rounded-[var(--ds-radius-sm)] bg-[var(--ds-color-primary)] px-5 text-sm font-semibold leading-5 text-[var(--ds-color-primary-foreground)] transition-colors duration-150 ease-out hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)] motion-reduce:transition-none " +
  FOCUS_RING;

const SECONDARY_ACTION_CLASSES =
  "inline-flex h-11 items-center justify-center rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border-strong)] bg-[var(--ds-color-surface)] px-5 text-sm font-semibold leading-5 text-[var(--ds-color-foreground)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] motion-reduce:transition-none " +
  FOCUS_RING;

// One radius language for every cell (§4.4) and a border-only hover lift.
const CELL_CLASSES =
  "rounded-[var(--ds-radius-lg)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-6 transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] motion-reduce:transition-none lg:p-8";

const DEFAULT_STATS: HeroStat[] = [
  { value: "663", label: "Production-ready snippets" },
];

function CheckIcon() {
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
      <path d="m3.5 8.5 2.5 2.5 6.5-6.5" />
    </svg>
  );
}

function CodeIcon() {
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
      <path d="M5.5 5 2 8l3.5 3M10.5 5 14 8l-3.5 3" />
    </svg>
  );
}

export function HeroSection({
  eyebrow = "React Sections",
  heading = "Assemble the page like a design system, not a mood board.",
  lede = "Every section ships as copy-paste React + TypeScript with Tailwind classes bound to the same semantic tokens — no visual negotiation between blocks.",
  primaryAction = { label: "Browse sections", href: "#sections" },
  secondaryAction = { label: "How tokens work", href: "#design-tokens" },
  stats = DEFAULT_STATS,
}: HeroSectionProps) {
  const headingId = useId();
  return (
    <section
      aria-labelledby={headingId}
      className="bg-[var(--ds-color-background)] font-[var(--ds-font-sans)] text-[var(--ds-color-foreground)]"
    >
      <div className="mx-auto max-w-[1280px] px-4 py-[clamp(5rem,3.5rem+6vw,8rem)] sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-12 lg:gap-6">
          <div className={CELL_CLASSES + " sm:col-span-2 lg:col-span-7"}>
            <p className="text-xs font-semibold uppercase leading-[1.3] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
              {eyebrow}
            </p>
            <h1
              id={headingId}
              className="mt-3 max-w-2xl text-[clamp(2.5rem,1.9rem+2.8vw,3.5rem)] font-semibold leading-[1.1] tracking-[-0.02em]"
            >
              {heading}
            </h1>
            <p className="mt-4 max-w-xl text-[clamp(1rem,0.95rem+0.25vw,1.125rem)] leading-[1.5] text-[var(--ds-color-muted-foreground)]">
              {lede}
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
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
            <p className="text-xs font-[var(--ds-font-mono)] uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
              Copy, paste, ship
            </p>
            <p className="mt-2 text-base leading-6 text-[var(--ds-color-foreground)]">
              One file per section. Nothing to install.
            </p>
            <pre className="mt-4 overflow-x-auto rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border-subtle)] bg-[var(--ds-color-surface-subtle)] p-4">
              <code className="text-sm leading-6 text-[var(--ds-color-foreground)]">
                {`import { HeroSection } from "./sections/Hero";

export function App() {
  return <HeroSection />;
}`}
              </code>
            </pre>
          </div>

          {stats.map((stat) => (
            <div key={stat.label} className={CELL_CLASSES + " lg:col-span-4"}>
              <p className="text-[clamp(1.75rem,1.5rem+1.2vw,2.25rem)] font-semibold leading-[1.2] tracking-[-0.02em] tabular-nums">
                {stat.value}
              </p>
              <p className="mt-2 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
                {stat.label}
              </p>
            </div>
          ))}

          <div className={CELL_CLASSES + " lg:col-span-4"}>
            <div className="flex items-center gap-2">
              <span className="text-[var(--ds-color-muted-foreground)]">
                <CodeIcon />
              </span>
              <p className="text-base font-semibold leading-6">Token-driven</p>
            </div>
            <p className="mt-2 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
              Light and dark themes flip without touching markup, because
              classes only ever reference semantic tokens.
            </p>
          </div>

          <div className={CELL_CLASSES + " lg:col-span-4"}>
            <div className="flex items-center gap-2">
              <span className="text-[var(--ds-color-muted-foreground)]">
                <CheckIcon />
              </span>
              <p className="text-base font-semibold leading-6">
                Accessible by default
              </p>
            </div>
            <p className="mt-2 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
              Semantic landmarks, real links, visible focus rings, and AA
              contrast are verified in QA — not aspirational.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
