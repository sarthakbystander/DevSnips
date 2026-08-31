import { useId } from "react";

/**
 * DevSnips React CTA — Dark Premium direction.
 *
 * A sophisticated conversion section on a pinned dark canvas (§4.3): an
 * asymmetric 5/7 split of 12 with the editorial headline block on the
 * left and a raised product/context panel on the right. One elevation step
 * above the canvas via a 1px border — no shadows, no glow, no mesh.
 *
 * The panel is a live "ship status" artifact: a real `<dl>` of release
 * pipeline telemetry, plus a quiet deployment line. The section pins the
 * dark theme mapping with `data-theme="dark"` on its own root, so it
 * consumes the same semantic tokens in both page themes — a theme mapping,
 * not a hard-coded dark page. One accent, spent on the primary CTA only
 * (§3.6):high contrast typography, thin borders, enterprise posture.
 */

export interface CtaAction {
  label: string;
  href: string;
}

export interface TelemetryRow {
  label: string;
  value: string;
}

export interface CTASectionProps {
  eyebrow?: string;
  title?: string;
  description?: string;
  primaryAction?: CtaAction;
  secondaryAction?: CtaAction;
  panelCaption?: string;
  telemetry?: TelemetryRow[];
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const PRIMARY_ACTION_CLASSES =
  "inline-flex h-11 items-center justify-center rounded-[var(--ds-radius-sm)] bg-[var(--ds-color-primary)] px-5 text-sm font-semibold leading-5 text-[var(--ds-color-primary-foreground)] transition-colors duration-150 ease-out hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)] motion-reduce:transition-none " +
  FOCUS_RING;

const SECONDARY_ACTION_CLASSES =
  "inline-flex h-11 items-center justify-center rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border-strong)] bg-transparent px-5 text-sm font-semibold leading-5 text-[var(--ds-color-foreground)] transition-colors duration-150 ease-out hover:bg-[color-mix(in_srgb,var(--ds-color-foreground)_6%,transparent)] motion-reduce:transition-none " +
  FOCUS_RING;

const DEFAULT_TELEMETRY: TelemetryRow[] = [
  { label: "Release cadence", value: "4× / day" },
  { label: "p95 deploy wall time", value: "11m 42s" },
  { label: "Rollback success", value: "99.8%" },
  { label: "Environments", value: "17" },
];

export function CTASection({
  eyebrow = "Atlas control plane",
  title = "Ship the platform your roadmap keeps promising.",
  description =
    "Deploy once to the edge, and every environment follows the same reviewed artifact. Atlas syncs builds, flags, and runtimes behind one API — no drift, no snowflake servers.",
  primaryAction = { label: "Start a private beta", href: "#beta" },
  secondaryAction = { label: "Talk to engineering", href: "#sales" },
  panelCaption = "Release pipeline — last 24 hours",
  telemetry = DEFAULT_TELEMETRY,

}: CTASectionProps) {
  const headingId = useId();
  return (
    <section
      data-theme="dark"
      aria-labelledby={headingId}
      className="bg-[var(--ds-color-background)] font-[var(--ds-font-sans)] text-[var(--ds-color-foreground)]"
    >
      <div className="mx-auto max-w-[1280px] px-4 py-[clamp(4rem,3rem+4vw,6rem)] sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 items-center gap-10 lg:grid-cols-12 lg:gap-8">
          <div className="lg:col-span-5">
            <p className="text-xs font-semibold uppercase leading-[1.3] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
              {eyebrow}
            </p>
            <h2
              id={headingId}
              className="mt-3 text-[clamp(2rem,1.7rem+1.4vw,2.75rem)] font-semibold leading-[1.1] tracking-[-0.02em]"
            >
              {title}
            </h2>
            <p className="mt-4 max-w-xl text-[clamp(1rem,0.95rem+0.25vw,1.125rem)] leading-[1.5] text-[var(--ds-color-muted-foreground)]">
              {description}
            </p>
            <div className="mt-8 flex flex-col gap-3 sm:flex-row">
              <a href={primaryAction.href} className={PRIMARY_ACTION_CLASSES}>
                {primaryAction.label}
              </a>
              <a
                href={secondaryAction.href}
                className={SECONDARY_ACTION_CLASSES}
              >
                {secondaryAction.label}
              </a>
            </div>
          </div>

          <div className="lg:col-span-7">
            <div className="rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-6 lg:p-8">
              <div className="flex items-center justify-between gap-4">
                <p className="font-[var(--ds-font-mono)] text-xs font-medium uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
                  {panelCaption}
                </p>
                <p className="flex items-center gap-2 rounded-[var(--ds-radius-full)] border border-[var(--ds-color-border)] px-3 py-1 text-xs font-medium leading-[1.4] text-[var(--ds-color-muted-foreground)]">
                  <span
                    aria-hidden="true"
                    className="h-1.5 w-1.5 rounded-full bg-[var(--ds-color-success)]"
                  />
                  Healthy
                </p>
              </div>
              <dl className="mt-6 border-t border-[var(--ds-color-border-subtle)]">
                {telemetry.map((row) => (
                  <div
                    key={row.label}
                    className="flex items-baseline justify-between gap-4 border-b border-[var(--ds-color-border-subtle)] py-4 last:border-b-0"
                  >
                    <dt className="text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
                      {row.label}
                    </dt>
                    <dd className="font-[var(--ds-font-mono)] text-sm font-medium leading-5 tabular-nums text-[var(--ds-color-foreground)]">
                      {row.value}
                    </dd>
                  </div>
                ))}
              </dl>
              <p className="mt-6 font-[var(--ds-font-mono)] text-xs leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
                Last deploy: 12 minutes ago · 0 active incidents
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}