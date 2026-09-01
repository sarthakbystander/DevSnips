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
  { name: "Alex Morgan", role: "Founder & Product", bio: "Sets direction, shapes product, and keeps the work close to what developers actually need.", initials: "AM", location: "New York", social: [{ label: "Alex Morgan profile", href: "#alex-morgan" }] },
  { name: "Maya Chen", role: "Engineering Lead", bio: "Builds the systems that keep the product quick, dependable, and pleasantly boring.", initials: "MC", location: "Toronto", social: [{ label: "Maya Chen profile", href: "#maya-chen" }] },
  { name: "Jon Bell", role: "Design Director", bio: "Turns complex workflows into interfaces that feel obvious after five minutes.", initials: "JB", location: "London", social: [{ label: "Jon Bell profile", href: "#jon-bell" }] },
  { name: "Priya Shah", role: "Developer Advocate", bio: "Connects product decisions to the people building with them every day.", initials: "PS", location: "Bengaluru", social: [{ label: "Priya Shah profile", href: "#priya-shah" }] },
];

export function TeamSection({
  eyebrow = "People behind the product",
  title = "A small team with a long view.",
  description = "We care about useful software, thoughtful defaults, and the details people notice after the first click.",
  members = DEFAULT_MEMBERS,
}: TeamSectionProps) {
  const headingId = React.useId();
  const featured = members[0];
  const supporting = members.slice(1);

  return (
    <section data-theme="dark" aria-labelledby={headingId} className="bg-[var(--ds-color-background)] font-[var(--ds-font-sans)] text-[var(--ds-color-foreground)]">
      <div className="mx-auto max-w-[1280px] px-4 py-[clamp(4.5rem,3rem+5vw,7.5rem)] sm:px-6 lg:px-8">
        <div className="grid gap-12 lg:grid-cols-[5fr_7fr] lg:items-end lg:gap-16">
          <header className="max-w-xl">
            <p className="font-[var(--ds-font-mono)] text-[11px] uppercase leading-[1.3] tracking-[0.06em] text-[var(--ds-color-muted-foreground)]">{eyebrow}</p>
            <h2 id={headingId} className="mt-4 max-w-[12ch] text-[clamp(2.15rem,1.6rem+2.4vw,3.5rem)] font-semibold leading-[1.05] tracking-[-0.03em]">{title}</h2>
            <p className="mt-5 max-w-[50ch] text-base leading-[1.6] text-[var(--ds-color-muted-foreground)]">{description}</p>
          </header>
          <div className="grid gap-px border border-[var(--ds-color-border)] bg-[var(--ds-color-border)] sm:grid-cols-2">
            {featured ? (
              <article className="group flex min-h-[390px] flex-col bg-[var(--ds-color-surface)] p-6 sm:col-span-2 sm:p-8">
                <div className="flex items-start justify-between gap-6 border-b border-[var(--ds-color-border)] pb-6">
                  <div>
                    <p className="font-[var(--ds-font-mono)] text-[10px] uppercase leading-[1.4] tracking-[0.08em] text-[var(--ds-color-muted-foreground)]">01 / Featured</p>
                    <h3 className="mt-3 text-2xl font-semibold leading-[1.2] tracking-[-0.015em]">{featured.name}</h3>
                    <p className="mt-1 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">{featured.role}</p>
                  </div>
                  <span aria-hidden="true" className="inline-flex size-16 shrink-0 items-center justify-center border border-[var(--ds-color-border-strong)] bg-[var(--ds-color-background)] font-[var(--ds-font-mono)] text-sm font-medium tracking-[0.05em]">{featured.initials ?? featured.name.slice(0, 2).toUpperCase()}</span>
                </div>
                <div className="mt-auto grid gap-6 pt-7 sm:grid-cols-[1fr_auto] sm:items-end">
                  <p className="max-w-[48ch] text-sm leading-[1.55] text-[var(--ds-color-muted-foreground)]">{featured.bio ?? "Bringing product, engineering, and craft together."}</p>
                  <dl className="grid grid-cols-2 gap-x-6 gap-y-3 font-[var(--ds-font-mono)] text-[10px] uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
                    <div><dt>Focus</dt><dd className="mt-1 text-[var(--ds-color-foreground)]">Product</dd></div>
                    <div><dt>Base</dt><dd className="mt-1 text-[var(--ds-color-foreground)]">{featured.location ?? "Remote"}</dd></div>
                  </dl>
                </div>
                {featured.social?.[0] ? <a href={featured.social[0].href} aria-label={featured.social[0].label} className={"mt-6 self-start text-xs font-medium text-[var(--ds-color-link)] underline underline-offset-4 transition-colors duration-150 ease-out hover:text-[var(--ds-color-link-hover)] motion-reduce:transition-none " + FOCUS_RING}>View profile</a> : null}
              </article>
            ) : null}
            {supporting.map((member, index) => (
              <article key={member.name} className="group flex min-h-[220px] flex-col bg-[var(--ds-color-surface)] p-6 transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] motion-reduce:transition-none">
                <div className="flex items-start justify-between gap-4">
                  <p className="font-[var(--ds-font-mono)] text-[10px] uppercase leading-[1.4] tracking-[0.08em] text-[var(--ds-color-muted-foreground)]">{String(index + 2).padStart(2, "0")} / Team</p>
                  <span aria-hidden="true" className="inline-flex size-11 items-center justify-center border border-[var(--ds-color-border-strong)] font-[var(--ds-font-mono)] text-xs font-medium">{member.initials ?? member.name.slice(0, 2).toUpperCase()}</span>
                </div>
                <div className="mt-auto pt-8">
                  <h3 className="text-base font-semibold leading-[1.4]">{member.name}</h3>
                  <p className="mt-1 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">{member.role}</p>
                  {member.location ? <p className="mt-3 font-[var(--ds-font-mono)] text-[10px] uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">{member.location}</p> : null}
                  {member.social?.[0] ? <a href={member.social[0].href} aria-label={member.social[0].label} className={"mt-5 inline-flex text-xs font-medium text-[var(--ds-color-link)] underline underline-offset-4 transition-colors duration-150 ease-out hover:text-[var(--ds-color-link-hover)] motion-reduce:transition-none " + FOCUS_RING}>Profile</a> : null}
                </div>
              </article>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
