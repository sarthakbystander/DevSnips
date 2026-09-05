import { Link } from "react-router-dom";

export default function Logo() {
  return (
    <Link to="/" className="font-display text-xl tracking-[0.15em] text-bone" aria-label="SPRAY, home">
      SPRAY
    </Link>
  );
}
