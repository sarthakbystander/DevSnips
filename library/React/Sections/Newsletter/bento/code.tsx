import type { FormEvent } from "react";
import { useId, useState } from "react";

/**
 * DevSnips React Newsletter — Bento composition(Bento direction).
 *
 * A genuine 12-column bento cell grid (§4.4) — varied cell sizes,
 * varied jobs, not four identical cards: one large 7-column hero cell
 * (span 7) carries the headline and the primary signup form — the visual
 * focus of the whole composition; a 5-column supporting cell (span 5)
 * lists what subscribers receive; two smaller topic cells (span 5 and 7,
 * stacked beneath the supporting cell) hold the editorial beats;and a
 * full-width bottom strip (span 12) carries the concise privacy/frequency
 * statement. Cells share one radius (radius-lg), one 1px border, one
 * uniform gap (16px mobile / 24px desktop),and a border-only hover
 * lift. One accent:the subscribe button. Published issues are presented
 * as plain editorial text, not cards-within-cards ($15).
 *
 * Collapse (§12.2):large cells span both columns at sm, everything stacks
 * to one column below. Form behavior matches the family exactly:real
 * label/email/required/autocomplete,visible error (`aria-invalid` +
 * `role="alert"`),an announced success state (`role="status"`),and an
 * overridable `onSubmit` — nothing reloads,and nothing leaves the page.

 * Topics are neutral singular-value topicships (props, no emoji);the
 * archive cell names two recent issuesas editorial text with real titles.

 */

export type NewsletterSubmitResult = {
  success: boolean;
  message?: string;
};

export interface NewsletterTopic {
  label: string;
  description: string;
}

export interface NewsletterIssue {
  title: string;
  issue: string;
}

export interface NewsletterSectionProps {
  eyebrow?: string;
  title?: string;
  description?: string;
  emailLabel?: string;
  emailPlaceholder?: string;
  buttonLabel?: string;
  privacyText?: string;
  topics?: NewsletterTopic[];
  issues?: NewsletterIssue[];
  onSubmit?: (email: string) => NewsletterSubmitResult | void;
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const CELL_CLASSES =
  "rounded-[var(--ds-radius-lg)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-6 transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] motion-reduce:transition-none lg:p-8";

const INPUT_CLASSES =
  "h-11 w-full min-w-0 rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-input)] px-4 text-sm leading-5 text-[var(--ds-color-foreground)] placeholder-[var(--ds-color-muted-foreground)] transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] focus:border-[var(--ds-color-focus-ring)] motion-reduce:transition-none " +
  FOCUS_RING;

const ERROR_INPUT_CLASSES =
  "border-[var(--ds-color-destructive)] focus:border-[var(--ds-color-destructive)]";

const BUTTON_CLASSES =
  "inline-flex h-11 w-full shrink-0 items-center justify-center rounded-[var(--ds-radius-sm)] bg-[var(--ds-color-primary)] px-5 text-sm font-semibold leading-5 text-[var(--ds-color-primary-foreground)] transition-colors duration-150 ease-out hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)] motion-reduce:transition-none " +
  FOCUS_RING;

const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const DEFAULT_TOPICS: NewsletterTopic[] = [
  {
    label: "React architecture",
    description: "Component contracts, state boundaries,and the tokens that hold them together.",
  },
  {
    label: "Performance",
    description: "Rendering budgets, layout stability,and measurable Core Web Vitals wins.",
  },
  {
    label: "Accessible interfaces",
    description: "Keyboard models, focus management,and states that never rely on color alone.",
  },
];

const DEFAULT_ISSUES: NewsletterIssue[] = [
  { issue: "Issue 12", title: "Designing a section direction matrix" },
  { issue: "Issue 11", title: "Contrast budgets for dark surfaces" },
];

export function NewsletterSection({
  eyebrow = "The DevSnips Dispatch",
  title = "Frontend engineering, one idea at a time.",
  description = "A short, practical newsletter on React architecture, performance, and accessible interfaces — written by the people shipping DevSnips.",
  emailLabel = "Email address",
  emailPlaceholder = "you@example.com",
  buttonLabel = "Subscribe",
  privacyText = "Twice monthly. No spam. Unsubscribe anytime.",
  topics = DEFAULT_TOPICS,
  issues = DEFAULT_ISSUES,
  onSubmit,
}: NewsletterSectionProps) {
  const headingId = useId();
  const inputId = `${headingId}-email`;
  const errorId = `${headingId}-error`;
  const statusId = `${headingId}-status`;
  const [email, setEmail] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [submitted, setSubmitted] = useState(false);

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const value = email.trim();
    if (!value) {
      setError("Enter your email address to subscribe.");
      setSubmitted(false);
      return;
    }
    if (!EMAIL_PATTERN.test(value)) {
      setError("Enter a valid email address — e.g. you@example.com.");
      setSubmitted(false);
      return;
    }
    setError(null);
    setSubmitted(true);
    if (onSubmit) {
      void onSubmit(value);
    }
  }

