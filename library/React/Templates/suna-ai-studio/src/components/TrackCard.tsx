import { useEffect, useRef, useState, type ReactNode } from "react";
import { Icon } from "./Icon";
import { Slider } from "./Slider";
import { TrackArtwork } from "./TrackArtwork";
import { copyText } from "../lib/clipboard";
import { formatTime } from "../lib/format";
import { getPreset } from "../lib/suna";
import { useStudio } from "../studio/StudioProvider";
import type { Track } from "../lib/types";

function durationLabel(track: Track): string {
  return track.duration ? formatTime(track.duration) : "—";
}

function MetaChip({
  children,
  mono = false,
}: {
  children: ReactNode;
  mono?: boolean;
}) {
  return (
    <span
      className={`inline-flex items-center gap-1 rounded-full border border-line bg-surface-2/80 px-2 py-0.5 text-[9.5px] text-muted ${
        mono ? "font-mono" : ""
      }`}
    >
      {children}
    </span>
  );
}

interface TrackCardProps {
  track: Track;
  featured?: boolean;
}

export function TrackCard({ track, featured = false }: TrackCardProps) {
  const {
    currentTrack,
    isPlaying,
    currentTime,
    duration,
    playTrack,
    togglePlay,
    selectTrack,
    seek,
    downloadTrack,
    downloadingId,
    removeTrack,
    renameTrack,
    notify,
  } = useStudio();
  const [editing, setEditing] = useState(false);
  const [draftTitle, setDraftTitle] = useState(track.title);
  const [copied, setCopied] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);
  const copyTimerRef = useRef<number | null>(null);

  const preset = getPreset(track.presetId);
  const isCurrent = currentTrack?.id === track.id;
  const isThisPlaying = isCurrent && isPlaying;
  const isDownloading = downloadingId === track.id;

  useEffect(() => {
    if (editing) {
      inputRef.current?.focus();
      inputRef.current?.select();
    }
  }, [editing]);

  useEffect(() => {
    return () => {
      if (copyTimerRef.current !== null) {
        window.clearTimeout(copyTimerRef.current);
      }
    };
  }, []);

  const handlePlay = () => {
    if (isCurrent) {
      togglePlay();
    } else {
      playTrack(track);
    }
  };

  const saveTitle = () => {
    const clean = draftTitle.trim();
    if (clean && clean !== track.title) {
      renameTrack(track.id, clean);
      notify("Track renamed for this session.", "success");
    } else {
      setDraftTitle(track.title);
    }
    setEditing(false);
  };

  const handleCopy = async () => {
    const success = await copyText(track.prompt);
    if (success) {
      setCopied(true);
      if (copyTimerRef.current !== null) {
        window.clearTimeout(copyTimerRef.current);
      }
      copyTimerRef.current = window.setTimeout(() => setCopied(false), 1800);
    } else {
      notify("The prompt couldn't be copied.", "error");
    }
  };

  if (!featured) {
    return (
      <article className="group flex items-center gap-2.5 rounded-xl px-1.5 py-1.5 transition hover:bg-surface/75">
        <button
          type="button"
          onClick={handlePlay}
          aria-label={
            isThisPlaying ? `Pause ${track.title}` : `Play ${track.title}`
          }
          className="relative h-11 w-11 shrink-0 overflow-hidden rounded-[10px] ring-1 ring-inset ring-black/5"
        >
          <TrackArtwork
            seed={track.id}
            palette={preset.palette}
            className="h-full w-full"
            playing={isThisPlaying}
          />
          <span
            className={`absolute inset-0 grid place-items-center bg-ink/35 text-cream transition ${
              isThisPlaying ? "opacity-100" : "opacity-0 group-hover:opacity-100"
            }`}
          >
            <Icon name={isThisPlaying ? "pause" : "play"} size={14} />
          </span>
        </button>

        <button
          type="button"
          onClick={() => selectTrack(track)}
          className="min-w-0 flex-1 text-left"
        >
          <span className="block truncate text-[12px] font-medium text-ink">
            {track.title}
          </span>
          <span className="mt-0.5 block truncate text-[9.5px] text-muted">
            {preset.label} · {durationLabel(track)}
          </span>
        </button>

        {isCurrent && (
          <span
            className="mr-1 flex h-4 items-end gap-[2px] text-accent"
            aria-label={isPlaying ? "Playing" : "Selected"}
          >
            <span
              className={`h-1.5 w-[2px] rounded-full bg-current ${
                isPlaying ? "animate-equalize origin-bottom" : ""
              }`}
            />
            <span
              className={`h-3 w-[2px] rounded-full bg-current ${
                isPlaying
                  ? "animate-equalize origin-bottom [animation-delay:120ms]"
                  : ""
              }`}
            />
            <span
              className={`h-2 w-[2px] rounded-full bg-current ${
                isPlaying
                  ? "animate-equalize origin-bottom [animation-delay:240ms]"
                  : ""
              }`}
            />
          </span>
        )}

        <button
          type="button"
          onClick={() => downloadTrack(track)}
          disabled={isDownloading}
          aria-label={`Download ${track.title}`}
          className="grid h-8 w-8 shrink-0 place-items-center rounded-full text-faint transition hover:bg-surface hover:text-ink disabled:opacity-50"
        >
          {isDownloading ? (
            <span className="h-3 w-3 animate-spin rounded-full border-[1.5px] border-faint/40 border-t-ink" />
          ) : (
            <Icon name="download" size={13} />
          )}
        </button>
        <button
          type="button"
          onClick={() => removeTrack(track.id)}
          aria-label={`Remove ${track.title} from session`}
          className="grid h-8 w-8 shrink-0 place-items-center rounded-full text-faint opacity-0 transition hover:bg-surface hover:text-accent-deep focus-visible:opacity-100 group-hover:opacity-100"
        >
          <Icon name="trash" size={13} />
        </button>
      </article>
    );
  }

  return (
    <article className="animate-fade-up overflow-hidden rounded-[26px] border border-line bg-surface p-4 shadow-card sm:p-5">
      <div className="flex gap-3.5 sm:gap-5">
        <div className="relative w-[108px] shrink-0 sm:w-[190px]">
          <TrackArtwork
            seed={track.id}
            palette={preset.palette}
            className="aspect-square w-full rounded-2xl ring-1 ring-inset ring-black/5"
            showLabel
            playing={isThisPlaying}
          />
          <button
            type="button"
            onClick={handlePlay}
            aria-label={
              isThisPlaying ? `Pause ${track.title}` : `Play ${track.title}`
            }
            className="absolute bottom-2.5 left-2.5 grid h-10 w-10 place-items-center rounded-full bg-cream/95 text-ink shadow-lg backdrop-blur transition hover:scale-[1.04] hover:bg-white sm:h-12 sm:w-12"
          >
            <Icon name={isThisPlaying ? "pause" : "play"} size={18} />
          </button>
        </div>

        <div className="min-w-0 flex-1">
          <div className="flex items-start justify-between gap-2">
            <div className="min-w-0">
              <p className="text-[9px] font-semibold uppercase tracking-[0.18em] text-accent-deep">
                New track · {preset.label}
              </p>
              {editing ? (
                <input
                  ref={inputRef}
                  value={draftTitle}
                  onChange={(event) => setDraftTitle(event.target.value)}
                  onBlur={saveTitle}
                  onKeyDown={(event) => {
                    if (event.key === "Enter") {
                      event.preventDefault();
                      saveTitle();
                    }
                    if (event.key === "Escape") {
                      setDraftTitle(track.title);
                      setEditing(false);
                    }
                  }}
                  maxLength={80}
                  aria-label="Track title"
                  className="mt-1 w-full rounded-md border border-line-strong bg-surface px-1.5 py-0.5 font-display text-[22px] leading-tight text-ink focus:outline-none sm:text-[28px]"
                />
              ) : (
                <h3 className="mt-0.5 truncate font-display text-[23px] leading-tight tracking-[-0.015em] text-ink sm:text-[30px]">
                  {track.title}
                </h3>
              )}
            </div>
            <button
              type="button"
              onClick={() => {
                setDraftTitle(track.title);
                setEditing(true);
              }}
              aria-label={`Rename ${track.title}`}
              className="grid h-7 w-7 shrink-0 place-items-center rounded-full text-faint transition hover:bg-surface-2 hover:text-ink"
            >
              <Icon name="pencil" size={12} />
            </button>
          </div>

          <p className="mt-1 line-clamp-2 text-[10.5px] leading-4 text-muted sm:text-[11.5px] sm:leading-5">
            “{track.prompt}”
          </p>

          <div className="mt-2 flex flex-wrap gap-1 sm:mt-3">
            <MetaChip mono>
              <Icon name="clock" size={10} /> {durationLabel(track)}
            </MetaChip>
            <MetaChip>{preset.shortLabel}</MetaChip>
            <MetaChip mono>
              {track.quality === "fidelity" ? "16-STEP" : "TURBO"}
            </MetaChip>
            {track.vocalName && <MetaChip>Vocal</MetaChip>}
          </div>

          {isCurrent && (
            <div className="mt-3">
              <Slider
                label={`Seek within ${track.title}`}
                value={currentTime}
                min={0}
                max={duration || track.duration || 1}
                step={0.1}
                onChange={seek}
                valueText={`${formatTime(currentTime)} of ${formatTime(
                  duration || track.duration,
                )}`}
              />
              <div className="flex justify-between font-mono text-[9px] tabular-nums text-faint">
                <span>{formatTime(currentTime)}</span>
                <span>{formatTime(duration || track.duration)}</span>
              </div>
            </div>
          )}

          <div className="mt-3 flex flex-wrap items-center gap-1.5">
            <button
              type="button"
              onClick={handlePlay}
              className="inline-flex h-8 items-center gap-1.5 rounded-full bg-ink px-3 text-[10.5px] font-semibold text-cream transition hover:bg-ink-2"
            >
              <Icon name={isThisPlaying ? "pause" : "play"} size={12} />
              {isThisPlaying ? "Pause" : "Listen"}
            </button>
            <button
              type="button"
              onClick={() => downloadTrack(track)}
              disabled={isDownloading}
              className="inline-flex h-8 items-center gap-1.5 rounded-full border border-line bg-surface px-2.5 text-[10.5px] font-medium text-ink-2 transition hover:bg-surface-2 disabled:opacity-50"
            >
              {isDownloading ? (
                <span className="h-3 w-3 animate-spin rounded-full border-[1.5px] border-faint/40 border-t-ink" />
              ) : (
                <Icon name="download" size={12} />
              )}
              Download
            </button>
            <button
              type="button"
              onClick={handleCopy}
              className="inline-flex h-8 items-center gap-1.5 rounded-full border border-line bg-surface px-2.5 text-[10.5px] font-medium text-ink-2 transition hover:bg-surface-2"
            >
              <Icon name={copied ? "check" : "copy"} size={12} />
              {copied ? "Copied" : "Copy prompt"}
            </button>
            <button
              type="button"
              onClick={() => removeTrack(track.id)}
              aria-label={`Remove ${track.title} from session`}
              className="ml-auto grid h-8 w-8 place-items-center rounded-full text-faint transition hover:bg-surface-2 hover:text-accent-deep"
            >
              <Icon name="trash" size={13} />
            </button>
          </div>
        </div>
      </div>

      <details className="mt-3 border-t border-line/80 pt-2.5 sm:mt-4">
        <summary className="flex w-fit items-center gap-1.5 text-[9px] font-medium uppercase tracking-[0.14em] text-faint transition hover:text-muted">
          <Icon name="wave" size={11} />
          Suna telemetry
        </summary>
        <p className="mt-1.5 font-mono text-[9.5px] leading-4 text-muted">
          {track.telemetry || "No telemetry was returned for this render."}
        </p>
        <p className="mt-1 font-mono text-[8.5px] leading-4 text-faint">
          Requested {track.requestedDuration}s · {track.mimeType} ·{" "}
          {track.fileName}
        </p>
        {track.lyrics && (
          <>
            <p className="mt-2.5 text-[9px] font-medium uppercase tracking-[0.14em] text-faint">
              Sung lyric sheet
            </p>
            <pre className="mt-1 max-h-48 overflow-auto whitespace-pre-wrap font-mono text-[9.5px] leading-4 text-muted">
              {track.lyrics}
            </pre>
          </>
        )}
      </details>
    </article>
  );
}
