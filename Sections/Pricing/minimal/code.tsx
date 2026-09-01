import { useId } from "react";

/**
 * DevSnips React Pricing — Minimal direction (the reference composition).
 *
 * A left-aligned header block above an even three-tier card grid
 * (3 columns at lg, 1 below — §12.2). The design is the spacing: flat
 * bordered cards, generous rhythm, hierarchy from type and border weight
 * alone (§4.2). Per §11.3: 2–4 tiers, at most one highlighted tier via
 * border-strong, feature lists are real <ul>.
 *
 * Each tier is a flat bordered card: name + audience, price block
 * (tabular-nums), hairline, feature list, CTA. The featured tier is marked
 * by a stronger border plus a "Most popular" pill — weight and border, not
 * color alone (§13). The included-feature check glyphs are decorative; the
 * text carries the meaning.
 */

export interface PricingAction {
  label: string;
  href: string;
}

export interface PricingTier {
  name: string;
  audience: string;
  price: string;
  period: string;
  priceNote?: string;
  features: string[];
  action: PricingAction;
  featured?: boolean;
}

export interface PricingSectionProps {
  eyebrow?: string;
  heading?: string;
  lede?: string;
  tiers?: PricingTier[];
  footnote?: string;
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const ACTION_BASE =
  "inline-flex h-11 w-full items-center justify-center rounded-[var(--ds-radius-sm)] px-5 text-sm font-semibold leading-5 transition-colors duration-150 ease-out motion-reduce:transition-none " +
  FOCUS_RING;

const FEATURED_ACTION_CLASSES =
  ACTION_BASE +
  " bg-[var(--ds-color-primary)] text-[var(--ds-color-primary-foreground)] hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)]";

const DEFAULT_ACTION_CLASSES =
  ACTION_BASE +
  " border border-[var(--ds-color-border-strong)] bg-[var(--ds-color-surface)] text-[var(--ds-color-foreground)] hover:bg-[var(--ds-color-surface-hover)]";

const DEFAULT_TIERS: PricingTier[] = [
  {
    name: "Hobby",
    audience: "Side projects and experiments",
    price: "$0",
    period: "per month",
    priceNote: "Free forever, no card required",
    features: [
      "1,000 components",
      "100 MB artifact storage",
      "Community snippets",
      "Public collections",
    ],
    action: { label: "Start for free", href: "#signup" },
  },
  {
    name: "Pro",
    audience: "Working developers and freelancers",
    price: "$12",
    period: "per user / month",
    priceNote: "Billed monthly, cancel anytime",
    features: [
      "Unlimited components",
      "10 GB artifact storage",
      "Private collections",
      "VS Code extension",
      "Priority support",
    ],
    action: { label: "Start 14-day trial", href: "#trial" },
    featured: true,
  },
  {
    name: "Team",
    audience: "Teams sharing a design system",
    price: "$24",
    period: "per user / month",
    priceNote: "Billed monthly, cancel anytime",
    features: [
      "Everything in Pro",
      "Shared team workspaces",
      "Review and approval flows",
      "Usage analytics",
      "SSO / SAML",
    ],
    action: { label: "Contact sales", href: "#sales" },
  },
];

function CheckGlyph() {
  return (
    <svg
      aria-hidden="true"
      viewBox="0 0 16 16"
      className="mt-0.5 h-4 w-4 shrink-0 text-[var(--ds-color-muted-foreground)]"
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

export function PricingSection({
  eyebrow = "Pricing",
  heading = "Pay for the library you actually use.",
  lede = "Every plan includes the full component library and unlimited previews. Upgrade when you need private collections, storage, or team controls.",
  tiers = DEFAULT_TIERS,
  footnote = "Prices in USD. Taxes may apply. Downgrade or cancel at any time — your work stays exportable.",
}: PricingSectionProps) {
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

        <ul className="mt-12 grid grid-cols-1 gap-6 lg:mt-16 lg:grid-cols-3">
          {tiers.map((tier) => (
            <li
              key={tier.name}
              className={
                "flex flex-col rounded-[var(--ds-radius-md)] border bg-[var(--ds-color-surface)] p-6 lg:p-8 " +
                (tier.featured
                  ? "border-[var(--ds-color-border-strong)]"
                  : "border-[var(--ds-color-border)]")
              }
            >
              <div className="flex items-center justify-between gap-4">
                <h3 className="text-base font-semibold leading-6">
                  {tier.name}
                </h3>
                {tier.featured ? (
                  <p className="rounded-[var(--ds-radius-full)] border border-[var(--ds-color-border-strong)] px-3 py-1 text-xs font-semibold leading-[1.4]">
                    Most popular
                  </p>
                ) : null}
              </div>
              <p className="mt-1 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
                {tier.audience}
              </p>
              <p className="mt-6 flex items-baseline gap-2">
                <span className="text-[clamp(1.75rem,1.5rem+1.2vw,2.25rem)] font-semibold leading-[1.2] tracking-[-0.02em] tabular-nums">
                  {tier.price}
                </span>
                <span className="text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
                  {tier.period}
                </span>
              </p>
              {tier.priceNote ? (
                <p className="mt-1 text-xs leading-[1.4] text-[var(--ds-color-muted-foreground)]">
                  {tier.priceNote}
                </p>
              ) : null}
              <ul className="mt-6 space-y-3 border-t border-[var(--ds-color-border)] pt-6">
                {tier.features.map((feature) => (
                  <li key={feature} className="flex gap-2">
                    <CheckGlyph />
                    <span className="text-sm leading-5">{feature}</span>
                  </li>
                ))}
              </ul>
              <div className="mt-8 flex-1" aria-hidden="true" />
              <a
                href={tier.action.href}
                className={
                  tier.featured
                    ? FEATURED_ACTION_CLASSES
                    : DEFAULT_ACTION_CLASSES
                }
              >
                {tier.action.label}
              </a>
            </li>
          ))}
        </ul>

        <p className="mt-8 text-xs leading-[1.4] text-[var(--ds-color-muted-foreground)]">
          {footnote}
        </p>
      </div>
    </section>
  );
}
