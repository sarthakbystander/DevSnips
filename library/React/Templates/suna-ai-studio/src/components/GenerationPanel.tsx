import { useEffect, useRef, useState } from "react";
import { Icon } from "./Icon";
import { paletteGradient } from "../lib/palettes";
import { formatTime } from "../lib/format";
import { focusComposer } from "../lib/focus";
import { getPreset } from "../lib/suna";
import { useStudio } from "../studio/StudioProvider";

function useElapsed(startedAt: number | undefined, active: boolean) {
  const [now, setNow] = useState(() => Date.now());

  useEffect(() => {
    if (!active || !startedAt) return;
    setNow(Date.now());
    const timer = window.setInterval(() => setNow(Date.now()), 1000);
    return () => window.clearInterval(timer);
  }, [active, startedAt]);

  if (!startedAt) return "0:00";
  return formatTime(Math.max(0, (now - startedAt) / 1000));
}

const ACTIVE_COPY: Record<
  "connecting" | "submitting" | "working" | "queued" | "rendering",
  { label: string; detail: string }
> = {
  connecting: {
    label: "Connecting to Suna",
    detail: "Waking the public Space. The first visit can take a moment.",
  },
  submitting: {
    label: "Sending your prompt",
    detail: "Handing your idea and settings to Suna.",
  },
  working: {
    label: "Suna is composing",
    detail: "Rendering on the Space. This can take a minute or two.",
  },
  queued: {
    label: "Waiting for Suna",
    detail: "The public GPU is busy. Your track will start as soon as it is free.",
  },
  rendering: {
    label: "Rendering audio",
    detail: "Suna is turning the arrangement into a stereo track.",
  },
};

