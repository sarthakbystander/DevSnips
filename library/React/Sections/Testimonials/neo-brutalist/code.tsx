import { useId } from "react";

/**
 * DevSnips React Testimonials — Neo-Brutalist direction.
 *
 * The expressive ceiling, kept disciplined (§4.5): three square
 * testimonial cards with uniform 2px borders, hard 4px offset shadows
 * (zero blur), and mono index numbers. One card is a flat accent fill —
 * the supporting-fill budget spent in a single block — everything else is
 * flat surface. The eyebrow is a bordered chip; the one action is a
 * press-down button that translates by its shadow offset on :active
 * (≤100ms). Nothing rounds, glows, or gradients.
 *
 * Collapse: 3 columns at lg, 1 below sm (2 at sm only if the row divides
 * evenly — here 3 cards go 3 → 1 to keep rows whole). The filled card
 * uses the warning token pair, which keeps AA contrast in both themes.
 */

export interface BrutalistTestimonial {
  quote: string;
  name: string;
  role: string;
  company: string;
  filled?: boolean;
}

export interface TestimonialAction {
  label: string;
  href: string;
}

export interface TestimonialsSectionProps {
  eyebrow?: string;
  heading?: string;
  lede?: string;
  testimonials?: BrutalistTestimonial[];
  action?: TestimonialAction;
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const ACTION_CLASSES =
  "inline-flex h-11 items-center justify-center rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] bg-[var(--ds-color-surface)] px-5 text-sm font-semibold leading-5 text-[var(--ds-color-foreground)] shadow-[4px_4px_0_0_var(--ds-color-border-strong)] transition-[transform,box-shadow] duration-100 ease-out active:translate-x-[4px] active:translate-y-[4px] active:shadow-none motion-reduce:transition-none " +
  FOCUS_RING;

const DEFAULT_TESTIMONIALS: BrutalistTestimonial[] = [
  {
    quote:
      "We broke production on purpose every week for a year. Real incidents dropped by four fifths. Breakglass made chaos boring — which is exactly the point.",
    name: "Nadia Hussain",
    role: "SRE Manager",
    company: "Kettle & Oak",
    filled: true,
  },
  {
    quote:
      "The game-day scheduler turned chaos engineering from a quarterly offsite into a Tuesday habit.",
    name: "Felix Andersson",
    role: "Platform Lead",
    company: "Baltic & Pine",
  },
  {
    quote:
      "Our incident reviews reference Breakglass experiment IDs now. It changed how the whole org talks about failure.",
    name: "Ruth Achebe",
    role: "Director of Infrastructure",
    company: "Saltbox Systems",
  },
];

export function TestimonialsSection({
  eyebrow = "War stories",
  heading = "Teams that break things on purpose.",
  lede = "Breakglass runs controlled failure experiments so real outages stop being surprises.",
  testimonials = DEFAULT_TESTIMONIALS,
  action = { label: "Read all case studies", href: "#customers" },
}: TestimonialsSectionProps) {
  const headingId = useId();
  return (
    <section
      aria-labelledby={headingId}
      className="bg-[var(--ds-color-background)] font-[var(--ds-font-sans)] text-[var(--ds-color-foreground)]"
    >
      <div className="mx-auto max-w-[1280px] px-4 py-[clamp(4rem,3rem+4vw,6rem)] sm:px-6 lg:px-8">
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

        <ul className="mt-12 grid grid-cols-1 gap-6 lg:mt-16 lg:grid-cols-3">
          {testimonials.map((testimonial, index) => (
            <li
              key={testimonial.name}
              className={
                "flex flex-col rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] p-6 shadow-[4px_4px_0_0_var(--ds-color-border-strong)] sm:p-8 " +
                (testimonial.filled
                  ? "bg-[var(--ds-color-warning)] text-[var(--ds-color-warning-foreground)]"
                  : "bg-[var(--ds-color-surface)]")
              }
            >
              <p
                className={
                  "font-[var(--ds-font-mono)] text-xs font-semibold uppercase leading-[1.4] tracking-[0.05em] " +
                  (testimonial.filled
                    ? ""
                    : "text-[var(--ds-color-muted-foreground)]")
                }
              >
                {String(index + 1).padStart(2, "0")}
              </p>
              <figure className="mt-4 flex flex-1 flex-col">
                <blockquote className="flex-1">
                  <p className="text-base font-medium leading-6">
                    {testimonial.quote}
                  </p>
                </blockquote>
                <figcaption className="mt-6 border-t-2 border-[var(--ds-color-border-strong)] pt-4">
                  <p className="text-sm font-bold leading-5">
                    {testimonial.name}
                  </p>
                  <p
                    className={
                      "text-sm leading-5 " +
                      (testimonial.filled
                        ? ""
                        : "text-[var(--ds-color-muted-foreground)]")
                    }
                  >
                    {testimonial.role}, {testimonial.company}
                  </p>
                </figcaption>
              </figure>
            </li>
          ))}
        </ul>

        <div className="mt-12 lg:mt-16">
          <a href={action.href} className={ACTION_CLASSES}>
            {action.label}
          </a>
        </div>
      </div>
    </section>
  );
}
