import { useId } from "react";

/**
 * DevSnips React Integrations — Minimal direction (ruled integration directory).
 *
 * The reference composition for the Integrations family: a restrained,
 * documentation-style directory. A tight header block names the ecosystem,
 * then a ruled list of integrations sits below — hairline rules, whitespace,
 * and typography carry the hierarchy, never cards (§4.2). Each row is a
 * real `<li>` with a compact visual identity treatment (invented geometric
 * glyph or initials, aria-hidden, name adjacent) a mono category label,
 * and a short description where provided.
 *
 * One accent for the directory link only (§3.6). Hover states are borders
 * and color fades only; there is no card, no shadow, no decoration.
 */

export type IntegrationMarkKind =
  | "square"
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

export interface IntegrationLink {
   label: string;
   href: string;
}

export interface IntegrationsSectionProps {
   eyebrow?: string;
   title?: string;
   description?: string;
   integrations?: Integration[];
   link?: IntegrationLink;
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const LINK_CLASSES =
  "text-sm font-semibold leading-5 text-[var(--ds-color-link)] underline underline-offset-4 transition-colors duration-150 ease-out hover:text-[var(--ds-color-link-hover)] motion-reduce:transition-none " +
  FOCUS_RING;

const DEFAULT_INTEGRATIONS: Integration[] = [
  {
    name: "GitHub",
    category: "Development",
    mark: "square",
    description:
      "Two-way sync for issues, pull requests,and deploy hooks, right from your workspace.",
  },
  {
    name: "Slack",
    category: "Communication",
    mark: "ring",
    description:
      "Route alerts, approvals,and digests into the channels your team already watches.",
  },
  {
    name: "Linear",
    category: "Development",
    mark: "triangle",
    description:
      "Mirror tickets and ship status back to Linear without leaving your flow.",
  },
  {
    name: "Notion",
    category: "Documentation",
    mark: "frame",
    description:
      "Publish runbooks, specs,and changelogs into Notion with one click.",
  },
  {
    name: "Figma",
    category: "Design",
    mark: "diamond",
    description:
      "Sync design tokens and component specs as the source of truth evolves.",
  },
  {
    name: "Vercel",
    category: "Platform",
    mark: "dot",
    description:
      "Preview sandboxes and production deploys straight from every pull request.",
  },
  {
    name: "Sentry",
    category: "Observability",
    mark: "half",
    description:
      "Attach stack traces and release context to every incidentas it opens.",
  },
  {
    name: "Stripe",
    category: "Finance",
    mark: "hexagon",
    description:
      "Reconcile invoices, payments,and failed-charge retries in one ledger.",
  },
];

/**
 * Compact identity treatment: an invented geometric mark drawn in
 * `currentColor`, or a two-letter text tile when only initials are
 * provided. Decorative — the adjacent name carries the identity — so
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
  eyebrow = "Works with your stack",
  title = "Connect the tools you already use.",
  description = "Bring your existing workflow into one place with integrations designed around the tools your team relies on.",
  integrations = DEFAULT_INTEGRATIONS,
  link = { label: "View all integrations", href: "#integrations" },
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

        <ul className="mt-12 border-t border-[var(--ds-color-border)] lg:mt-16">
          {integrations.map((integration) => (
            <li
              key={integration.name}
              className="grid grid-cols-1 gap-2 border-b border-[var(--ds-color-border)] py-5 md:grid-cols-12 md:gap-6"
            >
              <div className="flex min-w-0 items-center gap-3 md:col-span-4">
                <IntegrationGlyph
                  mark={integration.mark}
                  initials={integration.initials}
                />
                <div className="min-w-0">
                  <p className="text-sm font-semibold leading-5">{integration.name}</p>
                  {integration.category ? (
                    <p className="font-[var(--ds-font-mono)] text-xs leading-[1.4] text-[var(--ds-color-muted-foreground)]">
                      {integration.category}
                    </p>
                  ) : null}
                </div>
              </div>
              {integration.description ? (
                <p className="text-sm leading-5 text-[var(--ds-color-muted-foreground)] md:col-span-8">
                  {integration.description}
                </p>
              ) : null}
            </li>
          ))}
        </ul>

        <div className="mt-12 lg:mt-16">
          <a href={link.href} className={LINK_CLASSES}>
            {link.label}
          </a>
        </div>
      </div>
    </section>
  );
}