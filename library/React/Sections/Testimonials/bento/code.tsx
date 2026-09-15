import { useId } from "react";

/**
 * DevSnips React Testimonials — Bento composition (Bento direction).
 *
 * A modular 12-column cell grid for mixed-weight social proof (§4.4):
 * one hero quote cell (span 7) with the longest testimonial, one evidence
 * cell (span 5) carrying a single outcome stat, and three single-quote
 * supporting cells (span 4 each). Cells share one radius (radius-lg), one
 * 1px border, and a uniform gap (16px mobile / 24px desktop). Collapse:
 * authored spans at lg, large cells span both columns at sm, everything
 * stacks below (§12.2).
 *
 * One accent, spent on the stat number — the only non-neutral text.
 * Hover is a border-strong lift only. Intentionally action-free: the
 * cells are the content. Avatars are initials, `aria-hidden`.
 */

export interface BentoQuote {
  quote: string;
  name: string;
  initials: string;
  role: string;
  company: string;
}

export interface BentoStat {
  value: string;
  label: string;
  context: string;
}

export interface TestimonialsSectionProps {
  eyebrow?: string;
  heading?: string;
  lede?: string;
  heroQuote?: BentoQuote;
  stat?: BentoStat;
  quotes?: BentoQuote[];
}

const CELL_CLASSES =
  "rounded-[var(--ds-radius-lg)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-6 transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] motion-reduce:transition-none lg:p-8";

const DEFAULT_HERO_QUOTE: BentoQuote = {
  quote:
    "We used to learn about outages from support tickets. Pingline pages the right person with the failing check, the recent deploys, and the likely blast radius — most incidents are acknowledged before the first customer email arrives.",
  name: "Yuki Tanaka",
  initials: "YT",
  role: "Staff SRE",
  company: "Cairn Systems",
};

const DEFAULT_STAT: BentoStat = {
  value: "41%",
  label: "Fewer pages that turn out to be false alarms",
  context: "Median across 380 on-call teams, measured over six months",
};

const DEFAULT_QUOTES: BentoQuote[] = [
  {
    quote:
      "Status pages write themselves now. An incident opens, the page updates, and support stops relaying timestamps.",
    name: "Marcus Webb",
    initials: "MW",
    role: "Head of Reliability",
    company: "Bluebird Freight",
  },
  {
    quote:
      "The check debugger shows exactly what our users see from six regions. TLS issues stopped being guesswork.",
    name: "Anaïs Dubois",
    initials: "AD",
    role: "Engineering Lead",
    company: "Gable",
  },
  {
    quote:
      "We deleted three cron jobs and a spreadsheet. Escalation policies finally live in one reviewed place.",
    name: "Sam Whitfield",
    initials: "SW",
    role: "Platform Architect",
    company: "Holloway Systems",
  },
];

function Avatar({ initials }: { initials: string }) {
  return (
    <span
      aria-hidden="true"
      className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full border border-[var(--ds-color-border)] bg-[var(--ds-color-background)] text-xs font-semibold leading-none text-[var(--ds-color-muted-foreground)]"
    >
      {initials}
    </span>
  );
}

function Attribution({ quote }: { quote: BentoQuote }) {
  return (
    <figcaption className="mt-6 flex items-center gap-3">
      <Avatar initials={quote.initials} />
      <div>
        <p className="text-sm font-semibold leading-5">{quote.name}</p>
        <p className="text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
          {quote.role}, {quote.company}
        </p>
      </div>
    </figcaption>
  );
}

export function TestimonialsSection({
  eyebrow = "Customer stories",
  heading = "On-call teams trust Pingline with the 3 a.m. page.",
  lede = "Uptime monitoring, incident routing, and status pages for teams that measure calm in pages not sent.",
  heroQuote = DEFAULT_HERO_QUOTE,
  stat = DEFAULT_STAT,
  quotes = DEFAULT_QUOTES,
}: TestimonialsSectionProps) {
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
            {heading}
          </h2>
          <p className="mt-4 text-[clamp(1rem,0.95rem+0.25vw,1.125rem)] leading-[1.5] text-[var(--ds-color-muted-foreground)]">
            {lede}
          </p>
        </div>

        <div className="mt-12 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:mt-16 lg:grid-cols-12 lg:gap-6">
          <figure className={CELL_CLASSES + " sm:col-span-2 lg:col-span-7"}>
            <blockquote>
              <p className="text-lg font-medium leading-7 tracking-[-0.01em] text-[var(--ds-color-foreground)]">
                {heroQuote.quote}
              </p>
            </blockquote>
            <Attribution quote={heroQuote} />
          </figure>

          <div className={CELL_CLASSES + " sm:col-span-2 lg:col-span-5"}>
            <p className="text-[clamp(1.75rem,1.5rem+1.2vw,2.25rem)] font-semibold leading-[1.2] tracking-[-0.02em] tabular-nums text-[var(--ds-color-accent)]">
              {stat.value}
            </p>
            <p className="mt-2 text-sm leading-5 text-[var(--ds-color-foreground)]">
              {stat.label}
            </p>
            <p className="mt-6 font-[var(--ds-font-mono)] text-xs uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
              {stat.context}
            </p>
          </div>

          {quotes.map((quote) => (
            <figure key={quote.name} className={CELL_CLASSES + " lg:col-span-4"}>
              <blockquote>
                <p className="text-sm leading-5 text-[var(--ds-color-foreground)]">
                  {quote.quote}
                </p>
              </blockquote>
              <Attribution quote={quote} />
            </figure>
          ))}
        </div>
      </div>
    </section>
  );
}
