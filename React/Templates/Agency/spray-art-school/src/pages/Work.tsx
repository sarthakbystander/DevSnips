import SelectedWork from "../sections/SelectedWork";
import CTA from "../sections/CTA";
import Footer from "../sections/Footer";
import SectionHeading from "../components/SectionHeading";

export default function Work() {
  return (
    <>
      <div className="mx-auto max-w-6xl px-6 pb-4 pt-16">
        <SectionHeading eyebrow="Full archive" as="h1">Every piece our students have shipped.</SectionHeading>
      </div>
      <SelectedWork />
      <CTA />
      <Footer />
    </>
  );
}
