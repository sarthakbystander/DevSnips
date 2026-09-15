import type { Service } from "../data/services";

interface ServiceCardProps {
  service: Service;
}

export default function ServiceCard({ service }: ServiceCardProps) {
  return (
    <article
      className="flex flex-col border-4 border-neon-green bg-ink-navy p-6 transition-transform duration-300 hover:-translate-y-1 hover:rotate-0"
      style={{ transform: `rotate(${service.rotate}deg)` }}
    >
      <h3 className="font-display text-2xl text-bone">{service.name}</h3>
      <p className="mt-3 font-body text-sm leading-relaxed text-bone/70">{service.description}</p>
      <ul className="mt-4 flex flex-col gap-1.5">
        {service.bullets.map((bullet) => (
          <li key={bullet} className="flex items-start gap-2 font-body text-sm text-bone/80">
            <span aria-hidden="true" className="mt-1.5 h-1.5 w-1.5 shrink-0 bg-hot-pink" />
            {bullet}
          </li>
        ))}
      </ul>
      <p className="mt-auto pt-6 font-body text-xs uppercase tracking-wider text-neon-green">{service.schedule}</p>
    </article>
  );
}
