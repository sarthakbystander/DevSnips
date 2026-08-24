import { useId } from "react";

/**
 * DevSnips React Pricing — Neo-Brutalist direction.
 *
 * The expressive ceiling, kept disciplined (§4.5): three square plan
 * blocks with uniform 2px borders, hard 4px offset shadows (zero blur),
 * mono uppercase labels, and press-down buttons that translate by their
 * shadow offset on :active (≤100ms). Nothing rounds, glows, or gradients.
 *
 * Fill budget: the featured plan carries the one flat accent fill
 * (warning tokens — AA in both themes) and the primary CTA is the second
 * filled element; every other block is flat surface. The featured state
 * is also named in words ("Most popular"), never carried by color alone.
 */

export interface PricingAction {
  label: string;
  href: string;
}

export interface BrutalistTier {
  name: string;
  price: string;
  period: string;
  features: string[];
  action: PricingAction;
  featured?: boolean;
}

export interface PricingSectionProps {
  eyebrow?: string;
  heading?: string;
  lede?: string;
  tiers?: BrutalistTier[];
  footnote?: string;
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const NB_BUTTON_BASE =
  "inline-flex h-11 w-full items-center justify-center rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] px-5 text-sm font-semibold leading-5 shadow-[4px_4px_0_0_var(--ds-color-border-strong)] transition-[transform,box-shadow] duration-100 ease-out active:translate-x-[4px] active:translate-y-[4px] active:shadow-none motion-reduce:transition-none " +
  FOCUS_RING;

const PRIMARY_ACTION_CLASSES =
  NB_BUTTON_BASE +
  " bg-[var(--ds-color-primary)] text-[var(--ds-color-primary-foreground)]";

const QUIET_ACTION_CLASSES =
  NB_BUTTON_BASE +
  " bg-[var(--ds-color-surface)] text-[var(--ds-color-foreground)]";

const DEFAULT_TIERS: BrutalistTier[] = [
  {
    name: "Hobby",
    price: "$0",
    period: "per month",
    features: [
      "1,000 components",
      "100 MB storage",
      "Public collections",
    ],
    action: { label: "Start free", href: "#signup" },
  },
  {
    name: "Pro",
    price: "$12",
    period: "per user / month",
    features: [
      "Unlimited components",
      "10 GB storage",
      "Private collections",
      "VS Code extension",
    ],
    action: { label: "Go Pro", href: "#trial" },
    featured: true,
  },
  {
    name: "Team",
    price: "$24",
    period: "per user / month",
    features: [
      "Everything in Pro",
      "Workspaces + approvals",
      "SSO / SAML",
    ],
    action: { label: "Talk to us", href: "#sales" },
  },
];

function CheckGlyph() {
  return (
    <svg
      aria-hidden="true"
      viewBox="0 0 16 16"
      className="mt-0.5 h-4 w-4 shrink-0"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="m3.5 8.5 2.5 2.5 6.5-6.5" />
    </svg>
  );
}

export function PricingSection({
  eyebrow = "Pricing",
  heading = "Pick a plan. Get back to work.",
  lede = "No calculator, no sales maze. Three flat plans with the limits printed on the front — upgrade when the numbers stop fitting.",
  tiers = DEFAULT_TIERS,
  footnote = "Prices in USD. Yearly billing takes two months off. Cancel whenever — exporting your work is always free.",
}: PricingSectionProps) {
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

        <ul className="mt-12 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:mt-16 lg:grid-cols-3">
          {tiers.map((tier) => (
            <li
              key={tier.name}
              className={
                "flex flex-col rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] p-6 shadow-[4px_4px_0_0_var(--ds-color-border-strong)] sm:p-8 " +
                (tier.featured
                  ? "bg-[var(--ds-color-warning)] text-[var(--ds-color-warning-foreground)]"
                  : "bg-[var(--ds-color-surface)]")
              }
            >
              <div className="flex items-center justify-between gap-4">
                <h3 className="font-[var(--ds-font-mono)] text-sm font-bold uppercase leading-[1.4] tracking-[0.05em]">
                  {tier.name}
                </h3>
                {tier.featured ? (
                  <p className="rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] bg-[var(--ds-color-surface)] px-2 py-0.5 font-[var(--ds-font-mono)] text-xs font-semibold uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-foreground)]">
                    Most popular
                  </p>
                ) : null}
              </div>
              <p className="mt-4 flex items-baseline gap-2">
                <span className="text-[clamp(1.75rem,1.5rem+1.2vw,2.25rem)] font-bold leading-[1.2] tracking-[-0.02em] tabular-nums">
                  {tier.price}
                </span>
                <span className="font-[var(--ds-font-mono)] text-xs font-medium uppercase leading-[1.4] tracking-[0.05em]">
                  {tier.period}
                </span>
              </p>
              <ul className="mt-6 space-y-3 border-t-2 border-[var(--ds-color-border-strong)] pt-6">
                {tier.features.map((feature) => (
                  <li key={feature} className="flex gap-2">
                    <CheckGlyph />
                    <span className="text-sm font-medium leading-5">
                      {feature}
                    </span>
                  </li>
                ))}
              </ul>
              <div className="mt-8 flex-1" aria-hidden="true" />
              <a
                href={tier.action.href}
                className={
                  tier.featured ? PRIMARY_ACTION_CLASSES : QUIET_ACTION_CLASSES
                }
              >
                {tier.action.label}
              </a>
            </li>
          ))}
        </ul>

        <p className="mt-8 font-[var(--ds-font-mono)] text-xs leading-[1.4] text-[var(--ds-color-muted-foreground)]">
          {footnote}
        </p>
      </div>
    </section>
  );
}