export function GenerationPanel() {
  const {
    generation,
    isGenerating,
    cancelGeneration,
    retryGeneration,
    dismissGeneration,
  } = useStudio();
  const panelRef = useRef<HTMLElement>(null);
  const elapsed = useElapsed(generation.startedAt, isGenerating);
  const preset = generation.presetId ? getPreset(generation.presetId) : null;

  useEffect(() => {
    if (!isGenerating) return;
    const timer = window.setTimeout(() => {
      panelRef.current?.scrollIntoView({
        behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches
          ? "auto"
          : "smooth",
        block: "nearest",
      });
    }, 350);
    return () => window.clearTimeout(timer);
  }, [isGenerating]);

  if (
    generation.stage === "idle" ||
    generation.stage === "complete" ||
    !generation.prompt
  ) {
    return null;
  }

  if (generation.stage === "error" && generation.error) {
    return (
      <section
        ref={panelRef}
        role="alert"
        className="mt-4 animate-fade-up overflow-hidden rounded-[24px] border border-accent/30 bg-accent-soft/45 shadow-card"
      >
        <div className="flex gap-3.5 p-4 sm:p-5">
          <span className="grid h-9 w-9 shrink-0 place-items-center rounded-full bg-surface text-accent-deep">
            <Icon name="alert" size={17} />
          </span>
          <div className="min-w-0 flex-1">
            <p className="text-[10px] font-semibold uppercase tracking-[0.16em] text-accent-deep">
              {generation.error.title}
            </p>
            <p className="mt-1 text-[13px] leading-5 text-ink">
              {generation.error.message}
            </p>
            <p className="mt-2 line-clamp-2 text-[11px] leading-4 text-ink-2/70">
              “{generation.prompt}”
            </p>
            {generation.error.detail && (
              <details className="mt-2">
                <summary className="w-fit text-[10px] font-medium text-accent-deep/80 underline decoration-accent/30 underline-offset-2">
                  Technical details
                </summary>
                <pre className="mt-1.5 max-h-24 overflow-auto whitespace-pre-wrap break-words rounded-lg bg-surface/70 p-2 font-mono text-[9px] leading-4 text-ink-2/75">
                  {generation.error.detail}
                </pre>
              </details>
            )}
            <div className="mt-3 flex flex-wrap items-center gap-2">
              <button
                type="button"
                onClick={retryGeneration}
                className="inline-flex h-9 items-center gap-1.5 rounded-full bg-ink px-3.5 text-[11px] font-semibold text-cream transition hover:bg-ink-2"
              >
                <Icon name="rotate" size={13} />
                Try again
              </button>
              <button
                type="button"
                onClick={focusComposer}
                className="inline-flex h-9 items-center gap-1.5 rounded-full border border-line-strong bg-surface px-3.5 text-[11px] font-medium text-ink-2 transition hover:bg-surface-2"
              >
                <Icon name="pencil" size={12} />
                Edit prompt
              </button>
              <button
                type="button"
                onClick={dismissGeneration}
                className="ml-auto text-[10px] font-medium text-accent-deep/70 underline decoration-accent/25 underline-offset-2 transition hover:text-accent-deep"
              >
                Dismiss
              </button>
            </div>
          </div>
        </div>
      </section>
    );
  }

  if (generation.stage === "cancelled") {
    return (
      <section
        ref={panelRef}
        className="mt-4 flex items-center gap-3 rounded-2xl border border-line bg-surface-2/75 px-4 py-3 animate-fade-up"
      >
        <span className="grid h-7 w-7 shrink-0 place-items-center rounded-full bg-surface text-muted ring-1 ring-line">
          <Icon name="stop" size={12} />
        </span>
        <p className="flex-1 text-[11.5px] text-muted">
          Generation cancelled. Your prompt is still in the composer.
        </p>
        <button
          type="button"
          onClick={retryGeneration}
          className="rounded-full border border-line-strong bg-surface px-2.5 py-1 text-[10px] font-medium text-ink-2 transition hover:bg-surface"
        >
          Try again
        </button>
        <button
          type="button"
          onClick={dismissGeneration}
          aria-label="Dismiss cancelled message"
          className="grid h-7 w-7 place-items-center rounded-full text-muted transition hover:bg-surface hover:text-ink"
        >
          <Icon name="close" size={13} />
        </button>
      </section>
    );
  }

  const stage = generation.stage as keyof typeof ACTIVE_COPY;
  const copy = ACTIVE_COPY[stage] ?? ACTIVE_COPY.working;
  const queueDetail =
    generation.stage === "queued" && generation.position !== undefined
      ? `Position ${generation.position} in Suna's queue.`
      : copy.detail;

  return (
    <section
      ref={panelRef}
      role="status"
      aria-live="polite"
      aria-busy="true"
      className="mt-4 animate-fade-up overflow-hidden rounded-[24px] border border-line bg-surface shadow-card"
    >
      <div className="flex gap-3.5 p-4 sm:p-5">
        <div
          className="relative grid h-[76px] w-[76px] shrink-0 place-items-center overflow-hidden rounded-2xl ring-1 ring-inset ring-black/5"
          style={{ background: paletteGradient(preset?.palette ?? "sun") }}
          aria-hidden="true"
        >
          <div className="paper-grain pointer-events-none absolute inset-0 opacity-20 mix-blend-overlay" />
          <span className="absolute h-12 w-12 rounded-full border border-white/35" />
          <span className="absolute h-12 w-12 animate-orbit rounded-full border border-transparent border-t-white/90" />
          <span className="h-2 w-2 rounded-full bg-white/90 shadow-[0_0_16px_rgba(255,255,255,0.55)]" />
        </div>

        <div className="min-w-0 flex-1">
          <div className="flex items-center gap-2">
            <span className="relative flex h-1.5 w-1.5">
              <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-accent opacity-40" />
              <span className="relative inline-flex h-1.5 w-1.5 rounded-full bg-accent" />
            </span>
            <p className="text-[10px] font-semibold uppercase tracking-[0.16em] text-accent-deep">
              {copy.label}
            </p>
            <span className="ml-auto font-mono text-[10px] tabular-nums text-faint">
              {elapsed}
            </span>
          </div>

          <p className="mt-1.5 line-clamp-2 text-[13px] font-medium leading-5 text-ink">
            {generation.prompt}
          </p>
          <p className="mt-1 text-[11px] leading-4 text-muted">{queueDetail}</p>
        </div>
      </div>

      <div className="flex flex-wrap items-center justify-between gap-2 border-t border-line bg-surface-2/55 px-4 py-2.5 sm:px-5">
        <p className="flex items-center gap-1.5 text-[10px] text-muted">
          <Icon name="info" size={12} className="shrink-0 text-faint" />
          Suna does not expose a progress percentage. The timer is real.
        </p>
        <button
          type="button"
          onClick={cancelGeneration}
          className="inline-flex h-7 items-center gap-1.5 rounded-full border border-line-strong bg-surface px-2.5 text-[10px] font-medium text-ink-2 transition hover:bg-surface-2"
        >
          <Icon name="stop" size={10} />
          Cancel
        </button>
      </div>
    </section>
  );
}
