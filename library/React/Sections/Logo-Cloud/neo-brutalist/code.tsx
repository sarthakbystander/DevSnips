import { useId } from "react";

/**
 * DevSnips React Logo Cloud — Neo-Brutalist direction (brand-matrix
 * composition).
 *
 * The expressive ceiling, kept disciplined (§4.5): six square brand cells
 * with uniform 2px borders, hard 4px offset shadows (zero blur), mono
 * index numbers, and uppercase mono wordmarks. One cell is a flat accent
 * fill — the supporting-fill budget spent in a single block — everything
 * else is flat surface. The eyebrow is a bordered chip; the one action is
 * a press-down button that translates by its shadow offset on :active
 * (≤100ms). Nothing rounds, glows, or gradients.
 *
 * Collapse (§12.2): 3 columns at lg, 2 at sm, 1 below. The filled cell
 * uses the warning token pair, which keeps AA contrast in both themes.
 * Wordmark glyphs are invented geometry, `aria-hidden`.
 */

export type LogoMarkKind =
  | "square"
  | "ring"
  | "diamond"
  | "triangle"
  | "hexagon"
  | "half";

export interface BrutalistBrand {
  name: string;
  mark: LogoMarkKind;
  filled?: boolean;
}

export interface LogoAction {
  label: string;
  href: string;
}

export interface LogoCloudSectionProps {
  eyebrow?: string;
  heading?: string;
  lede?: string;
  brands?: BrutalistBrand[];
  action?: LogoAction;
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const ACTION_CLASSES =
  "inline-flex h-11 items-center justify-center rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] bg-[var(--ds-color-surface)] px-5 text-sm font-semibold leading-5 text-[var(--ds-color-foreground)] shadow-[4px_4px_0_0_var(--ds-color-border-strong)] transition-[transform,box-shadow] duration-100 ease-out active:translate-x-[4px] active:translate-y-[4px] active:shadow-none motion-reduce:transition-none " +
  FOCUS_RING;

const DEFAULT_BRANDS: BrutalistBrand[] = [
  { name: "Northkit", mark: "square" },
  { name: "Otterline", mark: "ring" },
  { name: "Slatemark", mark: "diamond", filled: true },
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
      className={className ?? "h-5 w-5 shrink-0"}
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
  heading = "Plugs into the stack you already have.",
  lede = "Brightbox meets your toolchain where it lives. No wrappers, no rewrites, no plugins to babysit.",
  brands = DEFAULT_BRANDS,
  action = { label: "Read the integration guides", href: "#integrations" },
}: LogoCloudSectionProps) {
  const headingId = useId();
  return (
    <section
      aria-labelledby={headingId}
      className="bg-[var(--ds-color-background)] font-[var(--ds-font-sans)] text-[var(--ds-color-foreground)]"
    >
      <div className="mx-auto max-w-[1280px] px-4 py-[clamp(2.5rem,2rem+2vw,4rem)] sm:px-6 lg:px-8">
        <div className="max-w-2xl">
          <p className="inline-block rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] bg-[var(--ds-color-surface)] px-3 py-1 font-[var(--ds-font-mono)] text-xs font-semibold uppercase leading-[1.3] tracking-[0.05em] shadow-[4px_4px_0_0_var(--ds-color-border-strong)]">
            {eyebrow}
          </p>
          <h2
            id={headingId}
            className="mt-6 text-[clamp(1.875rem,1.65rem+1vw,2.25rem)] font-bold leading-[1.15] tracking-[-0.02em]"
          >
            {heading}
          </h2>
          <p className="mt-4 max-w-xl text-[clamp(1rem,0.95rem+0.25vw,1.125rem)] leading-[1.5] text-[var(--ds-color-muted-foreground)]">
            {lede}
          </p>
        </div>

        <ul className="mt-12 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {brands.map((brand, index) => (
            <li
              key={brand.name}
              className={
                "rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] p-6 shadow-[4px_4px_0_0_var(--ds-color-border-strong)] sm:p-8 " +
                (brand.filled
                  ? "bg-[var(--ds-color-warning)] text-[var(--ds-color-warning-foreground)]"
                  : "bg-[var(--ds-color-surface)] text-[var(--ds-color-foreground)]")
              }
            >
              <p
                className={
                  "font-[var(--ds-font-mono)] text-xs font-semibold uppercase leading-[1.4] tracking-[0.05em] " +
                  (brand.filled ? "" : "text-[var(--ds-color-muted-foreground)]")
                }
              >
                {String(index + 1).padStart(2, "0")}
              </p>
              <div className="mt-8 flex items-center gap-3">
                <LogoGlyph kind={brand.mark} />
                <span className="font-[var(--ds-font-mono)] text-sm font-bold uppercase leading-5 tracking-[0.05em]">
                  {brand.name}
                </span>
              </div>
            </li>
          ))}
        </ul>

        <div className="mt-12">
          <a href={action.href} className={ACTION_CLASSES}>
            {action.label}
          </a>
        </div>
      </div>
    </section>
  );
}
