import { useId } from "react";

/**
 * DevSnips React Logo Cloud — Bento composition (Bento direction).
 *
 * A modular 12-column cell grid for an asymmetric brand ecosystem (§4.4):
 * one hero cell (span 8) gives the anchor brand a larger visual presence,
 * one statement cell (span 4) carries the integration count as the single
 * accent element, and seven supporting brand cells (span 3–4) complete
 * the grid. Cells share one radius (radius-lg), one 1px border, one
 * uniform gap, and a border-strong hover lift — no scale, no glow.
 *
 * Collapse (§12.2): two equal columns at sm (hero and statement cells
 * span both), one column below. Intentionally action-free: the cells are
 * the content. Wordmark glyphs are invented geometry, `aria-hidden`.
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

export interface FeaturedBrand extends LogoBrand {
  descriptor: string;
}

export interface EcosystemStatement {
  value: string;
  label: string;
  context: string;
}

export interface LogoCloudSectionProps {
  eyebrow?: string;
  heading?: string;
  lede?: string;
  featured?: FeaturedBrand;
  statement?: EcosystemStatement;
  brands?: LogoBrand[];
}

const CELL_CLASSES =
  "rounded-[var(--ds-radius-lg)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-6 transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] motion-reduce:transition-none lg:p-8";

const DEFAULT_FEATURED: FeaturedBrand = {
  name: "Northkit",
  mark: "square",
  descriptor: "Build orchestration — everything downstream of git push.",
};

const DEFAULT_STATEMENT: EcosystemStatement = {
  value: "38",
  label: "Maintained integrations",
  context: "Each one versioned, tested, and documented",
};

const DEFAULT_BRANDS: LogoBrand[] = [
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
  heading = "One pipeline, your whole toolchain.",
  lede = "Flowgate orchestrates builds across the CI, registry, and runtime your team already uses.",
  featured = DEFAULT_FEATURED,
  statement = DEFAULT_STATEMENT,
  brands = DEFAULT_BRANDS,
}: LogoCloudSectionProps) {
  const headingId = useId();
  const leading = brands.slice(0, 4);
  const trailing = brands.slice(4);
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

        <ul className="mt-10 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:mt-12 lg:grid-cols-12 lg:gap-6">
          <li className={CELL_CLASSES + " sm:col-span-2 lg:col-span-8"}>
            <div className="flex items-center gap-4">
              <LogoGlyph kind={featured.mark} className="h-6 w-6 shrink-0" />
              <div>
                <p className="text-2xl font-semibold leading-[1.25] tracking-[-0.01em]">
                  {featured.name}
                </p>
                <p className="mt-1 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
                  {featured.descriptor}
                </p>
              </div>
            </div>
          </li>

          <li className={CELL_CLASSES + " sm:col-span-2 lg:col-span-4"}>
            <p className="text-[clamp(1.75rem,1.5rem+1.2vw,2.25rem)] font-semibold leading-[1.2] tracking-[-0.02em] tabular-nums text-[var(--ds-color-accent)]">
              {statement.value}
            </p>
            <p className="mt-2 text-sm leading-5 text-[var(--ds-color-foreground)]">
              {statement.label}
            </p>
            <p className="mt-6 font-[var(--ds-font-mono)] text-xs uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
              {statement.context}
            </p>
          </li>

          {leading.map((brand) => (
            <li key={brand.name} className={CELL_CLASSES + " lg:col-span-3"}>
              <div className="flex items-center gap-2">
                <LogoGlyph kind={brand.mark} />
                <span className="text-sm font-semibold leading-5">{brand.name}</span>
              </div>
            </li>
          ))}

          {trailing.map((brand) => (
            <li key={brand.name} className={CELL_CLASSES + " lg:col-span-4"}>
              <div className="flex items-center gap-2">
                <LogoGlyph kind={brand.mark} />
                <span className="text-sm font-semibold leading-5">{brand.name}</span>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
