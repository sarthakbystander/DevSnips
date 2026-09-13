import { useId } from "react";

/**
 * DevSnips React Integrations - Bento composition (Bento direction).
 *
 * A modular 12-column cell grid for an integrations ecosystem (§4.4):
 * one large featured integration cell (span 7) carrying the anchor pair's
 * name, tagline, category, and description; one showcase cell (span 5)
 * holding four compact tool rows; three category cells (span 4 each)
 * grouping Development, Design, and Communication tools with short per-tool
 * descriptions; and a full-width ecosystem strip below connecting the count
 * to the integration directory link.

 * Cells share one radius (radius-lg), one 1px border, one uniform gap,
 * anda border-strong hover lift (no scale, no glow). At most one hero cell,
 * at most two accent cells: the featured tagline chip and the ecosystem count
 * (§4.4). The featured cell is intentionally not a logo-card — it reads
 * as a product ecosystem anchor, not a badge grid.

 * Collapse (§12.2):  two equal columns at sm (hero and showcase span
 * both), one column below. The category cells shrink into the hero column at
 * sm? No - the whole grid flips to a 2-col equal layout, then 1-col.

 * Whole grid is a real `<ul>`/`<li>`; every tool name is readable text
 * adjacent to an `aria-hidden` invented glyph or a text tile.
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

export interface Integration {
  name: string;
  description?: string;
  category?: string;
  initials?: string;
  mark?: IntegrationMarkKind;
}

export interface FeaturedIntegration extends Integration {
  tagline: string;
}

export interface CategoryCell {
  label: string;
  integrations: Integration[];
}

export interface IntegrationLink {
  label: string;
  href: string;
}

export interface IntegrationsSectionProps {
  eyebrow?: string;
  title?: string;
  description?: string;
  featured?: FeaturedIntegration;
  showcase?: CategoryCell;
  categories?: CategoryCell[];
  countValue?: string;
  countLabel?: string;
  link?: IntegrationLink;
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const LINK_CLASSES =
  "text-sm font-semibold leading-5 text-[var(--ds-color-link)] underline underline-offset-4 transition-colors duration-150 ease-out hover:text-[var(--ds-color-link-hover)] motion-reduce:transition-none " +
  FOCUS_RING;

const CELL_CLASSES =
  "rounded-[var(--ds-radius-lg)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-6 transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] motion-reduce:transition-none lg:p-8";

const DEFAULT_FEATURED: FeaturedIntegration = {
  name: "GitHub",
  category: "Development",
  mark: "square",
  tagline: "The anchor of your repo workflow",
  description:
    "Every issue, pull request, and release in your workspace stays in sync with GitHub. Fine-grained permissions follow your repo structure, so governance ships with the code.",
};

const DEFAULT_SHOWCASE: CategoryCell = {
  label: "Recent connections",
  integrations: [
    { name: "Slack", category: "Channels and alerts", mark: "ring", description: "Route digests and approvals into the channels your team already watches." },
    { name: "Linear", category: "Issue tracking", mark: "triangle", description: "Mirror tickets and ship status back to Linear without leaving your flow." },
    { name: "Vercel", category: "Deploys", mark: "dot", description: "Preview sandboxes and production deploys straight from every pull request." },
    { name: "Sentry", category: "Errors", mark: "half", description: "Attach stack traces and release context to every incidentas it opens." },
  ],
};

const DEFAULT_CATEGORIES: CategoryCell[] = [
  {
    label: "Development",
    integrations: [
      { name: "GitHub", mark: "square", description: "Issues, PRs,, and release sync." },
      { name: "Linear", mark: "triangle", description: "Tickets and roadmap mirrors." },
    ],
  },
  {
    label: "Design",
    integrations: [
      { name: "Figma", mark: "diamond", description: "Design tokens and specs stay current." },
      { name: "Notion", mark: "frame", description: "Docs, runbooks,,and specs publish." },
    ],
  },
  {
    label: "Communication",
    integrations: [
      { name: "Slack", mark: "ring", description: "Alerts, digests,,and approvals." },
      { name: "Stripe", mark: "hexagon", description: "Invoices,,payments,,and receipts." },
    ],
  },
];

/**
 * Compact identity treatment:an invented geometric mark drawn in
 * `currentColor`. When only initials are provided,a bordered two-letter text
 * tile is used instead. Decorative - the adjacent name carries the identity -
 * so `aria-hidden`.
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
          "flex h-8 w-8 shrink-0 items-center justify-center rounded-[var(--ds-radius-xs)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] text-xs font-semibold leading-none text-[var(--ds-color-muted-foreground)] " +
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
      className={className ?? "h-4 w-4 shrink-0"}
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
  eyebrow = "Ecosystem",
  title = "One workspace, every tool your team ships through.",
  description = "Flowgate routes your existing tools into one command surface, so context never has to leave the team's flow.",
  featured = DEFAULT_FEATURED,
  showcase = DEFAULT_SHOWCASE,
  categories = DEFAULT_CATEGORIES,
  countValue = "38",
  countLabel = "maintained integrations",
  link = { label: "Browse the connection directory", href: "#integrations" },
}: IntegrationsSectionProps) {
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
            {title}
          </h2>
          <p className="mt-4 text-[clamp(1rem,0.95rem+0.25vw,1.125rem)] leading-[1.5] text-[var(--ds-color-muted-foreground)]">
            {description}
          </p>
        </div>

        <div className="mt-12 lg:mt-16">
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-12 lg:gap-6">
            <div
              className={
                CELL_CLASSES +
                " sm:col-span-2 lg:col-span-7"
              }
            >
              <div className="flex items-center gap-4">
                <IntegrationGlyph mark={featured.mark} initials={featured.initials} className="h-6 w-6 shrink-0" />
                <div className="min-w-0">
                  <p className="text-xl font-semibold leading-[1.3] tracking-[-0.01em]">
                    {featured.name}
                  </p>
                  <p className="text-xs leading-[1.4] text-[var(--ds-color-muted-foreground)]">
                    {featured.category}
                  </p>
                </div>
              </div>
              <p className="mt-6 inline-flex items-center rounded-[var(--ds-radius-xs)] bg-[color-mix(in_srgb,var(--ds-color-accent)_10%,var(--ds-color-surface))] px-2 py-1 font-[var(--ds-font-mono)] text-xs font-semibold uppercase leading-[1.3] tracking-[0.05em] text-[var(--ds-color-accent)]">
                {featured.tagline}
              </p>
              <p className="mt-4 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
                {featured.description}
              </p>
            </div>

            <div className={CELL_CLASSES + " sm:col-span-2 lg:col-span-5"}>
              <p className="font-[var(--ds-font-mono)] text-xs font-medium uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
                {showcase.label}
              </p>
              <ul className="mt-4 divide-y divide-[var(--ds-color-border-subtle)]">
                {showcase.integrations.map((integration) => (
                  <li key={integration.name} className="flex items-start gap-3 py-3 first:pt-0 last:pb-0">
                    <IntegrationGlyph mark={integration.mark} initials={integration.initials} />
                    <div className="min-w-0">
                      <p className="text-sm font-semibold leading-5">{integration.name}</p>
                      <p className="text-xs leading-[1.4] text-[var(--ds-color-muted-foreground)]">
                        {integration.category}
                      </p>
                    </div>
                  </li>
                ))}
              </ul>
            </div>

            {categories.map((category) => (
              <div
                key={category.label}
                className={CELL_CLASSES + " lg:col-span-4"}
              >
                <p className="font-[var(--ds-font-mono)] text-xs font-medium uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
                  {category.label}
                </p>
                <ul className="mt-4 space-y-3">
                  {category.integrations.map((integration) => (
                    <li key={integration.name} className="flex items-start gap-3">
                      <IntegrationGlyph mark={integration.mark} initials={integration.initials} />
                      <div className="min-w-0">
                        <p className="text-sm font-semibold leading-5">{integration.name}</p>
                        {integration.description ? (
                          <p className="text-xs leading-[1.4] text-[var(--ds-color-muted-foreground)]">
                            {integration.description}
                          </p>
                        ) : null}
                      </div>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>

          <div className="mt-6 flex flex-col items-start justify-between gap-4 rounded-[var(--ds-radius-lg)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-6 sm:flex-row sm:items-center lg:mt-8 lg:p-8">
            <p className="text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
              <span className="font-semibold tabular-nums text-[var(--ds-color-accent)]">{countValue}</span>
              {" " + countLabel}
            </p>
            <a href={link.href} className={LINK_CLASSES}>
              {link.label}
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}