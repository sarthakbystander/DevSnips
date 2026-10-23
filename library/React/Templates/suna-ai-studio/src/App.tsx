import { useState } from "react";
import { Composer } from "./components/Composer";
import { GenerationPanel } from "./components/GenerationPanel";
import { Icon } from "./components/Icon";
import { MobileDrawer } from "./components/MobileDrawer";
import { NowPlaying } from "./components/NowPlaying";
import { PlayerBar } from "./components/PlayerBar";
import { Sidebar } from "./components/Sidebar";
import { SunaMark } from "./components/SunaMark";
import { TopBar } from "./components/TopBar";
import { TrackCard } from "./components/TrackCard";
import { focusComposer } from "./lib/focus";
import { pluralise } from "./lib/format";
import {
  SUNA_MODEL_LABEL,
  SUNA_SPACE_URL,
  SUNA_SPACE_ID,
} from "./lib/suna";
import type { Track } from "./lib/types";
import { useStudio } from "./studio/StudioProvider";

const DEVSNIPS_URL = "https://github.com/sarthakbystander/DevSnips";
const SUNA_SITE_URL = "https://suna.jjcoders.com";

function Hero() {
  return (
    <section className="pt-7 sm:pt-9 lg:pt-10">
      <div className="flex flex-wrap items-center gap-2">
        <span className="inline-flex items-center gap-1.5 rounded-full border border-line bg-surface/70 px-2.5 py-1 text-[8.5px] font-semibold uppercase tracking-[0.16em] text-muted">
          <span className="h-1 w-1 rounded-full bg-accent" />
          {SUNA_MODEL_LABEL} · Live Space
        </span>
        <span className="text-[9px] uppercase tracking-[0.14em] text-faint">
          A DevSnips template
        </span>
      </div>

      <h1 className="mt-4 max-w-[630px] text-balance font-display text-[42px] leading-[0.96] tracking-[-0.02em] text-ink sm:text-[54px] lg:text-[58px]">
        Start with a <em className="text-accent-deep">feeling.</em>
      </h1>
      <p className="mt-3.5 max-w-[520px] text-[13px] leading-6 text-muted sm:text-[14px]">
        Describe the track in your head. Suna AI renders it on its public
        Space as a real stereo file — then it is yours to play, shape, and keep.
      </p>

      <div className="mt-4 flex flex-wrap items-center gap-x-4 gap-y-2 text-[9.5px] text-faint">
        <span className="inline-flex items-center gap-1.5">
          <Icon name="wave" size={12} className="text-accent" />
          Real Suna render
        </span>
        <span className="inline-flex items-center gap-1.5">
          <Icon name="link" size={11} className="text-muted" />
          Public Space · no account
        </span>
        <span className="inline-flex items-center gap-1.5">
          <Icon name="clock" size={11} className="text-muted" />
          Session-only
        </span>
      </div>
    </section>
  );
}

function EmptySession() {
  return (
    <div className="mt-4 overflow-hidden rounded-[26px] border border-dashed border-line-strong bg-surface/35 p-6 sm:p-8">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center">
        <div className="grid h-16 w-16 shrink-0 place-items-center rounded-2xl bg-accent-soft/55 text-accent-deep">
          <SunaMark size={38} cut="#ECE6FD" />
        </div>
        <div>
          <h3 className="font-display text-[25px] leading-tight text-ink">
            The room is quiet.
          </h3>
          <p className="mt-1 max-w-[430px] text-[11.5px] leading-5 text-muted">
            Describe a track above and Suna will render it here, with its real
            duration, format, and telemetry. Nothing is stored after you leave
            this tab.
          </p>
        </div>
      </div>
      <div className="mt-5 flex flex-wrap gap-1.5">
        {["24–68s songs", "6 artist presets", "Editable lyrics", "MP3 + WAV masters"].map(
          (item) => (
            <span
              key={item}
              className="rounded-full border border-line bg-surface/70 px-2.5 py-1 text-[9px] text-muted"
            >
              {item}
            </span>
          ),
        )}
      </div>
    </div>
  );
}

