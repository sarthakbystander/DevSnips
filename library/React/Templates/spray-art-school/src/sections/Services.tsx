import { motion } from "framer-motion";
import { services } from "../data/services";
import ServiceCard from "../components/ServiceCard";
import SectionHeading from "../components/SectionHeading";

export default function Services() {
  return (
    <section id="courses" className="mx-auto max-w-6xl px-6 py-20" aria-label="Courses">
      <motion.div
        initial={{ opacity: 0, y: 16 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, amount: 0.3 }}
        transition={{ duration: 0.5 }}
      >
        <SectionHeading eyebrow="Our courses">Five ways in, depending on where you're starting.</SectionHeading>
      </motion.div>

      <div className="mt-12 grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
        {services.map((service) => (
          <ServiceCard key={service.id} service={service} />
        ))}
      </div>
    </section>
  );
}
