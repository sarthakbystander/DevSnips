import type { Project } from "../data/projects";
import Badge from "./Badge";

interface ProjectCardProps {
  project: Project;
}

export default function ProjectCard({ project }: ProjectCardProps) {
  return (
    <article
      className="group relative border-4 border-bone bg-ink-navy p-4 transition-transform duration-300 hover:-translate-y-1 hover:rotate-0"
      style={{ transform: `rotate(${project.rotate}deg)` }}
    >
      <div
        role="img"
        aria-label={`Placeholder artwork for ${project.title}, ${project.placeholderLabel}`}
        className="mb-4 flex h-48 items-center justify-center bg-gradient-to-br from-hot-pink/30 via-ink-navy to-neon-green/20 font-display text-sm tracking-widest text-bone/70"
      >
        {project.placeholderLabel}
      </div>
      <div className="flex items-start justify-between gap-2">
        <div>
          <h3 className="font-display text-xl text-bone">{project.title}</h3>
          <p className="mt-1 font-body text-sm text-bone/60">
            {project.student} &middot; {project.year}
          </p>
        </div>
        <Badge tone={project.rotate < 0 ? "green" : "pink"} rotate={-project.rotate}>
          {project.category}
        </Badge>
      </div>
    </article>
  );
}
