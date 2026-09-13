import Logo from "../components/Logo";

const SOCIALS = [
  { label: "Discord", href: "#" },
  { label: "Twitter", href: "#" },
  { label: "Instagram", href: "#" },
];

export default function Footer() {
  return (
    <footer className="border-t-2 border-bone/20 px-6 py-10" aria-label="Footer">
      <div className="mx-auto flex max-w-6xl flex-col gap-6 sm:flex-row sm:items-center sm:justify-between">
        <Logo />

        <ul className="flex flex-wrap gap-6 font-body text-sm text-bone/70">
          {SOCIALS.map((social) => (
            <li key={social.label}>
              <a href={social.href} className="hover:text-neon-green">
                {social.label}
              </a>
            </li>
          ))}
        </ul>

        <p className="font-body text-xs text-bone/40">© {new Date().getFullYear()} SPRAY Art School</p>
      </div>
    </footer>
  );
}
