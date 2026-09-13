import { useId } from "react";

/**
 * DevSnips React Testimonials — Minimal direction (even-grid composition).
 *
 * The reference composition for the Testimonials family: a left-aligned
 * header block above an even grid of six peer testimonials (3 columns at
 * lg, 2 at sm, 1 below — §12.2). Every voice carries the same weight;
 * separation comes from whitespace alone, never cards (§4.2).
 *
 * Each testimonial is a real `<figure>`: a `<blockquote>` quote plus a
 * `<figcaption>` attribution (name, role, company — §11.3). Avatars are
 * initials in a bordered circle — no external imagery — and are
 * `aria-hidden` because the adjacent name already carries the identity.
 * One accent: the single stories link below the grid.
 */

export interface Testimonial {
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
  lede?: string;
  testimonials?: Testimonial[];
  link?: TestimonialLink;
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const LINK_CLASSES =
  "text-sm font-semibold leading-5 text-[var(--ds-color-link)] underline underline-offset-4 transition-colors duration-150 ease-out hover:text-[var(--ds-color-link-hover)] motion-reduce:transition-none " +
  FOCUS_RING;

const DEFAULT_TESTIMONIALS: Testimonial[] = [
  {
    quote:
      "We replaced four internal tools with Formwork in a quarter. The admin panel our ops team had been requesting for a year took an afternoon, not a sprint.",
    name: "Maya Okafor",
    initials: "MO",
    role: "Director of Engineering",
    company: "Alderbrook",
  },
  {
    quote:
      "The audit log sold our security team before I finished the demo. Every action is recorded with an actor, a timestamp, and a reason.",
    name: "Daniel Reyes",
    initials: "DR",
    role: "Staff Platform Engineer",
    company: "Kestrel Robotics",
  },
  {
    quote:
      "I was skeptical of another internal tool builder. Then our support team shipped their own refund workflow without filing a single engineering ticket.",
    name: "Priya Raman",
    initials: "PR",
    role: "VP of Operations",
    company: "Tideline",
  },
  {
    quote:
      "Formwork's permission model maps to how our org actually works. Regional leads see their region, finance sees everything, and nobody files access requests anymore.",
    name: "Tom Aldridge",
    initials: "TA",
    role: "Head of IT",
    company: "Marsh & Field",
  },
  {
    quote:
      "We went from a backlog of fourteen internal-tool requests to zero in two months. Teams build the tools they need themselves now.",
    name: "Ingrid Sørensen",
    initials: "IS",
    role: "CTO",
    company: "Fernhill Data",
  },
  {
    quote:
      "It is the first internal platform our engineers don't route around. The components are good enough that building in-house feels wasteful.",
    name: "Kwame Mensah",
    initials: "KM",
    role: "Lead Frontend Engineer",
    company: "Osprey Health",
  },
];

/**
 * Initials avatar: a bordered circle rendered from the attribution data.
 * Decorative — the adjacent name carries the identity — so `aria-hidden`.
 */
function Avatar({ initials }: { initials: string }) {
  return (
    <span
      aria-hidden="true"
      className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] text-xs font-semibold leading-none text-[var(--ds-color-muted-foreground)]"
    >
      {initials}
    </span>
  );
}

export function TestimonialsSection({
  eyebrow = "Customer stories",
  heading = "Teams of every size ship on Formwork.",
  lede = "From ten-person startups to public companies, teams use Formwork to build the internal tools their roadmaps never had room for.",
  testimonials = DEFAULT_TESTIMONIALS,
  link = { label: "Browse all customer stories", href: "#customers" },
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

        <ul className="mt-12 grid grid-cols-1 gap-x-8 gap-y-10 sm:grid-cols-2 lg:mt-16 lg:grid-cols-3">
          {testimonials.map((testimonial) => (
            <li key={testimonial.name}>
              <figure>
                <blockquote>
                  <p className="text-base leading-6 text-[var(--ds-color-foreground)]">
                    {testimonial.quote}
                  </p>
                </blockquote>
                <figcaption className="mt-4 flex items-center gap-3">
                  <Avatar initials={testimonial.initials} />
                  <div>
                    <p className="text-sm font-semibold leading-5">
                      {testimonial.name}
                    </p>
                    <p className="text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
                      {testimonial.role}, {testimonial.company}
                    </p>
                  </div>
                </figcaption>
              </figure>
            </li>
          ))}
        </ul>

        <div className="mt-12 lg:mt-16">
          <a href={link.href} className={LINK_CLASSES}>
            {link.label}
          </a>
        </div>
      </div>
    </section>
  );
}
