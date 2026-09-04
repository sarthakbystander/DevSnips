import { useId } from "react";

export type ComparisonValue = boolean | string;
export interface ComparisonOption { id: string; name: string; description?: string; featured?: boolean; }
export interface ComparisonFeature { label: string; description?: string; values: Record<string, ComparisonValue>; }
export interface ComparisonSectionProps { eyebrow?: string; title?: string; description?: string; options?: ComparisonOption[]; features?: ComparisonFeature[]; }

const DEFAULT_OPTIONS: ComparisonOption[] = [
  { id: "devsnips", name: "DevSnips", description: "Sections, components, and patterns", featured: true },
  { id: "starter", name: "Starter kit", description: "A focused baseline" },
  { id: "custom", name: "In-house", description: "Built and maintained by your team" },
];
const DEFAULT_FEATURES: ComparisonFeature[] = [
  { label: "Responsive", values: { devsnips: true, starter: "Core layouts", custom: "Team-defined" } },
  { label: "Accessible states", values: { devsnips: true, starter: "Review needed", custom: "Team-owned" } },
  { label: "Token architecture", values: { devsnips: "Semantic", starter: "Lightweight", custom: "Custom" } },
  { label: "Exportable source", values: { devsnips: true, starter: true, custom: true } },
  { label: "Maintenance model", values: { devsnips: "Library updates", starter: "Self-managed", custom: "Team-owned" } },
];

const FOCUS = "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";
function Mark({ value }: { value: ComparisonValue }) {
  if (value === true) return <span className="font-medium">Included<span className="sr-only"> in this comparison</span></span>;
  if (value === false) return <span className="text-[var(--ds-color-muted-foreground)]">Not included</span>;
  return <span>{value}</span>;
}

export function ComparisonSection({
  eyebrow = "Compare by what matters",
  title = "A decision map, not another giant table.",
  description = "Each cell isolates one part of the trade-off so teams can scan capability, ownership, and fit without losing the bigger picture.",
  options = DEFAULT_OPTIONS,
  features = DEFAULT_FEATURES,
}: ComparisonSectionProps) {
  const headingId = useId();
  const recommended = options.find((option) => option.featured) ?? options[0];
  const primaryFeatures = features.slice(0, Math.min(3, features.length));
  const remainingFeatures = features.slice(primaryFeatures.length);
  return (
    <section aria-labelledby={headingId} className="bg-[var(--ds-color-background)] font-[var(--ds-font-sans)] text-[var(--ds-color-foreground)]">
      <div className="mx-auto max-w-[1280px] px-4 py-[clamp(4rem,3rem+4vw,6rem)] sm:px-6 lg:px-8">
        <header className="max-w-3xl">
          <p className="text-xs font-semibold uppercase tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">{eyebrow}</p>
          <h2 id={headingId} className="mt-3 text-[clamp(2rem,1.6rem+1.5vw,3rem)] font-semibold leading-[1.08] tracking-[-0.03em]">{title}</h2>
          <p className="mt-4 max-w-2xl text-base leading-7 text-[var(--ds-color-muted-foreground)]">{description}</p>
        </header>

        <div className="mt-10 grid grid-cols-1 gap-4 md:grid-cols-12 lg:gap-6">
          <article className="flex min-h-[280px] flex-col justify-between rounded-[var(--ds-radius-lg)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-6 md:col-span-7 lg:p-8">
            <div>
              <p className="font-[var(--ds-font-mono)] text-[10px] uppercase tracking-[0.06em] text-[var(--ds-color-muted-foreground)]">Why choose a library</p>
              <h3 className="mt-3 max-w-lg text-xl font-semibold tracking-[-0.015em]">Move interface decisions closer to the point of use.</h3>
            </div>
            <div className="mt-10 grid grid-cols-1 gap-5 sm:grid-cols-3">
              {primaryFeatures.map((feature) => <div key={feature.label} className="border-t border-[var(--ds-color-border)] pt-3"><p className="text-sm font-semibold">{feature.label}</p><p className="mt-1 text-xs leading-5 text-[var(--ds-color-muted-foreground)]">{feature.description ?? "A concrete capability to compare."}</p></div>)}
            </div>
          </article>

          <article className="rounded-[var(--ds-radius-lg)] border border-[var(--ds-color-border-strong)] bg-[var(--ds-color-surface)] p-6 md:col-span-5 lg:p-8">
            <p className="font-[var(--ds-font-mono)] text-[10px] uppercase tracking-[0.06em] text-[var(--ds-color-muted-foreground)]">Recommended path</p>
            <h3 className="mt-3 text-xl font-semibold">{recommended?.name ?? "Choose an option"}</h3>
            <p className="mt-2 text-sm leading-6 text-[var(--ds-color-muted-foreground)]">{recommended?.description ?? "Start with the option that best fits your team."}</p>
            <div className="mt-8 border-t border-[var(--ds-color-border)] pt-5">
              <p className="text-xs text-[var(--ds-color-muted-foreground)]">Best fit when</p>
              <p className="mt-2 text-sm font-medium">You want polished defaults without giving up source ownership.</p>
            </div>
          </article>

          <article className="rounded-[var(--ds-radius-lg)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-6 md:col-span-4 lg:p-8">
            <p className="font-[var(--ds-font-mono)] text-[10px] uppercase tracking-[0.06em] text-[var(--ds-color-muted-foreground)]">Capability snapshot</p>
            <dl className="mt-6 space-y-5">
              {primaryFeatures.map((feature) => <div key={feature.label}><dt className="text-sm font-medium">{feature.label}</dt><dd className="mt-1 text-xs leading-5 text-[var(--ds-color-muted-foreground)]">{options.length} approaches compared</dd></div>)}
            </dl>
          </article>

          <article className="rounded-[var(--ds-radius-lg)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-6 md:col-span-8 lg:p-8">
            <p className="font-[var(--ds-font-mono)] text-[10px] uppercase tracking-[0.06em] text-[var(--ds-color-muted-foreground)]">Feature fit</p>
            <div className="mt-5 divide-y divide-[var(--ds-color-border-subtle)]">
              {remainingFeatures.map((feature) => <div key={feature.label} className="grid grid-cols-1 gap-3 py-4 sm:grid-cols-[minmax(0,1fr)_2fr]"><div><p className="text-sm font-medium">{feature.label}</p>{feature.description ? <p className="mt-1 text-xs leading-5 text-[var(--ds-color-muted-foreground)]">{feature.description}</p> : null}</div><div className="grid grid-cols-1 gap-2 sm:grid-cols-3">{options.map((option) => <p key={option.id} className="text-xs leading-5"><span className="font-medium">{option.name}: </span><Mark value={feature.values[option.id] ?? "Not specified"} /></p>)}</div></div>)}
            </div>
          </article>

          <div className="flex items-center justify-between gap-5 rounded-[var(--ds-radius-lg)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface-subtle)] p-6 md:col-span-12 lg:p-7">
            <div><p className="text-sm font-semibold">Keep the decision reversible.</p><p className="mt-1 text-xs leading-5 text-[var(--ds-color-muted-foreground)]">The sample data is intentionally fictional. Exported source keeps implementation choices yours.</p></div>
            <a href="#comparison-details" className={"hidden shrink-0 rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border-strong)] px-4 py-2.5 text-sm font-semibold transition-colors duration-150 hover:bg-[var(--ds-color-surface-hover)] motion-reduce:transition-none sm:inline-flex " + FOCUS}>View details</a>
          </div>
        </div>
      </div>
    </section>
  );
}
