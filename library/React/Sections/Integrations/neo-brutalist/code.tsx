import { useId } from "react";

/**
 * DevSnips React Integrations - Neo-Brutalist direction (system-rack
 * composition).
 *
 * The expressive ceiling, kept disciplined (§4.5). An oversized 700
 * heading opens the section; a large central system block tops the matrix.
 * The center block is a flat accent fill (the supporting-fill budget spent in
 * a single block) carrying the product name and three spec rows. A rigid
 * grid of module blocks surrounds it: uniform 2px borders, radius-none,
 * hard 4px offset shadows( zero blur), mono index numbers, uppercase mono
 * names, anda "LINKED" connection indicator tag per module – the mechanical
 * connection language of the direction, no SVG needed. Mono category labels
 * and a short one-line description per module complete the rack.
 *
 * Collapse (§12.2): 3 columns at lg, 2 at sm, and​1 below​. The filled
 * central block uses the warning token pair, which keeps AA contrast in both
 * themes. The one action is a press-down button that translates by its
 * shadow offset on `:active` (plays 100ms). Nothing rounds, glows,
 * or gradients.
 *
 * The eyebrow is a bordered mono chip; every label is uppercase mono.
 The
 * action reads "Connect your stack".
 */

export type IntegrationMarkKind =
  |"square"
  |"ring"
  |"diamond"
  |"triangle"
  |"hexagon"
  |"half"
  |"frame"
  |"dot";

export interface SystemModule {
  name: string;
  category: string;
  description?: string;
  mark?: IntegrationMarkKind;
  initials?: string;
}

export interface SystemSpec {
  label: string;
  value: string;
}

export interface BrutalistAction {
  label: string;
  href: string;
}

