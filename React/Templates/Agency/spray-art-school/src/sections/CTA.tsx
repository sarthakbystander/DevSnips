import Button from "../components/Button";
import TornDivider from "../components/TornDivider";
import SplatterDecoration from "../components/SplatterDecoration";

export default function CTA() {
  return (
    <section className="relative overflow-hidden px-6 py-24 text-center" aria-label="Enroll call to action">
      <TornDivider color="bone" className="mb-16" />
      <SplatterDecoration color="green" size={110} className="absolute left-6 bottom-6 hidden sm:block" />

      <h2 className="font-display text-4xl leading-tight text-bone sm:text-5xl">
        Let's go draw
        <br />
        <span className="text-hot-pink">something interesting.</span>
      </h2>

      <div className="mt-8 flex justify-center">
        <Button variant="spray">Sign up for a course</Button>
      </div>
    </section>
  );
}
