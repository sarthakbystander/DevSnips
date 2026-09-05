import Hero from "../sections/Hero";
import SelectedWork from "../sections/SelectedWork";
import Services from "../sections/Services";
import About from "../sections/About";
import Process from "../sections/Process";
import Testimonials from "../sections/Testimonials";
import CTA from "../sections/CTA";
import Footer from "../sections/Footer";

export default function Home() {
  return (
    <>
      <Hero />
      <SelectedWork />
      <Services />
      <About />
      <Process />
      <Testimonials />
      <CTA />
      <Footer />
    </>
  );
}
