import { useId, useState } from "react";

/**
 * DevSnips React FAQ — Dark Premium direction (editorial split composition).
 *
 * An asymmetric 4/8 editorial split on a permanently dark canvas
 * (§4.3, §10.2): the large heading block — eyebrow, oversized
 * `section.display`-scale title, lede — sits left; a single raised panel
 * holding the question list sits right, one elevation step above the canvas
 * with a 1px border and no shadow. A ruled "Still have questions?"
 * block beneath the header carries the contact action.
 *
 * The section pins `data-theme="dark"` on its own root, so it consumes
 * the same semantic tokens in both page themes — a theme mapping, not a
 * hard-coded dark page. One accent, spent exactly twice per §3.6: a
 * leading question index on the open item and the contact link. No glow,
 * no mesh, no gradients.
 *
 * Accordion behavior matches the Minimal direction exactly: native
 * `<button>` triggers with `aria-expanded`/`aria-controls`, `role="region"`
 * panels, single-open collapsible state,and the CSS grid-rows height
 * trick with a discrete visibility transition, all reduced-motion-safe.
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
  "focus-visible:outline-2 focus-visible:-outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";

const TRIGGER_CLASSES =
  "flex w-full min-w-0 items-baseline gap-4 px-5 py-4 text-left transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] motion-reduce:transition-none " +
  FOCUS_RING;

const CONTACT_CLASSES =
  "inline-flex items-center text-sm font-semibold leading-5 text-[var(--ds-color-link)] underline underline-offset-4 transition-colors duration-150 ease-out hover:text-[var(--ds-color-link-hover)] motion-reduce:transition-none " +
  FOCUS_RING;

const DEFAULT_ITEMS: FAQItem[] = [
  {
    question: "How does DevSnips licensing work for an agency?",
    answer:
      "Agency work is fully licensed. Build client sites with any snippet, bill for the work, and keep the source. The MIT license covers commercial and client use with attribution waivable by written permission for enterprise agreements.",
  },
  {
    question: "Can I theme a section to match my brand in minutes?",
    answer:
      "Yes — without touching markup. Every section consumes the `--ds-*` semantic tokens, so rebranding is a token re-map. Swap the accent,and foreground, and border values in one CSS block and every family follows: light and dark mappings included.",
  },
  {
    question: "Do the React sections work in an existing design system?",
    answer:
      "They are designed to slot in. Sections compose existing primitives — buttons, accordions, badges — from the shared token layer, so they inherit your component APIs instead of bringing a second system. Use what works, drop what doesn't.",
  },
  {
    question: "What does the QA suite actually verify?",
    answer:
      "Each section family ships a Playwright suite checking structure, counting semantics, aria wiring, real keyboard interaction, focus rings, reduced-motion behavior, zero horizontal overflow at six widths in both themes, and no console errors. Drift between authored code and generated previews fails CI.",
  },
  {
    question: "How do I keep my fork sensitive during a large rebrand?",
    answer:
      "Treat the token block as your single point of change:the components that reference it re-skin instantly, while each snippet keeps standalone fallbacks. Run the family generators with `--check` after any token edit to confirm nothing drifted.",
  },
];

function IndexGlyph({ index, open }: { index: number; open: boolean }) {
  return (
    <span
      aria-hidden="true"
      className={
        "font-[var(--ds-font-mono)] text-xs font-semibold leading-[1.4] tabular-nums transition-colors duration-150 ease-out motion-reduce:transition-none " +
        (open
          ? "text-[var(--ds-color-accent)]"
          : "text-[var(--ds-color-muted-foreground)]")
      }
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
  eyebrow = "Support, documented",
  title = "Documentation is the answer key.",
  description = "The questions teams ask us most, answered in the open — licensing, theming, integration,and the engineering practices that keep a DevSnips section honest in production.",
  items = DEFAULT_ITEMS,
  contactLabel = "Open the full documentation",
  contactHref = "#docs",
}: FAQSectionProps) {
  const baseId = useId();
  const [openIndex, setOpenIndex] = useState<number | null>(0);

  return (
    <section
      data-theme="dark"
      aria-labelledby={`${baseId}-heading`}
      className="bg-[var(--ds-color-background)] font-[var(--ds-font-sans)] text-[var(--ds-color-foreground)]"
    >
      <div className="mx-auto max-w-[1280px] px-4 py-[clamp(4rem,3rem+4vw,6rem)] sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 gap-12 lg:grid-cols-12 lg:gap-8">
          <div className="lg:col-span-4">
            <p className="text-xs font-semibold uppercase leading-[1.3] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
              {eyebrow}
            </p>
            <h2
              id={`${baseId}-heading`}
              className="mt-3 text-[clamp(1.875rem,1.65rem+1vw,2.25rem)] font-semibold leading-[1.15] tracking-[-0.02em]"
            >
              {title}
            </h2>
            <p className="mt-5 text-[clamp(1rem,0.95rem+0.25vw,1.125rem)] leading-[1.5] text-[var(--ds-color-muted-foreground)]">
              {description}
            </p>

            <div className="mt-10 border-t border-[var(--ds-color-border-subtle)] pt-8 lg:mt-12">
              <p className="text-base font-semibold leading-6">Still have questions?</p>
              <p className="mt-2 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
                The docs cover every family, every token,and every generator.
              </p>
              <p className="mt-5">
                <a href={contactHref} className={CONTACT_CLASSES}>
                  {contactLabel}
                </a>
              </p>
            </div>
          </div>

          <div className="lg:col-span-8">
            <ul className="divide-y divide-[var(--ds-color-border-subtle)] rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)]">
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
                        <IndexGlyph index={index} open={open} />
                        <span className="break-words text-base font-medium leading-6">
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
                        <div className="break-words pl-[52px] pr-5 pb-5 text-sm leading-6 text-[var(--ds-color-muted-foreground)]">
                          {item.answer}
                        </div>
                      </div>
                    </div>
                  </li>
                );
              })}
            </ul>
          </div>
        </div>
      </div>
    </section>
  );
}