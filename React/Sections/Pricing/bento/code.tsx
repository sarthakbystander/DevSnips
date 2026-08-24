import { useId } from "react";

/**
 * DevSnips React Pricing — Bento composition (Bento direction).
 *
 * Pricing as a modular 12-column cell grid (§4.4): one hero cell (span 7)
 * carrying the recommended plan with its included list, two compact plan
 * cells stacked beside it (span 5), and a full-width guarantee strip
 * below. Cells share one radius (radius-lg), one 1px border, one uniform
 * gap, and a border-only hover lift. One idea per cell; the only accent
 * is the hero cell's primary CTA.
 *
 * Collapse (§12.2): 2 equal columns at sm (hero spans both), 1 column
 * below — no per-cell breakpoint choreography.
 */

export interface PricingAction {
  label: string;
  href: string;
}

export interface BentoHeroPlan {
  name: string;
  badge: string;
  audience: string;
  price: string;
  period: string;
  priceNote: string;
  features: string[];
  action: PricingAction;
}

export interface BentoPlan {
  name: string;
  price: string;
  period: string;
  summary: string;
  action: PricingAction;
}

export interface PricingSectionProps {
  eyebrow?: string;
  heading?: string;
  lede?: string;
  hero?: BentoHeroPlan;
  plans?: BentoPlan[];
  guarantees?: string[];
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const CELL_CLASSES =
  "rounded-[var(--ds-radius-lg)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-6 transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] motion-reduce:transition-none lg:p-8";

const PRIMARY_ACTION_CLASSES =
  "inline-flex h-11 w-full items-center justify-center rounded-[var(--ds-radius-sm)] bg-[var(--ds-color-primary)] px-5 text-sm font-semibold leading-5 text-[var(--ds-color-primary-foreground)] transition-colors duration-150 ease-out hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)] motion-reduce:transition-none sm:w-auto " +
  FOCUS_RING;

const QUIET_ACTION_CLASSES =
  "inline-flex h-9 shrink-0 items-center justify-center rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border-strong)] bg-[var(--ds-color-surface)] px-4 text-sm font-semibold leading-5 text-[var(--ds-color-foreground)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] motion-reduce:transition-none " +
  FOCUS_RING;

const DEFAULT_HERO: BentoHeroPlan = {
  name: "Pro",
  badge: "Recommended",
  audience: "For working developers and freelancers",
  price: "$12",
  period: "per user / month",
  priceNote: "Billed monthly. 14-day free trial, no card required.",
  features: [
    "Unlimited components and collections",
    "10 GB artifact storage",
    "Private, invite-only collections",
    "VS Code extension with inline insert",
    "Priority support (median response 4h)",
  ],
  action: { label: "Start 14-day trial", href: "#trial" },
};

const DEFAULT_PLANS: BentoPlan[] = [
  {
    name: "Hobby",
    price: "$0",
    period: "per month",
    summary: "1,000 components, 100 MB storage, public collections.",
    action: { label: "Start free", href: "#signup" },
  },
  {
    name: "Team",
    price: "$24",
    period: "per user / month",
    summary: "Everything in Pro, plus workspaces, approvals, and SSO.",
    action: { label: "Contact sales", href: "#sales" },
  },
];

const DEFAULT_GUARANTEES: string[] = [
  "30-day refund on every paid plan",
  "Your components stay exportable, always",
  "Downgrade at any time — prorated to the day",
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
  heading = "The plan grid, reorganized around the one you'll pick.",
  lede = "Pro gets the big cell because it earns it. Hobby and Team sit beside it at the same width, and the guarantees apply to every plan equally.",
  hero = DEFAULT_HERO,
  plans = DEFAULT_PLANS,
  guarantees = DEFAULT_GUARANTEES,
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

        <div className="mt-12 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:mt-16 lg:grid-cols-12 lg:gap-6">
          <div className={CELL_CLASSES + " sm:col-span-2 lg:col-span-7"}>
            <div className="flex flex-wrap items-center justify-between gap-3">
              <h3 className="text-xl font-semibold leading-[1.25] tracking-[-0.01em]">
                {hero.name}
              </h3>
              <p className="rounded-[var(--ds-radius-full)] border border-[var(--ds-color-border-strong)] px-3 py-1 text-xs font-semibold leading-[1.4]">
                {hero.badge}
              </p>
            </div>
            <p className="mt-1 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
              {hero.audience}
            </p>
            <p className="mt-6 flex items-baseline gap-2">
              <span className="text-[clamp(1.75rem,1.5rem+1.2vw,2.25rem)] font-semibold leading-[1.2] tracking-[-0.02em] tabular-nums">
                {hero.price}
              </span>
              <span className="text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
                {hero.period}
              </span>
            </p>
            <p className="mt-1 text-xs leading-[1.4] text-[var(--ds-color-muted-foreground)]">
              {hero.priceNote}
            </p>
            <ul className="mt-6 space-y-3 border-t border-[var(--ds-color-border)] pt-6">
              {hero.features.map((feature) => (
                <li key={feature} className="flex gap-2">
                  <CheckGlyph />
                  <span className="text-sm leading-5">{feature}</span>
                </li>
              ))}
            </ul>
            <a href={hero.action.href} className={PRIMARY_ACTION_CLASSES + " mt-8"}>
              {hero.action.label}
            </a>
          </div>

          <div className="grid grid-cols-1 gap-4 sm:col-span-2 lg:col-span-5 lg:gap-6">
            {plans.map((plan) => (
              <div key={plan.name} className={CELL_CLASSES}>
                <div className="flex items-baseline justify-between gap-4">
                  <h3 className="text-base font-semibold leading-6">
                    {plan.name}
                  </h3>
                  <p className="text-sm font-medium leading-5 tabular-nums">
                    {plan.price}
                    <span className="font-normal text-[var(--ds-color-muted-foreground)]">
                      {" "}
                      {plan.period}
                    </span>
                  </p>
                </div>
                <p className="mt-2 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
                  {plan.summary}
                </p>
                <a href={plan.action.href} className={QUIET_ACTION_CLASSES + " mt-4"}>
                  {plan.action.label}
                </a>
              </div>
            ))}
          </div>

          <div className={CELL_CLASSES + " sm:col-span-2 lg:col-span-12"}>
            <ul className="flex flex-col gap-3 sm:flex-row sm:flex-wrap sm:gap-x-8">
              {guarantees.map((guarantee) => (
                <li key={guarantee} className="flex gap-2">
                  <CheckGlyph />
                  <span className="text-sm leading-5">{guarantee}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </section>
  );
}
