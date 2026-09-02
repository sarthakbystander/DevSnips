import type { FormEvent } from "react";
import { useId, useState } from "react";

/**
 * DevSnips React Contact — Bento composition(Bento direction).
 *
 * A genuine 12-column bento cell grid (§4.4) with varied cell sizes
 * and varied jobs — not four identical cards: one large 7-column form
 * cell (span 7) carries the eyebrow, heading, lede,and the primary
 * contact form; a 5-column contact-information companion cell (span 5)
 * lists the office particulars as a ruled definition list; then a smaller
 * email cell (span 5) and a response/availability cell (span 7) carry
 * second-level contact facts;and a full-width supporting strip (span 12)
 * finishes the grid with the routing note. Cells share one radius (radius-lg),
 * one 1px border, one uniform gap (16px mobile / 24px desktop,),and
 * a border-only hover lift. One accent:the submit button. The form remains
 * the primary interaction and the visual focus of the grid.
 *
 * Collapse (§12.2):the 2 equal columns engage at sm (form cell spans
 * both), everything stacks to 1 below. Form behavior matches the family
 * exactly: semantic `<form>`, visible labels, typed overridable fields,
 * required + email validation, per-field accessible errors
 * (`aria-invalid` + `aria-describedby` + `role="alert"`),an announced success
 * state (`role="status"`),and a local `onSubmit` — nothing reloads,and
 * nothing leaves the page.

 * Office details area real and useful (a `<dl>`, not decorative chips):studio
 * address is fictional, email is the sample @example.dev address,and the
 * status line names availability in words — never color alone.
 */

export type ContactFieldType = "text" | "email" | "textarea";

export interface ContactField {
  name: string;
  label: string;
  type: ContactFieldType;
  placeholder?: string;
  required?: boolean;
}

export type ContactValues = Record<string, string>;

export type ContactSubmitResult = {
  success: boolean;
  message?: string;
};

export interface OfficeDetail {
  label: string;
  value: string;
  href?: string;
}

