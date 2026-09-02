import type { FormEvent } from "react";
import { useId, useState } from "react";

/**
 * DevSnips React Contact — Dark Premium direction (editorial split).
 *
 * A sophisticated contact section on a permanently dark canvas (§4.3):
 * an asymmetric 5/7 split. The left column leads with a large editorial
 * statement ("Have a project in mind? / Tell us where you're going. / We'll
 * help you figure out what comes next."), then a ruled metadata list —
 * email, response time, location/time zone — and a status line naming
 * availability in words(never color alone). The right column holds a
 * refined, product-interface form panel — one elevation step above the
 * canvas with a 1px border and no shadow, a mono panel caption, and
 * restrained spacing. The section pins `data-theme="dark"` on its own
 * root, so it consumes the same semantic tokens in both page themes —
 * a theme mapping, not a hard-coded dark page. One accent:the submit
 * button only (§3.6)。No gradients, no glow, no mesh, no decorative
 * blobs.
 *
 * Form behavior matches the Minimal direction exactly: semantic `<form>`,
 * visible labels, typed overridable fields, required + email validation,
 * per-field accessible errors (`aria-invalid` + `aria-describedby` +
 * `role="alert"`), an announced success state (`role="status"`), anda
 * local `onSubmit` — nothing reloads,and nothing leaves the page.**
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

export interface ContactSectionProps {
  eyebrow?: string;
  title?: string;
  description?: string;
  email?: string;
  location?: string;
  responseTime?: string;
  availability?: string;
  panelCaption?: string;
  fields?: ContactField[];
  submitLabel?: string;
  onSubmit?: (values: ContactValues) => ContactSubmitResult | void;
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const INPUT_CLASSES =
  "h-11 w-full min-w-0 rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-input)] px-4 text-sm leading-5 text-[var(--ds-color-foreground)] placeholder-[var(--ds-color-muted-foreground)] transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] focus:border-[var(--ds-color-focus-ring)] motion-reduce:transition-none " +
  FOCUS_RING;

const TEXTAREA_CLASSES =
  "min-h-[120px] w-full resize-y rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-input)] px-4 py-3 text-sm leading-6 text-[var(--ds-color-foreground)] placeholder-[var(--ds-color-muted-foreground)] transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] focus:border-[var(--ds-color-focus-ring)] motion-reduce:transition-none " +
  FOCUS_RING;

const ERROR_INPUT_CLASSES =
  "border-[var(--ds-color-destructive)] focus:border-[var(--ds-color-destructive)]";

const SUBMIT_CLASSES =
  "inline-flex h-11 w-full items-center justify-center rounded-[var(--ds-radius-sm)] bg-[var(--ds-color-primary)] px-5 text-sm font-semibold leading-5 text-[var(--ds-color-primary-foreground)] transition-colors duration-150 ease-out hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)] motion-reduce:transition-none " +
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
  { name: "message", label: "Message", type: "textarea", placeholder: "Tell us where your team is headed and what the next step looks like.", required: true },
];

const ERROR_MESSAGES: Record<string,string> = {
  name: "Enter your name.",
  email: "Enter your email address.",
  company: "",
  message: "Enter your message.",
};

export function ContactSection({
  eyebrow = "Project intake",
  title = "Have a project in mind?",
  description = "Tell us where you're going. We'll help you figure out what comes next.",
  email = "hello@example.dev",
  location = "Portland, OR — UTC−8, remote worldwide",
  responseTime = "Within two business days",
  availability = "Currently accepting new projects",
  panelCaption = "Project inquiry",
  fields = DEFAULT_FIELDS,
  submitLabel = "Send inquiry",
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
      data-theme="dark"
      aria-labelledby={headingId}
      className="bg-[var(--ds-color-background)] font-[var(--ds-font-sans)] text-[var(--ds-color-foreground)]"
    >
      <div className="mx-auto max-w-[1280px] px-4 py-[clamp(4rem,3rem+4vw,6rem)] sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 items-start gap-12 lg:grid-cols-12 lg:gap-8">
          <div className="lg:col-span-5">
            <p className="text-xs font-semibold uppercase leading-[1.3] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
              <span aria-hidden="true" className="mr-2 text-[var(--ds-color-accent)]">—</span>
              {eyebrow}
            </p>
            <h2
              id={headingId}
              className="mt-4 text-[clamp(2rem,1.7rem+1.4vw,2.75rem)] font-semibold leading-[1.1] tracking-[-0.02em]"
            >
              {title}
            </h2>
            <p className="mt-5 max-w-xl text-[clamp(1rem,0.95rem+0.25vw,1.125rem)] leading-[1.5] text-[var(--ds-color-muted-foreground)]">
              {description}
            </p>

            <dl className="mt-10 border-t border-[var(--ds-color-border-subtle)] pt-6 lg:mt-12">
              <div className="flex flex-col gap-1 py-4 sm:flex-row sm:items-baseline sm:justify-between sm:gap-4">
                <dt className="font-[var(--ds-font-mono)] text-xs font-medium uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
                  Email
                </dt>
                <dd className="break-words text-sm leading-5">
                  <a
                    href={`mailto:${email}`}
                    className={
                      "text-[var(--ds-color-link)] underline underline-offset-4 transition-colors duration-150 ease-out hover:text-[var(--ds-color-link-hover)] motion-reduce:transition-none " +
                      FOCUS_RING
                    }
                  >
                    {email}
                  </a>
                </dd>
              </div>
              <div className="flex flex-col gap-1 border-t border-[var(--ds-color-border-subtle)] py-4 sm:flex-row sm:items-baseline sm:justify-between sm:gap-4">
                <dt className="font-[var(--ds-font-mono)] text-xs font-medium uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
                  Response time
                </dt>
                <dd className="break-words text-sm leading-5">{responseTime}</dd>
              </div>
              <div className="flex flex-col gap-1 border-t border-[var(--ds-color-border-subtle)] py-4 sm:flex-row sm:items-baseline sm:justify-between sm:gap-4">
                <dt className="font-[var(--ds-font-mono)] text-xs font-medium uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
                  Location / time zone
                </dt>
                <dd className="break-words text-sm leading-5">{location}</dd>
              </div>
            </dl>

            <p className="mt-8 flex items-center gap-2 font-[var(--ds-font-mono)] text-xs font-medium uppercase leading-[1.4] tracking-[0.04em]">
              <span aria-hidden="true" className="h-1.5 w-1.5 rounded-full bg-[var(--ds-color-success)]" />
              {availability}
            </p>
          </div>

          <div className="lg:col-span-7">
            <div className="rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-6 lg:p-8">
              <p className="font-[var(--ds-font-mono)] text-xs font-medium uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
                {panelCaption}
              </p>
              <form onSubmit={handleSubmit} noValidate className="mt-6">
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

                <div className="mt-6">
                  <button type="submit" className={SUBMIT_CLASSES}>
                    {submitLabel}
                  </button>
                </div>

                <p
                  id={`${headingId}-status`}
                  role="status"
                  aria-live="polite"
                  className={
                    "mt-4 text-sm font-medium leading-5 " +
                    (submitted ? "text-[var(--ds-color-foreground)]" : "sr-only")
                  }
                >
                  {submitted ? "Thanks. Your message has been received." : ""}
                </p>

                <p className="mt-6 border-t border-[var(--ds-color-border-subtle)] pt-4 text-xs leading-[1.4] text-[var(--ds-color-muted-foreground)]">
                  Your message goes straight to the project team. No mailing lists, no third-party tracking.
                </p>
              </form>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}