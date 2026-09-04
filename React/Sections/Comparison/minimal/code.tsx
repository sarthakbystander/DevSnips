import { useId } from "react";
export type ComparisonValue = boolean | string;
export interface ComparisonOption { id: string; name: string; description?: string; featured?: boolean; }
export interface ComparisonFeature { label: string; description?: string; values: Record<string, ComparisonValue>; }
export interface ComparisonSectionProps { eyebrow?: string; title?: string; description?: string; options?: ComparisonOption[]; features?: ComparisonFeature[]; }
const DEFAULT_OPTIONS: ComparisonOption[] = [
  { id: "devsnips", name: "DevSnips", description: "Composable UI for working developers", featured: true },
  { id: "starter", name: "Starter kit", description: "A smaller local component set" },
  { id: "custom", name: "Build in-house", description: "Your team owns every decision" },
];
const DEFAULT_FEATURES: ComparisonFeature[] = [
  { label: "Ready-to-use React sections", values: { devsnips: true, starter: "12 sections", custom: "Build yourself" } },
  { label: "Design tokens", description: "Shared semantic values for consistent UI", values: { devsnips: true, starter: true, custom: "Custom system" } },
  { label: "Responsive states", values: { devsnips: true, starter: "Basic", custom: "Build yourself" } },
  { label: "Accessibility patterns", values: { devsnips: "Included", starter: false, custom: "Team-owned" } },
  { label: "Source ownership", values: { devsnips: "Exportable", starter: "Exportable", custom: true } },
  { label: "Ongoing maintenance", values: { devsnips: "Library updates", starter: "Self-managed", custom: "Team-owned" } },
];
const FOCUS = "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";
function State({ value }: { value: ComparisonValue }) {
  if (value === true) return <span className="inline-flex items-center gap-2 font-medium"><span aria-hidden="true">✓</span><span>Included</span></span>;
  if (value === false) return <span className="inline-flex items-center gap-2 text-[var(--ds-color-muted-foreground)]"><span aria-hidden="true">—</span><span>Not included</span></span>;
  return <span>{value}</span>;
}
export function ComparisonSection({ eyebrow="Compare approaches", title="Choose the path that keeps your product moving.", description="A compact view of what you get with a maintained UI library versus starting small or owning the system yourself.", options=DEFAULT_OPTIONS, features=DEFAULT_FEATURES }: ComparisonSectionProps) {
  const headingId = useId();
  return <section aria-labelledby={headingId} className="bg-[var(--ds-color-background)] font-[var(--ds-font-sans)] text-[var(--ds-color-foreground)]">
    <div className="mx-auto max-w-[1280px] px-4 py-[clamp(4rem,3rem+4vw,6rem)] sm:px-6 lg:px-8">
      <header className="max-w-2xl"><p className="text-xs font-semibold uppercase tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">{eyebrow}</p><h2 id={headingId} className="mt-3 text-[clamp(1.875rem,1.65rem+1vw,2.25rem)] font-semibold leading-[1.15] tracking-[-0.02em]">{title}</h2><p className="mt-4 text-base leading-6 text-[var(--ds-color-muted-foreground)]">{description}</p></header>
      <div className="mt-10 overflow-hidden rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)]"><div className="overflow-x-auto" aria-label="Comparison matrix"><table className="w-full min-w-[720px] border-collapse text-left"><caption className="sr-only">Comparison of available approaches and capabilities</caption><thead><tr className="border-b border-[var(--ds-color-border)] bg-[var(--ds-color-surface-subtle)]"><th scope="col" className="w-[34%] px-5 py-4 text-xs font-semibold uppercase tracking-[0.04em] text-[var(--ds-color-muted-foreground)]">Capability</th>{options.map((option)=><th scope="col" key={option.id} className="min-w-[180px] px-5 py-4 align-top"><div className="flex items-center gap-2"><span className="text-sm font-semibold">{option.name}</span>{option.featured?<span className="rounded-[var(--ds-radius-full)] border border-[var(--ds-color-border-strong)] px-2 py-0.5 text-[10px] font-semibold uppercase tracking-[0.04em]">Recommended</span>:null}</div>{option.description?<span className="mt-1 block text-xs font-normal leading-5 text-[var(--ds-color-muted-foreground)]">{option.description}</span>:null}</th>)}</tr></thead><tbody>{features.map((feature)=><tr key={feature.label} className="border-b border-[var(--ds-color-border-subtle)] last:border-b-0"><th scope="row" className="px-5 py-4 align-top text-sm font-medium">{feature.label}{feature.description?<span className="mt-1 block text-xs font-normal leading-5 text-[var(--ds-color-muted-foreground)]">{feature.description}</span>:null}</th>{options.map((option)=><td key={option.id} className="px-5 py-4 align-top text-sm leading-5"><State value={feature.values[option.id] ?? "Not specified"}/></td>)}</tr>)}</tbody></table></div></div>
      <p className="mt-4 text-xs leading-5 text-[var(--ds-color-muted-foreground)]">Use the matrix as a decision aid, not a scorecard. Actual capabilities can vary by implementation.</p>
    </div></section>;
}
