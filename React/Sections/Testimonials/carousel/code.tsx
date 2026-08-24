import { useId, useState } from "react";
import type { KeyboardEvent } from "react";

/**
 * DevSnips React Testimonials — Carousel composition (Minimal direction).
 *
 * One testimonial at a time, chosen deliberately: real carousel semantics
 * (`aria-roledescription="carousel"`, slides as `role="group"` with
 * `aria-roledescription="slide"` and positional labels), previous/next
 * buttons, and a slide picker of real `<button>` dots with `aria-current`.
 * ArrowLeft/ArrowRight/Home/End move between slides when focus is inside
 * the carousel; there is NO auto-rotation — motion this prominent must be
 * user-initiated (§14).
 *
 * Slides stay mounted and toggle with `hidden`, so nothing inside loses
 * state; a visually-hidden `aria-live="polite"` region announces the
 * current slide's attribution on change. The current dot is filled AND
 * carries `aria-current` — state is never color alone (§13). Slide height
 * follows content; no measurement, no layout hacks.
 */

export interface CarouselTestimonial {
  quote: string;
  name: string;
  initials: string;
  role: string;
  company: string;
}

export interface TestimonialsSectionProps {
  eyebrow?: string;
  heading?: string;
  lede?: string;
  testimonials?: CarouselTestimonial[];
  defaultIndex?: number;
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const CONTROL_CLASSES =
  "inline-flex h-11 w-11 shrink-0 items-center justify-center rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border-strong)] bg-[var(--ds-color-surface)] text-[var(--ds-color-foreground)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] motion-reduce:transition-none " +
  FOCUS_RING;

const DOT_CLASSES =
  "inline-flex h-11 w-11 items-center justify-center motion-reduce:transition-none " +
  FOCUS_RING;

const DEFAULT_TESTIMONIALS: CarouselTestimonial[] = [
  {
    quote:
      "We found a memory leak that had survived three quarters of dashboards because Lockstep's trace view made the allocation pattern obvious in one afternoon.",
    name: "Yuki Tanaka",
    initials: "YT",
    role: "Staff SRE",
    company: "Cairn Systems",
  },
  {
    quote:
      "Alert noise dropped by two thirds in the first month. The correlation engine groups what used to be forty pages into one incident with a story.",
    name: "Marcus Webb",
    initials: "MW",
    role: "Head of Reliability",
    company: "Bluebird Freight",
  },
  {
    quote:
      "I can answer 'what changed?' in one query. During an incident, that question is half the battle.",
    name: "Anaïs Dubois",
    initials: "AD",
    role: "Engineering Lead",
    company: "Gable",
  },
  {
    quote:
      "Our engineers actually look at traces now. The barrier was never discipline — it was that the old tool made answers take twenty minutes.",
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
      className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] text-sm font-semibold leading-none text-[var(--ds-color-muted-foreground)]"
    >
      {initials}
    </span>
  );
}

function ChevronLeft() {
  return (
    <svg
      aria-hidden="true"
      viewBox="0 0 16 16"
      className="h-4 w-4"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="m10 3-5 5 5 5" />
    </svg>
  );
}

function ChevronRight() {
  return (
    <svg
      aria-hidden="true"
      viewBox="0 0 16 16"
      className="h-4 w-4"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="m6 3 5 5-5 5" />
    </svg>
  );
}

export function TestimonialsSection({
  eyebrow = "Customer stories",
  heading = "Why on-call teams stay on Lockstep.",
  lede = "Four teams on what changed when observability stopped being a chore.",
  testimonials = DEFAULT_TESTIMONIALS,
  defaultIndex = 0,
}: TestimonialsSectionProps) {
  const headingId = useId();
  const [active, setActive] = useState(
    Math.min(Math.max(defaultIndex, 0), testimonials.length - 1),
  );

  const count = testimonials.length;
  const current = testimonials[active];

  function goTo(index: number) {
    setActive(((index % count) + count) % count);
  }

  function onCarouselKeyDown(event: KeyboardEvent<HTMLDivElement>) {
    if (event.key === "ArrowLeft") {
      event.preventDefault();
      goTo(active - 1);
    } else if (event.key === "ArrowRight") {
      event.preventDefault();
      goTo(active + 1);
    } else if (event.key === "Home") {
      event.preventDefault();
      goTo(0);
    } else if (event.key === "End") {
      event.preventDefault();
      goTo(count - 1);
    }
  }

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

        <div
          aria-roledescription="carousel"
          aria-label="Customer testimonials"
          onKeyDown={onCarouselKeyDown}
          className="mt-12 lg:mt-16"
        >
          <div aria-live="polite" className="sr-only">
            {current
              ? `Testimonial ${active + 1} of ${count}: ${current.name}, ${current.company}`
              : ""}
          </div>

          {testimonials.map((testimonial, index) => {
            const selected = index === active;
            return (
              <div
                key={testimonial.name}
                role="group"
                aria-roledescription="slide"
                aria-label={`${index + 1} of ${count}`}
                hidden={!selected}
                className={selected ? "block" : "hidden"}
              >
                <figure className="mx-auto max-w-3xl text-center">
                  <blockquote>
                    <p className="text-[clamp(1.25rem,1.1rem+0.75vw,1.625rem)] font-medium leading-[1.4] tracking-[-0.01em] text-[var(--ds-color-foreground)]">
                      {testimonial.quote}
                    </p>
                  </blockquote>
                  <figcaption className="mt-8 flex items-center justify-center gap-4">
                    <Avatar initials={testimonial.initials} />
                    <div className="text-left">
                      <p className="text-base font-semibold leading-6">
                        {testimonial.name}
                      </p>
                      <p className="text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
                        {testimonial.role}, {testimonial.company}
                      </p>
                    </div>
                  </figcaption>
                </figure>
              </div>
            );
          })}

          <div className="mt-10 flex items-center justify-center gap-4">
            <button
              type="button"
              aria-label="Previous testimonial"
              onClick={() => goTo(active - 1)}
              className={CONTROL_CLASSES}
            >
              <ChevronLeft />
            </button>
            <div className="flex items-center" role="group" aria-label="Choose testimonial">
              {testimonials.map((testimonial, index) => {
                const selected = index === active;
                return (
                  <button
                    key={testimonial.name}
                    type="button"
                    aria-label={`Go to testimonial ${index + 1}: ${testimonial.company}`}
                    aria-current={selected ? "true" : undefined}
                    onClick={() => goTo(index)}
                    className={DOT_CLASSES}
                  >
                    <span
                      aria-hidden="true"
                      className={
                        "block h-2 w-2 rounded-full transition-colors duration-150 ease-out motion-reduce:transition-none " +
                        (selected
                          ? "bg-[var(--ds-color-foreground)]"
                          : "border border-[var(--ds-color-border-strong)] bg-transparent")
                      }
                    />
                  </button>
                );
              })}
            </div>
            <button
              type="button"
              aria-label="Next testimonial"
              onClick={() => goTo(active + 1)}
              className={CONTROL_CLASSES}
            >
              <ChevronRight />
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}
