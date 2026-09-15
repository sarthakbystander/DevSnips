import { useId, useState } from "react";

/**
 * DevSnips React FAQ — Bento composition (Bento direction).
 *
 * A genuine 12-column bento composition (§4.4) — not a grid of
 * identical FAQ cards. Varied cell sizes carry varied jobs: a large
 * heading cell (span 5, holding eyebrow, title, lede); the FAQ
 * accordion cell (span 7) is the primary focus of the whole grid;
 * beneath, a contact cell (span 5) with the documentation action, and a
 * secondary "Good to know" cell (span 7) holding three quick reference
 * facts. Cells share one radius (radius-lg), one 1px border, one
 * uniform gap (16px mobile / 24px desktop),and a border-only hover
 * lift. One accent: the contact link and the open accordion index.

 * Collapse (§12.2): large cells span both columns at sm (header,FAQ,
 * sticky facts; the two lower cells halve),everything stacks to one
 * column below. The FAQ accordion reuses the same disclosure pattern as
 * every other direction: native `<button>` triggers with
 * `aria-expanded`/`aria-controls`,`role="region"` panels, single-open
 * collapsible state,and the CSS grid-rows height trick with a discrete
 * visibility transition, all reduced-motion-safe.

 * Intentionally action-light: the only primary action is the contact link
 * in the lower-left cell — one CTA per section (§11.1).
 */

export interface FAQItem {
  question: string;
  answer: string;
}

export interface QuickFact {
  label: string;
  value: string;
}

export interface FAQSectionProps {
  eyebrow?: string;
  title?: string;
  description?: string;
  items?: FAQItem[];
  contactLabel?: string;
  contactHref?: string;
  quickFacts?: QuickFact[];
}

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:-outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const CELL_CLASSES =
  "rounded-[var(--ds-radius-lg)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-6 transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] motion-reduce:transition-none lg:p-8";

const TRIGGER_CLASSES =
  "flex w-full min-w-0 items-baseline gap-3 px-0 py-4 text-left transition-colors duration-150 ease-out motion-reduce:transition-none " +
  FOCUS_RING;

const CONTACT_CLASSES =
  "text-sm font-semibold leading-5 text-[var(--ds-color-link)] underline underline-offset-4 transition-colors duration-150 ease-out hover:text-[var(--ds-color-link-hover)] motion-reduce:transition-none " +
  FOCUS_RING;

const DEFAULT_ITEMS: FAQItem[] = [
  {
    question: "Where do snippets fit in my stack?",
    answer:
      "Anywhere you can drop HTML, CSS, or a React function. Sections compose existing primitives from the shared token layer, so they inherit your design system's APIs — icons, buttons, accordions — instead of importing a parallel one.",
  },
  {
    question: "Can I take a section and adapt it to my own content?",
    answer:
      "That is the intended workflow. Every section is a function with overridable props — eyebrow, heading, lede, items, actions — so you replace the defaults with your real copy and ship. The generator only owns the preview; code.tsx is yours to edit.",
  },
  {
    question: "Do the tokens break anything if I omit them?",
    answer:
      "No. Every snippet carries its own values as CSS-variable fallbacks,so a bare copy-paste renders exactly as designed until you define a token layer. When you do, all snippets re-theme at once with a single block.",
  },
  {
    question: "How are the four directions different from four themes?",
    answer:
      "Directions are compositions, not paint jobs — a different layout, hierarchy,and interaction budget per direction, sharing the same tokens, API,and accessibility tree. Minimal is reference;Dark Premium is an editorial split;Bento is a mixed-weight grid;Neo-Brutalist is the expressive ceiling.",
  },
  {
    question: "What is the definition of done for a section?",
    answer:
      "The design-token spec lists thirteen gates — tokens, structure, responsiveness at six widths in two themes, contrast, keyboard, motion, types, direction parity, content, console, metadata,and preview fidelity. A section ships only when every gate passes.",
  },
];

const DEFAULT_QUICK_FACTS: QuickFact[] = [
  { label: "License", value: "MIT — commercial use included" },
  { label: "Stack", value: "HTML, Tailwind, and React — no runtime" },
  { label: "Support", value: "Every family ships a Playwright QA suite" },
];

