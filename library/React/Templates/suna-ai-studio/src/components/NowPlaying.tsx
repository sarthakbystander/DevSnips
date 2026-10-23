import { Icon } from "./Icon";
import { SunaMark } from "./SunaMark";
import { TrackArtwork } from "./TrackArtwork";
import { formatTime } from "../lib/format";
import { focusComposer } from "../lib/focus";
import { getPreset, SUNA_MODEL_LABEL, SUNA_SPACE_URL } from "../lib/suna";
import { useStudio } from "../studio/StudioProvider";

const AVAILABILITY_COPY = {
  checking: {
    label: "Checking",
    detail: "Pinging Suna's public endpoint.",
    dot: "bg-gold animate-pulse-soft",
  },
  online: {
    label: "Reachable",
    detail: "The public Space is answering.",
    dot: "bg-sage",
  },
  offline: {
    label: "Unreachable",
    detail: "The Space may be asleep. Generation will try to wake it.",
    dot: "bg-accent",
  },
  unknown: {
    label: "Unknown",
    detail: "Status could not be checked from this browser.",
    dot: "bg-faint",
  },
} as const;

export function NowPlaying() {
  const {
    currentTrack,
    isPlaying,
    duration,
    togglePlay,
    downloadTrack,
    downloadingId,
    availability,
  } = useStudio();

  const preset = currentTrack ? getPreset(currentTrack.presetId) : null;
  const availabilityCopy = AVAILABILITY_COPY[availability];
  const isDownloading = currentTrack
    ? downloadingId === currentTrack.id
    : false;

  return (
    <div className="flex h-full flex-col">
      <section aria-labelledby="now-playing-title">
        <div className="flex items-center justify-between gap-2">
          <p className="text-[9px] font-semibold uppercase tracking-[0.18em] text-faint">
            Now playing
          </p>
          {currentTrack && (
            <span className="inline-flex items-center gap-1.5 rounded-full border border-line bg-surface/70 px-2 py-0.5 text-[8.5px] text-muted">
              <span
                className={`h-1 w-1 rounded-full ${
                  isPlaying ? "bg-sage" : "bg-faint"
                }`}
              />
              {isPlaying ? "Listening" : "Paused"}
            </span>
          )}
        </div>

        {currentTrack && preset ? (
          <>
            <button
              type="button"
              onClick={togglePlay}
              aria-label={
                isPlaying
                  ? `Pause ${currentTrack.title}`
                  : `Play ${currentTrack.title}`
              }
              className="group relative mt-3 block w-full overflow-hidden rounded-2xl ring-1 ring-inset ring-black/5"
            >
              <TrackArtwork
                seed={currentTrack.id}
                palette={preset.palette}
                className="aspect-square w-full"
                showLabel
                playing={isPlaying}
              />
              <span className="absolute inset-0 bg-ink/0 transition group-hover:bg-ink/15" />
              <span className="absolute bottom-3 right-3 grid h-9 w-9 place-items-center rounded-full bg-cream/95 text-ink shadow-lg transition group-hover:scale-[1.04]">
                <Icon name={isPlaying ? "pause" : "play"} size={15} />
              </span>
            </button>

            <h2
              id="now-playing-title"
              className="mt-4 text-balance font-display text-[27px] leading-[1.03] tracking-[-0.015em] text-ink"
            >
              {currentTrack.title}
            </h2>
            <p className="mt-1 text-[10px] text-muted">
              {preset.label} · {SUNA_MODEL_LABEL}
            </p>
            <p className="mt-2 line-clamp-3 text-[10.5px] leading-4 text-muted">
              “{currentTrack.prompt}”
            </p>

            <dl className="mt-4 grid grid-cols-2 gap-x-3 gap-y-2.5 border-y border-line py-3">
              <div>
                <dt className="text-[8px] uppercase tracking-[0.14em] text-faint">
                  Length
                </dt>
                <dd className="mt-0.5 font-mono text-[10.5px] text-ink-2">
                  {duration ? formatTime(duration) : "—"}
                </dd>
              </div>
              <div>
                <dt className="text-[8px] uppercase tracking-[0.14em] text-faint">
                  Requested
                </dt>
                <dd className="mt-0.5 font-mono text-[10.5px] text-ink-2">
                  {currentTrack.requestedDuration}s
                </dd>
              </div>
              <div>
                <dt className="text-[8px] uppercase tracking-[0.14em] text-faint">
                  Engine
                </dt>
                <dd className="mt-0.5 font-mono text-[10.5px] text-ink-2">
                  {currentTrack.quality === "fidelity" ? "16-STEP" : "TURBO"}
                </dd>
              </div>
              <div>
                <dt className="text-[8px] uppercase tracking-[0.14em] text-faint">
                  Format
                </dt>
                <dd className="mt-0.5 font-mono text-[10.5px] text-ink-2">
                  {currentTrack.mimeType.replace("audio/", "").toUpperCase()}
                </dd>
              </div>
            </dl>

            <div className="mt-3 flex gap-2">
              <button
                type="button"
                onClick={togglePlay}
                className="inline-flex h-9 flex-1 items-center justify-center gap-1.5 rounded-full bg-ink px-3 text-[10.5px] font-semibold text-cream transition hover:bg-ink-2"
              >
                <Icon name={isPlaying ? "pause" : "play"} size={12} />
                {isPlaying ? "Pause" : "Listen"}
              </button>
              <button
                type="button"
                onClick={() => downloadTrack(currentTrack)}
                disabled={isDownloading}
                className="inline-flex h-9 items-center justify-center gap-1.5 rounded-full border border-line bg-surface px-3 text-[10.5px] font-medium text-ink-2 transition hover:bg-surface-2 disabled:opacity-50"
              >
                {isDownloading ? (
                  <span className="h-3 w-3 animate-spin rounded-full border-[1.5px] border-faint/40 border-t-ink" />
                ) : (
                  <Icon name="download" size={12} />
                )}
                Download
              </button>
            </div>

            <details className="mt-3">
              <summary className="flex w-fit items-center gap-1.5 text-[8.5px] font-medium uppercase tracking-[0.14em] text-faint transition hover:text-muted">
                <Icon name="wave" size={10} />
                Suna telemetry
              </summary>
              <p className="mt-1.5 rounded-lg border border-line bg-surface/60 p-2 font-mono text-[8.5px] leading-4 text-muted">
                {currentTrack.telemetry ||
                  "No telemetry was returned for this render."}
              </p>
            </details>
          </>
        ) : (
          <>
            <div className="relative mt-3 grid aspect-square w-full place-items-center overflow-hidden rounded-2xl border border-line bg-surface-2">
              <div className="absolute h-[78%] w-[78%] rounded-full border border-line" />
              <div className="absolute h-[54%] w-[54%] rounded-full border border-line" />
              <div className="absolute h-[30%] w-[30%] rounded-full border border-line" />
              <SunaMark size={42} className="relative text-accent/85" />
              <span className="absolute bottom-3 left-3 font-mono text-[8px] uppercase tracking-[0.24em] text-faint">
                Suna Studio
              </span>
            </div>
            <h2
              id="now-playing-title"
              className="mt-4 font-display text-[27px] leading-[1.03] tracking-[-0.015em] text-ink"
            >
              A quiet studio
            </h2>
            <p className="mt-1.5 text-[10.5px] leading-4 text-muted">
              Your latest render appears here with its real duration, format,
              and Suna telemetry.
            </p>
            <button
              type="button"
              onClick={focusComposer}
              className="mt-3 inline-flex h-9 items-center gap-1.5 rounded-full bg-ink px-4 text-[10.5px] font-semibold text-cream transition hover:bg-ink-2"
            >
              <Icon name="sparkles" size={12} />
              Describe a track
            </button>
          </>
        )}
      </section>

      <div className="mt-auto space-y-3 pt-5">
        <a
          href={SUNA_SPACE_URL}
          target="_blank"
          rel="noreferrer"
          className="group block rounded-xl border border-line bg-surface/60 p-3 transition hover:border-line-strong hover:bg-surface"
        >
          <div className="flex items-center justify-between gap-2">
            <span className="flex items-center gap-1.5 text-[9px] font-medium text-ink-2">
              <span className={`h-1.5 w-1.5 rounded-full ${availabilityCopy.dot}`} />
              Suna Space · {availabilityCopy.label}
            </span>
            <Icon
              name="arrow-up-right"
              size={11}
              className="text-faint transition group-hover:text-ink"
            />
          </div>
          <p className="mt-1 text-[9px] leading-3.5 text-muted">
            {availabilityCopy.detail}
          </p>
        </a>

        <p className="px-0.5 text-[8.5px] leading-3.5 text-faint">
          Renders are session-only. Download a track to keep it beyond this
          tab. Audio URLs are served by the Space and may expire.
        </p>
      </div>
    </div>
  );
}