export interface IntegrationsSectionProps {
  eyebrow?: string;
  title?: string;
  description?: string;
  product?: string;
  productLabel?: string;
  specs?: SystemSpec[];
  modules?: SystemModule[];
  action?: BrutalistAction;
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const ACTION_CLASSES =
  "inline-flex h-11 items-center justify-center rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] bg-[var(--ds-color-surface)] px-5 font-[var(--ds-font-mono)] text-xs font-bold uppercase leading-5 tracking-[0.05em] text-[var(--ds-color-foreground)] shadow-[4px_4px_0_0_var(--ds-color-border-strong)] transition-[transform,box-shadow] duration-100 ease-out active:translate-x-[4px] active:translate-y-[4px] active:shadow-none motion-reduce:transition-none " +
  FOCUS_RING;

const LOCKED_TAG =
  "inline-flex items-center rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] px-1.5 py-0.5 font-[var(--ds-font-mono)] text-[10px] font-bold uppercase leading-none tracking-[0.05em]";

const DEFAULT_PRODUCT = "DevSnips";

const DEFAULT_SPECS: SystemSpec[] = [
  { label: "Module", value: "Core" },
  { label: "Channels", value: "38" },
  { label: "Status", value: "Linked" },
];

const DEFAULT_MODULES: SystemModule[] = [
  {
    name: "GitHub",
    category: "Development",
    mark: "square",
    description: "Issues, PRs, releases,,and repo events in sync.",
  },
  {
    name: "Slack",
    category: "Communication",
    mark: "ring",
    description: "Alerts, digests,,and approvals routed to channels.",
  },
  {
    name: "Linear",
    category: "Development",
    mark: "triangle",
    description: "Tickets, roadmaps,,and ship status mirrored.",
  },
  {
    name: "Notion",
    category: "Documentation",
    mark: "frame",
    description: "Docs, specs,,and changelogs published.",
  },
  {
    name: "Figma",
    category: "Design",
    mark: "diamond",
    description: "Tokens and component specs stay current.",
  },
];

/**
 * Compact identity tile:an invented geometric mark or a two-letter text
 * tile. Decorative - the adjacent name carries the identity - so
 * `aria-hidden`.
 */
function IntegrationGlyph({
  mark,
  initials,
  className,
}: {
  mark?: IntegrationMarkKind;
  initials?: string;
  className?: string;
}) {
  if (!mark) {
    return initials ? (
      <span
        aria-hidden="true"
        className={
          "flex h-7 w-7 shrink-0 items-center justify-center rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] text-[11px] font-bold leading-none " +
          (className ?? "")
        }
      >
        {initials}
      </span>
    ) : null;
  }
  return (
    <svg
      aria-hidden="true"
      viewBox="0 0 16 16"
      className={className ?? "h-5 w-5 shrink-0"}
      fill="currentColor"
    >
      {mark === "square" && <rect x="2.5" y="2.5" width="11" height="11" />}
      {mark === "ring" && (
        <circle cx="8" cy="8" r="5" fill="none" stroke="currentColor" strokeWidth="2.5" />
      )}
      {mark === "diamond" && (
        <rect x="3" y="3" width="10" height="10" transform="rotate(45 8 8)" />
      )}
      {mark === "triangle" && <path d="M8 2.5 L14.5 13.5 L1.5 13.5 Z" />}
      {mark === "hexagon" && (
        <path d="M8 1 L13.8 4.5 L13.8 11.5 L8 15 L2.2 11.5 L2.2 4.5 Z" />
      )}
      {mark === "half" && <path d="M8 2 A6 6 0 0 1 8 14 Z" />}
      {mark === "frame" && (
        <rect
          x="2.5"
          y="2.5"
          width="11"
          height="11"
          fill="none"
          stroke="currentColor"
          strokeWidth="2.5"
        />
      )}
      {mark === "dot" && <circle cx="8" cy="8" r="3.5" />}
    </svg>
  );
}

export function IntegrationsSection({
  eyebrow = "Integration ecosystem",
  title = "INTEGRATIONS",
  description = "Brightbox routes your existing tools into one command surface - no wrappers, no rewrites, no plugins to babysit.",
  product = DEFAULT_PRODUCT,
  productLabel = "Core system",
  specs = DEFAULT_SPECS,
  modules = DEFAULT_MODULES,
  action = { label: "Connect your stack", href: "#integrations" },
}: IntegrationsSectionProps) {
  const headingId = useId();
  return (
    <section
      aria-labelledby={headingId}
      className="bg-[var(--ds-color-background)] font-[var(--ds-font-sans)] text-[var(--ds-color-foreground)]"
    >
      <div className="mx-auto max-w-[1280px] px-4 py-[clamp(4rem,3rem+4vw,6rem)] sm:px-6 lg:px-8">
        <div className="max-w-3xl">
          <p className="inline-block rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] bg-[var(--ds-color-surface)] px-3 py-1 font-[var(--ds-font-mono)] text-xs font-semibold uppercase leading-[1.3] tracking-[0.05em] shadow-[4px_4px_0_0_var(--ds-color-border-strong)]">
            {eyebrow}
          </p>
          <h2
            id={headingId}
            className="mt-6 text-[clamp(2.5rem,1.9rem+2.8vw,3.5rem)] font-bold leading-[1.1] tracking-[-0.02em]"
          >
            {title}
          </h2>
          <p className="mt-4 max-w-2xl text-[clamp(1rem,0.95rem+0.25vw,1.125rem)] leading-[1.5] text-[var(--ds-color-muted-foreground)]">
            {description}
          </p>
        </div>

        <div className="mt-12 lg:mt-16">
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
            <div className="rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] bg-[var(--ds-color-warning)] p-6 text-[var(--ds-color-warning-foreground)] shadow-[4px_4px_0_0_var(--ds-color-border-strong)] sm:col-span-2 lg:col-span-3 lg:p-8">
              <p className="font-[var(--ds-font-mono)] text-xs font-bold uppercase leading-[1.4] tracking-[0.05em]">
                {productLabel}
              </p>
              <p className="mt-4 font-[var(--ds-font-mono)] text-2xl font-bold uppercase leading-[1.2] tracking-[0.02em]">
                {product}
              </p>
              <dl className="mt-6 grid grid-cols-1 gap-0 sm:grid-cols-3">
                {specs.map((spec) => (
                  <div
                    key={spec.label}
                    className="border-t-2 border-[var(--ds-color-border-strong)] pt-3 sm:border-t-0 sm:border-l-2 sm:pl-4 first:border-t-0 first:pt-0"
                  >
                    <dt className="text-xs font-semibold uppercase leading-[1.4] tracking-[0.05em]">
                      {spec.label}
                    </dt>
                    <dd className="mt-1 text-sm font-bold leading-5">{spec.value}</dd>
                  </div>
                ))}
              </dl>
            </div>

            {modules.map((module, index) => (
              <div
                key={module.name}
                className="rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] bg-[var(--ds-color-surface)] p-6 text-[var(--ds-color-foreground)] shadow-[4px_4px_0_0_var(--ds-color-border-strong)]"
              >
                <div className="flex items-start justify-between gap-3">
                  <p className="font-[var(--ds-font-mono)] text-xs font-semibold uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
                    {String(index + 1).padStart(2, "0")}
                  </p>
                  <p className={LOCKED_TAG + " text-[var(--ds-color-muted-foreground)]"}>
                    Linked
                  </p>
                </div>
                <div className="mt-8 flex items-center gap-3">
                  <IntegrationGlyph mark={module.mark} initials={module.initials} />
                  <p className="font-[var(--ds-font-mono)] text-sm font-bold uppercase leading-5 tracking-[0.05em]">
                    {module.name}
                  </p>
                </div>
                <p className="mt-2 text-xs uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
                  {module.category}
                </p>
                {module.description ? (
                  <p className="mt-4 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
                    {module.description}
                  </p>
                ) : null}
              </div>
            ))}
          </div>

          <div className="mt-12">
            <a href={action.href} className={ACTION_CLASSES}>
              {action.label}
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}