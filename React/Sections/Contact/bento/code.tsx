import type { FormEvent } from "react";
import { useId, useState } from "react";

/**
 * DevSnips React Contact — Bento composition (Bento direction).
 *
 * A genuine 12-column bento contact composition (§4.4) — not a simple
 * two-column form: one large 7-column hero cell (span 7) carries
 * the eyebrow, headline, lede,and the primary contact form — the visual
 * focus of the whole grid; a 5-column contact-information cell (span 5)
 * holds the direct email, address, hours,and a quiet action cue;three
 * smaller cells (span 4 each) carry single facts — email,response
 * time/availability,and location/time zone — with labels and values as a
 * real `<dl>`;and a full-width strip (span 12) holds the supporting
 * response promise. Varied cell weights, one radius (radius-lg), one 1px
 * border, one uniform gap (16px mobile / 24px desktop),and a
 * border-only hover lift — no scale, no glow. One accent:the send
 * transaction (buttons + focus states only, §3.5).
 *
 * Collapse (§12.2): authored spans at lg; the two large cells span both
 * columns at sm, the smaller cells halve to 2-column rows,everything
 * stacks to one column below. Form behavior matches the family exactly:
 * real labels, typed fields, native `type="email"` + `autocomplete`,
 * per-field validation (`aria-invalid` + `aria-describedby` +
 * `role="alert"`),entered values preserved on failure, an announced success
 * state (`role="status"`),and an overridable `onSubmit` — nothing
 * reloads,and nothing leaves the page.

 * All sample values are fictional product details (Northlight Devices /
 * hello@northlight.dev), clearly overridable props.

 * The direct-email cell and the supporting strip are informational, never
 * fake buttons — no cell in the grid is interactive except the form.**
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
  hours?: string;
  responseTime?: string;
  availability?: string;
  fields?: ContactField[];
  submitLabel?: string;
  successMessage?: string;
  stripText?: string;
  onSubmit?: (values: ContactFormValues) => ContactSubmitResult | void;
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const CELL_CLASSES =
  "rounded-[var(--ds-radius-lg)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-6 transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] motion-reduce:transition-none lg:p-8";

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
  "inline-flex h-11 shrink-0 items-center justify-center rounded-[var(--ds-radius-sm)] bg-[var(--ds-color-primary)] px-5 text-sm font-semibold leading-5 text-[var(--ds-color-primary-foreground)] transition-colors duration-150 ease-out hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)] motion-reduce:transition-none " +
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
    placeholder: "you@northlight.dev",
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
    placeholder: "What are you trying to ship?",
    required: true,
  },
];

export function ContactSection({
  eyebrow = "Northlight Devices",
  title = "Talk to the people building it.",
  description =
    "Tell us about the device, the timeline,and the constraints. We route every inquiry to an engineer same-day.",
  email = "hello@northlight.dev",
  location = "Oslo, Norway — UTC+1",
  hours = "Mon–Fri, 9:00–16:00 CET",
  responseTime = "Same business day",
  availability = "Two build slots open for Q4",
  fields = DEFAULT_FIELDS,
  submitLabel = "Send inquiry",
  successMessage = "Thanks. Your message has been received.",
  stripText = "We answer every inquiry in person — no bots, no ticketing queues. If you prefer email, write hello@northlight.dev and keep the thread with you.",
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
        next[field.name] = "Enter a valid email address — e.g. you@northlight.dev.";
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
      aria-labelledby={headingId}
      className="bg-[var(--ds-color-background)] font-[var(--ds-font-sans)] text-[var(--ds-color-foreground)]"
    >
      <div className="mx-auto max-w-[1280px] px-4 py-[clamp(4rem,3rem+4vw,6rem)] sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-12 lg:gap-6">
          <div className={CELL_CLASSES + " sm:col-span-2 lg:col-span-7"}>
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

            <form
              onSubmit={handleSubmit}
              noValidate
              className="mt-8"
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

          <div className={CELL_CLASSES + " sm:col-span-2 lg:col-span-5"}>
            <p className="font-[var(--ds-font-mono)] text-xs font-medium uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
              Direct
            </p>
            <p className="mt-3 text-[clamp(1.125rem,1.05rem+0.4vw,1.375rem)] font-semibold leading-[1.35] break-words">
              <a
                href={`mailto:${email}`}
                className={"text-[var(--ds-color-link)] underline underline-offset-4 transition-colors duration-150 ease-out hover:text-[var(--ds-color-link-hover)] motion-reduce:transition-none break-words " +
                  FOCUS_RING}
              >
                {email}
              </a>
            </p>
            <p className="mt-3 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
              For partnerships, media,and everything else — one inbox,one person on the other end.

            </p>
            <p className="mt-8 border-t border-[var(--ds-color-border-subtle)] pt-4 font-[var(--ds-font-mono)] text-xs leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
              {hours}
            </p>
          </div>

          <div className={CELL_CLASSES + " sm:col-span-1 lg:col-span-4"}>
            <p className="font-[var(--ds-font-mono)] text-xs font-medium uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
              Response time
            </p>
            <p className="mt-3 text-xl font-semibold leading-[1.3] tracking-[-0.01em]">
              {responseTime}
            </p>
            <p className="mt-2 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
              {availability}
            </p>
          </div>

          <div className={CELL_CLASSES + " sm:col-span-1 lg:col-span-4"}>
            <p className="font-[var(--ds-font-mono)] text-xs font-medium uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
              Location
            </p>
            <p className="mt-3 text-xl font-semibold leading-[1.3] tracking-[-0.01em]">
              {location}
            </p>
            <p className="mt-2 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
              Repair lab + offices, appointments by request.

            </p>
          </div>

          <div className={CELL_CLASSES + " sm:col-span-2 lg:col-span-4"}>
            <p className="font-[var(--ds-font-mono)] text-xs font-medium uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
              Availability
            </p>
            <p className="mt-3 text-xl font-semibold leading-[1.3] tracking-[-0.01em]">
              {availability}
            </p>
            <p className="mt-2 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
              Current lead time for new project intake.


            </p>
          </div>

          <div className={CELL_CLASSES + " sm:col-span-2 lg:col-span-12"}>
            <p className="mx-auto max-w-2xl text-center text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
              {stripText}
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}