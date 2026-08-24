import { useId } from "react";

/**
 * DevSnips React Testimonials — Rows composition (Minimal direction).
 *
 * The high-density composition: six short testimonials as hairline-divided
 * rows in a real `<ul>`, each row a 3/6/3 split of 12 — company wordmark,
 * one-sentence quote, attribution (§10.2). Rows stack wordmark-first
 * below sm (§12.2). Nothing but 1px dividers and type; the rhythm is the
 * design (§4.2).
 *
 * Short quotes are the point: this composition is for scanning many
 * voices quickly, not for deep narrative. Wordmarks are plain text —
 * styled uniformly, invented names, never fake versions of real brands
 * (§15). One accent: the stories link below the list.
 */

export interface RowTestimonial {
  company: string;
  quote: string;
  name: string;
  role: string;
}

export interface TestimonialLink {
  label: string;
  href: string;
}

export interface TestimonialsSectionProps {
  eyebrow?: string;
  heading?: string;
  lede?: string;
  testimonials?: RowTestimonial[];
  link?: TestimonialLink;
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const LINK_CLASSES =
  "text-sm font-semibold leading-5 text-[var(--ds-color-link)] underline underline-offset-4 transition-colors duration-150 ease-out hover:text-[var(--ds-color-link-hover)] motion-reduce:transition-none " +
  FOCUS_RING;

const DEFAULT_TESTIMONIALS: RowTestimonial[] = [
  {
    company: "Stonecutter",
    quote:
      "Rollbacks went from a runbook page to a button. Our on-call stress dropped measurably.",
    name: "Rachel Kim",
    role: "SRE Lead",
  },
  {
    company: "Willowmark",
    quote:
      "The deploy graph is the first thing I open every morning.",
    name: "Devang Patel",
    role: "Platform Engineer",
  },
  {
    company: "Redfern",
    quote:
      "We audit who deployed what in seconds. Compliance reviews used to take a week.",
    name: "Omar Farouk",
    role: "Security Engineer",
  },
  {
    company: "Ashdown",
    quote:
      "Preview environments for every pull request ended our staging-server queue entirely.",
    name: "Hanna Lindqvist",
    role: "Engineering Manager",
  },
  {
    company: "Copperwood",
    quote:
      "Migrated sixty services in a month. The importer read our old pipeline YAML without complaint.",
    name: "Chris Doan",
    role: "Staff Engineer",
  },
  {
    company: "Vessel",
    quote:
      "Deploy infrastructure that respects your existing tooling instead of replacing it.",
    name: "Grace Njoroge",
    role: "CTO",
  },
];

export function TestimonialsSection({
  eyebrow = "What teams say",
  heading = "Six teams, one deploy platform.",
  lede = "Patchbay orchestrates deploys for teams that would rather ship than babysit pipelines.",
  testimonials = DEFAULT_TESTIMONIALS,
  link = { label: "Read all customer stories", href: "#customers" },
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

        <ul className="mt-12 divide-y divide-[var(--ds-color-border)] border-y border-[var(--ds-color-border)] lg:mt-16">
          {testimonials.map((testimonial) => (
            <li
              key={testimonial.company}
              className="grid grid-cols-1 gap-2 py-6 sm:grid-cols-12 sm:items-baseline sm:gap-8"
            >
              <p className="text-sm font-semibold leading-5 sm:col-span-3">
                {testimonial.company}
              </p>
              <blockquote className="sm:col-span-6">
                <p className="text-sm leading-5 text-[var(--ds-color-foreground)]">
                  {testimonial.quote}
                </p>
              </blockquote>
              <p className="text-sm leading-5 text-[var(--ds-color-muted-foreground)] sm:col-span-3 sm:text-right">
                {testimonial.name}, {testimonial.role}
              </p>
            </li>
          ))}
        </ul>

        <div className="mt-12">
          <a href={link.href} className={LINK_CLASSES}>
            {link.label}
          </a>
        </div>
      </div>
    </section>
  );
}
