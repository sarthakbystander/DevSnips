import { useId } from "react";

/**
 * DevSnips React Hero — Minimal direction.
 *
 * The reference direction for the Hero family: a simple top navigation row,
 * a centered headline block, and a quiet wordmark proof strip. Typography and
 * spacing carry the design — separation comes from whitespace and 1px
 * hairlines, never from cards or shadows.
 *
 * Composition (per React/Sections/DESIGN_TOKENS.md §11.1):
 *   <section aria-labelledby> → header (nav) → centered header block
 *     (eyebrow + h1 + lede + actions) → proof region (wordmark list)
 *
 * All four Hero directions share this props surface. Values below are the
 * authored defaults; every slot is overridable from the consuming page.
 */

export interface HeroAction {
  label: string;
  href: string;
}

export interface HeroSectionProps {
  eyebrow?: string;
  heading?: string;
  lede?: string;
  primaryAction?: HeroAction;
  secondaryAction?: HeroAction;
  proofLogos?: string[];
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const PRIMARY_ACTION_CLASSES =
  "inline-flex h-11 items-center justify-center rounded-[var(--ds-radius-sm)] bg-[var(--ds-color-primary)] px-5 text-sm font-semibold leading-5 text-[var(--ds-color-primary-foreground)] transition-colors duration-150 ease-out hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)] motion-reduce:transition-none " +
  FOCUS_RING;

const SECONDARY_ACTION_CLASSES =
  "inline-flex h-11 items-center justify-center rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border-strong)] bg-[var(--ds-color-surface)] px-5 text-sm font-semibold leading-5 text-[var(--ds-color-foreground)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] motion-reduce:transition-none " +
  FOCUS_RING;

const NAV_LINK_CLASSES =
  "text-sm font-medium leading-5 text-[var(--ds-color-muted-foreground)] transition-colors duration-150 ease-out hover:text-[var(--ds-color-foreground)] motion-reduce:transition-none " +
  FOCUS_RING;

const DEFAULT_PROOF_LOGOS = [
  "Northwind Labs",
  "Helio Systems",
  "Flatiron",
  "Sendero",
  "Vantage Works",
];

export function HeroSection({
  eyebrow = "React Sections",
  heading = "Ship polished product pages, one section at a time.",
  lede = "Production-ready React sections composed from semantic tokens — accessible, theme-aware, and responsive from mobile to wide desktop.",
  primaryAction = { label: "Browse sections", href: "#sections" },
  secondaryAction = { label: "Read the design tokens", href: "#design-tokens" },
  proofLogos = DEFAULT_PROOF_LOGOS,
}: HeroSectionProps) {
  const headingId = useId();
  return (
    <section
      aria-labelledby={headingId}
      className="bg-[var(--ds-color-background)] font-[var(--ds-font-sans)] text-[var(--ds-color-foreground)]"
    >
      <header className="border-b border-[var(--ds-color-border-subtle)]">
        <div className="mx-auto flex max-w-[1280px] items-center justify-between gap-4 px-4 py-4 sm:px-6 lg:px-8">
          <a
            href="#"
            aria-label="DevSnips home"
            className={
              "text-base font-semibold leading-6 text-[var(--ds-color-foreground)] " +
              FOCUS_RING
            }
          >
            DevSnips
          </a>
          <nav aria-label="Primary">
            <ul className="flex items-center gap-3 sm:gap-6">
              <li className="hidden sm:block">
                <a href="#components" className={NAV_LINK_CLASSES}>
                  Components
                </a>
              </li>
              <li className="hidden sm:block">
                <a href="#sections" className={NAV_LINK_CLASSES}>
                  Sections
                </a>
              </li>
              <li className="hidden sm:block">
                <a href="#design-tokens" className={NAV_LINK_CLASSES}>
                  Tokens
                </a>
              </li>
              <li>
                <a
                  href="#sections"
                  className={
                    "inline-flex h-9 items-center rounded-[var(--ds-radius-sm)] bg-[var(--ds-color-primary)] px-4 text-sm font-semibold leading-5 text-[var(--ds-color-primary-foreground)] transition-colors duration-150 ease-out hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)] motion-reduce:transition-none " +
                    FOCUS_RING
                  }
                >
                  Browse library
                </a>
              </li>
            </ul>
          </nav>
        </div>
      </header>

      <div className="mx-auto max-w-[1280px] px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-2xl py-[clamp(5rem,3.5rem+6vw,8rem)] text-center">
          <p className="text-xs font-semibold uppercase leading-[1.3] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
            {eyebrow}
          </p>
          <h1
            id={headingId}
            className="mt-3 text-[clamp(2.5rem,1.9rem+2.8vw,3.5rem)] font-semibold leading-[1.1] tracking-[-0.02em]"
          >
            {heading}
          </h1>
          <p className="mt-4 text-[clamp(1rem,0.95rem+0.25vw,1.125rem)] leading-[1.5] text-[var(--ds-color-muted-foreground)]">
            {lede}
          </p>
          <div className="mt-8 flex flex-col gap-3 sm:flex-row sm:justify-center">
            <a href={primaryAction.href} className={PRIMARY_ACTION_CLASSES}>
              {primaryAction.label}
            </a>
            <a href={secondaryAction.href} className={SECONDARY_ACTION_CLASSES}>
              {secondaryAction.label}
            </a>
          </div>
        </div>

        <div className="border-t border-[var(--ds-color-border-subtle)] py-[clamp(2.5rem,2rem+2vw,4rem)] text-center">
          <p className="text-xs font-[var(--ds-font-mono)] uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
            Trusted by product teams shipping with DevSnips
          </p>
          <ul className="mt-4 flex flex-wrap items-center justify-center gap-x-8 gap-y-2">
            {proofLogos.map((logo) => (
              <li
                key={logo}
                className="text-sm font-medium leading-5 text-[var(--ds-color-muted-foreground)]"
              >
                {logo}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  );
}
