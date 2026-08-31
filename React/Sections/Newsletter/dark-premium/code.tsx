import type { FormEvent } from "react";
import { useId, useState } from "react";

/**
 * DevSnips React Newsletter — Dark Premium direction (editorial split).
 *
 * An asymmetric 4/8 editorial split on a permanently dark canvas
 * (§4.3, §10.2): the oversized heading block — eyebrow, title, lede —
 * sits left with a ruled metadata list; the signup form sits right inside a
 * single raised panel, one elevation step above the canvas with a 1px
 * border and no shadow. Restrained accent: the subscribe button and one
 * data highlight (the readers figure). No glow, no mesh, no gradients.
 *
 * The section pins `data-theme="dark"` on its own root, so it consumes the
 * same semantic tokens in both page themes — a theme mapping, not a
 * hard-coded dark page. Form behavior matches the Minimal direction exactly:
 * native label/email/required/autocomplete, visible error (`aria-invalid`
 * + `role="alert"`), an announced success state (`role="status"`),and an
 * overridable `onSubmit` — nothing reloads,and nothing leaves the page.

 * Metadata values are neutral sample figures (readers, frequency, focus),
 * clearly overridable props rather than fabricated social-proof claims.

 */

export type NewsletterSubmitResult = {
  success: boolean;
  message?: string;
};

export interface NewsletterStat {
  value: string;
  label: string;
  accent?: boolean;
}

export interface NewsletterSectionProps {
  eyebrow?: string;
  title?: string;
  description?: string;
  emailLabel?: string;
  emailPlaceholder?: string;
  buttonLabel?: string;
  privacyText?: string;
  panelCaption?: string;
  stats?: NewsletterStat[];
  onSubmit?: (email: string) => NewsletterSubmitResult | void;
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const INPUT_CLASSES =
  "h-11 w-full min-w-0 rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-input)] px-4 text-sm leading-5 text-[var(--ds-color-foreground)] placeholder-[var(--ds-color-muted-foreground)] transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] focus:border-[var(--ds-color-focus-ring)] motion-reduce:transition-none " +
  FOCUS_RING;

const ERROR_INPUT_CLASSES =
  "border-[var(--ds-color-destructive)] focus:border-[var(--ds-color-destructive)]";

const BUTTON_CLASSES =
  "inline-flex h-11 w-full shrink-0 items-center justify-center rounded-[var(--ds-radius-sm)] bg-[var(--ds-color-primary)] px-5 text-sm font-semibold leading-5 text-[var(--ds-color-primary-foreground)] transition-colors duration-150 ease-out hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)] motion-reduce:transition-none " +
  FOCUS_RING;

const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const DEFAULT_STATS: NewsletterStat[] = [
  { value: "24k+", label: "Readers" },
  { value: "Twice monthly", label: "One essay, one dispatch" },
  { value: "Frontend + product engineering", label: "Built by shipping teams" },
];

export function NewsletterSection({
  eyebrow = "The DevSnips Dispatch",
  title = "Design notes from the front lines.",
  description = "One practical essay every other week — render performance, accessible components, and the systems thinking that ships both. No feed, no noise.",
  emailLabel = "Email address",
  emailPlaceholder = "you@example.com",
  buttonLabel = "Subscribe",
  privacyText = "Unsubscribe anytime. We never share your address.",
  panelCaption = "The Dispatch",
  stats = DEFAULT_STATS,
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
      data-theme="dark"
      aria-labelledby={headingId}
      className="bg-[var(--ds-color-background)] font-[var(--ds-font-sans)] text-[var(--ds-color-foreground)]"
    >
      <div className="mx-auto max-w-[1280px] px-4 py-[clamp(4rem,3rem+4vw,6rem)] sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 gap-10 lg:grid-cols-12 lg:gap-12">
          <div className="lg:col-span-4">
            <p className="text-xs font-semibold uppercase leading-[1.3] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
              <span aria-hidden="true" className="mr-2 text-[var(--ds-color-accent)]">—</span>
              {eyebrow}
            </p>
            <h2
              id={headingId}
              className="mt-4 text-[clamp(1.875rem,1.65rem+1vw,2.25rem)] font-semibold leading-[1.15] tracking-[-0.02em]"
            >
              {title}
            </h2>
            <p className="mt-5 text-[clamp(1rem,0.95rem+0.25vw,1.125rem)] leading-[1.5] text-[var(--ds-color-muted-foreground)]">
              {description}
            </p>

            <dl className="mt-10 divide-y divide-[var(--ds-color-border-subtle)] border-t border-[var(--ds-color-border-subtle)] lg:mt-12">
              {stats.map((stat) => (
                <div
                  key={stat.label}
                  className="flex items-baseline justify-between gap-4 py-4"
                >
                  <dt className="text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
                    {stat.label}
                  </dt>
                  <dd
                    className={
                      "text-right font-[var(--ds-font-mono)] text-sm font-medium leading-5 tabular-nums " +
                      (stat.accent
                        ? "text-[var(--ds-color-accent)]"
                        : "text-[var(--ds-color-foreground)]")
                    }
                  >
                    {stat.value}
                  </dd>
                </div>
              ))}
            </dl>
          </div>

          <div className="lg:col-span-8">
            <div className="rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-6 lg:p-8">
              <p className="font-[var(--ds-font-mono)] text-xs font-medium uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
                {panelCaption}
              </p>
              <form
                onSubmit={handleSubmit}
                noValidate
                className="mt-6"
              >
                <div className="grid grid-cols-1 gap-3 sm:grid-cols-[1fr_auto]">
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

                <p className="mt-4 border-t border-[var(--ds-color-border-subtle)] pt-4 text-xs leading-[1.4] text-[var(--ds-color-muted-foreground)]">
                  {privacyText}
                </p>
              </form>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}