import { useState } from "react";
import Button from "../components/Button";
import Footer from "../sections/Footer";
import SectionHeading from "../components/SectionHeading";
import TornDivider from "../components/TornDivider";

export default function Contact() {
  const [submitted, setSubmitted] = useState(false);

  return (
    <>
      <section className="mx-auto max-w-2xl px-6 py-20" aria-label="Contact form">
        <SectionHeading eyebrow="Get in touch" as="h1">Tell us what you want to learn.</SectionHeading>
        <TornDivider color="pink" className="my-10" />

        {submitted ? (
          <p role="status" className="font-body text-lg text-neon-green">
            Sent. We'll get back to you within a couple of days.
          </p>
        ) : (
          <form
            className="flex flex-col gap-5"
            onSubmit={(event) => {
              event.preventDefault();
              setSubmitted(true);
            }}
          >
            <div className="flex flex-col gap-1.5">
              <label htmlFor="name" className="font-body text-sm text-bone/80">
                Name
              </label>
              <input
                id="name"
                name="name"
                type="text"
                required
                className="border-2 border-bone/30 bg-ink-navy px-4 py-2.5 font-body text-bone focus-visible:border-neon-green"
              />
            </div>

            <div className="flex flex-col gap-1.5">
              <label htmlFor="email" className="font-body text-sm text-bone/80">
                Email
              </label>
              <input
                id="email"
                name="email"
                type="email"
                required
                className="border-2 border-bone/30 bg-ink-navy px-4 py-2.5 font-body text-bone focus-visible:border-neon-green"
              />
            </div>

            <div className="flex flex-col gap-1.5">
              <label htmlFor="message" className="font-body text-sm text-bone/80">
                Message
              </label>
              <textarea
                id="message"
                name="message"
                rows={4}
                required
                className="border-2 border-bone/30 bg-ink-navy px-4 py-2.5 font-body text-bone focus-visible:border-neon-green"
              />
            </div>

            <Button variant="spray" type="submit" className="self-start">
              Send message
            </Button>
          </form>
        )}
      </section>
      <Footer />
    </>
  );
}
