import { useId } from "react";

/**
 * DevSnips React Integrations - Dark Premium direction (connected-ecosystem).
 *
 * An asymmetric connected-ecosystem composition on a pinned dark canvas (
 * the section-level dark mapping; design tokens §4.3). A central product
 * node names the product; six integration nodes orbit it in two ruled ringss.
 *
 * Each node is a real item with the node's name and category, so the semantic
 * reading order stays intact. Hairline connection lines - 1px, muted -
 * are drawn from the central product node toward the section edges, purely
 * decorative (`aria-hidden` SVG),and never overlap text.
 *
 * The section pins `data-theme="dark"` on its own root and consumes the same
 * semantic tokens in both page themes - a theme mapping, not a hard-coded
 * dark page. Surfaces lift exactly one step above the canvas with a 1px
 * border, no shadow, no glow, no mesh. One accent:the connect action
 * (design tokens §3.6).
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

export interface IntegrationNode {
  name: string;
  category: string;
  ring: number;
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
  product?: string;
  productLabel?: string;
  nodes?: IntegrationNode[];
  link?: IntegrationLink;
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const LINK_CLASSES =
  "inline-flex h-9 items-center justify-center rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] px-4 text-sm font-semibold leading-5 text-[var(--ds-color-foreground)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] hover:border-[var(--ds-color-border-strong)] motion-reduce:transition-none " +
  FOCUS_RING;

const DEFAULT_PRODUCT = "DevSnips";

const RING_ONE = 1;

const RING_TWO = RING_ONE + RING_ONE;

const DEFAULT_NODES: IntegrationNode[] = [
  { name: "GitHub", category: "Development", ring: RING_ONE, mark: "square" },
  { name: "Slack", category: "Communication", ring: RING_ONE, mark: "ring" },
  { name: "Linear", category: "Development", ring: RING_TWO, mark: "triangle" },
  { name: "Notion", category: "Documentation", ring: RING_TWO, mark: "frame" },
  { name: "Figma", category: "Design", ring: RING_TWO, mark: "diamond" },
  { name: "Vercel", category: "Platform", ring: RING_TWO, mark: "dot" },
];

/**
 * Invented geometric node glyph drawn in `currentColor`. Decorative -
 * the adjacent name carries the identity - so `aria-hidden`.
 */
function NodeGlyph({ mark }: { mark: IntegrationMarkKind }) {
  return (
    <svg
      aria-hidden="true"
      viewBox="0 0 16 16"
      className="h-4 w-4 shrink-0"
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

/**
 * Decorative connection-line layer. Draws four static hairlines out from
 * the central product node toward the section edges. Purely decorative:
 * `aria-hidden`, behing the nodes,and the section's real content structure is
 * the `<ul>` of named nodes, so reading order stays intact.
 */

function ConnectionLines() {
  return (
    <svg
      aria-hidden="true"
      className="pointer-events-none absolute inset-0 h-full w-full text-[var(--ds-color-border)]"
      viewBox="0 0 100 100"
      preserveAspectRatio="none"
      fill="none"
      stroke="currentColor"
      strokeWidth="0.5"
    >
      <line x1="50" y1="8" x2="50" y2="0" />
      <line x1="50" y1="92" x2="50" y2="100" />
      <line x1="0" y1="46" x2="100" y2="46" />
      <line x1="0" y1="55" x2="100" y2="55" />
    </svg>
  );
}

export function IntegrationsSection({
  eyebrow = "Connected ecosystem",
  title = "DevSnips plugs into the tools your team already runs.",
  description = "One command surface for your whole toolchain - sync, verify,and ship without leaving the tools you already trust.",
  product = DEFAULT_PRODUCT,
  productLabel = "Core system",
  nodes = DEFAULT_NODES,
  link = { label: "Browse 38 integrations", href: "#integrations" },
}: IntegrationsSectionProps) {
  const headingId = useId();
  const outer = nodes.filter((node) => node.ring === RING_ONE);
  const inner = nodes.filter((node) => node.ring === RING_TWO);
  return (
    <section
      data-theme="dark"
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
          <div className="rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-6 lg:p-8">
            <div className="relative">
              <ConnectionLines />
              <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-6">
                <div className="rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border-strong)] bg-[var(--ds-color-surface-elevated)] p-5 text-center sm:col-span-2 lg:col-span-2">
                  <p className="font-[var(--ds-font-mono)] text-xs uppercase leading-[1.3] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
                    {productLabel}
                  </p>
                  <p className="mt-2 text-xl font-semibold leading-[1.3] tracking-[-0.01em]">
                    {product}
                  </p>
                </div>
                {outer.map((node) => (
                  <div
                    key={node.name}
                    className="flex items-center gap-3 rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-4"
                  >
                    <NodeGlyph mark={node.mark ?? "square"} />
                    <div className="min-w-0">
                      <p className="text-sm font-semibold leading-5">{node.name}</p>
                      <p className="text-xs leading-[1.4] text-[var(--ds-color-muted-foreground)]">
                        {node.category}
                      </p>
                    </div>
                  </div>
                ))}
                {inner.map((node) => (
                  <div
                    key={node.name}
                    className="flex items-center gap-3 rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-4"
                  >
                    <NodeGlyph mark={node.mark ?? "square"} />
                    <div className="min-w-0">
                      <p className="text-sm font-semibold leading-5">{node.name}</p>
                      <p className="text-xs leading-[1.4] text-[var(--ds-color-muted-foreground)]">
                        {node.category}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
          <div className="mt-6 flex justify-end">
            <a href={link.href} className={LINK_CLASSES}>
              {link.label}
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}