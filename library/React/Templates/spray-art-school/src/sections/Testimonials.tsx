import { motion } from "framer-motion";
import { testimonials } from "../data/testimonials";
import SectionHeading from "../components/SectionHeading";

export default function Testimonials() {
  return (
    <section className="mx-auto max-w-6xl px-6 py-20" aria-label="Student testimonials">
      <SectionHeading eyebrow="From students" align="center">
        Don't take our word for it.
      </SectionHeading>

      <div className="mt-12 grid gap-8 sm:grid-cols-3">
        {testimonials.map((testimonial, index) => (
          <motion.figure
            key={testimonial.id}
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.4 }}
            transition={{ duration: 0.4, delay: index * 0.08 }}
            className="border-4 border-bone bg-ink-navy p-6"
            style={{ transform: `rotate(${testimonial.rotate}deg)` }}
          >
            <blockquote className="font-body text-sm leading-relaxed text-bone/90">“{testimonial.quote}”</blockquote>
            <figcaption className="mt-4 font-display text-sm text-neon-green">
              {testimonial.name}
              <span className="ml-2 font-body text-xs font-normal text-bone/50">{testimonial.course}</span>
            </figcaption>
          </motion.figure>
        ))}
      </div>
    </section>
  );
}
