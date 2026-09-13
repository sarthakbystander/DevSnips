import type { FormEvent } from "react";
import { useId, useState } from "react";

/**
 * DevSnips React Contact — Minimal direction (the reference composition).
 *
 * A restrained editorial contact section (§4.2): an asymmetric 6/6 split
 * of 12. The left column carries the compact eyebrow, headline, one
 * short description, the primary email address, a ruled contact-information
 * list (location, hours,and response time),and a small supporting note.
 * The right column carries the accessible contact form: Name, Email,
 * Company (optional), Message, anda primary send action. Separation
 * comes from whitespace, typography,and hairline rules — no cards, no
 * soft shadows, no decoration. The only accent is the send button and the
 * email link (CTA/links only, §3.6).
 *
 * Form behavior (shared by every Contact direction):
 *   - semantic `<form>` with real `<label>`s, `type="email"` +
 *     `autocomplete="email"` + `name="email"` + `required` on Name/Email/
 *     Message; Company is optional. Appropriate `autocomplete` values
 *     on every field.
 *   - client-side validation without a network request: empty required
 *     fields and malformed email render visible per-field errors
 *     (`aria-invalid` + `aria-describedby` + `role="alert"`, never color
 *     alone), and entered values are preserved when validation fails.
 *   - successful demo submission prevents default, resolves an announced
 *     success state (`role="status"`),and calls the overridable `onSubmit`
 *     with the typed form values. Nothing reloads, nothing navigates, and
 *     nothing leaves the page. All transitions are disabled under
 *     `prefers-reduced-motion`.
 */

export type ContactFieldType = "text" | "email" | "textarea";

export interface ContactField {
  name: string;
  label: string;
  type: ContactFieldType;
  placeholder?: string;
  required?: boolean;
  autoComplete?: string;
}

export interface ContactFormValues {
  name: string;
  email: string;
  company?: string;
  message: string;
}

export interface ContactSubmitResult {
  success: boolean;
  message?: string;
}

export interface ContactDetail {
  label: string;
  value: string;
}

