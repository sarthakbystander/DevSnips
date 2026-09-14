import type { FormEvent } from "react";
import { useId, useState } from "react";

/**
 * DevSnips React Newsletter — Neo-Brutalist direction (signup billboard).
 *
 * The expressive ceiling, kept disciplined (§4.5): an oversized
 * statement headline, a ruled metadata strip, a large bordered email
 * field, a heavy press-down subscribe button,and a compact privacy note —
 * square geometry, uniform 2px borders, hard 4px offset shadows
 * (zero blur), mono uppercase labels,and flat token fills. The one filled
 * element is the CTA (primary tokens — AA in both themes);the filled
 * statements cell under the metadata uses the warning pair (AA in both
 * themes),the family's single supporting fill ($4.5 fill budget:
 * 1 primary + 1 supporting accent,fitting the sanctioned caps).
 *
 * Restraint: the palette spends its whole budget on those two blocks
 * — every other element is flat surface. Press-down:buttons translate
 * by their shadow offset on `:active` (≤100ms),no grow,no glow,
 * no rounded corners,no gradients. Form behavior matches the family
 * exactly:real label/email/required/autocomplete,visible error
 * (`aria-invalid` + `role="alert"`),an announced success state
 * (`role="status"`),and an overridable `onSubmit` — nothing reloads,and
 * nothing leaves the page. Shadows stay inside the CSS box,and cells are
 * spaced by the gap,so hard offsets never push outside the viewport.**
 */

export type NewsletterSubmitResult = {
  success: boolean;
  message?: string;
};

export interface NewsletterSectionProps {
  eyebrow?: string;
  title?: string;
  description?: string;
  emailLabel?: string;
  emailPlaceholder?: string;
  buttonLabel?: string;
  privacyText?: string;
  metaCaption?: string;
  onSubmit?: (email: string) => NewsletterSubmitResult | void;
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const INPUT_CLASSES =
  "h-13 w-full min-w-0 rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] bg-[var(--ds-color-input)] px-4 text-base leading-6 text-[var(--ds-color-foreground)] placeholder-[var(--ds-color-muted-foreground)] shadow-[4px_4px_0_0_var(--ds-color-border-strong)] transition-[box-shadow,transform] duration-100 ease-out focus:border-[var(--ds-color-foreground)] motion-reduce:transition-none " +
  FOCUS_RING;

const ERROR_INPUT_CLASSES =
  "border-[var(--ds-color-destructive)] shadow-[4px_4px_0_0_var(--ds-color-destructive)] focus:border-[var(--ds-color-destructive)]";

const BUTTON_CLASSES =
  "inline-flex h-13 shrink-0 items-center justify-center rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] bg-[var(--ds-color-primary)] px-6 text-sm font-bold uppercase leading-5 tracking-[0.04em] text-[var(--ds-color-primary-foreground)] shadow-[4px_4px_0_0_var(--ds-color-border-strong)] transition-[transform,box-shadow] duration-100 ease-out active:translate-x-[4px] active:translate-y-[4px] active:shadow-none motion-reduce:transition-none " +
  FOCUS_RING;

const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export function NewsletterSection({
  eyebrow = "Join the dispatch",
  title = "Frontend ideas, straight to your inbox.",
  description = "Two practical essays a month on React architecture, performance,and accessible interfaces — no feed, no noise, unsubscribe in one click.",
  emailLabel = "Email address",
  emailPlaceholder = "you@example.com",
  buttonLabel = "Subscribe",
  privacyText = "No spam. Unsubscribe anytime.",
  metaCaption = "24k+ readers · Twice monthly · Frontend + product engineering",
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
        <div className="max-w-3xl">
          <p className="inline-block rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] bg-[var(--ds-color-surface)] px-3 py-1 font-[var(--ds-font-mono)] text-xs font-semibold uppercase leading-[1.3] tracking-[0.05em] shadow-[4px_4px_0_0_var(--ds-color-border-strong)]">
            {eyebrow}
          </p>
          <h2
            id={headingId}
            className="mt-8 text-[clamp(2.25rem,1.9rem+1.6vw,3rem)] font-bold leading-[1.1] tracking-[-0.02em]"
          >
            {title}
          </h2>
          <p className="mt-5 max-w-xl text-[clamp(1rem,0.95rem+0.25vw,1.125rem)] leading-[1.5] text-[var(--ds-color-muted-foreground)]">
            {description}
          </p>
        </div>

        <div className="mt-10 max-w-3xl">
          <p className="inline-block rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] bg-[var(--ds-color-warning)] px-4 py-2 font-[var(--ds-font-mono)] text-xs font-bold uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-warning-foreground)] shadow-[4px_4px_0_0_var(--ds-color-border-strong)]">
            {metaCaption}
          </p>
        </div>

        <form
          onSubmit={handleSubmit}
          noValidate
          className="mt-10 max-w-3xl"
        >
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-[1fr_auto] sm:gap-4">
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
              "mt-3 text-sm font-semibold leading-5 text-[var(--ds-color-destructive)] " +
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
              "mt-4 flex items-center gap-2 text-sm font-semibold leading-5 " +
              (submitted
                ? "text-[var(--ds-color-foreground)]"
                : "sr-only")
            }
          >
            {submitted ? "Thanks — you are on the list." : ""}
          </div>
        </form>

        <p className="mt-8 max-w-3xl border-t-2 border-[var(--ds-color-border-strong)] pt-4 text-xs leading-[1.4] text-[var(--ds-color-muted-foreground)]">
          {privacyText}
        </p>
      </div>
    </section>
  );
}