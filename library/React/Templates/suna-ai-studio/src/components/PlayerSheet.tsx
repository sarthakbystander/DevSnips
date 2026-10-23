import { useEffect, useRef } from "react";
import { Icon } from "./Icon";
import { Slider } from "./Slider";
import { TrackArtwork } from "./TrackArtwork";
import { formatTime } from "../lib/format";
import { getPreset } from "../lib/suna";
import { useStudio } from "../studio/StudioProvider";

interface PlayerSheetProps {
  open: boolean;
  onClose: () => void;
}

export function PlayerSheet({ open, onClose }: PlayerSheetProps) {
  const {
    currentTrack,
    isPlaying,
    currentTime,
    duration,
    volume,
    muted,
    togglePlay,
    seek,
    setVolume,
    toggleMute,
    playNext,
    playPrevious,
    downloadTrack,
    downloadingId,
    tracks,
  } = useStudio();
  const dialogRef = useRef<HTMLDialogElement>(null);

  const preset = currentTrack ? getPreset(currentTrack.presetId) : null;
  const isDownloading = currentTrack
    ? downloadingId === currentTrack.id
    : false;

  useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) return;
    if (open && !dialog.open) dialog.showModal();
    else if (!open && dialog.open) dialog.close();
  }, [open]);

  useEffect(() => {
    if (!open) return;
    const previous = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = previous;
    };
  }, [open]);

  const maxDuration = duration || currentTrack?.duration || 1;

  return (
    <dialog
      ref={dialogRef}
      aria-labelledby="player-sheet-title"
      onClose={onClose}
      onCancel={(event) => {
        event.preventDefault();
        onClose();
      }}
      onClick={(event) => {
        if (event.target === event.currentTarget) onClose();
      }}
      className="fixed bottom-0 left-0 right-0 top-auto m-0 max-h-[92dvh] w-full max-w-none overflow-y-auto rounded-t-[28px] border-0 bg-night p-0 text-cream shadow-2xl sm:left-1/2 sm:right-auto sm:w-[440px] sm:max-w-[calc(100vw-2rem)] sm:-translate-x-1/2 sm:rounded-[28px] sm:bottom-4"
    >
      <div className="relative px-5 pb-[calc(1.25rem+env(safe-area-inset-bottom))] pt-3">
        <div className="mx-auto h-1 w-10 rounded-full bg-cream/20" />
        <div className="mt-3 flex items-center justify-between">
          <p className="text-[9px] font-semibold uppercase tracking-[0.18em] text-cream/45">
            Now playing
          </p>
          <button
            type="button"
            onClick={onClose}
            aria-label="Close now playing"
            className="grid h-8 w-8 place-items-center rounded-full text-cream/60 transition hover:bg-white/10 hover:text-cream"
          >
            <Icon name="close" size={16} />
          </button>
        </div>

        {currentTrack && preset ? (
          <>
            <div className="mx-auto mt-4 w-full max-w-[280px]">
              <TrackArtwork
                seed={currentTrack.id}
                palette={preset.palette}
                className="aspect-square w-full rounded-2xl ring-1 ring-inset ring-white/10"
                showLabel
                playing={isPlaying}
              />
            </div>

            <h2
              id="player-sheet-title"
              className="mt-5 text-balance font-display text-[30px] leading-[1.02] tracking-[-0.015em]"
            >
              {currentTrack.title}
            </h2>
            <p className="mt-1 text-[10px] text-cream/50">
              {preset.label} · Suna AI
            </p>
            <p className="mt-2 line-clamp-2 text-[10.5px] leading-4 text-cream/45">
              “{currentTrack.prompt}”
            </p>

            <div className="mt-5">
              <Slider
                label={`Seek within ${currentTrack.title}`}
                value={currentTime}
                min={0}
                max={maxDuration}
                step={0.1}
                onChange={seek}
                valueText={`${formatTime(currentTime)} of ${formatTime(
                  maxDuration,
                )}`}
                dark
              />
              <div className="mt-0.5 flex justify-between font-mono text-[9px] tabular-nums text-cream/40">
                <span>{formatTime(currentTime)}</span>
                <span>{formatTime(maxDuration)}</span>
              </div>
            </div>

            <div className="mt-2 flex items-center justify-center gap-5">
              <button
                type="button"
                onClick={playPrevious}
                disabled={tracks.length < 2}
                aria-label="Previous track"
                className="grid h-10 w-10 place-items-center rounded-full text-cream/65 transition hover:bg-white/10 hover:text-cream disabled:opacity-25"
              >
                <Icon name="skip-back" size={18} />
              </button>
              <button
                type="button"
                onClick={togglePlay}
                aria-label={isPlaying ? "Pause" : "Play"}
                className="grid h-14 w-14 place-items-center rounded-full bg-cream text-ink shadow-lg transition hover:scale-[1.03]"
              >
                <Icon name={isPlaying ? "pause" : "play"} size={21} />
              </button>
              <button
                type="button"
                onClick={playNext}
                disabled={tracks.length < 2}
                aria-label="Next track"
                className="grid h-10 w-10 place-items-center rounded-full text-cream/65 transition hover:bg-white/10 hover:text-cream disabled:opacity-25"
              >
                <Icon name="skip-forward" size={18} />
              </button>
            </div>

            <div className="mt-4 flex items-center gap-2 rounded-full bg-white/[0.04] px-3 py-2">
              <button
                type="button"
                onClick={toggleMute}
                aria-label={muted ? "Unmute" : "Mute"}
                className="text-cream/60 transition hover:text-cream"
              >
                <Icon name={muted ? "volume-off" : "volume"} size={15} />
              </button>
              <Slider
                label="Volume"
                value={muted ? 0 : volume}
                min={0}
                max={1}
                step={0.01}
                onChange={setVolume}
                valueText={`${Math.round((muted ? 0 : volume) * 100)} percent`}
                dark
                className="flex-1"
              />
              <span className="w-7 text-right font-mono text-[9px] text-cream/40">
                {Math.round((muted ? 0 : volume) * 100)}
              </span>
            </div>

            <div className="mt-3 flex gap-2">
              <button
                type="button"
                onClick={() => downloadTrack(currentTrack)}
                disabled={isDownloading}
                className="inline-flex h-10 flex-1 items-center justify-center gap-2 rounded-full border border-white/10 px-4 text-[11px] font-medium text-cream/85 transition hover:bg-white/10 disabled:opacity-50"
              >
                {isDownloading ? (
                  <span className="h-3.5 w-3.5 animate-spin rounded-full border-2 border-cream/25 border-t-cream" />
                ) : (
                  <Icon name="download" size={14} />
                )}
                Download track
              </button>
            </div>

            <details className="mt-4 border-t border-white/10 pt-3">
              <summary className="flex w-fit items-center gap-1.5 text-[8.5px] font-medium uppercase tracking-[0.14em] text-cream/35 transition hover:text-cream/60">
                <Icon name="wave" size={10} />
                Suna telemetry
              </summary>
              <p className="mt-1.5 font-mono text-[8.5px] leading-4 text-cream/40">
                {currentTrack.telemetry ||
                  "No telemetry was returned for this render."}
              </p>
            </details>
          </>
        ) : (
          <div className="py-10 text-center">
            <h2
              id="player-sheet-title"
              className="font-display text-2xl text-cream"
            >
              Nothing playing
            </h2>
            <p className="mt-1 text-[11px] text-cream/50">
              Generate a track, then press play.
            </p>
          </div>
        )}
      </div>
    </dialog>
  );
}
