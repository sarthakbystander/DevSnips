import { motion } from "framer-motion";
import SectionHeading from "../components/SectionHeading";

const STEPS = [
  { label: "Enroll", detail: "Pick a course, meet your teacher, get your materials list." },
  { label: "Sketch", detail: "Every piece starts on paper. We won't let you skip this." },
  { label: "Wall time", detail: "Practice walls first, then supervised legal spots." },
  { label: "Critique", detail: "Weekly group review — direct, specific, no ego." },
  { label: "Show", detail: "End-of-term group show, open to the public." },
];

export default function Process() {
  return (
    <section id="process" className="mx-auto max-w-5xl px-6 py-20" aria-label="How the program works">
      <SectionHeading eyebrow="Roadmap">How it actually runs, start to finish.</SectionHeading>

      <ol className="relative mt-14 flex flex-col gap-10 border-l-2 border-neon-green/40 pl-8 sm:flex-row sm:gap-6 sm:border-l-0 sm:border-t-2 sm:pl-0 sm:pt-10">
        {STEPS.map((step, index) => (
          <motion.li
            key={step.label}
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.4 }}
            transition={{ duration: 0.4, delay: index * 0.05 }}
            className="relative flex-1"
          >
            <span
              aria-hidden="true"
              className="absolute -left-[38px] top-0 flex h-6 w-6 items-center justify-center rounded-full bg-neon-green font-display text-xs text-ink-black sm:-top-[46px] sm:left-1/2 sm:-translate-x-1/2"
            >
              {index + 1}
            </span>
            <h3 className="font-display text-lg text-bone">{step.label}</h3>
            <p className="mt-2 font-body text-sm text-bone/70">{step.detail}</p>
          </motion.li>
        ))}
      </ol>
    </section>
  );
}
