import { useId } from "react";

/**
 * DevSnips React Testimonials — Featured composition (Minimal direction).
 *
 * One voice, amplified: a 7/5 split of 12 (§10.2) with the featured quote
 * on the left and a bordered evidence panel on the right — three outcome
 * metrics as a real `<dl>`, company context, and the story link. The
 * panel earns its border: it groups evidence, not decoration (§11).
 * Columns stack quote-first below lg (§12.2).
 *
 * The quote is set at a fluid display-adjacent size because it is the
 * content, not a caption. One accent: the "read the full story" link.
 * The avatar is initials — no external imagery — and `aria-hidden`.
 */

export interface FeaturedTestimonial {
  quote: string;
  name: string;
  initials: string;
  role: string;
  company: string;
}

export interface ResultMetric {
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
  lede?: string;
  testimonial?: FeaturedTestimonial;
  companyContext?: string;
  metrics?: ResultMetric[];
  link?: TestimonialLink;
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const LINK_CLASSES =
  "text-sm font-semibold leading-5 text-[var(--ds-color-link)] underline underline-offset-4 transition-colors duration-150 ease-out hover:text-[var(--ds-color-link-hover)] motion-reduce:transition-none " +
  FOCUS_RING;

const DEFAULT_TESTIMONIAL: FeaturedTestimonial = {
  quote:
    "Mergeline cut our median review turnaround from two days to four hours. But the number isn't the story — the story is that reviews stopped being the thing engineers scheduled their day around. Small changes ship small, and nobody batches a week's work into one terrifying pull request anymore.",
  name: "Elena Vasquez",
  initials: "EV",
  role: "VP of Engineering",
  company: "Brightmarch",
};

const DEFAULT_METRICS: ResultMetric[] = [
  {
    value: "4h",
    label: "Median review turnaround, down from 2 days",
  },
  {
    value: "63%",
    label: "Fewer review rounds per pull request",
  },
  {
    value: "97%",
    label: "Pull requests reviewed within one business day",
  },
];

function Avatar({ initials }: { initials: string }) {
  return (
    <span
      aria-hidden="true"
      className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] text-sm font-semibold leading-none text-[var(--ds-color-muted-foreground)]"
    >
      {initials}
    </span>
  );
}

export function TestimonialsSection({
  eyebrow = "Featured customer",
  heading = "Code review stopped being the bottleneck.",
  lede = "Brightmarch ships a payments product with 140 engineers. Here's what changed when review moved to Mergeline.",
  testimonial = DEFAULT_TESTIMONIAL,
  companyContext = "Brightmarch · 140 engineers · Customer since 2024",
  metrics = DEFAULT_METRICS,
  link = { label: "Read the full story", href: "#customers/brightmarch" },
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

        <div className="mt-12 grid grid-cols-1 gap-12 lg:mt-16 lg:grid-cols-12 lg:gap-8">
          <figure className="lg:col-span-7">
            <blockquote>
              <p className="text-[clamp(1.25rem,1.1rem+0.7vw,1.625rem)] font-medium leading-[1.4] tracking-[-0.01em] text-[var(--ds-color-foreground)]">
                {testimonial.quote}
              </p>
            </blockquote>
            <figcaption className="mt-8 flex items-center gap-4">
              <Avatar initials={testimonial.initials} />
              <div>
                <p className="text-base font-semibold leading-6">
                  {testimonial.name}
                </p>
                <p className="text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
                  {testimonial.role}, {testimonial.company}
                </p>
              </div>
            </figcaption>
          </figure>

          <div className="lg:col-span-5">
            <div className="rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-6 lg:p-8">
              <p className="font-[var(--ds-font-mono)] text-xs font-medium uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
                Results after two quarters
              </p>
              <dl className="mt-4 divide-y divide-[var(--ds-color-border-subtle)] border-y border-[var(--ds-color-border-subtle)]">
                {metrics.map((metric) => (
                  <div
                    key={metric.label}
                    className="flex items-baseline gap-4 py-4"
                  >
                    <dd className="w-16 shrink-0 text-2xl font-semibold leading-[1.2] tracking-[-0.02em] tabular-nums">
                      {metric.value}
                    </dd>
                    <dt className="text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
                      {metric.label}
                    </dt>
                  </div>
                ))}
              </dl>
              <p className="mt-4 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
                {companyContext}
              </p>
              <p className="mt-4">
                <a href={link.href} className={LINK_CLASSES}>
                  {link.label}
                </a>
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