function SessionFeed({ tracks }: { tracks: Track[] }) {
  const [featured, ...earlier] = tracks;

  return (
    <section aria-labelledby="session-heading" className="mt-10 sm:mt-12">
      <div className="flex items-end justify-between gap-4">
        <div>
          <p className="text-[9px] font-semibold uppercase tracking-[0.18em] text-faint">
            This session
          </p>
          <h2
            id="session-heading"
            className="mt-1 font-display text-[27px] leading-none tracking-[-0.015em] text-ink"
          >
            Your tracks
          </h2>
        </div>
        <span className="pb-0.5 text-[9px] text-faint">
          {tracks.length > 0
            ? `${pluralise(tracks.length, "render")} · newest first`
            : "Nothing rendered yet"}
        </span>
      </div>

      {tracks.length === 0 ? (
        <EmptySession />
      ) : (
        <div className="mt-4 space-y-3">
          {featured && <TrackCard track={featured} featured />}
          {earlier.length > 0 && (
            <div className="rounded-2xl border border-line bg-surface/45 p-1.5">
              <p className="px-2 pb-1 pt-1.5 text-[8.5px] font-semibold uppercase tracking-[0.16em] text-faint">
                Earlier in this session
              </p>
              <div className="divide-y divide-line/60">
                {earlier.map((track) => (
                  <TrackCard key={track.id} track={track} />
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </section>
  );
}

function Footer() {
  return (
    <footer className="mt-12 border-t border-line/80 pb-8 pt-5 sm:mt-14">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div className="max-w-[450px]">
          <p className="text-[9.5px] leading-4 text-faint">
            Suna Studio is an open DevSnips template, built for Suna AI. Audio
            is generated on the public{" "}
            <a
              href={SUNA_SPACE_URL}
              target="_blank"
              rel="noreferrer"
              className="underline decoration-line-strong underline-offset-2 transition hover:text-muted"
            >
              Hugging Face Space
            </a>
            . This app does not store audio or prompts; tracks live in this tab
            until you close it.
          </p>
          <p className="mt-2 font-mono text-[8px] uppercase tracking-[0.14em] text-faint/80">
            Session media is served by {SUNA_SPACE_ID}
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-x-4 gap-y-2">
          <a
            href={SUNA_SITE_URL}
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-1 text-[9px] font-medium text-muted transition hover:text-ink"
          >
            Suna AI
            <Icon name="arrow-up-right" size={10} />
          </a>
          <a
            href={SUNA_SPACE_URL}
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-1 text-[9px] font-medium text-muted transition hover:text-ink"
          >
            The Space
            <Icon name="arrow-up-right" size={10} />
          </a>
          <a
            href={DEVSNIPS_URL}
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-1 text-[9px] font-medium text-muted transition hover:text-ink"
          >
            DevSnips
            <Icon name="arrow-up-right" size={10} />
          </a>
        </div>
      </div>
    </footer>
  );
}

function NoticeToast() {
  const { notice, dismissNotice } = useStudio();
  if (!notice) return null;

  const tone =
    notice.tone === "success"
      ? "border-sage/50 bg-sage-soft text-ink"
      : notice.tone === "error"
        ? "border-accent/30 bg-accent-soft text-accent-deep"
        : "border-line bg-surface text-ink-2";

  return (
    <div className="pointer-events-none fixed inset-x-0 bottom-[calc(76px+env(safe-area-inset-bottom)+0.75rem)] z-[60] flex justify-center px-4 lg:bottom-[100px]">
      <div
        role="status"
        aria-live="polite"
        className={`pointer-events-auto flex max-w-[92vw] items-center gap-2 rounded-full border px-3.5 py-2 text-[10.5px] font-medium shadow-lift backdrop-blur animate-fade-up ${tone}`}
      >
        <Icon
          name={
            notice.tone === "success"
              ? "check"
              : notice.tone === "error"
                ? "alert"
                : "info"
          }
          size={13}
          className="shrink-0"
        />
        <span className="min-w-0">{notice.message}</span>
        <button
          type="button"
          onClick={dismissNotice}
          aria-label="Dismiss notification"
          className="ml-1 grid h-5 w-5 shrink-0 place-items-center rounded-full opacity-55 transition hover:bg-black/5 hover:opacity-100"
        >
          <Icon name="close" size={11} />
        </button>
      </div>
    </div>
  );
}

export default function App() {
  const { tracks } = useStudio();
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <div className="min-h-dvh bg-paper text-ink">
      <a
        href="#main"
        className="fixed left-4 top-4 z-[100] -translate-y-24 rounded-full bg-ink px-4 py-2 text-[11px] font-medium text-cream transition focus:translate-y-0"
      >
        Skip to content
      </a>

      <div className="mx-auto flex min-h-dvh w-full max-w-[1600px]">
        <Sidebar onNewTrack={focusComposer} />

        <div className="flex min-w-0 flex-1 flex-col">
          <TopBar onOpenMenu={() => setMenuOpen(true)} />

          <main
            id="main"
            tabIndex={-1}
            className="flex-1 pb-[calc(82px+env(safe-area-inset-bottom))] focus:outline-none lg:pb-[104px]"
          >
            <div className="mx-auto w-full max-w-[780px] px-4 sm:px-6 lg:px-8">
              <Hero />
              <div className="mt-6 sm:mt-7">
                <Composer />
                <GenerationPanel />
              </div>
              <SessionFeed tracks={tracks} />
              <Footer />
            </div>
          </main>
        </div>

        <aside className="sticky top-0 hidden h-[calc(100dvh-84px)] w-[308px] shrink-0 border-l border-line/80 min-[1360px]:block">
          <div className="h-full overflow-y-auto px-5 py-6">
            <NowPlaying />
          </div>
        </aside>
      </div>

      <MobileDrawer
        open={menuOpen}
        onClose={() => setMenuOpen(false)}
        onNewTrack={focusComposer}
      />
      <PlayerBar />
      <NoticeToast />
    </div>
  );
}
