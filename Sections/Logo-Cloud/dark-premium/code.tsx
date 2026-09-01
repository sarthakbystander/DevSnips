import { useId } from "react";

/**
 * DevSnips React Logo Cloud — Dark Premium direction (brand-wall panel).
 *
 * An asymmetric 4/8 split on a pinned dark canvas (§4.3, §10.2): the
 * header block and one quiet link sit left; a single raised panel sits
 * right, one elevation step above the canvas with a 1px border and no
 * shadow. The panel holds a uniform ruled wall of invented wordmarks in
 * the muted ramp — a brand wall, not a badge grid — separated by
 * border-subtle hairlines.
 *
 * The section pins `data-theme="dark"` on its own root, so it consumes
 * the same semantic tokens in both page themes — a theme mapping, not a
 * hard-coded dark page. One accent, one element type: the integration
 * link (§3.6). No glow, no mesh, no gradients.
 */

export type LogoMarkKind =
  | "square"
  | "ring"
  | "diamond"
  | "triangle"
  | "hexagon"
  | "half";

export interface LogoBrand {
  name: string;
  mark: LogoMarkKind;
}

export interface LogoLink {
  label: string;
  href: string;
}

export interface LogoCloudSectionProps {
  eyebrow?: string;
  heading?: string;
  lede?: string;
  link?: LogoLink;
  panelCaption?: string;
  brands?: LogoBrand[];
}

const LINK_CLASSES =
  "mt-6 inline-flex items-center rounded-[var(--ds-radius-sm)] text-sm font-medium leading-5 text-[var(--ds-color-link)] underline underline-offset-4 transition-colors duration-150 ease-out hover:text-[var(--ds-color-link-hover)] motion-reduce:transition-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const DEFAULT_BRANDS: LogoBrand[] = [
  { name: "Northkit", mark: "square" },
  { name: "Otterline", mark: "ring" },
  { name: "Slatemark", mark: "diamond" },
  { name: "Hexfold", mark: "triangle" },
  { name: "Quarrybase", mark: "hexagon" },
  { name: "Tallybase", mark: "half" },
];

/**
 * Invented geometric brand glyph, drawn in `currentColor`. Decorative —
 * the adjacent name carries the identity — so `aria-hidden`.
 */
function LogoGlyph({
  kind,
  className,
}: {
  kind: LogoMarkKind;
  className?: string;
}) {
  return (
    <svg
      aria-hidden="true"
      viewBox="0 0 16 16"
      className={className ?? "h-4 w-4 shrink-0"}
      fill="currentColor"
    >
      {kind === "square" && <rect x="2.5" y="2.5" width="11" height="11" />}
      {kind === "ring" && (
        <circle cx="8" cy="8" r="5" fill="none" stroke="currentColor" strokeWidth="2.5" />
      )}
      {kind === "diamond" && (
        <rect x="3" y="3" width="10" height="10" transform="rotate(45 8 8)" />
      )}
      {kind === "triangle" && <path d="M8 2.5 L14.5 13.5 L1.5 13.5 Z" />}
      {kind === "hexagon" && (
        <path d="M8 1 L13.8 4.5 L13.8 11.5 L8 15 L2.2 11.5 L2.2 4.5 Z" />
      )}
      {kind === "half" && <path d="M8 2 A6 6 0 0 1 8 14 Z" />}
    </svg>
  );
}

export function LogoCloudSection({
  eyebrow = "Integrations",
  heading = "Your edge stack, observed end to end.",
  lede = "Ironvale ingests from the platforms you already operate. Instrumentation is a config flag, not a rewrite.",
  link = { label: "See every integration", href: "#integrations" },
  panelCaption = "Connected platforms",
  brands = DEFAULT_BRANDS,
}: LogoCloudSectionProps) {
  const headingId = useId();
  return (
    <section
      data-theme="dark"
      aria-labelledby={headingId}
      className="bg-[var(--ds-color-background)] font-[var(--ds-font-sans)] text-[var(--ds-color-foreground)]"
    >
      <div className="mx-auto max-w-[1280px] px-4 py-[clamp(2.5rem,2rem+2vw,4rem)] sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 gap-8 lg:grid-cols-12 lg:gap-12">
          <div className="lg:col-span-4">
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
            <a href={link.href} className={LINK_CLASSES}>
              {link.label}
            </a>
          </div>

          <div className="lg:col-span-8">
            <div className="rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-6 lg:p-8">
              <p className="font-[var(--ds-font-mono)] text-xs font-medium uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
                {panelCaption}
              </p>
              <ul className="mt-6 grid grid-cols-1 border-r border-b border-[var(--ds-color-border-subtle)] sm:grid-cols-2 lg:grid-cols-3">
                {brands.map((brand) => (
                  <li
                    key={brand.name}
                    className="flex items-center justify-center gap-2 border-l border-t border-[var(--ds-color-border-subtle)] px-6 py-5 text-[var(--ds-color-muted-foreground)]"
                  >
                    <LogoGlyph kind={brand.mark} />
                    <span className="text-sm font-semibold leading-5">{brand.name}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