  return (
    <section
      aria-labelledby={headingId}
      className="bg-[var(--ds-color-background)] font-[var(--ds-font-sans)] text-[var(--ds-color-foreground)]"
    >
      <div className="mx-auto max-w-[1280px] px-4 py-[clamp(4rem,3rem+4vw,6rem)] sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-12 lg:gap-6">
          <div className={"sm:col-span-2 lg:col-span-7 " + CELL_CLASSES}>
            <p className="text-xs font-semibold uppercase leading-[1.3] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
              {eyebrow}
            </p>
            <h2
              id={headingId}
              className="mt-3 max-w-lg text-[clamp(1.875rem,1.65rem+1vw,2.25rem)] font-semibold leading-[1.15] tracking-[-0.02em]"
            >
              {title}
            </h2>
            <p className="mt-4 max-w-lg text-sm leading-6 text-[var(--ds-color-muted-foreground)]">
              {description}
            </p>

            <form
              onSubmit={handleSubmit}
              noValidate
              className="mt-8"
            >
              <div className="grid grid-cols-1 gap-3 sm:grid-cols-[1fr_auto] lg:max-w-xl">
                <div className="min-w-0">
                  <label
                    htmlFor={inputId}
                    className="sr-only"
                  >
                    {emailLabel}
                  </label>
                  <input
                    id={inputId}
                    type="email"
                    name="email"
                    autoComplete="email"
                    required
                    placeholder={emailPlaceholder}
                    value={email}
                    onChange={(event) => setEmail(event.target.value)}
                    aria-invalid={error ? true : undefined}
                    aria-describedby={error ? errorId : undefined}
                    className={INPUT_CLASSES + (error ? " " + ERROR_INPUT_CLASSES : "")}
                  />
                </div>
                <button type="submit" className={BUTTON_CLASSES}>
                  {buttonLabel}
                </button>
              </div>

              <p
                id={errorId}
                role="alert"
                className={
                  "mt-2 text-sm font-medium leading-5 text-[var(--ds-color-destructive)] " +
                  (error ? "" : "sr-only")
                }
              >
                {error ?? "There was a problem with your subscription."}
              </p>

              <div
                id={statusId}
                role="status"
                aria-live="polite"
                className={
                  "mt-4 flex items-center gap-2 text-sm font-medium leading-5 " +
                  (submitted
                    ? "text-[var(--ds-color-foreground)]"
                    : "sr-only")
                }
              >
                {submitted ? "Thanks — you are on the list." : ""}
              </div>
            </form>
          </div>

          <div className={"sm:col-span-2 lg:col-span-5 " + CELL_CLASSES}>
            <p className="font-[var(--ds-font-mono)] text-xs font-medium uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
              What you receive
            </p>
            <ul className="mt-4 space-y-5">
              <li className="text-sm leading-6">
                <p className="font-medium">One dispatch, twice a month</p>
                <p className="mt-1 text-[var(--ds-color-muted-foreground)]">
                  Two short essays on interface engineering and product systems — a 4–5 minute read each.
                </p>
              </li>
              <li className="text-sm leading-6">
                <p className="font-medium">Real, reviewable code</p>
                <p className="mt-1 text-[var(--ds-color-muted-foreground)]">
                  Every dispatch links the actual snippets — tokens, props,and generated previews included.
                </p>
              </li>
              <li className="text-sm leading-6">
                <p className="font-medium">No feed, no noise</p>
                <p className="mt-1 text-[var(--ds-color-muted-foreground)]">
                  Occasional extras only when there is something worth saying.
                </p>
              </li>
            </ul>
          </div>

          <div className={"sm:col-span-1 lg:col-span-5 " + CELL_CLASSES}>
            <p className="font-[var(--ds-font-mono)] text-xs font-medium uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
              Recent issues
            </p>
            <ul className="mt-4 space-y-4 border-t border-[var(--ds-color-border-subtle)] pt-4">
              {issues.map((item) => (
                <li key={item.issue} className="text-sm leading-5">
                  <p className="font-[var(--ds-font-mono)] text-xs text-[var(--ds-color-muted-foreground)]">
                    {item.issue}
                  </p>
                  <p className="mt-1 font-medium">{item.title}</p>
                </li>
              ))}
            </ul>
          </div>

          <div className={"sm:col-span-1 lg:col-span-7 " + CELL_CLASSES}>
            <p className="font-[var(--ds-font-mono)] text-xs font-medium uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
              Topics on rotation
            </p>
            <ul className="mt-4 grid grid-cols-1 gap-4 border-t border-[var(--ds-color-border-subtle)] pt-4 sm:grid-cols-3">
              {topics.map((topic) => (
                <li key={topic.label} className="text-sm leading-5">
                  <p className="font-medium">{topic.label}</p>
                  <p className="mt-1 text-[var(--ds-color-muted-foreground)]">
                    {topic.description}
                  </p>
                </li>
              ))}
            </ul>
          </div>

          <div className={CELL_CLASSES + " lg:col-span-12"}>
            <p className="mx-auto max-w-2xl text-center text-xs leading-[1.4] text-[var(--ds-color-muted-foreground)]">
              {privacyText}
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}