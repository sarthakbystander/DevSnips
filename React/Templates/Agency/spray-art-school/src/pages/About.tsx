import About from "../sections/About";
import Process from "../sections/Process";
import Testimonials from "../sections/Testimonials";
import CTA from "../sections/CTA";
import Footer from "../sections/Footer";

export default function AboutPage() {
  return (
    <>
      <About as="h1" />
      <Process />
      <Testimonials />
      <CTA />
      <Footer />
    </>
  );
}
