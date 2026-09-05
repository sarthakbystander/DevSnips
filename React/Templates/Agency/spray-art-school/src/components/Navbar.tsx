import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import Logo from "./Logo";
import Button from "./Button";

const NAV_LINKS = [
  { label: "Work", to: "/work" },
  { label: "About", to: "/about" },
  { label: "Contact", to: "/contact" },
];

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 12);
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <header
      className={`sticky top-0 z-40 border-b-2 transition-colors ${
        scrolled ? "border-bone/20 bg-ink-black/90 backdrop-blur" : "border-transparent bg-transparent"
      }`}
    >
      <nav className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4" aria-label="Primary">
        <Logo />

        <ul className="hidden items-center gap-8 font-body text-sm md:flex">
          {NAV_LINKS.map((link) => (
            <li key={link.to}>
              <Link to={link.to} className="transition-colors hover:text-neon-green">
                {link.label}
              </Link>
            </li>
          ))}
        </ul>

        <div className="hidden md:block">
          <Button variant="standard">Sign up</Button>
        </div>

        <button
          type="button"
          className="text-2xl md:hidden"
          aria-label={menuOpen ? "Close menu" : "Open menu"}
          aria-expanded={menuOpen}
          onClick={() => setMenuOpen((open) => !open)}
        >
          {menuOpen ? "✕" : "☰"}
        </button>
      </nav>

      {menuOpen && (
        <ul className="flex flex-col gap-4 border-t-2 border-bone/20 bg-ink-black px-6 py-6 font-body text-sm md:hidden">
          {NAV_LINKS.map((link) => (
            <li key={link.to}>
              <Link to={link.to} onClick={() => setMenuOpen(false)}>
                {link.label}
              </Link>
            </li>
          ))}
          <li>
            <Button variant="standard" className="w-full">
              Sign up
            </Button>
          </li>
        </ul>
      )}
    </header>
  );
}
