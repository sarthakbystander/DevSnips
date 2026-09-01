import type { FormEvent } from "react";
import { useId, useState } from "react";

/**
 * DevSnips React Newsletter — Minimal direction (editorial signup).
 *
 * The reference composition for the Newsletter family: a restrained,
 * editorial signup with a compact eyebrow, a strong-but-controlled
 * headline, one short description, a horizontal email form on desktop
 * (stacked on narrow screens), a subtle divider, and a small privacy note
 * (§4.2). Generous whitespace and hairlines carry the hierarchy — no
 * cards, no shadows, no decorative gradients. The only accent is the
 * subscribe button and the error state.
 *
 * Form behavior(shared by every Newsletter direction):
 *   - semantic `<form>` with a real `<label>` + `type="email"` + `required`
 *     + `name="email"` + `autocomplete="email"`
 *   - client-side validation: empty input and malformed email render a
 *     visible error (`aria-invalid` + `role="alert"`, never color alone)
 *   - successful demo submission prevents default, resolves a success state
 *     announced with `role="status"`,and calls the overridable `onSubmit`
 *   - focus is preserved, nothing reloads,and nothing leaves the page.
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
  onSubmit?: (email: string) => NewsletterSubmitResult | void;
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const INPUT_CLASSES =
  "h-11 w-full min-w-0 rounded-[var(--ds-radius-sm)] border bg-[var(--ds-color-input)] px-4 text-sm leading-5 text-[var(--ds-color-foreground)] placeholder-[var(--ds-color-muted-foreground)] transition-colors duration-150 ease-out " +
  "border-[var(--ds-color-border)] hover:border-[var(--ds-color-border-strong)] focus:border-[var(--ds-color-focus-ring)] motion-reduce:transition-none " +
  FOCUS_RING;

const ERROR_INPUT_CLASSES =
  "border-[var(--ds-color-destructive)] focus:border-[var(--ds-color-destructive)]";

const BUTTON_CLASSES =
  "inline-flex h-11 shrink-0 items-center justify-center rounded-[var(--ds-radius-sm)] bg-[var(--ds-color-primary)] px-5 text-sm font-semibold leading-5 text-[var(--ds-color-primary-foreground)] transition-colors duration-150 ease-out hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)] motion-reduce:transition-none " +
  FOCUS_RING;

const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export function NewsletterSection({
  eyebrow = "The DevSnips Dispatch",
  title = "Useful frontend ideas, without the noise.",
  description = "Practical components, patterns,and interface notes delivered occasionally.",
  emailLabel = "Email address",
  emailPlaceholder = "you@example.com",
  buttonLabel = "Subscribe",
  privacyText = "No spam. Unsubscribe anytime.",
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
      <div className="mx-auto max-w-[768px] px-4 py-[clamp(4rem,3rem+4vw,6rem)] sm:px-6 lg:px-8">
        <p className="text-center text-xs font-semibold uppercase leading-[1.3] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
          {eyebrow}
        </p>
        <h2
          id={headingId}
          className="mx-auto mt-3 max-w-xl text-center text-[clamp(1.875rem,1.65rem+1vw,2.25rem)] font-semibold leading-[1.15] tracking-[-0.02em]"
        >
          {title}
        </h2>
        <p className="mx-auto mt-4 max-w-xl text-center text-[clamp(1rem,0.95rem+0.25vw,1.125rem)] leading-[1.5] text-[var(--ds-color-muted-foreground)]">
          {description}
        </p>

        <form
          onSubmit={handleSubmit}
          noValidate
          className="mx-auto mt-10 max-w-xl"
        >
          <div className="flex flex-col gap-3 sm:flex-row">
            <div className="min-w-0 flex-1">
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
        </form>

        <div
          id={statusId}
          role="status"
          aria-live="polite"
          className={
            "mx-auto mt-6 flex max-w-xl items-center justify-center gap-2 text-sm font-medium leading-5 " +
            (submitted
              ? "text-[var(--ds-color-foreground)]"
              : "sr-only")
          }
        >
          {submitted ? "Thanks — you are on the list." : ""}
        </div>

        <div className="mx-auto mt-8 max-w-xl border-t border-[var(--ds-color-border-subtle)] pt-6">
          <p className="text-center text-xs leading-[1.4] text-[var(--ds-color-muted-foreground)]">
            {privacyText}
          </p>
        </div>
      </div>
    </section>
  );
}