import { useEffect, useState } from "react";
import { Icon } from "./Icon";
import { SunaMark } from "./SunaMark";
import { TrackArtwork } from "./TrackArtwork";
import { formatTime } from "../lib/format";
import { getPreset, SUNA_SPACE_URL } from "../lib/suna";
import { useStudio } from "../studio/StudioProvider";
import type { Track } from "../lib/types";

const DEVSNIPS_URL = "https://github.com/sarthakbystander/DevSnips";

const AVAILABILITY_COPY = {
  checking: { label: "Checking Suna", dot: "bg-gold animate-pulse-soft" },
  online: { label: "Suna is reachable", dot: "bg-sage" },
  offline: { label: "Suna is unreachable", dot: "bg-accent" },
  unknown: { label: "Suna status unknown", dot: "bg-faint" },
} as const;

function SidebarTrack({
  track,
  onSelect,
}: {
  track: Track;
  onSelect?: () => void;
}) {
  const {
    currentTrack,
    isPlaying,
    playTrack,
    togglePlay,
  } = useStudio();
  const preset = getPreset(track.presetId);
  const isCurrent = currentTrack?.id === track.id;
  const isThisPlaying = isCurrent && isPlaying;

  return (
    <button
      type="button"
      onClick={() => {
        if (isCurrent) togglePlay();
        else playTrack(track);
        onSelect?.();
      }}
      aria-label={
        isThisPlaying ? `Pause ${track.title}` : `Play ${track.title}`
      }
      aria-current={isCurrent ? "true" : undefined}
      className={`group flex w-full items-center gap-2.5 rounded-xl px-2 py-1.5 text-left transition ${
        isCurrent
          ? "bg-surface shadow-sm ring-1 ring-line"
          : "hover:bg-surface/70"
      }`}
    >
      <span className="relative h-9 w-9 shrink-0 overflow-hidden rounded-lg ring-1 ring-inset ring-black/5">
        <TrackArtwork
          seed={track.id}
          palette={preset.palette}
          className="h-full w-full"
        />
        <span
          className={`absolute inset-0 grid place-items-center bg-ink/25 text-cream transition ${
            isThisPlaying ? "opacity-100" : "opacity-0 group-hover:opacity-100"
          }`}
        >
          <Icon name={isThisPlaying ? "pause" : "play"} size={12} />
        </span>
      </span>

      <span className="min-w-0 flex-1">
        <span
          className={`block truncate text-[11px] font-medium ${
            isCurrent ? "text-ink" : "text-ink-2"
          }`}
        >
          {track.title}
        </span>
        <span className="mt-0.5 block truncate text-[8.5px] text-muted">
          {preset.shortLabel} ·{" "}
          {track.duration ? formatTime(track.duration) : "—"}
        </span>
      </span>

      {isThisPlaying && (
        <span className="mr-0.5 flex h-3 items-end gap-[2px] text-accent">
          <span className="h-1 w-[2px] origin-bottom animate-equalize rounded-full bg-current" />
          <span className="h-2.5 w-[2px] origin-bottom animate-equalize rounded-full bg-current [animation-delay:120ms]" />
          <span className="h-1.5 w-[2px] origin-bottom animate-equalize rounded-full bg-current [animation-delay:240ms]" />
        </span>
      )}
    </button>
  );
}

interface SidebarContentProps {
  onNewTrack: () => void;
  onClose?: () => void;
  onNavigate?: () => void;
}

