import { useId } from "react";

/**
 * DevSnips React Logo Cloud — Minimal direction (ruled brand-wall composition).
 *
 * The reference composition for the Logo Cloud family: a compact,
 * left-aligned header block above a full-width hairline brand wall (the
 * compact rhythm, §8). Every brand sits in a uniform cell separated by 1px
 * rules alone — whitespace and hairlines, never cards (§4.2). Logos are
 * invented wordmarks: one geometric glyph plus a plain name, styled
 * uniformly in the foreground token (§15). A small caption label names
 * the wall, per §11.3.
 *
 * Each wordmark is a real `<li>` inside a `<ul>`; the glyph is
 * `aria-hidden` because the adjacent name carries the brand identity. The
 * one interactive element is the quiet integration link below the wall
 * (accent for links only, §3.6).
 */

export type LogoMarkKind =
  | "square"
  | "ring"
  | "diamond"
  | "triangle"
  | "hexagon"
  | "half"
  | "frame"
  | "dot";

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
  caption?: string;
  brands?: LogoBrand[];
  link?: LogoLink;
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const LINK_CLASSES =
  "text-sm font-semibold leading-5 text-[var(--ds-color-link)] underline underline-offset-4 transition-colors duration-150 ease-out hover:text-[var(--ds-color-link-hover)] motion-reduce:transition-none " +
  FOCUS_RING;

const DEFAULT_BRANDS: LogoBrand[] = [
  { name: "Northkit", mark: "square" },
  { name: "Otterline", mark: "ring" },
  { name: "Slatemark", mark: "diamond" },
  { name: "Hexfold", mark: "triangle" },
  { name: "Quarrybase", mark: "hexagon" },
  { name: "Tallybase", mark: "half" },
  { name: "Boxframe", mark: "frame" },
  { name: "Cornmark", mark: "dot" },
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
      {kind === "frame" && (
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
      {kind === "dot" && <circle cx="8" cy="8" r="3.5" />}
    </svg>
  );
}

export function LogoCloudSection({
  eyebrow = "Ecosystem",
  heading = "Plays well with the stack you already have.",
  lede = "Waypoint previews and deploys plug straight into the tools your team already runs — no migration project, no plugin babysitting.",
  caption = "Integration partners",
  brands = DEFAULT_BRANDS,
  link = { label: "Browse the integration directory", href: "#integrations" },
}: LogoCloudSectionProps) {
  const headingId = useId();
  return (
    <section
      aria-labelledby={headingId}
      className="bg-[var(--ds-color-background)] font-[var(--ds-font-sans)] text-[var(--ds-color-foreground)]"
    >
      <div className="mx-auto max-w-[1280px] px-4 py-[clamp(2.5rem,2rem+2vw,4rem)] sm:px-6 lg:px-8">
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

        <div className="mt-10 lg:mt-12">
          <p className="font-[var(--ds-font-mono)] text-xs font-medium uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
            {caption}
          </p>
          <ul className="mt-6 grid grid-cols-1 border-r border-b border-[var(--ds-color-border)] sm:grid-cols-2 lg:grid-cols-4">
            {brands.map((brand) => (
              <li
                key={brand.name}
                className="flex items-center justify-center gap-2 border-l border-t border-[var(--ds-color-border)] px-6 py-6"
              >
                <LogoGlyph kind={brand.mark} />
                <span className="text-sm font-semibold leading-5">{brand.name}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="mt-10 lg:mt-12">
          <a href={link.href} className={LINK_CLASSES}>
            {link.label}
          </a>
        </div>
      </div>
    </section>
  );
}