export interface ContactSectionProps {
  eyebrow?: string;
  title?: string;
  description?: string;
  email?: string;
  location?: string;
  responseTime?: string;
  studio?: string;
  availability?: string;
  details?: OfficeDetail[];
  fields?: ContactField[];
  submitLabel?: string;
  disclaimer?: string;
  onSubmit?: (values: ContactValues) => ContactSubmitResult | void;
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const CELL_CLASSES =
  "rounded-[var(--ds-radius-lg)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-6 transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] motion-reduce:transition-none lg:p-8";

const INPUT_CLASSES =
  "h-11 w-full min-w-0 rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-input)] px-4 text-sm leading-5 text-[var(--ds-color-foreground)] placeholder-[var(--ds-color-muted-foreground)] transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] focus:border-[var(--ds-color-focus-ring)] motion-reduce:transition-none " +
  FOCUS_RING;

const TEXTAREA_CLASSES =
  "min-h-[120px] w-full resize-y rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-input)] px-4 py-3 text-sm leading-6 text-[var(--ds-color-foreground)] placeholder-[var(--ds-color-muted-foreground)] transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] focus:border-[var(--ds-color-focus-ring)] motion-reduce:transition-none " +
  FOCUS_RING;

const ERROR_INPUT_CLASSES =
  "border-[var(--ds-color-destructive)] focus:border-[var(--ds-color-destructive)]";

const SUBMIT_CLASSES =
  "inline-flex h-11 w-full items-center justify-center rounded-[var(--ds-radius-sm)] bg-[var(--ds-color-primary)] px-5 text-sm font-semibold leading-5 text-[var(--ds-color-primary-foreground)] transition-colors duration-150 ease-out hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)] motion-reduce:transition-none sm:w-auto " +
  FOCUS_RING;

const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const AUTOCOMPLETE: Record<string, string> = {
  name: "name",
  email: "email",
  company: "organization",
};

const DEFAULT_FIELDS: ContactField[] = [
  { name: "name", label: "Name", type: "text", placeholder: "Ada Lovelace", required: true },
  { name: "email", label: "Email", type: "email", placeholder: "you@example.dev", required: true },
  { name: "company", label: "Company", type: "text", placeholder: "Acme Inc. — optional", required: false },
  { name: "message", label: "Message", type: "textarea", placeholder: "What are you building,and what does good look like?", required: true },
];

const ERROR_MESSAGES: Record<string,string> = {
  name: "Enter your name.",
  email: "Enter your email address.",
  company: "",
  message: "Enter your message.",
};

const DEFAULT_DETAILS: OfficeDetail[] = [
  { label: "Studio", value: "Fieldwork Studio · 4th floor, 220 NW Alder Avenue" },
  { label: "Email", value: "hello@example.dev", href: "mailto:hello@example.dev" },
  { label: "LinkedIn", value: "Fieldwork Design", href: "#linkedin" },
];

export function ContactSection({
  eyebrow = "Contact",
  title = "Start the conversation.",
  description = "Tell us what you are building, whom it is for,and where you are stuck. The right person reads every message.",
  email = "hello@example.dev",
  location = "Portland, OR — remote worldwide",
  responseTime = "Within two business days",
  studio = "Fieldwork, Portland — remote worldwide",
  availability = "Currently accepting new projects",
  details = DEFAULT_DETAILS,
  fields = DEFAULT_FIELDS,
  submitLabel = "Send inquiry",
  disclaimer = "Sales, partnerships,and support all route to the same inbox. A small team replies within two business days — usually sooner.",
  onSubmit,
}: ContactSectionProps) {
  const headingId = useId();
  const idFor = (name: string) => `${headingId}-${name}`;
  const [values, setValues] = useState<ContactValues>({});
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [submitted, setSubmitted] = useState(false);

  function handleChange(field: ContactField, value: string) {
    setValues((prev) => ({ ...prev, [field.name]: value }));
    setSubmitted(false);
    setErrors((prev) => {
      if (!prev[field.name]) return prev;
      const next = { ...prev };
      delete next[field.name];
      return next;
    });
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const nextErrors: Record<string, string> = {};
    for (const field of fields) {
      const raw = (values[field.name] ?? "").trim();
      if (field.required && !raw) {
        nextErrors[field.name] = ERROR_MESSAGES[field.name] ?? `Enter your ${field.type === "email" ? "email address" : field.label.toLowerCase()}.`;
      } else if (field.type === "email" && raw && !EMAIL_PATTERN.test(raw)) {
        nextErrors[field.name] = "Enter a valid email address — e.g. you@example.com.";
      }
    }
    setErrors(nextErrors);
    if (Object.keys(nextErrors).length > 0) {
      setSubmitted(false);
      return;
    }
    setSubmitted(true);
    if (onSubmit) {
      void onSubmit(values);
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
            <p className="mt-4 max-w-xl text-sm leading-6 text-[var(--ds-color-muted-foreground)]">
              {description}
            </p>

            <form onSubmit={handleSubmit} noValidate className="mt-8">
              <div className="grid grid-cols-1 gap-5 sm:grid-cols-2">
                {fields.map((field) => (
                  <div
                    key={field.name}
                    className={field.name === "company" || field.type === "textarea" ? "sm:col-span-2" : ""}
                  >
                    <label
                      htmlFor={idFor(field.name)}
                      className="block text-sm font-medium leading-5"
                    >
                      {field.label}
                      {field.required ? (
                        <>
                          <span aria-hidden="true" className="text-[var(--ds-color-muted-foreground)]"> *</span>
                          <span className="sr-only"> (required)</span>
                        </>
                      ) : null}
                    </label>
                    {field.type === "textarea" ? (
                      <textarea
                        id={idFor(field.name)}
                        name={field.name}
                        placeholder={field.placeholder}
                        required={field.required}
                        value={values[field.name] ?? ""}
                        onChange={(event) => handleChange(field, event.target.value)}
                        aria-invalid={errors[field.name] ? true : undefined}
                        aria-describedby={errors[field.name] ? `${idFor(field.name)}-error` : undefined}
                        className={TEXTAREA_CLASSES + (errors[field.name] ? " " + ERROR_INPUT_CLASSES : "")}
                      />
                    ) : (
                      <input
                        id={idFor(field.name)}
                        type={field.type}
                        name={field.name}
                        autoComplete={AUTOCOMPLETE[field.name]}
                        placeholder={field.placeholder}
                        required={field.required}
                        value={values[field.name] ?? ""}
                        onChange={(event) => handleChange(field, event.target.value)}
                        aria-invalid={errors[field.name] ? true : undefined}
                        aria-describedby={errors[field.name] ? `${idFor(field.name)}-error` : undefined}
                        className={INPUT_CLASSES + (errors[field.name] ? " " + ERROR_INPUT_CLASSES : "")}
                      />
                    )}
                    {errors[field.name] ? (
                      <p
                        id={`${idFor(field.name)}-error`}
                        role="alert"
                        className="mt-1.5 text-sm font-medium leading-5 text-[var(--ds-color-destructive)]"
                      >
                        {errors[field.name]}
                      </p>
                    ) : null}
                  </div>
                ))}
              </div>

              <div className="mt-6 flex flex-col gap-3 sm:flex-row sm:items-center">
                <button type="submit" className={SUBMIT_CLASSES}>
                  {submitLabel}
                </button>
                <p
                  id={`${headingId}-status`}
                  role="status"
                  aria-live="polite"
                  className={
                    "text-sm font-medium leading-5 " +
                    (submitted ? "text-[var(--ds-color-foreground)]" : "sr-only")
                  }
                >
                  {submitted ? "Thanks. Your message has been received." : ""}
                </p>
              </div>
            </form>
          </div>

          <div className={"sm:col-span-2 lg:col-span-5 " + CELL_CLASSES}>
            <p className="font-[var(--ds-font-mono)] text-xs font-medium uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
              Office
            </p>
            <dl className="mt-2 divide-y divide-[var(--ds-color-border-subtle)]">
              {details.map((detail) => (
                <div
                  key={detail.label}
                  className="flex flex-col gap-1 py-4 first:pt-4 sm:flex-row sm:items-baseline sm:justify-between sm:gap-4"
                >
                  <dt className="font-[var(--ds-font-mono)] text-xs font-medium uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
                    {detail.label}
                  </dt>
                  <dd className="break-words text-sm leading-5">
                    {detail.href ? (
                      <a
                        href={detail.href}
                        className={
                          "text-[var(--ds-color-link)] underline underline-offset-4 transition-colors duration-150 ease-out hover:text-[var(--ds-color-link-hover)] motion-reduce:transition-none " +
                          FOCUS_RING
                        }
                      >
                        {detail.value}
                      </a>
                    ) : (
                      detail.value
                    )}
                  </dd>
                </div>
              ))}
            </dl>
            <p className="mt-2 flex items-center gap-2 text-sm leading-5">
              <span aria-hidden="true" className="h-1.5 w-1.5 rounded-full bg-[var(--ds-color-success)]" />
              {availability}
            </p>
          </div>

          <div className={"sm:col-span-1 lg:col-span-5 " + CELL_CLASSES}>
            <p className="font-[var(--ds-font-mono)] text-xs font-medium uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
              Email us directly
            </p>
            <p className="mt-3 break-words text-sm leading-5">
              <a
                href={`mailto:${email}`}
                className={
                  "text-[var(--ds-color-link)] underline underline-offset-4 transition-colors duration-150 ease-out hover:text-[var(--ds-color-link-hover)] motion-reduce:transition-none " +
                  FOCUS_RING
                }
              >
                {email}
              </a>
            </p>
            <p className="mt-3 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
              For partnerships, speaking,and press.
            </p>
          </div>

          <div className={"sm:col-span-1 lg:col-span-7 " + CELL_CLASSES}>
            <p className="font-[var(--ds-font-mono)] text-xs font-medium uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
              Response time
            </p>
            <p className="mt-3 text-[clamp(1.75rem,1.5rem+1.2vw,2.25rem)] font-semibold leading-[1.2] tracking-[-0.02em]">
              {responseTime}
            </p>
            <p className="mt-2 max-w-md text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
              Most questions are answered within 24 hours during the work week. Complex inquiries get a considered reply, not a rushed one.
            </p>
            <p className="mt-4 border-t border-[var(--ds-color-border-subtle)] pt-4 font-[var(--ds-font-mono)] text-xs font-medium uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
              {location}
            </p>
          </div>

          <div className={"lg:col-span-12 " + CELL_CLASSES}>
            <p className="mx-auto max-w-2xl text-center text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
              {disclaimer}
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}