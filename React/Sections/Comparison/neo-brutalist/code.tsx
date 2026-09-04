import { useId } from "react";

export type ComparisonValue = boolean | string;
export interface ComparisonOption { id: string; name: string; description?: string; featured?: boolean; }
export interface ComparisonFeature { label: string; description?: string; values: Record<string, ComparisonValue>; }
export interface ComparisonSectionProps { eyebrow?: string; title?: string; description?: string; options?: ComparisonOption[]; features?: ComparisonFeature[]; }

const DEFAULT_OPTIONS: ComparisonOption[] = [
  { id: "devsnips", name: "DevSnips", description: "Structured, exportable UI", featured: true },
  { id: "starter", name: "Starter", description: "Lean baseline" },
  { id: "custom", name: "In-house", description: "Total team ownership" },
];
const DEFAULT_FEATURES: ComparisonFeature[] = [
  { label: "Section library", values: { devsnips: "Curated", starter: "Small", custom: "Build" } },
  { label: "Accessible states", values: { devsnips: true, starter: "Review", custom: "Own" } },
  { label: "Responsive layouts", values: { devsnips: true, starter: "Core", custom: "Own" } },
  { label: "Semantic tokens", values: { devsnips: true, starter: "Basic", custom: "Custom" } },
  { label: "Exportable source", values: { devsnips: true, starter: true, custom: true } },
];
const FOCUS = "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";
function Status({ value }: { value: ComparisonValue }) {
  if (value === true) return <span className="font-semibold">YES <span className="sr-only">, included</span></span>;
  if (value === false) return <span className="font-semibold">NO <span className="sr-only">, not included</span></span>;
  return <span>{value}</span>;
}

export function ComparisonSection({
  eyebrow = "Comparison / field notes",
  title = "Make the architecture visible.",
  description = "A rigid comparison for teams that prefer decisions to be explicit, measurable, and easy to scan.",
  options = DEFAULT_OPTIONS,
  features = DEFAULT_FEATURES,
}: ComparisonSectionProps) {
  const headingId = useId();
  return (
    <section aria-labelledby={headingId} className="overflow-x-clip bg-[var(--ds-color-background)] font-[var(--ds-font-sans)] text-[var(--ds-color-foreground)]">
      <div className="mx-auto max-w-[1280px] px-4 py-[clamp(4rem,3rem+4vw,6rem)] sm:px-6 lg:px-8">
        <div className="grid gap-8 border-b-2 border-[var(--ds-color-border-strong)] pb-10 lg:grid-cols-[1.2fr_0.8fr] lg:items-end">
          <div>
            <p className="font-[var(--ds-font-mono)] text-xs font-bold uppercase tracking-[0.05em]">{eyebrow}</p>
            <h2 id={headingId} className="mt-3 max-w-4xl text-[clamp(2.5rem,2rem+2vw,4rem)] font-bold uppercase leading-[0.95] tracking-[-0.035em]">{title}</h2>
          </div>
          <p className="max-w-md text-sm leading-6">{description}</p>
        </div>

        <div className="mt-8 max-w-full overflow-x-auto" role="region" aria-label="Comparison matrix">
          <table className="w-full min-w-[760px] border-collapse border-2 border-[var(--ds-color-border-strong)] bg-[var(--ds-color-surface)] text-left">
            <thead>
              <tr className="border-b-2 border-[var(--ds-color-border-strong)] bg-[var(--ds-color-surface-subtle)]">
                <th scope="col" className="w-[30%] border-r-2 border-[var(--ds-color-border-strong)] px-4 py-4 font-[var(--ds-font-mono)] text-xs uppercase">Feature</th>
                {options.map((option) => <th scope="col" key={option.id} className={"border-r-2 border-[var(--ds-color-border-strong)] px-4 py-4 align-top last:border-r-0 " + (option.featured ? "bg-[var(--ds-color-accent-soft)]" : "")}><span className="block text-base font-bold uppercase">{option.name}</span>{option.description ? <span className="mt-1 block text-xs font-normal leading-5">{option.description}</span> : null}{option.featured ? <span className="mt-3 inline-block border-2 border-[var(--ds-color-border-strong)] px-2 py-1 font-[var(--ds-font-mono)] text-[10px] font-bold uppercase">Recommended</span> : null}</th>)}
              </tr>
            </thead>
            <tbody>
              {features.map((feature) => <tr key={feature.label} className="border-b-2 border-[var(--ds-color-border-strong)] last:border-b-0"><th scope="row" className="border-r-2 border-[var(--ds-color-border-strong)] px-4 py-4 align-top font-bold uppercase">{feature.label}{feature.description ? <span className="mt-1 block font-sans text-xs font-normal normal-case leading-5">{feature.description}</span> : null}</th>{options.map((option) => <td key={option.id} className={"border-r-2 border-[var(--ds-color-border-strong)] px-4 py-4 align-top text-sm last:border-r-0 " + (option.featured ? "bg-[var(--ds-color-accent-soft)]" : "")}><Status value={feature.values[option.id] ?? "Not specified"} /></td>)}</tr>)}
            </tbody>
          </table>
        </div>

        <div className="mt-8 grid gap-4 border-2 border-[var(--ds-color-border-strong)] p-5 shadow-[4px_4px_0_0_var(--ds-color-border-strong)] sm:grid-cols-[1fr_auto] sm:items-center">
          <div><p className="font-[var(--ds-font-mono)] text-xs font-bold uppercase">Decision rule</p><p className="mt-2 text-sm leading-6">Prefer the option that reduces repeated interface decisions without hiding the implementation.</p></div>
          <a href="#choose" className={"inline-flex min-h-11 items-center justify-center border-2 border-[var(--ds-color-border-strong)] bg-[var(--ds-color-primary)] px-5 text-sm font-bold uppercase text-[var(--ds-color-primary-foreground)] shadow-[4px_4px_0_0_var(--ds-color-border-strong)] transition-transform duration-75 active:translate-x-1 active:translate-y-1 active:shadow-none motion-reduce:transition-none " + FOCUS}>Choose a path</a>
        </div>
      </div>
    </section>
  );
}
