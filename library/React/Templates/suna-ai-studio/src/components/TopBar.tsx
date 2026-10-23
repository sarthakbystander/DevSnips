import { Icon } from "./Icon";
import { SunaMark } from "./SunaMark";
import { pluralise } from "../lib/format";
import { SUNA_SPACE_URL } from "../lib/suna";
import { useStudio } from "../studio/StudioProvider";

const AVAILABILITY_COPY = {
  checking: { label: "Checking", dot: "bg-gold animate-pulse-soft" },
  online: { label: "Reachable", dot: "bg-sage" },
  offline: { label: "Offline", dot: "bg-accent" },
  unknown: { label: "Unknown", dot: "bg-faint" },
} as const;

export function TopBar({ onOpenMenu }: { onOpenMenu: () => void }) {
  const { tracks, availability } = useStudio();
  const copy = AVAILABILITY_COPY[availability];

  return (
    <header className="sticky top-0 z-30 border-b border-line/70 bg-paper/80 backdrop-blur-xl">
      <div className="flex h-[62px] items-center gap-3 px-4 sm:px-6 lg:px-8">
        <button
          type="button"
          onClick={onOpenMenu}
          aria-label="Open session panel"
          className="grid h-9 w-9 shrink-0 place-items-center rounded-full border border-line bg-surface/70 text-ink-2 transition hover:bg-surface lg:hidden"
        >
          <Icon name="menu" size={17} />
        </button>

        <div className="flex min-w-0 items-center gap-2.5 lg:hidden">
          <SunaMark size={24} className="shrink-0 text-accent" />
          <span className="truncate font-display text-[19px] leading-none text-ink">
            Suna Studio
          </span>
        </div>

        <div className="hidden min-w-0 items-center gap-2 lg:flex">
          <span className="font-mono text-[9px] uppercase tracking-[0.2em] text-faint">
            Studio
          </span>
          <span className="h-3 w-px bg-line" aria-hidden="true" />
          <span className="text-[11px] text-muted">
            {tracks.length === 0
              ? "A fresh session"
              : `${pluralise(tracks.length, "track")} in this session`}
          </span>
        </div>

        <div className="ml-auto flex shrink-0 items-center gap-2">
          <span
            className="inline-flex h-8 items-center gap-1.5 rounded-full border border-line bg-surface/60 px-2.5 text-[9.5px] text-muted"
            title="Suna's public Space status"
          >
            <span className={`h-1.5 w-1.5 rounded-full ${copy.dot}`} />
            <span>{copy.label}</span>
          </span>

          <a
            href={SUNA_SPACE_URL}
            target="_blank"
            rel="noreferrer"
            className="hidden h-8 items-center gap-1.5 rounded-full border border-line bg-surface/60 px-3 text-[9.5px] text-muted transition hover:bg-surface hover:text-ink sm:inline-flex"
          >
            Suna AI
            <Icon name="arrow-up-right" size={10} />
          </a>
        </div>
      </div>
    </header>
  );
}
