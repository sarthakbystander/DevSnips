import { useState } from "react";
import { Icon } from "./Icon";
import { PlayerSheet } from "./PlayerSheet";
import { Slider } from "./Slider";
import { SunaMark } from "./SunaMark";
import { TrackArtwork } from "./TrackArtwork";
import { formatTime } from "../lib/format";
import { getPreset } from "../lib/suna";
import { useStudio } from "../studio/StudioProvider";

export function PlayerBar() {
  const {
    tracks,
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
  } = useStudio();
  const [sheetOpen, setSheetOpen] = useState(false);

  const preset = currentTrack ? getPreset(currentTrack.presetId) : null;
  const maxDuration = duration || currentTrack?.duration || 1;
  const progress =
    maxDuration > 0 ? Math.min(100, (currentTime / maxDuration) * 100) : 0;
  const isDownloading = currentTrack
    ? downloadingId === currentTrack.id
    : false;
  const hasTrack = Boolean(currentTrack);

  const cover = (size: string) => (
    <span
      className={`relative shrink-0 overflow-hidden rounded-lg ring-1 ring-inset ring-white/10 ${size}`}
    >
      {currentTrack && preset ? (
        <TrackArtwork
          seed={currentTrack.id}
          palette={preset.palette}
          className="h-full w-full"
          playing={isPlaying}
        />
      ) : (
        <span className="grid h-full w-full place-items-center bg-white/[0.06]">
          <SunaMark size={18} className="text-cream/20" cut="#151220" />
        </span>
      )}
    </span>
  );

  return (
    <div
      role="region"
      aria-label="Music player"
      className="fixed inset-x-0 bottom-0 z-40 border-t border-white/10 bg-night text-cream shadow-player"
    >
      {/* Desktop transport */}
      <div className="hidden h-[84px] grid-cols-[minmax(0,1fr)_minmax(0,1.5fr)_minmax(0,1fr)] items-center gap-5 px-6 lg:grid">
        <div className="flex min-w-0 items-center gap-3">
          {cover("h-12 w-12")}
          <div className="min-w-0">
            <p className="truncate text-[11.5px] font-medium text-cream">
              {currentTrack ? currentTrack.title : "Nothing playing"}
            </p>
            <p className="mt-0.5 truncate text-[9px] text-cream/40">
              {currentTrack && preset
                ? `${preset.label} · Suna AI`
                : "Generate a track to begin"}
            </p>
          </div>
        </div>

        <div className="flex min-w-0 flex-col items-center gap-0.5">
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={playPrevious}
              disabled={!hasTrack || tracks.length < 2}
              aria-label="Previous track"
              className="grid h-8 w-8 place-items-center rounded-full text-cream/55 transition hover:bg-white/10 hover:text-cream disabled:opacity-25"
            >
              <Icon name="skip-back" size={15} />
            </button>
            <button
              type="button"
              onClick={togglePlay}
              disabled={!hasTrack}
              aria-label={isPlaying ? "Pause" : "Play"}
              className="grid h-9 w-9 place-items-center rounded-full bg-cream text-ink shadow transition hover:scale-[1.03] disabled:opacity-35"
            >
              <Icon name={isPlaying ? "pause" : "play"} size={16} />
            </button>
            <button
              type="button"
              onClick={playNext}
              disabled={!hasTrack || tracks.length < 2}
              aria-label="Next track"
              className="grid h-8 w-8 place-items-center rounded-full text-cream/55 transition hover:bg-white/10 hover:text-cream disabled:opacity-25"
            >
              <Icon name="skip-forward" size={15} />
            </button>
          </div>

          <div className="flex w-full max-w-[430px] items-center gap-2">
            <span className="w-8 text-right font-mono text-[8.5px] tabular-nums text-cream/35">
              {formatTime(currentTime)}
            </span>
            <Slider
              label="Seek within current track"
              value={currentTime}
              min={0}
              max={maxDuration}
              step={0.1}
              onChange={seek}
              disabled={!hasTrack}
              valueText={`${formatTime(currentTime)} of ${formatTime(
                maxDuration,
              )}`}
              dark
              className="flex-1"
            />
            <span className="w-8 font-mono text-[8.5px] tabular-nums text-cream/35">
              {formatTime(hasTrack ? maxDuration : 0)}
            </span>
          </div>
        </div>

        <div className="flex items-center justify-end gap-1.5">
          <button
            type="button"
            onClick={toggleMute}
            aria-label={muted ? "Unmute" : "Mute"}
            className="grid h-8 w-8 place-items-center rounded-full text-cream/55 transition hover:bg-white/10 hover:text-cream"
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
            className="w-[88px]"
          />
          <button
            type="button"
            onClick={() => currentTrack && downloadTrack(currentTrack)}
            disabled={!hasTrack || isDownloading}
            aria-label="Download current track"
            className="ml-1 grid h-8 w-8 place-items-center rounded-full text-cream/55 transition hover:bg-white/10 hover:text-cream disabled:opacity-25"
          >
            {isDownloading ? (
              <span className="h-3 w-3 animate-spin rounded-full border-[1.5px] border-cream/25 border-t-cream" />
            ) : (
              <Icon name="download" size={14} />
            )}
          </button>
        </div>
      </div>

      {/* Mobile mini player */}
      <div className="relative lg:hidden">
        <span className="absolute inset-x-0 top-0 h-[2px] bg-cream/10">
          <span
            className="block h-full bg-cream/75 transition-[width] duration-200"
            style={{ width: `${progress}%` }}
          />
        </span>
        <div className="flex items-center gap-2 px-3 pb-[calc(0.5rem+env(safe-area-inset-bottom))] pt-2">
          <button
            type="button"
            onClick={() => hasTrack && setSheetOpen(true)}
            disabled={!hasTrack}
            aria-label="Open now playing"
            className="flex min-w-0 flex-1 items-center gap-2.5 text-left disabled:cursor-default"
          >
            {cover("h-10 w-10")}
            <span className="min-w-0">
              <span className="block truncate text-[11px] font-medium text-cream">
                {currentTrack ? currentTrack.title : "Nothing playing"}
              </span>
              <span className="mt-0.5 block truncate text-[8.5px] text-cream/40">
                {currentTrack && preset
                  ? `${preset.label} · ${formatTime(currentTime)} / ${formatTime(
                      maxDuration,
                    )}`
                  : "Describe a track above"}
              </span>
            </span>
          </button>

          <button
            type="button"
            onClick={togglePlay}
            disabled={!hasTrack}
            aria-label={isPlaying ? "Pause" : "Play"}
            className="grid h-10 w-10 shrink-0 place-items-center rounded-full bg-cream text-ink disabled:opacity-35"
          >
            <Icon name={isPlaying ? "pause" : "play"} size={17} />
          </button>

          <button
            type="button"
            onClick={() => setSheetOpen(true)}
            disabled={!hasTrack}
            aria-label="Expand player"
            className="grid h-8 w-8 shrink-0 place-items-center rounded-full text-cream/50 transition hover:bg-white/10 hover:text-cream disabled:opacity-25"
          >
            <Icon name="expand" size={14} />
          </button>
        </div>
      </div>

      <PlayerSheet open={sheetOpen} onClose={() => setSheetOpen(false)} />
    </div>
  );
}
