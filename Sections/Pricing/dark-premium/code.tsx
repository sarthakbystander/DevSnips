import { useId } from "react";

/**
 * DevSnips React Pricing — Dark Premium direction.
 *
 * Two plans on a dark canvas (§4.3): a free Community tier and a Pro tier
 * with a metered platform-usage rate card beside it. The section pins the
 * dark theme mapping with `data-theme="dark"` on its own root, so it
 * consumes the same semantic tokens in both page themes — a theme mapping,
 * not a hard-coded dark page.
 *
 * Surfaces lift exactly one step above the canvas via a 1px border; no
 * shadows, no glow, no mesh. One accent: the Pro CTA. The rate card is a
 * real data panel (dl of unit prices), not decoration — it explains what
 * the paid plan actually meters.
 */

export interface PricingAction {
  label: string;
  href: string;
}

export interface DarkPlan {
  name: string;
  audience: string;
  price: string;
  period: string;
  priceNote: string;
  features: string[];
  action: PricingAction;
  featured?: boolean;
}

export interface UsageRate {
  label: string;
  price: string;
  unit: string;
}

export interface PricingSectionProps {
  eyebrow?: string;
  heading?: string;
  lede?: string;
  plans?: DarkPlan[];
  rates?: UsageRate[];
  ratesCaption?: string;
  footnote?: string;
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const PRIMARY_ACTION_CLASSES =
  "inline-flex h-11 w-full items-center justify-center rounded-[var(--ds-radius-sm)] bg-[var(--ds-color-primary)] px-5 text-sm font-semibold leading-5 text-[var(--ds-color-primary-foreground)] transition-colors duration-150 ease-out hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)] motion-reduce:transition-none " +
  FOCUS_RING;

const QUIET_ACTION_CLASSES =
  "inline-flex h-11 w-full items-center justify-center rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border-strong)] px-5 text-sm font-semibold leading-5 text-[var(--ds-color-foreground)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] motion-reduce:transition-none " +
  FOCUS_RING;

const DEFAULT_PLANS: DarkPlan[] = [
  {
    name: "Community",
    audience: "Open source and learning",
    price: "$0",
    period: "per month",
    priceNote: "Free forever, no card required",
    features: [
      "1,000 components",
      "100 MB artifact storage",
      "Public collections",
      "Community support",
    ],
    action: { label: "Start for free", href: "#signup" },
  },
  {
    name: "Pro",
    audience: "Professional work, metered fairly",
    price: "$12",
    period: "per user / month",
    priceNote: "Plus platform usage, metered per second",
    features: [
      "Unlimited components",
      "10 GB artifact storage included",
      "Private collections",
      "VS Code extension",
      "Priority support",
    ],
    action: { label: "Start 14-day trial", href: "#trial" },
    featured: true,
  },
];

const DEFAULT_RATES: UsageRate[] = [
  { label: "Extra storage", price: "$0.15", unit: "per GB / month" },
  { label: "Bandwidth", price: "$0.09", unit: "per GB" },
  { label: "Build minutes", price: "$0.004", unit: "per minute" },
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
  heading = "A free tier that stays free, a paid tier that meters honestly.",
  lede = "Community covers learning and open source. Pro adds the professional surface — and anything you consume beyond the plan is priced per unit, in the open.",
  plans = DEFAULT_PLANS,
  rates = DEFAULT_RATES,
  ratesCaption = "Platform usage beyond the Pro allowance",
  footnote = "Prices in USD. Usage is calculated per second and capped with spend limits you set yourself.",
}: PricingSectionProps) {
  const headingId = useId();
  return (
    <section
      data-theme="dark"
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

        <div className="mt-12 grid grid-cols-1 gap-6 lg:mt-16 lg:grid-cols-12">
          <ul className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:col-span-8">
            {plans.map((plan) => (
              <li
                key={plan.name}
                className={
                  "flex flex-col rounded-[var(--ds-radius-md)] border bg-[var(--ds-color-surface)] p-6 lg:p-8 " +
                  (plan.featured
                    ? "border-[var(--ds-color-border-strong)]"
                    : "border-[var(--ds-color-border)]")
                }
              >
                <div className="flex items-center justify-between gap-4">
                  <h3 className="text-base font-semibold leading-6">
                    {plan.name}
                  </h3>
                  {plan.featured ? (
                    <p className="rounded-[var(--ds-radius-full)] border border-[var(--ds-color-border-strong)] px-3 py-1 text-xs font-semibold leading-[1.4]">
                      Most popular
                    </p>
                  ) : null}
                </div>
                <p className="mt-1 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
                  {plan.audience}
                </p>
                <p className="mt-6 flex items-baseline gap-2">
                  <span className="text-[clamp(1.75rem,1.5rem+1.2vw,2.25rem)] font-semibold leading-[1.2] tracking-[-0.02em] tabular-nums">
                    {plan.price}
                  </span>
                  <span className="text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
                    {plan.period}
                  </span>
                </p>
                <p className="mt-1 text-xs leading-[1.4] text-[var(--ds-color-muted-foreground)]">
                  {plan.priceNote}
                </p>
                <ul className="mt-6 space-y-3 border-t border-[var(--ds-color-border)] pt-6">
                  {plan.features.map((feature) => (
                    <li key={feature} className="flex gap-2">
                      <CheckGlyph />
                      <span className="text-sm leading-5">{feature}</span>
                    </li>
                  ))}
                </ul>
                <div className="mt-8 flex-1" aria-hidden="true" />
                <a
                  href={plan.action.href}
                  className={
                    plan.featured
                      ? PRIMARY_ACTION_CLASSES
                      : QUIET_ACTION_CLASSES
                  }
                >
                  {plan.action.label}
                </a>
              </li>
            ))}
          </ul>

          <div className="rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-6 lg:col-span-4 lg:p-8">
            <p className="font-[var(--ds-font-mono)] text-xs font-medium uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
              {ratesCaption}
            </p>
            <dl className="mt-6 divide-y divide-[var(--ds-color-border-subtle)] border-t border-[var(--ds-color-border-subtle)]">
              {rates.map((rate) => (
                <div
                  key={rate.label}
                  className="flex items-baseline justify-between gap-4 py-4"
                >
                  <dt className="text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
                    {rate.label}
                  </dt>
                  <dd className="text-right">
                    <span className="font-[var(--ds-font-mono)] text-sm font-medium leading-5 tabular-nums">
                      {rate.price}
                    </span>
                    <span className="block text-xs leading-[1.4] text-[var(--ds-color-muted-foreground)]">
                      {rate.unit}
                    </span>
                  </dd>
                </div>
              ))}
            </dl>
            <p className="mt-6 text-xs leading-[1.4] text-[var(--ds-color-muted-foreground)]">
              Set a monthly spend cap per workspace. The meter stops at the
              cap — never a surprise invoice.
            </p>
          </div>
        </div>

        <p className="mt-8 text-xs leading-[1.4] text-[var(--ds-color-muted-foreground)]">
          {footnote}
        </p>
      </div>
    </section>
  );
}
