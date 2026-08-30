import { useId, useState } from "react";

/**
 * DevSnips React FAQ — Neo-Brutalist direction (structured-block composition).
 *
 * The expressive ceiling, kept disciplined (§4.5): FAQ items as square,
 * 2px-bordered interface blocks with hard 4px offset shadows (zero blur,
 * zero spread), mono index numbers, bold questions,and a press-down
 * trigger that translates by its shadow offset on `:active` (≤100ms).
 * Question and answer read as one structured unit — not an ordinary card.
 *
 * Restraint: every block sits flat surface (bg-surface) — no accent-filled
 * cells, no collage. The palette spends its whole budget on one element:
 * the contact action, a filled primary press-down button. The eyebrow
 * is a bordered mono chip with the same hard offset shadow language. All
 * borders are 2px `color.border-strong` — uniform everywhere (§4.5).
 *
 * The accordion uses the same disclosure pattern as every other direction:
 * native `<button>` triggers with `aria-expanded`/`aria-controls`,
 * `role="region"` panels, collapsible single-open state,and a discrete
 * visibility transition — nothing rounds, glows, or gradients.
 */

export interface FAQItem {
  question: string;
  answer: string;
}

export interface FAQSectionProps {
  eyebrow?: string;
  title?: string;
  description?: string;
  items?: FAQItem[];
  contactLabel?: string;
  contactHref?: string;
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const TRIGGER_CLASSES =
  "flex w-full min-w-0 items-baseline gap-4 px-0 py-4 text-left transition-colors duration-100 ease-out active:translate-y-[4px] motion-reduce:transition-none " +
  FOCUS_RING;

const CONTACT_CLASSES =
  "inline-flex h-11 items-center justify-center rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] bg-[var(--ds-color-primary)] px-5 text-sm font-semibold leading-5 text-[var(--ds-color-primary-foreground)] shadow-[4px_4px_0_0_var(--ds-color-border-strong)] transition-[transform,box-shadow] duration-100 ease-out active:translate-x-[4px] active:translate-y-[4px] active:shadow-none motion-reduce:transition-none " +
  FOCUS_RING;

const DEFAULT_ITEMS: FAQItem[] = [
  {
    question: "Is DevSnips one more design system?",
    answer:
      "No — it is a library of systems: components, sections,and templates, each consuming one shared semantic token layer. There is no account, no cloud sync, no package to install. You copy the code and own it.",
  },
  {
    question: "What exactly do I get per section?",
    answer:
      "Three files per variant: an authored `code.tsx`, a `metadata.json`, and a generated, self-contained `preview.html`. Drag the component into your page, override the props,and ship. The preview stays derived — never hand-edited — so it can't drift from the source.",
  },
  {
    question: "Can the four directions sit on one page?",
    answer:
      "Yes — that is the point of the shared token layer. A Minimal hero, a Dark Premium FAQ, a Bento features grid,and a Neo-Brutalist CTA all re-theme from the same variables and keep one visual language per page, however you mix them.",
  },
  {
    question: "Do I have to use the tokens to use the components?",
    answer:
      "No. Every snippet ships with its values embedded as fallbacks, so a lone copy-paste renders identically with zero setup. Define the token block once, though,and every component you pull in re-themes in place with it.",
  },
  {
    question: "What is the one rule the QA suite refuses to bend?",
    answer:
      "Zero horizontal overflow, both themes, at every width from 320 to 1440 pixels. It is the single easiest thing to get wrong and the single most common source of broken embeds — so every family's Playwright run checks it before anything ships.",
  },
];

function IndexBadge({ index }: { index: number }) {
  return (
    <span
      aria-hidden="true"
      className="inline-flex h-8 w-10 shrink-0 items-center justify-center rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] bg-[var(--ds-color-surface)] font-[var(--ds-font-mono)] text-xs font-semibold leading-[1.4] tabular-nums text-[var(--ds-color-muted-foreground)]"
    >
      {String(index + 1).padStart(2, "0")}
    </span>
  );
}

function Chevron({ open }: { open: boolean }) {
  return (
    <svg
      aria-hidden="true"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={2}
      strokeLinecap="square"
      strokeLinejoin="miter"
      className={
        "ml-auto h-4 w-4 shrink-0 transition-transform duration-100 ease-out motion-reduce:transition-none " +
        (open ? "rotate-180" : "")
      }
    >
      <path d="m6 9 6 6 6-6" />
    </svg>
  );
}

export function FAQSection({
  eyebrow = "FAQ",
  title = "Read this before you ask.",
  description = "Five answers that cover licensing, structure, theming, and the one rule QA refuses to bend.",
  items = DEFAULT_ITEMS,
  contactLabel = "Read the docs",
  contactHref = "#docs",
}: FAQSectionProps) {
  const baseId = useId();
  const [openIndex, setOpenIndex] = useState<number | null>(0);

  return (
    <section
      aria-labelledby={`${baseId}-heading`}
      className="bg-[var(--ds-color-background)] font-[var(--ds-font-sans)] text-[var(--ds-color-foreground)]"
    >
      <div className="mx-auto max-w-[1280px] px-4 py-[clamp(4rem,3rem+4vw,6rem)] sm:px-6 lg:px-8">
        <div className="max-w-2xl">
          <p className="inline-block rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] bg-[var(--ds-color-surface)] px-3 py-1 font-[var(--ds-font-mono)] text-xs font-semibold uppercase leading-[1.3] tracking-[0.05em] shadow-[4px_4px_0_0_var(--ds-color-border-strong)]">
            {eyebrow}
          </p>
          <h2
            id={`${baseId}-heading`}
            className="mt-6 text-[clamp(1.875rem,1.65rem+1vw,2.25rem)] font-bold leading-[1.15] tracking-[-0.02em]"
          >
            {title}
          </h2>
          <p className="mt-4 max-w-xl text-[clamp(1rem,0.95rem+0.25vw,1.125rem)] leading-[1.5] text-[var(--ds-color-muted-foreground)]">
            {description}
          </p>
        </div>

        <ul className="mt-12 grid grid-cols-1 gap-6 lg:mt-16">
          {items.map((item, index) => {
            const open = index === openIndex;
            const triggerId = `${baseId}-trigger-${index}`;
            const contentId = `${baseId}-content-${index}`;
            return (
              <li
                key={triggerId}
                className={
                  "rounded-[var(--ds-radius-none)] border-2 border-[var(--ds-color-border-strong)] bg-[var(--ds-color-surface)] px-5 py-4 shadow-[4px_4px_0_0_var(--ds-color-border-strong)] sm:px-6 " +
                  (open ? "border-[var(--ds-color-foreground)]" : "")
                }
              >
                <h3 className="m-0">
                  <button
                    type="button"
                    id={triggerId}
                    aria-expanded={open}
                    aria-controls={contentId}
                    onClick={() => setOpenIndex(open ? null : index)}
                    className={TRIGGER_CLASSES}
                  >
                    <IndexBadge index={index} />
                    <span className="break-words text-base font-bold leading-6">
                      {item.question}
                    </span>
                    <Chevron open={open} />
                  </button>
                </h3>
                <div
                  id={contentId}
                  role="region"
                  aria-labelledby={triggerId}
                  className={
                    "grid transition-[grid-template-rows] duration-200 ease-out motion-reduce:transition-none " +
                    (open ? "grid-rows-[1fr]" : "grid-rows-[0fr]")
                  }
                >
                  <div
                    className={
                      "min-h-0 overflow-hidden transition-[visibility] duration-200 motion-reduce:transition-none " +
                      (open ? "visible" : "invisible")
                    }
                  >
                    <div className="break-words pb-1 pr-2 pl-[56px] text-sm leading-6 text-[var(--ds-color-muted-foreground)]">
                      {item.answer}
                    </div>
                  </div>
                </div>
              </li>
            );
          })}
        </ul>

        <div className="mt-12 lg:mt-14">
          <a href={contactHref} className={CONTACT_CLASSES}>
            {contactLabel}
          </a>
        </div>
      </div>
    </section>
  );
}