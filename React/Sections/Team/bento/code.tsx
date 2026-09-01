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

const DEFAULT_MEMBERS: TeamMember[] = [
  {
    name: "Alex Morgan",
    role: "Founder & Product",
    bio: "Building tools for developers with a bias toward clarity, useful defaults, and calm software.",
    initials: "AM",
    location: "New York",
  },
  {
    name: "Maya Chen",
    role: "Engineering Lead",
    bio: "Systems, reliability, and the invisible work behind fast interfaces.",
    initials: "MC",
    location: "Toronto",
  },
  {
    name: "Jon Bell",
    role: "Design Director",
    bio: "Interface systems and product language.",
    initials: "JB",
    location: "London",
  },
  {
    name: "Priya Shah",
    role: "Developer Advocate",
    bio: "Docs, examples, and the space between product and community.",
    initials: "PS",
    location: "Bengaluru",
  },
];

export function TeamSection({
  eyebrow = "Team / 01",
  title = "Built by people who care about the details.",
  description = "Four perspectives, one shared standard for making software easier to understand and easier to use.",
  members = DEFAULT_MEMBERS,
}: TeamSectionProps) {
  const headingId = React.useId();
  const featured = members[0];
  const secondary = members[1];
  const compact = members.slice(2);

  return (
    <section
      aria-labelledby={headingId}
      className="bg-[var(--ds-color-background)] font-[var(--ds-font-sans)] text-[var(--ds-color-foreground)]"
    >
      <div className="mx-auto max-w-[1280px] px-4 py-[clamp(4rem,3rem+4vw,6rem)] sm:px-6 lg:px-8">
        <header className="max-w-2xl">
          <p className="font-[var(--ds-font-mono)] text-xs uppercase leading-[1.3] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
            {eyebrow}
          </p>
          <h2
            id={headingId}
            className="mt-3 text-[clamp(1.875rem,1.65rem+1vw,2.25rem)] font-semibold leading-[1.15] tracking-[-0.02em]"
          >
            {title}
          </h2>
          <p className="mt-4 max-w-xl text-[clamp(1rem,0.95rem+0.25vw,1.125rem)] leading-[1.5] text-[var(--ds-color-muted-foreground)]">
            {description}
          </p>
        </header>

        <div className="mt-12 grid grid-cols-12 gap-4 lg:mt-16 lg:gap-6">
          {featured ? (
            <article className="col-span-12 flex min-h-[360px] flex-col rounded-[var(--ds-radius-lg)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-6 transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] motion-reduce:transition-none sm:p-8 lg:col-span-7">
              <div className="flex items-start justify-between gap-6">
                <div className="max-w-[44ch]">
                  <p className="font-[var(--ds-font-mono)] text-xs uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
                    Featured profile
                  </p>
                  <h3 className="mt-4 text-2xl font-semibold leading-[1.2] tracking-[-0.015em]">{featured.name}</h3>
                  <p className="mt-1 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">{featured.role}</p>
                </div>
                <span
                  aria-hidden="true"
                  className="inline-flex size-16 shrink-0 items-center justify-center rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border-strong)] bg-[var(--ds-color-surface-subtle)] font-[var(--ds-font-mono)] text-sm font-medium tracking-[0.05em]"
                >
                  {featured.initials ?? featured.name.slice(0, 2).toUpperCase()}
                </span>
              </div>
              <div className="mt-auto grid gap-8 pt-12 sm:grid-cols-[1fr_auto] sm:items-end">
                <p className="max-w-[48ch] text-sm leading-[1.6] text-[var(--ds-color-muted-foreground)]">
                  {featured.bio ?? "Building useful things with a small team."}
                </p>
                <dl className="grid min-w-[150px] gap-3 font-[var(--ds-font-mono)] text-[10px] uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
                  <div className="border-l-2 border-[var(--ds-color-accent)] pl-3">
                    <dt>Focus</dt>
                    <dd className="mt-1 text-[var(--ds-color-foreground)]">Product craft</dd>
                  </div>
                  <div>
                    <dt>Base</dt>
                    <dd className="mt-1 text-[var(--ds-color-foreground)]">{featured.location ?? "Remote"}</dd>
                  </div>
                </dl>
              </div>
            </article>
          ) : null}

          {secondary ? (
            <article className="col-span-12 flex min-h-[360px] flex-col rounded-[var(--ds-radius-lg)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-6 transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] motion-reduce:transition-none sm:p-8 lg:col-span-5">
              <div className="flex items-start justify-between gap-4">
                <p className="font-[var(--ds-font-mono)] text-xs uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
                  Leadership
                </p>
                <span aria-hidden="true" className="text-lg font-semibold tracking-[-0.02em]">
                  02
                </span>
              </div>
              <div className="mt-auto">
                <span
                  aria-hidden="true"
                  className="inline-flex size-12 items-center justify-center rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border-strong)] font-[var(--ds-font-mono)] text-xs font-medium"
                >
                  {secondary.initials ?? secondary.name.slice(0, 2).toUpperCase()}
                </span>
                <h3 className="mt-6 text-xl font-semibold leading-[1.25]">{secondary.name}</h3>
                <p className="mt-1 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">{secondary.role}</p>
                <p className="mt-5 max-w-[40ch] text-sm leading-[1.6] text-[var(--ds-color-muted-foreground)]">
                  {secondary.bio ?? "Leading engineering with care for the details nobody sees."}
                </p>
              </div>
            </article>
          ) : null}

          {compact.map((member, index) => (
            <article
              key={member.name}
              className="col-span-12 min-h-[220px] rounded-[var(--ds-radius-lg)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-6 transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] motion-reduce:transition-none sm:col-span-6 lg:col-span-3"
            >
              <div className="flex items-start justify-between gap-4">
                <span
                  aria-hidden="true"
                  className="inline-flex size-11 items-center justify-center rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border-strong)] font-[var(--ds-font-mono)] text-xs font-medium"
                >
                  {member.initials ?? member.name.slice(0, 2).toUpperCase()}
                </span>
                <span className="font-[var(--ds-font-mono)] text-xs uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
                  {String(index + 3).padStart(2, "0")}
                </span>
              </div>
              <h3 className="mt-10 text-base font-semibold leading-[1.4]">{member.name}</h3>
              <p className="mt-1 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">{member.role}</p>
              {member.location ? (
                <p className="mt-4 font-[var(--ds-font-mono)] text-xs uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
                  {member.location}
                </p>
              ) : null}
            </article>
          ))}

          <div className="col-span-12 rounded-[var(--ds-radius-lg)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface-subtle)] p-6 sm:p-8 lg:col-span-6">
            <p className="font-[var(--ds-font-mono)] text-xs uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
              How we work
            </p>
            <p className="mt-4 max-w-[48ch] text-lg font-medium leading-[1.45] tracking-[-0.01em]">
              Fewer meetings. Clearer writing. More time spent making the thing.
            </p>
          </div>
          <div className="col-span-12 flex items-end rounded-[var(--ds-radius-lg)] border border-[var(--ds-color-border)] p-6 sm:p-8 lg:col-span-6">
            <p className="max-w-[48ch] text-sm leading-[1.6] text-[var(--ds-color-muted-foreground)]">
              The grid is modular on purpose: featured context first, compact identities second, shared philosophy last.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
