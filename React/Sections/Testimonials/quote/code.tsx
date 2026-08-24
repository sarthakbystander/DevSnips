import { useId } from "react";

/**
 * DevSnips React Testimonials — Quote composition (Minimal direction).
 *
 * The maximum-restraint composition: one voice, one oversized quote,
 * nothing else. A narrow container (§10.1) with a centered header block,
 * the quote set at a fluid display-adjacent size, and a centered
 * attribution. Typography does all of the work — no cards, no borders,
 * no artifacts (§4.2).
 *
 * One accent: the writeup link in the attribution. The oversized
 * quotation mark is editorial punctuation, rendered in the border color
 * and `aria-hidden` — the `<blockquote>` carries the semantics.
 */

export interface QuoteTestimonial {
  quote: string;
  name: string;
  initials: string;
  role: string;
  company: string;
}

export interface TestimonialLink {
  label: string;
  href: string;
}

export interface TestimonialsSectionProps {
  eyebrow?: string;
  heading?: string;
  testimonial?: QuoteTestimonial;
  link?: TestimonialLink;
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const LINK_CLASSES =
  "text-sm font-semibold leading-5 text-[var(--ds-color-link)] underline underline-offset-4 transition-colors duration-150 ease-out hover:text-[var(--ds-color-link-hover)] motion-reduce:transition-none " +
  FOCUS_RING;

const DEFAULT_TESTIMONIAL: QuoteTestimonial = {
  quote:
    "We run four hundred services on Longshore and think about it maybe once a month. It is the most boring piece of infrastructure we own — and I mean that as the highest compliment.",
  name: "James O'Connell",
  initials: "JO",
  role: "Principal Engineer",
  company: "North Pier",
};

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
  eyebrow = "In their words",
  heading = "Infrastructure you forget about.",
  testimonial = DEFAULT_TESTIMONIAL,
  link = { label: "Read the engineering writeup", href: "#customers/north-pier" },
}: TestimonialsSectionProps) {
  const headingId = useId();
  return (
    <section
      aria-labelledby={headingId}
      className="bg-[var(--ds-color-background)] font-[var(--ds-font-sans)] text-[var(--ds-color-foreground)]"
    >
      <div className="mx-auto max-w-[768px] px-4 py-[clamp(4rem,3rem+4vw,6rem)] sm:px-6">
        <div className="text-center">
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

        <figure className="mt-12 text-center lg:mt-16">
          <span
            aria-hidden="true"
            className="block text-[clamp(3rem,2.4rem+2.8vw,4.5rem)] font-semibold leading-[0.8] text-[var(--ds-color-border-strong)]"
          >
            &ldquo;
          </span>
          <blockquote className="mt-6">
            <p className="text-[clamp(1.375rem,1.15rem+1.1vw,1.875rem)] font-medium leading-[1.35] tracking-[-0.01em] text-[var(--ds-color-foreground)]">
              {testimonial.quote}
            </p>
          </blockquote>
          <figcaption className="mt-8 flex flex-col items-center gap-3">
            <Avatar initials={testimonial.initials} />
            <div>
              <p className="text-base font-semibold leading-6">
                {testimonial.name}
              </p>
              <p className="text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
                {testimonial.role}, {testimonial.company}
              </p>
            </div>
            <a href={link.href} className={LINK_CLASSES}>
              {link.label}
            </a>
          </figcaption>
        </figure>
      </div>
    </section>
  );
}
