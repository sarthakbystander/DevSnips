import { motion } from "framer-motion";
import Button from "../components/Button";
import TornDivider from "../components/TornDivider";
import SplatterDecoration from "../components/SplatterDecoration";

export default function Hero() {
  return (
    <section className="relative overflow-hidden px-6 pb-20 pt-16 sm:pt-24" aria-label="Introduction">
      <SplatterDecoration color="green" className="absolute -left-6 top-10 hidden sm:block" size={140} />
      <SplatterDecoration color="pink" className="absolute -right-4 top-40 hidden md:block" size={100} />

      <div className="relative mx-auto max-w-5xl text-center">
        <motion.h1
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="font-display text-[clamp(3.5rem,12vw,8.5rem)] leading-[0.92] text-bone"
        >
          ART
          <br />
          <span className="text-neon-green">SCHOOL</span>
        </motion.h1>

        <div className="relative my-8">
          <TornDivider color="green" />
        </div>

        <p className="mx-auto max-w-xl font-body text-base text-bone/70 sm:text-lg">
          Real walls, real critique, no clean corners. Learn graffiti, stencils, and muralism from artists who still
          work the street.
        </p>

        <div className="mt-8 flex justify-center">
          <Button variant="spray">Start a course</Button>
        </div>
      </div>
    </section>
  );
}
