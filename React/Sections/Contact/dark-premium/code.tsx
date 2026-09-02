import type { FormEvent } from "react";
import { useId, useState } from "react";

/**
 * DevSnips React Contact — Dark Premium direction (editorial funnel).
 *
 * A sophisticated contact composition on a pinned dark canvas (§4.3):
 * the left column carries a large editorial statement — a four-line
 * headline with an emphasized line, a lede, then the contact metadata
 * (email, response time, location/time zone) as a ruled list. The
 * right column carries one refined form surface, one elevation step above
 * the canvas with a 1px border and no shadow — designed to read as part
 * of a product interface, not a generic form card. Thin borders,
 * restrained accent (the send action only), premium typography with tight
 * tracking, subtle metadata, and a strong vertical rhythm.
 The section pins `data-theme="dark"` on its own root, so it consumes the
 * same semantic tokens in both page themes — a theme mapping, not a
 * hard-coded dark page (§4.3). No gradients, no glow, no mesh.
 *
 * Form behavior matches the family exactly: real labels, typed fields,
 * native `type="email"` + `autocomplete`, per-field validation
 * (`aria-invalid` + `aria-describedby` + `role="alert"`),entered values
 * preserved on failure, an announced success state (`role="status"`),and
 * an overridable `onSubmit` — nothing reloads,and nothing leaves the page.

 * All sample values are fictional studio details (Example Studio / hello@example.studio),
 * clearly overridable props.
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

export interface ContactSectionProps {
  eyebrow?: string;
  title?: string;
  description?: string;
  email?: string;
  location?: string;
  responseTime?: string;
  fields?: ContactField[];
  submitLabel?: string;
  successMessage?: string;
  panelCaption?: string;
  statement?: string;
  onSubmit?: (values: ContactFormValues) => ContactSubmitResult | void;
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const LINK_CLASSES =
  "font-semibold text-[var(--ds-color-link)] underline underline-offset-4 transition-colors duration-150 ease-out hover:text-[var(--ds-color-link-hover)] motion-reduce:transition-none break-words " +
  FOCUS_RING;

const INPUT_CLASSES =
  "h-11 w-full min-w-0 rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-input)] px-4 text-sm leading-5 text-[var(--ds-color-foreground)] placeholder-[var(--ds-color-muted-foreground)] transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] focus:border-[var(--ds-color-focus-ring)] motion-reduce:transition-none " +
  FOCUS_RING;

const TEXTAREA_CLASSES =
  "w-full min-w-0 resize-y rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-input)] px-4 py-3 text-sm leading-5 text-[var(--ds-color-foreground)] placeholder-[var(--ds-color-muted-foreground)] transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] focus:border-[var(--ds-color-focus-ring)] motion-reduce:transition-none " +
  FOCUS_RING;

const ERROR_INPUT_CLASSES =
  "border-[var(--ds-color-destructive)] focus:border-[var(--ds-color-destructive)]";

const ERROR_TEXT_CLASSES =
  "text-sm font-medium leading-5 text-[var(--ds-color-destructive)]";

const BUTTON_CLASSES =
  "inline-flex h-11 w-full shrink-0 items-center justify-center rounded-[var(--ds-radius-sm)] bg-[var(--ds-color-primary)] px-5 text-sm font-semibold leading-5 text-[var(--ds-color-primary-foreground)] transition-colors duration-150 ease-out hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)] motion-reduce:transition-none " +
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
    placeholder: "you@example.studio",
    required: true,
    autoComplete: "email",
  },
  {
    name: "company",
    label: "Company",
    type: "text",
    placeholder: "Company (optional)",
    required: false,
    autoComplete: "organization",
  },
  {
    name: "message",
    label: "Message",
    type: "textarea",
    placeholder: "What are you building, and where are you headed?",
    required: true,
  },
];

export function ContactSection({
  eyebrow = "Example Studio",
  title = "Have a project in mind?",
  description =
    "Tell us where you're going. We'll help you figure out what comes next — scoping, architecture, and the first build, one conversation at a time.",
  email = "hello@example.studio",
  location = "Copenhagen · UTC+1 — remote worldwide",
  responseTime = "Within one business day",
  fields = DEFAULT_FIELDS,
  submitLabel = "Send inquiry",
  successMessage = "Thanks. Your message has been received.",
  panelCaption = "Start the conversation",
  statement = "We take on a small number of product builds each quarter, and we answer every inquiry.",
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
        next[field.name] = "Enter a valid email address — e.g. you@example.studio.";
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

  return (
    <section
      data-theme="dark"
      aria-labelledby={headingId}
      className="bg-[var(--ds-color-background)] font-[var(--ds-font-sans)] text-[var(--ds-color-foreground)]"
    >
      <div className="mx-auto max-w-[1280px] px-4 py-[clamp(4rem,3rem+4vw,6rem)] sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 gap-12 lg:grid-cols-12 lg:gap-10">
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
            <p className="mt-6 max-w-md text-[clamp(1rem,0.95rem+0.25vw,1.125rem)] leading-[1.5] text-[var(--ds-color-muted-foreground)]">
              {description}
            </p>

            <p className="mt-10 max-w-md text-sm leading-5">
              <span className="sr-only">Primary email</span>
              <a href={`mailto:${email}`} className={LINK_CLASSES}>
                {email}
              </a>
            </p>

            <dl className="mt-6 max-w-md divide-y divide-[var(--ds-color-border-subtle)] border-t border-[var(--ds-color-border-subtle)]">
              <div className="flex items-baseline justify-between gap-4 py-3">
                <dt className="font-[var(--ds-font-mono)] text-xs font-medium uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
                  Response time
                </dt>
                <dd className="text-right text-sm leading-5">{responseTime}</dd>
              </div>
              <div className="flex items-baseline justify-between gap-4 py-3">
                <dt className="font-[var(--ds-font-mono)] text-xs font-medium uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
                  Location
                </dt>
                <dd className="max-w-[60%] text-right text-sm leading-5 break-words">{location}</dd>
              </div>
            </dl>

            <p className="mt-8 max-w-md text-xs leading-[1.5] text-[var(--ds-color-muted-foreground)]">
              {statement}
            </p>
          </div>

          <div className="lg:col-span-7">
            <div className="rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-6 lg:p-8">
              <div className="flex items-baseline justify-between gap-4">
                <p className="font-[var(--ds-font-mono)] text-xs font-medium uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
                  {panelCaption}
                </p>
                <p aria-hidden="true" className="font-[var(--ds-font-mono)] text-xs leading-[1.4] text-[var(--ds-color-muted-foreground)]">
                  01
                </p>
              </div>

              <form
                onSubmit={handleSubmit}
                noValidate
                className="mt-6"
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

                <div className="mt-6 border-t border-[var(--ds-color-border-subtle)] pt-5">
                  <button type="submit" className={BUTTON_CLASSES}>
                    {submitLabel}
                  </button>

                  <div
                    id={statusId}
                    role="status"
                    aria-live="polite"
                    className={
                      "mt-4 text-sm font-medium leading-5 " +
                      (submitted
                        ? "text-[var(--ds-color-success)]"
                        : "sr-only")
                    }
                  >
                    {submitted ? successMessage : ""}
                  </div>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}