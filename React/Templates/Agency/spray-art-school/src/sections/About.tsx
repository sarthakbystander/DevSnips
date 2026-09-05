import SplatterDecoration from "../components/SplatterDecoration";
import TornDivider from "../components/TornDivider";

interface AboutProps {
  as?: "h1" | "h2";
}

export default function About({ as = "h2" }: AboutProps) {
  const Heading = as;

  return (
    <section id="about" className="relative overflow-hidden px-6 py-20" aria-label="About the school">
      <TornDivider color="pink" className="mb-16" />

      <div className="relative mx-auto max-w-3xl">
        <SplatterDecoration color="pink" size={90} className="absolute -left-10 -top-10 hidden sm:block" />

        <Heading
          className="font-display text-3xl leading-snug text-bone sm:text-4xl"
        >
          Discover the school where true{" "}
          <span className="text-neon-green">street art</span> is born, and every student becomes a{" "}
          <span className="text-hot-pink">creator</span> who changes how the city looks.
        </Heading>

        <p className="mt-6 max-w-xl font-body text-base text-bone/70">
          SPRAY was founded by working artists, not administrators. We don't just teach technique — we help you find
          a visual voice that holds up outside the classroom, on a real wall, in public.
        </p>
      </div>
    </section>
  );
}
