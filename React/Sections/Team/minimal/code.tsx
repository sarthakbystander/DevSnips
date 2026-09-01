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
    initials: "AM",
    location: "New York",
    social: [{ label: "Alex Morgan profile", href: "#alex-morgan" }],
  },
  {
    name: "Maya Chen",
    role: "Engineering Lead",
    initials: "MC",
    location: "Toronto",
    social: [{ label: "Maya Chen profile", href: "#maya-chen" }],
  },
  {
    name: "Jon Bell",
    role: "Design Director",
    initials: "JB",
    location: "London",
    social: [{ label: "Jon Bell profile", href: "#jon-bell" }],
  },
  {
    name: "Priya Shah",
    role: "Developer Advocate",
    initials: "PS",
    location: "Bengaluru",
    social: [{ label: "Priya Shah profile", href: "#priya-shah" }],
  },
];

export function TeamSection({
  eyebrow = "The team",
  title = "Small team. Serious craft.",
  description = "A focused group building tools that make software work feel clearer, faster, and more humane.",
  members = DEFAULT_MEMBERS,
}: TeamSectionProps) {
  const headingId = React.useId();

  return (
    <section
      aria-labelledby={headingId}
      className="bg-[var(--ds-color-background)] font-[var(--ds-font-sans)] text-[var(--ds-color-foreground)]"
    >
      <div className="mx-auto max-w-[1200px] px-4 py-[clamp(4.5rem,3rem+5vw,7rem)] sm:px-6 lg:px-8">
        <header className="max-w-2xl">
          <p className="text-[11px] font-semibold uppercase leading-[1.3] tracking-[0.06em] text-[var(--ds-color-muted-foreground)]">
            {eyebrow}
          </p>
          <h2
            id={headingId}
            className="mt-3 text-[clamp(2rem,1.45rem+2.2vw,3rem)] font-semibold leading-[1.12] tracking-[-0.02em]"
          >
            {title}
          </h2>
          <p className="mt-4 max-w-[62ch] text-[clamp(1rem,0.96rem+0.2vw,1.125rem)] leading-[1.55] text-[var(--ds-color-muted-foreground)]">
            {description}
          </p>
        </header>

        <ul className="mt-14 grid grid-cols-1 border-t border-[var(--ds-color-border)] sm:grid-cols-2 lg:grid-cols-4">
          {members.map((member) => (
            <li
              key={member.name}
              className="group flex min-h-[210px] flex-col border-b border-[var(--ds-color-border)] px-0 py-7 sm:px-5 sm:py-8 lg:border-r lg:px-6 lg:last:border-r-0"
            >
              <div className="flex items-start justify-between gap-4">
                <span
                  aria-hidden="true"
                  className="inline-flex size-11 shrink-0 items-center justify-center border border-[var(--ds-color-border-strong)] bg-[var(--ds-color-surface)] font-[var(--ds-font-mono)] text-xs font-medium tracking-[0.04em] text-[var(--ds-color-foreground)]"
                >
                  {member.initials ?? member.name.slice(0, 2).toUpperCase()}
                </span>
                {member.social?.[0] ? (
                  <a
                    href={member.social[0].href}
                    aria-label={member.social[0].label}
                    className={
                      "shrink-0 text-xs font-medium text-[var(--ds-color-muted-foreground)] underline decoration-[var(--ds-color-border-strong)] underline-offset-4 transition-colors duration-150 ease-out hover:text-[var(--ds-color-foreground)] motion-reduce:transition-none " +
                      FOCUS_RING
                    }
                  >
                    Profile
                  </a>
                ) : null}
              </div>
              <div className="mt-auto pt-8">
                <h3 className="text-base font-semibold leading-[1.4] tracking-[-0.01em]">
                  {member.name}
                </h3>
                <p className="mt-1 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
                  {member.role}
                </p>
                {member.location ? (
                  <p className="mt-3 font-[var(--ds-font-mono)] text-[11px] uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
                    {member.location}
                  </p>
                ) : null}
              </div>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
