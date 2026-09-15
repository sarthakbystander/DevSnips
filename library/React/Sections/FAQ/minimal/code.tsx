import { useId, useState } from "react";

/**
 * DevSnips React FAQ — Minimal direction (editorial FAQ composition).
 *
 * The reference composition for the FAQ family: a restrained, editorial
 * question list. A left-aligned header block (eyebrow, heading, lede) sits
 * above a narrow single column of questions (`container-narrow`), each
 * trigger separated by thin 1px hairlines — no cards, no shadows, no
 * decoration (§4.2). Typography and spacing carry the hierarchy; the
 * only accent is the contact link at the foot of the list.
 *
 * The accordion follows the disclosure pattern: a real `<button>` trigger
 * with `aria-expanded` + `aria-controls` wired to a stable, unique panel
 * id,and a `role="region"` panel labelled back by its trigger. At most
 * one item is open at a time,and activating an open item closes it
 * (collapsible). Height animates via the CSS grid-rows trick — no
 * JavaScript measurement —and the closed region is hidden from the
 * accessibility tree and tab order via a discrete `visibility` transition.
 * All transitions are disabled under `prefers-reduced-motion`.
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
  "flex w-full min-w-0 items-center gap-4 px-0 py-4 text-left transition-colors duration-150 ease-out hover:text-[var(--ds-color-foreground)] motion-reduce:transition-none " +
  FOCUS_RING;

const CONTACT_CLASSES =
  "text-sm font-semibold leading-5 text-[var(--ds-color-link)] underline underline-offset-4 transition-colors duration-150 ease-out hover:text-[var(--ds-color-link-hover)] motion-reduce:transition-none " +
  FOCUS_RING;

const CHEVRON =
  "inline-flex h-6 w-6 shrink-0 items-center justify-center rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] text-[var(--ds-color-muted-foreground)] transition-colors duration-150 ease-out motion-reduce:transition-none";

const DEFAULT_ITEMS: FAQItem[] = [
  {
    question: "Can I use DevSnips snippets in commercial projects?",
    answer:
      "Yes. Every snippet is licensed for commercial use under the MIT license, so you can ship it in client work, internal tools,and open-source projects. The only thing we ask is that you keep attribution where the snippet comment requests it.",
  },
  {
    question: "Do the snippets require a build step?",
    answer:
      "No. Tailwind and Vanilla snippets are copy-paste ready: drop `code.html` into any page with the Tailwind CDN or your own compiled build. React snippets are plain function components — paste the component, or pull it in via your bundler. There is no DevSnips runtime or registry to install.",
  },
  {
    question: "How do the design tokens adapt to my own design system?",
    answer:
      "Every component consumes the `--ds-*` semantic tokens via CSS variables. Define your own values once, or omit the block entirely — each snippet ships with its original values as fallbacks, so it renders correctly standalone and upgrades in place when you add a token layer.",
  },
  {
    question: "Are the React sections accessible out of the box?",
    answer:
      "Yes. Sections ship with semantic landmarks, exactly one heading per section wired through `aria-labelledby`, real buttons for every control, visible focus rings, keyboard-operable accordions,and `prefers-reduced-motion` guards on every transition. The QA suite verifies these per variant, in both themes.",
  },
  {
    question: "How do I keep generated previews in sync with my code?",
    answer:
      "Previews are derived, never hand-edited. Each family ships a generator that transforms the authored `code.tsx` into a self-contained `preview.html`; run it with `--check` in CI to fail on drift. You edit one file — the component — and everything else regenerates.",
  },
  {
    question: "Which browsers do you support?",
    answer:
      "All modern evergreen browsers:the last two versions of Chrome, Edge, Firefox,and Safari. The previews use standard grid, custom-property,and container-query features with no polyfills;the components themselves avoid anything experimental.",
  },
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
        "h-3.5 w-3.5 transition-transform duration-200 ease-out motion-reduce:transition-none " +
        (open ? "rotate-180" : "")
      }
    >
      <path d="m6 9 6 6 6-6" />
    </svg>
  );
}

export function FAQSection({
  eyebrow = "Questions, answered.",
  title = "Everything you need to know.",
  description = "Clear answers about using DevSnips in your next project.",
  items = DEFAULT_ITEMS,
  contactLabel = "Read the documentation",
  contactHref = "#docs",
}: FAQSectionProps) {
  const baseId = useId();
  const [openIndex, setOpenIndex] = useState<number | null>(0);

  return (
    <section
      aria-labelledby={`${baseId}-heading`}
      className="bg-[var(--ds-color-background)] font-[var(--ds-font-sans)] text-[var(--ds-color-foreground)]"
    >
      <div className="mx-auto max-w-[768px] px-4 py-[clamp(4rem,3rem+4vw,6rem)] sm:px-6 lg:px-8">
        <div className="max-w-xl">
          <p className="text-xs font-semibold uppercase leading-[1.3] tracking-[0.05em] text-[var(--ds-color-muted-foreground)]">
            {eyebrow}
          </p>
          <h2
            id={`${baseId}-heading`}
            className="mt-3 text-[clamp(1.875rem,1.65rem+1vw,2.25rem)] font-semibold leading-[1.15] tracking-[-0.02em]"
          >
            {title}
          </h2>
          <p className="mt-4 text-[clamp(1rem,0.95rem+0.25vw,1.125rem)] leading-[1.5] text-[var(--ds-color-muted-foreground)]">
            {description}
          </p>
        </div>

        <ul className="mt-10 border-t border-[var(--ds-color-border)] lg:mt-12">
          {items.map((item, index) => {
            const open = index === openIndex;
            const triggerId = `${baseId}-trigger-${index}`;
            const contentId = `${baseId}-content-${index}`;
            return (
              <li
                key={triggerId}
                className="border-b border-[var(--ds-color-border)] last:border-b-0"
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
                    <span className="break-words text-base font-medium leading-6">
                      {item.question}
                    </span>
                    <span className={CHEVRON}>
                      <Chevron open={open} />
                    </span>
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
                    <div className="break-words pb-6 text-sm leading-6 text-[var(--ds-color-muted-foreground)]">
                      {item.answer}
                    </div>
                  </div>
                </div>
              </li>
            );
          })}
        </ul>

        <div className="mt-10 lg:mt-12">
          <a href={contactHref} className={CONTACT_CLASSES}>
            {contactLabel}
          </a>
        </div>
      </div>
    </section>
  );
}