function Chevron({ open }: { open: boolean }) {
  return (
    <svg
      aria-hidden="true"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={1.75}
      strokeLinecap="round"
      strokeLinejoin="round"
      className={
        "ml-auto h-4 w-4 shrink-0 transition-transform duration-200 ease-out motion-reduce:transition-none " +
        (open ? "rotate-180" : "")
      }
    >
      <path d="m6 9 6 6 6-6" />
    </svg>
  );
}

export function FAQSection({
  eyebrow = "Help center",
  title = "The answers, organized.",
  description = "Installation, licenses, tokens, and the engineering practices behind every DevSnips section — right where you are looking.",
  items = DEFAULT_ITEMS,
  contactLabel = "Talk to support",
  contactHref = "#support",
  quickFacts = DEFAULT_QUICK_FACTS,
}: FAQSectionProps) {
  const baseId = useId();
  const [openIndex, setOpenIndex] = useState<number | null>(0);

  return (
    <section
      aria-labelledby={`${baseId}-heading`}
      className="bg-[var(--ds-color-background)] font-[var(--ds-font-sans)] text-[var(--ds-color-foreground)]"
    >
      <div className="mx-auto max-w-[1280px] px-4 py-[clamp(4rem,3rem+4vw,6rem)] sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-12 lg:gap-6">
          <div className={"sm:col-span-2 lg:col-span-5 " + CELL_CLASSES}>
            <p className="text-xs font-semibold uppercase leading-[1.3] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
              {eyebrow}
            </p>
            <h2
              id={`${baseId}-heading`}
              className="mt-3 text-[clamp(1.875rem,1.65rem+1vw,2.25rem)] font-semibold leading-[1.15] tracking-[-0.02em]"
            >
              {title}
            </h2>
            <p className="mt-4 text-sm leading-6 text-[var(--ds-color-muted-foreground)]">
              {description}
            </p>
          </div>

          <div className={"sm:col-span-2 lg:col-span-7 " + CELL_CLASSES}>
            <p className="font-[var(--ds-font-mono)] text-xs font-medium uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
              Frequently asked
            </p>
            <ul className="mt-2 divide-y divide-[var(--ds-color-border-subtle)]">
              {items.map((item, index) => {
                const open = index === openIndex;
                const triggerId = `${baseId}-trigger-${index}`;
                const contentId = `${baseId}-content-${index}`;
                return (
                  <li key={triggerId}>
                    <h3 className="m-0">
                      <button
                        type="button"
                        id={triggerId}
                        aria-expanded={open}
                        aria-controls={contentId}
                        onClick={() => setOpenIndex(open ? null : index)}
                        className={TRIGGER_CLASSES}
                      >
                        <span className="break-words text-sm font-medium leading-5">
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
                        <div className="break-words pb-4 text-sm leading-6 text-[var(--ds-color-muted-foreground)]">
                          {item.answer}
                        </div>
                      </div>
                    </div>
                  </li>
                );
              })}
            </ul>
          </div>

          <div className={"sm:col-span-1 lg:col-span-5 " + CELL_CLASSES}>
            <p className="text-base font-semibold leading-6">Still have questions?</p>
            <p className="mt-2 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
              Real humans answer, usually within a day.
            </p>
            <p className="mt-6">
              <a href={contactHref} className={CONTACT_CLASSES}>
                {contactLabel}
              </a>
            </p>
          </div>

          <div className={"sm:col-span-1 lg:col-span-7 " + CELL_CLASSES}>
            <p className="font-[var(--ds-font-mono)] text-xs font-medium uppercase leading-[1.4] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
              Good to know
            </p>
            <dl className="mt-4 divide-y divide-[var(--ds-color-border-subtle)] border-t border-[var(--ds-color-border-subtle)]">
              {quickFacts.map((fact) => (
                <div
                  key={fact.label}
                  className="flex items-baseline justify-between gap-4 py-3"
                >
                  <dt className="text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
                    {fact.label}
                  </dt>
                  <dd className="text-right text-sm font-medium leading-5">
                    {fact.value}
                  </dd>
                </div>
              ))}
            </dl>
          </div>
        </div>
      </div>
    </section>
  );
}