import * as React from "react";

export type TeamMember = {
  name: string;
  role: string;
  bio?: string;
  initials?: string;
  location?: string;
  social?: { label: string; href: string }[];
};

export interface TeamSectionProps {
  eyebrow?: string;
  title?: string;
  description?: string;
  members?: TeamMember[];
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const DEFAULT_MEMBERS: TeamMember[] = [
  {
    name: "Alex Morgan",
    role: "Founder & Product",
    bio: "Direction, product, and the final call on what ships.",
    initials: "AM",
    location: "New York",
  },
  {
    name: "Maya Chen",
    role: "Engineering Lead",
    bio: "Architecture, performance, and systems thinking.",
    initials: "MC",
    location: "Toronto",
  },
  {
    name: "Jon Bell",
    role: "Design Director",
    bio: "Visual systems, interaction, and product language.",
    initials: "JB",
    location: "London",
  },
  {
    name: "Priya Shah",
    role: "Developer Advocate",
    bio: "Docs, examples, and community feedback loops.",
    initials: "PS",
    location: "Bengaluru",
  },
];

const PANEL =
  "border-2 border-[var(--ds-color-border-strong)] bg-[var(--ds-color-surface)] shadow-[4px_4px_0_0_var(--ds-color-border-strong)]";

export function TeamSection({
  eyebrow = "People / 04",
  title = "THE PEOPLE MAKING THE THING.",
  description = "A compact group with strong opinions about useful software, readable interfaces, and shipping work that can survive contact with reality.",
  members = DEFAULT_MEMBERS,
}: TeamSectionProps) {
  const headingId = React.useId();
  const featured = members[0];

  return (
    <section
      aria-labelledby={headingId}
      className="bg-[var(--ds-color-background)] font-[var(--ds-font-sans)] text-[var(--ds-color-foreground)]"
    >
      <div className="mx-auto max-w-[1240px] px-4 py-[clamp(4rem,2.75rem+4vw,6rem)] sm:px-6 lg:px-8">
        <header className="border-b-2 border-[var(--ds-color-border-strong)] pb-8">
          <p className="font-[var(--ds-font-mono)] text-[11px] font-semibold uppercase leading-[1.3] tracking-[0.06em] text-[var(--ds-color-muted-foreground)]">
            {eyebrow}
          </p>
          <h2
            id={headingId}
            className="mt-4 max-w-[12ch] text-[clamp(2.5rem,1.8rem+3vw,4.5rem)] font-bold leading-[0.98] tracking-[-0.03em]"
          >
            {title}
          </h2>
          <p className="mt-5 max-w-[62ch] text-base leading-[1.5] text-[var(--ds-color-muted-foreground)]">
            {description}
          </p>
        </header>

        <div className="mt-8 grid gap-8 lg:grid-cols-[1.35fr_1fr] lg:gap-12">
          {featured ? (
            <article className={"min-h-[420px] p-6 sm:p-8 lg:p-10 " + PANEL}>
              <div className="flex items-start justify-between gap-8">
                <div>
                  <p className="font-[var(--ds-font-mono)] text-[10px] font-semibold uppercase leading-[1.4] tracking-[0.07em] text-[var(--ds-color-muted-foreground)]">
                    Featured operator
                  </p>
                  <h3 className="mt-5 text-[clamp(2rem,1.55rem+2vw,3rem)] font-bold leading-[1.05] tracking-[-0.025em]">
                    {featured.name}
                  </h3>
                  <p className="mt-2 font-[var(--ds-font-mono)] text-xs font-semibold uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-foreground)]">
                    {featured.role}
                  </p>
                </div>
                <span
                  aria-hidden="true"
                  className="inline-flex size-20 shrink-0 items-center justify-center border-2 border-[var(--ds-color-border-strong)] bg-[var(--ds-color-accent)] font-[var(--ds-font-mono)] text-lg font-bold text-[var(--ds-color-accent-foreground)] shadow-[4px_4px_0_0_var(--ds-color-border-strong)]"
                >
                  {featured.initials ?? featured.name.slice(0, 2).toUpperCase()}
                </span>
              </div>
              <div className="mt-16 grid gap-6 border-t-2 border-[var(--ds-color-border-strong)] pt-6 sm:grid-cols-[1fr_auto] sm:items-end">
                <p className="max-w-[46ch] text-base leading-[1.55]">{featured.bio ?? "Making the hard calls and keeping the product useful."}</p>
                <div className="font-[var(--ds-font-mono)] text-[10px] font-semibold uppercase leading-[1.5] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
                  <p>{featured.location ?? "Remote"}</p>
                  <p className="mt-1 text-[var(--ds-color-foreground)]">Product / Direction</p>
                </div>
              </div>
            </article>
          ) : null}

          <div className="grid grid-cols-1 border-2 border-[var(--ds-color-border-strong)] sm:grid-cols-2 lg:grid-cols-1">
            {members.slice(1).map((member, index) => (
              <article
                key={member.name}
                className="min-h-[150px] border-b-2 border-[var(--ds-color-border-strong)] p-5 last:border-b-0 sm:border-r-2 sm:last:border-r-0 lg:border-b-2 lg:border-r-0"
              >
                <div className="flex items-start justify-between gap-4">
                  <p className="font-[var(--ds-font-mono)] text-[10px] font-semibold uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
                    {String(index + 2).padStart(2, "0")}
                  </p>
                  <span className="font-[var(--ds-font-mono)] text-[10px] font-semibold uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
                    {member.location ?? "Remote"}
                  </span>
                </div>
                <h3 className="mt-7 text-lg font-bold leading-[1.25] tracking-[-0.01em]">{member.name}</h3>
                <p className="mt-1 font-[var(--ds-font-mono)] text-[11px] font-semibold uppercase leading-[1.4] tracking-[0.05em]">{member.role}</p>
              </article>
            ))}
          </div>
        </div>

        <div className="mt-10 flex flex-col gap-5 border-t-2 border-[var(--ds-color-border-strong)] pt-7 sm:flex-row sm:items-end sm:justify-between">
          <p className="max-w-[58ch] font-[var(--ds-font-mono)] text-[11px] uppercase leading-[1.55] tracking-[0.04em] text-[var(--ds-color-muted-foreground)]">
            WORK WITH PEOPLE WHO LIKE SHIPPING.
          </p>
          <a
            href="#work-with-us"
            className={
              "inline-flex min-h-11 items-center justify-center border-2 border-[var(--ds-color-border-strong)] bg-[var(--ds-color-accent)] px-5 font-[var(--ds-font-mono)] text-xs font-bold uppercase leading-[1.3] tracking-[0.05em] text-[var(--ds-color-accent-foreground)] shadow-[4px_4px_0_0_var(--ds-color-border-strong)] transition-transform duration-100 ease-out active:translate-x-1 active:translate-y-1 active:shadow-none motion-reduce:transition-none " +
              FOCUS_RING
            }
          >
            Work with us
          </a>
        </div>
      </div>
    </section>
  );
}