export function SidebarContent({
  onNewTrack,
  onClose,
  onNavigate,
}: SidebarContentProps) {
  const { tracks, availability, clearTracks } = useStudio();
  const [confirmClear, setConfirmClear] = useState(false);
  const availabilityCopy = AVAILABILITY_COPY[availability];

  useEffect(() => {
    if (!confirmClear) return;
    const timer = window.setTimeout(() => setConfirmClear(false), 3500);
    return () => window.clearTimeout(timer);
  }, [confirmClear]);

  const handleNewTrack = () => {
    onNewTrack();
    onNavigate?.();
  };

  return (
    <div className="flex h-full flex-col bg-paper">
      <div className="flex items-center justify-between gap-2 px-4 pb-1 pt-5">
        <button
          type="button"
          onClick={handleNewTrack}
          className="flex min-w-0 items-center gap-2.5 text-left"
          aria-label="Suna Studio — start a new track"
        >
          <SunaMark size={30} className="shrink-0 text-accent" />
          <span className="min-w-0">
            <span className="block truncate font-display text-[20px] leading-none tracking-[-0.01em] text-ink">
              Suna Studio
            </span>
            <span className="mt-1 block text-[8px] uppercase tracking-[0.2em] text-faint">
              A DevSnips template
            </span>
          </span>
        </button>
        {onClose && (
          <button
            type="button"
            onClick={onClose}
            aria-label="Close session panel"
            className="grid h-8 w-8 shrink-0 place-items-center rounded-full text-muted transition hover:bg-surface hover:text-ink"
          >
            <Icon name="close" size={16} />
          </button>
        )}
      </div>

      <div className="px-3 pt-4">
        <button
          type="button"
          onClick={handleNewTrack}
          className="flex h-10 w-full items-center justify-center gap-2 rounded-xl bg-ink px-3 text-[11.5px] font-semibold text-cream shadow-sm transition hover:bg-ink-2"
        >
          <Icon name="plus" size={14} />
          New track
        </button>
      </div>

      <div className="mt-6 flex items-center justify-between px-4">
        <h2 className="text-[9px] font-semibold uppercase tracking-[0.18em] text-faint">
          This session
        </h2>
        <span className="font-mono text-[9px] text-faint">
          {String(tracks.length).padStart(2, "0")}
        </span>
      </div>

      <div className="-mx-1 mt-2 flex-1 overflow-y-auto px-2 pb-2">
        {tracks.length === 0 ? (
          <div className="mx-2 mt-1 rounded-xl border border-dashed border-line-strong px-3 py-5 text-center">
            <SunaMark size={22} className="mx-auto text-line-strong" />
            <p className="mt-2 text-[10.5px] font-medium text-muted">
              No tracks yet
            </p>
            <p className="mt-0.5 text-[9px] leading-3.5 text-faint">
              Your session appears here. Nothing is stored after you leave.
            </p>
          </div>
        ) : (
          <div className="space-y-0.5">
            {tracks.map((track) => (
              <SidebarTrack
                key={track.id}
                track={track}
                onSelect={onNavigate}
              />
            ))}
          </div>
        )}
      </div>

      {tracks.length > 0 && (
        <div className="px-4 pb-2">
          {confirmClear ? (
            <div className="flex items-center gap-2 rounded-lg border border-accent/20 bg-accent-soft/50 px-2 py-1.5">
              <span className="flex-1 text-[9px] text-accent-deep">
                Clear the session?
              </span>
              <button
                type="button"
                onClick={() => {
                  clearTracks();
                  setConfirmClear(false);
                }}
                className="rounded-full bg-accent px-2 py-0.5 text-[9px] font-semibold text-white"
              >
                Clear
              </button>
              <button
                type="button"
                onClick={() => setConfirmClear(false)}
                className="text-[9px] text-accent-deep/75"
              >
                Keep
              </button>
            </div>
          ) : (
            <button
              type="button"
              onClick={() => setConfirmClear(true)}
              className="text-[9px] font-medium text-faint transition hover:text-ink"
            >
              Clear session
            </button>
          )}
        </div>
      )}

      <div className="mt-auto border-t border-line/80 px-4 pb-4 pt-3">
        <a
          href={SUNA_SPACE_URL}
          target="_blank"
          rel="noreferrer"
          className="flex items-center justify-between gap-2 rounded-xl border border-line bg-surface/70 px-2.5 py-2 transition hover:border-line-strong hover:bg-surface"
        >
          <span className="flex min-w-0 items-center gap-2">
            <span className={`h-1.5 w-1.5 shrink-0 rounded-full ${availabilityCopy.dot}`} />
            <span className="min-w-0">
              <span className="block truncate text-[10px] font-medium text-ink-2">
                Suna AI
              </span>
              <span className="block truncate text-[8.5px] text-muted">
                {availabilityCopy.label}
              </span>
            </span>
          </span>
          <Icon name="arrow-up-right" size={11} className="shrink-0 text-faint" />
        </a>

        <p className="mt-2.5 px-0.5 text-[8.5px] leading-3.5 text-faint">
          Audio is rendered on Suna's public Hugging Face Space. Tracks live in
          this tab only — download the ones you keep.
        </p>

        <div className="mt-2.5 flex items-center justify-between gap-2 px-0.5">
          <a
            href={DEVSNIPS_URL}
            target="_blank"
            rel="noreferrer"
            className="text-[8px] uppercase tracking-[0.12em] text-faint transition hover:text-muted"
          >
            DevSnips × Suna AI
          </a>
          <span className="font-mono text-[8px] text-faint">48 kHz</span>
        </div>
      </div>
    </div>
  );
}

export function Sidebar({ onNewTrack }: { onNewTrack: () => void }) {
  return (
    <aside className="sticky top-0 hidden h-[calc(100dvh-84px)] w-[244px] shrink-0 border-r border-line/80 lg:block">
      <SidebarContent onNewTrack={onNewTrack} />
    </aside>
  );
}
