import { useId } from "react";

/**
 * DevSnips React Features — Editorial composition (Minimal direction).
 *
 * An asymmetric 4/8 split of 12 (§10.2): a quiet heading block on the left,
 * a numbered feature list on the right. The list is typography-driven —
 * mono index numbers, semibold titles, one-sentence descriptions, and 1px
 * hairline dividers doing all of the separation (§9). No cards, no icons,
 * no shadows. Columns stack below lg with the heading block first (§12.2).
 *
 * One accent: the single text link under the lede. Numbers use the mono
 * stack per §5.1 (metadata role), never color.
 */

export interface EditorialFeature {
  title: string;
  description: string;
}

export interface FeaturesSectionProps {
  eyebrow?: string;
  heading?: string;
  lede?: string;
  features?: EditorialFeature[];
  link?: { label: string; href: string };
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const LINK_CLASSES =
  "text-sm font-semibold leading-5 text-[var(--ds-color-link)] underline underline-offset-4 transition-colors duration-150 ease-out hover:text-[var(--ds-color-link-hover)] motion-reduce:transition-none " +
  FOCUS_RING;

const DEFAULT_FEATURES: EditorialFeature[] = [
  {
    title: "Double-entry by default",
    description:
      "Every transaction writes balanced entries across accounts, so books reconcile themselves instead of being reconciled later.",
  },
  {
    title: "Idempotent requests",
    description:
      "An idempotency key on every mutation makes retries safe — a flaky network can never charge a customer twice.",
  },
  {
    title: "Signed webhooks",
    description:
      "Balance changes, settlements, and reversals arrive as signed events your services can verify without a round trip.",
  },
  {
    title: "Append-only audit trail",
    description:
      "Corrections are new entries, never edits; the full history of every account is queryable back to day one.",
  },
];

export function FeaturesSection({
  eyebrow = "Financial infrastructure",
  heading = "A ledger your accountant would approve of.",
  lede = "Ledger is a financial data API that treats correctness as the feature: balanced writes, safe retries, and an audit trail you never have to reconstruct.",
  features = DEFAULT_FEATURES,
  link = { label: "Read the data model", href: "#data-model" },
}: FeaturesSectionProps) {
  const headingId = useId();
  return (
    <section
      aria-labelledby={headingId}
      className="bg-[var(--ds-color-background)] font-[var(--ds-font-sans)] text-[var(--ds-color-foreground)]"
    >
      <div className="mx-auto max-w-[1280px] px-4 py-[clamp(4rem,3rem+4vw,6rem)] sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 gap-12 lg:grid-cols-12 lg:gap-8">
          <div className="lg:col-span-4">
            <div className="max-w-md">
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
                <a href={link.href} className={LINK_CLASSES}>
                  {link.label}
                </a>
              </p>
            </div>
          </div>

          <ol className="border-t border-[var(--ds-color-border)] lg:col-span-8">
            {features.map((feature, index) => (
              <li
                key={feature.title}
                className="grid grid-cols-1 gap-2 border-b border-[var(--ds-color-border)] py-6 sm:grid-cols-[3rem_1fr] sm:gap-6 sm:py-8"
              >
                <span
                  aria-hidden="true"
                  className="font-[var(--ds-font-mono)] text-sm font-medium leading-6 text-[var(--ds-color-muted-foreground)]"
                >
                  {String(index + 1).padStart(2, "0")}
                </span>
                <div>
                  <h3 className="text-base font-semibold leading-6">
                    {feature.title}
                  </h3>
                  <p className="mt-2 max-w-xl text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
                    {feature.description}
                  </p>
                </div>
              </li>
            ))}
          </ol>
        </div>
      </div>
    </section>
  );
}
