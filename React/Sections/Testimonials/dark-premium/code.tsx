import { useId } from "react";

/**
 * DevSnips React Testimonials — Dark Premium direction (customer-story composition).
 *
 * The case-study composition: an asymmetric 4/8 split of 12 (§10.2) with a
 * customer evidence card on the left (wordmark, company facts as a real
 * `<dl>`, three outcome metrics) and the narrative on the right — two
 * paragraphs of first-person account with one emphasized pull-quote line
 * set off by a hairline rule. Columns stack narrative-first below lg
 * (§12.2).
 *
 * The section pins the dark theme mapping with `data-theme="dark"` on its
 * own root, consuming the same semantic tokens in both page themes — a
 * theme mapping, not a hard-coded dark page (§4.3). Surfaces lift exactly
 * one step above the canvas via a 1px border; no shadows, no glow, no
 * mesh. One accent: the case-study link.
 */

export interface StoryFact {
  label: string;
  value: string;
}

export interface StoryMetric {
  value: string;
  label: string;
}

export interface TestimonialLink {
  label: string;
  href: string;
}

export interface TestimonialsSectionProps {
  eyebrow?: string;
  heading?: string;
  company?: string;
  companyDescription?: string;
  facts?: StoryFact[];
  metrics?: StoryMetric[];
  paragraphs?: string[];
  pullQuote?: string;
  name?: string;
  initials?: string;
  role?: string;
  link?: TestimonialLink;
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const LINK_CLASSES =
  "text-sm font-semibold leading-5 text-[var(--ds-color-link)] underline underline-offset-4 transition-colors duration-150 ease-out hover:text-[var(--ds-color-link-hover)] motion-reduce:transition-none " +
  FOCUS_RING;

const DEFAULT_FACTS: StoryFact[] = [
  { label: "Industry", value: "Freight logistics" },
  { label: "Engineers", value: "210" },
  { label: "Infrastructure", value: "Multi-region AWS" },
  { label: "Customer since", value: "2023" },
];

const DEFAULT_METRICS: StoryMetric[] = [
  { value: "31%", label: "Idle cloud spend eliminated in one quarter" },
  { value: "$214k", label: "Annualized savings at current usage" },
  { value: "2 wks", label: "From connect to first accepted recommendation" },
];

const DEFAULT_PARAGRAPHS: string[] = [
  "Our bill had grown with the business for three years, and every review ended the same way: a spreadsheet, a shrug, and a promise to look again next quarter. Ballast was the first tool that didn't just show us the waste — it showed us which team owned it and what changing it would break.",
  "The difference is that recommendations arrive as pull requests. An engineer reviews the diff, sees the blast radius, and merges. Finance gets the savings report without a meeting, and we got a quarter of our infrastructure budget back without a single late night.",
];

export function TestimonialsSection({
  eyebrow = "Customer story",
  heading = "How Vessel cut idle cloud spend by 31% in one quarter.",
  company = "Vessel",
  companyDescription = "Freight logistics platform moving 1.2M shipments a month",
  facts = DEFAULT_FACTS,
  metrics = DEFAULT_METRICS,
  paragraphs = DEFAULT_PARAGRAPHS,
  pullQuote = "Recommendations arrive as pull requests. An engineer reviews the diff and merges — nobody schedules a cost review meeting anymore.",
  name = "Laura Chen",
  initials = "LC",
  role = "VP of Platform Engineering",
  link = { label: "Read the full case study", href: "#customers/vessel" },
}: TestimonialsSectionProps) {
  const headingId = useId();
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
            {heading}
          </h2>
        </div>

        <div className="mt-12 grid grid-cols-1 gap-12 lg:mt-16 lg:grid-cols-12 lg:gap-8">
          <div className="lg:col-span-8 lg:order-2">
            <figure>
              <blockquote className="space-y-6">
                {paragraphs.map((paragraph) => (
                  <p
                    key={paragraph.slice(0, 32)}
                    className="text-base leading-7 text-[var(--ds-color-muted-foreground)]"
                  >
                    {paragraph}
                  </p>
                ))}
                <p className="border-l-2 border-[var(--ds-color-border-strong)] pl-6 text-xl font-semibold leading-[1.4] tracking-[-0.01em] text-[var(--ds-color-foreground)]">
                  {pullQuote}
                </p>
              </blockquote>
              <figcaption className="mt-8 flex items-center gap-4">
                <span
                  aria-hidden="true"
                  className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] text-sm font-semibold leading-none text-[var(--ds-color-muted-foreground)]"
                >
                  {initials}
                </span>
                <div>
                  <p className="text-base font-semibold leading-6">{name}</p>
                  <p className="text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
                    {role}, {company}
                  </p>
                </div>
              </figcaption>
            </figure>
            <p className="mt-8">
              <a href={link.href} className={LINK_CLASSES}>
                {link.label}
              </a>
            </p>
          </div>

          <div className="lg:col-span-4 lg:order-1">
            <div className="rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-6 lg:p-8">
              <p className="text-xl font-semibold leading-7 tracking-[-0.01em]">
                {company}
              </p>
              <p className="mt-1 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
                {companyDescription}
              </p>

              <dl className="mt-6 divide-y divide-[var(--ds-color-border-subtle)] border-y border-[var(--ds-color-border-subtle)]">
                {facts.map((fact) => (
                  <div
                    key={fact.label}
                    className="flex items-baseline justify-between gap-4 py-3"
                  >
                    <dt className="text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
                      {fact.label}
                    </dt>
                    <dd className="text-right text-sm font-medium leading-5">
                      {fact.value}
                    </dd>
                  </div>
                ))}
              </dl>

              <p className="mt-6 font-[var(--ds-font-mono)] text-xs font-medium uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
                Outcomes
              </p>
              <ul className="mt-4 space-y-5">
                {metrics.map((metric) => (
                  <li key={metric.label}>
                    <p className="text-2xl font-semibold leading-[1.2] tracking-[-0.02em] tabular-nums">
                      {metric.value}
                    </p>
                    <p className="mt-1 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
                      {metric.label}
                    </p>
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
