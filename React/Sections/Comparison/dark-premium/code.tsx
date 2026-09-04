import { useId } from "react";

export type ComparisonValue = boolean | string;
export interface ComparisonOption { id: string; name: string; description?: string; featured?: boolean; }
export interface ComparisonFeature { label: string; description?: string; values: Record<string, ComparisonValue>; }
export interface ComparisonSectionProps { eyebrow?: string; title?: string; description?: string; options?: ComparisonOption[]; features?: ComparisonFeature[]; }

const DEFAULT_OPTIONS: ComparisonOption[] = [
  { id: "devsnips", name: "DevSnips", description: "A maintained path from idea to interface", featured: true },
  { id: "starter", name: "Starter kit", description: "Useful primitives, fewer decisions" },
  { id: "custom", name: "Build in-house", description: "Maximum ownership, maximum surface area" },
];
const DEFAULT_FEATURES: ComparisonFeature[] = [
  { label: "Sections", values: { devsnips: "Curated library", starter: "Small set", custom: "Build as needed" } },
  { label: "Semantic tokens", description: "Theme-ready visual decisions", values: { devsnips: true, starter: "Basic", custom: "Team-defined" } },
  { label: "Responsive behavior", values: { devsnips: "Designed in", starter: "Varies", custom: "Team-owned" } },
  { label: "Accessibility", values: { devsnips: "Built into patterns", starter: "Review needed", custom: "Team-owned" } },
  { label: "Source control", values: { devsnips: "Exportable", starter: "Exportable", custom: true } },
];
const FOCUS = "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

function Value({ value }: { value: ComparisonValue }) {
  if (value === true) return <span className="font-medium">Included<span className="sr-only"> in this option</span></span>;
  if (value === false) return <span className="text-[var(--ds-color-muted-foreground)]">Not included</span>;
  return <span>{value}</span>;
}

export function ComparisonSection({
  eyebrow = "Make the trade-off explicit",
  title = "The right comparison is about ownership, not feature count.",
  description = "See how a maintained section library changes the amount of interface work your team needs to carry.",
  options = DEFAULT_OPTIONS,
  features = DEFAULT_FEATURES,
}: ComparisonSectionProps) {
  const headingId = useId();
  return (
    <section aria-labelledby={headingId} className="bg-[var(--ds-color-background)] font-[var(--ds-font-sans)] text-[var(--ds-color-foreground)]">
      <div className="mx-auto grid max-w-[1280px] gap-12 px-4 py-[clamp(4rem,3rem+4vw,6rem)] lg:grid-cols-[minmax(280px,0.75fr)_minmax(0,1.6fr)] lg:items-start lg:gap-20 sm:px-6 lg:px-8">
        <div className="lg:sticky lg:top-20">
          <p className="font-[var(--ds-font-mono)] text-xs font-medium uppercase tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">{eyebrow}</p>
          <h2 id={headingId} className="mt-4 max-w-xl text-[clamp(2rem,1.6rem+1.5vw,3rem)] font-semibold leading-[1.08] tracking-[-0.03em]">{title}</h2>
          <p className="mt-5 max-w-md text-base leading-7 text-[var(--ds-color-muted-foreground)]">{description}</p>
          <div className="mt-8 border-l border-[var(--ds-color-border-strong)] pl-4 text-sm leading-6 text-[var(--ds-color-muted-foreground)]">Recommended options balance ready-made capability with exportable ownership. No lock-in is implied by this sample.</div>
        </div>

        <div className="space-y-8">
          {options.map((option) => (
            <article key={option.id} className={"rounded-[var(--ds-radius-md)] border bg-[var(--ds-color-surface)] p-6 sm:p-7 " + (option.featured ? "border-[var(--ds-color-primary)]" : "border-[var(--ds-color-border)]")}>
              <div className="flex flex-wrap items-start justify-between gap-4">
                <div>
                  <p className="font-[var(--ds-font-mono)] text-[10px] uppercase tracking-[0.06em] text-[var(--ds-color-muted-foreground)]">Option</p>
                  <h3 className="mt-2 text-lg font-semibold">{option.name}</h3>
                  {option.description ? <p className="mt-1 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">{option.description}</p> : null}
                </div>
                {option.featured ? <span className="rounded-[var(--ds-radius-full)] bg-[var(--ds-color-primary)] px-3 py-1 text-xs font-semibold text-[var(--ds-color-primary-foreground)]">Recommended</span> : null}
              </div>
              <dl className="mt-6 divide-y divide-[var(--ds-color-border-subtle)] border-y border-[var(--ds-color-border-subtle)]">
                {features.map((feature) => (
                  <div key={feature.label} className="grid grid-cols-[minmax(0,1fr)_minmax(130px,0.7fr)] gap-5 py-4">
                    <dt className="text-sm font-medium">{feature.label}{feature.description ? <span className="mt-1 block text-xs font-normal leading-5 text-[var(--ds-color-muted-foreground)]">{feature.description}</span> : null}</dt>
                    <dd className="text-right text-sm leading-5"><Value value={feature.values[option.id] ?? "Not specified"} /></dd>
                  </div>
                ))}
              </dl>
            </article>
          ))}
          <a href="#decision" className={"inline-flex h-11 items-center justify-center rounded-[var(--ds-radius-sm)] bg-[var(--ds-color-primary)] px-5 text-sm font-semibold text-[var(--ds-color-primary-foreground)] transition-colors duration-150 hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)] motion-reduce:transition-none " + FOCUS}>Review the decision</a>
        </div>
      </div>
    </section>
  );
}
