import type { FormEvent } from "react";
import { useId, useState } from "react";

/**
 * DevSnips React Contact — Neo-Brutalist direction (inquiry billboard).
 *
 * The expressive ceiling, kept disciplined (§4.5): an oversized
 * "CONTACT" statement heading, a large bordered form block, a contact
 * information matrix, a bold response-time block, and a rigid supporting
 * metadata rail — square geometry, uniform 2px borders, hard 4px
 * offset shadows (zero blur), mono uppercase labels, and oversized form
 * controls that feel intentionally substantial. Inputs carry the same hard
 * shadow as the panels,so the whole block reads as one rigid object.
 The one
 * filled element is the submit button (primary tokens — AA in both themes);
 * the availability chip uses the warning pair (AA in both themes),the
 * family's single supporting fill. Every other element is flat surface —
 * the fill budget spends exactly twice per §4.5. Press-down:the submit
 * button translates by its shadow offset on `:active` (≤100ms),no grow,
 * no glow,no rounded corners,no gradients.
 *
 * Form behavior matches the family exactly:semantic `<form>`, visible
 * labels, typed overridable fields, required + email validation, per-field
 * accessible errors (`aria-invalid` + `aria-describedby` + `role="alert"`),an
 * announced success state (`role="status"`),and a local `onSubmit` —
 * nothing reloads,and nothing leaves the page. Shadows stay inside the CSS
 * box,and blocks are spaced by the gap,so hard offsets never push outside
 * the viewport.

 * Email addresses wrap safely (`break-words`,`truncate` fallbacks),and the
 * availability status is named in words("Open for Q4") next to a
 * decorative dot — never carried by color alone.
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
   availabilityLabel?: string;
  fields?: ContactField[];
  submitLabel?: string;
  metaCaption?: string;
  onSubmit?: (values: ContactValues) => ContactSubmitResult | void;
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const PANEL_CLASSES =
  "rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] bg-[var(--ds-color-surface)] shadow-[4px_4px_0_0_var(--ds-color-border-strong)]";

const INPUT_CLASSES =
  "h-13 w-full min-w-0 rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] bg-[var(--ds-color-input)] px-4 text-base leading-6 text-[var(--ds-color-foreground)] placeholder-[var(--ds-color-muted-foreground)] shadow-[4px_4px_0_0_var(--ds-color-border-strong)] transition-[box-shadow,transform] duration-100 ease-out focus:border-[var(--ds-color-foreground)] motion-reduce:transition-none " +
  FOCUS_RING;

const TEXTAREA_CLASSES =
  "min-h-[140px] w-full resize-y rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] bg-[var(--ds-color-input)] px-4 py-3 text-base leading-6 text-[var(--ds-color-foreground)] placeholder-[var(--ds-color-muted-foreground)] shadow-[4px_4px_0_0_var(--ds-color-border-strong)] transition-[box-shadow,transform] duration-100 ease-out focus:border-[var(--ds-color-foreground)] motion-reduce:transition-none " +
  FOCUS_RING;

const ERROR_INPUT_CLASSES =
  "border-[var(--ds-color-destructive)] shadow-[4px_4px_0_0_var(--ds-color-destructive)] focus:border-[var(--ds-color-destructive)]";

const SUBMIT_CLASSES =
  "inline-flex h-13 w-full items-center justify-center rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] bg-[var(--ds-color-primary)] px-6 text-sm font-bold uppercase leading-5 tracking-[0.04em] text-[var(--ds-color-primary-foreground)] shadow-[4px_4px_0_0_var(--ds-color-border-strong)] transition-[transform,box-shadow] duration-100 ease-out active:translate-x-[4px] active:translate-y-[4px] active:shadow-none motion-reduce:transition-none " +
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
  { name: "message", label: "Message", type: "textarea", placeholder: "Scope, timeline,and what you need from us.", required: true },
];

const ERROR_MESSAGES: Record<string,string> = {
  name: "Enter your name.",
  email: "Enter your email address.",
  company: "",
  message: "Enter your message.",
};

export function ContactSection({
  eyebrow = "Get in touch",
  title = "CONTACT",
  description = "Tell us what you are building, whom it is for,and where you are stuck. One short form — the right person reads every message.",
  email = "hello@example.dev",
  location = "Portland, OR — UTC−8, remote worldwide",
  responseTime = "Within 2 business days",
  availability = "Open for Q4 projects",
  availabilityLabel = "Availability",
  fields = DEFAULT_FIELDS,
  submitLabel = "Send inquiry",
  metaCaption = "Sales · Support · Partnerships — all routed to the same inbox",
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

        <div className="mt-12 grid grid-cols-1 gap-6 lg:grid-cols-12 lg:gap-8 lg:items-start">
          <div className={"lg:col-span-7 p-6 lg:p-8 " + PANEL_CLASSES}>
            <form onSubmit={handleSubmit} noValidate>
              <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
                {fields.map((field) => (
                  <div
                    key={field.name}
                    className={field.name === "company" || field.type === "textarea" ? "sm:col-span-2" : ""}
                  >
                    <label
                      htmlFor={idFor(field.name)}
                      className="block font-[var(--ds-font-mono)] text-xs font-semibold uppercase leading-[1.4] tracking-[0.05em]"
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
                        className="mt-2 text-sm font-semibold leading-5 text-[var(--ds-color-destructive)]"
                      >
                        {errors[field.name]}
                      </p>
                    ) : null}
                  </div>
                ))}
              </div>

              <div className="mt-8">
                <button type="submit" className={SUBMIT_CLASSES}>
                  {submitLabel}
                </button>
              </div>

              <p
                id={`${headingId}-status`}
                role="status"
                aria-live="polite"
                className={
                  "mt-5 text-sm font-semibold leading-5 " +
                  (submitted ? "text-[var(--ds-color-foreground)]" : "sr-only")
                }
              >
                {submitted ? "Thanks. Your message has been received." : ""}
              </p>
            </form>
          </div>

          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:col-span-5 lg:grid-cols-1">
            <div className={"p-6 " + PANEL_CLASSES}>
              <p className="font-[var(--ds-font-mono)] text-xs font-semibold uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
                Email
              </p>
              <p className="mt-3 break-words text-sm leading-6">
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
            </div>

            <div className={"p-6 " + PANEL_CLASSES}>
              <p className="font-[var(--ds-font-mono)] text-xs font-semibold uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
                Location
              </p>
              <p className="mt-3 break-words text-sm leading-6">{location}</p>
            </div>

            <div className={"p-6 " + PANEL_CLASSES}>
              <p className="font-[var(--ds-font-mono)] text-xs font-semibold uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
                Response time
              </p>
              <p className="mt-3 text-[clamp(1.75rem,1.5rem+1.2vw,2.25rem)] font-bold leading-[1.2] tracking-[-0.02em] tabular-nums">
                {responseTime}
              </p>
            </div>

            <div className="rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] bg-[var(--ds-color-warning)] p-6 text-[var(--ds-color-warning-foreground)] shadow-[4px_4px_0_0_var(--ds-color-border-strong)]">
              <p className="font-[var(--ds-font-mono)] text-xs font-bold uppercase leading-[1.4] tracking-[0.05em]">
                {availabilityLabel}
              </p>
              <p className="mt-3 flex items-center gap-2 text-sm font-semibold leading-6">
                <span aria-hidden="true" className="h-2 w-2 rounded-[var(--ds-radius-none)] bg-[var(--ds-color-foreground)]" />
                {availability}
              </p>
            </div>
          </div>
        </div>

        <div className="mt-12 border-t-2 border-[var(--ds-color-border-strong)] pt-6 lg:mt-14">
          <p className="font-[var(--ds-font-mono)] text-xs uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
            {metaCaption}
          </p>
        </div>
      </div>
    </section>
  );
}