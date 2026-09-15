import type { FormEvent } from "react";
import { useId, useState } from "react";

/**
 * DevSnips React Contact — Neo-Brutalist direction (contact billboard).
 *
 * The expressive ceiling, kept disciplined (§4.5): an oversized three-line
 * "CONTACT" statement headline leading the composition, a large bordered
 * form block (uniform 2px borders, square corners, hard 4px offset
 * shadows with zero blur, oversized h-13 controls),and a rigid
 * contact-information matrix beneath — two flat-fill blocks (one warning
 * fill, the family's single supporting accent) plus a solid bordered block,
 * all aligned to the same grid. Mono uppercase labels, bold typography,
 * strong visual hierarchy, restrained flat token fills — no gradients, no
 * rounded corners, no glow. Press-down:buttons and inputs translate by
 * their shadow offset on `:active` (≤100ms),shadow collapses; the send
 * button carries the one primary fill ($4.5 fill budget:1 primary + 1
 * supporting warning).
 *
 * Status availability is stated in words ("Open for Q4 builds"),never by
 * color alone. The status dot is decorative (`aria-hidden`). Form behavior
 * matches the family exactly:real labels, typed fields,native
 * `type="email"` + `autocomplete`, per-field validation (`aria-invalid` +
 * `aria-describedby` + `role="alert"`),entered values preserved on failure,
 * an announced success state (`role="status"`),and an overridable `onSubmit`
 * — nothing reloads,and nothing leaves the page. Shadows stay inside the
 * CSS box and cells are spaced by the gap,so hard offsets never push outside
 * the viewport. All sample details are fictional (Quarrybase, a storage
 * company, hello@quarrybase.dev).
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

export interface ContactInfoItem {
  label: string;
  value: string;
}

export interface ContactSectionProps {
  eyebrow?: string;
  title?: string;
  description?: string;
  email?: string;
  location?: string;
  responseTime?: string;
  availability?: string;
  availabilityStatus?: string;
  fields?: ContactField[];
  submitLabel?: string;
  successMessage?: string;
  metaCaption?: string;
  contactInfo?: ContactInfoItem[];
  onSubmit?: (values: ContactFormValues) => ContactSubmitResult | void;
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const INPUT_CLASSES =
  "h-13 w-full min-w-0 rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] bg-[var(--ds-color-input)] px-4 text-base leading-6 text-[var(--ds-color-foreground)] placeholder-[var(--ds-color-muted-foreground)] shadow-[4px_4px_0_0_var(--ds-color-border-strong)] transition-[box-shadow,transform] duration-100 ease-out focus:border-[var(--ds-color-foreground)] active:translate-x-[2px] active:translate-y-[2px] active:shadow-[2px_2px_0_0_var(--ds-color-border-strong)] motion-reduce:transition-none " +
  FOCUS_RING;

const TEXTAREA_CLASSES =
  "w-full min-w-0 resize-y rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] bg-[var(--ds-color-input)] px-4 py-4 text-base leading-6 text-[var(--ds-color-foreground)] placeholder-[var(--ds-color-muted-foreground)] shadow-[4px_4px_0_0_var(--ds-color-border-strong)] transition-[box-shadow,transform] duration-100 ease-out focus:border-[var(--ds-color-foreground)] motion-reduce:transition-none " +
  FOCUS_RING;

const ERROR_INPUT_CLASSES =
  "border-[var(--ds-color-destructive)] shadow-[4px_4px_0_0_var(--ds-color-destructive)] focus:border-[var(--ds-color-destructive)]";

const ERROR_TEXT_CLASSES =
  "text-sm font-semibold leading-5 text-[var(--ds-color-destructive)]";

const BUTTON_CLASSES =
  "inline-flex h-13 w-full shrink-0 items-center justify-center rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] bg-[var(--ds-color-primary)] px-6 text-sm font-bold uppercase leading-5 tracking-[0.04em] text-[var(--ds-color-primary-foreground)] shadow-[4px_4px_0_0_var(--ds-color-border-strong)] transition-[transform,box-shadow] duration-100 ease-out active:translate-x-[4px] active:translate-y-[4px] active:shadow-none motion-reduce:transition-none sm:w-auto " +
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
    placeholder: "you@quarrybase.dev",
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
    placeholder: "What are you building?",
    required: true,
  },
];

const DEFAULT_CONTACT_INFO: ContactInfoItem[] = [
  { label: "Email", value: "hello@quarrybase.dev" },
  { label: "Location", value: "Reykjavík · UTC+0" },
  { label: "Response time", value: "Same day" },
  { label: "Sales", value: "sales@quarrybase.dev" },
];

export function ContactSection({
  eyebrow = "Quarrybase",
  title = "CONTACT",
  description =
    "Storage infrastructure for teams that ship cold, warm,and archive data — same-day answers, no ticket queues.",
  email = "hello@quarrybase.dev",
  location = "Reykjavík · UTC+0",
  responseTime = "Same day",
  availability = "Open for Q4 builds",
  availabilityStatus = "Open",
  fields = DEFAULT_FIELDS,
  submitLabel = "Send inquiry",
  successMessage = "Thanks. Your message has been received.",
  metaCaption = "Sales · Support · Partnerships · Media",
  contactInfo = DEFAULT_CONTACT_INFO,
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
        next[field.name] = "Enter a valid email address — e.g. you@quarrybase.dev.";
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
        <div className="max-w-3xl">
          <p className="inline-block rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] bg-[var(--ds-color-surface)] px-3 py-1 font-[var(--ds-font-mono)] text-xs font-semibold uppercase leading-[1.3] tracking-[0.05em] shadow-[4px_4px_0_0_var(--ds-color-border-strong)]">
            {eyebrow}
          </p>
          <h2
            id={headingId}
            className="mt-8 text-[clamp(2.75rem,2.2rem+2.4vw,4rem)] font-bold leading-[0.95] tracking-[-0.03em]"
          >
            {title}
          </h2>
          <p className="mt-5 max-w-xl text-[clamp(1rem,0.95rem+0.25vw,1.125rem)] leading-[1.5] text-[var(--ds-color-muted-foreground)]">
            {description}
          </p>
        </div>

        <div className="mt-10 grid grid-cols-1 gap-6 lg:grid-cols-12 lg:items-start">
          <form
            onSubmit={handleSubmit}
            noValidate
            className="rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] bg-[var(--ds-color-surface)] p-6 shadow-[8px_8px_0_0_var(--ds-color-border-strong)] sm:p-8 lg:col-span-7"
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
                        className="mb-1.5 block font-[var(--ds-font-mono)] text-xs font-semibold uppercase leading-[1.3] tracking-[0.05em]"
                      >
                        {field.label}
                      </label>
                      {field.required ? (
                        <span aria-hidden="true" className="font-[var(--ds-font-mono)] text-xs leading-[1.3] text-[var(--ds-color-muted-foreground)]">
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

            <div className="mt-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
              <button type="submit" className={BUTTON_CLASSES}>
                {submitLabel}
              </button>
              <p className="font-[var(--ds-font-mono)] text-xs leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
                {metaCaption}
              </p>
            </div>

            <div
              id={statusId}
              role="status"
              aria-live="polite"
              className={
                "mt-4 text-sm font-semibold leading-5 " +
                (submitted ? "text-[var(--ds-color-success)]" : "sr-only")
              }
            >
              {submitted ? successMessage : ""}
            </div>
          </form>

          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:col-span-5">
            <div className="rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] bg-[var(--ds-color-warning)] p-6 shadow-[4px_4px_0_0_var(--ds-color-border-strong)] text-[var(--ds-color-warning-foreground)]">
              <p className="font-[var(--ds-font-mono)] text-xs font-semibold uppercase leading-[1.3] tracking-[0.05em]">
                Response time
              </p>
              <p className="mt-4 text-[clamp(1.75rem,1.5rem+1.2vw,2.25rem)] font-bold leading-[1.1] tracking-[-0.02em]">
                {responseTime}
              </p>
              <p className="mt-2 text-sm font-semibold leading-5">
                {availability}
              </p>
            </div>

            <div className="rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] bg-[var(--ds-color-surface)] p-6 shadow-[4px_4px_0_0_var(--ds-color-border-strong)]">
              <p className="flex items-center gap-2 font-[var(--ds-font-mono)] text-xs font-semibold uppercase leading-[1.3] tracking-[0.05em]">
                <span
                  aria-hidden="true"
                  className="h-2 w-2 rounded-[var(--ds-radius-none)] bg-[var(--ds-color-success)]"
                />
                {availabilityStatus}
              </p>
              <p className="mt-4 text-[clamp(1.75rem,1.5rem+1.2vw,2.25rem)] font-bold leading-[1.1] tracking-[-0.02em] break-words">
                <a
                  href={`mailto:${email}`}
                  className={
                    "text-[var(--ds-color-foreground)] underline underline-offset-4 transition-colors duration-150 ease-out hover:text-[var(--ds-color-link)] motion-reduce:transition-none break-words " +
                    FOCUS_RING
                  }
                >
                  {email}
                </a>
              </p>
              <p className="mt-2 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
                {location}
              </p>
            </div>

            <div className="rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] bg-[var(--ds-color-surface)] p-6 shadow-[4px_4px_0_0_var(--ds-color-border-strong)] sm:col-span-2">
              <dl className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                {contactInfo.map((item) => (
                  <div key={item.label}>
                    <dt className="font-[var(--ds-font-mono)] text-xs font-semibold uppercase leading-[1.3] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
                      {item.label}
                    </dt>
                    <dd className="mt-1.5 text-sm font-medium leading-5 break-words">
                      {item.value}
                    </dd>
                  </div>
                ))}
              </dl>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}