export interface ContactSectionProps {
  eyebrow?: string;
  title?: string;
  description?: string;
  email?: string;
  emailLabel?: string;
  location?: string;
  hours?: string;
  responseTime?: string;
  note?: string;
  fields?: ContactField[];
  submitLabel?: string;
  successMessage?: string;
  onSubmit?: (values: ContactFormValues) => ContactSubmitResult | void;
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const EMAIL_LINK_CLASSES =
  "font-semibold text-[var(--ds-color-link)] underline underline-offset-4 transition-colors duration-150 ease-out hover:text-[var(--ds-color-link-hover)] motion-reduce:transition-none break-words " +
  FOCUS_RING;

const INPUT_CLASSES =
  "h-11 w-full min-w-0 rounded-[var(--ds-radius-sm)] border bg-[var(--ds-color-input)] px-4 text-sm leading-5 text-[var(--ds-color-foreground)] placeholder-[var(--ds-color-muted-foreground)] transition-colors duration-150 ease-out " +
  "border-[var(--ds-color-border)] hover:border-[var(--ds-color-border-strong)] focus:border-[var(--ds-color-focus-ring)] motion-reduce:transition-none " +
  FOCUS_RING;

const TEXTAREA_CLASSES =
  "w-full min-w-0 resize-y rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-input)] px-4 py-3 text-sm leading-5 text-[var(--ds-color-foreground)] placeholder-[var(--ds-color-muted-foreground)] transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] focus:border-[var(--ds-color-focus-ring)] motion-reduce:transition-none " +
  FOCUS_RING;

const ERROR_INPUT_CLASSES =
  "border-[var(--ds-color-destructive)] focus:border-[var(--ds-color-destructive)]";

const ERROR_TEXT_CLASSES =
  "text-sm font-medium leading-5 text-[var(--ds-color-destructive)]";

const BUTTON_CLASSES =
  "inline-flex h-11 w-full shrink-0 items-center justify-center rounded-[var(--ds-radius-sm)] bg-[var(--ds-color-primary)] px-5 text-sm font-semibold leading-5 text-[var(--ds-color-primary-foreground)] transition-colors duration-150 ease-out hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)] motion-reduce:transition-none sm:w-auto " +
  FOCUS_RING;

const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const DEFAULT_FIELDS: ContactField[] = [
  {
    name: "name",
    label: "Name",
    type: "text",
    placeholder: "Ada Lovelace",
    required: true,
    autoComplete: "name",
  },
  {
    name: "email",
    label: "Email",
    type: "email",
    placeholder: "you@example.dev",
    required: true,
    autoComplete: "email",
  },
  {
    name: "company",
    label: "Company",
    type: "text",
    placeholder: "Acme Studio (optional)",
    required: false,
    autoComplete: "organization",
  },
  {
    name: "message",
    label: "Message",
    type: "textarea",
    placeholder: "Tell us what you are working on…",
    required: true,
  },
];

const DETAILS: ContactDetail[] = [
  { label: "Location", value: "Remote — serving teams in every timezone" },
  { label: "Hours", value: "Mon–Fri, 9:00–17:00 CT" },
  { label: "Response time", value: "Within one business day" },
];

export function ContactSection({
  eyebrow = "Get in touch",
  title = "Let's build something useful.",
  description =
    "Tell us what you're working on and what you need help with. We read every inquiry and reply to each one.",
  email = "hello@example.dev",
  emailLabel = "Email us",
  location = "Remote — serving teams in every timezone",
  hours = "Mon–Fri, 9:00–17:00 CT",
  responseTime = "Within one business day",
  note = "Prefer email? Write the address above and keep the whole thread in one place.",
  fields = DEFAULT_FIELDS,
  submitLabel = "Send inquiry",
  successMessage = "Thanks. Your message has been received.",
  onSubmit,
}: ContactSectionProps) {
  const headingId = useId();
  const statusId = `${headingId}-status`;
  const [values, setValues] = useState<Record<string, string>>({});
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [submitted, setSubmitted] = useState(false);

  function handleChange(field: ContactField, event: { target: { value: string } }) {
    setValues((prev) => ({ ...prev, [field.name]: event.target.value }));
    setErrors((prev) => {
      if (!prev[field.name]) return prev;
      const next = { ...prev };
      delete next[field.name];
      return next;
    });
  }

  function validate() {
    const next: Record<string, string> = {};
    for (const field of fields) {
      const raw = values[field.name] ?? "";
      if (field.required && !raw.trim()) {
        next[field.name] = `Enter your ${field.label.toLowerCase()}.`;
      } else if (field.type === "email" && raw.trim() && !EMAIL_PATTERN.test(raw.trim())) {
        next[field.name] = "Enter a valid email address — e.g. you@example.dev.";
      }
    }
    return next;
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const nextErrors = validate();
    setErrors(nextErrors);
    if (Object.keys(nextErrors).length > 0) {
      setSubmitted(false);
      const firstInvalid = fields.find((f) => nextErrors[f.name]);
      if (firstInvalid) {
        document.getElementById(`${headingId}-${firstInvalid.name}`)?.focus();
      }
      return;
    }
    setSubmitted(true);
    const formValues: ContactFormValues = {
      name: (values["name"] ?? "").trim(),
      email: (values["email"] ?? "").trim(),
      message: (values["message"] ?? "").trim(),
    };
    if (values["company"]?.trim()) {
      formValues.company = values["company"].trim();
    }
    if (onSubmit) {
      void onSubmit(formValues);
    }
  }

  const detailRows: ContactDetail[] = [
    { label: "Email", value: email },
    { label: "Location", value: location },
    { label: "Hours", value: hours },
    { label: "Response time", value: responseTime },
  ];

  return (
    <section
      aria-labelledby={headingId}
      className="bg-[var(--ds-color-background)] font-[var(--ds-font-sans)] text-[var(--ds-color-foreground)]"
    >
      <div className="mx-auto max-w-[1280px] px-4 py-[clamp(4rem,3rem+4vw,6rem)] sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 gap-12 lg:grid-cols-12 lg:gap-16">
          <div className="lg:col-span-6">
            <p className="text-xs font-semibold uppercase leading-[1.3] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
              {eyebrow}
            </p>
            <h2
              id={headingId}
              className="mt-3 max-w-xl text-[clamp(1.875rem,1.65rem+1vw,2.25rem)] font-semibold leading-[1.15] tracking-[-0.02em]"
            >
              {title}
            </h2>
            <p className="mt-4 max-w-xl text-[clamp(1rem,0.95rem+0.25vw,1.125rem)] leading-[1.5] text-[var(--ds-color-muted-foreground)]">
              {description}
            </p>

            <p className="mt-8 text-sm leading-5">
              <span className="sr-only">{emailLabel}</span>
              <a href={`mailto:${email}`} className={EMAIL_LINK_CLASSES}>
                {email}
              </a>
            </p>

            <dl className="mt-8 divide-y divide-[var(--ds-color-border-subtle)] border-t border-[var(--ds-color-border-subtle)]">
              {detailRows.map((row) => (
                <div
                  key={row.label}
                  className="flex items-baseline justify-between gap-4 py-3"
                >
                  <dt className="font-[var(--ds-font-mono)] text-xs font-medium uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
                    {row.label}
                  </dt>
                  <dd className="max-w-[60%] text-right text-sm leading-5 break-words">
                    {row.value}
                  </dd>
                </div>
              ))}
            </dl>

            <p className="mt-8 max-w-md text-xs leading-[1.5] text-[var(--ds-color-muted-foreground)]">
              {note}
            </p>
          </div>

          <div className="lg:col-span-6">
            <form
              onSubmit={handleSubmit}
              noValidate
              className="border-t border-[var(--ds-color-border-subtle)] pt-8"
            >
              <div className="grid grid-cols-1 gap-5 sm:grid-cols-2">
                {fields.map((field) => {
                  const fieldId = `${headingId}-${field.name}`;
                  const errorId = `${fieldId}-error`;
                  const error = errors[field.name];
                  return (
                    <div
                      key={field.name}
                      className={
                        "min-w-0 " +
                        (field.type === "textarea" ? "sm:col-span-2" : "")
                      }
                    >
                      <div className="flex items-baseline justify-between gap-3">
                        <label
                          htmlFor={fieldId}
                          className="mb-1.5 block text-sm font-medium leading-5"
                        >
                          {field.label}
                        </label>
                        {field.required ? (
                          <span aria-hidden="true" className="text-[var(--ds-color-muted-foreground)]">
                            *
                          </span>
                        ) : null}
                      </div>
                      {field.type === "textarea" ? (
                        <textarea
                          id={fieldId}
                          name={field.name}
                          rows={5}
                          placeholder={field.placeholder}
                          required={field.required}
                          value={values[field.name] ?? ""}
                          onChange={(event) => handleChange(field, event)}
                          aria-invalid={error ? true : undefined}
                          aria-describedby={error ? errorId : undefined}
                          className={TEXTAREA_CLASSES + (error ? " " + ERROR_INPUT_CLASSES : "")}
                        />
                      ) : (
                        <input
                          id={fieldId}
                          name={field.name}
                          type={field.type}
                          placeholder={field.placeholder}
                          required={field.required}
                          autoComplete={field.autoComplete}
                          value={values[field.name] ?? ""}
                          onChange={(event) => handleChange(field, event)}
                          aria-invalid={error ? true : undefined}
                          aria-describedby={error ? errorId : undefined}
                          className={INPUT_CLASSES + (error ? " " + ERROR_INPUT_CLASSES : "")}
                        />
                      )}
                      {error ? (
                        <p
                          id={errorId}
                          role="alert"
                          className={"mt-1.5 " + ERROR_TEXT_CLASSES}
                        >
                          {error}
                        </p>
                      ) : null}
                    </div>
                  );
                })}
              </div>

              <div className="mt-6">
                <button type="submit" className={BUTTON_CLASSES}>
                  {submitLabel}
                </button>
              </div>

              <div
                id={statusId}
                role="status"
                aria-live="polite"
                className={
                  "mt-4 flex items-center gap-2 text-sm font-medium leading-5 " +
                  (submitted
                    ? "text-[var(--ds-color-success)]"
                    : "sr-only")
                }
              >
                {submitted ? successMessage : ""}
              </div>
            </form>
          </div>
        </div>
      </div>
    </section>
  );
}